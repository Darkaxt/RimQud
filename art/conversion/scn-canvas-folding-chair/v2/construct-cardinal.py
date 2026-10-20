"""Qud portable sling stool, reconstructed in one straight south map view."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
packet=json.loads((OLD/'source-packet.json').read_text(encoding='utf-8'))
ref=json.loads((ROOT/'art/conversion/scn-chair/v2/source-packet.json').read_text(encoding='utf-8'))['donor_reference']
ref['role']='Actual installed VFE Chair_south supplies straight map-facing parallel seat edges, aligned supports and restrained top visibility only. Its tall back, padded seat, mechanics and footprint are not copied.'
packet.update(supersedes=asset(OLD/'source-packet.json'),camera_reference=ref,camera={'facing':'south/front','rule':'Symmetric cardinal footprint, horizontal seat extents and only shallow top visibility. X braces are intrinsic folding structure, not a rotated camera.'},construction='Backless thin knit-watervine sling between short parallel wooden edge rails, crossed jointed wood supports with one visible central pivot. Far supports overlap in the straight front view. Hidden joinery is authored, not native mechanism metadata.',source_camera_boundary='Original has an oblique seat; preserve its sling and folding wood identity while rebuilding the camera. No actual fold/unfold state or new four-way rotation is introduced.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
frame='''<g fill="#9c9c9c" stroke="#414141" stroke-width=".15" stroke-linejoin="round">
<path d="M3.05 14.1H3.62L4.85 20.15H4.27ZM12.38 14.1H12.95L11.73 20.15H11.15Z" fill="#777777"/>
<path d="M3.15 14.1L3.7 13.75L12.55 21.4L12.05 21.95ZM12.3 13.75L12.85 14.1L3.95 21.95L3.45 21.4Z"/>
<path d="M3.6 14.3L11.95 21.45M12.35 14.3L3.95 21.4" fill="none" stroke="#d2d2d2" stroke-width=".065"/>
<circle cx="8" cy="17.8" r=".27" fill="#6d6d6d"/><circle cx="8" cy="17.8" r=".11" fill="#c8c8c8"/>
</g>'''
cloth='''<g stroke="#41656c" stroke-width=".14" stroke-linejoin="round">
<path d="M2.9 10.55Q8 11.1 13.1 10.55V13.85Q8 14.55 2.9 13.85Z" fill="#8bcbd4"/>
<path d="M3.1 10.84Q8 11.35 12.9 10.84M3.12 13.55Q8 14.18 12.88 13.55" fill="none" stroke="#bde8ec" stroke-width=".075"/>
<path d="M4.2 11.4Q8 12.55 11.8 11.4M4 12.2Q8 13.1 12 12.2" fill="none" stroke="#6baeb9" stroke-width=".055"/>
</g>'''
rails='''<g fill="#ababab" stroke="#414141" stroke-width=".14"><path d="M2.45 10.25H3.05V14.2H2.45ZM12.95 10.25H13.55V14.2H12.95Z"/><path d="M2.7 10.45V13.95M13.2 10.45V13.95" stroke="#dedede" stroke-width=".07"/></g>'''
for name,content in [('front',frame+cloth+rails),('frame',frame+rails),('fabric',cloth)]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{content}</svg>'
    p=HERE/f'constructed-{name}.svg';p.write_bytes(svg.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
plate=Image.new('RGB',(1440,830),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
d.text((20,15),'CANVAS FOLDING CHAIR / preserve Qud sling and jointed wood; reconstruct the cardinal camera',font=font,fill='#e3cf43')
for x,p,label in [(35,OLD/'refined-proposal.png','Historical angled draft / superseded camera'),(510,HERE/'constructed-front.png','Straight south / backless sling and X frame')]:
    im=Image.open(p).convert('RGBA').resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,65),im);d.text((x,530),label,font=font,fill='#e3cf43')
im=Image.open(ref['path']).convert('RGBA').resize((144,192),Image.Resampling.NEAREST);plate.paste(im,(1080,160),im);d.text((970,530),'Actual VFE Chair_south / camera only',font=font,fill='#e3cf43')
for i,t in enumerate(['No backrest, armrests, padded cushion, metal mechanism, occupant or packed pose is added.',
'Cloth detail y stays separate from jointed wooden primary w; cyan is an extraction aid only.',
'The diagonal X is physical bracing under a cardinal seat, not an oblique footprint.',
'One deployed native tile, one full 16x24 cell frame. Native sitting/takeability stays native.']):d.text((20,615+i*32),t,font=font,fill='#e5e8d8')
plate.save(HERE/'camera-construction-comparison.png')
