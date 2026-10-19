// Narrow known-layer adapter and native-world diagnostic for the first pawn scene.
using System;
using System.Collections.Generic;
using System.Linq;
using XRL;
using XRL.Core;
using XRL.World;
using GO=XRL.World.GameObject;

namespace RenderingTransplantProbe
{
    public static class PawnPresentation
    {
        public static bool Enabled { get { return Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")=="pawns"; } }
        sealed class Pose { public int X,Y,Facing=2; }
        static readonly Dictionary<int,Pose> poses=new Dictionary<int,Pose>();
        static XRLGame owner;
        public static GO Human,Animal,Prop;
        public static bool InjectLateMutation;
        public static bool IsLayered(string kind){return kind=="human" || kind=="animal" || kind=="prop";}
        public static string Kind(GO obj)
        {
            if(!Enabled || obj==null)return null;
            if(obj.Blueprint=="WatervineFarmerJoppa" || obj==XRLCore.Core.Game.Player.Body)return "human";
            if(obj.Blueprint=="Ctesiphus")return "animal";
            if(obj.Blueprint=="Chair")return "prop";
            return null;
        }
        public static void Capture(Cell cell,GO obj,JoppaCell result)
        {
            if(!Enabled || !result.Visible || !cell.ParentZone.GetVisibility(cell.X,cell.Y))return;
            if(owner!=XRLCore.Core.Game){owner=XRLCore.Core.Game;poses.Clear();}
            string kind=Kind(obj);
            if(kind==null)return;
            result.Kind=kind;
            // Native BaseID is the game's own serialized instance identity.
            int id=obj.BaseID;Pose pose;
            if(!poses.TryGetValue(id,out pose)){pose=new Pose{X=cell.X,Y=cell.Y};poses[id]=pose;}
            int dx=cell.X-pose.X,dy=cell.Y-pose.Y;
            if(dx!=0 || dy!=0)pose.Facing=Math.Abs(dx)>=Math.Abs(dy)?(dx>0?1:3):(dy>0?2:0);
            pose.X=cell.X;pose.Y=cell.Y;
            result.Instance=id;result.Facing=pose.Facing;
            // Read only explicit, visible floor families; do not render objects twice.
            if(cell.Objects.Any(o=>o.Blueprint=="DirtPath" && o.Render!=null && o.Render.Visible))result.GroundKind="path";
            else if(cell.Objects.Any(o=>o.Blueprint=="DirtFloor" && o.Render!=null && o.Render.Visible) || KnownPaint(cell.PaintTile))result.GroundKind="ground";
            if(result.WaterDepth>0)result.GroundKind="water";
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
