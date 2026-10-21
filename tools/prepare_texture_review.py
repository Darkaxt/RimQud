"""Inventory selected conversion textures and prepare bounded visual-review packets.

Read-only for artwork and status. Reviewers/main-agent write findings separately.
Superseded provenance is indexed, never silently re-approved as current output.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'evidence/texture-review-20261021';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
cache={}
def ref(p):
 p=p.resolve()
 if p not in cache:cache[p]=dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 return cache[p]
def strings(v):
 if isinstance(v,dict):
  for x in v.values():yield from strings(x)
 elif isinstance(v,list):
  for x in v:yield from strings(x)
 elif isinstance(v,str):yield v
def resolve(s,base):
 for p in [ROOT/s,base/s]:
  if p.is_file():return p.resolve()
def latest(e,suffix):
 for event in reversed(e['process_log']):
  for r in event.get('outputs',[]):
   if isinstance(r,dict) and r.get('path','').endswith(suffix) and (ROOT/r['path']).is_file():return ROOT/r['path']

l=read(ROOT/'evidence/conversion-ledger.json');sets=[];absent=[]
for e in l['entries']:
 current=e.get('current_registration') or {};model=current.get('model',{}).get('path');mp=ROOT/model if model else latest(e,'fittings.json')
 if not mp or not mp.exists():
  absent.append(dict(entry=e['id'],category=e['category'],status='NO CURRENT CREATED TEXTURE SET',generation_ready=bool(e.get('generation_ready'))));continue
 m=read(mp);primary=current.get('plate',{}).get('path');pp=ROOT/primary if primary else None
 if not pp or not pp.exists():pp=latest(e,'comparison.png')
 components=[]
 for s in strings(m):
  if s.lower().endswith('.png'):
   p=resolve(s,mp.parent)
   if p and ref(p) not in components:components.append(ref(p))
 extras=[]
 for p in sorted(mp.parent.glob('*.png')):
  if any(k in p.stem for k in ['comparison','turnaround','all-views','all-states','all-layouts','all-phases','connected','family','native-palette','palette']):extras.append(ref(p))
 selected=[ref(pp)] if pp and pp.exists() else []
 # Always include a complementary neutral/native view set when available.
 for r in extras:
  if r not in selected and any(k in r['path'] for k in ['neutral','native','palette','all-views','all-states','all-layouts','all-phases']):selected.append(r)
  if len(selected)>=3:break
 metadata=e.get('metadata',{});descs=[]
 for s in strings(metadata):
  if 30<len(s)<1800 and (' ' in s) and not s.startswith(('art/','http')):descs.append(s)
 sets.append(dict(entry=e['id'],name=e['name'],category=e['category'],model=ref(mp),generation_ready=bool(e.get('generation_ready')),required_variants=e['required_variants'],source_context=descs[:2],primary_images=selected,available_review_images=extras,component_textures=components,review_status='PENDING'))

groups=[('bodies',[x for x in sets if x['entry'].startswith('BODY-') or x['category']=='Template garments']),
 ('garments',[x for x in sets if x['entry'].startswith('FIT-') and x['category']!='Template garments' and any(k in x['entry'] for k in ['ROBE','VEST','TUNIC','APRON','MAIL'])]),
 ('head_and_feet',[x for x in sets if x['entry'].startswith('FIT-') and any(k in x['entry'] for k in ['SANDALS','BOOTS','MONOCLE','SPECTACLES','HORNS','HAT'])]),
 ('held_items',[x for x in sets if x['entry'].startswith('FIT-') and any(k in x['entry'] for k in ['SHILLELAGH','VINEREAPER','KNIFE','WRENCH','STICK','GLOWSPHERE','PESTLE','BLADE'])]),
 ('furniture',[x for x in sets if x['category']=='Furniture']),
 ('machinery',[x for x in sets if x['category']=='Machinery/appliances']),
 ('named_assemblies',[x for x in sets if x['category'] in ['NPC assemblies','Creatures']]),
 ('terrain',[x for x in sets if x['category'] in ['Surface/grass tiles','Terrain/structures']]),
 ('vegetation_props',[x for x in sets if x['category'] in ['Vegetation','Other props/debris/light','Containers']])]
assigned=set();batches=[]
for name,items in groups:
 items=[x for x in items if x['entry'] not in assigned];assigned.update(x['entry'] for x in items)
 # Twelve sets per packet keeps actual image inspection bounded.
 for start in range(0,len(items),12):
  ident=f'{len(batches)+1:02d}-{name}';packet=dict(batch=ident,scope='Read-only visual structural review; current selected texture sets, all required views/states. No native/game validation.',sets=items[start:start+12]);write(OUT/f'packet-{ident}.json',packet);batches.append(dict(id=ident,packet=ref(OUT/f'packet-{ident}.json'),entries=[x['entry'] for x in packet['sets']]))
aggregates=[x for x in sets if x['entry'] not in assigned]
assert all(x['entry'].startswith('ITEM-') for x in aggregates),[x['entry'] for x in aggregates]
for x in aggregates:x['review_status']='REVIEW VIA EXACT FITTING DEPENDENCIES AND AGGREGATE PLATE'
all_art=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size) for p in sorted((ROOT/'art').rglob('*.png'))]
direct={r['path'] for x in sets for r in x['component_textures']};write(OUT/'png-file-index.json',dict(policy='Complete PNG path inventory, including provenance/rejected attempts/review plates. Unselected historical files are not counted as visually approved current textures.',files=all_art))
write(OUT/'inventory.json',dict(recorded_at=datetime.now(timezone.utc).isoformat(),ledger=ref(ROOT/'evidence/conversion-ledger.json'),scope='Every selected current texture set, its declared component files and required views/states. Current failed horn v5 draft reviewed separately; no production model exists for it. Historical superseded attempts are indexed, not re-approved.',sets=sets,not_created=absent,aggregate_entries=[x['entry'] for x in aggregates],batches=batches,total_sets=len(sets),component_file_count=len(direct),all_png_file_count=len(all_art)))
print(json.dumps(dict(current_sets=len(sets),direct_component_files=len(direct),no_current_set=len(absent),aggregate_sets=len(aggregates),batches=[(x['id'],len(x['entries'])) for x in batches]),indent=2))
