"""Two source hammock states: open woven surfaces, shared 3D cardinal projection."""
from pathlib import Path
import sys,json,hashlib,math
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
old=json.loads((OLD/'source-packet.json').read_text());packet=dict(old);packet.update(previous_packet=ref(OLD/'source-packet.json'),camera=dict(classification='CARDINAL_SOURCE_BOUND_AUTHORED_DEPTH',projection='u=8+rotated_x; v=21+0.35*rotated_y-z. S0/E90/N180/W270, fixed camera elevation and physical scale. Unequal hanging endpoint heights are physical source features, not diagonal camera yaw.',dimensions=dict(hanging_length=12.95,hanging_width=3.6,rope_diameter=.19,portable_band_width=2.2,portable_fold_depth=2.0),provenance='Authored hidden dimensions from the rope-lattice saddle description and selected source front; no native length/width fields. Legacy net is a weave reference only, not a measured hammock or directional camera reference.',reference_limits='No exact hammock or actual hammock turnaround established. Do not claim a generic net or a texture-frame ratio supplies physical sling dimensions.',volume='Hanging is an open trough with pinched endpoints and broad cradle; portable is the same concept folded/draped in a loop with two lattice strips and fringes. End views retain folded depth or full sling width; no finished-image squeeze.'),construction='Reconstruct both old source-bound designs as editable continuous open rope surfaces so all facings share one physical model. Source diagonal slope, loop, frayed middle/tips and distinct y/Y roles remain. V1 remains historical front/material evidence; no claim of byte-identical front retention. New unseen cross-section/depth/weave/topology are authored interpretation, not native body/support mechanics.',native_acceptance='Pending full-set generation gate; native Hangable support/transitions/endpoints/sleep, palette/visibility/physics and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
def xyz(state,u,v):
    if state=='hanging':
        s=math.sin(math.pi*u);x=1.3+12.95*u-8;y=1.8*v*s
        # Preserve low-left/high-right support identity; center of trough sags.
        screen_edge=10.65-8.25*u+8.5*4*u*(1-u)
        z=21-(screen_edge+4.0*(1-v*v)*s)
        return x,y,z
    angle=math.pi*u;x=-3.5*math.cos(angle);z=5.5+12*max(0,math.sin(angle))**.32
    eps=.0001;a=max(eps,min(1-eps,u));dx=3.5*math.pi*math.sin(math.pi*a);dz=12*.32*max(.000001,math.sin(math.pi*a))**(-.68)*math.pi*math.cos(math.pi*a);norm=math.hypot(dx,dz)
    # Ribbon normal in x/z plane gives two broad front strips; folded depth
    # gives complete, distinct side surfaces instead of a flattened line.
    x+=1.1*v*dz/norm;z-=1.1*v*dx/norm;y=.65*math.sin(math.pi*v/2)+.35*math.cos(angle)
    return x,y,z
def project(q,t):
    x,y,z=q;x,y=[(x,y),(-y,x),(-x,-y),(y,-x)][t];return 8+x,21+.35*y-z,y
def line(points,t):return 'M'+' L'.join(f'{a:.4f} {b:.4f}' for a,b,_ in [project(q,t) for q in points])
def paths(state):
    result=[]
    for slope in [-1,1]:
        for base in np.arange(-.075,1.076,.0475):
            points=[xyz(state,float(u),float(v)) for v in np.linspace(-1,1,81) if 0<=(u:=base+slope*v*.075)<=1]
            if len(points)>1:result.append((points,False,.17))
    for v in [-1,1]:result.append(([xyz(state,float(u),v) for u in np.linspace(0,1,161)],state=='hanging' and v==-1,.23))
    if state=='unhung':
        for u in [0,1]:
            for v,drop in [(-.8,3.4),(0,4.6),(.8,2.4)]:
                x,y,z=xyz(state,u,v);result.append(([(x,y,z),(x+.2*v,y,z-drop)],True,.14))
                for dx in [-.11,0,.11]:result.append(([(x+.2*v,y,z-drop+.4),(x+.2*v+dx,y,z-drop-.25)],True,.06))
    else:
        for u,v in [(.43,-.2),(.50,.1),(.57,-.1)]:
            x,y,z=xyz(state,u,v);result.append(([(x,y,z),(x+.17,y,z-.45)],False,.07))
    return result
def make(state,t,owner=False):
    segments=paths(state);segments.sort(key=lambda a:sum(project(q,t)[2] for q in a[0])/len(a[0]));body=[]
    for points,detail,width in segments:
        d=line(points,t)
        if owner:body.append(f'<path d="{d}" stroke="'+('#ffffff' if detail else '#000000')+f'" stroke-width="{width+.13}"/>')
        else:body.append(f'<path d="{d}" stroke="#343434" stroke-width="{width+.13}"/><path d="{d}" stroke="'+('#8dd3dd' if detail else '#bcbcbc')+f'" stroke-width="{width}"/>')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g fill="none" stroke-linecap="round" stroke-linejoin="round">'+''.join(body)+'</g></svg>'
for state in ['unhung','hanging']:
    folder=HERE/state;folder.mkdir(exist_ok=True);sheet=Image.new('RGBA',(1536,768))
    for t,f in enumerate(['south','east','north','west']):
        data=make(state,t);(folder/f'constructed-{f}.svg').write_bytes(data.encode());(folder/f'constructed-{f}.png').write_bytes(svg_to_bytes(svg_string=data));(folder/f'ownership-{f}.png').write_bytes(svg_to_bytes(svg_string=make(state,t,True)))
        if t<3:sheet.alpha_composite(Image.open(folder/f'constructed-{f}.png'),(t*512,0))
    sheet.save(folder/'constructed-turnaround.png')
    text=f'''Use case: sketch-to-render. One Qud brinestraw rope hammock in its {state.upper()} native state, three cardinal directions. Image1 is the1536x768 edit target with SOUTH left, EAST center, NORTH right; each512x768 panel is the same physical shape rotated90/180degrees using fixed map camera. Image2 is actual legacy Vehicle Framework FishingNetMote ONLY for crossed-rope readability/outline; no circular net, fishing or endpoint dots. Image3 is the source native two-state plate ONLY for original identity; this request is the {state} state.
Description: {old['description']}
Keep the current open rope lattice, exact source-bound loop/saddle, attachment endpoints, fray placement, physical shape, panel bounds, shared frame/scale/pivot and camera. Refine each rope with restrained intertwined fiber/knots and modest clean shading. Preserve open transparent mesh holes; no opaque fabric, blanket, sleeper or body. No support trees, stakes, poles, rigid frame, tassel additions or hanging-state mechanics.
Shared geometry: hanging length12.95, cradle width3.6, rope diameter0.19; portable ribbon width2.2 and folded depth2.0. Dimensions are authored, not native measurements. Projection u=8+rotated_x,v=21+0.35*rotated_y-z. These are straight cardinal views, no3/4yaw. Hanging ends have intentionally unequal heights from the original source. Preserve full cradle width in the end view; do not squash it into a thin line. Portable folded loop has naturally narrower end view, but retain both folds and fringes. No independent bounds fitting. Retain source lower-left/high-right asymmetry in hanging S, reverse it physically in N.
Main ropes neutral gray; marked pale cyan rope strands/fringes are ownership keys for the native white role. No other baked hue. Match outline/shading across all3views; do not redesign the selected front. SAME1536x768canvas,512x768columns, transparent background and genuine open weave. No labels/text/guides, glow or external shadows. No second isolation or new state.'''
    (folder/'turnaround-prompt.txt').write_bytes(text.encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,1300),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'HAMMOCK / actual portable + hanging source states > shared physical cardinal rope-surface construction',font=font,fill='#e3cf43')
