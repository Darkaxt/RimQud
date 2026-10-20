"""Source-bound hillfolk bed: oblique wooden slats and chaff-stuffed fabric."""
from pathlib import Path
import hashlib,json,re,subprocess
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p))
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Bed','BaseBed','MountedFurniture','Furniture']}
bed=ET.fromstring(objects['Bed']);description=bed.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/bed-mask.png');assert digest(source)=='7a697abb6c2ab7bd54b8b97d655c45dc332382a58fb3e2fa19ee04c0ae1b1e12'
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Building/Furniture/Bed/Bed_south.png')
about=donor.parents[5]/'About/About.xml'
assembly=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed/Assembly-CSharp.dll')
code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.Bed',str(assembly)],capture_output=True,check=True).stdout
packet=dict(entry='SCN-BED',identity='Bed -> BaseBed -> MountedFurniture -> Furniture',description=description,
 native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_bed.bmp',canvas=[16,24],info_id=9291,atlas_id=185,rect=[972,234,16,24]),
 source_shape='The installed sprite is oblique: headboard at upper-right, sleeping surface descends toward lower-left, broad foot rail and short feet. Upper open wooden bars remain visible. This source perspective is retained instead of substituting the donor straight top-down footprint.',
 palette=dict(primary='w',detail='Y',native_primary_rgb='98875f',native_detail_rgb='ffffff',rule='Wood/slats/frame receive primary w; stuffed-fabric sleeping surface receives Y. Pale cyan fabric in the construction/refinement is only an extraction aid; both final layers must be neutral.'),
 donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed Bed_south supplies restrained fabric folds, padded edge shading, wooden-frame readability and outline weight. Its pillow, blanket subdivision, straight orientation, four facings, bed dimensions and sleeping mechanics are not copied.'),
 construction='Editable oblique slatted wood frame, open headboard, broad low foot rail, short supports and one softly stuffed fabric pad. Fabric is chaff-stuffed, not a modern spring mattress. Exact hidden slat spacing and seams are authored interpretation; no pillow or additional blanket absent from source is invented.',
 native_state=dict(tile='One fixed Items/sw_bed.bmp; no RandomTile or alternate occupied tile is declared by Bed/BaseBed.',part='XRL.World.Parts.Bed',assembly_sha256=digest(assembly),decompiled_stdout_sha256=hashlib.sha256(code).hexdigest(),part_declares_Render_or_Tile=bool(re.search(rb'\b(Render|Tile)\b',code)),rule='Native sleeping/occupant state stays native; no donor occupancy sprite or independent furniture rotation is invented. Rare Animated builder needs original fallback at final integration.'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full-cell mapping for wood/fabric coverage, including oblique overhangs. Do not independently center mattress or wooden alpha bounds.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
wood='''<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M6.35 2.25V8.2 M14.25 2.25V12.8" fill="none" stroke="#adadad" stroke-width=".48"/>
<path d="M6.4 3.1 Q7 4.25 8.3 2.9 Q9.4 4.1 10.35 2.9 Q11.4 4.15 12.45 2.9 Q13.5 4.2 14.2 3.05 M6.4 5.65H14.2" fill="none" stroke="#c2c2c2" stroke-width=".42"/>
<path d="M9.1 3.35V5.65 M11.35 3.35V5.65" fill="none" stroke="#999" stroke-width=".3"/>
<path d="M6.25 6.65H14.25L10.5 18.9H1.2Z" fill="#888"/>
<path d="M5.6 8.2H13.65 M4.9 10.1H13 M4.1 12.3H12.35 M3.3 14.4H11.65 M2.6 16.55H10.95" fill="none" stroke="#bcbcbc" stroke-width=".46"/>
<path d="M1.25 18.35L6.2 6.7H6.55L1.8 18.75Z M13.85 6.85H14.25L10.5 19H9.8Z" fill="#b8b8b8"/>
<path d="M1.35 18.4H10.25V19.65H1.35Z" fill="#bcbcbc"/>
<path d="M1.45 19.55V20.75H1.85V19.55 M9.85 19.6V21.4H10.25V19.6" fill="#999"/>
</g>'''
fabric='''<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M6.3 7.1Q9.8 6.8 13.65 7.1L9.75 18.25Q5.4 18.6 1.55 18.15L1.5 17.8L5.9 7.6Z" fill="#8fd0da"/>
<path d="M6.3 7.1Q10.1 7.25 13.65 7.1 M1.55 18.15Q5.6 18.5 9.75 18.25L13.65 7.1 M2.05 17.9L6.3 7.7" fill="none" stroke="#d9f0f3" stroke-width=".12"/>
<path d="M5.2 9.5Q5.7 9.25 6.1 9.35 M9.25 10.6L10.3 10.45 M3.75 13.9Q4.4 14.1 5.05 13.9 M7.6 16.65L8.8 16.4" fill="none" stroke="#73b6c0" stroke-width=".12"/>
</g>'''
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+wood+fabric+'</svg>'
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('ffffff')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,820),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'HILLFOLK BED / native oblique silhouette > wooden slats + chaff-stuffed fabric > actual VTE reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + Y'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable source-shaped construction'),(1000,Image.open(donor).convert('RGBA'),'Actual VTE Bed_south / style only')]:
 im=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(im,(x,100),im);draw.text((x,565),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Preserve the source headboard at upper-right, sleeping surface toward lower-left, low foot rail and short supports.',
 'The fabric is stuffed with watervine chaff over wooden slats. No donor pillow, spring mattress or extra blanket is added.',
 'Pale cyan identifies fabric ownership for extraction; final layers are neutral and receive actual native w/Y tint.',
 'One fixed-view source tile. Native sleeping/occupant behavior and rare animated-furniture fallback remain pending.']):draw.text((20,655+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared source bed, actual VTE reference and editable oblique frame/fabric. Bed part bytes:',len(code))
