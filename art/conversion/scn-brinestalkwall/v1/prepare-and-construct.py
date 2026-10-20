"""Brinestalk wall: stripped trunks and mud, with a documented mod reference."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2608762624')
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Walls.xml')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
ref=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x.get('blueprint')=='BrinestalkWall')
assert sha(DONOR/ref['reference_file'])==ref['reference_sha256']
raw_path=DONOR/'village-originals/brinestalkwall-mask.png';assert sha(raw_path)==ref['native_mask_sha256']
tree=ET.parse(NATIVE).getroot();native=tree.find(".//object[@Name='BrinestalkWall']")
about=ET.parse(MOD/'About/About.xml').getroot();defs=MOD/'1.6/Defs/ThingDefs_Buildings/Buildings_Structure.xml'
moddef=next(x for x in ET.parse(defs).getroot().findall('ThingDef') if x.findtext('defName')=='VFEArch_LogWall')
packet=dict(entry='SCN-BRINESTALKWALL',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='BrinestalkWall -> BaseWallWood -> Wall',description=ref['description'],original=ref,
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode')),
 source_shape='Default isolated wall glyph has a mud/lattice-like upper panel and four narrow upright support/stalk columns below. Fine stipple interpretation is uncertain; the description explicitly establishes stripped brinestalk trunks bonded with mud.',
 source_palette=dict(primary='w',primary_hex=palette['w'],detail='y',detail_hex=palette['y'],
  field_background='Source-owned native background; ColorString includes ^y but visible voids follow actual native appearance/ownership rather than an invented global fill.',
  mask_roles='Original182opaque primary pixels and43opaque detail pixels. Black RGB means primary coverage; white means detail. Transparent pixels are not opaque black.'),
 donor_reference=dict(mod_name=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2608762624',
  atlas=dict(path=str(MOD/'Textures/LogWall/LogWall_Atlas.png'),sha256=sha(MOD/'Textures/LogWall/LogWall_Atlas.png')),
  icon=dict(path=str(MOD/'Textures/LogWall/LogWall_MenuIcon.png'),sha256=sha(MOD/'Textures/LogWall/LogWall_MenuIcon.png')),
  definition=dict(path=str(defs),sha256=sha(defs),selected=ET.tostring(moddef.find('graphicData'),encoding='unicode')),
  version_mapping='Installed LoadFolders maps1.7 to root plus1.6; the recorded1.6 definition uses Graphic_Single and CornerFiller.',
  role='Actual installed Vanilla Furniture Expanded - Architect log wall supplies readable 2.5D wall faces/caps, outlines and linked joins. Its horizontal logs, brown hue and CornerFiller atlas ordering are not copied into Qud.'),
 construction='Four stripped vertical stalks bonded by packed mud, with low-relief fibrous grain and light weathered ridges. No brick courses, cut planks, nails, leaves or rope are invented. Author a neutral face material, deterministic raised caps/faces and independent native w/y tint regions.',
 state_contract='The recipient adapter currently selects16N/E/S/W atlas masks, bits1/2/4/8, with a4x4bottom-origin layout. These are recipient states, not a claim that native eight-neighbor PaintedWall atlas bytes were all exported. Do not reuse the mod atlas order.',
 geometry_contract='Connected footprint and fixed-height raised top/visible south faces in one square cell frame. Build3x3neighbor context before extrusion/cropping to avoid per-cell caps/outlines across connected edges. No per-mask independent fitting.',
 native_behaviors='Native solid/organic/occluding wall, damage, visibility, exploration and rare graffiti/animation stay native. This authoring pass does not alter collision, hitpoints, roof mechanics or unknown visual states.',
 native_acceptance='Deferred until every conversion is generation-ready')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><defs>
<linearGradient id="stalk"><stop stop-color="#444444"/><stop offset=".2" stop-color="#aaaaaa"/><stop offset=".45" stop-color="#dddddd"/><stop offset=".8" stop-color="#a6a6a6"/><stop offset="1" stop-color="#505050"/></linearGradient>
<pattern id="mud" width="34" height="38" patternUnits="userSpaceOnUse"><rect width="34" height="38" fill="#888888"/><path d="M4 6l3 1 M23 14l2 -1 M11 28l4 1" stroke="#b0b0b0" stroke-width="1.2"/><path d="M7 17l2 -2 M28 31l3 1" stroke="#5a5a5a" stroke-width="1"/></pattern>
</defs><rect width="512" height="512" fill="url(#mud)"/>
<g fill="url(#stalk)" stroke="#424242" stroke-width="3">
<path d="M14 0H105L109 124 104 252 107 379 102 512H16L13 386 18 251 12 126Z"/>
<path d="M143 0H231L234 126 229 251 233 383 230 512H140L144 380 139 253 145 127Z"/>
<path d="M270 0H359L355 128 360 254 354 382 358 512H269L274 384 267 256 273 127Z"/>
<path d="M398 0H486L489 125 483 252 490 381 485 512H398L395 384 402 255 397 127Z"/></g>
<g stroke="#eeeeee" stroke-width="1.5" opacity=".55" fill="none"><path d="M45 0Q40 96 44 170T45 350T44 512 M174 0Q170 100 176 179T174 360T175 512 M301 0Q306 110 301 191T302 380T300 512 M429 0Q424 120 430 202T428 400T430 512"/></g>
<g stroke="#666666" stroke-width="3" fill="none"><path d="M15 126Q59 136 107 124 M142 251Q187 260 232 252 M270 383Q316 392 357 381 M397 125Q445 133 487 124"/></g></svg>'''
(HERE/'constructed-face.svg').write_bytes(svg.encode());(HERE/'constructed-face.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-face.svg'),skip_system_fonts=True))
g=ImageOps.grayscale(Image.open(HERE/'constructed-face.png'));lo=bytes.fromhex(palette['w']);hi=bytes.fromhex(palette['y'])
colored=Image.merge('RGB',tuple(g.point(lambda v,l=l,h=h:round((l*.42+(h-l*.42)*(v/255)))) for l,h in zip(lo,hi)));colored.save(HERE/'constructed-qud-preview.png')
raw=Image.open(raw_path).convert('RGBA');native_preview=Image.new('RGBA',raw.size,'#'+palette['k'])
for y in range(raw.height):
 for x in range(raw.width):
  rr,_,_,aa=raw.getpixel((x,y));mix=rr/255
  if aa:native_preview.putpixel((x,y),(*[round(a*(1-mix)+b*mix) for a,b in zip(lo,hi)],aa))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');d=ImageDraw.Draw(plate)
d.text((22,16),'BRINESTALK WALL / stripped upright trunks + mud / installed Architect log-wall reference',font=font,fill='#e3cf43')
plate.paste(native_preview.resize((224,336),Image.Resampling.NEAREST).convert('RGB'),(35,90))
mod=Image.open(MOD/'Textures/LogWall/LogWall_Atlas.png').convert('RGBA').resize((320,320),Image.Resampling.NEAREST);plate.paste(mod,(360,105),mod)
plate.paste(colored.resize((320,320),Image.Resampling.LANCZOS),(755,105));plate.paste(g.resize((256,320),Image.Resampling.LANCZOS).convert('RGB'),(1150,105))
for x,t in [(22,'Original isolated16x24glyph'),(353,'Actual VFE Architect atlas'),(745,'Manual four stalks + mud'),(1140,'Neutral face construction')]:d.text((x,478),t,font=font,fill='#e5e8d8')
for i,t in enumerate(['Description, not donor material, defines the object: stripped brinestalk trunks bonded with mud.',
 'Qud primary w #98875F and detail y #B1C9C3. The reference horizontal log orientation is not adopted.',
 'Neutral surface refinement does not decide topology:16connected states are built from explicit geometry.',
 'Fixed cell/frame and raised-face height. Connected joins must not gain a cap or dark outline at every tile edge.']):d.text((22,555+i*34),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
