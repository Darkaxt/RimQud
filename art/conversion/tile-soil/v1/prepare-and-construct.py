"""Author packed-earth coverage from the native sparse DirtFloor and donor grain."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, random, math, xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont, ImageOps
import resvg_py

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
reference=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x.get('blueprint')=='DirtFloor')
assert sha(DONOR/reference['reference_file'])==reference['reference_sha256']
mask_path=DONOR/'village-originals/dirtfloor-mask.png'
assert sha(mask_path)==reference['native_mask_sha256']
mask=Image.open(mask_path).convert('RGBA')
covered=[dict(x=x,y=y,role='primary' if mask.getpixel((x,y))[0]==0 else 'detail') for y in range(24) for x in range(16) if mask.getpixel((x,y))[3]]
tree=ET.parse(NATIVE).getroot()
definitions={n:ET.tostring(tree.find(f".//object[@Name='{n}']"),encoding='unicode') for n in ['Floor','DirtFloor','DirtPath']}
donor=next(x for x in json.loads((DONOR/'package.json').read_text())['textures'] if x['file']=='soil.png')
packet=dict(entry='TILE-SOIL',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='DirtFloor -> Floor -> CosmeticObject, packed dirt floor; soil.png is an adapter resource slot, not a replacement for every interior/terrain type',
 description='No native Description.Short on this floor. Render.DisplayName is packed dirt floor. Cosmetic non-solid terrain; no creature anatomy, clothing or movement animation applies.',
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected_definitions=definitions),
 original=reference,native_coverage=covered,
 source_color_roles=dict(primary='w',detail='w',brown_hex=palette['w'],field_background='k',background_hex=palette['k'],
  explanation='The mask has six primary and two detail points; both use native brown w. All other pixels retain native field background. The reference image includes its extraction preview background; it is not the actual shader background.'),
 native_selectors=['Terrain/sw_ground_dots1.png','Terrain/sw_ground_dots2.png','Terrain/sw_ground_dots3.png','Terrain/sw_ground_dots4.png'],
 selector_limit='Only dots1 was exported as an exact original mask. The four selectors are declared native aliases, not four independently observed or reconstructed masks. The authored continuous packed-earth material can serve those aliases without claiming their unexported point layouts.',
 donor_reference=dict(**donor,png_sha256=sha(DONOR/'soil.png'),package_sha256=sha(DONOR/'package.json'),
  role='Actual extracted RimWorld Soil supplies fine irregular packed-earth grain and scale only. Do not copy its broad solid brown fill, color, mechanics or per-cell material repetition.'),
 construction='Editable periodic neutral coverage: quiet fine compressed earth, sparse grit and shallow scuffs. Retain broad native dark-teal negative space and native-brown deposits. No cobblestones, regular slabs, sand dunes, plants or water.',
 material_contract='Independent neutral RGB + opacity; native primary tint w over the source-owned background k. Do not bake the preview colors into production. Where another object owns the visible cell, respect native visibility/layer ownership.',
 required_states='Seamless world-continuous coverage and eight-neighbor transition shapes. These masks use actual bare-soil eligibility, not path occupancy. No liquid depth or humanoid views apply.',
 distinction='DirtPath inherits DirtFloor, but its user-directed cobble interpretation is separate. This entry is fine bare soil/interior ground and must not replace all visible floors with paving.',
 registration='World-anchored repeat independent of cell crop. No body/contact pivot. Preserve Qud rectangular display-cell proportions in comparison views.',
 adapter_evidence=asset(ROOT/'art/conversion/tile-grassy-ground/v1/adapter-source/JoppaRenderer.cs'),
 binding_pending='Existing broad adapter selection uses Color.white and quad-local UV. The new neutral coverage, native background/foreground tint and precise source eligibility need final integration after every entry is generated.',
 native_acceptance='Deferred until all conversions are generation-ready')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())

rng=random.Random(20518);side=512
shapes=['<rect width="512" height="512" fill="#070707"/>'];defs=[]
for i in range(24):
 x,y=rng.uniform(0,side),rng.uniform(0,side);rx,ry=rng.uniform(20,65),rng.uniform(15,45)
 defs.append(f'<radialGradient id="m{i}"><stop stop-color="#555555" stop-opacity=".18"/><stop offset="1" stop-color="#555555" stop-opacity="0"/></radialGradient>')
 for dx in [-side,0,side]:
  for dy in [-side,0,side]:
   shapes.append(f'<ellipse cx="{x+dx:.2f}" cy="{y+dy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="url(#m{i})"/>')
for i in range(520):
 x,y=rng.uniform(0,side),rng.uniform(0,side);rx,ry=rng.uniform(.3,1.7),rng.uniform(.3,1.3);tone=rng.randint(40,205)
 for dx in [-side,0,side]:
  for dy in [-side,0,side]:
   if x+dx+rx<0 or x+dx-rx>side or y+dy+ry<0 or y+dy-ry>side:continue
   shapes.append(f'<ellipse cx="{x+dx:.2f}" cy="{y+dy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="rgb({tone},{tone},{tone})"/>')
for i in range(46):
 x,y=rng.uniform(8,side-8),rng.uniform(8,side-8);length=rng.uniform(2,7);angle=rng.uniform(0,2*math.pi)
 shapes.append(f'<path d="M{x:.2f} {y:.2f} q{math.cos(angle)*length/2:.2f} {math.sin(angle)*length/2-1:.2f} {math.cos(angle)*length:.2f} {math.sin(angle)*length:.2f}" stroke="#777777" stroke-opacity=".22" stroke-width=".5" fill="none"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><defs>'+''.join(defs)+'</defs>'+''.join(shapes)+'</svg>'
(HERE/'constructed-coverage.svg').write_bytes(svg.encode())
(HERE/'constructed-coverage.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-coverage.svg'),skip_system_fonts=True))
coverage=ImageOps.grayscale(Image.open(HERE/'constructed-coverage.png'))
layer=Image.new('RGBA',coverage.size,'#'+palette['w']);layer.putalpha(coverage)
preview=Image.new('RGBA',coverage.size,'#'+palette['k']);preview.alpha_composite(layer);preview.save(HERE/'constructed-qud-preview.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1440,785),'#142823');d=ImageDraw.Draw(plate)
d.text((24,18),'BARE SOIL / native sparse DirtFloor > editable grit coverage > actual donor grain',font=font,fill='#e3cf43')
# Show the exact native mask in the correct primary/detail/background colors.
orig=Image.new('RGBA',(16,24),'#'+palette['k'])
for p in covered:orig.putpixel((p['x'],p['y']),(*bytes.fromhex(palette['w']),255))
plate.paste(orig.resize((208,312),Image.Resampling.NEAREST).convert('RGB'),(68,96))
ref=Image.open(DONOR/'soil.png').convert('RGB').resize((320,320),Image.Resampling.LANCZOS);plate.paste(ref,(406,92))
plate.paste(preview.resize((320,320),Image.Resampling.LANCZOS).convert('RGB'),(790,92))
plate.paste(coverage.resize((240,240),Image.Resampling.LANCZOS).convert('RGB'),(1160,130))
for x,t in [(28,'Original 16 x 24 / k + w'),(400,'Actual RimWorld Soil / grain only'),(786,'Manual / sparse native-brown grit'),(1150,'Editable neutral coverage')]:d.text((x,450),t,font=font,fill='#e5e8d8')
for i,t in enumerate(['Six primary + two detail points; both tint w #98875F. The native field background remains k #0F3B3A.',
 'Fine earth is an authored material interpretation. Do not replace the field with a solid brown carpet.',
 'Keep bare soil distinct from cobbled paths, vegetation, water and other native floor materials.',
 'No creature views or equipment apply. Repetition/boundary states and final source-aware binding remain required.']):d.text((24,530+i*34),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
