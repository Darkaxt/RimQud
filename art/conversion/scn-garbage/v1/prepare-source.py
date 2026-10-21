"""Capture Garbage's actual native random tiles and private Core trash references."""
from pathlib import Path
from datetime import datetime,timezone
import sys,importlib.util,json,hashlib,struct,re,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/rimqud-native-garbage-20261021');PRIVATE.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=sha(p))
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-GARBAGE';entry=next(e for e in ledger['entries'] if e['id']=='SCN-GARBAGE');assert not entry['process_log']
defs=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Items.xml');fragment=re.search(r'<object Name="Garbage"(?=\s|>).*?</object>',defs.read_text(),re.S).group();node=ET.fromstring(fragment)
random=next(n for n in node.findall('builder') if n.get('Name')=='RandomTile').get('Tiles').split(',');fallback=node.find('part[@Name="Render"]').get('Tile');assert len(random)==4
tiles=random+[fallback]
spec=importlib.util.spec_from_file_location('qud_tile_decode',ROOT/'tools/extract_village_references.py');decode=importlib.util.module_from_spec(spec);spec.loader.exec_module(decode)
wanted={decode.key(tile):tile for tile in tiles};qud=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/resources.assets');assert sha(qud)=='61f5c811a061626bc646f7ee654afb4575c2b4b9ad703a05b18655b2505ed376'
env=UnityPy.load(str(qud));objects={o.path_id:o for o in env.objects};states=[];atlases={}
for obj in env.objects:
    if obj.type.name!='MonoBehaviour':continue
    raw=obj.get_raw_data()
    try:
        name,off=decode.string(raw,28)
        if name.lower() not in wanted:continue
        _,off=decode.string(raw,off);_,off=decode.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotation=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotation
        if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
        im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));slug=re.sub(r'[^a-z0-9_-]','-',wanted[name.lower()].lower().replace('/','_'));p=PRIVATE/(slug+'-mask.png');crop.save(p)
        states.append(dict(native_tile=wanted[name.lower()],info_id=obj.path_id,atlas_id=atlas,rect=[x,y,w,h],private_mask=ref(p),role='RandomTile choice' if wanted[name.lower()] in random else 'Declared Render fallback; not a fifth random choice'))
    except (ValueError,UnicodeDecodeError,struct.error):continue
assert {s['native_tile'] for s in states}==set(tiles)
states.sort(key=lambda r:tiles.index(r['native_tile']));write(HERE/'native-state-index.json',dict(resources=ref(qud),states=states))
del env,objects,atlases
core=Path('D:/Steam/steamapps/common/RimWorld');donordef=core/'Data/Core/Defs/ThingDefs_Misc/Filth_Various.xml';filth=next(n for n in ET.parse(donordef).getroot() if n.findtext('defName')=='Filth_Trash')
asset=core/'RimWorldWin64_Data/resources.assets';env=UnityPy.load(str(asset));references=[]
for obj in env.objects:
    if obj.type.name!='Texture2D':continue
    data=obj.read()
    if data.m_Name not in ['TrashA','TrashB','TrashC']:continue
    p=PRIVATE/('core-'+data.m_Name+'.png');data.image.convert('RGBA').save(p);references.append(dict(**ref(p),name=data.m_Name,source_id=obj.path_id,role='Actual Core trash scatter: outline, overlapping fragments and quiet map-art shading only; do not copy its exact rubbish contents, palette, footprint, rotation or filth mechanics.'))
