// A bounded diagnostic of the real Qud renderer, not a replacement renderer.
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Reflection.Emit;
using System.Security.Cryptography;
using System.Text;
using System.Threading;
using ConsoleLib.Console;
using HarmonyLib;
using Newtonsoft.Json.Linq;
using XRL;
using XRL.Core;
using XRL.World;
using GO = XRL.World.GameObject;

namespace RenderingTransplantProbe
{
    [HarmonyPatch(typeof(XRLCore), "LoadEverything")]
    public static class CaptureReady
    {
        static void Postfix()
        {
            if (Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE") == "capture") SceneCapture.Run();
        }
    }

    [HarmonyPatch(typeof(Cell), "Render", new Type[] { typeof(RenderEvent),typeof(bool),typeof(LightLevel),
        typeof(bool),typeof(bool),typeof(bool),typeof(List<GO>) })]
    public static class SelectedSourceHook
    {
        static void Prefix(Cell __instance) { SceneCapture.Enter(__instance); }
        static void Postfix(Cell __instance, RenderEvent E) { SceneCapture.Leave(__instance,E); }
        static IEnumerable<CodeInstruction> Transpiler(IEnumerable<CodeInstruction> instructions)
        {
            var code=instructions.ToList(); bool radar=false; int anchors=0;
            foreach (var instruction in code)
            {
                var method=instruction.operand as MethodInfo;
                if (method!=null && method.DeclaringType==typeof(Cell) && method.Name=="GetRadarReveal") radar=true;
                var field=instruction.operand as FieldInfo;
                bool renderRead=(field!=null && field.DeclaringType==typeof(GO) && field.Name=="Render") ||
                    (method!=null && method.DeclaringType==typeof(GO) && method.Name=="get_Render");
                if (radar && renderRead && anchors==0)
                {
                    // Selected source is already on the evaluation stack. Observe
                    // a duplicate, without depending on a decompiler's local index.
                    var dup=new CodeInstruction(OpCodes.Dup);
                    dup.labels.AddRange(instruction.labels); instruction.labels.Clear();
                    yield return dup;
                    yield return new CodeInstruction(OpCodes.Call,AccessTools.Method(typeof(SceneCapture),"Selected"));
                    anchors++;
                }
                yield return instruction;
            }
            if (anchors!=1) throw new InvalidOperationException("Cell.Render selection anchor changed");
            SceneCapture.SelectionHookInstalled=true;
        }
    }

    [HarmonyPatch(typeof(TextConsole), "DrawBuffer")]
    public static class AcceptedFrameHook
    {
        static IEnumerable<CodeInstruction> Transpiler(IEnumerable<CodeInstruction> instructions)
        {
            int anchors=0;
            foreach (var instruction in instructions)
            {
                yield return instruction;
                var method=instruction.operand as MethodInfo;
                if (method!=null && method.DeclaringType==typeof(ScreenBuffer) && method.Name=="Copy")
                {
                    yield return new CodeInstruction(OpCodes.Ldarg_1);
                    yield return new CodeInstruction(OpCodes.Call,AccessTools.Method(typeof(SceneCapture),"Publish"));
                    anchors++;
                }
            }
            if (anchors!=1) throw new InvalidOperationException("DrawBuffer copy anchor changed");
            SceneCapture.PublishHookInstalled=true;
        }
    }

    [HarmonyPatch(typeof(ConsoleChar), "AfterRender")]
    public static class ConsumedFrameHook
    {
        static void Postfix(int x,int y,ScreenBuffer buffer)
        {
            if (x==79 && y==24) SceneCapture.Consumed(buffer);
        }
    }

    public static class SceneCapture
    {
        public static bool SelectionHookInstalled,PublishHookInstalled;
        public static volatile bool Done;
        public static int ExitCode;
        static int started,generation;
        static bool rendering,prepared;
        static Zone zone;
        static ScreenBuffer producer;
        static string phase;
        static Cell current;
        static GO selected;
        static readonly List<JObject> cells=new List<JObject>();
        static readonly JArray frames=new JArray();
        static JObject accepted;
        static readonly ManualResetEventSlim consumed=new ManualResetEventSlim(false);

