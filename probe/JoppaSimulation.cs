// Controlled native-map simulation. No desktop input, normal-profile installation,
// or assertion of normal gameplay/save-load parity.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using UnityEngine;
using XRL;
using XRL.Core;
using XRL.World;
using XRL.World.ZoneBuilders;
using GO = XRL.World.GameObject;

namespace RenderingTransplantProbe
{
    public sealed class JoppaCell
    {
        public int X,Y,Instance,Facing;
        public int HurtSerial;
        public float HurtDX,HurtDY;
        public EquippedAppearance[] Equipment;
        public string BodyShape,ApparelFallback,ArtFallback;
        public string Source,Kind,Resolved,GroundKind,AssetFamily;
        public bool Visible,RequiresOriginal,Grass,DoorOpen,WaterPure,WaterSupported,Explored;
        public int WaterDepth,WaterVolume;
        public int NativeLight,ConnectionMask;
        public ConsoleChar Display;
    }
    public sealed class JoppaFrame
    {
        public int Generation,ProducerThread,World;
        public string Phase,Hash,View,ExpectedView,Zone;
        public bool Enabled;
        public JoppaCell[] Cells;
    }
    public static class JoppaSimulation
    {
        public static volatile bool Done;
        public static int ExitCode;
        static int started,generation;
        static Zone zone;
        static Cell current;
        static GO selected;
        static bool rendering,prepared,enabled=true;
        static string phase,expectedView;
        static ScreenBuffer producer;
        static readonly JoppaCell[] observations=new JoppaCell[2000];
        static JoppaFrame accepted;
        static readonly ManualResetEventSlim consumed=new ManualResetEventSlim();
        static readonly JArray results=new JArray();
        static JoppaRenderer renderer;
        public static bool Gameplay { get; private set; }
        public static void BeginGameplay(Zone area,ScreenBuffer buffer)
        {
            if(!GameplayProbe.Presenting || area!=XRLCore.Core.Game.ZoneManager.ActiveZone)return;
            Gameplay=true;zone=area;producer=buffer;phase=GameplayProbe.Phase;expectedView="Stage";
            NativeApparel.BeginFrame();
            DromadArt.BeginFrame();
            VillageArt.BeginFrame();
            CurrentArt.BeginFrame();
            Array.Clear(observations,0,observations.Length);rendering=true;
        }
        public static void EndGameplay(Zone area,ScreenBuffer buffer)
        {
            if(!Gameplay || area!=zone || !ReferenceEquals(buffer,producer))return;
            rendering=false;current=null;prepared=true;
        }

