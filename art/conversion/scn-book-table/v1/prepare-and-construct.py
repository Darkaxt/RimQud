"""Low puzzle-box book table with source side-by-side drawers and tinted top."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Book Table','Furniture']};obj=ET.fromstring(objects['Book Table']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/book-table-mask.png');assert digest(source)=='c27d3941fa5f74f559530f9672acabc4dc376fae690aea40e4db469059915764'
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Building/Furniture/EndTable_south.png');about=donor.parents[4]/'About/About.xml'
packet=dict(entry='SCN-BOOK-TABLE',identity='Book Table -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_table_low_drawers.bmp',canvas=[16,24],info_id=10120,atlas_id=185,rect=[36,416,16,24]),
 source_shape='Broad shallow trapezoidal top at y7..11, two side-by-side low rectangular drawer fronts at y13..15, low rail at y17 and short outer feet at y19. Source has no visible books, papers, stacks or separate lamp.',
 palette=dict(primary='w',detail='W',native_primary_rgb='98875f',native_detail_rgb='cfc041',rule='Drawer fronts, housing, low rail and supports use primary w. The broad tabletop including its shallow front edge uses detail W. Gold top is an extraction aid; final layers are neutral.'),
 donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed EndTable_south supplies wood-front shading, restrained drawer seams and crisp furniture contours. Its vertically stacked drawers, round knobs, footprint and donor gameplay are not copied.'),
 construction='Editable low wooden housing, two side-by-side inset drawer fronts with recessed pulls, shallow broad top and short feet. Puzzle-box joinery is suggested by precise seams, not an invented mechanism. Opaque wooden faces fill native outline glyphs. Exact joinery and dark pull cavities are authored interpretation.',
 native_state='Book Table inherits Furniture directly, not Table: no inherited EmptyTile/FullTile or alternate detail-color tags apply. One fixed source tile; native container/on inventory, non-solid80-weight non-takeable organic furniture and rare Animated builder remain native.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full-cell transform for entire table and top ownership. Preserve source cell margins; do not fit/center drawers or tabletop separately.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".15" stroke-linejoin="round">
<path d="M1.35 11.6H14.65V17.75H1.35Z" fill="#858585"/>
<path d="M1.35 17.35H14.65V18H1.35Z" fill="#bababa"/>
<path d="M1.4 17.9V19.75H1.95V17.9 M14.05 17.9V19.75H14.6V17.9" fill="#aaa"/>
<path d="M1.5 13.05H6.8V15.75H1.5Z M9.2 13.05H14.5V15.75H9.2Z" fill="#bdbdbd"/>
<path d="M1.7 13.25H6.6 M9.4 13.25H14.3" stroke="#e3e3e3" fill="none" stroke-width=".1"/>
<path d="M3.5 14.1H4.8V14.7H3.5Z M11.2 14.1H12.5V14.7H11.2Z" fill="#4b4b4b"/>
<path d="M1.2 10.25L4.15 7.1H11.85L14.8 10.25V11.6H1.2Z" fill="#cfc041"/>
<path d="M1.2 10.25H14.8 M1.5 10.6H14.5" fill="none" stroke="#ece29b" stroke-width=".11"/>
<path d="M3.2 9.1H12.8 M6.2 8.1H9.8" fill="none" stroke="#b6a538" stroke-width=".08"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('cfc041')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'BOOK TABLE / original broad top + side-by-side drawers > editable puzzle-box wood > actual VTE reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + W'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable low drawer table'),(1000,Image.open(donor).convert('RGBA'),'Actual VTE EndTable / style only')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,545),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Broad shallow top, two horizontal drawer fronts, lower rail and short supports follow the source marks.',
 'No books or papers are visible in this sprite. Real container contents are not baked onto the tabletop.',
 'Gold identifies tabletop detail ownership; final neutral wood/top layers receive actual native w/W.',
 'This inherits Furniture, not Table: no generic empty/full table artwork. Native inventory/animation stays native.']):draw.text((20,620+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared low puzzle-box table, fixed source state and installed VTE drawer reference.')
