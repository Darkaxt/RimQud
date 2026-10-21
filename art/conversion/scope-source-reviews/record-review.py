"""Record one explicitly reviewed non-art scope decision; never classify an unseen entry."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,re,hashlib,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];DEFS=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
p=argparse.ArgumentParser();p.add_argument('--entry',required=True);p.add_argument('--next');p.add_argument('--reason',required=True);p.add_argument('--code',action='append',default=[]);args=p.parse_args();l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']==args.entry;e=next(e for e in l['entries'] if e['id']==args.entry);assert e['category']=='Baseline exclusion review' and not e.get('generation_ready') and not e['process_log'];OUT=HERE/e['name'].lower().replace(' ','-');OUT.mkdir(exist_ok=True)
definitions={}
for path in DEFS.glob('*.xml'):
 for match in re.finditer(r'<object\s+Name="([^"]+)"[^>]*>.*?</object>',path.read_text(encoding='utf-8-sig'),re.S):definitions[match.group(1)]=(path,match.group())
name=e['name'];chain=[];render={};parts={}
while name:
 path,xml=definitions[name];ob=ET.fromstring(xml);chain.append(dict(name=name,definition=ref(path),selected=xml));name=ob.get('Inherits')
for row in reversed(chain):
 ob=ET.fromstring(row['selected'])
 for part in ob.findall('part'):
  parts.setdefault(part.get('Name'),{}).update(part.attrib)
  if part.get('Name')=='Render':render.update(part.attrib)
assert render.get('Visible')=='false',render
codes=[ref(Path(path)) for path in args.code];packet=dict(entry=e['id'],blueprint=e['name'],ancestry=chain,effective_render=render,effective_parts=parts,code_evidence=codes,decision='No independent visible texture to convert',main_source_evaluation=args.reason,preserve='Keep native placement, effects, lighting, discovery, transition and interaction ownership. Do not turn an invisible marker into a drawn prop or remove it from the native zone.',limit='Installed definitions/part-code scope audit, not a new runtime/game verification.',generation_ready=True,native_activation=False)
write(OUT/'source-scope-review.json',packet);now=datetime.now(timezone.utc).isoformat()
for step,action in [('verify_blueprint_visibility_and_any_tile','Inspect exact installed ancestry, effective Render.Visible/Tile and attached part code for independent visible art or state changes.'),('record_justified_art_exclusion_or_add_conversion_target','Record the source-bound no-independent-art decision while preserving native behavior.')]:
 e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(Path(__file__))],outputs=[ref(OUT/'source-scope-review.json')],review=args.reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='record_justified_art_exclusion_or_add_conversion_target',disposition='Source-reviewed invisible marker / no independent art',known_issues=[],scope_review=ref(OUT/'source-scope-review.json'))
if args.next:
 n=next(x for x in l['entries'] if x['id']==args.next);assert not n.get('generation_ready');n.update(status='IN PROGRESS',current_step=n['required_steps'][0])
l.update(active_entry=args.next,updated_at=now);write(ROOT/'evidence/conversion-ledger.json',l);print(e['id']+' source scope recorded; next='+str(args.next))
