"""Four source cushion patterns: tufting/creases are not faces or physical holes."""
from pathlib import Path
import hashlib,json,re
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p))
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Floor Cushion','BaseChair','Furniture']};obj=ET.fromstring(objects['Floor Cushion']);description=obj.find("part[@Name='Description']").get('Short')
states=json.loads((HERE/'native-state-index.json').read_text())['states'];assert len(states)==4
for state in states:assert digest(Path(state['private_mask']['path']))==state['private_mask']['sha256']
default=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/floor-cushion-mask.png');assert digest(default)=='32a6bd94b619acf6aae8befb08baa9d346abd5a1074d562de8457d767912eb1f'
d=Image.open(default).convert('RGBA');v1=Image.open(states[0]['private_mask']['path']).convert('RGBA')
assert d.getchannel('A').tobytes()==v1.getchannel('A').tobytes()
assert all(not a or (r,a)==(rr,aa) for (r,g,b,a),(rr,gg,bb,aa) in zip(d.get_flattened_data(),v1.get_flattened_data()))
donor=Path('D:/Steam/steamapps/workshop/content/294100/1718190143/Textures/NewThings/Furniture/SittingCushion/SittingCushion.png');about=donor.parents[4]/'About/About.xml'
patterns=['Two upper dimples and central star-like folds, following the first native pattern. These are pillow tufts, not a face.',
 'Four source dimple positions at top, left, right and lower center; retain the diamond arrangement.',
 'Plain upper pad with deeper lower-front edge folds; no new visible top buttons are added where the source has none.',
 'A diagonal sequence of pinched folds/dimples follows the original stepped diagonal marks; no readable slash symbol or embroidery.']
packet=dict(entry='SCN-FLOOR-CUSHION',identity='Floor Cushion -> BaseChair -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),
 default_reference=dict(path=str(default),sha256=digest(default),tile='Items/sw_floor_cushion.png',binding='Same alpha coverage and same shader-relevant R wherever covered as RandomTile variant1. Raw RGBA differs only in invisible RGB; no extra visible fifth model is required.'),
 source_shapes=patterns,palette=dict(primary='w',detail='y',native_primary_rgb='98875f',native_detail_rgb='b1c9c3',rule='Upper stuffed fabric receives w; pale lower/front binding receives y. Crease/button marks are shaded primary fabric, not transparent holes. Cyan binding in authoring is an extraction aid; final layers are neutral.'),
 donor_reference=dict(mod='Vanilla Furniture Expanded',workshop_id='1718190143',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed NewThings/Furniture/SittingCushion supplies soft tufting, restrained fabric folds and clean outlined cushion rendering. Its exact four-corner fold layout, square footprint, source colors and seating mechanics are not copied.'),
 construction='Four editable low oblique diamond-like stuffed pads retain native pattern differences and pale lower/front binding. Native gaps are interpreted as creases/button indents in opaque fabric, not a face or holes through a stuffed pillow. Exact tuft circles, fold depths and cloth seams are authored interpretation. Chaff/feathers are stuffing, not loose objects or luminous glowcrow effects.',
 native_state='RandomTile chooses sw_cushion1..4.bmp, not four facings. Default thumbnail is visibly equivalent to variant1 under actual shader coverage. Native Chair Level-1,2-weight BaseChair-derived furniture, inherited takeability/cover and rare Animated state stay native. Do not infer portability merely from low weight.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='Same full source-cell transform for every pad/binding mask. Do not separately fit/center different tuft patterns or pale edge.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
body='''<path d="M7.95 8.15Q9.2 8.05 11.6 9.6L14.6 11.25Q15.6 12.15 14.6 13.25L9.45 16.25Q8 17.15 6.4 16.2L1.4 13.2Q.4 12.2 1.4 11.25L5.2 8.9Q6.8 8.05 7.95 8.15Z" fill="#bcbcbc"/>
<path d="M1.25 12.85Q7.7 16.35 8 16.2Q8.3 16.35 14.75 12.85L14.6 13.5Q8.35 17.1 8 16.9Q7.65 17.1 1.4 13.5Z" fill="#8dd3dd"/>'''
def dimple(x,y):return f'<ellipse cx="{x}" cy="{y}" rx=".2" ry=".13" fill="#686868"/><path d="M{x-.5} {y-.3}L{x-.15} {y-.05} M{x+.15} {y+.05}L{x+.5} {y+.3}" fill="none" stroke="#969696" stroke-width=".1"/>'
tufts=[dimple(5.5,10.5)+dimple(9.5,10.5)+dimple(7.6,12.1)+'<path d="M5.4 13.35L7.6 12.1L9.9 13.35 M6.8 11.3L7.6 12.1L8.5 11.25" fill="none" stroke="#858585" stroke-width=".12"/>',
 ''.join(dimple(x,y) for x,y in [(7.7,9.65),(3.6,11.55),(11.8,11.55),(7.7,13.55)]),
 '<path d="M2.5 13Q4.1 12.95 5.15 14.65 M10.8 14.65Q12 12.95 13.5 13 M6.8 15.7Q8 15.3 9.2 15.7" fill="none" stroke="#858585" stroke-width=".15"/>',
 ''.join(dimple(x,y) for x,y in [(4.9,10.35),(7.7,11.55),(10.5,12.8)])+'<path d="M5.1 10.4L7.5 11.5 M7.9 11.65L10.3 12.75" fill="none" stroke="#8b8b8b" stroke-width=".11"/>']
for n,tuft in enumerate(tufts,1):
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g stroke="#303030" stroke-width=".13" stroke-linejoin="round">'+body+tuft+'</g></svg>'
 (HERE/f'constructed-variant-{n}.svg').write_bytes(svg.encode());(HERE/f'constructed-variant-{n}.png').write_bytes(svg_to_bytes(svg_string=svg))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1210),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'FLOOR CUSHION / four actual native patterns > editable stuffed cloth + lower binding > actual VFE reference',font=font,fill='#e3cf43')
for n,state in enumerate(states,1):
 mask=Image.open(state['private_mask']['path']).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('b1c9c3')))+(a,) for r,g,b,a in mask.get_flattened_data()])
 for y,im,label in [(65,native,'Actual native'),(430,Image.open(HERE/f'constructed-variant-{n}.png').convert('RGBA'),'Editable pattern')]:
  big=im.resize((208,312),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);x=50+(n-1)*360;plate.paste(big,(x,y),big);draw.text((x,y+318),f'{label} {n}',font=font,fill='#e3cf43')
im=Image.open(donor).convert('RGBA');im.thumbnail((200,200));plate.paste(im,(1120,860),im);draw.text((1010,1080),'Actual VFE SittingCushion',font=font,fill='#e3cf43')
for i,line in enumerate(['Four cosmetic tuft/crease variants, not four rotations; default thumbnail binds to visible-equivalent variant1.',
 'Creases are opaque padded fabric. The first pattern is not a face; the third does not gain invented upper buttons.',
 'Native w fabric + y front binding. Chaff/feather stuffing does not imply luminous effects or loose feathers.',
 'One shared source-cell frame. Native seating/cover/physics and rare animated fallback remain pending.']):draw.text((20,880+i*34),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared all four exact native cushion patterns, default binding and editable opaque fabric/edge geometry.')
