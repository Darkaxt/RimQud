"""Two source-bound irregular galvanized multicabinet layouts, not a generic dresser."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');MOD=Path('D:/Steam/steamapps/workshop/content/294100/1718190143');REF=MOD/'Textures/NewThings/Misc/FilingCabinet/FilingCabinet_south.png';DEFS=MOD/'1.6/Defs/Buildings_Furniture/Buildings_Misc.xml'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
text=NATIVE.read_text(encoding='utf-8-sig')
def obj(name):return ET.fromstring(re.search(r'<object Name="'+re.escape(name)+r'"\s[^>]*>.*?</object>',text,re.S).group())
native,parent=obj('Argyve Multicabinet'),obj('Multicabinet');about=ET.parse(MOD/'About/About.xml').getroot();index=json.loads((HERE/'native-state-index.json').read_text());assert len(index['states'])==2
for row in index['states']:assert sha(Path(row['private_mask']['path']))==row['private_mask']['sha256']
packet=dict(entry='SCN-ARGYVE-MULTICABINET',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Argyve Multicabinet -> Multicabinet -> MountedFurniture',
 description=parent.find("part[@Name='Description']").get('Short'),native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode'),parent=ET.tostring(parent,encoding='unicode')),
 original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),
 source_shapes=['Variant1 has three small upper fronts, two middle fronts plus a partial/recessed right compartment, unequal-width lower fronts and one broad bottom drawer. Gold-role marks are upper-center, middle-left and broad bottom front.',
 'Variant2 has a small gold-role storage box with two short metal projections above the cabinet, two rows of narrow mixed-height fronts, a large lower-left door and a lower-right recess/shelf with small nested storage blocks. These ambiguous tiny marks are not evidence for a radio, robot or electronics.'],
 palette=dict(primary='c',detail='W',native_primary_rgb='40a4b9',native_detail_rgb='cfc041',rule='Neutral metal case/fronts receive native c. Source-selected fronts/trim receive W. Gold during refinement identifies detail ownership; production layers must be neutral.'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='1718190143',path=str(REF),sha256=sha(REF),definition_path=str(DEFS),definition_sha256=sha(DEFS),role='Actual installed Vanilla Furniture Expanded filing cabinet supplies restrained galvanized-metal bevels, recessed pulls and clean game-art edge weight. Its two equal drawers, facing model, research bonus and donor palette are not copied.'),
 construction='Editable cabinet bodies preserve each source layout, assorted rectangular front sizes, recesses, top storage block and short base supports. Closed metal faces are filled authored surfaces: a tiny outline glyph does not establish physically transparent drawer panels. Partial source marks are represented as recessed storage without inventing a dynamic open state.',
 states='Inherited RandomTile picks sw_multi_cabinet_1 or2. These are fixed-view cosmetic layouts, not open/closed states or rotated donor facings. No source alternate container-open tile is declared here.',
 inventory_boundary='Argyve child changes InventoryPopulationTable to Argyve Cabinet but does not change render/shape. Actual inventory remains native and is not drawn as invented visible loot.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_anchor=[8,16],rule='One full-cell coordinate mapping for each complete layout and all tint masks. No independent drawer or top-box bbox centering.'),
 native_behavior='Preserve solid200-weight metal container, occluding=true, native inventory/smart-use and source random selection. No donor research/storage mechanics are transplanted.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
def front(x,y,w,h,gold=False,vertical=False):
 color='#cfc041' if gold else '#bcbcbc';edge='#81762e' if gold else '#747474';hi='#ede39b' if gold else '#e2e2e2'
 s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx=".06" fill="{color}" stroke="#3d3d3d" stroke-width=".12"/><path d="M{x+.13} {y+h-.14}V{y+.14}H{x+w-.14}" fill="none" stroke="{hi}" stroke-width=".08"/><path d="M{x+.13} {y+h-.14}H{x+w-.14}V{y+.14}" fill="none" stroke="{edge}" stroke-width=".09"/>'
 if vertical:s+=f'<rect x="{x+w*.67}" y="{y+h*.34}" width=".22" height="{h*.3}" fill="#474747"/>'
 else:
  handle=min(1.6,w*.33);s+=f'<rect x="{x+w/2-handle/2}" y="{y+h*.43}" width="{handle}" height=".23" rx=".03" fill="#494949"/>'
 return s
def case(top):return f'''<path d="M1.15 {top+.7}H14.85V21H1.15Z" fill="#949494" stroke="#3f3f3f" stroke-width=".16"/>
<path d="M1 {top+.65}L1.9 {top}H14.1L15 {top+.65}V{top+1.05}H1Z" fill="#cbcbcb" stroke="#3f3f3f" stroke-width=".14"/>
<path d="M1 21H15V21.7H13.9V22.45H12.9V21.7H3.15V22.45H2.15V21.7H1Z" fill="#a6a6a6" stroke="#3f3f3f" stroke-width=".14"/>'''
v1=case(1.15)
for row in [(1.35,4,3.55,2.7,False),(6.2,4,3.55,2.7,True),(11.05,4,3.55,2.7,False),(1.35,8,3.55,2.7,True),(6.2,8,3.55,2.7,False),(1.35,12,5.4,2.7,False),(8.1,12,2.6,2.7,False),(12,12,2.6,2.7,False),(1.35,16.05,13.25,3.65,True)]:v1+=front(*row)
v1+='<rect x="11.1" y="8" width="3.45" height="2.7" fill="#555555" stroke="#363636" stroke-width=".08"/><path d="M14.2 8.2H14.6M14.2 10.5H14.6" stroke="#bcbcbc" stroke-width=".18"/>'
v2=case(4.15)
for i,x in enumerate([1.35,4.2,7.05,9.9,12.7]):
 v2+=front(x,7.0+(1 if i==3 else 0),1.9,2.0-(1 if i==3 else 0),False)
 v2+=front(x,10.0+(.6 if i in [1,2] else 0),1.9,1.8-(.6 if i in [1,2] else 0),True)
v2+=front(1.35,13.05,5.4,6.65,False,True)
v2+='<rect x="8.0" y="13.05" width="6.55" height="6.65" fill="#565656" stroke="#3b3b3b" stroke-width=".12"/><rect x="8.6" y="15.95" width="4.9" height=".55" fill="#bcbcbc" stroke="#444444" stroke-width=".1"/>'
v2+=front(9.4,14.0,.8,1.8,True)+front(11.3,14.9,.8,.9,True)
v2+='<path d="M10.2 19.2L11.15 18.5 12 19.2" fill="none" stroke="#a4a4a4" stroke-width=".16"/>'
v2+=front(8.25,2.1,3.5,2.6,True)
v2+='<path d="M9.3 2.1V1.15H9.7V2.1M11.2 2.1V1.15H11.6V2.1" stroke="#9d9d9d" stroke-width=".18" fill="none"/>'
for n,content in [(1,v1),(2,v2)]:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{content}</svg>';path=HERE/f'constructed-variant-{n}.svg';path.write_bytes(svg.encode());(HERE/f'constructed-variant-{n}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(path),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,790),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'ARGYVE MULTICABINET / two original irregular layouts > editable galvanized fronts > installed VFE reference',font=font,fill='#e3cf43')
source=Image.open(HERE/'native-states-comparison.png');plate.paste(source.crop((45,84,301,468)),(20,80))
for x,n in [(380,1),(730,2)]:
 im=Image.open(HERE/f'constructed-variant-{n}.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(x,80),im)
im=Image.open(REF).convert('RGBA').resize((288,288),Image.Resampling.NEAREST);plate.paste(im,(1090,105),im)
for x,label in [(20,'Native1 / c + W'),(360,'Manual1 / unequal drawers'),(710,'Manual2 / nested storage'),(1050,'VFE filing cabinet / metal style')]:draw.text((x,510),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['Both inherited RandomTile shapes are retained; the child changes inventory population rather than appearance.',
 'Assorted front sizes, recesses and top storage block follow source marks. Ambiguous glyphs do not imply electronics.',
 'Gray metal and gold-role fronts are extraction aids; neutral layers will receive actual native c/W tint.',
 'These are fixed cosmetic variants, not open/closed poses. Real inventory and source solid/occlusion stay native.']):draw.text((20,585+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
