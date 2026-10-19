// Explicit full-map diagnostic renderer. Uses donor material/quad/atlas/fan
// conventions and Qud's own sprite component for conservative original fallback.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using HarmonyLib;
using Kobold;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using UnityEngine;
using UnityEngine.Rendering;

namespace RenderingTransplantProbe
{
    public sealed class JoppaRenderer : IDisposable
    {
        const float CellWidth=2f/3f;
        readonly AssetBundle bundle;
        readonly Dictionary<string,Shader> shaders;
        readonly Dictionary<string,Texture2D> textures=new Dictionary<string,Texture2D>();
        readonly Dictionary<string,Material> materials=new Dictionary<string,Material>();
        readonly Camera camera;
        readonly RenderTexture target;
        public RenderTexture Texture { get { return target; } }
        public bool[] Covered { get; private set; }
        readonly MethodInfo flush=AccessTools.Method(typeof(exStandaloneSprite),"LateUpdate");
        readonly List<UnityEngine.Object> scene=new List<UnityEngine.Object>();
        readonly Dictionary<Material,Geometry> groups=new Dictionary<Material,Geometry>();
        sealed class Geometry
        {
            public readonly List<Vector3> Vertices=new List<Vector3>();
            public readonly List<Vector3> UV=new List<Vector3>();
            public readonly List<Color32> Colors=new List<Color32>();
            public readonly List<int> Triangles=new List<int>();
        }
        public JoppaRenderer()
        {
            bundle=AssetBundle.LoadFromFile(Path.Combine(ProbeRunner.Root,"donor","donor-shaders.bundle"));
            if(bundle==null)throw new InvalidDataException("Donor bundle failed to load");
            shaders=bundle.LoadAllAssets<Shader>().ToDictionary(s=>s.name);
            if(shaders.Count!=6 || shaders.Values.Any(s=>!s.isSupported))throw new InvalidDataException("Unsupported donor shader");
            target=new RenderTexture(1920,900,24,RenderTextureFormat.ARGB32,RenderTextureReadWrite.Linear);
            target.Create();
            var go=new UnityEngine.GameObject("RimQudOffscreenCamera");camera=go.AddComponent<Camera>();
            camera.enabled=false;camera.orthographic=true;camera.orthographicSize=12.5f;
            camera.transform.position=new Vector3(80*CellWidth/2,100,12.5f);
            camera.transform.rotation=Quaternion.LookRotation(Vector3.down,Vector3.forward);
            camera.nearClipPlane=.1f;camera.farClipPlane=150;
            camera.clearFlags=CameraClearFlags.SolidColor;camera.backgroundColor=new Color(.04f,.08f,.12f,1);
            camera.cullingMask=1<<30;camera.targetTexture=target;
            camera.transparencySortMode=TransparencySortMode.Orthographic;
        }
        Material Material(string shader,string filename,Color color)
        {
            string key=shader+"|"+filename+"|"+color;
            Material mat;if(materials.TryGetValue(key,out mat))return mat;
            Texture2D texture;
            if(!textures.TryGetValue(filename,out texture))
            {
                texture=new Texture2D(2,2,TextureFormat.RGBA32,true);
                if(!ImageConversion.LoadImage(texture,File.ReadAllBytes(Path.Combine(ProbeRunner.Root,"donor",filename))))
                    throw new InvalidDataException(filename);
                // Match the inspected donor textures: repeat, trilinear and mips.
                bool sprite=filename.StartsWith("human-") || filename.StartsWith("cat-") || filename.StartsWith("chair-");
                texture.wrapMode=sprite?TextureWrapMode.Clamp:TextureWrapMode.Repeat;texture.filterMode=UnityEngine.FilterMode.Trilinear;
                texture.anisoLevel=1;textures[filename]=texture;
            }
            mat=new Material(shaders[shader]);mat.mainTexture=texture;mat.SetColor("_Color",color);
            // Donor terrain drawing uses precedence-ordered materials. Explicit
            // queues preserve that order across independently grouped meshes.
            if(shader=="Custom/Terrain hard")mat.renderQueue=2000;
            if(shader.Contains("Terrain fade"))
                mat.renderQueue=filename=="sand.png"?2350:filename=="marsh.png"?2325:2340;
            if(shader.Contains("rough"))
            {
                var rough=Material("Custom/Terrain hard","rough.png",Color.white).mainTexture;
                mat.SetTexture("_AlphaAddTex",rough);
            }
            mat.SetFloat("_SwayHead",.35f);materials[key]=mat;return mat;
        }
        Geometry Group(Material mat)
        {
            Geometry group;if(!groups.TryGetValue(mat,out group)){group=new Geometry();groups[mat]=group;}return group;
        }
        static Vector3 Point(float x,float y,float altitude){return new Vector3(x*CellWidth,altitude,25-y);}
        void Quad(Material mat,float x,float y,float width=1,float height=1,float altitude=0,int atlas=-1,bool plant=false)
        {
            var g=Group(mat);int start=g.Vertices.Count;
            g.Vertices.Add(Point(x,y+height,altitude));g.Vertices.Add(Point(x,y,altitude+.0001f));
            g.Vertices.Add(Point(x+width,y,altitude+.0001f));g.Vertices.Add(Point(x+width,y+height,altitude));
            float scale=atlas<0?1:.1875f;
            float u=atlas<0?0:(atlas%4)*.25f+1f/32f,v=atlas<0?0:(atlas/4)*.25f+1f/32f;
            float phase=(int)(x*17+y*31)%1024;
            g.UV.Add(new Vector3(u,v,phase));g.UV.Add(new Vector3(u,v+scale,phase));
            g.UV.Add(new Vector3(u+scale,v+scale,phase));g.UV.Add(new Vector3(u+scale,v,phase));
            for(int i=0;i<4;i++)g.Colors.Add(new Color32(255,255,255,(byte)(plant && (i==0 || i==3)?0:255)));
            foreach(int index in new[]{0,1,2,0,2,3})g.Triangles.Add(start+index);
        }
        static bool CanMap(JoppaCell c)
        {
            return c.Visible && !c.RequiresOriginal && c.Kind!="original" &&
                (!PawnPresentation.IsLayered(c.Kind) || (!string.IsNullOrEmpty(c.GroundKind) && !c.Display.VFlip));
        }
        static string Ground(JoppaCell c){return PawnPresentation.IsLayered(c.Kind)?c.GroundKind:c.Kind;}
        static bool Is(JoppaFrame f,int x,int y,string kind)
        {
            if(x<0 || x>=80 || y<0 || y>=25)return false;
            var c=f.Cells[x+80*y];return CanMap(c) && (kind=="path"?Ground(c):c.Kind)==kind;
        }
        static bool Wet(JoppaFrame f,int x,int y)
        {
            if(x<0 || x>=80 || y<0 || y>=25)return false;
            var c=f.Cells[x+80*y];return c.Visible && !c.RequiresOriginal && c.WaterDepth>0;
        }
        Material WaterMaterial(int depth,bool feather=false)
        {
            // Original donor ramps, using the proven cutout/fade shaders rather
            // than claiming transplantation of RimWorld's WaterDepth pipeline.
            string file=depth>=3?"water-deep.png":"water-shallow.png";
            Color tint=depth>=3?new Color(.38f,.95f,1.3f,1):new Color(.65f,1.5f,1.5f,1);
            return Material(feather?"Custom/Terrain fade rough":"Custom/Cutout",file,tint);
        }
        void WaterSurface(JoppaFrame f,JoppaCell c)
        {
            bool s=Wet(f,c.X,c.Y+1),w=Wet(f,c.X-1,c.Y),n=Wet(f,c.X,c.Y-1),e=Wet(f,c.X+1,c.Y);
            float left=w?0:.08f,right=e?1:.92f,top=n?0:.08f,bottom=s?1:.92f;
            float[] px={.5f,left,left,left,.5f,right,right,right};
            float[] py={bottom,bottom,.5f,top,top,top,.5f,bottom};
            var g=Group(WaterMaterial(c.WaterDepth));int start=g.Vertices.Count;
            for(int i=0;i<9;i++)
            {
                float x=c.X+(i==8?.5f:px[i]),y=c.Y+(i==8?.5f:py[i]);
                g.Vertices.Add(Point(x,y,.025f));
                // World-continuous UV coordinates: neighboring cells do not
                // restart the water texture or draw a border at their shared edge.
                g.UV.Add(new Vector3(x*.17f,y*.17f,0));g.Colors.Add(new Color32(255,255,255,255));
            }
            for(int i=0;i<8;i++){g.Triangles.Add(start+i);g.Triangles.Add(start+(i+1)%8);g.Triangles.Add(start+8);}
        }
        // RimWorld's eight-neighbor terrain feather convention: side neighbors
        // light their side midpoint and both corners; diagonals light one corner.
        void PathTransition(JoppaFrame f,JoppaCell c,Material path,bool water=false)
        {
            int[] dx={0,-1,-1,-1,0,1,1,1},dy={1,1,0,-1,-1,-1,0,1};
            bool[] alpha=new bool[8];
            for(int i=0;i<8;i++)if(water?Wet(f,c.X+dx[i],c.Y+dy[i]):Is(f,c.X+dx[i],c.Y+dy[i],"path"))
            {
                alpha[i]=true;if(i%2==0){alpha[(i+7)%8]=true;alpha[(i+1)%8]=true;}
            }
            if(!alpha.Any(a=>a))return;
            float[] px={.5f,0,0,0,.5f,1,1,1},py={1,1,.5f,0,0,0,.5f,1};
            var g=Group(path);int start=g.Vertices.Count;
            for(int i=0;i<9;i++)
            {
                float x=c.X+(i==8?.5f:px[i]),y=c.Y+(i==8?.5f:py[i]);
                g.Vertices.Add(Point(x,y,water?.03f:.006f));g.UV.Add(new Vector3(x,y,0));
                g.Colors.Add(new Color32(255,255,255,(byte)(i<8 && alpha[i]?255:0)));
            }
            for(int i=0;i<8;i++){g.Triangles.Add(start+i);g.Triangles.Add(start+(i+1)%8);g.Triangles.Add(start+8);}
        }
        UnityEngine.GameObject Original(JoppaCell c)
        {
            ConsoleChar d=c.Display;
            string tile=d.Char=='\0'?d.Tile:"assets_content_textures_text_"+(int)d.Char+".bmp";
            if(string.IsNullOrEmpty(tile))tile="assets_content_textures_text_32.bmp";
            var go=SpriteManager.CreateSprite(tile);scene.Add(go);go.layer=30;
            var sprite=go.GetComponent<ex3DSprite2>();
            sprite.shader=SpriteManager.GetShaderMode(sprite.textureInfo.ShaderMode);
            sprite.color=d.Char=='\0'?d.Foreground:d.Background;
            sprite.backcolor=d.Char=='\0'?d.Background:d.Foreground;
            sprite.detailcolor=d.Char=='\0'?d.Detail:d.Foreground;
            go.transform.position=Point(c.X+.5f,c.Y+.5f,.3f+(25-c.Y)*.001f);
            go.transform.rotation=Quaternion.Euler(90,0,0);
            go.transform.localScale=new Vector3((d.HFlip?-1:1)/24f,(d.VFlip?-1:1)/24f,1f/24f);
            flush.Invoke(sprite,null);
            return go;
        }
        static float ForegroundDepth(JoppaCell c,float original)
        {
            // Mapped foreground sorts by its ground contact row, not image height.
            return PawnPresentation.Enabled?.2f+c.Y*.002f:original;
        }
        void SpriteLayer(Transform parent,Material material,float width,float height,float x,float z,float layer)
        {
            float w=width*CellWidth;var mesh=new Mesh();scene.Add(mesh);
            mesh.vertices=new[]{new Vector3(x*CellWidth-w/2,layer,z-height/2),new Vector3(x*CellWidth-w/2,layer,z+height/2),
                new Vector3(x*CellWidth+w/2,layer,z+height/2),new Vector3(x*CellWidth+w/2,layer,z-height/2)};
            mesh.uv=new[]{new Vector2(0,0),new Vector2(0,1),new Vector2(1,1),new Vector2(1,0)};
            mesh.triangles=new[]{0,1,2,0,2,3};mesh.RecalculateBounds();
            var go=new UnityEngine.GameObject("RimQudSpriteLayer");scene.Add(go);go.layer=30;
            go.transform.SetParent(parent,false);go.AddComponent<MeshFilter>().sharedMesh=mesh;
            var renderer=go.AddComponent<MeshRenderer>();renderer.sharedMaterial=material;
            renderer.shadowCastingMode=ShadowCastingMode.Off;renderer.receiveShadows=false;
        }
        void Foreground(JoppaCell c)
        {
            string direction=c.Facing==0?"north":c.Facing==2?"south":"east";
            var go=new UnityEngine.GameObject("RimQudForeground:"+c.Instance);scene.Add(go);go.layer=30;
            go.transform.position=Point(c.X+.5f,c.Y+.86f,ForegroundDepth(c,.2f));
            bool flip=(c.Facing==3)^c.Display.HFlip;go.transform.localScale=new Vector3(flip?-1:1,1,1);
            if(c.Kind=="human")
            {
                // Donor Male body: 1 x .9 graphic scale; head offset (.04,.34).
                const float scale=1.2f,bodyHeight=1.35f*scale;
                float center=(108f/128f-.5f)*bodyHeight;
                Color skin=new Color(.82f,.69f,.55f,1)*c.Display.Foreground;
                SpriteLayer(go.transform,Material("Custom/Cutout","human-body-"+direction+".png",skin),1.5f*scale,bodyHeight,0,center,0);
                SpriteLayer(go.transform,Material("Custom/Cutout","human-head-"+direction+".png",skin),1.5f*scale,1.5f*scale,
                    c.Facing==1 || c.Facing==3?.04f*scale:0,center+.34f*scale,.001f);
            }
            else
            {
                bool animal=c.Kind=="animal";float size=animal?.9f:1.15f;
                string file=(animal?"cat-":"chair-")+direction+".png";
                // Explicit alpha-bound feet anchors from the extracted donor images.
                float bottom=animal?(c.Facing==0?60:c.Facing==2?61:52):(c.Facing==0?61:c.Facing==2?62:60);
                Color tint=(animal?Color.white:new Color(.62f,.45f,.28f,1))*c.Display.Foreground;
                SpriteLayer(go.transform,Material("Custom/Cutout",file,tint),size,size,0,(bottom/64f-.5f)*size,0);
            }
        }
        void FlushGeometry()
        {
            foreach(var entry in groups)
            {
                var mesh=new Mesh();scene.Add(mesh);mesh.indexFormat=IndexFormat.UInt32;
                mesh.SetVertices(entry.Value.Vertices);mesh.SetUVs(0,entry.Value.UV);
                mesh.SetColors(entry.Value.Colors);mesh.SetTriangles(entry.Value.Triangles,0);mesh.RecalculateBounds();
                var go=new UnityEngine.GameObject("RimQudMaterialGroup");scene.Add(go);go.layer=30;
                go.AddComponent<MeshFilter>().sharedMesh=mesh;
                var renderer=go.AddComponent<MeshRenderer>();renderer.sharedMaterial=entry.Key;
                renderer.shadowCastingMode=ShadowCastingMode.Off;renderer.receiveShadows=false;
            }
        }
        string Capture(string name)
        {
            camera.Render();var previous=RenderTexture.active;RenderTexture.active=target;
            var image=new Texture2D(target.width,target.height,TextureFormat.RGBA32,false,true);
            try
            {
                image.ReadPixels(new Rect(0,0,target.width,target.height),0,0);image.Apply();
                string file="joppa-"+name+".png";File.WriteAllBytes(Path.Combine(ProbeRunner.Root,file),image.EncodeToPNG());return file;
            }
            finally{RenderTexture.active=previous;UnityEngine.Object.DestroyImmediate(image);}
        }
        public JObject Draw(JoppaFrame frame,bool live=false)
        {
            var clock=System.Diagnostics.Stopwatch.StartNew();
            var originals=new UnityEngine.GameObject[2000];var counts=new Dictionary<string,int>();
            var masks=new int[16];var rows=new JArray();int grass=0,water=0,shallow=0,deep=0;
            bool eligible=frame.Enabled && frame.View==frame.ExpectedView && frame.Zone=="JoppaWorld.11.22.1.1.10";
            Covered=new bool[2000];
            try
            {
                camera.backgroundColor=live?Color.clear:new Color(.04f,.08f,.12f,1);
                Shader.SetGlobalFloat("_FallIntensity",0);Shader.SetGlobalVector("_FallGlobalControls",Vector4.zero);
                if(!live)foreach(var cell in frame.Cells)originals[cell.X+80*cell.Y]=Original(cell);
                string original=live?null:Capture(frame.Phase+"-original");
                foreach(var c in frame.Cells)
                {
                    bool mapped=eligible && CanMap(c);
                    bool waterLayer=eligible && Wet(frame,c.X,c.Y);
                    Covered[c.X+80*c.Y]=mapped || waterLayer;
                    if(waterLayer)
                    {
                        WaterSurface(frame,c);water++;if(c.WaterDepth>=3)deep++;else shallow++;
                        if(!mapped)
                        {
                            // Scoped liquid-underlay adapter: keep the native
                            // foreground/detail silhouette while exposing water.
                            if(live)originals[c.X+80*c.Y]=Original(c);
                            var sprite=originals[c.X+80*c.Y].GetComponent<ex3DSprite2>();
                            sprite.backcolor=Color.clear;flush.Invoke(sprite,null);
                        }
                    }
                    if(mapped)
                    {
                        if(!counts.ContainsKey(c.Kind))counts[c.Kind]=0;counts[c.Kind]++;
                        if(!live)originals[c.X+80*c.Y].SetActive(false);
                        string ground=Ground(c);
                        bool marsh=ground=="ground" || ground=="tree" || ground=="reed" || ground=="water";
                        Quad(Material("Custom/Terrain fade rough",marsh?"marsh.png":"soil.png",
                            Color.white),c.X,c.Y);
                        var pathTint=Color.white;
                        if(ground=="path")Quad(Material("Custom/Terrain fade rough","sand.png",pathTint),c.X,c.Y,altitude:.005f);
                        if(ground=="ground")PathTransition(frame,c,Material("Custom/Terrain fade rough","sand.png",pathTint));
                        if(ground=="ground")PathTransition(frame,c,WaterMaterial(2,true),true);
                        if(ground=="ground" && c.Grass)
                        {
                            float dx=((c.X*13+c.Y*7)%11-5)*.02f,dy=((c.X*3+c.Y*17)%11-5)*.02f;
                            Quad(Material("Custom/Plant cutout","grass.png",Color.white),c.X+.1f+dx,c.Y+.1f+dy,.8f,.8f,.12f,plant:true);grass++;
                        }
                        if(c.Kind=="wall")
                        {
                            int mask=(Is(frame,c.X,c.Y-1,"wall")?1:0)|(Is(frame,c.X+1,c.Y,"wall")?2:0)|
                                (Is(frame,c.X,c.Y+1,"wall")?4:0)|(Is(frame,c.X-1,c.Y,"wall")?8:0);
                            masks[mask]++;Quad(Material("Custom/Cutout","wall.png",new Color(.75f,.68f,.48f,1)),c.X,c.Y,altitude:ForegroundDepth(c,.1f),atlas:mask);
                        }
                        if(c.Kind=="door")Quad(Material("Custom/Cutout","door.png",Color.white),c.X,c.Y,altitude:ForegroundDepth(c,.11f));
                        if(PawnPresentation.IsLayered(c.Kind))Foreground(c);
                        if(c.Kind=="crop" || c.Kind=="reed" || c.Kind=="tree")
                        {
                            string texture=c.Kind=="crop"?"crop.png":c.Kind=="reed"?"reed.png":"plant.png";
                            float size=c.Kind=="tree"?2f:1f;
                            Quad(Material("Custom/Plant cutout",texture,Color.white),c.X-(size-1)/2,c.Y-(size-1),size,size,
                                ForegroundDepth(c,.15f+(25-c.Y)*.002f),plant:true);
                        }
                    }
                    var binding=live && PawnPresentation.IsLayered(c.Kind)?
                        GameManager.Instance.ConsoleCharacter[c.X,c.Y].GetComponent<TileBehavior>():null;
                    var screen=live && PawnPresentation.IsLayered(c.Kind)?GameManager.Instance.getScreenTileCenter(c.X,c.Y):Vector3.zero;
                    rows.Add(new JObject{{"x",c.X},{"y",c.Y},{"source",c.Source},{"kind",c.Kind},
                        {"instance",c.Instance},{"facing",c.Facing},{"groundKind",c.GroundKind},
                        {"foregroundLayers",mapped?(c.Kind=="human"?2:PawnPresentation.IsLayered(c.Kind)?1:0):0},
                        {"feetX",c.X+.5f},{"feetY",c.Y+.86f},
                        {"foregroundDepth",ForegroundDepth(c,.2f)},
                        {"foregroundColor",new JArray(c.Display.Foreground.r,c.Display.Foreground.g,c.Display.Foreground.b,c.Display.Foreground.a)},
                        {"inputX",binding==null?-1:binding.x},{"inputY",binding==null?-1:binding.y},
                        {"nativeInputEnabled",binding!=null && binding.enabled && binding.GetComponents<Collider>().Any(collider=>collider.enabled)},
                        {"screenX",screen.x},{"screenY",screen.y},
                        {"visible",c.Visible},{"requiresOriginal",c.RequiresOriginal},{"mapped",mapped},
                        {"nativeGrassPaint",c.Grass},{"grassDrawn",mapped && c.Kind=="ground" && c.Grass},
                        {"waterDepth",c.WaterDepth},{"waterVolume",c.WaterVolume},{"waterLayer",waterLayer}});
                }
                FlushGeometry();string replacement=null;
                if(live)camera.Render();else replacement=Capture(frame.Phase+"-replacement");clock.Stop();
                return JObject.FromObject(new{phase=frame.Phase,generation=frame.Generation,original,replacement,
                    enabled=frame.Enabled,eligible,zone=frame.Zone,mappedByKind=counts,wallMasks=masks,
                    grassClumps=grass,waterLayerCells=water,shallowWaterCells=shallow,deepWaterCells=deep,
                    originalFallbackCells=2000-counts.Values.Sum(),offscreenMilliseconds=clock.Elapsed.TotalMilliseconds,
                    materialGroups=groups.Count,cells=rows});
            }
            finally
            {
                for(int i=scene.Count-1;i>=0;i--)if(scene[i]!=null)UnityEngine.Object.DestroyImmediate(scene[i]);
                scene.Clear();groups.Clear();
            }
        }
        public void Dispose()
        {
            foreach(var mat in materials.Values)UnityEngine.Object.DestroyImmediate(mat);
            foreach(var texture in textures.Values)UnityEngine.Object.DestroyImmediate(texture);
            target.Release();UnityEngine.Object.DestroyImmediate(target);
            UnityEngine.Object.DestroyImmediate(camera.gameObject);bundle.Unload(true);
        }
    }
}
