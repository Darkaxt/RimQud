// Hidden native-game bootstrap and lifecycle diagnostics; never OS input.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using HarmonyLib;
using UnityEngine;
using XRL;
using XRL.Core;
using XRL.CharacterBuilds;
using XRL.CharacterBuilds.Qud;

namespace RenderingTransplantProbe
{
    [HarmonyPatch(typeof(Qud.UI.PopupMessage),"ShowPopup")]
    public static class DiagnosticPopup
    {
        static void Postfix(Qud.UI.PopupMessage __instance, string message, List<Qud.UI.QudMenuItem> buttons)
        {
            if(Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")!="gameplay")return;
            ProbeRunner.Record("gameplay-popup.json",new{message,commands=buttons.Select(b=>b.command).ToArray()});
            if(message=="You embark for the caves of Qud." && buttons.Count==1 && buttons[0].command=="Accept")
            {
                __instance.OnActivateCommand(buttons[0]);return;
            }
            // Unknown prompts require inspection rather than a guessed response.
            GameplayProbe.ExitCode=2;GameplayProbe.Done=true;
        }
    }
    [HarmonyPatch(typeof(EmbarkBuilder),"Begin")]
    public static class DiagnosticEmbark
    {
        static bool Prefix(ref Task<EmbarkInfo> __result)
        {
            if(Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")!="gameplay")return true;
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
        static string lastView;
        public static void ObserveView()
        {
            if(Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")!="gameplay")return;
            string view=GameManager.Instance.CurrentGameView;
            if(view==lastView)return;
            lastView=view;
            ProbeRunner.Record("gameplay-view.json",new{view,audioPaused=AudioListener.pause,
                listenerVolume=AudioListener.volume,masterVolume=SoundManager.MasterVolume});
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
            }
            catch(Exception ex){ExitCode=1;ProbeRunner.Record("gameplay-failure.json",new{exception=ex.ToString()});}
            finally{Done=true;}
        }
    }
}
