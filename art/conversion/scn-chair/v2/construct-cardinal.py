"""Reproject marsh-dweller plank chair into one straight south map-facing view."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'source-packet.json').exists(),'Preserve authoring history'
packet=json.loads((OLD/'source-packet.json').read_text(encoding='utf-8'))
packet.update(supersedes=asset(OLD/'source-packet.json'),camera=dict(facing='south/front',reference='Actual installed VFE Things/Seating/SquareChair/Chair_south, not its east image or the original Qud diagonal projection.',projection='Straight symmetrical back, horizontal rails/seat and vertical supports; only shallow layer shading. No yaw, isometric seat, diagonal footprint or converging side rails.'),
 construction='Source nailed plank chair reconstructed with tall open back, two inner vertical back slats, upper/lower rails, hard horizontal plank seat and two source-like long visible supports. Rear supports overlap/are occluded in this straight-facing authoring, not a claim that native furniture physically has only two legs. Exact hidden joinery remains interpretation. No canvas, upholstery, armrests or curved back.',
 source_camera_boundary='Original Qud art has an oblique hard seat and offset support extents. Preserve its parts/materials/palette in a new cardinal presentation; do not trace its camera or claim source-pixel position is native facing data.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
frame='''<g fill="#a6a6a6" stroke="#414141" stroke-width=".17" stroke-linejoin="round">
<path d="M3.5 2.05H4.25V20.5H3.5ZM11.75 2.05H12.5V20.5H11.75Z"/>
<path d="M3.65 4.05H12.35V4.85H3.65ZM3.65 9.55H12.35V10.35H3.65Z"/>
<path d="M6.35 4.75H7.05V9.7H6.35ZM8.95 4.75H9.65V9.7H8.95Z"/>
<path d="M3.5 16.15H4.35V22H3.5ZM11.65 16.15H12.5V22H11.65Z"/>
<path d="M3.9 17H12.1V17.85H3.9Z" fill="#878787"/>
<path d="M3.65 2.3V3.8M3.75 5.1V9.2M11.95 5.1V9.2M3.75 18V21.7M11.9 18V21.7" fill="none" stroke="#dddddd" stroke-width=".065"/>
<path d="M4.7 4.4H11.1M4.65 9.95H11.2" fill="none" stroke="#777777" stroke-width=".055"/>
</g>'''
seat='''<g stroke="#3e6065" stroke-width=".15" stroke-linejoin="round"><path d="M2.75 13.1H13.25V16.4H2.75Z" fill="#83c6cf"/><path d="M2.75 16.4H13.25V17.05H2.75Z" fill="#5898a3"/>
<path d="M2.95 14.15H13.05M2.95 15.25H13.05" stroke="#538d96" stroke-width=".065"/><path d="M3 13.32H12.95M3 16.55H12.95" stroke="#c5ebef" stroke-width=".065"/>
<path d="M4.1 13.75L5.6 13.7M8.7 14.65L10.8 14.7M5 15.8L7 15.75" stroke="#609aa4" stroke-width=".045"/></g>'''
# Joint nails are on the structural back; pale/cyan hard seat remains a separate native tint region.
for x,y in [(4,4.45),(12,4.45),(4,9.95),(12,9.95)]:frame+=f'<circle cx="{x}" cy="{y}" r=".11" fill="#636363"/>'
for name,content in [('front',frame+seat),('frame',frame),('seat',seat)]:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{content}</svg>'
 (HERE/f'constructed-{name}.svg').write_bytes(svg.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{name}.svg'),skip_system_fonts=True))
plate=Image.new('RGB',(1440,830),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);d.text((20,15),'CHAIR / source identity retained > corrected cardinal south construction > actual named RimWorld view',font=font,fill='#e3cf43')
for x,p,label in [(35,OLD/'refined-proposal.png','Rejected oblique source-camera draft'),(510,HERE/'constructed-front.png','New cardinal front / hard plank seat')]:
 im=Image.open(p).convert('RGBA').resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,65),im);d.text((x,530),label,font=font,fill='#e3cf43')
ref=Path(packet['donor_reference']['path']);im=Image.open(ref).convert('RGBA');im.thumbnail((300,360));im=im.resize((240,320),Image.Resampling.NEAREST);plate.paste(im,(1005,110),im);d.text((975,530),'Actual VFE Chair_south / cardinal',font=font,fill='#e3cf43')
for i,line in enumerate(['Tall slatted back, nailed right-angle planks and hard seat remain Qud design features.',
 'Back, seat and supports face straight south; no diagonal seat, three-quarter camera or skewed rails.',
 'Cyan seat is a segmentation aid for native y, not cloth or upholstery. Wood frame uses native w.',
 'Hidden rear support overlap is authored; native sitting/physics/fallback behavior is unchanged.']):d.text((20,615+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'camera-construction-comparison.png')
