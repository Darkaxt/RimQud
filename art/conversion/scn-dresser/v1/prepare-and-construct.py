"""Precisely fitted source dresser: three stacked fronts, matching native tint roles."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Dresser','Furniture']};obj=ET.fromstring(objects['Dresser']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/dresser-mask.png');assert digest(source)=='dcbb96fb536e69747a582927b5c2f7a3255e68b98c0a08a7c7918fbc64b5add3'
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Building/Furniture/Dresser_south.png');about=donor.parents[4]/'About/About.xml'
packet=dict(entry='SCN-DRESSER',identity='Dresser -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_dresser.bmp',canvas=[16,24],info_id=9557,atlas_id=185,rect=[810,156,16,24]),
 source_shape='Tall narrow case with broad shallow trapezoid cap, one upper rectangular-pull drawer and two lower fronts with opposed curved mark patterns, low support rail and two tiny outer feet. Three stacked-front interpretation follows the original glyph, not donor four-drawer layout.',
 palette=dict(primary='w',detail='w',native_primary_rgb='98875f',native_detail_rgb='98875f',rule='Case/fronts/pull marks are primary. Top cap and tiny feet are source detail. Both roles currently tint identically w; do not invent gold brass rails. Cyan cap/feet are only an extraction aid; final layers must be neutral.'),
 donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed Dresser_south supplies restrained inset-front wood shading, precise seam edges and low-relief contours. Its four2x2drawers, round knobs, broad footprint, facings and mechanics are not copied.'),
 construction='Editable three stacked closed wooden fronts, precise case/cap joinery, plain top recessed pull and opposed lower curved pull motifs matching source marks. Exact hidden drawer segmentation, curved pull construction, seams and grain remain authored interpretation. Described brass rails are inside closed drawers and do not become visible gold bands.',
 native_state='One fixed source tile,80-weight non-takeable non-solid organic container/inventory furniture with junk inventory builder, non-occlusion and rare Animated builder. No source random, open/closed or empty/full sprite is declared. Native inventory and rare/custom behavior remain native.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One complete source-cell mapping for case/fronts, cap and feet ownership. No independently centered fronts or tiny feet.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M2.15 4.8H13.85V20.7H2.15Z" fill="#888"/>
<path d="M2.2 6.15H13.8V10.7H2.2Z M2.2 12.1H13.8V15.65H2.2Z M2.2 16.05H13.8V19.6H2.2Z" fill="#bcbcbc"/>
<path d="M2.45 6.4H13.55 M2.45 12.35H13.55 M2.45 16.3H13.55" fill="none" stroke="#e1e1e1" stroke-width=".1"/>
<path d="M6.1 8.05H9.9V8.7H6.1Z" fill="#505050"/>
<path d="M4.65 13.3Q8 15.35 11.35 13.3 M4.65 13.3V13.9 M11.35 13.3V13.9 M4.65 18.45Q8 16.4 11.35 18.45 M4.65 18.45V17.85 M11.35 18.45V17.85" fill="none" stroke="#505050" stroke-width=".25"/>
<path d="M2.1 20.15H13.9V20.85H2.1Z" fill="#aaa"/>
<path d="M2.2 20.7H2.85V21.75H2.2Z M13.15 20.7H13.8V21.75H13.15Z" fill="#8dd3dd"/>
<path d="M2.05 4.35L4.05 2.25H11.95L13.95 4.35V5.05H2.05Z" fill="#8dd3dd"/>
<path d="M2.3 4.6H13.7" fill="none" stroke="#d4eff3" stroke-width=".1"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(bytes.fromhex('98875f'))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'DRESSER / original stacked fronts + shallow cap > editable precise wood > actual VTE reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + w'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable three stacked fronts'),(1000,Image.open(donor).convert('RGBA'),'Actual VTE dresser / style only')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,545),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Top recessed pull and opposed lower curved source marks remain, with precise closed wooden fronts.',
 'Top cap and tiny feet retain a separate source detail mask, even though both native roles currently use w.',
 'Internal brass rails do not imply visible gold hardware. No clothing, mirror or donor four-drawer layout is added.',
 'One full-cell frame. Actual inventory, native furniture physics and rare animated fallback remain pending.']):draw.text((20,620+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared source three-front dresser with matching native w/w roles and actual VTE reference.')
