"""Freeze current race/anatomy and verified accepted-ray-cat generation history."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/qud-transplant-probe-pawns-20261019');BASE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base')
sys.path.insert(0,str(ROOT/'tools'));from audit_joppa_anatomy import xml
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(n,v):(HERE/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='BODY-RAY-CAT';e=next(e for e in l['entries'] if e['id']==l['active_entry']);s=read(ROOT/'art/village/sources.json');g=next(g for g in s['actors'] if g['creature']=='Ctesiphus');actor=g['native_instances'][0]
definitions={}
for p in sorted((BASE/'ObjectBlueprints').glob('*.xml')):
 for obj in xml(p).findall('object'):definitions[obj.get('Name')]=(obj,p)
def ancestry(name):
 rows=[]
 while name in definitions:
  obj,p=definitions[name];rows.append(dict(blueprint=name,parent=obj.get('Inherits'),file=str(p),sha256=sha(p),object_xml=ET.tostring(obj,encoding='unicode')));name=obj.get('Inherits')
 return rows
chain=ancestry('Ray Cat');merged={}
for row in reversed(chain):
 obj=ET.fromstring(row['object_xml'])
 for child in obj:
  key=(child.tag,child.get('Name') or child.get('Blueprint') or '')
  if child.tag.startswith('remove'):merged.pop((child.tag[6:],key[1]),None)
  else:merged[key]={**merged.get(key,{}),**child.attrib}
assert merged[('part','Body')]['Anatomy']=='Quadruped' and merged[('tag','Species')]['Value']=='cat'
body=next(n for n in xml(BASE/'Bodies.xml').iter('anatomy') if n.get('Name')=='Quadruped');parts=actor['parts'];assert sum(p['type']=='Foot' for p in parts)==4 and sum(p['type']=='Tail' for p in parts)==1 and not any(p.get('equipped') for p in parts)
write('native-anatomy-evidence.json',dict(race_ancestry=chain,named_override=ancestry('Ctesiphus')[0],resolved_race=[dict(kind=k[0],**v) for k,v in merged.items()],anatomy_file=dict(file=str(BASE/'Bodies.xml'),sha256=sha(BASE/'Bodies.xml'),xml=ET.tostring(body,encoding='unicode')),observed_actor=actor,interpretation='Four actual Foot nodes plus two dependent Feet groups; the groups do not add legs. Tail is intrinsic. Cat Bite/Claw defaults are natural behavior, not worn garments. Static inherited DarkVision is not extra anatomy; unexported active mutation state remains unknown.'))
legacy=read(PRIVATE/'faithful-cat.json');catalogue=read(ROOT/'evidence/joppa-creature-catalogue.json');donorrows=catalogue['references']['cat'] if 'references' in catalogue and 'cat' in catalogue['references'] else None
# The original packet independently binds exact Core Cat texture identities/hashes.
refs=[]
for f in ['south','east','north']:
 r=legacy['views'][f]['donor_reference'];p=PRIVATE/'donor'/('cat-'+f+'.png');assert sha(p)==r['png_sha256'];refs.append(dict(facing=f,file=str(p),**r,role='Compact small feline, fixed cardinal map camera, restrained outline/shading. No humanoid, panther size, imported behavior or native age claim.'))
donordef=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Races/Races_Animal_CatGroup.xml');doc=ET.parse(donordef).getroot();kind=next(n for n in doc.findall('PawnKindDef') if n.findtext('defName')=='Cat')
write('donor-reference-evidence.json',dict(references=refs,definition=dict(file=str(donordef),sha256=sha(donordef),xml=ET.tostring(kind,encoding='unicode')),physical_scale='Retain already selected authoring scale from faithful-cat.json. Historical0.9 multiplier is an authored presentation choice; current Core cat life stages declare0.6/0.8/1.0, not0.9. No native Qud age/height is inferred.',legacy_registration=dict(file=str(PRIVATE/'faithful-cat.json'),sha256=sha(PRIVATE/'faithful-cat.json'),views=legacy['views'])))
history=read(HERE/'historical-generation-provenance.json');assert len(history['calls'])==4
for r in history['calls']:
 assert sha(ROOT/r['image'])==r['sha256']
 if r['label']!='north-before-tail-correction':assert r['matches_current_accepted_bytes']
now=datetime.now(timezone.utc).isoformat();packet=dict(entry=e['id'],recorded_at=now,race='Ray Cat',source=ref(ROOT/'art/village/sources.json'),race_description=merged[('part','Description')]['Short'],native_anatomy=ref(HERE/'native-anatomy-evidence.json'),donor=ref(HERE/'donor-reference-evidence.json'),historical_generation=ref(HERE/'historical-generation-provenance.json'),original_named_mask=dict(file=str(PRIVATE/'donor/ctesiphus-original-mask.png'),sha256=sha(PRIVATE/'donor/ctesiphus-original-mask.png'),**legacy['original_model']),
 policy='Preserve accepted ray-cat design per authoritative specification. Recover actual historical calls/images, retain rejected north root and actual tail correction. New manual registration/ownership controls must be labeled as current work, never retroactively claimed as historical generation inputs.',
 scope='Reusable intrinsic quadruped feline shape, no named gear or mutation appendages. Named Ctesiphus and generic Ray Cat use different source glyphs; selected appearance was generated for Ctesiphus as a small Ray Cat. Generic blueprint tile identity remains explicit, not replaced by named metadata.',
 palette=dict(primary='m',primary_rgb='b154cf',detail='y',detail_rgb='b1c9c3',remaining='Old base has no separate detail region. Current work must author/review body/head and native detail ownership while retaining accepted silhouette/physical scale.'),
 age='Native life stage unknown. No new child/sex geometry or demographic simulation change.',new_imagegen_calls=0,current_state='Metadata/reference/history recovered. Manual ownership controls, common-frame registration, independent tint layers and current visual review remain unfinished. No native validation.')
write('source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14);out=Image.new('RGB',(1200,680),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'RAY CAT / actual Core references, accepted generated views, rejected north root',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
 donor=Image.open(PRIVATE/'donor'/('cat-'+f+'.png')).convert('RGBA').resize((192,192),Image.Resampling.NEAREST);out.paste(donor,(i*300+40,60),donor);d.text((i*300+20,265),'CORE '+f.upper(),font=font,fill='#e3cf43')
 accepted=Image.open(ROOT/'art/ctesiphus'/(f+'-albedo.png')).convert('RGBA');accepted.thumbnail((260,340),Image.Resampling.LANCZOS);out.paste(accepted,(i*300+20,300),accepted)
bad=Image.open(HERE/'north-before-tail-correction-historical-output.png').convert('RGBA');bad.thumbnail((260,340),Image.Resampling.LANCZOS);out.paste(bad,(920,300),bad);d.text((920,265),'REJECTED NORTH',font=font,fill='#e3cf43');out.save(HERE/'source-reference-history.png')
reason='Fresh installed Ray Cat ancestry, native Quadruped tree and captured Ctesiphus parts confirm a small feline with four Foot nodes and intrinsic Tail. Exact Core Cat directional texture hashes and current definition are recorded. Recovered all four original ImageGen calls and actual PNG bytes: accepted south/east/corrected north exactly match current source files; rejected neck-root north is retained. No new generation or native acceptance claim.'
for step,names in [('resolve_race_description_original_sprite_runtime_anatomy',['source-packet.json','native-anatomy-evidence.json']),('select_actual_core_dlc_or_mod_reference',['donor-reference-evidence.json','source-reference-history.png'])]:
 e['process_log'].append(dict(timestamp=now,step=step,action=reason,inputs=[ref(ROOT/'art/village/sources.json')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
e['process_log'].append(dict(timestamp=now,step='imagegen_side_back_from_front_and_race_facts',action='Recover historical source-bound front-guided actual calls without claiming new generation or a pre-existing manual stage.',inputs=[ref(ROOT/'art/ctesiphus/generation-prompts.json')],outputs=[ref(HERE/'historical-generation-provenance.json')]+[ref(ROOT/r['image']) for r in history['calls']],review=reason,result='PASS'))
e.update(current_step='construct_front',generation_ready=False,metadata=dict(race='Ray Cat',anatomy='Quadruped',source_packet=ref(HERE/'source-packet.json')),art_review=dict(status='REQUIRES REVIEW',reason=packet['current_state']))
l.update(updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode())
print('Ray Cat metadata/references and exact historical generation recovered; manual registration/detail work remains active.')
