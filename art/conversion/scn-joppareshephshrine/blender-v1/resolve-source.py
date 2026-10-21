"""Resolve actual native shrine initialization tiles before constructing a model."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,struct,sys,importlib.util,subprocess,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/rimqud-native-shrine-20261021');PRIVATE.mkdir(exist_ok=True)
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');DEFS=NATIVE/'StreamingAssets/Base/ObjectBlueprints';ASSEMBLY=NATIVE/'Managed/Assembly-CSharp.dll';ASSET=NATIVE/'resources.assets';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');DONOR=MOD/'Textures/Things/Building/Furniture/LargeSteleA.png'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'source-packet.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-JOPPARESHEPHSHRINE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert not entry['process_log'];ancestry={}
for name,f in [('JoppaReshephShrine','Furniture.xml'),('SultanShrine','Furniture.xml'),('MountedFurniture','Furniture.xml'),('Furniture','Furniture.xml'),('InorganicObject','PhysicalPhenomena.xml'),('PhysicalObject','PhysicalPhenomena.xml')]:
 p=DEFS/f;m=re.search(r'<object\s+Name="'+name+r'"[^>]*>.*?</object>',p.read_text(encoding='utf-8-sig'),re.S);assert m,name;ET.fromstring(m.group());ancestry[name]=dict(file=ref(p),selected=m.group())
codes={}
for name in ['SultanShrine','Shrine','RandomSubterraneanColors']:
 p=PRIVATE/(name+'.cs');result=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.'+name,str(ASSEMBLY)],check=True,capture_output=True,text=True);p.write_text(result.stdout,encoding='utf-8',newline='\n');codes[name]=ref(p)
code=(PRIVATE/'SultanShrine.cs').read_text();assert 'Terrain/sw_resheph_sultanstatue.bmp' in code and 'terrain/sw_tombstone_' in code and 'Stat.Random(1, 4)' in code
tiles=['Terrain/tile_tombstone1.png']+[f'terrain/sw_tombstone_{i}.bmp' for i in range(1,5)]+['Terrain/sw_resheph_sultanstatue.bmp']
spec=importlib.util.spec_from_file_location('decode',ROOT/'tools/extract_village_references.py');decode=importlib.util.module_from_spec(spec);spec.loader.exec_module(decode);wanted={decode.key(t):t for t in tiles};env=UnityPy.load(str(ASSET));objects={o.path_id:o for o in env.objects};atlases={};states=[]
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=decode.string(raw,28)
  if name.lower() not in wanted:continue
  _,off=decode.string(raw,off);_,off=decode.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotation=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotation
  if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
  im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));target=PRIVATE/(Path(wanted[name.lower()]).stem+'-mask.png');crop.save(target)
  states.append(dict(native_tile=wanted[name.lower()],info_id=obj.path_id,atlas_id=atlas,rect=[x,y,w,h],private_mask=ref(target)))
 except (ValueError,UnicodeDecodeError,struct.error):continue
assert len(states)==len(tiles),(tiles,states);states.sort(key=lambda r:tiles.index(r['native_tile']));assert states[0]['private_mask']['sha256']==entry['metadata']['original_reference']['native_mask_sha256'];del env,objects,atlases
write(HERE/'native-state-index.json',dict(assembly=ref(ASSEMBLY),resources=ref(ASSET),states=states))
packet=dict(entry=entry['id'],identity='JoppaReshephShrine -> SultanShrine -> MountedFurniture -> Furniture -> InorganicObject -> PhysicalObject -> Object',declared_description='',ancestry=ancestry,native_states=ref(HERE/'native-state-index.json'),native_code=codes,
 source_resolution=dict(catalogue_tile='Terrain/tile_tombstone1.png',preinitialization_fallbacks=tiles[1:5],normal_resheph_tile=tiles[-1],reason='EnteredCell assigns one of four native tombstones, then ShrineInitialize selects the named Resheph statue when a historical snapshot is available. Declared catalogue icon alone is not the stable native identity.',gospel='Description is supplied from native sultan history and JoppaShrine gospel; do not invent a fixed historical scene or inscription.'),
 palette=dict(primary='Declared ColorString y, black background k; no TileColor override declared',detail='Declared g, with native RandomSubterraneanColors DetailColor r,c,w,Y for inside zones only',worship='Native WorshipColorString Y / WorshipDetailColor C; preserve event-owned appearance',rule='Use semantic neutral primary/detail and one coverage; do not freeze all runtime states to a single preview palette.'),
 native_behavior=dict(default_initialized=False,current_runtime_initialized='Not captured this turn',preset_gospel_by_property='JoppaShrine',pregenerated_name='Resheph',epithet='the Last Sultan',worship_faction='Resheph',worship_power=3,quest_events=['Prayed','Desecrated'],zone_landmark_radius=6,solid=True,takeable=False,occluding=False,render_layer=8,scope='Keep native history initialization, look/reveal, worship, interior random-color behavior and solid mounted-furniture ownership. No new animation, clock or history content.'),
 donor_reference=dict(name='Vanilla Textures Expanded LargeSteleA',package_id='VanillaExpanded.VTEXE',workshop_id='2016436324',asset=ref(DONOR),about=ref(MOD/'About/About.xml'),role='Actual installed neutral engraved-monument shading/edge reference only; do not copy its slab silhouette, iconography, size or gameplay.'),
 authored_interpretation='Pending inspection of all six actual source masks. Stone-like surface and hidden depth will be explicit construction estimates, not recovered native dimensions.',
 view_contract=dict(required=['south','east','north'],reason='MountedFurniture ancestry requires complete cardinal authoring views. Source-supported tile state stays native, auxiliary facings do not establish native direction dispatch.',frame='Each source16x24 cell retains common full-cell registration and anchor; physical model rotation rather than per-facing bounds resizing.'),
 next_action='Inspect six decoded masks and model their source-supported distinct silhouettes/material roles. No geometry or generation-ready credit yet.',native_activation=False,native_acceptance='Pending full generation gate')
write(HERE/'source-packet.json',packet)
pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.array(list(bytes.fromhex(pal['y'])));dt=np.array(list(bytes.fromhex(pal['g'])));font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14);plate=Image.new('RGB',(1540,830),'#142823');d=ImageDraw.Draw(plate)
for i,state in enumerate(states):
 a=np.array(Image.open(state['private_mask']['path']).convert('RGBA'));w=a[:,:,:1].astype(float)/255;native=np.dstack([np.uint8(np.round((1-w)*fg+w*dt)),a[:,:,3]]);im=Image.fromarray(native).resize((224,336),Image.Resampling.NEAREST);bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB'),(15+i*255,65));d.text((15+i*255,18),['CATALOGUE FALLBACK','INITIAL TOMBSTONE1','INITIAL TOMBSTONE2','INITIAL TOMBSTONE3','INITIAL TOMBSTONE4','NORMAL RESHEPH'][i],font=font,fill='#e3cf43');print(state['native_tile'])
 for row in a:print(''.join(' ' if p[3]==0 else 'P' if p[0]<128 else 'D' for p in row))
donor=Image.open(DONOR).convert('RGBA');bg=Image.new('RGBA',donor.size,'#20382d');bg.alpha_composite(donor);plate.paste(ImageOps.contain(bg.convert('RGB'),(280,280),Image.Resampling.NEAREST),(25,445))
for i,line in enumerate(['Actual VTE engraved monument / material reference only',
 'Native initialization changes the catalogue tile; normal Resheph uses the far-right statue.',
 'Intermediate tombstones remain possible native fallbacks; no fixed history image or text is invented.',
 'Preview uses declared y/g. Interior random detail and worship Y/C remain native-owned.',
 'No model or in-game acceptance claimed. Source shapes must be inspected before construction.']):d.text((335,485+i*42),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-state-reference-comparison.png');now=datetime.now(timezone.utc).isoformat()
for step,action,inputs in [('resolve_object_description_original_tile_palette_state','Resolve shrine ancestry, actual initialization/statue tile replacement, interior random colors and worship ownership; extract all six source masks.',[ref(ASSEMBLY),ref(ASSET),*codes.values()]),('select_render_reference_or_document_no_equivalent','Inspect actual installed VTE LargeSteleA for restrained engraved monument materials and edges only.',[ref(DONOR),ref(MOD/'About/About.xml')])]:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=[ref(HERE/'source-packet.json'),ref(HERE/'native-state-index.json'),ref(HERE/'source-state-reference-comparison.png')],review='Catalogue fallback is not the normal Resheph appearance. Exact six native source shapes and code are retained; construction remains required and native behavior is not replaced.',result='PASS'))
entry.update(current_step='construct_faithful_shape',known_issues=['Actual shrine initialization selects a Resheph statue; six source masks resolved, geometry and cardinal/material authoring still required.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger);print('Shrine source resolution retained; construction remains pending.')
