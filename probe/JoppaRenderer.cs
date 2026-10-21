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
        sealed class Impact { public int Serial;public double Started;public Vector2 Offset;public bool Finished;public float AppliedTicks; }
        readonly Dictionary<int,Impact> impacts=new Dictionary<int,Impact>();
        readonly Dictionary<int,Transform> actors=new Dictionary<int,Transform>();
        readonly Dictionary<int,Vector3> anchors=new Dictionary<int,Vector3>();
        int world=-1;
        bool retained;
        static double Now { get { return (double)System.Diagnostics.Stopwatch.GetTimestamp()/System.Diagnostics.Stopwatch.Frequency; } }
        static float Ticks(Impact impact){return (float)((Now-impact.Started)*60);}
        public JObject VisualState(int id)
        {
            Impact impact;Transform actor;
            if(!impacts.TryGetValue(id,out impact) || !actors.TryGetValue(id,out actor))return null;
            float ticks=impact.AppliedTicks;var offset=actor.position-anchors[id];
            var block=new MaterialPropertyBlock();var layer=actor.GetComponentInChildren<MeshRenderer>();layer.GetPropertyBlock(block);
            Color color=block.GetColor("_Color");
            var layers=new JArray();
            foreach(var renderer in actor.GetComponentsInChildren<MeshRenderer>())
            {
                var properties=new MaterialPropertyBlock();renderer.GetPropertyBlock(properties);var applied=properties.GetColor("_Color");
                layers.Add(new JObject{{"name",renderer.name},{"color",new JArray(applied.r,applied.g,applied.b,applied.a)}});
            }
            return new JObject{{"instance",id},{"serial",impact.Serial},{"visualTicks",ticks},{"layers",layers},
                {"offsetX",offset.x/CellWidth},{"offsetY",-offset.z},
                {"color",new JArray(color.r,color.g,color.b,color.a)},{"finished",impact.Finished},
                {"world",world}};
        }
        bool ApplyImpact(int id,Transform actor)
        {
            Impact impact;if(!impacts.TryGetValue(id,out impact))return false;
            float ticks=Ticks(impact),amount=Mathf.Clamp01(1-ticks/16);
            impact.AppliedTicks=ticks;
            Vector2 offset=impact.Offset;
            offset=offset.normalized*Mathf.Max(0,offset.magnitude-.018f*ticks);
            actor.position=anchors[id]+new Vector3(offset.x*CellWidth,0,-offset.y);
            foreach(var layer in actor.GetComponentsInChildren<MeshRenderer>())
            {
                var block=new MaterialPropertyBlock();
                block.SetColor("_Color",Color.Lerp(layer.sharedMaterial.GetColor("_Color"),Color.red,amount));
                layer.SetPropertyBlock(block);
            }
            bool changed=!impact.Finished;impact.Finished=amount==0;return changed;
        }
        public void TickVisuals()
        {
            if(!retained)return;
            bool changed=false;foreach(var pair in actors)changed=ApplyImpact(pair.Key,pair.Value) || changed;
            if(changed)camera.Render();
            GameplayProbe.ObserveReaction(this);
        }
        void ClearScene()
        {
            for(int i=scene.Count-1;i>=0;i--)if(scene[i]!=null)UnityEngine.Object.DestroyImmediate(scene[i]);
            scene.Clear();groups.Clear();actors.Clear();anchors.Clear();retained=false;
        }
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
            filename=VillageArt.Surface(filename);
            string key=shader+"|"+filename+"|"+color;
            Material mat;if(materials.TryGetValue(key,out mat))return mat;
            Texture2D texture;
            if(!textures.TryGetValue(filename,out texture))
            {
                if(filename.StartsWith("current:"))texture=CurrentArt.Texture(filename);
                else if(filename.StartsWith("current-source:"))texture=CurrentArt.SourceTexture(filename.Substring(15),true);
                else
                {
                texture=new Texture2D(2,2,TextureFormat.RGBA32,true);
                if(!ImageConversion.LoadImage(texture,File.ReadAllBytes(Path.Combine(ProbeRunner.Root,"donor",filename))))
                    throw new InvalidDataException(filename);
                // Match the inspected donor textures: repeat, trilinear and mips.
                bool sprite=filename.StartsWith("village-") && !filename.StartsWith("village-surface-") || filename.StartsWith("dromad-") || filename.StartsWith("human-") || filename.StartsWith("cat-") || filename.StartsWith("faithful-cat-") || filename.StartsWith("chair-") ||
                    filename.StartsWith("prop-") || filename.StartsWith("worn-") || filename.StartsWith("held-");
                texture.wrapMode=sprite?TextureWrapMode.Clamp:TextureWrapMode.Repeat;texture.filterMode=UnityEngine.FilterMode.Trilinear;
                texture.anisoLevel=1;textures[filename]=texture;
                texture.name=filename;
                }
                textures[filename]=texture;
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
            if(CurrentArt.Enabled)return CurrentArt.CanMap(c);
            return c.Visible && !c.RequiresOriginal && c.Kind!="original" && CtesiphusArt.Failure(c)==null &&
                (!JoppaCoverage.Enabled || !c.Display.VFlip) &&
                (!PawnPresentation.IsLayered(c.Kind) || (!string.IsNullOrEmpty(c.GroundKind) && !c.Display.VFlip));
        }
        static string Ground(JoppaCell c){return (PawnPresentation.IsLayered(c.Kind) || JoppaCoverage.Enabled && !string.IsNullOrEmpty(c.GroundKind))?c.GroundKind:c.Kind;}
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
        static bool Linked(JoppaFrame f,int x,int y,string kind)
        {
            if(x<0 || x>=80 || y<0 || y>=25)return false;
            var c=f.Cells[x+80*y];return c.Visible && !c.RequiresOriginal &&
                (c.Kind==kind || kind=="wall" && c.Source=="BrinestalkWallWithGearbox");
        }
        static int LinkMask(JoppaFrame f,JoppaCell c,string kind)
        {
            return (Linked(f,c.X,c.Y-1,kind)?1:0)|(Linked(f,c.X+1,c.Y,kind)?2:0)|
                (Linked(f,c.X,c.Y+1,kind)?4:0)|(Linked(f,c.X-1,c.Y,kind)?8:0);
        }
        Material WaterMaterial(int depth,bool feather=false)
        {
            // Original donor ramps, using the proven cutout/fade shaders rather
            // than claiming transplantation of RimWorld's WaterDepth pipeline.
            string file=depth>=3?"water-deep.png":"water-shallow.png";
            Color tint=depth>=3?new Color(.38f,.95f,1.3f,1):new Color(.65f,1.5f,1.5f,1);
            if(VillageArt.Enabled)tint=Color.white;
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
            return PawnPresentation.Enabled || JoppaCoverage.Enabled?.2f+c.Y*.002f:original;
        }
        MeshRenderer SpriteLayer(Transform parent,Material material,float width,float height,float x,float z,float layer)
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
            return renderer;
        }
        void Foreground(JoppaCell c)
        {
            string direction=c.Facing==0?"north":c.Facing==2?"south":"east";
            var go=new UnityEngine.GameObject("RimQudForeground:"+c.Instance);scene.Add(go);go.layer=30;
            go.transform.position=Point(c.X+.5f,c.Y+.86f,ForegroundDepth(c,.2f));
            bool flip=(!CurrentArt.Enabled && c.Facing==3)^c.Display.HFlip;go.transform.localScale=new Vector3(flip?-1:1,1,1);
            if(CurrentArt.Enabled)
            {
                var view=CurrentArt.ActorView(c);
                SpriteLayer(go.transform,Material("Custom/Cutout",CurrentArt.ActorTexture(c,view),CurrentArt.Lighting(c)),
                    (float)view["width"],(float)view["height"],(float)view["center_x"],(float)view["center_z"],0);
            }
            else if(VillageArt.Enabled && c.AssetFamily!=null && c.AssetFamily.StartsWith("village:"))
            {
                foreach(JObject part in VillageArt.Layers(c))
                {
                    var renderer=SpriteLayer(go.transform,Material("Custom/Cutout",(string)part["file"],VillageArt.Tint(c,part)),
                        (float)part["width"],(float)part["height"],(float)part["center_x"],(float)part["center_z"],(float)part["layer"]);
                    string equipmentKey=(string)part["equipment_key"];
                    renderer.name=equipmentKey==null?"RimQudVillage:"+(string)part["component"]:"RimQudEquipped:"+c.Equipment.Single(e=>e.Family==equipmentKey).Instance+":"+equipmentKey;
                }
            }
            else if(DromadArt.Enabled && c.AssetFamily=="dromad")
            {
                foreach(JObject part in DromadArt.View(c.Facing))
                {
                    string component=(string)part["component"],role=(string)part["color_role"];
                    var item=c.Equipment==null?null:c.Equipment.FirstOrDefault(e=>e.Family==component);
                    if(role=="equipment" && item==null)continue;
                    Color color=role=="detail"?c.Display.Detail:role=="equipment"?item.Color:c.Display.Foreground;
                    var renderer=SpriteLayer(go.transform,Material("Custom/Cutout",(string)part["file"],color),
                        (float)part["width"],(float)part["height"],(float)part["center_x"],(float)part["center_z"],(float)part["layer"]);
                    renderer.name=role=="equipment"?"RimQudEquipped:"+item.Instance+":"+item.Slot:"RimQudDromad:"+component;
                }
            }
            else if(c.Kind=="human")
            {
                // Donor Male body: 1 x .9 graphic scale; head offset (.04,.34).
                const float scale=1.2f,bodyHeight=1.35f*scale;
                float center=(108f/128f-.5f)*bodyHeight;
                Color skin=new Color(.82f,.69f,.55f,1)*c.Display.Foreground;
                SpriteLayer(go.transform,Material("Custom/Cutout","human-body-"+direction+".png",skin),1.5f*scale,bodyHeight,0,center,0);
                SpriteLayer(go.transform,Material("Custom/Cutout","human-head-"+direction+".png",skin),1.5f*scale,1.5f*scale,
                    c.Facing==1 || c.Facing==3?.04f*scale:0,center+.34f*scale,.001f);
                if(c.Equipment!=null)foreach(var item in c.Equipment)
                {
                    MeshRenderer layer;
                    if(item.Family=="sword")
                    {
                        layer=SpriteLayer(go.transform,Material("Custom/Cutout","held-sword.png",item.Color),.85f,.85f,0,0,c.Facing==0?-.0002f:.0016f);
                        layer.transform.localPosition=new Vector3(.34f*CellWidth,0,.30f);
                        layer.transform.localRotation=Quaternion.Euler(0,c.Facing==0?-45:c.Facing==2?45:0,0);
                    }
                    else
                    {
                        bool head=item.Slot=="Head";
                        layer=SpriteLayer(go.transform,Material("Custom/Cutout","worn-"+item.Family+"-"+direction+".png",item.Color),
                            1.5f*scale,head?1.5f*scale:bodyHeight,
                            head && (c.Facing==1 || c.Facing==3)?.04f*scale:0,center+(head?.34f*scale:0),item.Layer*.00002f);
                    }
                    layer.name="RimQudEquipped:"+item.Instance+":"+item.Slot;
                }
            }
            else if(CtesiphusArt.Enabled && c.Kind=="animal" && c.AssetFamily=="ray-cat")
            {
                var view=CtesiphusArt.View(c.Facing);
                SpriteLayer(go.transform,Material("Custom/Cutout",(string)view["file"],c.Display.Foreground),
                    (float)view["width"],(float)view["height"],(float)view["center_x"],(float)view["center_z"],0);
            }
            else if(JoppaCoverage.Enabled && c.Kind=="prop" && c.AssetFamily!="chair")
            {
                var asset=JoppaCoverage.Asset(c.AssetFamily);float width=(float)asset["width"],height=(float)asset["height"];
                string file="prop-"+c.AssetFamily+"-"+direction+".png";
                SpriteLayer(go.transform,Material("Custom/Cutout",file,c.Display.Foreground),width,height,
                    0,JoppaCoverage.Foot(file)*height,0);
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
            if(PawnPresentation.Stage>=2 && (c.Kind!="prop" || VillageArt.Enabled))
            {
                actors[c.Instance]=go.transform;anchors[c.Instance]=go.transform.position;
                Impact old=null;
                if(c.HurtSerial>0 && (!impacts.TryGetValue(c.Instance,out old) || old.Serial!=c.HurtSerial))
                {
                    Vector2 residual=old==null?Vector2.zero:old.Offset.normalized*Mathf.Max(0,old.Offset.magnitude-.018f*Ticks(old));
                    impacts[c.Instance]=new Impact{Serial=c.HurtSerial,
                        Offset=Vector2.ClampMagnitude(residual+new Vector2(c.HurtDX,c.HurtDY),.35f)};
                }
            }
        }
        int CurrentMask(JoppaFrame frame,JoppaCell cell,string domain)
        {
            int[] dx={0,1,1,1,0,-1,-1,-1},dy={-1,-1,0,1,1,1,0,-1};int mask=0;
            for(int i=0;i<8;i++)
            {
                int x=cell.X+dx[i],y=cell.Y+dy[i];if(x<0 || x>=80 || y<0 || y>=25)continue;
                var next=frame.Cells[x+80*y];
                if(next.Visible && !next.RequiresOriginal && (domain=="water"?next.WaterDepth>0:domain=="deep"?next.WaterDepth>=3:next.Source=="DirtPath" || next.GroundKind=="path"))mask|=1<<i;
            }
            return mask;
        }
        void CurrentCell(JoppaFrame frame,JoppaCell c)
        {
            var shade=CurrentArt.Lighting(c);
            // Retain source background and actual full-cell registration. No old
            // donor sand/grass/door recipe participates in this branch.
            Quad(Material("Custom/Cutout","current-source:white.png",c.Display.Background*shade),c.X,c.Y);
            bool water=c.WaterDepth>0;
            if(water)
            {
                int mask=CurrentMask(frame,c,"water");
                Color b=ConsoleLib.Console.ColorUtility.colorFromChar('b'),detail=ConsoleLib.Console.ColorUtility.colorFromChar('B');
                Quad(Material("Custom/Cutout",CurrentArt.Surface("shallow",c,mask),b*shade),c.X,c.Y,altitude:.01f);
                Quad(Material("Custom/Cutout",CurrentArt.Surface("shallow",c,mask,true),detail*shade),c.X,c.Y,altitude:.011f);
                if(c.WaterDepth>=3)
                {
                    int deep=CurrentMask(frame,c,"deep");
                    Quad(Material("Custom/Cutout",CurrentArt.Surface("swimming",c,deep),b*shade),c.X,c.Y,altitude:.012f);
                    Quad(Material("Custom/Cutout",CurrentArt.Surface("swimming",c,deep,true),detail*shade),c.X,c.Y,altitude:.013f);
                }
            }
            else if(c.Source=="DirtFloor" || c.GroundKind=="ground")
                Quad(Material("Custom/Cutout",CurrentArt.Surface("soil",c,255),ConsoleLib.Console.ColorUtility.colorFromChar('w')*shade),c.X,c.Y,altitude:.002f);
            if(c.Source=="DirtPath" || c.GroundKind=="path")
                Quad(Material("Custom/Cutout",CurrentArt.Surface("path",c,CurrentMask(frame,c,"path")),ConsoleLib.Console.ColorUtility.colorFromChar('w')*shade),c.X,c.Y,altitude:.005f);
            if((c.AssetFamily??"").StartsWith("current:NPC-"))Foreground(c);
            else
            {
                var ops=CurrentArt.Scenery(c)??CurrentArt.Data["paint"][CurrentArt.Canonical(c.Display.Tile)] as JArray;
                if(ops!=null)Quad(Material("Custom/Cutout",CurrentArt.Compose(c,ops,(c.Source??"paint")+"/"+c.Display.Tile+"/"+c.ConnectionMask),shade),
                    c.X,c.Y,altitude:ForegroundDepth(c,.2f));
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
            ClearScene();
            if(world!=frame.World){world=frame.World;impacts.Clear();}
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
                    bool waterLayer=eligible && !CurrentArt.Enabled && Wet(frame,c.X,c.Y);
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
                    if(mapped && CurrentArt.Enabled)
                    {
                        if(!counts.ContainsKey(c.Kind))counts[c.Kind]=0;counts[c.Kind]++;
                        if(!live)originals[c.X+80*c.Y].SetActive(false);
                        CurrentCell(frame,c);
                    }
                    else if(mapped)
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
                            int mask=JoppaCoverage.Enabled?LinkMask(frame,c,"wall"):(Is(frame,c.X,c.Y-1,"wall")?1:0)|(Is(frame,c.X+1,c.Y,"wall")?2:0)|
                                (Is(frame,c.X,c.Y+1,"wall")?4:0)|(Is(frame,c.X-1,c.Y,"wall")?8:0);
                            string file=JoppaCoverage.Enabled?(c.Source=="RustedMetalWall"?"wall-metal.png":"wall-planks.png"):"wall.png";
                            if(VillageArt.Enabled)file=VillageArt.Wall(c.Source)??file;
                            Color tint=JoppaCoverage.Enabled?c.Display.Foreground:new Color(.75f,.68f,.48f,1);
                            masks[mask]++;Quad(Material("Custom/Cutout",file,tint),c.X,c.Y,altitude:ForegroundDepth(c,.1f),atlas:mask);
                            if(VillageArt.Enabled && VillageArt.Wall(c.Source,true)!=null)
                                Quad(Material("Custom/Cutout",VillageArt.Wall(c.Source,true),c.Display.Detail),c.X,c.Y,altitude:ForegroundDepth(c,.1002f),atlas:mask);
                        }
                        if(c.Kind=="fence")Quad(Material("Custom/Cutout","fence.png",c.Display.Foreground),c.X,c.Y,
                            altitude:ForegroundDepth(c,.11f),atlas:LinkMask(frame,c,"fence"));
                        if(c.Kind=="bridge")Quad(Material("Custom/Cutout","bridge.png",c.Display.Foreground),c.X,c.Y,altitude:.04f);
                        if(VillageArt.Enabled && c.Kind=="fence")Quad(Material("Custom/Cutout","fence-detail.png",c.Display.Detail),c.X,c.Y,altitude:ForegroundDepth(c,.1102f),atlas:LinkMask(frame,c,"fence"));
                        if(VillageArt.Enabled && c.Kind=="bridge")
                        {
                            var detail=VillageArt.Scenery(c.Source)["views"]["south"].FirstOrDefault(p=>(string)p["color_role"]=="detail");
                            if(detail!=null)Quad(Material("Custom/Cutout",(string)detail["file"],c.Display.Detail),c.X,c.Y,altitude:.0402f);
                        }
                        if(c.Kind=="door")
                        {
                            float dx=0,dy=0;
                            if(c.DoorOpen)
                            {
                                if(Linked(frame,c.X-1,c.Y,"wall"))dx=-.65f;
                                else if(Linked(frame,c.X+1,c.Y,"wall"))dx=.65f;
                                else dy=Linked(frame,c.X,c.Y-1,"wall")?-.65f:.65f;
                            }
                            Quad(Material("Custom/Cutout","door.png",JoppaCoverage.Enabled?c.Display.Foreground:Color.white),c.X+dx,c.Y+dy,
                                altitude:ForegroundDepth(c,.11f)-(c.DoorOpen?.003f:0));
                            if(VillageArt.Enabled)
                            {
                                var detail=VillageArt.Scenery(c.Source)["views"]["south"].FirstOrDefault(p=>(string)p["color_role"]=="detail");
                                if(detail!=null)Quad(Material("Custom/Cutout",(string)detail["file"],c.Display.Detail),c.X+dx,c.Y+dy,altitude:ForegroundDepth(c,.1102f)-(c.DoorOpen?.003f:0));
                            }
                        }
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
                        {"art",ArtState(c,mapped)},{"artFallback",c.ArtFallback??CtesiphusArt.Failure(c)},
                        {"assetFamily",c.AssetFamily},{"doorOpen",c.DoorOpen},{"tile",c.Display.Tile},
                        {"bodyShape",c.BodyShape},{"apparelFallback",c.ApparelFallback},{"equipment",EquipmentRows(c.Equipment)},
                        {"detailColor",new JArray(c.Display.Detail.r,c.Display.Detail.g,c.Display.Detail.b,c.Display.Detail.a)},
                        {"hFlip",c.Display.HFlip},{"vFlip",c.Display.VFlip},
                        {"foregroundLayers",mapped && actors.ContainsKey(c.Instance)?actors[c.Instance].GetComponentsInChildren<MeshRenderer>().Length:
                            mapped?(c.Kind=="human"?2+(c.Equipment==null?0:c.Equipment.Length):PawnPresentation.IsLayered(c.Kind)?1:0):0},
                        {"feetX",c.X+.5f},{"feetY",c.Y+.86f},
                        {"foregroundDepth",ForegroundDepth(c,.2f)},
                        {"foregroundColor",new JArray(c.Display.Foreground.r,c.Display.Foreground.g,c.Display.Foreground.b,c.Display.Foreground.a)},
                        {"nativeChar",(int)c.Display.Char},{"backgroundColor",new JArray(c.Display.Background.r,c.Display.Background.g,c.Display.Background.b,c.Display.Background.a)},
                        {"inputX",binding==null?-1:binding.x},{"inputY",binding==null?-1:binding.y},
                        {"nativeInputEnabled",binding!=null && binding.enabled && binding.GetComponents<Collider>().Any(collider=>collider.enabled)},
                        {"screenX",screen.x},{"screenY",screen.y},
                        {"visible",c.Visible},{"requiresOriginal",c.RequiresOriginal},{"mapped",mapped},
                        {"nativeLight",c.NativeLight},{"currentArt",CurrentArt.Enabled && mapped},
                        {"pureWater",c.WaterPure},
                        {"nativeGrassPaint",c.Grass},{"grassDrawn",mapped && c.Kind=="ground" && c.Grass},
                        {"waterDepth",c.WaterDepth},{"waterVolume",c.WaterVolume},{"waterLayer",waterLayer}});
                }
                FlushGeometry();string replacement=null;
                foreach(var actor in actors)
                {
                    Impact impact;if(impacts.TryGetValue(actor.Key,out impact) && impact.Started==0)impact.Started=Now;
                    ApplyImpact(actor.Key,actor.Value);
                }
                if(live)camera.Render();else replacement=Capture(frame.Phase+"-replacement");clock.Stop();
                retained=live && PawnPresentation.Enabled && PawnPresentation.Stage>=2;
                return JObject.FromObject(new{phase=frame.Phase,generation=frame.Generation,world=frame.World,original,replacement,
                    enabled=frame.Enabled,eligible,zone=frame.Zone,mappedByKind=counts,wallMasks=masks,
                    grassClumps=grass,waterLayerCells=water,shallowWaterCells=shallow,deepWaterCells=deep,
                    originalFallbackCells=2000-counts.Values.Sum(),offscreenMilliseconds=clock.Elapsed.TotalMilliseconds,
                    materialGroups=groups.Count,cells=rows});
            }
            finally
            {
                if(!retained)ClearScene();
            }
        }
        public void Dispose()
        {
            ClearScene();impacts.Clear();
            foreach(var mat in materials.Values)UnityEngine.Object.DestroyImmediate(mat);
            foreach(var pair in textures)if(!pair.Key.StartsWith("current"))UnityEngine.Object.DestroyImmediate(pair.Value);
            CurrentArt.Dispose();
            target.Release();UnityEngine.Object.DestroyImmediate(target);
            UnityEngine.Object.DestroyImmediate(camera.gameObject);bundle.Unload(true);
        }
        JObject ArtState(JoppaCell c,bool mapped)
        {
            if(mapped && VillageArt.Enabled && c.AssetFamily!=null && c.AssetFamily.StartsWith("village:"))
            {
                Transform villageActor;if(!actors.TryGetValue(c.Instance,out villageActor))return null;var rows=new JArray();
                var parts=VillageArt.Layers(c).Cast<JObject>().ToArray();
                foreach(var layer in villageActor.GetComponentsInChildren<MeshRenderer>())
                {
                    var part=parts.Single(p=>(string)p["file"]==layer.sharedMaterial.mainTexture.name);
                    var villageVertices=layer.GetComponent<MeshFilter>().sharedMesh.vertices;
                    float villageU=(float)part["contact"][0]/(float)part["size"][0],villageV=1-(float)part["contact"][1]/(float)part["size"][1];
                    var villageContact=layer.transform.TransformPoint(villageVertices[0]+villageU*(villageVertices[3]-villageVertices[0])+villageV*(villageVertices[1]-villageVertices[0]));var color=layer.sharedMaterial.GetColor("_Color");
                    rows.Add(new JObject{{"name",layer.name},{"file",layer.sharedMaterial.mainTexture.name},{"role",part["color_role"]},{"equipmentKey",part["equipment_key"]},
                        {"contactX",villageContact.x/CellWidth},{"contactY",25-villageContact.z},{"width",(villageVertices[3]-villageVertices[0]).magnitude},{"height",(villageVertices[1]-villageVertices[0]).magnitude},
                        {"color",new JArray(color.r,color.g,color.b,color.a)},{"shader",layer.sharedMaterial.shader.name}});
                }
                return new JObject{{"family",c.AssetFamily},{"layers",rows}};
            }
            if(mapped && DromadArt.Enabled && c.AssetFamily=="dromad")
            {
                Transform dromadActor;if(!actors.TryGetValue(c.Instance,out dromadActor))return null;
                var layers=new JArray();
                foreach(var layer in dromadActor.GetComponentsInChildren<MeshRenderer>())
                {
                    var mesh=layer.GetComponent<MeshFilter>().sharedMesh;var dromadVertices=mesh.vertices;
                    var part=DromadArt.View(c.Facing).Cast<JObject>().Single(p=>(string)p["file"]==layer.sharedMaterial.mainTexture.name);
                    float contactU=DromadArt.Refined?(float)part["contact"][0]/(float)part["size"][0]:.5f;
                    float contactV=DromadArt.Refined?1-(float)part["contact"][1]/(float)part["size"][1]:1-296f/320;
                    var dromadContact=layer.transform.TransformPoint(dromadVertices[0]+contactU*(dromadVertices[3]-dromadVertices[0])+contactV*(dromadVertices[1]-dromadVertices[0]));
                    var color=layer.sharedMaterial.GetColor("_Color");
                    layers.Add(new JObject{{"name",layer.name},{"file",layer.sharedMaterial.mainTexture.name},
                        {"contactX",dromadContact.x/CellWidth},{"contactY",25-dromadContact.z},{"width",(dromadVertices[3]-dromadVertices[0]).magnitude},
                        {"height",(dromadVertices[1]-dromadVertices[0]).magnitude},{"altitude",dromadVertices[0].y},
                        {"color",new JArray(color.r,color.g,color.b,color.a)},
                        {"shader",layer.sharedMaterial.shader.name}});
                }
                return new JObject{{"family","dromad"},{"layers",layers}};
            }
            if(!mapped || !CtesiphusArt.Enabled || c.AssetFamily!="ray-cat")return null;
            Transform actor;if(!actors.TryGetValue(c.Instance,out actor))return null;
            var view=CtesiphusArt.View(c.Facing);var mf=actor.GetComponentInChildren<MeshFilter>();
            var vertices=mf.sharedMesh.vertices;var points=view["landmarks"];var size=view["size"];
            float u=(float)points["contact_x"]/(float)size[0],v=1-(float)points["contact_y"]/(float)size[1];
            var contact=mf.transform.TransformPoint(vertices[0]+u*(vertices[3]-vertices[0])+v*(vertices[1]-vertices[0]));
            var material=mf.GetComponent<MeshRenderer>().sharedMaterial;
            return new JObject{{"file",view["file"]},{"contactX",contact.x/CellWidth},{"contactY",25-contact.z},
                {"width",(vertices[3]-vertices[0]).magnitude/CellWidth},{"height",(vertices[1]-vertices[0]).magnitude},
                {"shader",material.shader.name},{"textureWidth",material.mainTexture.width},{"textureHeight",material.mainTexture.height}};
        }
        static JArray EquipmentRows(EquippedAppearance[] equipment)
        {
            var rows=new JArray();if(equipment==null)return rows;
            foreach(var item in equipment)rows.Add(new JObject{{"instance",item.Instance},{"blueprint",item.Blueprint},
                {"slot",item.Slot},{"family",item.Family},{"layer",item.Layer},{"colorCode",item.ColorCode},
                {"laterality",item.Laterality},{"detail",new JArray(item.Detail.r,item.Detail.g,item.Detail.b,item.Detail.a)},
                {"color",new JArray(item.Color.r,item.Color.g,item.Color.b,item.Color.a)}});
            return rows;
        }
    }
}