        public static string Appearance(ConsoleChar c)
        {
            return (c.Tile??"")+"|"+(int)c.Char+"|"+c.Foreground+"|"+c.Background+"|"+c.Detail+
                "|"+c.HFlip+"|"+c.VFlip+"|"+c.WantsBackdrop;
        }
        static string Hash(ScreenBuffer b)
        {
            var text=new StringBuilder();
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)text.Append(Appearance(b.Buffer[x,y])).Append('\n');
            using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(text.ToString()))).Replace("-","");
        }
        public static void Enter(Cell cell)
        {
            if(!rendering || cell.ParentZone!=zone)return;
            current=cell;selected=null;
        }
        public static void Selected(GO obj)
        {
            if(rendering && current!=null && current.ParentZone==zone)selected=obj;
        }
        static string Kind(GO obj)
        {
            if(obj==null)return "original";
            if(JoppaCoverage.Enabled)return JoppaCoverage.Kind(obj);
            string n=obj.Blueprint;
            if(obj.LiquidVolume!=null && obj.LiquidVolume.IsOpenVolume() && obj.LiquidVolume.Volume>0 &&
                obj.LiquidVolume.Proportion("water")>0)return "water";
            if(n=="BrinestalkWall" || n=="WoodWall" || n=="StoneWall")return "wall";
            if(n=="DirtPath")return "path";
            if(n=="DirtFloor")return "ground";
            if(n=="Watervine")return "crop";
            if(n=="Brinestalk")return "reed";
            if(obj.HasTag("Tree"))return "tree";
            if(n=="Door")return "door";
            return "original";
        }
        public static void Leave(Cell cell,RenderEvent e)
        {
            if(!rendering || cell!=current)return;
            var display=new ConsoleChar();display.Set(e);
            bool paintedGround=selected==null && (cell.PaintTile=="Tiles/tile-dirt1.png" ||
                cell.PaintTile=="assets_content_textures_tiles_tile-grass1.png" ||
                cell.PaintTile=="Terrain/sw_grass1.bmp" || cell.PaintTile=="Terrain/sw_grass2.bmp" ||
                cell.PaintTile=="Terrain/sw_grass3.bmp");
            int depth=0,volume=0;bool waterPure=false,waterSupported=false;
            if(e.Visible && zone.GetVisibility(cell.X,cell.Y))
            {
                // Explicit known liquid-underlay adapter for visible open water.
                var liquid=cell.Objects.FirstOrDefault(o=>o.Render!=null && o.Render.Visible && o.LiquidVolume!=null &&
                    o.LiquidVolume.IsOpenVolume() && o.LiquidVolume.Volume>0 && o.LiquidVolume.Proportion("water")>0);
                if(liquid!=null)
                {
                    var v=liquid.LiquidVolume;volume=v.Volume;
                    waterPure=v.IsPureLiquid("water");
                    // Fresh water and water-primary brine share Qud's b/B
                    // surface palette. Other mixtures and frozen water stay native.
                    waterSupported=!liquid.IsFrozen() && v.GetPrimaryLiquidID()=="water" &&
                        v.ComponentLiquids.Keys.All(k=>k=="water" || k=="salt");
                    depth=v.IsSwimmingDepth()?3:v.IsWadingDepth()?2:1;
                }
            }
            var observation=new JoppaCell{X=cell.X,Y=cell.Y,Visible=e.Visible,
                Source=e.Visible && selected!=null?selected.Blueprint:null,
                Kind=e.Visible?(paintedGround?"ground":Kind(selected)):"original",Resolved=Appearance(display),WaterDepth=depth,WaterVolume=volume,WaterPure=waterPure,WaterSupported=waterSupported,
                Grass=e.Visible && cell.PaintTile!=null && cell.PaintTile.IndexOf("grass",StringComparison.OrdinalIgnoreCase)>=0};
            PawnPresentation.Capture(cell,selected,observation);
            observation.NativeLight=(int)zone.GetLight(cell.X,cell.Y);
            observation.Explored=zone.GetExplored(cell.X,cell.Y);
            if(CurrentArt.Enabled && observation.Source!=null && new[]{"BrinestalkWall","BrinestalkWallWithGearbox"}.Contains(observation.Source))
            {
                int mask=0,bit=1;
                foreach(string direction in new[]{"N","E","S","W"})
                {var next=cell.GetCellFromDirection(direction);if(next!=null && next.Objects.Any(o=>o.Blueprint=="BrinestalkWall" || o.Blueprint=="BrinestalkWallWithGearbox"))mask|=bit;bit*=2;}
                observation.ConnectionMask=mask;
            }
            observations[cell.X+80*cell.Y]=observation;
        }
        public static void Publish(ScreenBuffer buffer)
        {
            if(!prepared || !ReferenceEquals(buffer,producer)){accepted=null;return;}
            if(!Monitor.IsEntered(TextConsole.BufferCS))throw new InvalidOperationException("Joppa publish outside lock");
            NativeApparel.MutateLate();
            CtesiphusArt.MutateLate();
            DromadArt.MutateLate();
            VillageArt.MutateLate();
            if(PawnPresentation.Enabled && PawnPresentation.InjectLateMutation)
            {
                var position=PawnPresentation.Human.CurrentCell;
                var changedCell=TextConsole.CurrentBuffer.Buffer[position.X,position.Y];
                changedCell.Tile=null;changedCell.Char='!';
            }
            var cells=new JoppaCell[2000];
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)
            {
                int i=x+80*y;var observed=observations[i];
                var display=new ConsoleChar();display.Copy(TextConsole.CurrentBuffer.Buffer[x,y]);
                bool changed=observed==null || observed.Resolved!=Appearance(display);
                bool equipmentChanged=NativeApparel.Changed(i) || DromadArt.Changed(i) || VillageArt.Changed(i) || CurrentArt.Changed(i);
                bool currentPaint=CurrentArt.Enabled && observed!=null && CurrentArt.KnownFinalTile(observed.Source,display.Tile) &&
                    observed.Resolved.Substring(observed.Resolved.IndexOf('|'))==Appearance(display).Substring(Appearance(display).IndexOf('|'));
                // A known wall-paint adapter may change the tile variant only.
                bool wallPaint=observed!=null && observed.Kind=="wall" && display.Tile!=null &&
                    display.Tile.StartsWith("Walls/wall_brinestalk",StringComparison.OrdinalIgnoreCase) &&
                    observed.Resolved.Substring(observed.Resolved.IndexOf('|'))==Appearance(display).Substring(Appearance(display).IndexOf('|'));
                bool waterPaint=observed!=null && observed.Kind=="water" && observed.WaterDepth>0 &&
                    display.Tile!=null && display.Tile.StartsWith("Liquids/Water/",StringComparison.OrdinalIgnoreCase);
                cells[i]=new JoppaCell{X=x,Y=y,Source=observed==null?null:observed.Source,
                    Visible=observed!=null && observed.Visible,Kind=observed==null?"original":observed.Kind,
                    RequiresOriginal=changed && !wallPaint && !waterPaint && !currentPaint || equipmentChanged,Display=display,
                    NativeLight=observed==null?0:observed.NativeLight,ConnectionMask=observed==null?0:observed.ConnectionMask,
                    Instance=observed==null?0:observed.Instance,Facing=observed==null?2:observed.Facing,
                    HurtSerial=observed==null?0:observed.HurtSerial,HurtDX=observed==null?0:observed.HurtDX,HurtDY=observed==null?0:observed.HurtDY,
                    GroundKind=observed==null?null:observed.GroundKind,
                    AssetFamily=observed==null?null:observed.AssetFamily,DoorOpen=observed!=null && observed.DoorOpen,
                    Equipment=observed==null || equipmentChanged?null:observed.Equipment,
                    BodyShape=observed==null?null:observed.BodyShape,
                    ArtFallback=observed==null?null:observed.ArtFallback,
                    ApparelFallback=equipmentChanged?"Equipped appearance changed after observation":observed==null?null:observed.ApparelFallback,
                    Grass=observed!=null && observed.Grass,WaterDepth=observed==null?0:observed.WaterDepth,
                    WaterVolume=observed==null?0:observed.WaterVolume};
                cells[i].WaterPure=observed!=null && observed.WaterPure;
                cells[i].WaterSupported=observed!=null && observed.WaterSupported;
                cells[i].Explored=zone.GetExplored(x,y);
            }
            PawnPresentation.Accepted(cells);
            accepted=new JoppaFrame{Generation=++generation,World=PawnPresentation.World,Phase=phase,Enabled=enabled && (!Gameplay || GameplayProbe.Replacement),Cells=cells,
                Hash=Hash(TextConsole.CurrentBuffer),View=TextConsole.CurrentBuffer.ViewTag,
                ExpectedView=expectedView,Zone=zone.ZoneID,ProducerThread=Thread.CurrentThread.ManagedThreadId};
            prepared=false;
        }
        public static void Consumed(ScreenBuffer buffer)
        {
            if(Gameplay && accepted==null){GameplayProbe.HideUnmatched();return;}
            if(accepted==null || !ReferenceEquals(buffer,TextConsole.CurrentBuffer))return;
            var frame=accepted;accepted=null;
            try
            {
                if(!Monitor.IsEntered(TextConsole.BufferCS) || frame.Hash!=Hash(buffer) || frame.View!=buffer.ViewTag)
                    throw new InvalidOperationException("Joppa accepted frame mismatch");
                if(renderer==null)renderer=new JoppaRenderer();
                JObject result=renderer.Draw(frame,Gameplay);
                result["producerThread"]=frame.ProducerThread;
                result["consumerThread"]=Thread.CurrentThread.ManagedThreadId;
                result["submittedHash"]=frame.Hash;result["consumedHash"]=Hash(buffer);
                result["insideBufferLock"]=true;result["view"]=frame.View;
                if(Gameplay)GameplayProbe.Present(frame,renderer,result);else results.Add(result);
            }
            catch(Exception ex)
            {
                ExitCode=1;ProbeRunner.Record("joppa-render-failure.json",new{exception=ex.ToString()});
                if(Gameplay)GameplayProbe.PresentationFailed();
            }
            finally{consumed.Set();}
        }
        public static void TickVisuals(){if(renderer!=null)renderer.TickVisuals();}
        static void Frame(string name,bool mutate=false)
        {
            phase=name;Array.Clear(observations,0,observations.Length);consumed.Reset();rendering=true;
            try{zone.Render(producer);}finally{rendering=false;current=null;}
            if(mutate){producer.Buffer[40,12].Tile=null;producer.Buffer[40,12].Char='!';}
            prepared=true;XRLCore._Console.DrawBuffer(producer);consumed.Wait();
            if(ExitCode!=0)throw new InvalidOperationException("Joppa renderer failed; inspect diagnostic");
        }
        public static void Run()
        {
            if(Interlocked.Exchange(ref started,1)!=0)return;
            var old=XRLCore.Core.Game;string oldView=GameManager.Instance.CurrentGameView;
            try
            {
                if(!XRLCore.IsCoreThread || !SceneCapture.SelectionHookInstalled || !SceneCapture.PublishHookInstalled)
                    throw new InvalidOperationException("Required core thread/hooks absent");
                var game=new XRLGame();XRLCore.Core.Game=game;game.CreateNewGame();
                game.GameID="RimQudJoppaProbe";game.IntGameState["WorldSeed"]=11619;
                zone=new Zone(80,25);zone.ZoneID="JoppaWorld.11.22.1.1.10";
                game.ZoneManager.ActiveZone=zone;game.ZoneManager.CachedZones[zone.ZoneID]=zone;
                // Explicit controlled fill, not a claim of full seeded-world generation.
                for(int y=0;y<25;y++)for(int x=0;x<80;x++)zone.GetCell(x,y).AddObject("DirtFloor");
                var map=new MapBuilder("Joppa.rpm");
                int placements=0;
                for(int y=0;y<25;y++)for(int x=0;x<80;x++)placements+=map.Map.Cells[x,y].Objects.Count;
                if(!map.BuildZone(zone))throw new InvalidOperationException("Native Joppa map build failed");
                zone.Built=true;zone.ExploreAll();zone.VisAll();zone.LightAll();
                var body=zone.GetCell(40,12).AddObject("WatervineFarmerJoppa");game.Player._Body=body;
                var counts=new Dictionary<string,int>();
                for(int y=0;y<25;y++)for(int x=0;x<80;x++)foreach(var obj in zone.GetCell(x,y).Objects)
                {if(!counts.ContainsKey(obj.Blueprint))counts[obj.Blueprint]=0;counts[obj.Blueprint]++;}
                ProbeRunner.Record("joppa-map.json",new{width=80,height=25,placements,objects=counts,
                    map="Joppa.rpm",fill="DirtFloor",normalWorldGeneration=false});
                expectedView=oldView;producer=ScreenBuffer.create(80,25);
                Frame("baseline");
                if(JoppaCoverage.Enabled)
                {
                    var fixtures=JoppaCoverage.PlaceVariants(zone);Frame("coverage-props-placed");
                    foreach(var obj in fixtures.Keys)PawnPresentation.Place(obj,zone.GetCell(obj.CurrentCell.X,obj.CurrentCell.Y+1));
                    Frame("coverage-props-south");
                    foreach(var obj in fixtures.Keys)PawnPresentation.Place(obj,zone.GetCell(obj.CurrentCell.X+1,obj.CurrentCell.Y));
                    Frame("coverage-props-east");
                    foreach(var obj in fixtures.Keys)PawnPresentation.Place(obj,zone.GetCell(obj.CurrentCell.X,obj.CurrentCell.Y-1));
                    Frame("coverage-props-north");
                    var first=fixtures.Keys.First();first.Render.VFlip=true;Frame("coverage-unsupported-flip");first.Render.VFlip=false;
                    foreach(var pair in fixtures)PawnPresentation.Place(pair.Key,pair.Value);
                    Frame("coverage-props-restored");
                    var door=Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects)
                        .First(o=>o.Blueprint=="Door").GetPart<XRL.World.Parts.Door>();
                    door.PerformOpen();Frame("coverage-door-open");door.PerformClose();Frame("coverage-door-closed");
                }
                var sample=Enumerable.Range(0,2000).SelectMany(i=>zone.GetCell(i%80,i/80).Objects)
                    .First(o=>o.Blueprint=="Pond").LiquidVolume;
                int initialVolume=sample.Volume;
                var thresholds=new JArray();
                foreach(int volume in new[]{199,200,1999,2000})
                {
                    sample.Volume=volume;thresholds.Add(JObject.FromObject(new{volume,wading=sample.IsWadingDepth(),swimming=sample.IsSwimmingDepth()}));
                }
                sample.Volume=4000;Frame("liquid-depth-deep");
                sample.Volume=initialVolume;Frame("liquid-depth-restored");
                ProbeRunner.Record("joppa-liquid-thresholds.json",thresholds);
                zone.GetCell(40,12).RemoveObject(body);zone.GetCell(41,12).AddObject(body);XRLCore.CurrentFrame++;
                Frame("actor-moved");
                for(int y=2;y<6;y++)for(int x=2;x<10;x++)
                {zone.SetVisibility(x,y,false);zone.ExploredMap[x+80*y]=false;zone.SetLight(x,y,LightLevel.None);}
                Frame("visibility-changed");zone.ExploreAll();zone.VisAll();zone.LightAll();
                Frame("late-buffer-mutation",true);
                enabled=false;Frame("replacement-disabled");enabled=true;
                GameManager.Instance.CurrentGameView="Popup:Text";Frame("unrelated-view");
                GameManager.Instance.CurrentGameView=oldView;
                var joppa=zone;var other=new Zone(80,25);other.ZoneID="RimQudProbe.Other";
                game.ZoneManager.ActiveZone=other;zone=other;zone.ExploreAll();zone.VisAll();zone.LightAll();Frame("other-zone");
                zone=joppa;game.ZoneManager.ActiveZone=zone;Frame("zone-reentered");
                zone.GetCell(41,12).RemoveObject(body);zone.GetCell(40,12).AddObject(body);XRLCore.CurrentFrame++;
                Frame("baseline-restored");
                ProbeRunner.Record("joppa-results.json",new{frames=results,scope="Native authored-map offscreen simulation; gameplay input/save-load unverified"});
            }
            catch(Exception ex){ExitCode=1;ProbeRunner.Record("joppa-failure.json",new{exception=ex.ToString()});}
            finally
            {
                rendering=prepared=false;accepted=null;XRLCore.Core.Game=old;
                GameManager.Instance.CurrentGameView=oldView;Done=true;
            }
        }
        public static void DisposeRenderer(){if(renderer!=null){renderer.Dispose();renderer=null;}}
    }
}
