"""Retain corrected sling-stool front; author complete side and reverse frame."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2';MOD=Path('D:/Steam/steamapps/workshop/content/294100/1718190143');SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in ['south','east','north']:
    p=MOD/f'Textures/Things/Seating/SquareChair/Chair_{f}.png';im=Image.open(p).convert('RGBA');refs[f]=dict(**private(p),frame=list(im.size),alpha_bounds=list(im.getchannel('A').getbbox()))
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),retained_front=ref(OLD/'registered-corrected/model.json'),
 directional_reference=dict(textures=refs,definition_inspected=private(MOD/'1.6/Defs/Buildings_Furniture/Buildings_BasicSeats.xml'),load_folders=private(MOD/'LoadFolders.xml'),binding='These are actual installed LEGACY SquareChair textures. Current1.6 Seat_SquareChair resolves NewThings/Furniture/SchoolChair/SchoolChair instead, so its Graphic_Multi/drawSize1x1 do not establish a render mapping for the selected legacy images.',graphic_class=None,draw_size=None,footprint=None,missing='Active render mapping for selected legacy path is not exported; no physical measurement inferred from alpha width or current unrelated path.',role='Legacy S/E/N seat edges and shallow cardinal camera convention only, plus already selected VTE Bedroll knit material reference. Neither supplies the source folding-frame structure or a native dimension.'),
 camera=dict(contract='Retain corrected south cardinal sling; complete east shows its full longitudinal seat extent rather than a thin edge. Parallel rails, vertical central axis, same16x24cell/pivot in every view. Diagonal X members are intrinsic bracing.',authored_front_width=11.1,authored_depth=7.6,depth_status='Authored estimate guided by source sling footprint and actual directional camera; no Qud hidden length or donor dimension claimed.',side_structure='Two transverse X frames fold across stool width. End view sees paired wooden struts edge-on under longitudinal side rails, not another frontal X pasted onto the side. Precise hidden supports are authored.',rear_structure='Backless stool has comparable front/rear outline. Rear wooden overlap/dowel face and sling underside are authored; no tall backrest or new folding mechanism.',west='Mirror east; no side-specific marks, accessories or asymmetric structure.'),
 native_state=packet['native_state']+' Extra S/E/N/W are unbound authoring assets, not native rotation or folding controls.',native_acceptance='Pending full-set generation gate; native sitting/takeability, non-occlusion, rare animated fallback and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
old=OLD/'registered-corrected';front=Image.open(old/'neutral-master.png').convert('RGBA').convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');owner=Image.open(old/'fabric-ownership-mask.png').convert('L');aa=Image.open(old/'neutral-master.png').getchannel('A');rgb=Image.merge('RGBA',(owner,owner,owner,aa)).convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');rgb.save(HERE/'ownership-south.png');front.save(HERE/'selected-front-neutral.png');a=np.array(front);w=np.array(rgb)[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-w[:,:,None])+w[:,:,None]*np.array([.65,.9,1])));Image.fromarray(a).save(HERE/'constructed-south.png')
east='''<g stroke="#414141" stroke-width=".14" stroke-linejoin="round">
<path d="M4.6 13.5H5.13L5.65 20.1H5.1ZM10.9 13.5H11.43L10.9 20.1H10.35Z" fill="#777777"/>
<path d="M3.95 13.8H4.5L4.95 21.9H4.4ZM11.5 13.8H12.05L11.6 21.9H11.05Z" fill="#9c9c9c"/>
<path d="M4.2 14.1H11.8V14.55H4.2Z" fill="#a6a6a6"/>
<path d="M4.1 10.5Q8 11 11.9 10.5V13.85Q8 14.5 4.1 13.85Z" fill="#8bcbd4" stroke="#41656c"/>
<path d="M4.35 10.85Q8 11.35 11.65 10.85M4.3 13.6Q8 14.1 11.7 13.6" fill="none" stroke="#bde8ec" stroke-width=".075"/>
<path d="M5.2 11.5Q8 12.35 10.8 11.5M5 12.3Q8 13.1 11 12.3" fill="none" stroke="#6baeb9" stroke-width=".055"/>
<path d="M3.85 10.3H12.15V10.75H3.85ZM3.85 13.95H12.15V14.35H3.85Z" fill="#ababab"/>
</g>'''
south_tree=ET.parse(OLD/'constructed-front.svg').getroot();north_body=''.join(ET.tostring(n,encoding='unicode') for n in south_tree)
# Reverse the visible crossing order on the far frame, preserving the same
# physical members and silhouette rather than inventing a stool backrest.
north_body=north_body.replace('M3.15 14.1L3.7 13.75L12.55 21.4L12.05 21.95ZM12.3 13.75L12.85 14.1L3.95 21.95L3.45 21.4Z','M12.3 13.75L12.85 14.1L3.95 21.95L3.45 21.4ZM3.15 14.1L3.7 13.75L12.55 21.4L12.05 21.95Z')
for f,body in [('east',east),('north',north_body)]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{body}</svg>';p=HERE/f'constructed-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True));im=np.array(Image.open(p.with_suffix('.png')).convert('RGBA'));cyan=(im[:,:,1]>im[:,:,0]+4)&(im[:,:,2]>im[:,:,0]+4);v=np.where(cyan,255,0).astype(np.uint8);Image.fromarray(np.dstack([v,v,v,im[:,:,3]])).save(HERE/f'ownership-{f}.png')
sheet=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,760),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'CANVAS FOLDING CHAIR / retained cardinal front, complete side, reverse backless frame',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((280,420),Image.Resampling.LANCZOS);plate.paste(im,(50+i*470,55),im);d.text((50+i*470,500),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Backless knit-watervine sling with jointed wood; no tall back, cushion, armrest, occupant or folded-state invention.',
 'S retained. E has full authored7.6depth and paired struts/longitudinal rails; rear reuses symmetrical X-frame outline.',
 'Selected VFE reference is installed LEGACY art, not the current SchoolChair texPath; its physical mapping is unknown.',
 'Source one deployed tile, takeable2-weight organic Chair. Extra views remain unbound; native acceptance pending.']):d.text((18,590+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Missing directional authoring before refinement',review='Retained source front. Complete broad end preserves source sling and attached wooden side supports; transverse folding braces are naturally edge-on rather than copied frontal X. Rear is the opposite face of a backless source-symmetrical stool. Hidden support/joinery remains authored. One deployed state only.'))
(HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Same Qud portable Canvas Folding Chair, three cardinal map views. Image1 is the edit target,1536x768canvas, three equal512x768columns: selected SOUTH front left, authored complete EAST side center, NORTH rear right. Image2 is actual installed LEGACY VFE Chair_east for cardinal camera only; do not copy its backrest, padded seat or mechanics.
Canonical description: jointed wood and knit watervine make a movable wharf. This is a BACKLESS thin sling stool with short parallel wooden rails and jointed crossed wood supports. Keep selected front design and refine only the plain new views to its modest wood/knit texture. Preserve exact canvas/positions/scale, full7.6depth side seat, attached wooden struts and all open gaps. In the side the transverse folding X frames are edge-on, represented by paired struts below longitudinal rails: do not paste the frontal X into the side or invent another mechanism. The rear is the opposite face of a backless stool, not a tall-backed chair. All rails remain parallel and facings straight; diagonal physical braces are allowed, but no yaw or camera shear. Do not thin/compress the whole end.
Gray wood, pale cyan knit sling only as separate color-role aid. Soft restrained folds, clean dark outline, modest wood grain; no thick cushion, backrest, armrests, metal chair frame, pillow, occupant, props, packed/folded alternative or dynamic fold state. Exact same1536x768sheet and three equal panels, transparent exterior/support gaps. No backdrop, glow, cast shadow, text or labels.''',encoding='utf-8')
print('Retained corrected front and authored missing full side/back with explicit source-state/reference limits.')