assert {r['name'] for r in references}=={'TrashA','TrashB','TrashC'};references.sort(key=lambda r:r['name'])
packet=dict(entry='SCN-GARBAGE',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Garbage -> Item',description=entry['metadata']['description']['Short'],source_definition=dict(**ref(defs),object=fragment),original_reference=entry['metadata']['original_reference'],native_states=ref(HERE/'native-state-index.json'),
    required_native_art=dict(random_tile_choices=random,declared_fallback=fallback,selection='Native RandomTile builder owns selection. Preserve all four actual choices; keep declared fallback distinguishable. No inferred adjacency, animation or view-state conversion.',burning='BurnGenerateObjectInCell may create a separate native TrashFire-table object; it does not establish an extra burning Garbage texture. No fire simulation or art is invented here.'),
    source_parts={n.get('Name'):dict(n.attrib) for n in node.findall('part')},
    palette=dict(ColorString='&K^k',primary='K',background='k',detail='Not explicitly set on Garbage; resolve inherited/default/native mapping before final registration. Do not treat ^k background as a DetailColor or bake it into object alpha.',inspection='Source plate uses neutral primary/detail tones to make masks readable; it is not a claim of final native colour rendering.'),
    donor_reference=dict(definition=dict(**ref(donordef),object=ET.tostring(filth,encoding='unicode')),resources=ref(asset),assets=references,role='Visual map-scatter convention only. Qud description, individual tile layouts and dark source palette govern the new art.'),
    construction_contract='Preserve the recognisable layout/coverage of each Qud variant. Reconstruct readable fragments including glass lens, ink serif, corroded lug and wire ribbon without turning every blob into a generic bottle/can pile. Unseen material surfaces and exact fragment identities remain authored interpretations.',
    views='Fixed map-facing debris, not furniture: one source-bound view per actual tile choice/fallback. No invented south/east/north turnaround or runtime rotation.',
    scope='Source/reference preparation only; construction, actual refinement, extraction/registration, palette resolution and final art review remain unfinished.',native_activation=False)
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);sheet=Image.new('RGB',(1400,900),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'GARBAGE / FOUR actual RandomTile choices + declared fallback / source inspection',font=font,fill='#e3cf43')
for i,state in enumerate(states):
    a=np.array(Image.open(state['private_mask']['path']).convert('RGBA'));weight=a[:,:,:1].astype(float)/255;rgb=np.uint8(np.round((1-weight)*225+weight*150));im=Image.fromarray(np.concatenate([np.repeat(rgb,3,axis=2),a[:,:,3:]],axis=2)).resize((160,240),Image.Resampling.NEAREST);xx=25+i*275;sheet.paste(im,(xx,65),im);d.text((xx,325),'CHOICE '+str(i+1) if i<4 else 'DECLARED FALLBACK',font=font,fill='#e3cf43');d.text((xx,355),Path(state['native_tile']).name,font=font,fill='#e5e8d8')
for i,r in enumerate(references):
    im=Image.open(r['path']).convert('RGBA');im.thumbnail((210,210),Image.Resampling.LANCZOS);xx=50+i*330;sheet.paste(im,(xx,440),im);d.text((xx,680),'ACTUAL CORE '+r['name'],font=font,fill='#e3cf43')
for i,line in enumerate(['Qud prose: glass lens, ink serif, acid-eaten lug, ribbon of wire. Keep source layout and dark K/^k palette.',
    'Core samples guide scatter/readability only; their contents, colours, size and filth behavior are not imported.',
    'Neutral source-mask tones shown for inspection; inherited DetailColor is unresolved before registration.',
    'No construction/refinement/registered replacement or native acceptance yet.']):d.text((18,745+i*32),line,font=font,fill='#e5e8d8')
sheet.save(HERE/'source-reference-variants.png')
now=datetime.now(timezone.utc).isoformat()
def event(step,action,ins,outs,review):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(p) for p in ins],outputs=[ref(p) for p in outs],review=review,result='PASS'))
event(entry['required_steps'][0],'Resolve exact Garbage definition and extract all four native RandomTile choices plus declared fallback from version-pinned Qud resources.',[defs,qud],[HERE/'prepare-source.py',HERE/'native-state-index.json',HERE/'source-packet.json',HERE/'source-reference-variants.png'],'Old catalogue declared tile alone omits four builder-selected shapes. All five source masks retained privately with exact atlas/rect/hash. Native selection, non-solid/takeable behavior and separate burning object ownership retained; final detail-colour mapping remains explicitly unresolved.')
entry.update(current_step=entry['required_steps'][1],known_issues=['Actual source variants and Core references extracted. Inspect reference plate, then construct each source-bound debris shape, refine, resolve inherited DetailColor, register and review. No generation-ready credit yet.'])
ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Captured all4actual trash choices plus declared fallback and three actual Core references; reference inspection and construction pending.')
