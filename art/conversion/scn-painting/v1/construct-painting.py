"""Construct both native Painting designs in a shared physical easel frame."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
source=read(HERE/'native-state-index.json'); ledger=read(ROOT/'evidence/conversion-ledger.json');entry=next(e for e in ledger['entries'] if e['id']=='SCN-PAINTING')
assert ledger['active_entry']=='SCN-PAINTING' and not (HERE/'construction-controls.json').exists()
W,H,S=512,768,32; E=math.radians(14)
def project(p,f):
    x,y,z=p
    if f=='north':x,y=-x,-y
    elif f=='east':x,y=y,-x
    return (256+x*S,712+(y*math.sin(E)-z*math.cos(E))*S)
def coords(ps,f):return ' '.join('%.3f,%.3f'%project(p,f) for p in ps)
def polygon(ps,f,fill,stroke='#262a29',width=3):return f'<polygon points="{coords(ps,f)}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>'
def beam(a,b,w,f,fill='#999b96',width=3):
    # A rectangular support in its own vertical plane; physical cross-section retained.
    dx,dy,dz=np.array(b)-a; length=math.hypot(dx,dz)
    if length>0.01: off=np.array([dz,0,-dx])*w/(2*length)
    else:off=np.array([w/2,0,0])
    return polygon([np.array(a)-off,np.array(b)-off,np.array(b)+off,np.array(a)+off],f,fill,width=width)
def plane(x,z,yoff=0):return (x,0.8-.065*z+yoff,z)
def box(w,z0,z1,f,front=False):
    # Stretched linen over a shallow stretcher: thickness .36 source units.
    a,b,c,d=[plane(x,z,.18 if front else -.18) for x,z in [(-w/2,z0),(w/2,z0),(w/2,z1),(-w/2,z1)]]
    return [a,b,c,d]
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
controls=dict(frame=[W,H],contact=[256,712],pixels_per_source_unit=S,source_cell=[16,24],camera_elevation_degrees=14,
    dimensions=dict(front_foot_span=11.6,depth=5.6,canvas_thickness=.36,leg_thickness=.52,source_unit_in_cells=1/16),
    provenance='Canvas aspect/height, ledge, spreading legs and abstract two-role motifs follow each native tile. Hidden easel depth, tilt, stretcher and rear brace are authored estimates. Actual Lectern Graphic_Multi drawSize/size1x1 is rendering context only; no donor ratio copied.',
    depth_contract='Front feet y=1, rear foot y=-4.6; shared14-degree shallow map-camera, not edge-on elevations. Profile retains tilted panel thickness and spread stand. No independent bounds fit or side compression.',states=[])
for i,s in enumerate(source['states']):
    a=np.array(Image.open(s['private_mask']['path']).convert('RGBA'))
    # Tile1 canvas landscape; tile2 taller portrait canvas. Pixel motifs remain abstract.
    x0,x1,y0,y1=(2,14,4,12) if i==0 else (3,13,2,13)
    cw=x1-x0-.25; z0=22-y1; z1=22-y0; slug=f'design-{i+1}'
    state=dict(id=slug,native_tile=s['native_tile'],canvas_width=cw,canvas_height=z1-z0,canvas_z=[z0,z1],motif='Source primary/detail/negative image-space arrangement; no inferred representational subject.',views={})
    for facing in ['south','east','north']:
        groups={'stand':[],'linen':[],'primary_paint':[],'detail_paint':[]}
        # Back support is physically behind the front frame, and visible in the reverse.
        rear=beam((0,-4.6,0),(0,-.35,18.5),.65,facing,'#8d908a')
        brace=beam((-3.4,.4,5.5),(3.4,.4,5.5),.48,facing,'#a1a39e')
        frontlegs=''.join(beam((side*5.8,1,0),(side*3.2,.1,10),.54,facing,'#aaa9a0') for side in [-1,1])
        mast=beam((0,-.1,5),(0,-.6,z1+1.5),.65,facing,'#aaa9a0')
        stand=rear+brace+frontlegs+mast
        groups['stand'].append(stand)
        # Reverse has canvas back + stretcher, never a mirrored copy of the painted face.
        face=polygon(box(cw,z0,z1,facing,True),facing,'#c6c6bd')
        back=polygon(box(cw,z0,z1,facing),facing,'#b8b9b0')
        edge=polygon([plane(cw/2,z0,-.18),plane(cw/2,z0,.18),plane(cw/2,z1,.18),plane(cw/2,z1,-.18)],facing,'#94978e',width=2)
        if facing=='south':
            groups['linen'].append(face)
            # Negative pixels become dark painted image space, not physical holes through linen.
            groups['primary_paint'].append(polygon(box(cw-.35,z0+.17,z1-.17,facing,True),facing,'#666e69',stroke='none',width=0))
            for yy in range(y0,y1):
                for xx in range(x0,x1):
                    p=a[yy,xx]
                    if not p[3]:continue
                    xx0=(xx-x0)/(x1-x0)*(cw-.36)-(cw-.36)/2;xx1=(xx+1-x0)/(x1-x0)*(cw-.36)-(cw-.36)/2
                    zz1=z1-.18-(yy-y0)/(y1-y0)*(z1-z0-.36);zz0=z1-.18-(yy+1-y0)/(y1-y0)*(z1-z0-.36)
                    role='detail_paint' if p[0]>=128 else 'primary_paint'
                    groups[role].append(polygon([plane(x,z,.19) for x,z in [(xx0,zz0),(xx1,zz0),(xx1,zz1),(xx0,zz1)]],facing,'#bdbeb4' if role=='detail_paint' else '#dfdfd3',stroke='none',width=0))
            # Discrete oil drips reach the support ledge, tied to each actual detail region.
            for dx in ([-3.8,3.8] if i==0 else [-3.6,2.7]):
                groups['detail_paint'].append(beam(plane(dx,z0+.2,.21),plane(dx,z0-.35,.21),.10,facing,'#bdbeb4',width=0))
        elif facing=='east':
            # A planar canvas genuinely has a thin edge; the full stand retains depth.
            groups['linen'].append(edge)
            groups['stand'].append(beam((0,-4.2,1),(0,.3,8.4),.38,facing,'#aaa9a0',width=2))
        else:
            groups['linen'].append(back)
            stretcher=''.join(beam(plane(x,z,-.21),plane(x2,z2,-.21),.35,facing,'#92978e',width=2) for x,z,x2,z2 in [(-cw/2+.4,z0+.4,cw/2-.4,z0+.4),(-cw/2+.4,z1-.4,cw/2-.4,z1-.4),(-cw/2+.4,z0+.4,-cw/2+.4,z1-.4),(cw/2-.4,z0+.4,cw/2-.4,z1-.4)])
            groups['linen'].append(stretcher)
            groups['linen'].append(beam(plane(0,z0-.7,-.5),(0,-4.6,0),.65,facing,'#8d908a'))
        # The shelf projects .8 units beyond both edges, preserving native width relationship.
        shelf_w=12.8 if i==1 else 10.8
        shelf=[(-shelf_w/2,1.2,z0-.7),(shelf_w/2,1.2,z0-.7),(shelf_w/2,.1,z0-.7),(-shelf_w/2,.1,z0-.7)]
        groups['detail_paint'].append('')
        shelf_art=polygon(shelf,facing,'#b4b6ac',width=2)+beam((-shelf_w/2,1.2,z0-1),(shelf_w/2,1.2,z0-1),.40,facing,'#92978e',width=2)
        groups['linen'].append(shelf_art)
        order=['stand','linen','primary_paint','detail_paint']
        content=''.join(f'<g id="{k}">{"".join(groups[k])}</g>' for k in order)
        base=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{{}}</svg>'
        svg=HERE/f'{slug}-{facing}.svg';svg.write_text(base.format(content),encoding='utf-8');png=svg.with_suffix('.png');png.write_bytes(svg_to_bytes(svg_string=svg.read_text()))
        # Parallel ownership masks from the same projected geometry, never AI segmentation.
        for role in ['stand','linen','detail_paint']:
            fragment=''.join(groups[role]);fragment=__import__('re').sub(r'fill="[^"]+"','fill="white"',fragment);fragment=__import__('re').sub(r'stroke="[^"]+"','stroke="white"',fragment)
            (HERE/f'{slug}-{facing}-{role}-mask.png').write_bytes(svg_to_bytes(svg_string=base.format(fragment)))
        state['views'][facing]=dict(svg=ref(svg),constructed=ref(png),ownership={role:ref(HERE/f'{slug}-{facing}-{role}-mask.png') for role in ['stand','linen','detail_paint']})
    controls['states'].append(state)
write(HERE/'construction-controls.json',controls)
sheet=Image.new('RGBA',(1536,1536));d=ImageDraw.Draw(sheet)
for i,state in enumerate(controls['states']):
    for j,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(ROOT/state['views'][f]['constructed']['path']).convert('RGBA'),(j*512,i*768))
sheet.save(HERE/'constructed-turnarounds.png')
plate=Image.new('RGB',(1536,1640),'#142823');plate.paste(sheet,(0,50),sheet);d=ImageDraw.Draw(plate)
d.text((20,12),'PAINTING / two actual designs / SOUTH - EAST - NORTH / shared physical frame',font=font,fill='#e3cf43')
for i in range(2):
    for j,f in enumerate(['south','east','north']):d.text((j*512+20,i*768+770),f'DESIGN {i+1} / {f.upper()}',font=font,fill='#e3cf43')
plate.save(HERE/'manual-suggestion.png')
prompt='''Use case: game-asset material refinement, not redesign.
Input1 is the authoritative editable construction: two rows are two native Caves of Qud Painting designs, columns SOUTH(front), EAST(right profile), NORTH(back). Refine every view as the same corresponding physical easel. Input2 is the original native silhouettes/palette-mask designs and ACTUAL installed Vanilla Textures Expanded Lectern references: only quiet line/material/map-camera conventions; do not turn the easel into a lectern.
Qud description: Nacreous oil wets the ecru linen and has dripped onto the easel. From the plane of the canvas, an image is pressed out. No image subject is specified. Keep the source abstract paint shapes, not a landscape, portrait or lettering. First canvas is landscape, second canvas is portrait. Keep each design distinct.
Retain SOUTH straight front, EAST straight profile and NORTH straight back, common shallow map-camera elevation14 degrees. Common source-unit scale32pixels, frame512x768 per view, contact(256,712). Physical stand: front foot span11.6source units, front/rear depth5.6, legs.54thick, canvas thickness.36. First canvas width11.75height8, z10..18; second width9.75height11,z9..20. Rear support foot y=-4.6, front feet y=1. No independent side-view compression, perspective turntable, panel-bounds fitting or inflated profile canvas: it is planar while the complete leaning easel stand has real depth. Copy the fixed input geometry and preserve gaps between legs.
Only improve restrained neutral linen weave, nacreous oil surface and wooden supports, simple clean outlines and quiet broad shading readable at map scale. Grayscale only: no baked brown wood, red painting or added coloured frame. The source primary/detail regions will be separately tinted by native palettes later. Keep reverse unpainted with stretcher and rear brace; NEVER show the front motif through the back or profile. Do not add paint pots, chair, scenery, floor, lettering, cast shadow or border. Transparent background. Keep six isolated complete objects in the same2x3 grid with transparent margins, no generated labels. Preserve proportions and physical component attachments. No glowing/oily photoreal render. Material refinement is the output purpose; original editable geometry remains authoritative.'''
(HERE/'refinement-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
def event(step,action,outs,review):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'source-reference.png')],outputs=[ref(HERE/n) for n in outs],review=review,result='PASS'))
event(entry['required_steps'][1],'Inspect actual Qud designs and installed Lectern S/E/N reference; record narrow visual-only role and source colour precedence.',['construction-controls.json'],'Actual Lectern has quiet rectangular panels/supports and a sloping directional profile. Its Graphic_Multi/1x1 frame is not a target easel ratio. Low nonzero background alpha in donor PNGs is reference-only; no donor coverage imported. No close whole easel equivalent.')
event(entry['required_steps'][2],'Build editable projected easels with native landscape/portrait canvas shapes and source-bound abstract paint regions.',['construct-painting.py','manual-suggestion.png','constructed-turnarounds.png','refinement-prompt.txt'],'Shared width/depth/camera/component thickness carried into exact prompt. Negative source image pixels interpreted as dark painted space on continuous linen, not physical holes. Hidden stand/stretcher are explicitly authored. Original P/D motif layout preserved.')
event(entry['required_steps'][3],'Construct complete S/E/N variants of both actual tile choices, keeping reverse unpainted and projected stand depth.',['construction-controls.json']+[f'design-{i}-{f}.svg' for i in [1,2] for f in ['south','east','north']],'Extra cardinal views are unbound authoring, not native rotation. Common frame/pivot/scale; planar canvas edge remains thin, while stand has5.6unitsdepth. All geometry awaits pre-refinement visual inspection.')
entry.update(current_step=entry['required_steps'][4],known_issues=['Inspect all six constructed views and correct structural issues before actual refinement. No generation-ready credit.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Built two source-bound paintings, six editable cardinal views, masks and exact refinement prompt.')
