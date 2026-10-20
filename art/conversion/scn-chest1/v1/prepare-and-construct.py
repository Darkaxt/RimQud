"""Source chest: hinged wood lid, bright side bands, native primary-colored latch."""
from pathlib import Path
import hashlib,json,re,subprocess
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Chest1','Chest','Furniture']};obj=ET.fromstring(objects['Chest']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/chest1-mask.png');assert digest(source)=='ee9142fb81d55c406ed7ed1530310f9f3991ecbc044ca82292af498117272af2'
donor=Path('D:/Steam/steamapps/workshop/content/294100/1961098970/1.5/Textures/Things/CrateA/CrateA_south.png');about=donor.parents[4]/'About/About.xml'
assembly=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed/Assembly-CSharp.dll');code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.Container',str(assembly)],capture_output=True,check=True).stdout
packet=dict(entry='SCN-CHEST1',identity='Chest1 -> Chest -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Assets_Content_Textures_Tiles_sw_chest.bmp',canvas=[16,24],info_id=14698,atlas_id=277,rect=[1512,754,16,24]),
 source_shape='Low broad closed chest. Raised/shouldered lid at top, two bright bands running down its outer sides with a lid seam, central primary-colored rectangular latch and front-panel marks. Gaps in the tiny glyph do not establish transparent wooden faces or detached straps.',
 palette=dict(primary='w',detail='W',native_primary_rgb='98875f',native_detail_rgb='cfc041',rule='Wood body/lid, front marks and center latch stay primary w. Only two source-bright side bands use W. Gold bands are an extraction aid; final layers are neutral. A latch is not automatically assigned bright gold because it is hardware.'),
 donor_reference=dict(mod='[JDS] Simple Storage',package_id='JangoDsoul.SimpleStorage',workshop_id='1961098970',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed1.5CrateA_south supplies restrained plank grain, shallow wooden-edge shading and game-art contours. Its flat crate top, cross-brace, nails, dimensions, storage mechanics and brown source pixels are not copied.'),
 construction='Editable opaque wood case and shallow shouldered hinged lid, two side reinforcing bands, central recessed primary-role latch and sparse abstract scratched notches. Band material, exact plank seams and notch forms remain authored interpretation; source bright bands do not establish a new native material property. No visible loot, letters, ornate lock or open-lid alternate state.',
 native_state=dict(tile='One fixed inherited chest tile; Chest1 changes inventory builder/tier/aggregation rather than appearance. No open/closed, empty/full or random tile is declared.',part='XRL.World.Parts.Container',assembly_sha256=digest(assembly),decompiled_stdout_sha256=hashlib.sha256(code).hexdigest(),part_declares_Render_or_Tile=bool(re.search(rb'\b(Render|Tile)\b',code)),rule='Keep native container/inventory/smart-use/open sound and original physics. Do not infer a new packed/open appearance or unspecified takeability/solidity defaults.'),
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full-cell transform for wood, lid, bands, latch and masks; no independent strap/latch centering.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".15" stroke-linejoin="round">
<path d="M1.3 8.5L3.35 6.25H12.65L14.7 8.5V17.8H1.3Z" fill="#aaa"/>
<path d="M1.3 8.5Q7.95 7.8 14.7 8.5V12.05H1.3Z" fill="#c4c4c4"/>
<path d="M3.55 6.5H12.4 M3.1 9.7H12.9 M3.1 15.75H12.9 M3.1 17H12.9" fill="none" stroke="#818181" stroke-width=".09"/>
<path d="M3.2 6.25H4.4L2.65 8.7V11.95H1.3V8.5Z M11.6 6.25H12.8L14.7 8.5V11.95H13.35V8.7Z M1.3 12.35H2.65V17.8H1.3Z M13.35 12.35H14.7V17.8H13.35Z" fill="#cfc041"/>
<path d="M1.3 12.15H14.7" fill="none" stroke="#454545" stroke-width=".2"/>
<path d="M6.5 11.2H9.5V14.8H6.5Z" fill="#a4a4a4"/>
<path d="M7.2 11.85H8.8V14H7.2Z" fill="#4a4a4a"/>
<path d="M4.1 13.2V15.1H11.9V13.2 M4.25 10.1L4.65 10.45L5.2 10.05 M10.1 9.4L10.1 10.05L10.65 9.85 M5.3 16.6L5.75 16.2L6.2 16.55" fill="none" stroke="#5d5d5d" stroke-width=".1"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('98875f'),bytes.fromhex('cfc041')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'CHEST1 / original shouldered lid + bright side bands + primary latch > editable wood > actual mod reference',font=font,fill='#e3cf43')
for x,im,label in [(70,native,'Original / native w + W'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable wood/lid/bands/latch'),(1000,Image.open(donor).convert('RGBA'),'Actual JDS crate / wood style only')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,545),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Low closed wooden chest, side bands, center latch and abstract scratched notches follow source identity.',
 'Native W belongs to the two side bands; the central latch stays primary w as in the original mask.',
 'No visible loot, readable language, donor cross-brace or invented open-lid state is introduced.',
 'One shared source-cell frame. Actual container/inventory, source physics and visibility acceptance remain pending.']):draw.text((20,620+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared source-shaped chest, exact native container appearance boundary and actual JDS crate reference.')
