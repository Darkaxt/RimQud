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
        public int X,Y;
        public string Source,Kind,Resolved;
        public bool Visible,RequiresOriginal,Grass;
        public int WaterDepth,WaterVolume;
        public ConsoleChar Display;
    }
    public sealed class JoppaFrame
    {
        public int Generation,ProducerThread;
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
            int depth=0,volume=0;
            if(e.Visible && zone.GetVisibility(cell.X,cell.Y))
            {
                // Explicit known liquid-underlay adapter for visible open water.
                var liquid=cell.Objects.FirstOrDefault(o=>o.Render!=null && o.Render.Visible && o.LiquidVolume!=null &&
                    o.LiquidVolume.IsOpenVolume() && o.LiquidVolume.Volume>0 && o.LiquidVolume.Proportion("water")>0);
                if(liquid!=null)
                {
                    var v=liquid.LiquidVolume;volume=v.Volume;
                    depth=v.IsSwimmingDepth()?3:v.IsWadingDepth()?2:1;
                }
            }
            observations[cell.X+80*cell.Y]=new JoppaCell{X=cell.X,Y=cell.Y,Visible=e.Visible,
                Source=e.Visible && selected!=null?selected.Blueprint:null,
                Kind=e.Visible?Kind(selected):"original",Resolved=Appearance(display),WaterDepth=depth,WaterVolume=volume,
                Grass=e.Visible && cell.PaintTile!=null && cell.PaintTile.IndexOf("grass",StringComparison.OrdinalIgnoreCase)>=0};
        }
        public static void Publish(ScreenBuffer buffer)
        {
            if(!prepared || !ReferenceEquals(buffer,producer)){accepted=null;return;}
            if(!Monitor.IsEntered(TextConsole.BufferCS))throw new InvalidOperationException("Joppa publish outside lock");
            var cells=new JoppaCell[2000];
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)
            {
                int i=x+80*y;var observed=observations[i];
                var display=new ConsoleChar();display.Copy(TextConsole.CurrentBuffer.Buffer[x,y]);
                bool changed=observed==null || observed.Resolved!=Appearance(display);
                // A known wall-paint adapter may change the tile variant only.
                bool wallPaint=observed!=null && observed.Kind=="wall" && display.Tile!=null &&
                    display.Tile.StartsWith("Walls/wall_brinestalk",StringComparison.OrdinalIgnoreCase) &&
                    observed.Resolved.Substring(observed.Resolved.IndexOf('|'))==Appearance(display).Substring(Appearance(display).IndexOf('|'));
                bool waterPaint=observed!=null && observed.Kind=="water" && observed.WaterDepth>0 &&
                    display.Tile!=null && display.Tile.StartsWith("Liquids/Water/",StringComparison.OrdinalIgnoreCase);
                cells[i]=new JoppaCell{X=x,Y=y,Source=observed==null?null:observed.Source,
                    Visible=observed!=null && observed.Visible,Kind=observed==null?"original":observed.Kind,
                    RequiresOriginal=changed && !wallPaint && !waterPaint,Display=display,
                    Grass=observed!=null && observed.Grass,WaterDepth=observed==null?0:observed.WaterDepth,
                    WaterVolume=observed==null?0:observed.WaterVolume};
            }
            accepted=new JoppaFrame{Generation=++generation,Phase=phase,Enabled=enabled,Cells=cells,
                Hash=Hash(TextConsole.CurrentBuffer),View=TextConsole.CurrentBuffer.ViewTag,
                ExpectedView=expectedView,Zone=zone.ZoneID,ProducerThread=Thread.CurrentThread.ManagedThreadId};
            prepared=false;
        }
        public static void Consumed(ScreenBuffer buffer)
        {
            if(accepted==null || !ReferenceEquals(buffer,TextConsole.CurrentBuffer))return;
            var frame=accepted;accepted=null;
            try
            {
                if(!Monitor.IsEntered(TextConsole.BufferCS) || frame.Hash!=Hash(buffer) || frame.View!=buffer.ViewTag)
                    throw new InvalidOperationException("Joppa accepted frame mismatch");
                if(renderer==null)renderer=new JoppaRenderer();
                JObject result=renderer.Draw(frame);
                result["producerThread"]=frame.ProducerThread;
                result["consumerThread"]=Thread.CurrentThread.ManagedThreadId;
                result["submittedHash"]=frame.Hash;result["consumedHash"]=Hash(buffer);
                result["insideBufferLock"]=true;result["view"]=frame.View;
                results.Add(result);
            }
            catch(Exception ex){ExitCode=1;ProbeRunner.Record("joppa-render-failure.json",new{exception=ex.ToString()});}
            finally{consumed.Set();}
        }
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
