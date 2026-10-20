"""Source-bound slate door construction; native state/occlusion stays native."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, re, subprocess, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data')
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def save(name,x): (HERE/name).write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
index=json.loads((HERE/'native-state-index.json').read_text())
for row in index['states']: assert sha(Path(row['private_mask']['path']))==row['private_mask']['sha256']
definition=DATA/'StreamingAssets/Base/ObjectBlueprints/Furniture.xml'
# Other furniture definitions contain legacy numeric character references that
# modern XML parsers reject. Parse this exact object's valid source block only.
native=ET.fromstring(re.search(r'<object Name="Door"\s[^>]*>.*?</object>',definition.read_text(encoding='utf-8-sig'),re.S).group())
code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.Door',str(DATA/'Managed/Assembly-CSharp.dll')],capture_output=True,check=True).stdout
assert b'ClosedTile = "Tiles/sw_door_basic.bmp"' in code and b'OpenTile = "Tiles/sw_door_basic_open.bmp"' in code
reference=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='door.png')
assert sha(DONOR/'door.png')==reference['png_sha256']
packet=dict(entry='SCN-DOOR',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Door -> MountedFurniture',
 description=native.find("part[@Name='Description']").get('Short'),
 native_definition=dict(path=str(definition),sha256=sha(definition),selected=ET.tostring(native,encoding='unicode')),
 installed_state_evidence=dict(assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),class_name='XRL.World.Parts.Door',scoped_decompilation_sha256=hashlib.sha256(code).hexdigest(),
  facts=['SyncRender defaults true. ObjectCreatedEvent selects ClosedTile or OpenTile, superseding the static blueprint thumbnail.',
   'ClosedTile=Tiles/sw_door_basic.bmp; OpenTile=Tiles/sw_door_basic_open.bmp.',
   'Open sets Render.Occluding=false and Physics.Solid=false. Closed restores solid/occluding state; native code and caches own this behavior.']),
 source_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),
 palette=dict(primary='y',detail='y',native_rgb='b1c9c3',ownership='Native runtime arch uses R255/detail, leaf R0/foreground; equal current colors do not erase these roles.'),
 donor_reference=dict(package='RimWorld Core',record=reference,path=str(DONOR/'door.png'),sha256=sha(DONOR/'door.png'),
  role='Actual DoorSimple_Mover supplies restrained planar shading and handle readability only. It is a rectangular moving panel, not an equivalent arched slate design. No donor sliding motion, wood appearance or mechanics is copied.'),
 authored_interpretation='Arched frame and chipped slate slab preserve native stepped/rounded outline, left hinges and right recessed handle. Restrained slate lamination, faint hand wear and pitted hinges derive from the description. Rust stays a neutral value role so native y palette remains authoritative.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],anchor=[8,16],rule='Same native-coordinate frame in both states. Frame is byte-identical; open leaf becomes the source left edge-on strip, not a newly centered or sliding door.'),
 views='Only native closed/open map views are required. No unsupported north/east art is inferred from a generic door graphic.',
 native_acceptance='Deferred until every conversion is generation-ready')
save('source-packet.json',packet)
frame='M1.05 22.9V5.05L4.1 1.05H11.9L14.95 5.05V22.9H14.05V5.45L11.5 2.5H4.5L1.95 5.45V22.9Z'
leaf='M3.1 21.95V19.1L3.85 18.9V17L3.1 16.8V12.05L3.85 11.85V10.15L3.1 9.95V7.2L5.15 5.1H10.85L12.9 7.2V21.95Z'
defs='<defs><linearGradient id="slate"><stop stop-color="#a8a8a8"/><stop offset=".35" stop-color="#d2d2d2"/><stop offset="1" stop-color="#b4b4b4"/></linearGradient></defs>'
frame_svg=f'<path d="{frame}" fill="url(#slate)" stroke="#404040" stroke-width=".14"/><path d="M1.53 22.6V5.2L4.3 1.7H11.7L14.48 5.2V22.6" fill="none" stroke="#ececec" stroke-width=".1"/>'
leaf_svg=f'<path d="{leaf}" fill="url(#slate)" stroke="#3e3e3e" stroke-width=".18"/>'
leaf_svg+='''<path d="M4.6 7.7L11.9 8.05M4.2 10.4L12.3 10.1M4.4 16.8L12.2 16.45M4.1 20.2L11.9 20.5" fill="none" stroke="#989898" stroke-width=".07"/>
<path d="M3.3 10.3H4.1V11H3.3M3.3 17.5H4.1V18.2H3.3" fill="#656565" stroke="#3c3c3c" stroke-width=".09"/>
<ellipse cx="3.65" cy="10.3" rx=".38" ry=".18" fill="none" stroke="#8d8d8d" stroke-width=".12"/>
<path d="M10.55 13.15H11.7V15.3H11.3V13.55H10.55Z" fill="#424242"/>
<ellipse cx="9.8" cy="13.6" rx=".53" ry=".7" fill="#969696" opacity=".16"/>
<path d="M8.95 12.9L8.8 12.4M9.3 12.75V12.15M9.65 12.7V12.05M10 12.8L10.15 12.3" stroke="#939393" stroke-width=".15" opacity=".18"/>'''
open_svg='<path d="M3.05 21.95V6H3.95V21.95Z" fill="#a0a0a0" stroke="#404040" stroke-width=".14"/><path d="M3.25 6.15V21.7" stroke="#dedede" stroke-width=".12"/>'
for name,content in [('closed',frame_svg+leaf_svg),('open',frame_svg+open_svg),('leaf',leaf_svg),('frame',frame_svg)]:
 text=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{defs}{content}</svg>'
 (HERE/f'constructed-{name}.svg').write_bytes(text.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{name}.svg'),skip_system_fonts=True))
plate=Image.new('RGB',(1440,760),'#142823');draw=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
draw.text((20,15),'DOOR / actual runtime closed > editable weathered slate > native open state > actual Core reference',font=font,fill='#e3cf43')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];raw=Image.open(Path(index['states'][1]['private_mask']['path'])).convert('RGBA');original=Image.new('RGBA',raw.size,'#'+palette['k'])
color=bytes.fromhex(palette['y'])
for y in range(raw.height):
 for x in range(raw.width):
  if raw.getpixel((x,y))[3]:original.putpixel((x,y),(*color,255))
plate.paste(original.resize((256,384),Image.Resampling.NEAREST).convert('RGB'),(30,80))
for x,name in [(390,'closed'),(750,'open')]:
 im=Image.open(HERE/f'constructed-{name}.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(x,80),im)
im=Image.open(DONOR/'door.png').convert('RGBA').resize((224,224),Image.Resampling.NEAREST);plate.paste(im,(1130,155),im)
for x,label in [(20,'Native runtime closed'),(370,'Manual / slate + hinges'),(730,'Manual / fixed-frame open'),(1090,'Core DoorSimple_Mover')]:draw.text((x,500),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['The blueprint thumbnail differs from the Door part runtime tile. Both source states were extracted and decoded.',
 'Slate, left hinges, right recessed handle and hand wear follow Qud. Core panel contributes only rendering conventions.',
 'Both native palette roles are y here. Neutral materials retain independent arch/detail and leaf/foreground ownership.',
 'Open preserves the exact arch and leaves a thin slate edge on the source left; no collision/occlusion code is replaced.']):draw.text((20,570+34*i),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
