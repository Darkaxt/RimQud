"""Freeze Canteen source/state and actual scoped Core material references."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,xml.etree.ElementTree as ET
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs');import UnityPy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');BASE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base');sys.path.insert(0,str(ROOT/'tools'));from audit_joppa_anatomy import xml
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(n,v):(HERE/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='SCN-CANTEEN';e=next(e for e in l['entries'] if e['id']==l['active_entry']);defs={}
for p in sorted((BASE/'ObjectBlueprints').glob('*.xml')):
 for obj in xml(p).findall('object'):defs[obj.get('Name')]=(obj,p)
chain=[];name='Canteen';resolved={}
while name in defs:
 obj,p=defs[name];chain.append(dict(blueprint=name,parent=obj.get('Inherits'),file=str(p),sha256=sha(p),xml=ET.tostring(obj,encoding='unicode')));name=obj.get('Inherits')
for row in reversed(chain):
 for child in ET.fromstring(row['xml']):
  k=(child.tag,child.get('Name') or child.get('Blueprint') or '')
  if child.tag.startswith('remove'):resolved.pop((child.tag[6:],k[1]),None)
  else:resolved[k]={**resolved.get(k,{}),**child.attrib}
assert resolved[('part','Render')]['Tile']=='Items/sw_canteen.png';write('native-definition.json',dict(ancestry=chain,resolved=[dict(kind=k[0],**v) for k,v in resolved.items()],empty_canteen_xml=ET.tostring(defs['Empty Canteen'][0],encoding='unicode')))
assets=Path('D:/Steam/steamapps/common/RimWorld/RimWorldWin64_Data/resources.assets');donor_hash=sha(assets);assert donor_hash=='7c0c69bde01910dde60205bc1417cd56a39e27affd2de36735dcedd6facd6155';env=UnityPy.load(str(assets));wanted={'Chemfuel','Cloth_a'};references=[]
for o in env.objects:
 if o.type.name!='Texture2D':continue
 data=o.read();name=data.m_Name
 if name not in wanted:continue
 p=PRIVATE/('canteen-core-'+name.lower()+'.png');data.image.save(p);references.append(dict(texture=name,source_id=o.path_id,file=str(p),sha256=sha(p),resources_sha256=donor_hash,size=list(data.image.size),role='Core Cloth: restrained textile shading/weave and contour density only; no rolled-bolt shape.' if name=='Cloth_a' else 'Core Chemfuel: small manufactured-container outline and cap/edge shading only; no jerrycan proportions, hazard marks, fuel contents or metal body colour.'))
assert {r['texture'] for r in references}==wanted
for name,filename in [('Chemfuel','Items_Resource_Manufactured.xml'),('Cloth','Items_Resource_Stuff.xml')]:
 p=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Items')/filename;obj=next(n for n in ET.parse(p).getroot().findall('ThingDef') if n.findtext('defName')==name);next(r for r in references if r['texture']==('Cloth_a' if name=='Cloth' else name))['definition']=dict(file=str(p),sha256=sha(p),xml=ET.tostring(obj,encoding='unicode'))
write('donor-references.json',dict(source='Actual installed Core textures, retained privately; exact roles do not redefine Qud identity.',references=references))
mask=PRIVATE/'village-originals/canteen-mask.png';assert sha(mask)==e['metadata']['original_reference']['native_mask_sha256'];now=datetime.now(timezone.utc).isoformat();packet=dict(entry=e['id'],recorded_at=now,identity='Canteen -> WaterContainer',description=resolved[('part','Description')]['Short'],definition=ref(HERE/'native-definition.json'),original=dict(e['metadata']['original_reference'],private_mask=dict(file=str(mask),sha256=sha(mask))),palette=dict(primary='g',detail='w',primary_rgb='009403',detail_rgb='98875f',meaning='Source green cloth body/side loop; native w cap/exposed neck is tan-gray, not automatically silver white. Aluminum and cloth are materials, palette codes remain exact.'),donor=ref(HERE/'donor-references.json'),
 source_shape='Small round-bodied jug, short top cap, circular cloth-covered face with central reinforcement and a short loop to upper right. Glyph gaps/isolated interior strokes do not establish holes through the physical flask or a disconnected cap.',
 camera='One fixed cardinal map-icon view, front of circular canteen; mild controlled cap top shading only. No object turnaround required for this fixed container entry.',
 states=dict(liquid=resolved[('part','LiquidVolume')],static_tiles='Inspected complete ancestry declares one fixed Canteen tile. Empty Canteen changes StartVolume only; no alternate static exterior is declared.',mapping='Reuse the same closed exterior for declared fill range, without painting exposed water, inventing an open lid/fill-level window or liquid animation. Actual current fill/seal and dynamic liquid painting are not exported; unsupported native state must retain native fallback at final integration.'),
 frame=dict(canvas=[512,768],pivot=[256,384],world=[2/3,1],width_cells=1,height_world=1,pixel_world_size=1/768,meaning='Authoring cell frame follows original16x24 rectangular Qud cell at isotropic world pixel scale. Circle/cap/loop remains at source-relative location; no native measured jug volume inferred.'),
 boundaries='Cloth and aluminum materials only. No human body, hand fit, clothing framework, furniture rotation or gameplay state implementation. Do not change water/seal/capacity.',current_state='Source/reference resolved; construct editable silhouette and region masks next.')
write('source-packet.json',packet)
for step,names,action in [('resolve_object_description_original_tile_palette_state',['source-packet.json','native-definition.json'],'Resolve round cloth-sheathed aluminum canteen from complete installed ancestry, actual source glyph and g/w palette. Declared liquid start/fill range has no alternate static exterior; unknown native dynamic state remains explicit.'),('select_render_reference_or_document_no_equivalent',['donor-references.json'],'Select exact actual Core Cloth and Chemfuel only for restrained textile/manufactured-edge shading. Preserve round Qud jug, upper cap and short side loop; no jerrycan/bolt shape, labels, fuel or donor gameplay.')]:e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[],outputs=[ref(HERE/n) for n in names],review=action,result='PASS'))
e.update(current_step='construct_faithful_shape',generation_ready=False,art_review=dict(status='REQUIRES REVIEW',reason=packet['current_state']));l['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Canteen source/state and actual scoped donor material references recorded; manual construction next.')
