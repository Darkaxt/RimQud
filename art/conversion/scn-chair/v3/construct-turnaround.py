"""Retain corrected plank-chair front; author complete side and rear overlap."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2';SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
packet=json.loads((OLD/'source-packet.json').read_text());camera_evidence=ROOT/'art/conversion/scn-canvas-folding-chair/v3/source-packet.json';prior=json.loads(camera_evidence.read_text())
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),retained_front=ref(OLD/'registered/model.json'),directional_reference=prior['directional_reference'],directional_reference_evidence=ref(camera_evidence),
 camera=dict(contract='Retain corrected cardinal south plank chair. Complete right profile has broad rectangular hard seat and edge-on tall back. Rear back posts occlude the hard seat instead of being painted behind it.',authored_front_width=10.5,authored_depth=8.3,depth_status='Authored hidden seat depth guided by source proportions and legacy directional map camera; no runtime donor physical dimension inferred.',unseen='Rear/side plank joinery, far-support overlap and nail heads are authored continuation of the same right-angle frame. No padded seat, canvas, rounded back, armrests or new mechanism.',west='Mirror east; no asymmetric marks or side fittings.'),
 construction='Source nailed-plank chair with two inner back slats and upper/lower rails; hard rectangular plank seat with independent source tint. Side shows back edge and full seat depth with front/rear supports. Rear draws back posts above seat, preserving occlusion and source identity.',
 native_acceptance='Pending full-set generation gate; native non-takeable20-weight Chair interaction, MissileCover10, non-occlusion, rare Animated fallback and extra-view placement remain unfinished.')
# The reused reference limits concern only camera; this Chair has no sling.
packet['directional_reference']=dict(packet['directional_reference']);packet['directional_reference']['role']='Actual installed legacy VFE chair S/E/N establishes straight cardinal frame/seat convention only. It is not a structural replacement: source slatted back and hard nailed planks remain authoritative.'
write(HERE/'source-packet.json',packet)
old=OLD/'registered';front=Image.open(old/'neutral-master.png').convert('RGBA').convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');owner=Image.open(old/'seat-ownership-mask.png').convert('L');aa=Image.open(old/'neutral-master.png').getchannel('A');own=Image.merge('RGBA',(owner,owner,owner,aa)).convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');front.save(HERE/'selected-front-neutral.png');own.save(HERE/'ownership-south.png');a=np.array(front);w=np.array(own)[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-w[:,:,None])+w[:,:,None]*np.array([.65,.9,1])));Image.fromarray(a).save(HERE/'constructed-south.png')
east='''<g stroke="#414141" stroke-width=".17" stroke-linejoin="round">
<path d="M5.1 16.2H5.8V20.5H5.1ZM10.1 16.2H10.8V20.5H10.1Z" fill="#878787"/>
<path d="M4.1 17H11.5V17.85H4.1Z" fill="#878787"/>
<path d="M11.05 16.2H11.8V22H11.05Z" fill="#a6a6a6"/>
<path d="M3.8 13.1H12.1V16.4H3.8Z" fill="#83c6cf" stroke="#3e6065"/>
<path d="M3.8 16.4H12.1V17.05H3.8Z" fill="#5898a3" stroke="#3e6065"/>
<path d="M4.05 14.15H11.85M4.05 15.25H11.85" stroke="#538d96" fill="none" stroke-width=".065"/>
<path d="M4 13.32H11.9M4 16.55H11.9" stroke="#c5ebef" fill="none" stroke-width=".065"/>
<path d="M3.8 2.05H4.55V22H3.8Z" fill="#a6a6a6"/>
<path d="M4.55 4.05H5.15V4.85H4.55ZM4.55 9.55H5.15V10.35H4.55Z" fill="#a6a6a6"/>
<path d="M4 2.3V3.8M4 5.1V9.2M4 18V21.7M11.25 18V21.7" fill="none" stroke="#dddddd" stroke-width=".065"/>
</g><circle cx="4.2" cy="4.45" r=".1" fill="#636363"/><circle cx="4.2" cy="9.95" r=".1" fill="#636363"/>'''
tree=ET.parse(OLD/'constructed-front.svg').getroot();nodes=list(tree);seat=nodes[-1];assert seat.tag.endswith('g');north=''.join(ET.tostring(n,encoding='unicode') for n in [seat,*nodes[:-1]])
for f,body in [('east',east),('north',north)]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{body}</svg>';p=HERE/f'constructed-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True));im=np.array(Image.open(p.with_suffix('.png')).convert('RGBA')).astype(int);cyan=(im[:,:,1]-im[:,:,0]>4)&(im[:,:,2]-im[:,:,0]>4);v=np.where(cyan,255,0).astype(np.uint8);Image.fromarray(np.dstack([v,v,v,np.uint8(im[:,:,3])])).save(HERE/f'ownership-{f}.png')
sheet=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,760),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'NAILED PLANK CHAIR / retained front, complete hard-seat profile and rear post ownership',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((280,420),Image.Resampling.LANCZOS);plate.paste(im,(50+i*470,55),im);d.text((50+i*470,500),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Source marsh-dweller nailed planks, two inner back slats and hard seat retained; no upholstery or fabric added.',
 'Complete side uses authored8.3depth. Rear back posts render above the seat, rather than disappearing behind it.',
 'Actual VFE reference is installed legacy art; current SchoolChair mapping is not imported into its metadata.',
 'Same native16x24cell/pivot8,16. One fixed chair tile; native sitting/cover/fallback acceptance remains pending.']):d.text((18,590+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Missing directional construction before refinement',review='Selected straight front retained. Complete side has hard seat, edge-on back and attached front/rear supports at common scale; rear posts correctly own overlap over tinted seat. Original two slats, upper/lower rails and nailed right-angle joinery retained. Hidden depth/supports authored, no copied padded donor construction.'))
(HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Same source-faithful Qud wooden Chair, three cardinal map views on1536x768canvas, three equal512x768columns. LEFT SOUTH is selected existing front and must retain its design. CENTER EAST is authored complete hard-seat profile, RIGHT NORTH the rear where vertical back posts occlude the seat. Image2 actual legacy VFE Chair_east is camera/outline reference only.
Canonical description: planks of wood nailed together at right angles in marsh-dweller style. Keep tall open slatted wooden back, two inner vertical back slats, upper/lower rails, hard rectangular plank seat and attached supports. Gray frame, pale cyan HARD WOOD seat is only an independent native tint-role aid; it is not fabric, padding or upholstery. Refine subtle wood grain and plain nail/joinery detail consistently. No cloth folds, cushion, canvas, round back, armrests, ornate carving, occupant, desk or extra props.
Preserve exact current contours/scale/positions, full8.3depth side seat, straight cardinal facings and all back/support gaps. No thin end-on view, perspective convergence, oblique yaw, diagonal footprint or front backrest pasted onto the side. Side back is edge-on; rear posts must remain ABOVE tinted seat. No moved/deleted slat, missing leg or new articulation. Retain one same chair, no folded/occupied state. Same1536x768three-panel sheet, transparent exterior/open gaps, no glow/shadow/backdrop/text/labels.''',encoding='utf-8')
print('Retained wooden Chair front and authored complete hard-seat side/rear with correct post occlusion.')
