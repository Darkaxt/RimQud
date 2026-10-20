"""Source portable canvas seat, oblique sling and jointed wooden supports."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Canvas Folding Chair','BasePortableChair','BaseChair','Furniture']};obj=ET.fromstring(objects['Canvas Folding Chair']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/canvas-folding-chair-mask.png');assert digest(source)=='82f476c2194a86101de39efe6f1adc7458e7736f9a75f2728d4f3c26bedafca5'
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Building/Furniture/Bed/Bedroll_south.png');about=donor.parents[5]/'About/About.xml'
packet=dict(entry='SCN-CANVAS-FOLDING-CHAIR',identity='Canvas Folding Chair -> BasePortableChair -> BaseChair -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_chair_canvas.bmp',canvas=[16,24],info_id=9402,atlas_id=185,rect=[288,208,16,24]),
 source_shape='Oblique broad sling seat fills the upper diamond-like region, with thin dark source rails on upper-left and lower-right edges. Primary wooden support marks below show crossed near supports and short farther supports. No tall backrest appears.',
 palette=dict(primary='w',detail='y',native_primary_rgb='98875f',native_detail_rgb='b1c9c3',rule='Jointed wooden rails/supports receive primary w. Knit-watervine canvas seat receives detail y. Cyan seat is only an extraction aid; final layers must be neutral.'),
 donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed Bedroll_south supplies restrained fabric folds/seams, soft canvas shading and clean contour convention only. It is a cloth material reference, not a folding-chair structural equivalent. No pillow, sleeping-bag shape, patchwork or mechanics is copied.'),
 reference_limits='A focused installed filename search for folding/camp/director/deck chairs found no named close folding-frame reference. VFE school chair and Reskin Combined HD stool were inspected but not selected: rigid backrest/seat and unrelated structure do not establish this source frame. The source sprite/description control all wooden support construction.',
 construction='Editable knit-watervine sling with modest sag, two oblique seat rails, jointed crossed near wooden supports and short far supports. Exact overlap, wood joinery and under-seat attachment are authored interpretations of sparse original marks. No tall backrest, armrests, metal folding mechanism or padded cushion is added.',
 native_state='One fixed source tile in its deployed source pose. No fold/unfold part or alternate packed tile is declared. Native Chair interaction and takeable2-weight portable organic furniture remain native. BasePortableChair removes MissileCover; rare Animated builder is inherited from BaseChair and needs original fallback.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full-cell transform for entire sling/frame and masks. Support feet and seat are not separately centered or fitted.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M12.05 10.9L13.5 14.7H13.05L11.65 11.15Z M13.05 10.7L12.3 14.15L12.7 14.35L13.55 10.95Z" fill="#999"/>
<path d="M3.3 11.65L6.5 17.95V18.5H6.05L2.9 11.9Z" fill="#b8b8b8"/>
<path d="M6.65 11.8L3.35 16.85L3.05 16.6L6.1 11.5Z" fill="#8e8e8e"/>
<circle cx="4.75" cy="14.65" r=".2" fill="#d2d2d2"/>
<path d="M1.55 8.2L7.35 5.45L14.3 8.05L6.6 11.95Z" fill="#8dd3dd"/>
<path d="M2.1 8.4Q7.6 9.45 13.65 8.3 M5.8 7.45Q7.65 8.6 9.65 8.35 M5.2 10.1L6.5 10.75" fill="none" stroke="#cdeff3" stroke-width=".11"/>
<path d="M1.05 8.05L7.35 5.05L7.75 5.4L1.5 8.45Z M6.1 11.85L14.5 7.7L14.95 8.1L6.55 12.35Z" fill="#aaa"/>
<path d="M1.6 8.05L7.4 5.3 M6.65 12L14.5 8.05" fill="none" stroke="#ddd" stroke-width=".1"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('b1c9c3')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'CANVAS FOLDING CHAIR / source sling + jointed wood > editable open supports > actual VTE fabric reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + y'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable sling and support frame'),(1000,Image.open(donor).convert('RGBA'),'Actual VTE cloth / material only')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,545),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Broad oblique fabric seat and sparse crossed wood supports follow actual source positions.',
 'No tall backrest, armrests, metal mechanism or invented folded/packed view is added.',
 'The donor supplies cloth rendering only; it does not establish folding-frame geometry or gameplay.',
 'Neutral wood/seat layers receive native w/y. Portable seating and rare animated fallback stay native.']):draw.text((20,620+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared source-positioned canvas sling and crossed wooden supports with explicit reference limits.')
