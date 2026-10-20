"""Bind the native gearbox-wall variant to its genuinely shared ordinary artwork."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BASE=ROOT/'art/conversion/scn-brinestalkwall/v1'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Walls.xml')
ASSEMBLY=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed/Assembly-CSharp.dll')
ILSPY=Path('C:/Users/darka/.dotnet/tools/ilspycmd.exe')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
refs=json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries']
ref=next(x for x in refs if x.get('blueprint')=='BrinestalkWallWithGearbox')
plain=next(x for x in refs if x.get('blueprint')=='BrinestalkWall')
assert ref['native_mask_sha256']==plain['native_mask_sha256']
assert ref['reference_sha256']==plain['reference_sha256']
assert sha(DONOR/ref['reference_file'])==ref['reference_sha256']
assert sha(DONOR/'village-originals/brinestalkwallwithgearbox-mask.png')==ref['native_mask_sha256']
tree=ET.parse(NATIVE).getroot();definition=tree.find(".//object[@Name='BrinestalkWallWithGearbox']")
assert definition.get('Inherits')=='BrinestalkWall'
assert definition.find("part[@Name='Render']") is None
assert definition.find("part[@Name='ModGearbox']") is not None
classes={}
for name in ['ModGearbox','MechanicalPowerTransmission','IPowerTransmission']:
 p=subprocess.run([str(ILSPY),'-t','XRL.World.Parts.'+name,str(ASSEMBLY)],capture_output=True,check=True)
 code=p.stdout.decode('utf-8-sig');classes[name]=dict(type='XRL.World.Parts.'+name,scoped_decompilation_sha256=hashlib.sha256(p.stdout).hexdigest())
 if name=='ModGearbox':assert 'new MechanicalPowerTransmission()' in code
 if name=='MechanicalPowerTransmission':assert 'TileEffects = true' not in code
 if name=='IPowerTransmission':assert 'public bool TileEffects;' in code and 'if (TileEffects)' in code
packet=dict(entry='SCN-BRINESTALKWALLWITHGEARBOX',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='BrinestalkWallWithGearbox -> BrinestalkWall -> BaseWallWood -> Wall',
 description=ref['description'],original=ref,
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),parent='BrinestalkWall',added_part='ModGearbox',own_render_override=False),
 assembly=dict(path=str(ASSEMBLY),sha256=sha(ASSEMBLY),scoped_types=classes,
  inspection='Scoped ilspycmd inspection only; raw decompiled classes remain private and are not included in this repository.'),
 mechanical_facts=dict(modification='Adds MechanicalPowerTransmission or updates its charge rate; adds gearbox name/description information.',
  default_appearance='MechanicalPowerTransmission does not enable tile effects. IPowerTransmission TileEffects is an uninitialized bool defaulting false; its Render calls SyncTile only when enabled. Installed ordinary gearbox-wall references have exactly the same sprite/mask/palette as BrinestalkWall.',
  boundary='These installed defaults and exported ordinary appearance do not prove all future mod/runtime states. Preserve native changed-tile, powered/broken/spark/overlay behavior rather than inventing a new exposed-gear sprite.'),
 shared_conversion=dict(entry='SCN-BRINESTALKWALL',model=asset(BASE/'registered-v2/model.json'),source=asset(BASE/'source-packet.json'),
  provenance='Adopt the actual original/reference/manual face/refinement/rejected-cap/corrected16state conversion. No duplicate generation and no new machinery decal.'),
 required_states='All16recipient cardinal connections inherit the same fixed frame, primary/detail roles and material. Machinery/power behavior remains a separate native component, not additional painted parts.',
 authoring_decision='Use shared converted wall art for the unchanged ordinary native appearance. The word gearbox alone is not a visual-design reference.',
 native_acceptance='Deferred until all pending conversions are generation-ready; ordinary appearance and changed-state fallback remain final integration checks.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
base=json.loads((BASE/'registered-v2/model.json').read_text())
model=dict(kind='connected_wall_blueprint_binding',blueprint='BrinestalkWallWithGearbox',base_model=asset(BASE/'registered-v2/model.json'),
 primary=base['primary'],detail=base['detail'],states=base['states'],registration=base['registration'],
 source=asset(HERE/'source-packet.json'),native_component='ModGearbox -> MechanicalPowerTransmission',extra_visible_overlay=None,
 binding='Reuse converted brinestalk wall only while the native visible wall tile/palette belongs to the supported ordinary family. Other actual appearances retain native art; power transmission stays in Qud.',
 state='Generation-ready shared art binding; native state/visibility/integration acceptance pending')
(HERE/'model.json').write_bytes((json.dumps(model,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
plate=Image.new('RGB',(1440,800),'#142823');d=ImageDraw.Draw(plate)
d.text((24,18),'GEARBOX WALL / same ordinary source appearance / distinct native power component',font=font,fill='#e3cf43')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
for i,name in enumerate(['brinestalkwall','brinestalkwallwithgearbox']):
 raw=Image.open(DONOR/f'village-originals/{name}-mask.png').convert('RGBA');original=Image.new('RGBA',raw.size,'#'+palette['k'])
 for y in range(raw.height):
  for x in range(raw.width):
   rr,_,_,aa=raw.getpixel((x,y));mix=rr/255
   if aa:original.putpixel((x,y),(*[round(a*(1-mix)+b*mix) for a,b in zip(bytes.fromhex(palette['w']),bytes.fromhex(palette['y']))],aa))
 plate.paste(original.resize((192,288),Image.Resampling.NEAREST).convert('RGB'),(64+i*300,100))
 d.text((32+i*300,440),'ORIGINAL '+('PLAIN WALL' if i==0 else 'GEARBOX WALL'),font=font,fill='#e5e8d8')
 # Same selected example state in each column, with both native color roles.
 st=base['states'][10];a=Image.open(ROOT/st['primary']['path']).convert('RGBA');b=Image.open(ROOT/st['detail']['path']).convert('RGBA')
 def tint(im,key):
  v=im.getchannel('R');c=bytes.fromhex(palette[key]);return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
 selected=tint(a,'w');selected.alpha_composite(tint(b,'y'));selected=selected.resize((320,320),Image.Resampling.LANCZOS)
 plate.paste(selected,(722+i*345,100),selected);d.text((700+i*345,440),'SHARED SELECTED '+('PLAIN' if i==0 else 'GEARBOX'),font=font,fill='#e5e8d8')
for j,t in enumerate(['Exact ordinary original mask/reference hashes and native render values match.',
 'The installed modification adds power transmission and descriptive text; it does not supply an exposed-gear sprite.',
 'Adopt all16performed wall states and their original-to-refinement evidence. No duplicate ImageGen call.',
 'Native power, changed appearance, overlays and unsupported states stay native; integration acceptance is pending.']):d.text((24,530+j*36),t,font=font,fill='#e5e8d8')
plate.save(HERE/'shared-appearance-comparison.png')
