"""Project one physical short wood/iron holder into coherent furniture facings."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];INPUT=HERE.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'construction-controls.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-TORCHPOST';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
ANGLE=math.radians(14);SCALE=32;BASE=672-.6*math.sin(ANGLE)*SCALE
def project(p,f):
    x,y,z=p
    if f=='east':x,y=y,-x
    elif f=='north':x,y=-x,-y
    return (256+x*SCALE,BASE+y*math.sin(ANGLE)*SCALE-z*math.cos(ANGLE)*SCALE)
def points(ps,f):return ' '.join('%.3f,%.3f'%project(p,f) for p in ps)
def polygon(ps,f,fill,stroke='#303534',width=2.5):return f'<polygon points="{points(ps,f)}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>'
def solid_beam(a,b,width,f,fill):
    a=np.array(a,dtype=float);b=np.array(b,dtype=float);axis=b-a;axis/=np.linalg.norm(axis);n=np.cross(axis,[0,1,0])
    if np.linalg.norm(n)<1e-5:n=np.cross(axis,[1,0,0])
    n=n/np.linalg.norm(n)*width/2;m=np.cross(axis,n);ps=sorted(set(project(end+s*n+t*m,f) for end in [a,b] for s in [-1,1] for t in [-1,1]))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];hi=[]
    for p in ps:
        while len(lo)>1 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    for p in reversed(ps):
        while len(hi)>1 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    xy=' '.join('%.3f,%.3f'%p for p in lo[:-1]+hi[:-1]);return f'<polygon points="{xy}" fill="{fill}" stroke="#303534" stroke-width="2.5" stroke-linejoin="round"/>'
def path(ps,f):return 'M'+'L'.join('%.3f %.3f'%project(p,f) for p in ps)+'Z'
base='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 512 768">{}</svg>'
controls=dict(frame=dict(native=[16,24],master=[512,768],recipient=[256,256],pivot=[8,12],body_contact_y=21,policy='Shared full source-cell mapping; body remains at bottom-cell x4..12,y16..21 region with upper cell transparent for retained native prefab. No per-view bounds fitting or moving flame origin.'),
    physical_dimensions=dict(rim_width=7.5,rim_depth=3.2,rim_height=.30,rim_top_z=4.6,wood_stem_width=1.7,wood_stem_depth=1.2,wood_stem_height=2.5,strut_thickness=.32,pixels_per_source_unit=32,camera_elevation_degrees=14,projection_baseline=BASE),
    provenance='Source supports broad rim, short central stem, flanking support marks, wood+iron and bottom-cell position. Rectangular open rim depth, solid square-section struts, back and material subdivisions are authored estimates, not source-measured unseen geometry. Core WallTorch S/E/N guides cardinal wood-end/light shading only; no donor wall offset or footprint copied.',
    native_roles='Every new holder pixel remains detail w; wood/iron are authored material ownership for shading, not separate native tints. No static flame or primary R/W/r art.',views={})
for f in ['south','east','north']:
    # Short wood block, with its top/back/side faces projected from one physical box.
    wood=polygon([(-.85,.6,0),(.85,.6,0),(.85,.6,2.5),(-.85,.6,2.5)],f,'#b1b1b1')
    wood+=polygon([(-.85,-.6,0),(-.85,.6,0),(-.85,.6,2.5),(-.85,-.6,2.5)],f,'#8e8e8e')
    wood+=polygon([(.85,-.6,0),(.85,.6,0),(.85,.6,2.5),(.85,-.6,2.5)],f,'#999999')
    wood+=polygon([(-.85,-.6,2.5),(.85,-.6,2.5),(.85,.6,2.5),(-.85,.6,2.5)],f,'#cccccc')
    wood+=polygon([(-.85,-.6,0),(.85,-.6,0),(.85,-.6,2.5),(-.85,-.6,2.5)],f,'#a4a4a4')
    # Three solid supports retain thickness in profile; rear support changes occlusion naturally.
    iron=''
    supports=[((0,-.35,2.2),(0,-1.43,4.45)),((-.55,.30,2.2),(-2.9,1.43,4.45)),((.55,.30,2.2),(2.9,1.43,4.45))]
    if f=='north':supports=list(reversed(supports))
    for start,end in supports:iron+=solid_beam(start,end,.32,f,'#a0a0a0')
    # The open iron rim is a real physical rectangle, not an independently narrowed end view.
    outer=[(-3.75,-1.6,4.6),(3.75,-1.6,4.6),(3.75,1.6,4.6),(-3.75,1.6,4.6)]
    inner=[(-3.38,-1.23,4.6),(3.38,-1.23,4.6),(3.38,1.23,4.6),(-3.38,1.23,4.6)]
    # Visible vertical rim face chosen from the facing, using shared dimensions.
    if f=='south':side=[(-3.75,1.6,4.30),(3.75,1.6,4.30),(3.75,1.6,4.6),(-3.75,1.6,4.6)]
    elif f=='north':side=[(-3.75,-1.6,4.30),(3.75,-1.6,4.30),(3.75,-1.6,4.6),(-3.75,-1.6,4.6)]
    else:side=[(3.75,-1.6,4.30),(3.75,1.6,4.30),(3.75,1.6,4.6),(3.75,-1.6,4.6)]
    iron+=polygon(side,f,'#888888')
    iron+=f'<path d="{path(outer,f)} {path(list(reversed(inner)),f)}" fill="#c8c8c8" fill-rule="evenodd" stroke="#303534" stroke-width="2.5" stroke-linejoin="round"/>'
    svg=HERE/f'holder-{f}.svg';svg.write_text(base.format(f'<g id="wood">{wood}</g><g id="iron">{iron}</g>'),encoding='utf-8');png=svg.with_suffix('.png');png.write_bytes(svg_to_bytes(svg_string=svg.read_text()))
    import re
    masks={}
    for role,fragment in [('wood',wood),('iron',iron)]:
        fragment=re.sub(r'(fill|stroke)="(?!none)[^"]+"',lambda m:m.group(1)+'="white"',fragment);p=HERE/f'{role}-{f}-ownership.png';p.write_bytes(svg_to_bytes(svg_string=base.format(fragment)));masks[role]=ref(p)
    controls['views'][f]=dict(svg=ref(svg),constructed=ref(png),material_ownership=masks)
write(HERE/'construction-controls.json',controls)
turn=Image.new('RGBA',(1536,768))
for j,f in enumerate(['south','east','north']):turn.alpha_composite(Image.open(HERE/f'holder-{f}.png').convert('RGBA'),(j*512,0))
turn.save(HERE/'constructed-turnarounds.png')
# Presentation crop is explicit; production keeps the complete original cell/pivot.
turn.crop((0,480,1536,720)).save(HERE/'refinement-target.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1536,800),'#142823');plate.paste(turn,(0,0),turn);d=ImageDraw.Draw(plate);d.text((20,18),'TORCHPOST / holder ONLY / SOUTH - EAST - NORTH / fixed bottom-cell placement',font=font,fill='#e3cf43')
for j,f in enumerate(['south','east','north']):
    d.rectangle((j*512+128,16*32,j*512+384,21*32),outline='#776d31',width=1);d.text((j*512+20,720),f.upper()+' / shared depth3.2',font=font,fill='#e3cf43')
d.text((20,770),'Upper space remains transparent for native TorchpostFlames. Gold box is native holder bbox, never production art.',font=font,fill='#e5e8d8');plate.save(HERE/'manual-suggestion.png')
prompt='''Use case: restrained RimWorld-style material refinement of Qud furniture support, NO FIRE.
Image1 shows THREE flame-free holder views in a cropped presentation strip: SOUTH/front, EAST/right profile, NORTH/back, left to right. The strip is a documented crop of the bottom of three512x768source-cell frames; it is NOT permission to enlarge the production sprite. Image2 is the original Qud mask/palette and actual Core WallTorch S/E/N material references. Do not copy the donor's narrow wood torch silhouette or flame.
Subject is Qud Torchpost, display torch sconce: description A brightly burning handfire hangs across wood and iron. The fire is already a separate native TorchpostFlames particle prefab and MUST NOT appear in this drawing. Refine ONLY the small wood-and-iron holder: wide open iron rim, three supporting struts, short central wooden stem. No tall pole, wall plaque, fuel, brazier bowl fill, logs, candles, torch bundle or light source added.
Shared physical dimensions in source-pixel units: rim width7.5, depth3.2, topheight4.6, thickness.30; stem width1.7,depth1.2,height2.5; solid strut thickness.32; shallow cardinal map-camera elevation14degrees. Preserve exactly the three views of this same construction, with coherent depth and volume. Side is naturally depth3.2 rather than a thin flat line; do not compress it independently or turn camera to three-quarter/isometric. Back retains same parts, with rear strut occlusion. Keep actual open rim and gaps between supports transparent.
Neutral grayscale ONLY. Wood and iron differ by broad restrained shading/grain, not baked brown/grey native palettes; all static holder pixels later use Qud detail w. Keep neutral smooth clean outlines, simple broad material shading readable at map scale. No red/yellow/orange fire, glow, smoke, sparks, soot cloud, halo or cast shadow. No extra angles, labels, scene, wall or background. Output three complete holders in the same horizontal order, with true transparent background/holes and margins.
The canonical manual frame/pivot/geometry and native particle origin remain authoritative. Only subtle material refinement is requested; no new light mechanics, animation clock, wall placement offset or independent resizing.'''
(HERE/'refinement-prompt.txt').write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
def event(step,action,outs,review):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(INPUT/'source-packet.json'),ref(INPUT/'source-reference.png')],outputs=[ref(HERE/n) for n in outs],review=review,result='PASS'))
event(entry['required_steps'][1],'Inspect actual Core WallTorch S/E/N textures and inherited Graphic_Multi wall mapping as narrow material/camera reference.',['construction-controls.json'],'Actual Core torch supplies cardinal wood-end and restrained edge rendering, not a whole broad Qud holder equivalent. No donor wall offsets, glow radius, fuel/heat logic, height or slender silhouette imported.')
event(entry['required_steps'][2],'Construct short wood/iron holder with one shared rim depth, solid supports and fixed native bottom-cell placement.',['construct-holder.py','manual-suggestion.png','constructed-turnarounds.png','refinement-target.png','refinement-prompt.txt'],'Source broad rim/stem/support marks retained. Depth/back/strut geometry are authored estimates; all holder pixels remain detail w. Upper cell stays transparent for unchanged native flame prefab. Manual full frame and explicit crop retained; initial struts ended inside the open rim; corrected endpoint centres now lie within the iron rim volume at y=+/-1.43,z4.45, retaining all dimensions. Inspect revised full views before actual refinement.')
event(entry['required_steps'][3],'Generate required S/E/N furniture construction and preserve native effect/state ownership.',['construction-controls.json']+[f'holder-{f}.svg' for f in ['south','east','north']],'All three views share width7.5/depth3.2/camera14deg and stem/strut dimensions. No independent side compression. Extra facings unbound; native fixed tile/particle/light controls unchanged. Unlit Torchpost remains separate blueprint, not invented toggle or acceptance credit.')
entry.update(current_step=entry['required_steps'][4],known_issues=['Inspect all three shared-geometry holder views and native bounds, then actual refinement without flame or donor placement.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Built coherent S/E/N short holder with explicit crop, full native frames and no flame art.')
