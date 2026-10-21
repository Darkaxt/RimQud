"""Resolve Painting's native designs, colour ownership and actual directional reference."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re, struct, sys, importlib.util
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
PRIVATE=Path('E:/Temp/rimqud-native-painting-20261021'); PRIVATE.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=sha(p))
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x): p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json'); assert ledger['active_entry']=='SCN-PAINTING'
entry=next(e for e in ledger['entries'] if e['id']=='SCN-PAINTING'); assert not entry['process_log']
defs=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml')
text=defs.read_text(); ancestry=[]
for name in ['Painting','MountedFurniture','Furniture']:
    match=re.search(r'<object\s+Name="'+name+r'"(?=\s|>).*?</object>',text,re.S)
    assert match, name
    ancestry.append(dict(name=name,definition=ref(defs),object=match.group()))
node=ET.fromstring(ancestry[0]['object']); tiles=node.find('builder[@Name="RandomTile"]').get('Tiles').split(','); assert len(tiles)==2
spec=importlib.util.spec_from_file_location('decode',ROOT/'tools/extract_village_references.py'); decode=importlib.util.module_from_spec(spec); spec.loader.exec_module(decode)
asset=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/resources.assets')
assert sha(asset)=='61f5c811a061626bc646f7ee654afb4575c2b4b9ad703a05b18655b2505ed376'
env=UnityPy.load(str(asset)); objects={o.path_id:o for o in env.objects}; wanted={decode.key(t):t for t in tiles}; states=[]; atlases={}
for obj in env.objects:
    if obj.type.name!='MonoBehaviour': continue
    raw=obj.get_raw_data()
    try:
        name,off=decode.string(raw,28)
        if name.lower() not in wanted: continue
        _,off=decode.string(raw,off); _,off=decode.string(raw,off)
        atlas=struct.unpack_from('<q',raw,off+4)[0]; rotation=struct.unpack_from('<i',raw,off+12)[0]; x,y,w,h=struct.unpack_from('<4i',raw,off+40); assert not rotation
        if atlas not in atlases: atlases[atlas]=objects[atlas].read().image.convert('RGBA')
        im=atlases[atlas]; crop=im.crop((x,im.height-y-h,x+w,im.height-y)); target=PRIVATE/(Path(wanted[name.lower()]).stem+'-mask.png'); crop.save(target)
        states.append(dict(native_tile=wanted[name.lower()],info_id=obj.path_id,atlas_id=atlas,rect=[x,y,w,h],private_mask=ref(target)))
    except (ValueError, UnicodeDecodeError, struct.error): continue
assert len(states)==2; states.sort(key=lambda s:tiles.index(s['native_tile']))
write(HERE/'native-state-index.json',dict(resources=ref(asset),states=states))
del env, objects, atlases
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324')
donordef=Path('D:/Steam/steamapps/common/RimWorld/Data/Ideology/Defs/ThingDefs_Buildings/Buildings_Misc.xml')
lectern=next(n for n in ET.parse(donordef).getroot() if n.findtext('defName')=='Lectern')
references=[dict(**ref(donor/f'Textures/Things/Building/Misc/Lectern/Lectern_{f}.png'),facing=f) for f in ['south','east','north']]
random_code=PRIVATE/'RandomColors.cs'; cell=Path('E:/Temp/qud-transplant-probe-pawns-20261019/scratch/inspect/XRL.World.Cell.decompiled.cs')
assert 'render.TileColor = text2' in random_code.read_text(encoding='utf-8-sig')
assert 'E.ColorString = render2.TileColor' in cell.read_text(encoding='utf-8-sig')
packet=dict(entry='SCN-PAINTING',timestamp=datetime.now(timezone.utc).isoformat(),identity='Painting -> MountedFurniture -> Furniture',description=entry['metadata']['description']['Short'],ancestry=ancestry,
    native_states=ref(HERE/'native-state-index.json'),native_parts={n.get('Name'):dict(n.attrib) for n in node.findall('part')},
    palette=dict(declared_tile_primary='w',declared_detail='R',random_glyph_main=['m','W','r','R','b','B','g','G'],random_detail=['m','W','r','R','b','B','g','G'],
        effective_tile_primary='w: RandomColors.MainColor changes ColorString only. TileColor is unspecified on the builder, so declared Render.TileColor=&w remains and Cell prefers it for tile rendering.',
        effective_detail='Native creation chooses one of eight DetailColor values independently of glyph MainColor (PairDetailWithForeground defaults false). Declared R is a fallback/example, not every painting.',
        ownership='Opaque source R=0 is primary, R=255 detail; A is object coverage. Keep masks separate and apply runtime values. No palette clocks or resampling of native random choices.',
        evidence=[ref(random_code),ref(cell)]),
    donor_reference=dict(name='Vanilla Textures Expanded / Ideology Lectern',definition=dict(**ref(donordef),object=ET.tostring(lectern,encoding='unicode')),about=ref(donor/'About/About.xml'),load_folders=ref(donor/'LoadFolders.xml'),assets=references,
        mapping=dict(GraphicClass='Graphic_Multi',drawSize=[1,1],size=[1,1],interpretation='Actual texture/margins and shared one-cell drawing frame; not an easel footprint or width-ratio target.'),
        role='Supported panel, quiet outline/material shading and cardinal map-camera reference only. No close whole easel equivalent found in bounded installed filename inventory. Do not substitute the lectern, ritual behavior or pedestal.'),
    views=dict(required=['south','east','north'],west='Author or mirror only if geometry permits; this construction is bilaterally symmetric in structure, back motif is not mirrored onto canvas reverse.',reason='MountedFurniture inheritance requires furniture turnaround despite catalogue fixed-prop category. Extra facings remain unbound authoring assets.'),
    uncertainties=['Painting subject is unspecified: preserve the two actual abstract source motifs; do not invent a portrait, landscape or text.','Easel depth, canvas thickness, rear brace and unseen reverse are authored estimates, not metadata dimensions.'],
    process='Exact original masks -> editable physical easel and distinct abstract paint motifs -> three coherent cardinal views -> actual restrained ImageGen material proposal -> inspect/patch while preserving geometry -> registered neutral primary/detail/coverage and native palette examples.',native_activation=False)
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
sheet=Image.new('RGB',(1250,810),'#142823'); d=ImageDraw.Draw(sheet); d.text((20,18),'PAINTING / two native designs / actual directional reference',font=font,fill='#e3cf43')
for i,s in enumerate(states):
    a=np.array(Image.open(s['private_mask']['path']).convert('RGBA')); weight=a[:,:,:1].astype(float)/255
    rgb=np.uint8(np.round((1-weight)*224+weight*142)); im=Image.fromarray(np.concatenate([np.repeat(rgb,3,2),a[:,:,3:]],2)).resize((192,288),Image.Resampling.NEAREST)
    sheet.paste(im,(60+i*290,65),im); d.text((35+i*290,365),Path(s['native_tile']).name,font=font,fill='#e5e8d8')
    print(s['native_tile'])
    for row in a: print(''.join('.' if p[3]==0 else 'P' if p[0]<128 else 'D' for p in row))
for i,r in enumerate(references):
    im=Image.open(r['path']).convert('RGBA'); print('donor',r['facing'],im.size,im.getbbox()); im=im.resize((192,192),Image.Resampling.NEAREST); sheet.paste(im,(650+i*195,105),im); d.text((650+i*195,330),r['facing'],font=font,fill='#e3cf43')
lines=['Qud: nacreous oil on ecru linen; paint has dripped onto an easel. No depicted subject is specified.',
 'Two native RandomTile choices; native creation owns variant and colour selection.',
 'Tile primary stays w. RandomColors.MainColor changes glyph ColorString; TileColor is not assigned.',
 'Eight native detail choices. Neutral mask tones above show roles, not final painting colours.',
 'Actual mod Lectern S/E/N textures guide map-camera/materials only; no close whole easel equivalent.',
 'Shared physical width/depth, component thickness and map-camera elevation will govern all views.',
 'Source-supported form and authored hidden structure will be recorded separately. Native tests deferred.']
for i,line in enumerate(lines): d.text((20,475+i*39),line,font=font,fill='#e5e8d8')
sheet.save(HERE/'source-reference.png')
now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][0],action='Resolve Painting ancestry, extract both native RandomTile masks, and trace independent glyph/tile/detail colour assignment.',inputs=[ref(defs),ref(asset),ref(random_code),ref(cell)],outputs=[ref(HERE/n) for n in ['prepare-source.py','native-state-index.json','source-packet.json','source-reference.png']],review='Actual source masks and code captured. Tile primary remains w; eight native detail choices, separate randomized glyph main. Furniture inheritance requires S/E/N. Construction and reference visual review remain pending.',result='PASS'))
entry.update(current_step=entry['required_steps'][1],known_issues=['Native source and actual references resolved; inspect motifs/reference and construct coherent easel turnarounds. No generation-ready credit yet.'],authoring_views=packet['views'])
ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