        static string Appearance(ConsoleChar c)
        {
            return (c.Tile??"")+"|"+(int)c.Char+"|"+c.Foreground+"|"+c.Background+"|"+c.Detail+
                "|"+c.HFlip+"|"+c.VFlip+"|"+c.WantsBackdrop;
        }
        static string Hash(ScreenBuffer buffer)
        {
            var text=new StringBuilder();
            for(int y=0;y<25;y++)for(int x=0;x<80;x++) text.Append(Appearance(buffer.Buffer[x,y])).Append('\n');
            using(var sha=SHA256.Create()) return BitConverter.ToString(sha.ComputeHash(Encoding.UTF8.GetBytes(text.ToString()))).Replace("-","");
        }
        public static void Enter(Cell cell)
        {
            if(!rendering || cell.ParentZone!=zone) return;
            current=cell; selected=null;
        }
        public static void Selected(GO obj)
        {
            if(rendering && current!=null && current.ParentZone==zone) selected=obj;
        }
        public static void Leave(Cell cell,RenderEvent e)
        {
            if(!rendering || cell!=current || cell.X<8 || cell.X>14 || cell.Y<8 || cell.Y>9) return;
            var c=new ConsoleChar(); c.Set(e);
            cells.Add(JObject.FromObject(new {x=cell.X,y=cell.Y,visible=e.Visible,
                // Conservative public payload: invisible cells retain appearance
                // but never expose an object identity from the raw world.
                source=e.Visible && selected!=null ? selected.Blueprint : null,
                resolved=Appearance(c),tile=c.Tile,paintRequested=e.WantsToPaint}));
        }
        public static void Publish(ScreenBuffer buffer)
        {
            if(!prepared || !ReferenceEquals(buffer,producer)) { accepted=null; return; }
            if(!Monitor.IsEntered(TextConsole.BufferCS)) throw new InvalidOperationException("Publish outside BufferCS");
            var rows=new JArray();
            foreach(var cell in cells)
            {
                var copy=(JObject)cell.DeepClone(); int x=(int)copy["x"],y=(int)copy["y"];
                string submitted=Appearance(TextConsole.CurrentBuffer.Buffer[x,y]);
                copy["submitted"]=submitted;
                copy["requiresOriginal"]=(string)copy["resolved"]!=submitted;
                rows.Add(copy);
            }
            accepted=JObject.FromObject(new {generation=Interlocked.Increment(ref generation),phase,
                zone=zone.ZoneID,producerThread=Thread.CurrentThread.ManagedThreadId,
                publishInsideBufferLock=true,submittedHash=Hash(TextConsole.CurrentBuffer)});
            accepted["cells"]=rows;
            prepared=false;
        }
        public static void Consumed(ScreenBuffer buffer)
        {
            if(accepted==null || !ReferenceEquals(buffer,TextConsole.CurrentBuffer)) return;
            if(!Monitor.IsEntered(TextConsole.BufferCS)) throw new InvalidOperationException("Consume outside BufferCS");
            accepted["consumerThread"]=Thread.CurrentThread.ManagedThreadId;
            accepted["consumeInsideBufferLock"]=true;
            accepted["view"]=buffer.ViewTag;
            accepted["consumedHash"]=Hash(buffer);
            accepted["matchesSubmitted"]=(string)accepted["submittedHash"]==(string)accepted["consumedHash"];
            frames.Add(accepted); accepted=null;
            consumed.Set();
        }

        static void Frame(string name,bool lateMutation)
        {
            phase=name; cells.Clear(); consumed.Reset(); rendering=true;
            try { zone.Render(producer); }
            finally { rendering=false; current=null; }
            if(lateMutation) { producer.Buffer[10,8].Tile=null; producer.Buffer[10,8].Char='!'; }
            prepared=true;
            XRLCore._Console.DrawBuffer(producer);
            // The game thread waits for the actual Unity consumer; no sleeps or
            // elapsed-time inference, and both sides use the existing buffer lock.
            consumed.Wait();
        }

        public static void Run()
        {
            if(Interlocked.Exchange(ref started,1)!=0) return;
            XRLGame old=XRLCore.Core.Game;
            try
            {
                if(!XRLCore.IsCoreThread || !SelectionHookInstalled || !PublishHookInstalled)
                    throw new InvalidOperationException("Required thread/hooks not established");
                var game=new XRLGame(); XRLCore.Core.Game=game;
                game.Player=new GamePlayer();
                zone=new Zone(80,25); zone.ZoneID="JoppaWorld.11.22.1.1.10";
                game.ZoneManager.ActiveZone=zone;
                zone.ExploreAll(); zone.VisAll(); zone.LightAll();
                for(int y=8;y<=9;y++)for(int x=8;x<=14;x++) zone.GetCell(x,y).AddObject("DirtPath");
                zone.GetCell(9,8).AddObject("BrinestalkWall");
                zone.GetCell(10,8).AddObject("Watervine");
                var actor=zone.GetCell(11,8).AddObject("WatervineFarmerJoppa");
                zone.GetCell(12,8).AddObject("Pond");
                var hidden=zone.GetCell(13,8).AddObject("WatervineFarmerJoppa"); hidden.Render.Visible=false;
                zone.GetCell(14,8).AddObject("WatervineFarmerJoppa");
                zone.SetVisibility(14,8,false); zone.ExploredMap[14+8*80]=false; zone.SetLight(14,8,LightLevel.None);
                var body=zone.GetCell(8,9).AddObject("WatervineFarmerJoppa"); game.Player._Body=body;
                producer=ScreenBuffer.create(80,25);
                Frame("baseline",false);
                Frame("late-buffer-mutation",true);
                zone.GetCell(11,8).RemoveObject(actor); zone.GetCell(11,9).AddObject(actor);
                XRLCore.CurrentFrame++;
                Frame("actor-moved",false);
                ProbeRunner.Record("capture.json",new {selectionHook=SelectionHookInstalled,
                    publicationHook=PublishHookInstalled,frames});
            }
            catch(Exception ex)
            {
                ExitCode=1; ProbeRunner.Record("capture-failure.json",new {exception=ex.ToString()});
            }
            finally
            {
                rendering=prepared=false; accepted=null; XRLCore.Core.Game=old;
                Done=true;
            }
        }
    }
}
