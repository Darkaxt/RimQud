// Bounded source-bound Joppa art. Qud remains the simulation/body/equipment owner.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using UnityEngine;
using XRL;
using XRL.Core;
using XRL.World.Anatomy;
using GO=XRL.World.GameObject;
using Event=XRL.World.Event;
using ColorUtility=ConsoleLib.Console.ColorUtility;

namespace RenderingTransplantProbe
{
    public static class VillageArt
    {
        public static bool Enabled {get{return Environment.GetEnvironmentVariable("QUDEXPERIMENT_ART")=="village";}}
        static JObject contract;
        public static JObject Contract {get {if(contract==null)contract=JObject.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"village.json")));return contract;}}
        public static JObject Actor(string name){return Enabled && name!=null?(JObject)Contract["actors"][name]:null;}
        public static JObject Scenery(string name){return Enabled && name!=null?(JObject)Contract["scenery"]["entries"][name]:null;}
        public static string Surface(string file){return Enabled?(string)Contract["scenery"]["surfaces"][file]??file:file;}
        public static string Wall(string name,bool detail=false)
        {var files=Enabled?(JArray)Contract["scenery"]["walls"][name]:null;return files==null?null:(string)files[detail?1:0];}
        static string Direction(int facing){return facing==0?"north":facing==2?"south":"east";}
        public static string Kind(GO obj)
        {
            if(!Enabled || obj==null)return null;
            if(obj==XRLCore.Core.Game.Player.Body)return "original";
            var a=Actor(obj.Blueprint);if(a!=null)return (string)a["family"]=="glowfish" || (string)a["family"]=="ray-cat"?"animal":"human";
            var s=Scenery(obj.Blueprint);return s==null?null:(string)s["kind"];
        }
        static string PartPath(BodyPart p){return(p.ParentPart==null?"":PartPath(p.ParentPart)+">")+p.Type+"/"+p.VariantType+"/"+p.Laterality;}
        static string Key(string blueprint,string slot,int laterality){return Regex.Replace(blueprint.ToLowerInvariant(),"[^a-z0-9]+","-").Trim('-')+"@"+slot+"@"+laterality;}
        static Color Fore(GO obj)
        {var r=obj.Render;return ColorUtility.colorFromChar(ColorUtility.ParseForegroundColor(string.IsNullOrEmpty(r.TileColor)?r.ColorString:r.TileColor));}
        static Color Detail(GO obj){return ColorUtility.colorFromChar(string.IsNullOrEmpty(obj.Render.DetailColor)?'y':obj.Render.DetailColor[0]);}
        static string Family(GO obj,JObject a)
        {string family=(string)a["family"];return family=="human"?"human-"+(obj.GetGender().Name=="female"?"female":"male"):family;}
        static string Signature(GO obj,out string family,out string failure,out EquippedAppearance[] items,out string shape)
        {
            var rule=Actor(obj.Blueprint);family=Family(obj,rule);failure=null;var result=new List<EquippedAppearance>();
            shape=obj.Body==null?"no body":obj.Body.Anatomy+":"+string.Join(";",obj.Body.GetParts().Select(PartPath).OrderBy(s=>s,StringComparer.Ordinal));
            if(obj.Body==null || obj.Body.Anatomy!=(string)rule["anatomy"] || !obj.Body.GetParts().Select(PartPath).OrderBy(s=>s,StringComparer.Ordinal)
                .SequenceEqual(((JArray)rule["expected_topology"]).Select(p=>(string)p).OrderBy(s=>s,StringComparer.Ordinal)))failure="Unsupported village body topology";
            if(obj.GetSpecies()!=(string)rule["species"])failure="Changed village species";
            if((string)rule["family"]=="human" && obj.GetGender().Name!="male" && obj.GetGender().Name!="female")failure="Unsupported ordinary human body selection";
            if(obj.HasEffect("Asleep") || obj.HasEffect("Prone"))failure="Unsupported village posture";
            if(rule["detail_guard"]!=null && rule["detail_guard"].Type!=JTokenType.Null && Detail(obj)!=ColorUtility.colorFromChar(((string)rule["detail_guard"])[0]))failure="Unsupported detail on retained neutral cat";
            var fixedPalette=rule["fixed_palette"] as JObject;
            if(fixedPalette!=null && (Fore(obj)!=ColorUtility.colorFromChar(ColorUtility.ParseForegroundColor((string)fixedPalette["foreground"])) ||
                Detail(obj)!=ColorUtility.colorFromChar(((string)fixedPalette["detail"])[0])))failure="Changed fixed glowfish palette";
            if(obj.Body!=null)foreach(var part in obj.Body.GetParts())
            {
                var item=part.Equipped;if(item==null || result.Any(e=>e.Instance==item.BaseID))continue;
                string key=Key(item.Blueprint,part.Type,part.Laterality);
                var eq=Contract["equipment"][family]?[key];
                if(eq==null || obj.Body.GetParts().Count(p=>p.Equipped==item)!=1 || item.Render==null)failure="Unsupported village equipped item/slot: "+item.Blueprint;
                if(item.Render==null)continue;
                result.Add(new EquippedAppearance{Instance=item.BaseID,Blueprint=item.Blueprint,Slot=part.Type,Family=key,Laterality=part.Laterality,
                    ColorCode=string.IsNullOrEmpty(item.Render.TileColor)?item.Render.ColorString:item.Render.TileColor,Color=Fore(item),Detail=Detail(item),Layer=part.Type=="Body"?20:80});
            }
            items=result.ToArray();return family+"|"+shape+"|"+failure+"|"+string.Join(";",items.Select(e=>e.Instance+"/"+e.Family+"/"+e.ColorCode+"/"+e.Detail));
        }
        sealed class Observation {public GO Object;public string Signature;}
        static readonly Dictionary<int,Observation> observations=new Dictionary<int,Observation>();
        public static void BeginFrame(){if(Enabled)observations.Clear();}
        public static void Capture(GO obj,JoppaCell cell)
        {
            if(!Enabled || obj==null)return;
            var scenery=Scenery(obj.Blueprint);
            if(scenery!=null){cell.AssetFamily="village:scenery";cell.Kind=(string)scenery["kind"];return;}
            var actor=Actor(obj.Blueprint);if(actor==null)return;
            string family,failure,shape;EquippedAppearance[] items;string signature=Signature(obj,out family,out failure,out items,out shape);
            cell.AssetFamily="village:"+family;cell.Equipment=items;cell.BodyShape=shape;cell.ArtFallback=failure;cell.ApparelFallback=failure;
            if(failure!=null)cell.Kind="original";
            observations[cell.X+80*cell.Y]=new Observation{Object=obj,Signature=signature};
        }
        public static bool Changed(int index)
        {
            Observation o;if(!Enabled || !observations.TryGetValue(index,out o))return false;
            string family,failure,shape;EquippedAppearance[] items;return o.Signature!=Signature(o.Object,out family,out failure,out items,out shape);
        }
        public static JArray Layers(JoppaCell cell)
        {
            var layers=new JArray();string d=Direction(cell.Facing);
            if(cell.AssetFamily=="village:scenery")return(JArray)Scenery(cell.Source)["views"][d];
            string family=cell.AssetFamily.Substring("village:".Length);
            foreach(var p in Contract["bodies"][family]["views"][d])layers.Add(p.DeepClone());
            if(cell.Equipment!=null)foreach(var item in cell.Equipment)
                foreach(var p in Contract["equipment"][family][item.Family]["views"][d])layers.Add(p.DeepClone());
            return new JArray(layers.Cast<JObject>().OrderBy(p=>(float)p["layer"]));
        }
        public static Color Tint(JoppaCell cell,JObject part)
        {
            string role=(string)part["color_role"];
            if(role=="fixed")return Color.white;
            if(role.StartsWith("equipment")){var item=cell.Equipment.Single(e=>e.Family==(string)part["equipment_key"]);return role=="equipment-detail"?item.Detail:item.Color;}
            return role=="detail"?cell.Display.Detail:cell.Display.Char=='\0'?cell.Display.Foreground:cell.Display.Background;
        }
        public static GO LateItem;
        public static bool LateChange;
        public static void MutateLate(){if(Enabled && LateChange)LateItem.Render.TileColor="&M";}
        static GO[] Residents(XRL.World.Zone zone)
        {return Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects).Where(o=>Actor(o.Blueprint)!=null).Distinct().ToArray();}
        static string Outfit(IEnumerable<GO> actors)
        {return string.Join(";",actors.OrderBy(o=>o.BaseID).SelectMany(o=>o.Body.GetParts().Where(p=>p.Equipped!=null).Select(p=>o.BaseID+":"+PartPath(p)+":"+p.Equipped.BaseID+":"+p.Equipped.Blueprint+":"+p.Equipped.Render.TileColor+":"+p.Equipped.Render.DetailColor)));}
        static void Reveal(XRL.World.Zone zone){zone.ExploreAll();zone.VisAll();zone.LightAll();}
        public static void RunBatch()
        {
            bool revealBefore=XRLCore.Core.VisAllToggle;XRLCore.Core.VisAllToggle=true;
            try{RunRevealedBatch();}finally{XRLCore.Core.VisAllToggle=revealBefore;}
        }
        static void RunRevealedBatch()
        {
            var game=XRLCore.Core.Game;var zone=game.Player.Body.CurrentZone;var actors=Residents(zone);string outfit=Outfit(actors);
            PawnPresentation.Prop=Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects).First(o=>o.Blueprint=="Chair");
            ProbeRunner.Record("village-residents.json",new{actors=actors.Select(o=>new{instance=o.BaseID,blueprint=o.Blueprint,gender=o.GetGender().Name,species=o.GetSpecies()}),diagnosticFullReveal=true});
            Reveal(zone);GameplayProbe.RenderPhase("village-native-layout");
            // Exercise both native depth classes without inventing a shallow
            // field. The generated Joppa ponds begin at actual wading depth.
            var pond=Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects).First(o=>o.Blueprint=="Pond");
            int pondVolume=pond.LiquidVolume.Volume;pond.LiquidVolume.Volume=10000;
            if(!pond.LiquidVolume.IsSwimmingDepth())throw new InvalidOperationException("Native deep-water fixture did not reach swimming depth");
            Reveal(zone);GameplayProbe.RenderPhase("village-deep-water");pond.LiquidVolume.Volume=pondVolume;
            // Direction review uses native location changes in isolated clear
            // cells. It does not claim a new locomotion or limb-animation system.
            var positions=actors.ToDictionary(o=>o,o=>o.CurrentCell);var fixtures=new Dictionary<GO,XRL.World.Cell>();var used=new List<XRL.World.Cell>();
            foreach(var actor in actors)
            {
                var target=Enumerable.Range(0,2000).Select(i=>zone.GetCell(i%80,i/80))
                    .Where(c=>c.X>1 && c.X<78 && c.Y>1 && c.Y<23 && !used.Any(u=>Math.Abs(u.X-c.X)<4 && Math.Abs(u.Y-c.Y)<3))
                    .First(c=>new[]{c,c.GetCellFromDirection("E"),c.GetCellFromDirection("W"),c.GetCellFromDirection("N"),c.GetCellFromDirection("S")}
                        .All(n=>n!=null && !n.IsSolidFor(actor) && n.Objects.All(o=>!o.HasPart("Combat"))));
                fixtures[actor]=target;used.Add(target);PawnPresentation.Place(actor,target);
            }
            Reveal(zone);GameplayProbe.RenderPhase("village-fixtures-south");
            foreach(var step in new[]{new[]{"E","east"},new[]{"W","west"},new[]{"N","north"},new[]{"S","south"}})
            {
                foreach(var actor in actors)PawnPresentation.Place(actor,actor.CurrentCell.GetCellFromDirection(step[0]));
                Reveal(zone);GameplayProbe.RenderPhase("village-"+step[1]);
            }
            var worn=new List<Tuple<GO,BodyPart,GO>>();
            foreach(var actor in actors)foreach(var part in actor.Body.GetParts().Where(p=>p.Type=="Body" && p.Equipped!=null))
            {
                var item=part.Equipped;var e=Event.New("CommandUnequipObject","Object",item,"BodyPart",part);e.SetSilent(true);e.SetFlag("NoStack",true);e.SetParameter("EnergyCost",0);
                if(!actor.FireEvent(e) || part.Equipped==item)throw new InvalidOperationException("Village native garment removal failed");
                worn.Add(Tuple.Create(actor,part,item));
            }
            Reveal(zone);GameplayProbe.RenderPhase("village-garments-removed");
            foreach(var w in worn)if(!w.Item1.EquipObject(w.Item3,w.Item2,Silent:true,EnergyCost:0))throw new InvalidOperationException("Village native garment restore failed");
            Reveal(zone);GameplayProbe.RenderPhase("village-equipped");
            LateItem=worn.First().Item3;string itemColor=LateItem.Render.TileColor;LateChange=true;Reveal(zone);GameplayProbe.RenderPhase("village-late-item");LateChange=false;LateItem.Render.TileColor=itemColor;
            var sample=actors.Single(o=>o.Blueprint=="Nima Ruda");const string manager="RimQudVillageExtraArm";
            sample.Body.GetBody().AddPart("Arm",Manager:manager);Reveal(zone);GameplayProbe.RenderPhase("village-unsupported-body");sample.RemoveBodyPartsByManager(manager,EvenIfDismembered:true);
            sample.Render.Visible=false;Reveal(zone);GameplayProbe.RenderPhase("village-hidden");sample.Render.Visible=true;
            Reveal(zone);GameplayProbe.RenderPhase("village-restored");GameplayProbe.TargetActor(sample,"village");GameplayProbe.DamageFixture(sample,"village");
            foreach(var pair in positions)PawnPresentation.Place(pair.Key,pair.Value);
            if(Outfit(actors)!=outfit)throw new InvalidOperationException("Native village outfit changed during diagnostics");
            game.SetIntGameState("RimQudVillageArt",1);var save=game.SaveGame("RimQudVillageArt");if(save!=null)save.GetAwaiter().GetResult();
            var loaded=XRLGame.LoadCurrentGame("RimQudVillageArt");if(loaded==null || loaded.GetIntGameState("RimQudVillageArt")!=1)throw new InvalidOperationException("Village save/load failed");
            zone=loaded.Player.Body.CurrentZone;actors=Residents(zone);if(Outfit(actors)!=outfit)throw new InvalidOperationException("Village native equipment did not survive load");
            Reveal(zone);GameplayProbe.RenderPhase("village-loaded");
            ProbeRunner.Record("village-result.json",new{residentCount=actors.Length,actorBlueprints=actors.Select(o=>o.Blueprint).Distinct().OrderBy(s=>s),nativeSaveLoad=true,nativeEquipUnequip=true,
                originalOutfitsRestored=true,diagnosticFullReveal=true,diagnosticPlacementForFacing=true,operatingSystemInput=false,contract=Contract});
        }
    }
}
