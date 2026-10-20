"""Source three-front dresser with rectified cap and complete cardinal end/back."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in ['south','east','north']:
    p=MOD/f'Textures/Things/Building/Furniture/Dresser_{f}.png';im=Image.open(p).convert('RGBA');refs[f]=dict(**private(p),frame=list(im.size),alpha_bounds=list(im.getchannel('A').getbbox()))
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),retained_front_material=ref(OLD/'registered/model.json'),
 directional_reference=dict(textures=refs,definition=private(Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Furniture.xml')),load_folders=private(MOD/'LoadFolders.xml'),graphic_class='Graphic_Multi',draw_size=[2,1],footprint=[2,1],mapping='Actual donor S/N wide frame and E portrait frame rotate render footprint; transparent bounds are not Qud physical dimensions.',role='Parallel rectangular top planes, inset wood surfaces and shallow map-camera visibility only. Retain Qud tall three-front form, not donor low four2x2drawers/knobs or footprint/mechanics.'),
 camera=dict(contract='Straight stacked fronts with parallel rectangular cap; complete end has substantial authored depth. No converging cap edges or yaw. Same16x24source cell/pivot8,16.',authored_width=11.9,authored_depth=7.5,top_visibility_factor=.28,depth_status='Authored hidden depth guided by original broad cap and actual directional reference, not native Qud measurements.',front_correction='Preserve existing body/front/pull/foot material and replace only the receding trapezoid cap geometry with a parallel plane. Reuse existing cap material by row-wise surface-coordinate remapping; no separate AI front redraw.',unseen='Plain closed end/back wood with precise seam joinery. No front pulls or hidden brass rails are drawn onto unseen closed faces.',west='Mirror east; symmetric unmarked end and feet.'),
 construction='Three stacked precise wooden fronts: top rectangular recessed pull and opposed lower curved source motifs retained. New parallel cap keeps separate source detail ownership along with tiny feet. Body and hidden-depth assumptions remain explicit; internal brass rails do not become visible gold.',
 native_acceptance='Pending full-set generation gate; native non-solid80-weight/non-takeable organic container/inventory, rare Animated fallback and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
old=OLD/'registered';base=Image.open(old/'neutral-master.png').convert('RGBA').convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');old_owner=Image.open(old/'cap-feet-ownership-mask.png').convert('L');old_master=Image.open(old/'neutral-master.png').convert('RGBA');owner=Image.merge('RGBA',(old_owner,old_owner,old_owner,old_master.getchannel('A'))).convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA');base.save(HERE/'retained-front-before-cap.png')
cap='<path d="M2.05 2.25H13.95V5.05H2.05Z" fill="#8dd3dd" stroke="#303030" stroke-width=".14"/><path d="M2.05 4.35H13.95M2.3 4.6H13.7" fill="none" stroke="#9abfc7" stroke-width=".1"/>'
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{cap}</svg>';p=HERE/'parallel-front-cap.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
ca=np.array(Image.open(p.with_suffix('.png')).convert('RGBA'));a=np.array(base);o=np.array(owner);old_top=(o[:,:,0]>0)&(np.indices(o.shape[:2])[0]<220);a[old_top]=0;o[old_top]=0
# Map actual cap material rows into the new rectangular cap. This changes only
# surface coordinates, not the retained body/feet or any independent view scale.
source=np.array(old_master);ow=np.array(old_owner);cap_mask=(ow>127)&(source[:,:,3]>128)&(np.indices(ow.shape)[0]<900);sy,sx=np.where(cap_mask);ymin,ymax=int(sy.min()),int(sy.max());left=np.zeros(source.shape[0]);right=left.copy()
for y in range(ymin,ymax+1):
    xs=np.flatnonzero(cap_mask[y]);left[y]=xs.min() if len(xs) else sx.min();right[y]=xs.max() if len(xs) else sx.max()
ty,tx=np.where(ca[:,:,3]>0);target=[int(tx.min()),int(ty.min()),int(tx.max()),int(ty.max())];yy,xx=np.indices((768,512));ry=ymin+(yy-target[1])*(ymax-ymin)/(target[3]-target[1]);ry=np.clip(ry,ymin,ymax);l=np.interp(ry,np.arange(len(left)),left);r=np.interp(ry,np.arange(len(right)),right);rx=l+(xx-target[0])*(r-l)/(target[2]-target[0]);v=ndimage.map_coordinates(source[:,:,0].astype(float),[ry,rx],order=1,mode='nearest');ink=ca[:,:,:3].mean(2);inside=ca[:,:,3]>0;v[inside&(ink<120)]=ink[inside&(ink<120)];cv=np.uint8(np.clip(np.round(v),0,255));cv[~inside]=0;cap_neutral=Image.fromarray(np.dstack([cv,cv,cv,ca[:,:,3]]));front=Image.fromarray(a);front.alpha_composite(cap_neutral);front.save(HERE/'selected-front-neutral.png');role=Image.fromarray(o);white=np.full(ca.shape[:2],255,np.uint8);cap_owner=Image.fromarray(np.dstack([white,white,white,ca[:,:,3]]));role.alpha_composite(cap_owner);role.save(HERE/'ownership-south.png')
write(HERE/'cap-geometry-correction.json',dict(source_material=ref(OLD/'registered/neutral-master.png'),source_owner=ref(OLD/'registered/cap-feet-ownership-mask.png'),source_cap_y=[ymin,ymax],target_cap_bounds=target,method='Row-wise same-material cap coordinates map old converging cap into explicit parallel plane; preserved original body/feet and source role. No new ImageGen front, no global view stretch.',body_unchanged_below_authoring_y=220))
a=np.array(front);w=np.array(role)[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-w[:,:,None])+w[:,:,None]*np.array([.65,.9,1])));Image.fromarray(a).save(HERE/'constructed-south.png')
def unseen(f):
    end=f=='east';x0,x1=(4.25,11.75) if end else (2.05,13.95);top=1.02 if end else 2.25
    return f'''<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M{x0+.1} 4.8H{x1-.1}V20.7H{x0+.1}Z" fill="#888888"/>
<path d="M{x0+.4} 5.55H{x1-.4}V19.65H{x0+.4}Z" fill="#a6a6a6" stroke="#747474" stroke-width=".08"/>
<path d="M{x0+.05} 20.15H{x1-.05}V20.85H{x0+.05}Z" fill="#aaaaaa"/>
<path d="M{x0+.15} 20.7H{x0+.8}V21.75H{x0+.15}ZM{x1-.8} 20.7H{x1-.15}V21.75H{x1-.8}Z" fill="#8dd3dd"/>
<path d="M{x0} {top}H{x1}V5.05H{x0}Z" fill="#8dd3dd"/>
<path d="M{x0} 4.35H{x1}M{x0+.25} 4.6H{x1-.25}" fill="none" stroke="#9abfc7" stroke-width=".1"/>
</g>'''
for f in ['east','north']:
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{unseen(f)}</svg>';p=HERE/f'constructed-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True));im=np.array(Image.open(p.with_suffix('.png')).convert('RGBA')).astype(int);cyan=(im[:,:,1]-im[:,:,0]>4)&(im[:,:,2]-im[:,:,0]>4);vv=np.where(cyan,255,0).astype(np.uint8);Image.fromarray(np.dstack([vv,vv,vv,np.uint8(im[:,:,3])])).save(HERE/f'ownership-{f}.png')
sheet=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,760),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'DRESSER / retained three fronts, corrected parallel cap, complete plain end/back',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((280,420),Image.Resampling.LANCZOS);plate.paste(im,(50+i*470,55),im);d.text((50+i*470,500),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Three stacked front motifs and precise wood retained. New cap planes have parallel edges; end depth7.5 is authored.',
 'Source frame/cap/feet all use native w. Cyan is ownership only; internal brass rails do not justify gold hardware.',
 'Actual VTE/Core Dresser uses Graphic_Multi with2x1drawSize/footprint; its donor four-drawer layout is not copied.',
 'Same native16x24cell/pivot8,16; extra views unbound. One source container state and rare Animated fallback stay native.']):d.text((18,590+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Camera correction and missing directions before composed refinement',review='Three source fronts/pulls and lower body/feet retained from selected art. Receding cap replaced by parallel geometry using existing cap material. Complete broad end/back have plain closed wood panels with no copied fronts, gold rails or clothing inventory. Depth and hidden joinery remain authored; one fixed source tile.'))
(HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Same Qud Dresser in three cardinal map views on1536x768canvas, equal512x768columns. Image1 edit target: patched SOUTH left retains selected three stacked fronts and new PARALLEL cap; complete EAST end center; NORTH back right. Image2 actual VTE Dresser_east only for precise wood surfaces and parallel map-camera convention; do not copy donor four-drawer layout/knobs/footprint.
Canonical description: wood precisely cut into drawers on brass rails to house clothes. Keep source top rectangular recessed pull and two opposed lower curved pull motifs. Source has three stacked fronts, tiny feet, plain precise joinery. Gray front/case, pale cyan cap/feet only as ownership aid; both eventual native roles are w, not visible gold. Brass rails are internal closed-drawer metadata: do NOT draw gold bands, exposed sliding rails, clothing inventory or opened drawers. No mirror, knobs, ornate carving, props or additional compartments.
Preserve exact positions/scale/pivots and three equal panels. Keep rectified parallel cap edges, broad7.5depth side and full closed wood coverage. Do not reintroduce cap convergence, diagonal yaw, thin edge-on side or independently scaled views. Side/back plain panels with modest seams; no repeated front pulls. Refine restrained plank grain and shallow inset shading to match selected front body. Transparent exterior, no glow/shadow/backdrop/text/labels. No extra state/rotation mechanic or design alternatives.''',encoding='utf-8')
print('Retained dresser fronts/body, rectified cap material and authored complete cardinal end/back.')
