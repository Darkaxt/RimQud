// Exact current-ledger bindings for the isolated Joppa test. No simulation owner.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using UnityEngine;
using XRL;
using XRL.Core;
using XRL.World;
using GO=XRL.World.GameObject;
using ColorUtility=ConsoleLib.Console.ColorUtility;

namespace RenderingTransplantProbe
{
    public static class CurrentArt
    {
        public static bool Enabled {get{return Environment.GetEnvironmentVariable("QUDEXPERIMENT_ART")=="current";}}
        static JObject data;
        public static JObject Data {get{if(data==null)
        {
            var value=JObject.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"selected/runtime/contract.json")));
            using(var sha=System.Security.Cryptography.SHA256.Create())
                foreach(var pair in new[]{new[]{"package.json","package_sha256"},new[]{"cast-v2.json","cast_sha256"}})
                {
                    string digest=BitConverter.ToString(sha.ComputeHash(File.ReadAllBytes(Path.Combine(ProbeRunner.Root,"selected",pair[0])))).Replace("-","").ToLowerInvariant();
                    if(digest!=(string)value[pair[1]])throw new InvalidDataException("Changed selected input "+pair[0]);
                }
            data=value;
        }return data;}}
        sealed class Seen {public GO Obj;public string Signature;}
        static readonly Dictionary<int,Seen> seen=new Dictionary<int,Seen>();
        static readonly Dictionary<string,Texture2D> images=new Dictionary<string,Texture2D>();
        static readonly Dictionary<string,Texture2D> composed=new Dictionary<string,Texture2D>();
        public static bool Night;
        public static bool Fog;
        public static Color Shade {get{return Night?new Color(.42f,.49f,.69f,1):Color.white;}}
        public static Color Lighting(JoppaCell cell){return Night && (!Fog || cell.NativeLight<200)?Shade:Color.white;}
        public static JObject Plant(JoppaCell cell){return cell.Source==null?null:Data["scenery"][cell.Source]?["plant"] as JObject;}
        public static string Canonical(string tile)
        {if(tile==null)return "";tile=tile.ToLowerInvariant();return tile.StartsWith("assets_content_textures_")?tile:"assets_content_textures_"+tile.Replace('/','_');}
        static string PartPath(XRL.World.Anatomy.BodyPart p)
        {return(p.ParentPart==null?"":PartPath(p.ParentPart)+">")+p.Type+"/"+p.VariantType+"/"+p.Laterality;}
        static string Key(string blueprint,string slot,int laterality)
        {return System.Text.RegularExpressions.Regex.Replace(blueprint.ToLowerInvariant(),"[^a-z0-9]+","-").Trim('-')+"@"+slot+"@"+laterality;}
        static Color Fore(GO obj){return ColorUtility.colorFromChar(ColorUtility.ParseForegroundColor(string.IsNullOrEmpty(obj.Render.TileColor)?obj.Render.ColorString:obj.Render.TileColor));}
        static Color Detail(GO obj){return ColorUtility.colorFromChar(string.IsNullOrEmpty(obj.Render.DetailColor)?'y':obj.Render.DetailColor[0]);}
        static string Signature(GO obj)
        {return obj.Blueprint+"|"+obj.GetGender().Name+"|"+obj.GetSpecies()+"|"+string.Join(";",obj.Body.GetParts().Select(PartPath).OrderBy(x=>x))+"|"+
            string.Join(";",obj.Body.GetParts().Where(p=>p.Equipped!=null).Select(p=>Key(p.Equipped.Blueprint,p.Type,p.Laterality)+"/"+p.Equipped.BaseID+"/"+Fore(p.Equipped)+"/"+Detail(p.Equipped)));}
        public static void BeginFrame(){if(Enabled)seen.Clear();}
        public static bool Changed(int index){Seen s;return Enabled && seen.TryGetValue(index,out s) && Signature(s.Obj)!=s.Signature;}
        public static string Kind(GO obj)
        {
            if(!Enabled || obj==null || obj==XRLCore.Core.Game.Player.Body)return null;
            if(((JObject)Data["actors"]).Properties().Any(p=>(string)p.Value["blueprint"]==obj.Blueprint))return "human";
            return Data["scenery"][obj.Blueprint]!=null?"prop":null;
        }
        public static void Capture(GO obj,JoppaCell cell)
        {
            if(!Enabled || obj==null)return;
            if(Data["scenery"][obj.Blueprint]!=null){cell.AssetFamily="current:scenery";return;}
            if(obj.Body==null || Kind(obj)==null)return;
            var parts=obj.Body.GetParts().ToArray();
            var topology=parts.Select(PartPath).OrderBy(x=>x).ToArray();
            var items=new List<EquippedAppearance>();
            foreach(var p in parts.Where(p=>p.Equipped!=null))
            {
                var item=p.Equipped;
                if(item.Render==null || items.Any(e=>e.Instance==item.BaseID)){cell.Kind="original";cell.ArtFallback="Unsupported multi-slot item";return;}
                items.Add(new EquippedAppearance{Instance=item.BaseID,Blueprint=item.Blueprint,Slot=p.Type,Laterality=p.Laterality,
                    Family=Key(item.Blueprint,p.Type,p.Laterality),Color=Fore(item),Detail=Detail(item),ColorCode=item.Render.TileColor});
            }
            var candidates=((JObject)Data["actors"]).Properties().Where(p=>(string)p.Value["blueprint"]==obj.Blueprint &&
                (string)p.Value["gender"]==obj.GetGender().Name && (string)p.Value["species"]==obj.GetSpecies() &&
                (string)p.Value["anatomy"]==obj.Body.Anatomy && ((JArray)p.Value["expected_topology"]).Select(x=>(string)x).OrderBy(x=>x).SequenceEqual(topology) &&
                items.All(e=>((JArray)p.Value["equipment"]).Any(x=>(string)x==e.Family))).ToArray();
            if(candidates.Length==0 || obj.HasEffect("Asleep") || obj.HasEffect("Prone"))
            {cell.Kind="original";cell.ArtFallback="Unsupported current body/equipment/posture";
                ProbeRunner.Record("current-fallback-"+obj.BaseID+".json",new{blueprint=obj.Blueprint,gender=obj.GetGender().Name,species=obj.GetSpecies(),anatomy=obj.Body.Anatomy,topology,
                    equipment=items.Select(e=>e.Family).ToArray(),asleep=obj.HasEffect("Asleep"),prone=obj.HasEffect("Prone")});return;}
            var match=candidates.OrderBy(p=>((JArray)p.Value["equipment"]).Count-items.Count).First();
            cell.AssetFamily="current:"+match.Name;cell.Equipment=items.ToArray();
            cell.BodyShape=string.Join(";",topology);
            seen[cell.X+80*cell.Y]=new Seen{Obj=obj,Signature=Signature(obj)};
        }
        public static JArray Scenery(JoppaCell cell)
        {
            if(!Enabled || cell.Source==null)return null;
            var rule=Data["scenery"][cell.Source];if(rule==null)return null;
            var result=rule["tiles"][Canonical(cell.Display.Tile)] as JArray;
            if(result==null && (bool)rule["connected"] && Canonical(cell.Display.Tile).Contains("wall_brinestalk"))
                result=rule["masks"][cell.ConnectionMask.ToString()] as JArray;
            return result;
        }
        public static bool KnownFinalTile(string source,string tile)
        {return source!=null && Data["scenery"][source]!=null &&
            (Data["scenery"][source]["tiles"][Canonical(tile)]!=null ||
             (bool)Data["scenery"][source]["connected"] && Canonical(tile).Contains("wall_brinestalk"));}
        public static bool CanMap(JoppaCell cell)
        {return cell.Visible && !cell.RequiresOriginal && !cell.Display.VFlip && cell.Display.Char=='\0' && (cell.WaterDepth==0 || cell.WaterSupported) &&
            ((cell.AssetFamily??"").StartsWith("current:NPC-") || Scenery(cell)!=null || Data["paint"][Canonical(cell.Display.Tile)]!=null ||
             cell.Source=="DirtPath" || cell.Source=="DirtFloor" || cell.Source=="Pond" && cell.WaterDepth>0);}
        static Texture2D Image(string file)
        {
            if(file==null)return null;Texture2D image;
            if(!images.TryGetValue(file,out image))
            {
                image=new Texture2D(2,2,TextureFormat.RGBA32,true,true);
                if(!ImageConversion.LoadImage(image,File.ReadAllBytes(Path.Combine((string)Data["image_root"],file))))throw new InvalidDataException(file);
                image.wrapMode=TextureWrapMode.Clamp;images[file]=image;
            }
            return image;
        }
        static Color[] Pixels(string file){var image=Image(file);return image==null?null:image.GetPixels();}
        public static string Compose(JoppaCell cell,JArray ops,string id)
        {
            string key="current:"+id+"|"+cell.Display.Foreground+"|"+cell.Display.Detail+"|"+
                string.Join(";",(cell.Equipment??new EquippedAppearance[0]).Select(e=>e.Family+"/"+e.Color+"/"+e.Detail));
            if(composed.ContainsKey(key))return key;
            Texture2D first=Image((string)ops[0]["file"]);var dst=new Color[first.width*first.height];
            foreach(JObject op in ops)
            {
                string itemKey=(string)op["key"];var item=itemKey==null?null:(cell.Equipment??new EquippedAppearance[0]).FirstOrDefault(e=>e.Family==itemKey);
                if(itemKey!=null && item==null)continue;
                Color pc=item==null?cell.Display.Foreground:item.Color,dc=item==null?cell.Display.Detail:item.Detail;
                string role=(string)op["role"];if(role=="fixed")pc=dc=Color.white;
                if(role=="detail" || role=="equipment-detail")pc=dc;
                var src=Pixels((string)op["file"]);var detail=Pixels((string)op["detail"]);
                var weight=Pixels((string)op["weight"]);var ownership=Pixels((string)op["ownership"]);
                if(src.Length!=dst.Length)throw new InvalidDataException("Mismatched current operation frame "+id);
                for(int i=0;i<dst.Length;i++)
                {
                    Color v=src[i];float alpha=v.a;
                    if((string)op["kind"]=="item" && detail!=null)
                    {
                        float da=Mathf.Min(alpha,detail[i].a);
                        v=alpha>0?(v*pc*(alpha-da)+detail[i]*dc*da)/alpha:Color.clear;
                    }
                    else v*=weight==null?pc:Color.Lerp(pc,dc,weight[i].r);
                    if(ownership!=null)alpha*=1-ownership[i].a;
                    v.a=alpha;float a=alpha+dst[i].a*(1-alpha);
                    Color result=a>0?(v*alpha+dst[i]*dst[i].a*(1-alpha))/a:Color.clear;
                    result.a=a;dst[i]=result;
                }
            }
            var texture=new Texture2D(first.width,first.height,TextureFormat.RGBA32,true,true);
            texture.SetPixels(dst);texture.Apply();texture.wrapMode=TextureWrapMode.Clamp;texture.filterMode=UnityEngine.FilterMode.Trilinear;
            texture.name=key;composed[key]=texture;return key;
        }
        public static Texture2D Texture(string key){return composed[key];}
        public static Texture2D SourceTexture(string key,bool repeat=false)
        {var image=Image(key);image.wrapMode=repeat?TextureWrapMode.Repeat:TextureWrapMode.Clamp;return image;}
        public static string Surface(string name,bool ripple=false)
        {
            string key="current:surface/"+name+"/"+ripple;
            if(composed.ContainsKey(key))return key;
            var rule=Data["surfaces"][name];
            string file=(string)(rule[ripple?"ripple":"base"]??rule["file"]);
            var texture=Image(file);texture.wrapMode=TextureWrapMode.Repeat;texture.filterMode=UnityEngine.FilterMode.Trilinear;
            composed[key]=texture;return key;
        }
        public static float Boundary(int mask,float u,float v)
        {return Image((string)Data["boundaries"][mask.ToString()]).GetPixelBilinear(u,v).r;}
        public static JObject ActorView(JoppaCell cell)
        {
            string id=cell.AssetFamily.Substring("current:".Length);
            string facing=cell.Facing==0?"north":cell.Facing==1?"east":cell.Facing==2?"south":"west";
            return (JObject)Data["actors"][id]["views"][facing];
        }
        public static string ActorTexture(JoppaCell cell,JObject view)
        {return Compose(cell,(JArray)view["ops"],cell.AssetFamily+"/"+cell.Facing);}
        public static void Dispose()
        {foreach(var texture in images.Values.Concat(composed.Values).Distinct())UnityEngine.Object.DestroyImmediate(texture);images.Clear();composed.Clear();}
        public static void Run()
        {
            var core=XRLCore.Core;var game=core.Game;var zone=game.Player.Body.CurrentZone;
            long ticks=game.TimeTicks;bool reveal=core.VisAllToggle;
            var explored=(bool[])zone.ExploredMap.Clone();var phases=new JArray();
            ProbeRunner.Record("current-liquid-inputs.json",Enumerable.Range(0,2000).Where(i=>zone.GetVisibility(i%80,i/80)).SelectMany(i=>zone.GetCell(i%80,i/80).Objects)
                .Where(o=>o.LiquidVolume!=null && o.LiquidVolume.IsOpenVolume() && o.LiquidVolume.Volume>0)
                .Select(o=>new{blueprint=o.Blueprint,x=o.CurrentCell.X,y=o.CurrentCell.Y,components=o.LiquidVolume.ComponentLiquids,
                    pureWater=o.LiquidVolume.IsPureLiquid("water"),waterProportion=o.LiquidVolume.Proportion("water")}));
            try
            {
                foreach(bool night in new[]{false,true})foreach(bool fog in new[]{false,true})
                {
                    Night=night;Fog=fog;game.TimeTicks=ticks-ticks%1200+(night?0:600);
                    core.VisAllToggle=!fog;
                    Array.Copy(explored,zone.ExploredMap,explored.Length);
                    string phase=(night?"night":"day")+(fog?"-fog":"-revealed");
                    GameplayProbe.RenderPhase("current-"+phase);
                    phases.Add(new JObject{{"phase",phase},{"nativeTicks",game.TimeTicks},{"nativeDay",Calendar.IsDay()},
                        {"fog",fog},{"revealOverride",!fog},{"adapterNightTint",new JArray(Shade.r,Shade.g,Shade.b)},
                        {"nativeVisibleCells",zone.VisibilityMap.Count(x=>x)},{"nativeExploredCells",zone.ExploredMap.Count(x=>x)}});
                }
                ProbeRunner.Record("current-four-views.json",new{phases,packageSha256=(string)Data["package_sha256"],
                    castSha256=(string)Data["cast_sha256"],nativeCamera=true,nativeLineOfSight=true,
                    nightTreatment="Explicit adapter tint on converted art; native Daylight, light sources and fog remain native. Revealed views intentionally override visibility/light."});
            }
            finally{game.TimeTicks=ticks;core.VisAllToggle=reveal;Array.Copy(explored,zone.ExploredMap,explored.Length);Night=false;Fog=false;}
        }
    }
}