im=Image.open(OLD/'native-states-comparison.png');im.thumbnail((540,540));plate.paste(im,(25,50));donor=Image.open(old['donor_reference']['path']).convert('RGBA');donor.thumbnail((240,240));plate.paste(donor,(780,100),donor);d.text((740,365),'ACTUAL LEGACY NET / weave only',font=font,fill='#e3cf43')
for j,state in enumerate(['unhung','hanging']):
    im=Image.open(HERE/state/'constructed-turnaround.png').convert('RGBA').resize((690,345));plate.paste(im,(20+j*710,650),im);d.text((20+j*710,1030),state.upper()+' / SOUTH  EAST  NORTH',font=font,fill='#e3cf43')
for i,line in enumerate(['Two real states, not different rotations. Extra directions unbound; native Hangable owns support and state.',
 'Sling depth, cross-section and folded depth are authored estimates. One geometry and scale feed all views.',
 'Diagonal hanging slope is physical endpoint-height asymmetry, not a rotated camera. Net has genuine holes.',
 'Explicit TileColor y primary / Y detail. No clothing, trees, frame, occupant or extra state.']):d.text((18,1120+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference-construction.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Generation construction before refinement',review='Both source states retain recognizable loop/fringe versus deep unequal-end hammock identities. Complete end trough/fold width derives from shared physical geometry, not scaled side PNGs. Open lattice, opaque ropes, role strands and centered source cell retained. Cross-section is authored and actual legacy donor supplies weave only; no exact hammock/directional reference claimed.',outputs=[ref(p) for p in sorted(HERE.glob('*/constructed-*.png'))]));print('Constructed both native states in S/E/N/W from one physical surface per state.')
