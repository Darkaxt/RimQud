"""Marsh-dweller plank chair with source tall slatted back and angled hard seat."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Chair','BaseChair','Furniture']};obj=ET.fromstring(objects['Chair']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/chair-mask.png');assert digest(source)=='98bc3882c4b2387cfb3f0bd3c431fc344cd61b424eb6a20197a66e61929bd1f2'
donor=Path('D:/Steam/steamapps/workshop/content/294100/1718190143/Textures/Things/Seating/SquareChair/Chair_south.png');about=donor.parents[4]/'About/About.xml'
packet=dict(entry='SCN-CHAIR',identity='Chair -> BaseChair -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_chair.bmp',canvas=[16,24],info_id=9399,atlas_id=185,rect=[342,208,16,24]),
 source_shape='Tall upper-left rectangular slatted back, right-angle plank joints and hard seat angled down-right. Three source-visible support extents remain: long front-left, front-right and shorter rear-left; rear-right structure is occluded by the seat. Source back/seat proportions, gaps and footprint are authoritative.',
 palette=dict(primary='w',detail='y',native_primary_rgb='98875f',native_detail_rgb='b1c9c3',rule='Back/rails/supports receive primary w; the hard wooden seat surface receives detail y. This is a color role, not evidence that the seat is cloth. Cyan seat is only an extraction aid; final layers are neutral.'),
 donor_reference=dict(mod='Vanilla Furniture Expanded',workshop_id='1718190143',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed legacy Things/Seating/SquareChair sprite supplies clean straight-frame contours and restrained bevel shading. It is retained installed reference art, not claimed as the active current VFE definition. Its smooth/padded seat, unslatted rectangular back, donor footprint/facings and gameplay are not copied.'),
 rejected_reference_note='VTE DiningChair_south and the previously extracted Core chair were viewed but their round backs/soft seats do not match the source plank structure; neither is selected for this refinement.',
 construction='Editable nailed-plank chair has tall open back with two inner bars, plain upper/lower back rails, hard oblique plank seat and source-positioned straight supports. All support tops extend beneath seat coverage. Exact grain, seams, nail placement and hidden rear-right attachment remain authored interpretation; no upholstered cushion, curved back, canvas sling or armrests.',
 native_state='One fixed native chair tile. BaseChair supplies native Chair interaction,20-weight non-takeable organic furniture, MissileCover10, non-occlusion and rare Animated builder. No source facing selector or occupied tile is declared; rare animated/custom shapes require original fallback.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One complete source-cell mapping for back, hard seat, supports and masks. No independent seat/back/foot bbox centering.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M3.05 3.15H3.6V17.75H3.05Z M8.85 3.15H9.4V13.25H8.85Z" fill="#a9a9a9"/>
<path d="M3.35 4.15H9.15V4.85H3.35Z M3.35 7.05H9.15V7.75H3.35Z" fill="#bcbcbc"/>
<path d="M5.05 4.75H5.5V7.2H5.05Z M7.05 4.75H7.5V7.2H7.05Z" fill="#989898"/>
<path d="M5.15 13.8H5.75V21.35H5.15Z M12.95 13.9H13.55V20.55H12.95Z" fill="#aaa"/>
<path d="M3.4 11.4L5.1 15.65H13.8V14.8H5.65L3.95 11.25Z" fill="#828282"/>
<path d="M3.65 11.15H9.35L13.6 14.8H5.4Z" fill="#8dd3dd"/>
<path d="M4.25 12.35H10.75 M4.85 13.65H12.25" fill="none" stroke="#6ab4bf" stroke-width=".1"/>
<path d="M3.8 11.35H9.2 M5.55 14.6H13.25" fill="none" stroke="#d5f0f3" stroke-width=".1"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('b1c9c3')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'PLANK CHAIR / source tall slatted back + hard oblique seat > editable wood > installed VFE reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + y'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable hard plank chair'),(1000,Image.open(donor).convert('RGBA'),'Installed VFE SquareChair / style')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,545),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Straight nailed planks, tall slatted back and hard angled seat follow actual source construction.',
 'Native y seat tint does not imply canvas or upholstery: every visible structural surface is wood.',
 'Preserve back gaps, support extents and source footprint. No padded seat, rounded back or donor rotations.',
 'Neutral back/frame and seat layers receive native w/y. Seating, cover and rare animation stay native.']):draw.text((20,620+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared source tall-back hard-seat plank chair with installed VFE contour reference.')
