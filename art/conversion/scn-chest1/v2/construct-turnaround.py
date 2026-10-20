"""Source shouldered chest retained; cardinal end/back authored without new states."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/1961098970');SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
packet=json.loads((OLD/'source-packet.json').read_text());textures={}
for f in ['south','east','north']:
    p=MOD/f'1.5/Textures/Things/CrateA/CrateA_{f}.png';im=Image.open(p).convert('RGBA');textures[f]=dict(**private(p),frame=list(im.size),alpha_bounds=list(im.getchannel('A').getbbox()))
defs=MOD/'1.5/Defs/ThingDefs_Building.xml';tree=ET.parse(defs).getroot();base=next(n for n in tree if n.get('Name')=='SimpleStorageBase');child=next(n for n in tree if n.findtext('defName')=='JDSS_CrateA')
camera_path=ROOT/'art/conversion/scn-argyve-multicabinet/v2/source-packet.json';camera=json.loads(camera_path.read_text())['directional_reference']
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),retained_front=ref(OLD/'registered/model.json'),
 directional_reference=dict(wood_textures=textures,wood_definition=private(defs),wood_definition_fields=dict(def_name='JDSS_CrateA',graphic_class=base.findtext('graphicData/graphicClass'),draw_size=child.findtext('graphicData/drawSize'),footprint=child.findtext('size')),wood_reference_version='Actual installed1.5folder; no LoadFolders.xml present and active current-game binding not claimed.',wood_limit='JDS east has diagonal/oblique camera and is REJECTED as the target camera. Wood grain/material reference only; its box/cross brace/nails/gameplay/dimensions are not imported.',cardinal_camera_reference=camera,cardinal_camera_evidence=ref(camera_path),role='Use actual JDS wood surface style plus documented VFE fixed cardinal box planes as camera convention only. Qud raised/shouldered lid, two bright bands and primary latch remain authoritative.'),
 camera=dict(contract='Front-aligned closed box. Source top outline is physically shouldered: retain raised central lid and sloping shoulders, not a hidden isometric yaw. New end is broad rectangular depth with parallel front/back edges and full body volume.',front_review='Original native mask itself steps up at the lid and includes the two outer bright bands. Front walls/latch/bands remain vertically aligned; retained slope is interpreted as a raised shouldered lid, an authored source-bound shape rather than a recovered perspective plane.',authored_width=13.4,authored_depth=8.4,depth_status='Authored hidden depth informed by cardinal box reference and source width; not measured from JDS diagonal image or Qud upright icon.',side='Plain wood end, lid seam and visible return of wrap bands along lid shoulder. No new side handle or front latch pasted onto end.',rear='Closed rear with the same wrapping bands and two small primary-role hinge joins. Hinged-lid description supports hinges; exact placement/material remains authored. No rear latch or repeated front scratch layout.',west='Mirror east; unmarked symmetric end geometry and band returns.'),
 construction='Retain original selected front without another front generation. Author broad closed wooden end and shouldered rear, continuing two reinforcing bands in plausible wrap geometry. Abstract front scratches are not readable writing or proof of inventory. Hidden band routing/hinge joins are authored, not native mechanism definitions.',native_acceptance='Pending full-set generation gate; native fixed chest inventory/smart-use/sound/physics/visibility and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
old=OLD/'registered';front=Image.open(old/'neutral-master.png').convert('RGBA').convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');owner=Image.open(old/'band-ownership-mask.png').convert('L');aa=Image.open(old/'neutral-master.png').getchannel('A');own=Image.merge('RGBA',(owner,owner,owner,aa)).convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');front.save(HERE/'selected-front-neutral.png');own.save(HERE/'ownership-south.png');a=np.array(front);w=np.array(own)[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-w[:,:,None])+w[:,:,None]*np.array([1,.95,.4])));Image.fromarray(a).save(HERE/'constructed-south.png')
east='''<g stroke="#303030" stroke-width=".15" stroke-linejoin="round">
<path d="M3.8 6.25H12.2V17.8H3.8Z" fill="#aaaaaa"/>
<path d="M3.8 6.25H12.2V8.5H3.8Z" fill="#c4c4c4"/>
<path d="M3.8 8.5H12.2V12.05H3.8Z" fill="#b9b9b9"/>
<path d="M3.8 7.8H12.2V8.5H3.8Z" fill="#cfc041"/>
<path d="M3.8 12.15H12.2" fill="none" stroke="#454545" stroke-width=".2"/>
<path d="M4.1 6.55H11.9M4.1 9.7H11.9M4.1 15.75H11.9M4.1 17H11.9" fill="none" stroke="#818181" stroke-width=".09"/>
</g>'''
north='''<g stroke="#303030" stroke-width=".15" stroke-linejoin="round">
<path d="M1.3 8.5L3.35 6.25H12.65L14.7 8.5V17.8H1.3Z" fill="#aaaaaa"/>
<path d="M1.3 8.5Q7.95 7.8 14.7 8.5V12.05H1.3Z" fill="#c4c4c4"/>
<path d="M3.55 6.5H12.4M3.1 9.7H12.9M3.1 15.75H12.9M3.1 17H12.9" fill="none" stroke="#818181" stroke-width=".09"/>
<path d="M3.2 6.25H4.4L2.65 8.7V11.95H1.3V8.5ZM11.6 6.25H12.8L14.7 8.5V11.95H13.35V8.7ZM1.3 12.35H2.65V17.8H1.3ZM13.35 12.35H14.7V17.8H13.35Z" fill="#cfc041"/>
<path d="M1.3 12.15H14.7" fill="none" stroke="#454545" stroke-width=".2"/>
<path d="M4.2 11.8H5.4V12.55H4.2ZM10.6 11.8H11.8V12.55H10.6Z" fill="#8a8a8a"/>
<path d="M4.35 12.15H5.25M10.75 12.15H11.65" fill="none" stroke="#5d5d5d" stroke-width=".08"/>
</g>'''
for f,body in [('east',east),('north',north)]:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{body}</svg>';p=HERE/f'constructed-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True));im=np.array(Image.open(p.with_suffix('.png')).convert('RGBA')).astype(int);gold=(im[:,:,0]-im[:,:,2]>12)&(im[:,:,1]-im[:,:,2]>12);v=np.where(gold,255,0).astype(np.uint8);Image.fromarray(np.dstack([v,v,v,np.uint8(im[:,:,3])])).save(HERE/f'ownership-{f}.png')
sheet=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,760),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'CHEST1 / retained source shouldered lid, complete closed end, wrapping bands and rear hinges',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((280,420),Image.Resampling.LANCZOS);plate.paste(im,(50+i*470,55),im);d.text((50+i*470,500),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Source shouldered closed lid, two bright bands, primary center latch and front abstract scratches retained.',
 'Complete8.4depth end uses parallel planes. Rear hinge joins and hidden band routing are authored, not recovered metadata.',
 'Actual JDS wood reference inspected; diagonal east is rejected for camera. Cardinal VFE box convention guides volume.',
 'One fixed native chest tile; no open/empty/full/packed art or visible loot. Extra views unbound; native acceptance pending.']):d.text((18,590+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Missing directional art before refinement',review='Retained front shoulder interpretation is supported by original stepped lid contour, aligned bands/walls and centered latch. Broad end continues lid seam and band return without an invented handle; rear hinges are explicit authored continuation. Shared cell/pivot and one source state, no copied oblique JDS camera.'))
(HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Same Qud Chest1 closed wooden storage box, three cardinal views on1536x768canvas, three equal512x768columns: selected SOUTH front left, authored complete EAST end center, NORTH rear right. Image1 is edit target; image2 actual JDS CrateA_south is ONLY a wood-grain/edge-shading reference. Do not copy crate design, cross brace, nails, footprint, camera or storage mechanics.
Canonical description: wood box with hinged lid and latch; abstract surface notches hint at language. Retain raised/shouldered lid as a physical shape, two source bright reinforcing bands and central primary-role front latch. Original stepped shoulders are intrinsic lid geometry, not permission for yaw or a diagonal camera. Preserve exact panel sizes/positions/scale and common frame. Complete end has broad8.4depth and parallel edges; rear has two bands and small primary-role hinge joins, no repeated front latch. No end handles, rear latch, readable letters, ornate lock, visible contents, new open/empty/full state or props.
Refine modest wood grain/shallow bevels to match the selected front. Gray wood including latch/hinges; muted gold ONLY in the existing source band ownership regions, including end roof return. No auto-gold latch/hinges. Preserve lid seams, attachments and full closed opaque wood coverage. Same1536x768three-column sheet and margins. Transparent exterior, no glow/shadow/backdrop/text/labels. No side squash, independent view centering, perspective convergence or new design alternatives.''',encoding='utf-8')
print('Retained source shoulder/latch front and authored complete cardinal end/rear with explicit reference/state limits.')
