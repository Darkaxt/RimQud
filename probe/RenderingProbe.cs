// Isolated diagnostic only. Activate with an explicit task-local profile and
// QUDEXPERIMENT_ROOT. Never installed in the user's normal mod directory.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using HarmonyLib;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Rendering;
using XRL.Core;

namespace RenderingTransplantProbe
{
    [HarmonyPatch(typeof(GameManager), "StartGameThread")]
    public static class ProbeBootstrap
    {
        static void Postfix(GameManager __instance)
        {
            string root = Environment.GetEnvironmentVariable("QUDEXPERIMENT_ROOT");
            if (string.IsNullOrEmpty(root)) return;
            if (!Path.GetFullPath(XRLCore.SavePath).StartsWith(Path.GetFullPath(root), StringComparison.OrdinalIgnoreCase))
                throw new InvalidOperationException("Probe refuses a non-isolated save path");
            AudioListener.pause = true;
            AudioListener.volume = 0f;
            __instance.gameObject.AddComponent<ProbeRunner>();
        }
    }

    public class ProbeRunner : MonoBehaviour
    {
        public static string Root { get { return Environment.GetEnvironmentVariable("QUDEXPERIMENT_ROOT"); } }
        public static void Record(string name, object value)
        {
            string path = Path.Combine(Root, name);
            File.WriteAllText(path, JsonConvert.SerializeObject(value, Formatting.Indented));
            Debug.Log("TRANSPLANT_PROBE " + name);
        }

        void Start()
        {
            int exit = 0;
            try
            {
                string mode = Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE");
                Record(mode == "capture" ? "runtime-capture.json" : "runtime.json", new { unity = Application.unityVersion,
                    graphics = SystemInfo.graphicsDeviceType.ToString(), gpu = SystemInfo.graphicsDeviceName,
                    renderPipeline = GraphicsSettings.currentRenderPipeline == null ? "BuiltIn" : GraphicsSettings.currentRenderPipeline.name,
                    thread = Thread.CurrentThread.ManagedThreadId, savePath = XRLCore.SavePath,
                    mode = Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE"),
                    audioPaused = AudioListener.pause, listenerVolume = AudioListener.volume,
                    masterVolume = SoundManager.MasterVolume, ambientVolume = XRL.UI.Options.AmbientVolume,
                    musicEnabled = XRL.UI.Options.Music, soundEnabled = XRL.UI.Options.Sound,
                    ambientEnabled = XRL.UI.Options.Ambient });
                if (!AudioListener.pause || AudioListener.volume != 0f || SoundManager.MasterVolume != 0f ||
                    XRL.UI.Options.Music || XRL.UI.Options.Sound || XRL.UI.Options.Ambient)
                    throw new InvalidOperationException("Isolated probe audio suppression was not applied");
                if (mode == "capture" || mode == "joppa" || mode == "gameplay" || mode == "review" || PawnPresentation.Enabled) return; // Core boot completion triggers simulation.
                ShaderExperiment();
            }
            catch (Exception ex)
            {
                exit = 1;
                Record("failure.json", new { exception = ex.ToString() });
                Debug.LogException(ex);
            }
            finally
            {
                string mode = Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE");
                if (mode != "capture" && mode != "joppa" && mode != "gameplay" && mode != "review" && !PawnPresentation.Enabled)
                {
                    Record("finished.json", new { exitCode = exit });
                    Application.Quit(exit);
                }
            }
        }

