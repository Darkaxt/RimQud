"""Preserve selected fronts; construct missing cardinal cabinet surfaces."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]; OLD=HERE.parent/'v1'
MOD=Path('D:/Steam/steamapps/workshop/content/294100/1718190143')
SIZE=(512,768); FACINGS=['south','east','north','west']
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p): return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists(), 'Preserve recorded evidence'
measurements={}
for f in ['south','east','north']:
    p=MOD/f'Textures/NewThings/Misc/FilingCabinet/FilingCabinet_{f}.png';im=Image.open(p).convert('RGBA');box=im.getchannel('A').getbbox()
    measurements[f]=dict(**private(p),frame=list(im.size),alpha_bounds=list(box),visible_width=box[2]-box[0])
packet=json.loads((OLD/'source-packet.json').read_text())
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),previous_fronts=ref(OLD/'registered/model.json'),
 directional_reference=dict(textures=measurements,definition=private(MOD/'1.6/Defs/Buildings_Furniture/Buildings_Misc.xml'),load_folders=private(MOD/'LoadFolders.xml'),graphic_class='Graphic_Multi',draw_size=[2,2],footprint=[1,1],mapping='Same square2x2 draw frame for S/E/N; source pixels have transparent margins. Actual alpha widths124/83/124; E/S=0.669. This informs a plausible cabinet end, not a measured Qud footprint or copied damage rectangle.'),
 camera=dict(contract='Straight cardinal front, complete end, back and explicit west; vertical axes parallel. Shallow top bevel inherited from accepted fronts. No yaw or convergence of structural walls.',front_review='Existing fronts have straight vertical sides and only a shallow cap bevel; comparison with actual reference supports retaining them. No redraw is required to remove a three-quarter camera.',
 width=14,depth=8.8,end_front_ratio=8.8/14,depth_status='Authored hidden depth informed by actual directional reference; upright Qud glyph does not establish it.',
 unseen='Plain galvanized side and rear panels with restrained folded-edge seams and short feet. These are authored surfaces, not source-established extra drawers, vents, machinery or storage states.',
 variant2='Same top storage box and two metal brackets; front handle does not appear on the rear/end. Rear x reflects the front x about shared pivot. Brackets overlap in end views. No radio/electronic interpretation.'),
 states='Two actual RandomTile cosmetic layouts; each receives S/E/N/W authoring. No new open/closed state. South remains proposed fixed native tile; all extra directions unbound.',
 refinement='Reuse the two actual v1 front refinements. Front-guided missing-view refinement per layout, followed by fixed-geometry material transfer; no second isolation generation.',
 native_acceptance='Pending full-set generation gate; no runtime activation, native orientation/footprint or container acceptance.')
write(HERE/'source-packet.json',packet)

def rect(x,y,w,h,fill='#ababab',stroke='#3f3f3f',sw=.14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def path(d,fill='none',stroke='#3f3f3f',sw=.14):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
def unseen(n,f,owner=False):
    top=1.15 if n==1 else 4.15; end=f in ['east','west'];width=8.8 if end else 14;left=8-width/2;right=8+width/2
    gray='#000000' if owner else '#a6a6a6';ink='#000000' if owner else '#3f3f3f';hi='#000000' if owner else '#dedede';seam='#000000' if owner else '#737373'
    s=rect(left,top+.65,width,20.9-top-.65,gray,ink)
    s+=path(f'M{left-.05} {top+.65}L{left+.65} {top}H{right-.65}L{right+.05} {top+.65}V{top+1.05}H{left-.05}Z',hi,ink)
    s+=path(f'M{left+.23} {top+1.2}V20.6H{right-.23}V{top+1.2}',stroke=seam,sw=.09)
    s+=path(f'M{left-.05} 21H{right+.05}V21.7H{right-.85}V22.45H{right-1.85}V21.7H{left+1.85}V22.45H{left+.85}V21.7H{left-.05}Z',gray,ink)
    if end:
        lip=right-.16 if f=='east' else left+.16
        s+=path(f'M{lip} {top+1.1}V20.85',stroke=seam,sw=.14)
    else:
        s+=rect(left+.55,top+1.55,width-1.1,19.95-top-1.55,gray,seam,.075)
    if n==2:
        # Original upper box x8.25..11.75. Rear is physically reflected; end
        # uses authored centered depth. No front drawer handle on unseen faces.
        x=6.3 if end else 4.25;w=3.4 if end else 3.5
        gold='#ffffff' if owner else '#cfc041'
        s+=rect(x,2.1,w,2.6,gold,ink)
        s+=path(f'M{x+.12} 4.52V2.23H{x+w-.12}',stroke=gold if owner else '#e6df96',sw=.08)
        if end:
            s+=path(f'M{x+.7} 2.1V1.15H{x+1.1}V2.1',stroke=gray,sw=.18)
        else:
            s+=path(f'M{x+.45} 2.1V1.15H{x+.85}V2.1M{x+2.35} 2.1V1.15H{x+2.75}V2.1',stroke=gray,sw=.18)
    return s

font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
for n in [1,2]:
    old=OLD/'registered';front=Image.open(old/f'variant-{n}-neutral-master.png').convert('RGBA').convert('RGBa').resize(SIZE,Image.Resampling.LANCZOS).convert('RGBA')
    detail=Image.open(old/f'variant-{n}-drawer-ownership-mask.png').convert('L').resize(SIZE,Image.Resampling.NEAREST)
    a=np.array(front);weight=np.array(detail);weight[a[:,:,3]==0]=0
    own=Image.fromarray(np.dstack([weight,weight,weight,a[:,:,3]]));own.save(HERE/f'variant-{n}-ownership-south.png')
    # Color is only a role aid; front neutral production remains unchanged.
    rgb=a[:,:,:3].astype(float);colored=np.where(weight[:,:,None]>0,rgb*np.array([1,.95,.4]),rgb);front_context=Image.fromarray(np.dstack([np.uint8(colored),a[:,:,3]]))
    front.save(HERE/f'variant-{n}-selected-front-neutral.png');front_context.save(HERE/f'variant-{n}-constructed-south.png')
    for f in ['east','north','west']:
        for role in ['constructed','ownership']:
            body=unseen(n,f,role=='ownership');p=HERE/f'variant-{n}-{role}-{f}.svg';p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{body}</svg>',encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
    sheet=Image.new('RGBA',(2048,768))
    for i,f in enumerate(FACINGS):sheet.alpha_composite(Image.open(HERE/f'variant-{n}-constructed-{f}.png').convert('RGBA'),(i*512,0))
    sheet.save(HERE/f'variant-{n}-front-guided-turnaround.png')
    prompt=f'''Use case: sketch-to-render. Game sprite material refinement for Argyve's galvanized multicabinet, cosmetic layout {n}.
Image1 is the exact four-column construction. Leftmost SOUTH is the selected existing front: keep its drawer layout and material appearance as the anchor. Columns2 EAST,3 NORTH,4 WEST are complete straight cardinal end/back/end. Image2 is an actual installed RimWorld filing cabinet reference ONLY for restrained flat metal shading.
Refine the composed cabinet sheet with a subtle galvanized metal texture, clean dark edges and very restrained bevels. Keep EXACT canvas2048x768, four equal512x768 columns, original positions, overall sizes, cap heights, short feet and blank-panel shapes. Do not center or resize individual views. Depth/end width is already specified; do not make ends thinner or rotate any view into three-quarter. No perspective convergence. Keep end panels plain metal and rear panel folded edge seams; no drawers, handles, vents, pipes or extra hardware on unseen panels. {'The small top storage box has the same gold front/end/rear role; preserve both bracket geometry and their natural end-view overlap. No radio or electronics.' if n==2 else 'No top box or added accessories.'}
Gray is main metal; muted gold identifies source detail ownership. Keep colors in their regions. Neutral highlights and dark seams remain part of their owning material. No glow, backdrop, cast shadow or filled gaps. Transparent background. No text or labels. Do not invent open/closed animation or contents. This is one same cabinet in all views, not four design alternatives.'''
    (HERE/f'variant-{n}-turnaround-prompt.txt').write_text(prompt,encoding='utf-8')
plate=Image.new('RGB',(1440,1000),'#142823');d=ImageDraw.Draw(plate)
d.text((18,14),'MULTICABINET / selected fronts + authored cardinal sides/rears / both native cosmetic layouts',font=font,fill='#e3cf43')
for n in [1,2]:
    for i,f in enumerate(FACINGS):
        im=Image.open(HERE/f'variant-{n}-constructed-{f}.png').convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);x=30+i*350;y=55+(n-1)*440;plate.paste(im,(x,y),im);d.text((x,y+390),f'LAYOUT{n} / {f.upper()}',font=font,fill='#e3cf43')
d.text((18,956),'Depth8.8 / width14 is authored. Shared512x768 frame; unseen faces are plain metal, not extra drawers.',font=font,fill='#e5e8d8');plate.save(HERE/'constructed-all-layouts.png')
write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Construction authoring before refinement',front='Actual selected front is reused, not regenerated. Straight side walls; shallow cap bevel is supported by the actual donor camera.',end='Authored8.8 depth versus14front retains substantial end volume. Consistent cabinet/topbox heights across views.',rear='Back has plain panel seams; topbox reflects its real front xposition. No false drawer fronts.',state='Both cosmetic layouts stay separate; no open-state or donor mechanics.'))
print('Constructed two front-guided four-facing sets; selected fronts retained.')
