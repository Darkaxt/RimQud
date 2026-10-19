// Bounded Qud equipped-slot adapter. No donor apparel, inventory or AI authority.
using System;
using System.Collections.Generic;
using System.Linq;
using ConsoleLib.Console;
using UnityEngine;
using XRL;
using XRL.Core;
using XRL.World;
using XRL.World.Anatomy;
using GO=XRL.World.GameObject;
using Event=XRL.World.Event;

namespace RenderingTransplantProbe
{
    public sealed class EquippedAppearance
    {
        public int Instance,Layer;
        public string Blueprint,Slot,Family,ColorCode;
        public Color Color;
    }
    public static class NativeApparel
    {
        public static bool Live,LateMutation;
        public static GO Fixture;
        static GO robe;
        static string residentBefore,savedOutfit;
        public static bool Enabled { get { return PawnPresentation.Enabled && PawnPresentation.Stage>=4 && Live; } }
        sealed class Rule
        {
            public string Slot,Family;public int Layer;
            public Rule(string slot,string family,int layer){Slot=slot;Family=family;Layer=layer;}
        }
        static readonly Dictionary<string,Rule> rules=new Dictionary<string,Rule>{
            {"Woven Tunic",new Rule("Body","tunic",20)},{"Cloth Robe",new Rule("Body","robe",20)},
            {"Leather Cloak",new Rule("Back","cloak",32)},{"Wide-brimmed Hat",new Rule("Head","hat",70)},
            {"Long Sword",new Rule("Hand","sword",80)}};
        sealed class Observation { public GO Object;public string Signature; }
        static readonly Dictionary<int,Observation> observed=new Dictionary<int,Observation>();
        public static void BeginFrame(){observed.Clear();}
        static EquippedAppearance[] Read(GO obj,out string shape,out string failure)
        {
            failure=null;var body=obj.Body;
            if(body==null){shape="no body";failure="Unsupported anatomy";return new EquippedAppearance[0];}
            var parts=body.GetParts();
            shape=body.Anatomy+":"+string.Join(",",new[]{"Body","Head","Arm","Hand","Back","Feet","Foot","Tail","Face"}.Select(t=>t+"="+body.GetPartCount(t)));
            var items=new List<EquippedAppearance>();
            foreach(var part in parts)
            {
                var item=part.Equipped;if(item==null || items.Any(e=>e.Instance==item.BaseID))continue;
                Rule rule;rules.TryGetValue(item.Blueprint,out rule);
                var render=item.Render;string color=render==null?"&y":string.IsNullOrEmpty(render.TileColor)?render.ColorString:render.TileColor;
                items.Add(new EquippedAppearance{Instance=item.BaseID,Blueprint=item.Blueprint,Slot=part.Type,
                    Family=rule==null?null:rule.Family,Layer=rule==null?0:rule.Layer,ColorCode=color,
                    Color=ConsoleLib.Console.ColorUtility.colorFromChar(ConsoleLib.Console.ColorUtility.ParseForegroundColor(color))});
                if(rule==null || rule.Slot!=part.Type || parts.Count(p=>p.Equipped==item)!=1)
                    failure="Unsupported equipped item or slot: "+item.Blueprint+" on "+part.Type;
            }
            if(PawnPresentation.Kind(obj)=="animal")
            {
                if(items.Count>0)failure="Unsupported animal equipment";
            }
            else if(body.Anatomy!="Humanoid" || body.GetPartCount("Body")!=1 || body.GetPartCount("Head")!=1 ||
                body.GetPartCount("Arm")!=2 || body.GetPartCount("Hand")!=2 || body.GetPartCount("Back")!=1 || body.GetPartCount("Feet")!=1)
                failure="Unsupported anatomy for the reviewed human outfit: "+shape;
            return items.OrderBy(e=>e.Layer).ThenBy(e=>e.Instance).ToArray();
        }
        static string Signature(EquippedAppearance[] items,string shape,string failure)
        {return shape+"|"+failure+"|"+string.Join(";",items.Select(e=>e.Instance+"/"+e.Blueprint+"/"+e.Slot+"/"+e.ColorCode));}
        public static void Capture(GO obj,JoppaCell cell)
        {
            if(DromadArt.Enabled && obj.Blueprint=="Tam")return;
            if(!Enabled || !PawnPresentation.IsLayered(cell.Kind) || cell.Kind=="prop")return;
            string shape,failure;var items=Read(obj,out shape,out failure);
            cell.Equipment=items;cell.BodyShape=shape;cell.ApparelFallback=failure;
            observed[cell.X+80*cell.Y]=new Observation{Object=obj,Signature=Signature(items,shape,failure)};
            if(failure!=null)cell.Kind="original";
        }
        public static bool Changed(int index)
        {
            if(!Enabled)return false;Observation observation;if(!observed.TryGetValue(index,out observation))return false;
            string shape,failure;var items=Read(observation.Object,out shape,out failure);
            return observation.Signature!=Signature(items,shape,failure);
        }
        public static void MutateLate(){if(Enabled && LateMutation)robe.Render.TileColor="&G";}
        static string Outfit(GO obj)
        {
            return string.Join(";",obj.Body.GetParts().Where(p=>p.Equipped!=null)
                .Select(p=>p.Type+":"+p.Equipped.BaseID+":"+p.Equipped.Blueprint+":"+p.Equipped.Render.TileColor+":"+p.Equipped.Render.ColorString).OrderBy(s=>s));
        }
        static GO Give(GO npc,string blueprint)
        {
            var item=GO.Create(blueprint);if(!npc.ReceiveObject(item,NoStack:true))throw new InvalidOperationException("NPC could not receive "+blueprint);
            return item;
        }
        static void Equip(GO npc,GO item,string slot)
        {
            var part=npc.Body.GetParts().Where(p=>p.Type==slot).OrderByDescending(p=>p.Primary).First();
            if(!npc.EquipObject(item,part,Silent:true,EnergyCost:0) || part.Equipped!=item)
                throw new InvalidOperationException("Native equip failed for "+item.Blueprint+" on "+slot);
        }
        static void Unequip(GO npc,GO item)
        {
            var e=Event.New("CommandUnequipObject","Object",item,"BodyPart",npc.Body.FindEquippedItem(item));
            e.SetSilent(true);e.SetFlag("NoStack",true);e.SetParameter("EnergyCost",0);
            if(!npc.FireEvent(e) || npc.Body.HasEquippedItem(item))throw new InvalidOperationException("Native unequip failed for "+item.Blueprint);
        }
        static void UnequipAll(GO npc)
        {
            foreach(var item in npc.Body.GetEquippedObjectsExceptNatural().ToArray())Unequip(npc,item);
            if(npc.Body.GetEquippedObjectsExceptNatural().Count!=0)
                throw new InvalidOperationException("Native fixture still has equipped starting gear");
        }
        static void Move(string direction,string phase)
        {
            if(!Fixture.Move(direction,DoConfirmations:false,EnergyCost:0,Peaceful:true))
                throw new InvalidOperationException("Native clothing fixture move failed: "+direction);
            GameplayProbe.RenderPhase(phase);
        }
        public static void RunFixture()
        {
            if(!PawnPresentation.Enabled || PawnPresentation.Stage<4)return;
            residentBefore=Outfit(PawnPresentation.Human);Live=true;
            Fixture=GO.Create("WatervineFarmerJoppa");Fixture.SetIntProperty("RimQudApparelFixture",1);
            var cell=PawnPresentation.Human.CurrentCell.GetCellFromDirection("W");
            if(cell.IsSolidFor(Fixture))throw new InvalidOperationException("No clear native apparel fixture cell");
            cell.AddObject(Fixture);
            string starting=Outfit(Fixture);UnequipAll(Fixture);
            ProbeRunner.Record("apparel-setup.json",new{starting,outfitAfterNativeUnequip=Outfit(Fixture),noStack=true});
            var tunic=Give(Fixture,"Woven Tunic");robe=Give(Fixture,"Cloth Robe");
            var cloak=Give(Fixture,"Leather Cloak");var hat=Give(Fixture,"Wide-brimmed Hat");var sword=Give(Fixture,"Long Sword");
            ProbeRunner.Record("apparel-fixture.json",new{instance=Fixture.BaseID,
                items=new[]{tunic,robe,cloak,hat,sword}.ToDictionary(o=>o.Blueprint,o=>o.BaseID),
                source="New native farmer diagnostic, not a resident's altered equipment",operatingSystemInput=false});
            GameplayProbe.RenderPhase("apparel-inventory-only");
            Equip(Fixture,tunic,"Body");Equip(Fixture,cloak,"Back");Equip(Fixture,hat,"Head");Equip(Fixture,sword,"Hand");
            GameplayProbe.RenderPhase("apparel-equipped");
            Unequip(Fixture,hat);GameplayProbe.RenderPhase("apparel-hat-removed");Equip(Fixture,hat,"Head");
            Unequip(Fixture,tunic);Equip(Fixture,robe,"Body");GameplayProbe.RenderPhase("apparel-swapped");
            string color=robe.Render.TileColor;robe.Render.TileColor="&R";GameplayProbe.RenderPhase("apparel-tint");
            robe.Render.TileColor=color;GameplayProbe.RenderPhase("apparel-tint-restored");
            LateMutation=true;GameplayProbe.RenderPhase("apparel-late-change");LateMutation=false;robe.Render.TileColor=color;
            GameplayProbe.RenderPhase("apparel-late-restored");
            Move("W","apparel-west");Move("E","apparel-east");Move("N","apparel-north");Move("S","apparel-south");
            GameplayProbe.TargetApparel(Fixture);GameplayProbe.DamageFixture(Fixture,"equipped");
            var unsupported=Give(Fixture,"Leather Boots");Equip(Fixture,unsupported,"Feet");
            GameplayProbe.RenderPhase("apparel-unsupported-item");Unequip(Fixture,unsupported);
            GameplayProbe.RenderPhase("apparel-supported-restored");
            var anatomy=GO.Create("WatervineFarmerJoppa");
            var other=Fixture.CurrentCell.GetCellFromDirection("W");
            if(other.IsSolidFor(anatomy))throw new InvalidOperationException("No clear unsupported anatomy fixture cell");
            other.AddObject(anatomy);UnequipAll(anatomy);anatomy.Body.GetFirstPart("Body").AddPart("Arm");
            GameplayProbe.RenderPhase("apparel-unsupported-anatomy");
            if(Outfit(PawnPresentation.Human)!=residentBefore)throw new InvalidOperationException("Resident equipment changed");
            savedOutfit=Outfit(Fixture);
            ProbeRunner.Record("apparel-before-save.json",new{instance=Fixture.BaseID,outfit=savedOutfit,
                residentEquipmentUnchanged=true,unsupportedAnatomyInstance=anatomy.BaseID,
                anatomyArms=anatomy.Body.GetPartCount("Arm"),carriedTunicUnworn=!Fixture.Body.HasEquippedItem(tunic)});
        }
        public static void AfterLoad(XRLGame game)
        {
            if(!Enabled)return;
            var zone=game.Player.Body.CurrentZone;
            Fixture=Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects)
                .Single(o=>o.GetIntProperty("RimQudApparelFixture")==1);
            if(Outfit(Fixture)!=savedOutfit)throw new InvalidOperationException("Native loaded equipment differs");
            ProbeRunner.Record("apparel-load.json",new{instance=Fixture.BaseID,outfit=Outfit(Fixture),nativeSaveLoad=true});
        }
    }
}