        bool captureQuit;
        void LateUpdate(){GameplayProbe.CaptureAfterLayout();}
        void Update()
        {
            GameplayProbe.ObserveView();
            if (!captureQuit && SceneCapture.Done)
            {
                captureQuit = true;
                Record("capture-finished.json", new { exitCode = SceneCapture.ExitCode });
                Application.Quit(SceneCapture.ExitCode);
            }
            if (!captureQuit && JoppaSimulation.Done)
            {
                captureQuit = true;
                JoppaSimulation.DisposeRenderer();
                Record("joppa-finished.json", new { exitCode = JoppaSimulation.ExitCode });
                Application.Quit(JoppaSimulation.ExitCode);
            }
            if (!captureQuit && GameplayProbe.Done)
            {
                captureQuit=true;
                GameplayProbe.DisposePresentation();
                JoppaSimulation.DisposeRenderer();
                Record("gameplay-finished.json",new{exitCode=GameplayProbe.ExitCode});
                Application.Quit(GameplayProbe.ExitCode);
            }
        }

        static Texture2D LoadTexture(string filename)
        {
            var tex = new Texture2D(2, 2, TextureFormat.RGBA32, false);
            if (!ImageConversion.LoadImage(tex, File.ReadAllBytes(Path.Combine(Root, "donor", filename))))
                throw new InvalidDataException("Texture decode failed: " + filename);
            tex.wrapMode = TextureWrapMode.Repeat;
            return tex;
        }

        void ShaderExperiment()
        {
            AssetBundle bundle = null;
            var textures = new List<Texture2D>();
            var objects = new List<UnityEngine.Object>();
            try
            {
                bundle = AssetBundle.LoadFromFile(Path.Combine(Root, "donor", "donor-shaders.bundle"));
                if (bundle == null) throw new InvalidDataException("Unity rejected the donor AssetBundle");
                Shader[] shaders = bundle.LoadAllAssets<Shader>();
                Record("loaded-shaders.json", shaders.Select(s => new { s.name, s.isSupported, passes = s.passCount }).ToArray());
                if (shaders.Length != 6) throw new InvalidDataException("Expected six donor shaders");
                var soil = LoadTexture("soil.png"); textures.Add(soil);
                var rough = LoadTexture("rough.png"); textures.Add(rough);
                var wall = LoadTexture("wall.png"); textures.Add(wall);
                var plant = LoadTexture("plant.png"); textures.Add(plant);
                var rt = new RenderTexture(128, 128, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.Linear);
                rt.Create(); objects.Add(rt);
                var cameraObject = new UnityEngine.GameObject("IsolatedDonorShaderCamera"); objects.Add(cameraObject);
                var camera = cameraObject.AddComponent<Camera>();
                camera.enabled = false;
                camera.orthographic = true; camera.orthographicSize = 0.72f;
                camera.transform.position = new Vector3(0, 10, 0);
                camera.transform.rotation = Quaternion.LookRotation(Vector3.down, Vector3.forward);
                camera.clearFlags = CameraClearFlags.SolidColor;
                camera.backgroundColor = new Color(0.04f, 0.08f, 0.12f, 1);
                camera.cullingMask = 1 << 30;
                camera.nearClipPlane = 0.1f; camera.farClipPlane = 30;
                camera.targetTexture = rt;
                var plane = new UnityEngine.GameObject("DonorPlane"); objects.Add(plane);
                plane.layer = 30;
                var filter = plane.AddComponent<MeshFilter>();
                var renderer = plane.AddComponent<MeshRenderer>();
                renderer.shadowCastingMode = ShadowCastingMode.Off; renderer.receiveShadows = false;
                var mesh = new Mesh(); objects.Add(mesh); filter.sharedMesh = mesh;
                // Printer_Plane vertex order, triangle winding, UV.z payload and
                // top-vertex altitude bias. No Qud/RimWorld simulation copied.
                mesh.vertices = new[] { new Vector3(-.5f,0,-.5f), new Vector3(-.5f,.01f,.5f),
                    new Vector3(.5f,.01f,.5f), new Vector3(.5f,0,-.5f) };
                mesh.triangles = new[] { 0,1,2,0,2,3 };
                mesh.SetUVs(0, new List<Vector3> { new Vector3(0,0,137),new Vector3(0,1,137),
                    new Vector3(1,1,137),new Vector3(1,0,137) });
                var results = new JArray();
                foreach (Shader shader in shaders)
                {
                    bool terrain = shader.name.Contains("Terrain");
                    bool vegetation = shader.name.Contains("Plant");
                    bool fade = shader.name.Contains("fade");
                    var mat = new Material(shader); objects.Add(mat);
                    mat.mainTexture = terrain ? soil : vegetation ? plant : wall;
                    mat.SetColor("_Color", Color.white);
                    if (shader.name.Contains("rough")) mat.SetTexture("_AlphaAddTex", rough);
                    if (!terrain && !vegetation)
                    {
                        mat.mainTextureScale = new Vector2(.1875f,.1875f);
                        mat.mainTextureOffset = new Vector2(1f/32f,1f/32f);
                    }
                    renderer.sharedMaterial = mat;
                    string key = shader.name.Replace('/', '_').Replace(' ', '_');
                    mesh.colors32 = new[] { new Color32(255,255,255,255),new Color32(255,255,255,255),
                        new Color32(255,255,255,255),new Color32(255,255,255,255) };
                    if (vegetation)
                        mesh.colors32 = new[] { new Color32(255,255,255,0),new Color32(255,255,255,255),
                            new Color32(255,255,255,255),new Color32(255,255,255,0) };
                    mat.SetFloat("_SwayHead", 0);
                    Shader.SetGlobalFloat("_FallIntensity", 0);
                    Shader.SetGlobalVector("_FallGlobalControls", Vector4.zero);
                    results.Add(ReadRender(camera, rt, key + "_base", shader));
                    if (fade)
                    {
                        mesh.colors32 = new[] { new Color32(255,255,255,0),new Color32(255,255,255,0),
                            new Color32(255,255,255,255),new Color32(255,255,255,255) };
                        results.Add(ReadRender(camera, rt, key + "_edge", shader));
                    }
                    else if (vegetation)
                    {
                        mat.SetFloat("_SwayHead", 1.5f);
                        results.Add(ReadRender(camera, rt, key + "_wind", shader));
                    }
                    else if (terrain)
                    {
                        mat.SetColor("_Color", new Color(.2f,.8f,.2f,1));
                        results.Add(ReadRender(camera, rt, key + "_tint", shader));
                    }
                }
                Record("shader-renders.json", results);
            }
            finally
            {
                foreach (var obj in objects) if (obj != null) UnityEngine.Object.DestroyImmediate(obj);
                foreach (var tex in textures) if (tex != null) UnityEngine.Object.DestroyImmediate(tex);
                if (bundle != null) bundle.Unload(true);
            }
        }

