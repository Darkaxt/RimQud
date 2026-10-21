// Renderer-only bridge to the user's installed CAI5000 fog shader.
// Its AI, faction sight grids and simulation are not loaded into Qud.
using System;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using UnityEngine;

namespace RenderingTransplantProbe
{
    public sealed class CaiFog : IDisposable
    {
        readonly AssetBundle bundle;
        readonly Shader shader;
        readonly Texture2D texture;
        public CaiFog()
        {
            string path=Path.Combine(ProbeRunner.Root,"donor/cai-fog.bundle");
            var receipt=JObject.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"donor/cai-fog-source.json")));
            using(var sha=System.Security.Cryptography.SHA256.Create())
                if(BitConverter.ToString(sha.ComputeHash(File.ReadAllBytes(path))).Replace("-","").ToLowerInvariant()!=(string)receipt["sha256"])
                    throw new InvalidDataException("Changed installed CAI fog shader");
            bundle=AssetBundle.LoadFromFile(path);
            if(bundle==null)throw new InvalidDataException("Installed CAI fog bundle could not load in this Unity build");
            shader=bundle.LoadAsset<Shader>("assets/fogshader.shader");
            if(shader==null || !shader.isSupported)throw new InvalidDataException("Installed CAI fog shader is unsupported");
            texture=new Texture2D(16,16,TextureFormat.RGBAFloat,true,true);texture.Apply();
            ProbeRunner.Record("current-fog-shader.json",new{shader=shader.name,supported=shader.isSupported,
                source="Installed CAI5000 Resources/Bundles/StandaloneWindows/isma",sourceSha256=(string)receipt["sha256"],
                modUrl=(string)receipt["url"],nativeVisibilityOwner="Qud",sectionSize=16});
        }
        public void Draw(JoppaFrame frame,Action<UnityEngine.Object> retain)
        {
            int visible=0,remembered=0,unknown=0;
            foreach(var cell in frame.Cells){if(cell.Visible)visible++;else if(cell.Explored)remembered++;else unknown++;}
            for(int sx=0;sx<5;sx++)for(int sz=0;sz<2;sz++)
            {
                var grid=new float[256];
                for(int x=0;x<16;x++)for(int z=0;z<16;z++)
                {
                    int cx=sx*16+x,cy=24-(sz*16+z);
                    if(cy<0 || cy>=25){grid[x*16+z]=1;continue;}
                    var cell=frame.Cells[cx+80*cy];
                    grid[x*16+z]=cell.Visible?0:cell.Explored?.65f:1;
                }
                var mat=new Material(shader);retain(mat);mat.renderQueue=4000;
                mat.SetVector("_Color",new Vector4(.1f,.1f,.1f,.8f));mat.SetTexture("_Tex",texture);mat.SetFloatArray("_Fog",grid);
                var mesh=new Mesh();retain(mesh);
                mesh.vertices=new[]{new Vector3(0,0,0),new Vector3(0,0,16),new Vector3(16,0,16),new Vector3(16,0,0)};
                mesh.uv=new[]{new Vector2(0,0),new Vector2(0,1),new Vector2(1,1),new Vector2(1,0)};
                mesh.triangles=new[]{0,1,2,0,2,3};mesh.RecalculateBounds();
                var go=new UnityEngine.GameObject("RimQudCAIFogSection");retain(go);go.layer=30;
                go.transform.position=new Vector3(sx*16*(2f/3f),2,sz*16);go.transform.localScale=new Vector3(2f/3f,1,1);
                go.AddComponent<MeshFilter>().sharedMesh=mesh;go.AddComponent<MeshRenderer>().sharedMaterial=mat;
            }
            ProbeRunner.Record("current-fog-"+frame.Phase+".json",new{visible,remembered,unknown,shader=shader.name,
                nativeVisibility=true,nativeExploration=true,hiddenObjectQueries=false});
        }
        public void Dispose(){UnityEngine.Object.DestroyImmediate(texture);bundle.Unload(true);}
    }
}
