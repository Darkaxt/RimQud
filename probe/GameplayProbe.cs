// Hidden native-game bootstrap and lifecycle diagnostics; never OS input.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using HarmonyLib;
using UnityEngine;
using UnityEngine.Rendering;
using XRL;
using XRL.Core;
using XRL.CharacterBuilds;
using XRL.CharacterBuilds.Qud;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using XRL.World;
using XRL.UI;

namespace RenderingTransplantProbe
{
    [HarmonyPatch(typeof(XRLCore),"NewGame")]
    public static class ReviewGameStarted
    {
        static void Postfix(XRLGame __result){GameplayProbe.StartReview(__result);}
    }
    [HarmonyPatch(typeof(XRLCore),"RunGame")]
    public static class ReviewGameEnded
    {
        static void Postfix()
        {
            if(GameplayProbe.ActiveMode && !GameplayProbe.Automated && GameplayProbe.Presenting)
                GameplayProbe.Done=true;
        }
    }
    [HarmonyPatch(typeof(Keyboard),"kbhit")]
    public static class DiagnosticInput
    {
        static void Prefix(){GameplayProbe.InjectInput();}
    }
    [HarmonyPatch(typeof(ConsoleChar),"BeforeRender")]
    public static class RestoreNativeCell
    {
        static void Prefix(int x,int y){GameplayProbe.RestoreCell(x,y);}
    }
    [HarmonyPatch(typeof(Look),"ShowLooker")]
    public static class DiagnosticLook
    {
        static void Prefix(int StartX,int StartY)
        {
            if(!GameplayProbe.Presenting)return;
            GameplayProbe.LookX=StartX;GameplayProbe.LookY=StartY;
        }
    }
    [HarmonyPatch(typeof(Qud.UI.PopupMessage),"ShowPopup")]
    public static class DiagnosticPopup
    {
        static void Postfix(Qud.UI.PopupMessage __instance, string message, List<Qud.UI.QudMenuItem> buttons)
        {
            if(!GameplayProbe.ActiveMode)return;
            ProbeRunner.Record("gameplay-popup.json",new{message,commands=buttons==null?new string[0]:buttons.Select(b=>b.command).ToArray()});
            bool joppaIntro=message!=null && message.Contains("you arrive at the oasis-hamlet of &GJoppa&y") &&
                message.EndsWith("rises above the fray and pierces the cloud-ribboned sky.");
            if((message=="You embark for the caves of Qud." || joppaIntro) && buttons!=null && buttons.Count==1 && buttons[0].command=="Accept")
            {
                __instance.OnActivateCommand(buttons[0]);return;
            }
            // In automated diagnostics, unknown prompts stop for inspection.
            // Interactive review leaves them with Qud's normal controls.
            if(GameplayProbe.Automated){GameplayProbe.ExitCode=2;GameplayProbe.Done=true;}
        }
    }
    [HarmonyPatch(typeof(EmbarkBuilder),"Begin")]
    public static class DiagnosticEmbark
    {
        static bool Prefix(ref Task<EmbarkInfo> __result)
        {
            if(!GameplayProbe.ActiveMode)return true;
            EmbarkBuilderConfiguration.Init();
            string code=EmbarkBuilderConfiguration.activeModules.OfType<QudPregenModule>().First().pregens.Values.First().Code;
            var builder=EmbarkBuilder.FromCode(code,true);builder.SkippingUIUpdates=true;
            // Native build codes deliberately omit these UI-owned selections.
            builder.GetModule<QudGamemodeModule>().setDataDirect(new QudGamemodeModuleData{Mode="Classic"});
            builder.GetModule<QudChartypeModule>().setDataDirect(new QudChartypeModuleData{type="Custom"});
            builder.GetModule<QudChooseStartingLocationModule>().setDataDirect(new QudChooseStartingLocationModuleData("Joppa"));
            var modules=(List<AbstractEmbarkBuilderModule>)AccessTools.Field(typeof(EmbarkBuilder),"modules").GetValue(builder);
            foreach(var module in modules){if(module.shouldBeEnabled())module.enable();else module.disable();}
            var info=builder.info;info.GameSeed="RimQud-Joppa-20261019";
            info._modules.AddRange(modules.Where(m=>m.enabled));
            foreach(var module in info._modules){var data=module.getData();if(data!=null)info._data.Add(data);}
            ProbeRunner.Record("gameplay-embark.json",new{pregen="First installed native pregen",startingLocation="Joppa",
                modules=info._modules.Select(m=>m.GetType().Name).ToArray(),silent=true});
            __result=Task.FromResult(info);return false;
        }
    }
    public static class GameplayProbe
    {
        public static volatile bool Done;
        public static int ExitCode;
        static int started;
        public static bool Automated { get { return Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")=="gameplay" || PawnPresentation.Enabled; } }
        public static bool ActiveMode { get { return Automated || Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")=="review"; } }
        static string lastView;
        static string reviewState;
        public static volatile bool Presenting,Replacement=true;
        public static volatile string Phase="boot";
        public static int LookX=-1,LookY=-1;
        static int targetX,targetY;
        static int inputSerial;
        static bool escaped;
        static volatile bool lookReady,menuSeen,awaiting;
        static readonly ManualResetEventSlim presented=new ManualResetEventSlim();
        static readonly Queue<string> commands=new Queue<string>();
        static readonly JArray frames=new JArray();
        static UnityEngine.GameObject overlay;
        static Mesh overlayMesh;
        static Material overlayMaterial;
        static bool cameraHook;
        static readonly Renderer[] hidden=new Renderer[2000];
        static readonly bool[] previous=new bool[2000];
        static readonly System.Reflection.MethodInfo flush=AccessTools.Method(typeof(exStandaloneSprite),"LateUpdate");
        static readonly System.Reflection.FieldInfo layoutRefresh=AccessTools.Field(typeof(LetterboxCamera),"_Refresh");
        static Action pendingCapture;
        static readonly ManualResetEventSlim reactionFinished=new ManualResetEventSlim();
        static volatile bool reactionArmed;
        static int reactionId;
        static string reactionName;
        static bool reactionMid;
        static readonly JArray reactions=new JArray();
        sealed class ReactionReadback { public JObject State;public byte[] Pixels;public int Width,Height; }
        static readonly List<ReactionReadback> reactionReadbacks=new List<ReactionReadback>();
        static int pendingReadbacks;
        static bool reactionEnded;
        public static void ObserveReaction(JoppaRenderer renderer)
        {
            if(!reactionArmed)return;
            try
            {
                var state=renderer.VisualState(reactionId);
                if(state==null)throw new InvalidOperationException("Damaged native actor has no mapped visual state");
                float ticks=(float)state["visualTicks"];
                if(!reactionMid && ticks>=8 && ticks<16){SampleReaction(renderer,"mid");reactionMid=true;}
                if((bool)state["finished"])
                {reactionEnded=true;reactionArmed=false;SampleReaction(renderer,"end");}
            }
            catch(Exception ex)
            {
                ExitCode=1;reactionArmed=false;ProbeRunner.Record("reaction-failure.json",new{exception=ex.ToString()});reactionFinished.Set();
            }
        }
        static void SampleReaction(JoppaRenderer renderer,string sample)
        {
            var state=renderer.VisualState(reactionId);
            if(state==null)throw new InvalidOperationException("Actual HP loss was not bridged to a selected actor");
            state["sample"]=sample;state["fixture"]=reactionName;state["gameTicks"]=XRLCore.Core.Game.TimeTicks;
            string file="gameplay-hurt-"+reactionName+"-"+sample+".png";state["image"]=file;
            var cam=GameManager.MapCamera;var old=cam.targetTexture;
            var target=new RenderTexture(Screen.width,Screen.height,24,RenderTextureFormat.ARGB32);
            var readback=new ReactionReadback{State=state,Width=Screen.width,Height=Screen.height};
            reactionReadbacks.Add(readback);pendingReadbacks++;
            try{cam.targetTexture=target;cam.Render();}finally{cam.targetTexture=old;}
            AsyncGPUReadback.Request(target,0,TextureFormat.RGBA32,request=>
            {
                try
                {
                    if(request.hasError)throw new InvalidOperationException("Reaction GPU readback failed");
                    readback.Pixels=request.GetData<byte>().ToArray();
                }
                catch(Exception ex){ExitCode=1;ProbeRunner.Record("reaction-failure.json",new{exception=ex.ToString()});}
                finally
                {
                    target.Release();UnityEngine.Object.DestroyImmediate(target);pendingReadbacks--;
                    if(pendingReadbacks==0 && reactionEnded)
                    {
                        try
                        {
                            foreach(var item in reactionReadbacks)
                            {
                                if(item.Pixels==null)throw new InvalidOperationException("Missing reaction pixels");
                                var image=new Texture2D(item.Width,item.Height,TextureFormat.RGBA32,false);
                                try
                                {
                                    image.LoadRawTextureData(item.Pixels);image.Apply();
                                    File.WriteAllBytes(Path.Combine(ProbeRunner.Root,(string)item.State["image"]),image.EncodeToPNG());
                                }
                                finally{UnityEngine.Object.DestroyImmediate(image);}
                                reactions.Add(item.State);
                            }
                            reactionReadbacks.Clear();ProbeRunner.Record("hurt-samples.json",reactions);
                        }
                        catch(Exception ex){ExitCode=1;ProbeRunner.Record("reaction-failure.json",new{exception=ex.ToString()});}
                        finally{reactionFinished.Set();}
                    }
                }
            });
        }
        public static void DamageFixture(XRL.World.GameObject victim,string name)
        {
            reactionId=victim.BaseID;reactionName=name;reactionMid=false;reactionEnded=false;reactionFinished.Reset();
            int before=victim.Stat("Hitpoints"),amount=1;long ticks=XRLCore.Core.Game.TimeTicks;
            // A native environmental event has an origin but no player attacker.
            // The earlier player-attributed fixture correctly angered native NPCs.
            victim.TakeDamage(ref amount,Attributes:"Blunt",Source:PawnPresentation.Prop,
                Message:"",Environmental:true,NoSetTarget:true,UsePopups:false);
            if(victim.Stat("Hitpoints")!=before-1)throw new InvalidOperationException("Fixture did not lose one native HP");
            RenderPhase("hurt-"+name+"-start");reactionFinished.Wait();
            if(ExitCode!=0 || !reactionMid || XRLCore.Core.Game.TimeTicks!=ticks)
                throw new InvalidOperationException("Native hurt reaction did not finish during input wait with a midpoint sample");
            RenderPhase("hurt-"+name+"-ended");
            ProbeRunner.Record("hurt-"+name+"-result.json",new{instance=victim.BaseID,hpBefore=before,
                hpAfter=victim.Stat("Hitpoints"),startTicks=ticks,endTicks=XRLCore.Core.Game.TimeTicks,
                actualQudDamage=true,simulationAdvanced=false,environmentalSource=PawnPresentation.Prop.BaseID,
                postureMapping="Unchanged upright graphic; HP loss does not select a downed or dead graphic"});
        }

        public static void CaptureAfterLayout()
        {
            if(pendingCapture==null)return;
            var layout=GameManager.MapCamera.GetComponent<LetterboxCamera>();
            // Native layout owns a view-transition delay and refresh state. Wait
            // for its actual completion, not an invented sleep or elapsed deadline.
            if(layout.UpdateDelay>0 || (bool)layoutRefresh.GetValue(layout))return;
            var capture=pendingCapture;pendingCapture=null;capture();
        }

        public static void RestoreCell(int x,int y)
        {
            int i=x+80*y;
            if(hidden[i]!=null){hidden[i].enabled=previous[i];hidden[i]=null;}
        }
        static void Hide()
        {
            if(overlay!=null)overlay.SetActive(false);
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)RestoreCell(x,y);
        }
        public static void HideUnmatched(){Hide();}
        static void Cover(bool[] covered)
        {
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)if(covered[x+80*y])
            {
                int i=x+80*y;var r=GameManager.Instance.ConsoleCharacter[x,y].GetComponent<Renderer>();
                hidden[i]=r;previous[i]=r.enabled;r.enabled=false;
            }
            overlay.SetActive(true);
        }
        static void BeforeCamera(Camera camera)
        {
            if(camera!=GameManager.MapCamera)return;
            if(!Presenting || GameManager.Instance.CurrentGameView!="Stage"){Hide();return;}
            if(overlay!=null && overlay.activeSelf)
                foreach(var renderer in hidden)if(renderer!=null)renderer.enabled=false;
        }
        static void CreateOverlay(RenderTexture texture)
        {
            if(overlay!=null)return;
            var shader=Shader.Find("UI/Default");
            if(shader==null || !shader.isSupported)throw new InvalidOperationException("Native transparent presentation shader unavailable");
            overlayMaterial=new Material(shader);overlayMaterial.mainTexture=texture;
            overlayMesh=new Mesh();overlayMesh.vertices=new[]{new Vector3(-640,-300,0),new Vector3(-640,300,0),
                new Vector3(640,300,0),new Vector3(640,-300,0)};
            overlayMesh.uv=new[]{new Vector2(0,0),new Vector2(0,1),new Vector2(1,1),new Vector2(1,0)};
            overlayMesh.triangles=new[]{0,1,2,0,2,3};overlayMesh.RecalculateBounds();
            overlay=new UnityEngine.GameObject("RimQudGameplayPresentation");overlay.transform.position=new Vector3(0,0,90);
            overlay.AddComponent<MeshFilter>().sharedMesh=overlayMesh;
            overlay.AddComponent<MeshRenderer>().sharedMaterial=overlayMaterial;
            Camera.onPreCull+=BeforeCamera;cameraHook=true;
            // No collider or event handler: Qud keeps its existing tile input targets.
        }
        static string Capture(string name)
        {
            var cam=GameManager.MapCamera;var old=cam.targetTexture;
            var target=new RenderTexture(Screen.width,Screen.height,24,RenderTextureFormat.ARGB32);
            var oldActive=RenderTexture.active;Texture2D image=null;
            try
            {
                foreach(var sprite in GameManager.Instance.ConsoleCharacter)flush.Invoke(sprite,null);
                cam.targetTexture=target;cam.Render();RenderTexture.active=target;
                image=new Texture2D(target.width,target.height,TextureFormat.RGBA32,false);
                image.ReadPixels(new Rect(0,0,target.width,target.height),0,0);image.Apply();
                string filename="gameplay-"+name+".png";
                File.WriteAllBytes(Path.Combine(ProbeRunner.Root,filename),image.EncodeToPNG());return filename;
            }
            finally
            {
                cam.targetTexture=old;RenderTexture.active=oldActive;
                if(image!=null)UnityEngine.Object.DestroyImmediate(image);
                target.Release();UnityEngine.Object.DestroyImmediate(target);
            }
        }
        public static void Present(JoppaFrame frame,JoppaRenderer renderer,JObject result)
        {
            Hide();
            bool show=(bool)result["eligible"] && GameManager.Instance.CurrentGameView=="Stage";
            CreateOverlay(renderer.Texture);
            if(show)Cover(renderer.Covered);
            if(frame.View=="Looker")
            {
                lookReady=true;
                ProbeRunner.Record(Phase=="apparel-look"?"apparel-target-view.json":Phase=="raycat-look"?"raycat-target-view.json":Phase=="dromad-look"?"dromad-target-view.json":"gameplay-target.json",new{view=frame.View,x=LookX,y=LookY,
                    overlayVisible=overlay.activeSelf,nativeHiddenCells=hidden.Count(r=>r!=null)});
            }
            if(!awaiting || frame.Phase!=Phase)return;
            if(PawnPresentation.Stage>=2 && Phase=="hurt-"+reactionName+"-start")
            {
                SampleReaction(renderer,"start");reactionArmed=true;
                awaiting=false;presented.Set();return;
            }
            Action capture=()=>{try
            {
                if(PawnPresentation.Enabled)
                {
                    foreach(JObject cell in (JArray)result["cells"])
                    {
                        if(!PawnPresentation.IsLayered((string)cell["kind"]))continue;
                        var point=GameManager.Instance.getScreenTileCenter((int)cell["x"],(int)cell["y"]);
                        cell["screenX"]=point.x;cell["screenY"]=point.y;
                    }
                    var camera=GameManager.MapCamera;
                    result["camera"]=new JObject{{"width",Screen.width},{"height",Screen.height},
                        {"orthographicSize",camera.orthographicSize},{"positionX",camera.transform.position.x},
                        {"positionY",camera.transform.position.y},{"nativeLayoutReady",true}};
                }
                Hide();string original=Capture(Phase+"-original");
                if(show)Cover(renderer.Covered);
                string replacement=Capture(Phase+"-replacement");
                result["original"]=original;result["replacement"]=replacement;
                result["nativeCamera"]=GameManager.MapCamera.name;
                result["overlayVisible"]=overlay.activeSelf;
                result["nativeHiddenCells"]=hidden.Count(r=>r!=null);
                result["nativeRenderersSuppressed"]=hidden.Where(r=>r!=null).All(r=>!r.enabled);
                result["audioPaused"]=AudioListener.pause;
                result["listenerVolume"]=AudioListener.volume;
                result["masterVolume"]=SoundManager.MasterVolume;
                if(Phase=="baseline")
                {
                    var old=RenderTexture.active;RenderTexture.active=renderer.Texture;
                    var layer=new Texture2D(renderer.Texture.width,renderer.Texture.height,TextureFormat.RGBA32,false,true);
                    try
                    {
                        layer.ReadPixels(new Rect(0,0,layer.width,layer.height),0,0);layer.Apply();
                        File.WriteAllBytes(Path.Combine(ProbeRunner.Root,"gameplay-layer.png"),layer.EncodeToPNG());
                    }
                    finally{RenderTexture.active=old;UnityEngine.Object.DestroyImmediate(layer);}
                }
                var body=XRLCore.Core.Game.Player.Body;
                result["player"]=JObject.FromObject(new{x=body.CurrentCell.X,y=body.CurrentCell.Y});
                var tile=GameManager.Instance.ConsoleCharacter[targetX,targetY];
                var behavior=tile.GetComponent<TileBehavior>();
                var screen=GameManager.Instance.getScreenTileCenter(targetX,targetY);
                result["targetBinding"]=JObject.FromObject(new{x=behavior.x,y=behavior.y,
                    enabled=behavior.enabled,colliders=tile.GetComponents<Collider>().Length,
                    screenX=screen.x,screenY=screen.y,screenZ=screen.z});
                frames.Add(result);ProbeRunner.Record("gameplay-frames.json",frames);
            }
            catch(Exception ex)
            {
                ExitCode=1;ProbeRunner.Record("gameplay-capture-failure.json",new{exception=ex.ToString()});
            }
            finally{awaiting=false;presented.Set();}};
            if(PawnPresentation.Enabled)pendingCapture=capture;else capture();
        }
        public static void RenderPhase(string name)
        {
            Phase=name;presented.Reset();awaiting=true;XRLCore.Core.RenderBase();presented.Wait();
            if(ExitCode!=0)throw new InvalidOperationException("Gameplay presentation failed");
        }
        public static void PresentationFailed()
        {
            ExitCode=1;
            if(awaiting)presented.Set();else Done=true;
        }
        public static void InjectInput()
        {
            if(!Automated || !Presenting || !XRLCore.IsCoreThread)return;
            if(GameManager.Instance.CurrentGameView=="Looker" && lookReady && !escaped)
            {escaped=true;Keyboard.PushKey(UnityEngine.KeyCode.Escape);return;}
            if(GameManager.Instance.CurrentGameView!="Stage" || commands.Count==0)return;
            string command=commands.Dequeue();
            inputSerial++;
            if(command=="look")Keyboard.PushMouseEvent("AdventureMouseLook",targetX,targetY);
            else Keyboard.PushMouseEvent("Command:"+command);
        }
        static void Command(string name,bool wait=false)
        {
            commands.Enqueue(name);if(wait)commands.Enqueue("CmdWait");
            XRLCore.Core.Game.Player.Body.Energy.BaseValue=1000;XRLCore.Core.PlayerTurn();
            if(commands.Count!=0)throw new InvalidOperationException("Native command sequence did not finish");
        }
        public static void TargetApparel(XRL.World.GameObject npc){TargetActor(npc,"apparel");}
        public static void TargetActor(XRL.World.GameObject npc,string fixture)
        {
            int restoreX=targetX,restoreY=targetY,oldLookX=LookX,oldLookY=LookY;
            targetX=npc.CurrentCell.X;targetY=npc.CurrentCell.Y;
            escaped=lookReady=false;LookX=LookY=-1;Phase=fixture+"-look";Command("look",true);
            if(LookX!=targetX || LookY!=targetY || !lookReady || !escaped)
                throw new InvalidOperationException("Native look did not target the fixture NPC");
            ProbeRunner.Record(fixture+"-target.json",new{x=LookX,y=LookY,instance=npc.BaseID,nativeLook=true});
            targetX=restoreX;targetY=restoreY;LookX=oldLookX;LookY=oldLookY;
            RenderPhase(fixture+"-look-returned");
        }
        public static void DisposePresentation()
        {
            Presenting=false;Hide();
            if(cameraHook){Camera.onPreCull-=BeforeCamera;cameraHook=false;}
            if(overlay!=null)UnityEngine.Object.DestroyImmediate(overlay);
            if(overlayMesh!=null)UnityEngine.Object.DestroyImmediate(overlayMesh);
            if(overlayMaterial!=null)UnityEngine.Object.DestroyImmediate(overlayMaterial);
        }
        public static void ObserveView()
        {
            if(!ActiveMode)return;
            string view=GameManager.Instance.CurrentGameView;
            if(!Automated && Presenting)
            {
                var body=XRLCore.Core.Game.Player.Body;var cell=body.CurrentCell;
                string token=view+"|"+cell.X+"|"+cell.Y+"|"+Application.isFocused+"|"+Screen.width+"|"+Screen.height;
                if(token!=reviewState || Input.anyKeyDown || Input.GetMouseButtonDown(0) || Input.GetMouseButtonDown(1))
                {
                    reviewState=token;
                    ProbeRunner.Record("review-state.json",new{view,x=cell.X,y=cell.Y,
                        applicationFocused=Application.isFocused,gameFocused=GameManager.focused,threadFocused=XRLCore.bThreadFocus,
                        screenWidth=Screen.width,screenHeight=Screen.height,fullscreen=Screen.fullScreen,
                        keyDown=Input.anyKeyDown,inputText=Input.inputString,overlayVisible=overlay!=null && overlay.activeSelf});
                }
            }
            if(view!="Stage")Hide();
            if(Automated && view=="GameSummaryScreen" && !Done)
            {
                var game=XRLCore.Core.Game;
                ProbeRunner.Record("gameplay-failure.json",new{reason="Unexpected native game summary",phase=Phase,
                    deathReason=game.DeathReason,remainingCommands=commands.Count,playerHP=game.Player.Body.Stat("Hitpoints")});
                ExitCode=1;Done=true;
            }
            if(Automated && Phase=="inventory" && view=="StatusScreensScreen" && !menuSeen)
            {
                var screen=Qud.UI.StatusScreensScreen.instance;
                if(screen!=null && screen.gameObject.activeInHierarchy && screen.navigationContext.IsActive())
                {
                    ProbeRunner.Record("gameplay-menu.json",new{view,screen=screen.CurrentScreen,
                        overlayVisible=overlay!=null && overlay.activeSelf,nativeHiddenCells=hidden.Count(r=>r!=null)});
                    menuSeen=true;screen.OnCloseButton();
                }
            }
            if(view!=lastView)
            {
                lastView=view;
                ProbeRunner.Record("gameplay-view.json",new{view,audioPaused=AudioListener.pause,
                    listenerVolume=AudioListener.volume,masterVolume=SoundManager.MasterVolume});
            }
        }
        public static void StartReview(XRLGame game)
        {
            if(!ActiveMode || Automated || game==null || Interlocked.Exchange(ref started,1)!=0)return;
            Presenting=true;Phase="review";
            ProbeRunner.Record("review-ready.json",new{zone=game.Player.Body.CurrentZone.ZoneID,
                silent=true,entry="Native main menu NewGame and RunGame",operatingSystemInput=false});
        }
        // One native-data collection pass, before any presentation fixture moves residents.
        static void CaptureCatalogue(XRL.World.Zone zone)
        {
            var rows=new JArray();var seen=new HashSet<int>();
            for(int y=0;y<zone.Height;y++)for(int x=0;x<zone.Width;x++)foreach(var obj in zone.GetCell(x,y).Objects)
            {
                if(obj.Body==null || obj.Brain==null || !seen.Add(obj.BaseID))continue;
                var parts=new JArray();
                foreach(var part in obj.Body.GetParts())
                {
                    var equipped=part.Equipped;var natural=part._DefaultBehavior;
                    parts.Add(new JObject{{"id",part.ID},{"parent",part.ParentPart==null?-1:part.ParentPart.ID},
                        {"type",part.Type},{"variant",part.VariantType},{"laterality",part.Laterality},
                        {"manager",part.Manager},{"defaultBlueprint",part.DefaultBehaviorBlueprint},
                        {"equipped",CatalogueItem(equipped)},{"defaultItem",CatalogueItem(natural)}});
                }
                var description=obj.GetPart<XRL.World.Parts.Description>();var render=obj.Render;
                rows.Add(new JObject{{"instance",obj.BaseID},{"blueprint",obj.Blueprint},{"species",obj.GetSpecies()},
                    {"gender",obj.GetGender().Name},{"description",description==null?null:description.Short},
                    {"anatomy",obj.Body.Anatomy},{"parts",parts},
                    {"tile",render==null?null:render.Tile},{"foreground",render==null?null:render.ColorString},
                    {"tileColor",render==null?null:render.TileColor},{"detailColor",render==null?null:render.DetailColor}});
            }
            ProbeRunner.Record("joppa-creature-catalogue.json",new{zone=zone.ZoneID,actors=rows,
                scope="Generated starting-area body/equipped/default-item data before presentation fixtures; not a rendering test",
                operatingSystemInput=false,rendererRegressionsRun=false});
        }
        static JObject CatalogueItem(XRL.World.GameObject item)
        {
            if(item==null)return null;var render=item.Render;var description=item.GetPart<XRL.World.Parts.Description>();
            return new JObject{{"instance",item.BaseID},{"blueprint",item.Blueprint},
                {"description",description==null?null:description.Short},{"tile",render==null?null:render.Tile},
                {"foreground",render==null?null:render.ColorString},{"tileColor",render==null?null:render.TileColor},
                {"detailColor",render==null?null:render.DetailColor}};
        }
        public static void Run()
        {
            if(Interlocked.Exchange(ref started,1)!=0)return;
            try
            {
                ProbeRunner.Record("gameplay-progress.json",new{state="native-new-game-started"});
                var game=XRLCore.Core.NewGame();
                if(game==null || game.Player==null || game.Player.Body==null)throw new InvalidOperationException("Native new game did not produce a player");
                ProbeRunner.Record("gameplay-boot.json",new{running=game.Running,zone=game.Player.Body.CurrentZone.ZoneID,
                    historyInitialized=game.sultanHistory!=null,player=game.Player.Body.Blueprint,
                    view=GameManager.Instance.CurrentGameView});
                if(Environment.GetEnvironmentVariable("QUDEXPERIMENT_CATALOGUE")=="1")
                {CaptureCatalogue(game.Player.Body.CurrentZone);return;}
                var core=XRLCore.Core;var body=game.Player.Body;var start=body.CurrentCell;
                GameManager.focused=true;GameManager.Instance.SetGameViewStack("Stage");
                body.CurrentZone.SetActive();core.UpdateGlobalChoices();Presenting=true;
                PawnPresentation.Setup(game);
                if(DromadArt.Enabled){targetX=start.X;targetY=start.Y;DromadArt.RunSample();return;}
                string direction=null;
                foreach(string d in new[]{"E","W","S","N"})
                {
                    var candidate=start.GetCellFromDirection(d);
                    if(candidate!=null && !candidate.IsSolidFor(body) && !candidate.Objects.Any(o=>o!=body && o.HasPart("Combat")))
                    {direction=d;targetX=candidate.X;targetY=candidate.Y;break;}
                }
                if(direction==null)throw new InvalidOperationException("No unobstructed native movement fixture");
                RenderPhase("baseline");
                if(PawnPresentation.Enabled)
                {
                    var human=PawnPresentation.Human;var original=human.CurrentCell;
                    PawnPresentation.Place(human,original.ParentZone.GetCell(original.X-1,original.Y));RenderPhase("pawn-west");
                    PawnPresentation.Place(human,original);RenderPhase("pawn-east");
                    var animal=PawnPresentation.Animal;var animalStart=animal.CurrentCell;
                    PawnPresentation.Place(animal,animalStart.ParentZone.GetCell(animalStart.X+1,animalStart.Y));RenderPhase("animal-east");
                    PawnPresentation.Place(animal,animal.CurrentCell.ParentZone.GetCell(animal.CurrentCell.X,animal.CurrentCell.Y-1));RenderPhase("animal-north");
                    human.Render.Visible=false;RenderPhase("pawn-hidden");human.Render.Visible=true;RenderPhase("pawn-visible");
                    PawnPresentation.InjectLateMutation=true;RenderPhase("pawn-late-change");
                    PawnPresentation.InjectLateMutation=false;RenderPhase("pawn-restored");
                    string color=human.Render.ColorString,tileColor=human.Render.TileColor;
                    human.Render.ColorString="&R";human.Render.TileColor="&R";RenderPhase("pawn-tint");
                    human.Render.ColorString=color;human.Render.TileColor=tileColor;RenderPhase("pawn-tint-restored");
                    var prop=PawnPresentation.Prop;var propStart=prop.CurrentCell;
                    PawnPresentation.Place(prop,original.ParentZone.GetCell(original.X,original.Y+1));RenderPhase("prop-front");
                    PawnPresentation.Place(prop,propStart);RenderPhase("prop-behind");
                }
                Command("CmdMove"+direction);RenderPhase("moved");
                if(body.CurrentCell.X!=targetX || body.CurrentCell.Y!=targetY)
                    throw new InvalidOperationException("Native movement did not reach the displayed adjacent cell");
                if(PawnPresentation.Enabled && PawnPresentation.Stage>=2)
                {
                    string opposite=direction=="E"?"W":direction=="W"?"E":direction=="N"?"S":"N";
                    Command("CmdMove"+opposite);RenderPhase("native-move-back");
                    Command("CmdMove"+direction);RenderPhase("native-move-forward");
                    DamageFixture(PawnPresentation.Human,"human");
                    DamageFixture(PawnPresentation.Animal,"animal");
                }
                Phase="look";Command("look",true);
                if(LookX!=targetX || LookY!=targetY || !lookReady || !escaped)
                    throw new InvalidOperationException("Native target look flow did not complete");
                RenderPhase("look-returned");
                if(PawnPresentation.Enabled)
                {
                    int restoreX=targetX,restoreY=targetY;
                    targetX=PawnPresentation.Human.CurrentCell.X;targetY=PawnPresentation.Human.CurrentCell.Y;
                    escaped=lookReady=false;LookX=LookY=-1;Phase="pawn-look";Command("look",true);
                    if(LookX!=targetX || LookY!=targetY || !lookReady || !escaped)
                        throw new InvalidOperationException("Native NPC look did not target the displayed human");
                    ProbeRunner.Record("pawn-target.json",new{x=LookX,y=LookY,instance=PawnPresentation.Human.BaseID,
                        nativeLook=true,operatingSystemInput=false});
                    targetX=restoreX;targetY=restoreY;RenderPhase("pawn-look-returned");
                }
                Phase="inventory";Command("CmdInventory",true);
                if(!menuSeen)throw new InvalidOperationException("Native inventory was not observed");
                RenderPhase("menu-returned");
                NativeApparel.RunFixture();
                CtesiphusArt.RunFixture();
                Replacement=false;RenderPhase("disabled");Replacement=true;RenderPhase("reenabled");
                game.SetIntGameState("RimQudProbeMarker",17391);
                var save=game.SaveGame("RimQudProbe");
                // This build returns null after synchronous success, or a Task
                // for asynchronous/failing storage. Validate the saved state by loading it.
                if(save!=null)save.GetAwaiter().GetResult();
                if(!File.Exists(game.GetCacheDirectory("RimQudProbe.sav.gz")))
                    throw new InvalidOperationException("Native save did not produce its file");
                var loaded=XRLGame.LoadCurrentGame("RimQudProbe");
                if(loaded==null || loaded.GetIntGameState("RimQudProbeMarker")!=17391 ||
                    loaded.Player.Body.CurrentCell.X!=targetX || loaded.Player.Body.CurrentCell.Y!=targetY)
                    throw new InvalidOperationException("Native save/load state did not match");
                NativeApparel.AfterLoad(loaded);
                RenderPhase("loaded");
                long startTicks=loaded.TimeTicks;int completedTurns=0,lastInput=inputSerial;
                string deathReason=loaded.DeathReason;
                Action<XRLCore> endTurn=c=>
                {
                    if(inputSerial==lastInput || c.Game.Player.Body.Energy.Value>=1000)return;
                    lastInput=inputSerial;completedTurns++;
                    if(completedTurns==3)c.Game.Running=false;
                };
                Phase="continuous";loaded.DeathReason="<nodeath>";
                for(int i=0;i<3;i++)commands.Enqueue("CmdWait");
                XRLCore.RegisterOnEndPlayerTurnCallback(endTurn);
                try{core.RunGame();}
                finally{XRLCore.RemoveOnEndPlayerTurnCallback(endTurn);loaded.DeathReason=deathReason;loaded.Running=true;}
                if(completedTurns!=3 || commands.Count!=0 || loaded.TimeTicks<=startTicks)
                    throw new InvalidOperationException("Continuous native game loop did not advance three commanded turns");
                RenderPhase("continuous-returned");
                ProbeRunner.Record("gameplay-result.json",new{nativeMovement=true,nativeLook=true,nativeInventory=true,
                    nativeSaveLoad=true,lookX=LookX,lookY=LookY,targetX,targetY,frames=frames.Count,
                    continuousNativeTurns=completedTurns,startTicks,endTicks=loaded.TimeTicks,
                    operatingSystemInput=false,focusOverride="Internal game flag only; no OS focus change",
                    turnScope="Native PlayerTurn command handlers plus three turns in RunGame with the native action scheduler"});
            }
            catch(Exception ex){ExitCode=1;ProbeRunner.Record("gameplay-failure.json",new{exception=ex.ToString()});}
            finally{Done=true;}
        }
    }
}
