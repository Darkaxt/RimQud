"""Source-bound diagonal goat-wool bedroll, folded end and canvas fastening."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Bedroll','Furniture']};obj=ET.fromstring(objects['Bedroll']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/bedroll-mask.png');assert digest(source)=='47bdcea3a7f3c0c121ae3e8a9f2ac78feb0732dd29bc6d2b9e852d4539653393'
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Building/Furniture/Bed/Bedroll_south.png');about=donor.parents[5]/'About/About.xml'
packet=dict(entry='SCN-BEDROLL',identity='Bedroll -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_bedroll.bmp',canvas=[16,24],info_id=9297,atlas_id=185,rect=[864,234,16,24]),
 source_shape='Diagonal long soft body extends toward lower-left with rounded lower end. Pale folded/rolled end sits upper-right; heavier primary marks cross their join. The raw hollow outline is not a physically transparent bed.',
 palette=dict(primary='w',detail='y',native_primary_rgb='98875f',native_detail_rgb='b1c9c3',rule='Main wool bed/canvas fastening receive w; the source pale upper folded end receives y. Cyan during authoring only marks the latter region; final production layers are neutral.'),
 donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed Bedroll_south supplies wool/fabric padding, restrained seams and clean contour shading. Its pillow, straight footprint, large repaired patches and four donor facings are not copied.'),
 construction='Editable soft diagonal wool body fills the source outline, a pale upper folded/rolled end follows the detail marks, and one canvas fastening crossing the join has two short tie ends. Fold depth, seam placement and tie interpretation are authored from description and tiny source marks; no separate pillow, frame, zipper or invented occupant.',
 native_state='One fixed tile, takeable4-weight non-solid furniture with native Bed interaction. It does not inherit BaseBed/mounted solidity or the donor sleeping-bag behavior. No source occupied/packed tile switch is declared.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full-cell coordinate transform for entire oblique bedroll and detail coverage. No independent folded-end centering.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".17" stroke-linejoin="round">
<path d="M6.05 8.7L11.5 12.05L7.35 17.35Q6.6 18.65 5.15 18.55Q3.55 18.1 1.6 16.8Q.25 15.75 .55 14.35Z" fill="#c5c5c5"/>
<path d="M1.1 14.55Q.9 15.55 2.2 16.35L5 18Q6.2 18.55 7.05 17.45 M2.7 13.3L3.9 14.05 M5.2 16.1L6.2 16.55" fill="none" stroke="#929292" stroke-width=".13"/>
<path d="M6.9 7.25Q7.1 5.9 8.75 5.3Q9.45 4.95 10.55 5.65L14.6 7.8Q15.75 8.55 15.05 9.5Q13.75 10.75 11.75 11.4L6.4 8.15Z" fill="#8dd3dd"/>
<path d="M7.3 7.4Q8.65 6.8 10.2 7.4L14.6 9.65 M8.6 5.8Q10.25 5.75 12.2 7 M12.6 8.75Q14.15 8.2 14.65 9.05Q14.7 9.7 13.7 10.05" fill="none" stroke="#cdeff3" stroke-width=".14"/>
<path d="M5.85 8.65L6.8 7.85L12.4 11.05L11.55 12.3Z" fill="#929292"/>
<path d="M6.5 8.55L11.7 11.5" fill="none" stroke="#ddd" stroke-width=".12"/>
<path d="M9.05 10.45L9.4 10.9L8.7 12.05L8.25 12.25L8.9 10.65 M9.45 10.65L10.7 11.95L10.9 11.6L9.7 10.4Z" fill="#aaa"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('b1c9c3')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'GOAT-WOOL BEDROLL / original diagonal fold > canvas fastening > actual VTE cloth reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + y'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable wool/fold/ties'),(1000,Image.open(donor).convert('RGBA'),'Actual VTE bedroll / style only')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,545),label,font=font,fill='#e3cf43')
for i,line in enumerate(['The source diagonal lower body, pale upper folded end and primary fastening remain distinct.',
 'A hollow glyph is filled as soft wool, not rendered as a transparent opening. Canvas ties follow the description.',
 'No separate pillow, frame, zipper, modern repair patches or baked sleeping occupant is introduced.',
 'Neutral production layers will receive native w/y. Fixed tile and takeable non-solid sleep behavior stay native.']):draw.text((20,620+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared diagonal source bedroll, explicit folded-end ownership and installed VTE reference.')
