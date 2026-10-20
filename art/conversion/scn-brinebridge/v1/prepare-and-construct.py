"""Dried-brinestalk deck interpretation with four native cosmetic accent layouts."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
index=json.loads((HERE/'native-variant-index.json').read_text());assert len(index['variants'])==4
accents={};mixes=set()
for row in index['variants']:
 p=Path(row['private_mask']['path']);assert sha(p)==row['private_mask']['sha256'];im=Image.open(p).convert('RGBA')
 accents[row['variant']]=[(1+8*c,1+6*r) for r in range(4) for c in range(2) if im.getpixel((1+8*c,1+6*r))[3]]
 mixes|={im.getpixel((x,y))[0] for y in range(24) for x in range(16) if im.getpixel((x,y))[3]}
assert mixes=={65}
native=ET.parse(NATIVE).getroot().find(".//object[@Name='BrineBridge']")
donor=next(x for x in json.loads((DONOR/'coverage-textures.json').read_text()) if x['file']=='bridge.png');assert sha(DONOR/'bridge.png')==donor['png_sha256']
packet=dict(entry='SCN-BRINEBRIDGE',recorded_at=datetime.now(timezone.utc).isoformat(),identity='BrineBridge -> Furniture',
 description=native.find("part[@Name='Description']").get('Short'),native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode')),
 originals=asset(HERE/'native-variant-index.json'),original_context=asset(HERE/'native-variants-comparison.png'),
 source_reference_correction='Static default sw_floor_brick1 from the older reference index is not the declared PickRandomTile set. Actual brickb1..4 masks are now extracted and inspected; old records remain unchanged.',
 source_interpretation='Four sparse rectangular-corner accent layouts across a two-column/four-row field. They are abstract floor glyphs, not proof of stone masonry or missing traversable bridge panels. Dried brinestalk material comes from the description.',
 native_accent_positions=accents,
 native_color_contract=dict(primary='w',detail='W',opaque_red_value=65,mix=65/255,
  explanation='All opaque actual bridge-source pixels have R65, with green RGB channels irrelevant under the audited Kobold formula. Preserve the native foreground/detail mix, not a binary black/white interpretation or baked literal green.'),
 donor_reference=dict(**donor,role='Actual extracted Core WoodFloor, aliased bridge.png in the earlier probe, supplies overhead dried-fiber/board grain and subtle surface shading. It is not a one-to-one brinestalk bridge object or proof of donor bridge mechanics.'),
 construction='Author a low dried-stalk deck from eight short three-slat bundles at the native rectangular panel anchors; preserve a sparse open-joint character and four cosmetic accent arrangements. No stone arches, invented railings, piles, nails or changed fluid support.',
 accent_policy='All four variants share the same physical deck coverage. Native missing corner accents change surface markings, not collision holes. Use the original L accent positions for light worn edge details.',
 native_behaviors='Non-solid organic Bridge=1 and SuspendedPlatform; non-occluding. Crossing/support and liquid remain native. Preserve water under the bridge and independent foreground above it.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],panel_origins=[[1+8*c,1+6*r] for r in range(4) for c in range(2)],panel_extent=[6,4],
  interpretation='Explicit dried-stalk surface interpretation of sparse native corner glyphs; fixed source coordinate frame for all variants, no independent per-variant fit.'),
 states='Fixed overhead view plus the actual four cosmetic source selectors. No character turnaround or clothing. Water underlay and walking/state acceptance remain final integration work.',
 native_acceptance='Deferred until every conversion is generation-ready')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
defs='<defs><linearGradient id="fiber" x2="0" y2="1"><stop stop-color="#636363"/><stop offset=".25" stop-color="#d0d0d0"/><stop offset=".55" stop-color="#b6b6b6"/><stop offset="1" stop-color="#6b6b6b"/></linearGradient></defs>'
def mat():
 out=[]
 for j in range(3):
  y=j*1.32+.08
  out.append(f'<path d="M.12 {y+.08}Q2 {y-.04} 3 {y+.04}T5.87 {y+.08}L5.96 {y+1.12}Q4 {y+1.25} 2.8 {y+1.17}T.08 {y+1.14}Z" fill="url(#fiber)" stroke="#414141" stroke-width=".08"/>')
  out.append(f'<path d="M.3 {y+.38}Q2 {y+.24} 3.4 {y+.36}T5.7 {y+.34} M.4 {y+.65}Q2.4 {y+.57} 3.3 {y+.69}T5.5 {y+.68}" fill="none" stroke="#dedede" stroke-width=".045"/>')
 return ''.join(out)
single='<svg xmlns="http://www.w3.org/2000/svg" width="768" height="512" viewBox="0 0 6 4">'+defs+mat()+'</svg>'
(HERE/'constructed-mat.svg').write_bytes(single.encode());(HERE/'constructed-mat.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-mat.svg'),skip_system_fonts=True))
deck='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+defs+''.join(f'<g transform="translate({x} {y})">{mat()}</g>' for x,y in packet['frame']['panel_origins'])+'</svg>'
(HERE/'constructed-deck.svg').write_bytes(deck.encode());(HERE/'constructed-deck.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-deck.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,820),'#142823');d=ImageDraw.Draw(plate)
d.text((20,16),'BRINEBRIDGE / actual four source variants > dried-stalk deck construction > actual Core WoodFloor grain',font=font,fill='#e3cf43')
src=Image.open(HERE/'native-variants-comparison.png').crop((45,84,301,468));plate.paste(src,(24,90))
deck=Image.open(HERE/'constructed-deck.png').convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);plate.paste(deck,(427,90),deck)
don=Image.open(DONOR/'bridge.png').convert('RGB').resize((352,352),Image.Resampling.LANCZOS);plate.paste(don,(800,100))
sample=Image.open(HERE/'constructed-mat.png').convert('RGBA').resize((240,160),Image.Resampling.LANCZOS);plate.paste(sample,(1180,200),sample)
for x,t in [(20,'Actual brickb1 /16x24'),(387,'Manual dried-stalk deck'),(760,'Actual Core WoodFloor / grain only'),(1170,'Shared three-slat mat')]:d.text((x,510),t,font=font,fill='#e5e8d8')
for i,t in enumerate(['Description supplies dried brinestalk identity; sparse L glyphs do not establish masonry or missing physical panels.',
 'Source uses one constant foreground/detail mix: R65/255 between native w and W. Literal raw green is not the output color.',
 'All four native cosmetic variants retain their actual corner-accent locations in the shared fixed frame.',
 'Keep liquid under the bridge and independent foreground above it. No invented railings, supports or new crossing rules.']):d.text((20,575+i*34),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
