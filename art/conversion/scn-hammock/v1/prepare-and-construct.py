"""Brinestraw lattice hammock: portable drape and actual support-owned hanging state."""
from pathlib import Path
import hashlib,json,re,subprocess
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p))
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Hammock','Furniture']};obj=ET.fromstring(objects['Hammock']);description=obj.find("part[@Name='Description']").get('Short')
states=json.loads((HERE/'native-state-index.json').read_text())['states'];assert len(states)==2
for state in states:assert digest(Path(state['private_mask']['path']))==state['private_mask']['sha256']
donor=Path('D:/Steam/steamapps/workshop/content/294100/3014915404/LegacyTextures/Textures/Animations/Fishing/FishingNetMote.png');about=Path('D:/Steam/steamapps/workshop/content/294100/3014915404/About/About.xml')
assembly=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed/Assembly-CSharp.dll')
code={name:subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.'+name,str(assembly)],capture_output=True,check=True).stdout for name in ['Hangable','Render']}
packet=dict(entry='SCN-HAMMOCK',identity='Hammock -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),
 source_shapes=dict(unhung='Native sw_shawl tile: top loop and two long hanging/draped lattice strips with pale frayed lower ends. This is the portable hammock appearance, not a new clothing item or creature.',hanging='Native sw_hammock tile: sagging diagonal rope lattice between a lower-left and upper-right end; open lower weave, selected pale inner edge and bright end tips. No support trees or stand are included in the tile.'),
 palette=dict(primary='y',detail='Y',native_primary_rgb='b1c9c3',native_detail_rgb='ffffff',glyph_only_ColorString='&Y',tile_specific_TileColor='&y',rule='TileColor explicitly supplies y for tile primary; ColorString Y remains glyph metadata. Native hanging render changes tile only, not colors. Main rope mesh uses y; selected bright strands/fringes/end tips use Y. Cyan authoring strands are an extraction aid; final layers are neutral.'),
 donor_reference=dict(mod='Vehicle Framework',package_id='SmashPhil.VehicleFramework',workshop_id='3014915404',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed legacy FishingNetMote supplies readable crossed-rope lattice and open mesh spacing only. It is retained legacy mod art, not claimed as an active current hammock asset. Its circular net outline, endpoint dots, fishing/vehicle behavior and source colors are not copied.'),
 reference_limits='Focused installed filename search found no direct hammock asset. Melee Animation coiled rope was viewed but not selected; the actual net is the closer lattice-material reference. Qud source tiles control both state silhouettes.',
 construction='Two editable rope-mesh silhouettes use actual open weave because the description specifies a lattice. The portable state keeps the source loop/two draped strips and frayed ends; the hanging state keeps source diagonal sag, end locations and frayed center. Mesh spacing, individual braids/knots and exact fray fibers are authored interpretation. No opaque blanket, clothing mannequin, baked trees, rigid stand or swinging animation.',
 native_state=dict(owner='XRL.World.Parts.Hangable',assembly_sha256=digest(assembly),decompiled_stdout_sha256={name:hashlib.sha256(value).hexdigest() for name,value in code.items()},rule='Hangable.CheckHanging uses actual native support availability; Render replaces E.Tile with HangingTile only while Hanging. Entered/LeftCell and zone lifecycle remain native. Keep2-weight organic takeable non-solid Bed/Hangable behavior, Hitpoints5and native support rules. No art-owned hanging state or new support objects.',render_color_evidence='Render.getTileColor returns the explicit TileColor when present; both native states retain the declared y/Y tile roles.'),
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One complete source-cell mapping for each native state and all role masks. Do not separately center mesh, fringes, end tips or state-specific visible alpha bounds.'),native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
shapes={
 'unhung':'M7.9 3.25C6.2 3.3 4.5 5.2 3.4 7.1L3.4 14.9L5.9 15.8L6.1 6.6L7.9 4.2L9.9 6.6L10.1 15.6L12.7 14.7L12.6 7.2C11.4 5.2 9.6 3.25 7.9 3.25Z',
 'hanging':'M1.3 10.65C2.1 15.1 6.2 17.2 9.65 13.5C12.1 11 13.55 7.2 14.25 2.4C14.7 9.5 13.9 15.6 9.7 19.3Q6.6 21 4.2 18.4C1.9 16.7 1.15 14.2 1.3 10.65Z'}
detail={
 'unhung':'M4 10.5L5 12 M11.1 8.6L12 10.3 M3.65 15L3.6 18.8 M4.6 15.4L5.4 21.2 M5.6 15.5L4.7 18.1 M10.45 15.3L10.5 19.8 M11.5 15.1L12.1 17.7 M12.3 14.9L11.3 17.6',
 'hanging':'M1.3 10.65C2.1 15.1 6.2 17.2 9.65 13.5C12.1 11 13.55 7.2 14.25 2.4'}
for state,path in shapes.items():
 mesh=''.join(f'<path d="M{-20+i} 0L{20+i} 24 M{-20+i} 24L{20+i} 0"/>' for i in range(-24,40,2))
 fringe='<path d="M6.5 19L6.2 19.8 M7.4 19.4L7.7 20 M8.35 19.4L8.6 19.85"/>' if state=='hanging' else ''
 svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<defs><clipPath id="mesh"><path d="{path}"/></clipPath></defs>
<g clip-path="url(#mesh)" fill="none" stroke-linecap="round"><g stroke="#303030" stroke-width=".36">{mesh}</g><g stroke="#b8b8b8" stroke-width=".22">{mesh}</g></g>
<path d="{path}" fill="none" stroke="#303030" stroke-width=".4" stroke-linejoin="round"/>
<path d="{path}" fill="none" stroke="#b8b8b8" stroke-width=".24" stroke-linejoin="round"/>
<g fill="none" stroke-linecap="round"><path d="{detail[state]}" stroke="#303030" stroke-width=".36"/><path d="{detail[state]}" stroke="#8dd3dd" stroke-width=".22"/></g>
<g fill="none" stroke="#aaa" stroke-width=".13" stroke-linecap="round">{fringe}</g></svg>'''
 (HERE/f'constructed-{state}.svg').write_bytes(svg.encode());(HERE/f'constructed-{state}.png').write_bytes(svg_to_bytes(svg_string=svg))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1000),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'BRINESTRAW HAMMOCK / real portable + hanging states > open rope lattice > actual installed net reference',font=font,fill='#e3cf43')
for x,state,label in [(65,'unhung','Editable portable / loop + fringe'),(535,'hanging','Editable hanging / diagonal sag')]:
 im=Image.open(HERE/f'constructed-{state}.png').convert('RGBA').resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,80),im);draw.text((x,550),label,font=font,fill='#e3cf43')
im=Image.open(donor).convert('RGBA');im.thumbnail((288,432));plate.paste(im,(1000,160),im);draw.text((960,550),'Actual legacy net / lattice only',font=font,fill='#e3cf43')
for i,line in enumerate(['Both exact native source states are shown in native-states-comparison.png; these are not two donor rotations.',
 'Hanging is selected by native support checks. No support trees, rigid stand or art-owned swinging behavior is added.',
 'Rope lattice has genuine holes; the folded/draped source is not clothing on an invented body.',
 'Native TILE primary is y via TileColor, detail Y. Glyph ColorString Y is retained separately.',
 'Cyan strands are extraction aids only. All production layers will be neutral before native tint.',
 'Braids, mesh spacing and small fray fibers are authored interpretation. Native state/visibility acceptance stays pending.']):draw.text((20,660+i*40),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared actual unhung/hanging mesh forms and explicit tile-color/native-support contracts.')
