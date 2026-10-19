// One explicit ray-cat asset contract; no donor pawn simulation or general resolver.
using System;
using System.IO;
using System.Linq;
using ConsoleLib.Console;
using Newtonsoft.Json.Linq;
using XRL.Core;
using GO=XRL.World.GameObject;

namespace RenderingTransplantProbe
{
    public static class CtesiphusArt
    {
        public static bool Enabled { get { return Environment.GetEnvironmentVariable("QUDEXPERIMENT_ART")=="ray-cat"; } }
        static JObject contract;
        public static JObject Contract
        {
            get
            {
                if(contract==null)
                {
                    contract=JObject.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"faithful-cat.json")));
                    if((string)contract["creature"]!="Ctesiphus" || (string)contract["race"]!="Ray Cat" ||
                        string.IsNullOrEmpty((string)contract["race_description"]) || contract["original_model"]==null)
                        throw new InvalidDataException("Incomplete creature/race/description/reference/original-model contract");
                }
                return contract;
            }
        }
        public static void Capture(GO obj,JoppaCell cell)
        {
            if(!Enabled || obj.Blueprint!="Ctesiphus" || cell.Kind!="animal")return;
            var body=obj.Body;var expected=(JObject)Contract["expected_body"];
            cell.BodyShape=body.Anatomy+":"+string.Join(",",expected.Properties().Select(p=>p.Name+"="+body.GetPartCount(p.Name)));
            if(body.Anatomy!="Quadruped" || expected.Properties().Any(p=>body.GetPartCount(p.Name)!=(int)p.Value))
            {cell.Kind="original";cell.ArtFallback="Unsupported ray-cat body shape";return;}
            cell.AssetFamily="ray-cat";
        }
        public static string Failure(JoppaCell cell)
        {
            if(!Enabled || cell.Source!="Ctesiphus")return null;
            if(cell.ArtFallback!=null)return cell.ArtFallback;
            if(cell.Display.Detail!=ColorUtility.colorFromChar('y'))return "Unsupported native detail color for neutral ray-cat base";
            return null;
        }
        public static JObject View(int facing)
        {return (JObject)Contract["views"][facing==0?"north":facing==2?"south":"east"];}
        static GO animal;
        public static bool LateAnatomy;
        const string Manager="RimQudRayCatFixtureFoot";
        public static void MutateLate()
        {
            if(Enabled && LateAnatomy && !animal.GetBodyPartsByManager(Manager).Any())
                animal.Body.GetBody().AddPart("Foot",Manager:Manager);
        }
        static void Move(string direction,string phase)
        {
            if(!animal.Move(direction,DoConfirmations:false,EnergyCost:0,Peaceful:true))
                throw new InvalidOperationException("Native ray-cat fixture move failed: "+direction);
            GameplayProbe.RenderPhase(phase);
        }
        public static void RunFixture()
        {
            if(!Enabled)return;
            animal=PawnPresentation.Animal;
            Move("S","raycat-south");Move("W","raycat-west");Move("E","raycat-east");Move("N","raycat-north");
            animal.Render.Visible=false;GameplayProbe.RenderPhase("raycat-hidden");
            animal.Render.Visible=true;GameplayProbe.RenderPhase("raycat-visible");
            var color=animal.Render.ColorString;var tile=animal.Render.TileColor;var detail=animal.Render.DetailColor;
            animal.Render.TileColor="&R";animal.Render.ColorString="&R";GameplayProbe.RenderPhase("raycat-tint");
            animal.Render.TileColor=tile;animal.Render.ColorString=color;GameplayProbe.RenderPhase("raycat-tint-restored");
            animal.Render.DetailColor="R";GameplayProbe.RenderPhase("raycat-detail-fallback");
            animal.Render.DetailColor=detail;GameplayProbe.RenderPhase("raycat-detail-restored");
            LateAnatomy=true;GameplayProbe.RenderPhase("raycat-late-anatomy");LateAnatomy=false;
            int extraFeet=animal.Body.GetPartCount("Foot");
            animal.RemoveBodyPartsByManager(Manager,EvenIfDismembered:true);
            GameplayProbe.RenderPhase("raycat-anatomy-restored");
            GameplayProbe.TargetActor(animal,"raycat");
            ProbeRunner.Record("raycat-fixture.json",new{instance=animal.BaseID,creature=animal.Blueprint,race="Ray Cat",
                nativeMoves=true,extraFeet,restoredFeet=animal.Body.GetPartCount("Foot"),
                foregroundRestored=animal.Render.TileColor==tile && animal.Render.ColorString==color,
                detailRestored=animal.Render.DetailColor==detail,artContract=Contract});
        }
    }
}
