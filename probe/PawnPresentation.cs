// Narrow known-layer adapter and native-world diagnostic for the first pawn scene.
using System;
using System.Collections.Generic;
using System.Linq;
using XRL;
using XRL.Core;
using XRL.World;
using HarmonyLib;
using GO=XRL.World.GameObject;

namespace RenderingTransplantProbe
{
    [HarmonyPatch]
    public static class NativePawnDamage
    {
        static System.Reflection.MethodBase TargetMethod(){return AccessTools.GetDeclaredMethods(typeof(GO)).Single(m=>
            m.Name=="TakeDamage" && m.GetParameters()[0].ParameterType==typeof(int).MakeByRefType());}
        static void Prefix(GO __instance,ref int __state){__state=__instance.Stat("Hitpoints");}
        static void Postfix(GO __instance,GO Attacker,GO Source,string Attributes,int __state)
        {PawnPresentation.Damaged(__instance,Attacker??Source,Attributes,__state-__instance.Stat("Hitpoints"));}
    }
    public static class PawnPresentation
    {
        public static bool Enabled { get { return Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")=="pawns"; } }
        public static int Stage { get { int stage;return int.TryParse(Environment.GetEnvironmentVariable("QUDEXPERIMENT_STAGE"),out stage)?stage:1; } }
        sealed class Pose { public int X,Y,Facing=2; }
        sealed class Hurt { public int Serial;public float DX,DY; }
        static readonly Dictionary<int,Pose> poses=new Dictionary<int,Pose>();
        static readonly Dictionary<int,Hurt> hurt=new Dictionary<int,Hurt>();
        static readonly HashSet<int> visible=new HashSet<int>();
        static int serial;
        public static int World { get; private set; }
        static XRLGame owner;
        public static GO Human,Animal,Prop;
        public static bool InjectLateMutation;
        static void EnsureWorld()
        {
            if(owner==XRLCore.Core.Game)return;
            owner=XRLCore.Core.Game;poses.Clear();hurt.Clear();visible.Clear();World++;
        }
        public static void Accepted(JoppaCell[] cells)
        {
            if(!Enabled && !JoppaCoverage.Enabled)return;EnsureWorld();visible.Clear();
            foreach(var c in cells)if(c.Visible && !c.RequiresOriginal && c.Instance>0 &&
                (c.Kind=="human" || c.Kind=="animal") && !string.IsNullOrEmpty(c.GroundKind) && !c.Display.VFlip)visible.Add(c.Instance);
        }
        public static void Damaged(GO obj,GO attacker,string attributes,int loss)
        {
            if(!Enabled || Stage<2 || loss<=0)return;EnsureWorld();
            var cell=obj.CurrentCell;
            if(cell==null || !visible.Contains(obj.BaseID) || obj.Render==null || !obj.Render.Visible ||
                !cell.ParentZone.GetVisibility(cell.X,cell.Y))return;
            var state=new Hurt{Serial=++serial};
            // Only explicitly physical Qud attributes supply a forceful impact.
            bool forceful=(attributes??"").Split(' ').Any(a=>new[]{"Blunt","Crushing","Cutting","Piercing"}.Contains(a));
            var from=attacker==null?null:attacker.CurrentCell;
            if(forceful && from!=null && from.ParentZone==cell.ParentZone)
            {
                float dx=cell.X-from.X,dy=cell.Y-from.Y,length=(float)Math.Sqrt(dx*dx+dy*dy);
                if(length>0){state.DX=.17f*dx/length;state.DY=.17f*dy/length;}
            }
            hurt[obj.BaseID]=state;
            ProbeRunner.Record("pawn-damage.json",new{instance=obj.BaseID,serial=state.Serial,hpLoss=loss,
                attributes,forceful,offsetX=state.DX,offsetY=state.DY,gameTicks=owner.TimeTicks,world=World});
        }
        public static bool IsLayered(string kind){return kind=="human" || kind=="animal" || kind=="prop";}
        public static string Kind(GO obj)
        {
            if((!Enabled && !JoppaCoverage.Enabled) || obj==null)return null;
            if(VillageArt.Enabled){var villageKind=VillageArt.Kind(obj);if(villageKind!=null)return villageKind;}
            if(DromadArt.Enabled && obj.Blueprint=="Tam")return "human";
            if(JoppaCoverage.Enabled)
            {
                if(obj==XRLCore.Core.Game.Player.Body && obj.Body!=null && obj.Body.Anatomy=="Humanoid" &&
                    !obj.HasEffect("Asleep") && !obj.HasEffect("Prone"))return "human";
                return JoppaCoverage.Kind(obj);
            }
            if(obj.Blueprint=="WatervineFarmerJoppa" || obj==XRLCore.Core.Game.Player.Body)return "human";
            if(obj.Blueprint=="Ctesiphus")return "animal";
            if(obj.Blueprint=="Chair")return "prop";
            return null;
        }
        public static void Capture(Cell cell,GO obj,JoppaCell result)
        {
            if((!Enabled && !JoppaCoverage.Enabled) || !result.Visible || !cell.ParentZone.GetVisibility(cell.X,cell.Y))return;
            if(obj==null)return;
            EnsureWorld();
            string kind=Kind(obj);
            if(kind==null)return;
            result.Kind=kind;
            if(JoppaCoverage.Enabled)
            {
                var rule=JoppaCoverage.Rule(obj.Blueprint);
                result.AssetFamily=rule==null?null:(string)rule["asset_family"];
                var door=obj.GetPart<XRL.World.Parts.Door>();result.DoorOpen=door!=null && door.Open;
            }
            // Native BaseID is the game's own serialized instance identity.
            int id=obj.BaseID;Pose pose;
            if(!poses.TryGetValue(id,out pose)){pose=new Pose{X=cell.X,Y=cell.Y};poses[id]=pose;}
            int dx=cell.X-pose.X,dy=cell.Y-pose.Y;
            if(dx!=0 || dy!=0)pose.Facing=Math.Abs(dx)>=Math.Abs(dy)?(dx>0?1:3):(dy>0?2:0);
            pose.X=cell.X;pose.Y=cell.Y;
            result.Instance=id;result.Facing=pose.Facing;
            Hurt impact;if(hurt.TryGetValue(id,out impact))
            {result.HurtSerial=impact.Serial;result.HurtDX=impact.DX;result.HurtDY=impact.DY;}
            // Read only explicit, visible floor families; do not render objects twice.
            if(cell.Objects.Any(o=>o.Blueprint=="DirtPath" && o.Render!=null && o.Render.Visible))result.GroundKind="path";
            else if(cell.Objects.Any(o=>o.Blueprint=="DirtFloor" && o.Render!=null && o.Render.Visible) || KnownPaint(cell.PaintTile))result.GroundKind="ground";
            if(result.WaterDepth>0)result.GroundKind="water";
            NativeApparel.Capture(obj,result);
            CtesiphusArt.Capture(obj,result);
            DromadArt.Capture(obj,result);
            VillageArt.Capture(obj,result);
        }
        static bool KnownPaint(string tile)
        {
            return tile=="Tiles/tile-dirt1.png" || tile=="assets_content_textures_tiles_tile-grass1.png" ||
                tile=="Terrain/sw_grass1.bmp" || tile=="Terrain/sw_grass2.bmp" || tile=="Terrain/sw_grass3.bmp";
        }
        public static void Setup(XRLGame game)
        {
            if(!Enabled)return;
            var body=game.Player.Body;var start=body.CurrentCell;var zone=body.CurrentZone;
            var objects=new List<GO>();
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)objects.AddRange(zone.GetCell(x,y).Objects);
            Human=objects.First(o=>o.Blueprint=="WatervineFarmerJoppa");
            Animal=objects.First(o=>o.Blueprint=="Ctesiphus");Prop=objects.First(o=>o.Blueprint=="Chair");
            Place(Human,zone.GetCell(start.X-1,start.Y));Place(Animal,zone.GetCell(start.X+1,start.Y));
            Place(Prop,zone.GetCell(start.X-1,start.Y-1));
            ProbeRunner.Record("pawn-fixture.json",new{scope="Generated Joppa; three existing objects relocated only inside the isolated diagnostic",
                human=Human.BaseID,animal=Animal.BaseID,prop=Prop.BaseID,
                playerX=start.X,playerY=start.Y,operatingSystemInput=false});
        }
        public static void Place(GO obj,Cell target)
        {
            if(target==null || target.IsSolidFor(obj))throw new InvalidOperationException("Pawn fixture target is not clear");
            obj.CurrentCell.RemoveObject(obj);target.AddObject(obj);
        }
    }
}
