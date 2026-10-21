"""Resolve the flame-free holder, native particle ownership and furniture view contract."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/rimqud-native-torchpost-20261021')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-TORCHPOST';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert not entry['process_log']
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');texts={p:p.read_text() for p in [base/'Furniture.xml',base/'PhysicalPhenomena.xml',base/'RootObjects.xml']};ancestry=[];nodes=[];name='Torchpost'
while name:
    found=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',t,re.S)) for p,t in texts.items()];found=[(p,m) for p,m in found if m];assert len(found)==1,name;p,m=found[0];node=ET.fromstring(m.group());nodes.append(node);ancestry.append(dict(name=name,definition=ref(p),object=m.group()));name=node.get('Inherits')
parts={}
for node in reversed(nodes):
    for part in node.findall('part'):parts.setdefault(part.get('Name'),{}).update(part.attrib)
assert parts['Render']['Tile']=='tiles/sw_torch_nofire.png' and parts['Render']['ColorString']=='&R' and parts['Render']['DetailColor']=='w' and not parts['Render'].get('TileColor')
assert parts['PrefabImposter']['Prefab']=='Prefabs/Particles/TorchpostFlames' and parts['LightSource']['Lit']=='true' and parts['LightSource']['Radius']=='6'
assert not any(n.findall('builder[@Name="RandomTile"]') for n in nodes)
native=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/torchpost-mask.png');assert ref(native)['sha256']==entry['metadata']['original_reference']['native_mask_sha256'];a=np.array(Image.open(native).convert('RGBA'));assert set(np.unique(a[:,:,0][a[:,:,3]>0]))=={255}
donordef=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Furniture.xml');defs=ET.parse(donordef).getroot();wall=next(n for n in defs if n.findtext('defName')=='TorchWallLamp');torch=next(n for n in defs if n.findtext('defName')=='TorchLamp');base_def=next(n for n in defs if n.get('Name')=='TorchBase');refs=read(PRIVATE/'core-walltorch-index.json')
for r in refs['textures']:assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
unlit=re.search(r'<object\s+Name="Unlit Torchpost"(?=\s|>).*?</object>',texts[base/'Furniture.xml'],re.S).group()
packet=dict(entry=entry['id'],timestamp=datetime.now(timezone.utc).isoformat(),identity=' -> '.join(n['name'] for n in ancestry),description=parts['Description']['Short'],ancestry=ancestry,resolved_parts=parts,
    original=dict(**entry['metadata']['original_reference'],private_mask=ref(native),size=[16,24],visible_bbox=list(Image.open(native).getbbox()),source_roles='Every visible pixel is R255/detail. Static wood/iron holder is detail w; source primary R/W/r fire colour is not static holder colour.'),
    palette=dict(declared_primary='R',native_animated_primary_sequence=['R','W','r','W'],native_cycle='AnimatedMaterialFire uses(CurrentFrame+FrameOffset)%60,15-frame sections, ApplyColors(foreground,priority30), cosmetic offset updates native-owned. No new clock or custom animated art.',detail='w',detail_rgb='98875f',holder_role='All source opaque pixels are detail. Registered body must have empty primary, full detail coverage, neutral gray luma. Do not tint holder bright flame red/yellow or bake brown into neutral.'),
    effects=dict(flame='Preserve existing Prefabs/Particles/TorchpostFlames, separate from flame-free tile. No new drawn flame/halo/particle texture or duplicate sprite animation.',light='Native LightSource Lit=true Radius=6 remains unchanged; donor glow/fuel/heat/radius not imported.',prefab_visibility='PrefabImposter.Render adds prefab only when not Disabled, RenderEvent.Visible and RenderEvent.Lit>1. Defaults X/Y/Z/Layer remain native; do not change flame anchor to fit artwork.',
        code=[ref(PRIVATE/n) for n in ['AnimatedMaterialFire.cs','RenderEvent.cs','PrefabImposter.cs','BasePrefabImposter.cs']],resources=dict(path='D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/resources.assets',sha256='61f5c811a061626bc646f7ee654afb4575c2b4b9ad703a05b18655b2505ed376'),
        unlit=dict(definition=ref(base/'Furniture.xml'),object=unlit,ownership='Separate Unlit Torchpost blueprint with same holder tile, not proof that Torchpost has a toggle/state transition. This entry does not grant another blueprint readiness or implement extinguishing.')),
    variants=dict(native_body_tiles=['tiles/sw_torch_nofire.png'],random_tile=False,required_authoring_views=['south','east','north'],west='Mirror east only if the chosen structure is symmetric; no native orientation/placement implementation.',reason='MountedFurniture ancestry requires furniture views despite generic prop ledger category; native fixed tile remains current binding. Extra views unbound.'),
    donor_reference=dict(name='Actual Core TorchWallLamp S/E/N texture set',definition=dict(**ref(donordef),objects=[ET.tostring(n,encoding='unicode') for n in [wall,torch,base_def]]),resources=refs['resources'],assets=refs['textures'],
        mapping=dict(GraphicClass='Graphic_Multi',parent='TorchLamp/TorchBase',drawRotated_in_parent=False,draw_offsets=dict(north=[0,0,.9],south=[0,0,-.9],east=[.9,0,0],west=[-.9,0,0]),interpretation='Inspect actual directional wood ends and source render mapping; donor wall offsets/radius/placement are not recipient offsets.'),
        role='Cardinal small wood/iron support readability, restrained edge and material shading only. Actual Core torch is a slender wood support, not a complete Qud sconce equivalent. Preserve Qud broad rim, short stem, open support gaps, source cell placement and native particle relationship.'),
    construction_contract='Shared front width/depth/camera/component thickness must enter geometry and exact refinement prompt. Source holder covers x4..12,y16..21 only; do not enlarge to a full-cell tall torch. Unseen rim depth/back/strut arrangement are authored estimates. All new pixels remain detail role w. Keep upper cell region transparent for native flame.',
    native_activation=False)
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1300,800),'#142823');d=ImageDraw.Draw(plate);d.text((20,18),'TORCHPOST / flame-free source holder + native effect contract / actual Core references',font=font,fill='#e3cf43')
neutral=np.dstack([np.full((24,16,3),216,np.uint8),a[:,:,3]]);ni=Image.fromarray(neutral).resize((256,384),Image.Resampling.NEAREST);plate.paste(ni,(40,60),ni);native_rgb=np.zeros((24,16,3),np.uint8);native_rgb[:]=[152,135,95];ci=Image.fromarray(np.dstack([native_rgb,a[:,:,3]])).resize((256,384),Image.Resampling.NEAREST);plate.paste(ci,(360,60),ci)
for i,f in enumerate(['south','east','north']):
    r=next(r for r in refs['textures'] if r['name']=='WallTorch_'+f);im=Image.open(r['path']).convert('RGBA').resize((192,192),Image.Resampling.NEAREST);plate.paste(im,(690+i*195,135),im);d.text((690+i*195,360),f.upper(),font=font,fill='#e3cf43')
for x,s in [(25,'SOURCE DETAIL COVERAGE'),(350,'ACTUAL DETAIL w'),(700,'ACTUAL CORE S / E / N')]:d.text((x,460),s,font=font,fill='#e3cf43')
lines=['Native tile is ONLY the small bottom-cell holder: source bbox(4,16)-(12,21), all detail w.',
 'TorchpostFlames is an existing native particle prefab; keep it and its origin/visibility ownership.',
 'AnimatedMaterialFire changes foreground R/W/r/W; RenderEvent.ApplyColors(fg,priority) leaves detail alone.',
 'Do not bake flames, glow, red/yellow tint or a false whole-cell torch into replacement holder.',
 'Furniture requires S/E/N with shared geometry; unseen dimensions are authored, extra views unbound.',
 'Unlit Torchpost is a separate blueprint. No new toggle, lighting radius, fuel, heat or placement rule.']
for i,s in enumerate(lines):d.text((20,525+i*38),s,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference.png');now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][0],action='Resolve Torchpost ancestry, static holder-only detail mask, native foreground animation and separate flame prefab ownership.',inputs=[ref(p) for p in texts]+[ref(native)]+[ref(PRIVATE/n) for n in ['AnimatedMaterialFire.cs','RenderEvent.cs','PrefabImposter.cs','BasePrefabImposter.cs']],outputs=[ref(HERE/n) for n in ['prepare-source.py','source-packet.json','source-reference.png']],review='All visible tile pixels are detail w, not animated fire foreground. Native particle prefab, original visibility/offset and LightSource Radius6 stay native. Unlit Torchpost is separate identity. MountedFurniture requires S/E/N authoring without rewriting fixed enumerator variants; no native validation run.',result='PASS'))
entry.update(current_step=entry['required_steps'][1],authoring_views=packet['variants'],known_issues=['Inspect actual source/Core references, then construct short holder with shared physical S/E/N geometry and retained native flame space.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Resolved Torchpost holder-only detail w, native fire/prefab contract and three furniture views.')
