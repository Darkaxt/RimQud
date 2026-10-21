// Explicit reviewed Joppa mappings, not a general mod or anatomy resolver.
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Newtonsoft.Json.Linq;
using XRL.World;
using GO=XRL.World.GameObject;

namespace RenderingTransplantProbe
{
    public static class JoppaCoverage
    {
        public static bool Enabled { get { return !CurrentArt.Enabled && PawnPresentation.Stage>=3 &&
            new[]{"pawns","joppa"}.Contains(Environment.GetEnvironmentVariable("QUDEXPERIMENT_MODE")); } }
        static JObject data;
        static Dictionary<string,JObject> rules,textures;
        static void Load()
        {
            if(data!=null)return;
            data=JObject.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"joppa-coverage.json")));
            rules=((JArray)data["entries"]).Cast<JObject>().ToDictionary(r=>(string)r["blueprint"]);
            if(rules.Values.Count(r=>(bool)r["baseline_selected"])!=67)
                throw new InvalidDataException("Expected the reviewed 67-type baseline");
            textures=JArray.Parse(File.ReadAllText(Path.Combine(ProbeRunner.Root,"donor","coverage-textures.json")))
                .Cast<JObject>().ToDictionary(r=>(string)r["file"]);
        }
        public static JObject Rule(string blueprint)
        {
            if(!Enabled || blueprint==null)return null;Load();JObject rule;rules.TryGetValue(blueprint,out rule);return rule;
        }
        public static string Kind(GO obj)
        {
            var rule=Rule(obj.Blueprint);string kind=rule==null?"original":(string)rule["render_kind"];
            if((kind=="human" || kind=="animal") && (obj.HasEffect("Asleep") || obj.HasEffect("Prone")))return "original";
            if(kind=="human" && (obj.Body==null || obj.Body.Anatomy!="Humanoid"))return "original";
            return kind;
        }
        public static JObject Asset(string family){Load();return (JObject)data["assets"][family];}
        public static float Foot(string file)
        {
            Load();var texture=textures[file];return (float)texture["alpha_bounds"][3]/(float)texture["height"]-.5f;
        }
        // Only the isolated authored-map diagnostic uses these relocations.
        public static Dictionary<GO,Cell> PlaceVariants(Zone zone)
        {
            var selected=new Dictionary<string,GO>();
            for(int y=0;y<25;y++)for(int x=0;x<80;x++)foreach(var obj in zone.GetCell(x,y).Objects)
            {
                var rule=Rule(obj.Blueprint);
                if(rule!=null && (string)rule["render_kind"]=="prop")
                {
                    string family=(string)rule["asset_family"];
                    if(family!="chair" && !selected.ContainsKey(family))selected.Add(family,obj);
                }
            }
            var original=new Dictionary<GO,Cell>();var occupied=new List<Cell>();
            foreach(var pair in selected)
            {
                Cell target=null;
                for(int y=22;y>=1 && target==null;y--)for(int x=1;x<79 && target==null;x++)
                {
                    var cell=zone.GetCell(x,y);
                    if(occupied.Any(other=>Math.Abs(other.X-x)<4 && Math.Abs(other.Y-y)<3))continue;
                    if(!cell.IsSolidFor(pair.Value) && cell.Objects.All(o=>o.Render==null || !o.Render.Visible || o.Render.RenderLayer<2) &&
                        zone.GetCell(x+1,y).Objects.All(o=>o.Render==null || !o.Render.Visible || o.Render.RenderLayer<2) &&
                        zone.GetCell(x,y+1).Objects.All(o=>o.Render==null || !o.Render.Visible || o.Render.RenderLayer<2) &&
                        zone.GetCell(x+1,y+1).Objects.All(o=>o.Render==null || !o.Render.Visible || o.Render.RenderLayer<2))target=cell;
                }
                if(target==null)throw new InvalidOperationException("No clear authored-map prop variant fixture for "+pair.Key);
                original[pair.Value]=pair.Value.CurrentCell;PawnPresentation.Place(pair.Value,target);occupied.Add(target);
            }
            ProbeRunner.Record("coverage-prop-fixture.json",selected.ToDictionary(p=>p.Key,p=>p.Value.BaseID));
            return original;
        }
    }
}
