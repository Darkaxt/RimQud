// Explicit adult dromad body/head and two actual equipped items. No limb rig.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using XRL;
using XRL.Core;
using XRL.World.Anatomy;
using GO=XRL.World.GameObject;
using Event=XRL.World.Event;

namespace RenderingTransplantProbe
{
    public static class DromadArt
    {
        public static bool Enabled { get { return Environment.GetEnvironmentVariable("QUDEXPERIMENT_ART")=="dromad"; } }
        static JObject contract;
        public static JObject Contract
        {
            get
            {
                if(contract==null)
                {
                    contract=JObject.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"dromad.json")));
                    if((string)contract["creature"]!="Tam" || (string)contract["race"]!="Dromad" || contract["original_model"]==null)
                        throw new InvalidDataException("Missing source-bound Tam race contract");
                }
                return contract;
            }
        }
        static string PathOf(BodyPart part)
        {return (part.ParentPart==null?"":PathOf(part.ParentPart)+">")+part.Type+"/"+part.VariantType+"/"+part.Laterality;}
        static EquippedAppearance[] Read(GO obj,out string shape,out string failure)
        {
            failure=null;shape=obj.Body==null?"no body":obj.Body.Anatomy+":"+
                string.Join(";",obj.Body.GetParts().Select(PathOf).OrderBy(s=>s,StringComparer.Ordinal));
            var expected=((JArray)Contract["expected_topology"]).Select(s=>(string)s).OrderBy(s=>s,StringComparer.Ordinal).ToArray();
            if(obj.Body==null || obj.Body.Anatomy!="Humanoid" ||
                !obj.Body.GetParts().Select(PathOf).OrderBy(s=>s,StringComparer.Ordinal).SequenceEqual(expected))
            {failure="Unsupported dromad body topology";return new EquippedAppearance[0];}
            var parts=obj.Body.GetParts();var items=new List<EquippedAppearance>();
            foreach(var p in parts)
            {
                var item=p.Equipped;if(item==null || items.Any(e=>e.Instance==item.BaseID))continue;
                string family=item.Blueprint=="Cloth Robe" && p.Type=="Body"?"robe":
                    item.Blueprint=="Shillelagh" && p.Type=="Hand"?"shillelagh":null;
                var r=item.Render;string color=r==null?"&y":string.IsNullOrEmpty(r.TileColor)?r.ColorString:r.TileColor;
                var tint=ColorUtility.colorFromChar(ColorUtility.ParseForegroundColor(color));
                items.Add(new EquippedAppearance{Instance=item.BaseID,Blueprint=item.Blueprint,Slot=p.Type,Family=family,
                    Layer=family=="robe"?20:80,ColorCode=color,Color=tint});
                if(family==null || parts.Count(b=>b.Equipped==item)!=1 || r==null ||
                    !string.IsNullOrEmpty(r.DetailColor) && ColorUtility.colorFromChar(r.DetailColor[0])!=tint)
                    failure="Unsupported dromad equipment, slot or independent item detail: "+item.Blueprint;
            }
            return items.OrderBy(e=>e.Layer).ToArray();
        }
        sealed class Observation { public GO Object;public string Signature; }
        static readonly Dictionary<int,Observation> observed=new Dictionary<int,Observation>();
        public static void BeginFrame(){if(Enabled)observed.Clear();}
        static string Signature(GO obj,out EquippedAppearance[] items,out string shape,out string failure)
        {
            items=Read(obj,out shape,out failure);
            return shape+"|"+failure+"|"+string.Join(";",items.Select(i=>i.Instance+"/"+i.Slot+"/"+i.Blueprint+"/"+i.ColorCode));
        }
        public static void Capture(GO obj,JoppaCell cell)
        {
            if(!Enabled || obj.Blueprint!="Tam")return;
            EquippedAppearance[] items;string shape,failure;
            string signature=Signature(obj,out items,out shape,out failure);
            if(obj.HasEffect("Asleep") || obj.HasEffect("Prone"))failure="Unsupported dromad posture";
            cell.AssetFamily="dromad";cell.Equipment=items;cell.BodyShape=shape;cell.ArtFallback=failure;cell.ApparelFallback=failure;
            if(failure!=null)cell.Kind="original";
            observed[cell.X+80*cell.Y]=new Observation{Object=obj,Signature=signature};
        }
        public static bool Changed(int index)
        {
            Observation o;if(!Enabled || !observed.TryGetValue(index,out o))return false;
            EquippedAppearance[] items;string shape,failure;
            return o.Signature!=Signature(o.Object,out items,out shape,out failure);
        }
        public static JArray View(int facing)
        {return (JArray)Contract["views"][facing==0?"north":facing==2?"south":"east"];}

        static GO tam;
        static string savedEquipment;
        public static bool LateEquipment;
        static GO robe;
        public static void MutateLate(){if(Enabled && LateEquipment)robe.Render.TileColor="&G";}
        static string Outfit(GO obj)
        {return string.Join(";",obj.Body.GetParts().Where(p=>p.Equipped!=null).Select(p=>p.Type+":"+p.Equipped.BaseID+":"+p.Equipped.Blueprint+":"+p.Equipped.Render.TileColor).OrderBy(s=>s));}
        static void Remove(GO item)
        {
            var e=Event.New("CommandUnequipObject","Object",item,"BodyPart",tam.Body.FindEquippedItem(item));
            e.SetSilent(true);e.SetFlag("NoStack",true);e.SetParameter("EnergyCost",0);
            if(!tam.FireEvent(e) || tam.Body.HasEquippedItem(item))throw new InvalidOperationException("Native dromad unequip failed");
        }
        static void Equip(GO item,string slot)
        {
            var part=tam.Body.GetParts().First(p=>p.Type==slot && p.Equipped==null);
            if(!tam.EquipObject(item,part,Silent:true,EnergyCost:0))throw new InvalidOperationException("Native dromad equip failed");
        }
        public static void RunSample()
        {
            var game=XRLCore.Core.Game;var zone=game.Player.Body.CurrentZone;
            tam=Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects).Single(o=>o.Blueprint=="Tam");
            // Relocation is diagnostic only; keep his actual equipment and identity.
            var player=game.Player.Body;var start=player.CurrentCell;
            var target=Enumerable.Range(0,81).Select(i=>new[]{start.X+i%9-4,start.Y+i/9-4})
                .Where(p=>p[0]>0 && p[0]<79 && p[1]>0 && p[1]<24)
                .Select(p=>zone.GetCell(p[0],p[1])).First(c=>new[]{c,c.GetCellFromDirection("E"),c.GetCellFromDirection("W"),c.GetCellFromDirection("N"),c.GetCellFromDirection("S")}
                    .All(n=>n!=null && !n.IsSolidFor(tam) && n.Objects.All(o=>!o.HasPart("Combat"))));
            string before=Outfit(tam);PawnPresentation.Place(tam,target);
            robe=tam.Body.GetEquippedObjectsExceptNatural().Single(o=>o.Blueprint=="Cloth Robe");
            var held=tam.Body.GetEquippedObjectsExceptNatural().Single(o=>o.Blueprint=="Shillelagh");
            GameplayProbe.RenderPhase("dromad-south");
            foreach(var move in new[]{new[]{"E","east"},new[]{"W","west"},new[]{"N","north"},new[]{"S","south-restored"}})
            {
                var old=tam.CurrentCell;var next=old.GetCellFromDirection(move[0]);
                if(next==null || next.IsSolidFor(tam) || next.Objects.Any(o=>o!=tam && o.HasPart("Combat")))
                    throw new InvalidOperationException("Dromad fixture move not clear: "+move[0]);
                if(!tam.Move(move[0],DoConfirmations:false,EnergyCost:0,Peaceful:true))throw new InvalidOperationException("Dromad native movement failed");
                GameplayProbe.RenderPhase("dromad-"+move[1]);
            }
            Remove(robe);GameplayProbe.RenderPhase("dromad-robe-removed");Equip(robe,"Body");
            Remove(held);GameplayProbe.RenderPhase("dromad-held-removed");Equip(held,"Hand");
            string color=robe.Render.TileColor;LateEquipment=true;GameplayProbe.RenderPhase("dromad-late-equipment");
            LateEquipment=false;robe.Render.TileColor=color;GameplayProbe.RenderPhase("dromad-equipped-restored");
            var foreground=tam.Render.TileColor;var detail=tam.Render.DetailColor;
            tam.Render.TileColor="&C";tam.Render.DetailColor="m";GameplayProbe.RenderPhase("dromad-palette");
            tam.Render.TileColor=foreground;tam.Render.DetailColor=detail;
            tam.Render.Visible=false;GameplayProbe.RenderPhase("dromad-hidden");tam.Render.Visible=true;
            const string manager="RimQudDromadDiagnosticArm";
            tam.Body.GetBody().AddPart("Arm",Manager:manager);GameplayProbe.RenderPhase("dromad-unsupported-anatomy");
            tam.RemoveBodyPartsByManager(manager,EvenIfDismembered:true);GameplayProbe.RenderPhase("dromad-restored");
            GameplayProbe.TargetActor(tam,"dromad");GameplayProbe.DamageFixture(tam,"dromad");
            if(Outfit(tam)!=before)throw new InvalidOperationException("Tam's actual starting outfit was not restored");
            savedEquipment=Outfit(tam);game.SetIntGameState("RimQudDromadSample",1);
            var save=game.SaveGame("RimQudDromad");if(save!=null)save.GetAwaiter().GetResult();
            var loaded=XRLGame.LoadCurrentGame("RimQudDromad");
            if(loaded==null || loaded.GetIntGameState("RimQudDromadSample")!=1)throw new InvalidOperationException("Dromad sample save/load failed");
            tam=Enumerable.Range(0,2000).SelectMany(i=>loaded.Player.Body.CurrentZone.GetCell(i%80,i/80).Objects).Single(o=>o.Blueprint=="Tam");
            if(Outfit(tam)!=savedEquipment)throw new InvalidOperationException("Dromad equipment changed across load");
            GameplayProbe.RenderPhase("dromad-loaded");
            ProbeRunner.Record("dromad-result.json",new{instance=tam.BaseID,creature="Tam",race="Dromad",nativeSaveLoad=true,
                actualStartingEquipmentRestored=true,nativeEquipUnequip=true,nativeMovement=true,operatingSystemInput=false,contract=Contract});
        }
    }
}