        static JObject ReadRender(Camera camera, RenderTexture rt, string key, Shader shader)
        {
            camera.Render();
            var old = RenderTexture.active;
            var image = new Texture2D(rt.width, rt.height, TextureFormat.RGBA32, false, true);
            try
            {
                RenderTexture.active = rt;
                image.ReadPixels(new Rect(0,0,rt.width,rt.height),0,0); image.Apply();
                Color32[] pixels = image.GetPixels32();
                int nonBackground = 0, pink = 0;
                Color32 bg = pixels[0];
                foreach (var p in pixels)
                {
                    if (Math.Abs(p.r-bg.r)+Math.Abs(p.g-bg.g)+Math.Abs(p.b-bg.b)>12) nonBackground++;
                    if (p.r>220 && p.b>220 && p.g<30) pink++;
                }
                byte[] png = image.EncodeToPNG();
                File.WriteAllBytes(Path.Combine(Root,key+".png"),png);
                return JObject.FromObject(new { test=key, shader=shader.name, supported=shader.isSupported,
                    nonBackgroundPixels=nonBackground, pinkPixels=pink, pngBytes=png.Length,
                    center=pixels[(rt.height/2)*rt.width+rt.width/2].ToString() });
            }
            finally { RenderTexture.active=old; UnityEngine.Object.DestroyImmediate(image); }
        }
    }
}
