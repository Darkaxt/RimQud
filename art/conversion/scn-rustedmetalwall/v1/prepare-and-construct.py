"""Construct source-owned industrial wall geometry and an editable metal material."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
index=json.loads((HERE/'native-state-index.json').read_text());assert len(index['all_native_states'])==256
for row in index['all_native_states']:assert sha(Path(row['private_mask']['path']))==row['private_mask']['sha256']
definition=DATA/'StreamingAssets/Base/ObjectBlueprints/Walls.xml';objects=ET.parse(definition).getroot()
chain=[objects.find(f".//object[@Name='{name}']") for name in ['RustedMetalWall','MetalWall','BaseWallMetal','Wall']]
reference=next(x for x in json.loads((DONOR/'coverage-textures.json').read_text()) if x['file']=='wall-metal.png');assert sha(DONOR/'wall-metal.png')==reference['png_sha256']
code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.ZoneManager',str(DATA/'Managed/Assembly-CSharp.dll')],capture_output=True,check=True).stdout
packet=dict(entry='SCN-RUSTEDMETALWALL',recorded_at=datetime.now(timezone.utc).isoformat(),identity='RustedMetalWall -> MetalWall -> BaseWallMetal -> Wall',
 description=chain[0].find("part[@Name='Description']").get('Short'),
 native_definition=dict(path=str(definition),sha256=sha(definition),selected_ancestry=[ET.tostring(o,encoding='unicode') for o in chain]),
 original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),
 source_correction='The inherited tile-0-13 static reference is a placeholder. Native PaintedWall=wall_metal uses256installed eight-neighbor masks, all now extracted privately. Cardinal examples are shown for the16ledger layouts.',
 installed_paint_evidence=dict(assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),class_name='XRL.World.ZoneManager',scoped_decompilation_sha256=hashlib.sha256(code).hexdigest(),
  facts=['PaintedWall appends N,NE,E,SE,S,SW,W,NW binary flags after a dash. Default Tiles prefix and .bmp extension apply.',
   'PaintWith=MetalWalls governs native joins. Material is not linked to unrelated fences/wood automatically.']),
 palette=dict(primary='r',detail='C',native_primary_rgb='a64a2e',native_detail_rgb='77bfcf',rule='Opaque source R0 is rust-metal foreground; R255 is pale-cyan edging. Transparent cells remain background, not a black fill.'),
 donor_reference=dict(package='RimWorld Core',record=reference,path=str(DONOR/'wall-metal.png'),sha256=sha(DONOR/'wall-metal.png'),
  role='Actual Wall_Atlas_Smooth supplies restrained bevel, metal shading and connected-atlas presentation only. Qud diamond pattern, lower industrial bracing, native geometry and r/C colors remain authoritative; no donor atlas order is copied.'),
 construction='Reconstruct all native coverage and color-role regions as explicit source-coordinate geometry, soften only subpixel edges and add shallow metal bevel/material within coverage. Preserve8neighbor source shapes instead of replacing them with generic masonry or a narrower four-direction extrusion.',
 material='Editable neutral sheet-metal sample with restrained diagonal welded/diamond pattern, scratches and scorch marks. One material refinement supplies surface detail; native masks retain shape and color ownership.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],anchor=[8,16],rule='Identical full-cell mapping for all256states. No state-specific alpha crop/recenter. No per-cell border caps or outline added on connected edges.'),
 views='All256native painted states plus a16cardinal recipient atlas. No creature turnarounds, clothing or arbitrary rotations apply.',
 native_behavior='Solid metal/occluding state, damage/graffiti, visibility and paintability remain native. Appearance alpha does not authorize new see-through navigation/line-of-sight behavior.',
 native_acceptance='Deferred until every conversion is generated')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
# Editable material, independent from source state topology.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 16 16"><rect width="16" height="16" fill="#b7b7b7"/>']
for v in range(-16,33,4):
 svg.append(f'<path d="M{v} 0L{v+16} 16M{v} 16L{v+16} 0" stroke="#858585" stroke-width=".1" fill="none"/>')
for x,y in [(2,3),(10,12),(13,5)]:svg.append(f'<ellipse cx="{x}" cy="{y}" rx="1.1" ry=".8" fill="#676767" opacity=".18"/>')
for x,y in [(3,11),(8,6),(11,14),(14,8)]:svg.append(f'<path d="M{x} {y}l.9 -.2m-.6 .4l.6 -.1" stroke="#e3e3e3" stroke-width=".04"/>')
svg.append('</svg>');(HERE/'constructed-material.svg').write_bytes(''.join(svg).encode());(HERE/'constructed-material.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-material.svg'),skip_system_fonts=True))
# Explicit high-resolution contour trace, recording every native run and color role.
raw=Image.open(Path(index['originals'][0]['private_mask']['path'])).convert('RGBA');paths=[]
for y in range(24):
 x=0
 while x<16:
  r,_,_,a=raw.getpixel((x,y))
  if not a:x+=1;continue
  end=x+1
  while end<16 and raw.getpixel((end,y))==raw.getpixel((x,y)):end+=1
  paths.append(f'<rect x="{x}" y="{y}" width="{end-x}" height="1" fill="{"#dadada" if r else "#929292"}"/>');x=end
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+''.join(paths)+'</svg>'
(HERE/'constructed-isolated.svg').write_bytes(svg.encode());(HERE/'constructed-isolated.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-isolated.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,765),'#142823');d=ImageDraw.Draw(plate)
d.text((20,15),'RUSTED METAL / source geometry + color roles > editable trace/material > actual Core metal atlas',font=font,fill='#e3cf43')
colors=[bytes.fromhex('a64a2e'),bytes.fromhex('77bfcf')];original=Image.new('RGBA',(16,24),'#0f3b3a')
for y in range(24):
 for x in range(16):
  r,_,_,a=raw.getpixel((x,y))
  if a:original.putpixel((x,y),(*colors[bool(r)],255))
plate.paste(original.resize((256,384),Image.Resampling.NEAREST).convert('RGB'),(30,80))
for x,name,size in [(385,'constructed-isolated.png',(256,384)),(740,'constructed-material.png',(288,288))]:
 im=Image.open(HERE/name).convert('RGBA').resize(size,Image.Resampling.LANCZOS);plate.paste(im,(x,80),im)
im=Image.open(DONOR/'wall-metal.png').convert('RGBA').resize((288,288),Image.Resampling.NEAREST);plate.paste(im,(1095,80),im)
for x,label in [(20,'Native isolated / r+C'),(365,'Explicit neutral geometry'),(720,'Manual welded metal'),(1070,'Core Wall_Atlas_Smooth')]:d.text((x,505),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['The actual source has diamond-pattern metal, pale cyan edging and lower industrial bracing, not a plain brown wall.',
 'All256native shapes retain source coverage, local color ownership and one shared anchor.16cardinal examples shown.',
 'Refinement supplies neutral metal surface only. Native topology and relative placement never depend on ImageGen.',
 'Source glyph gaps remain alpha; solid/occluding rules stay native. Unknown custom materials keep native fallback.']):d.text((20,575+34*i),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
