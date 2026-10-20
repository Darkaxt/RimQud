"""Shared source steel bench, physical empty/end volume and separate occupied marks."""
from pathlib import Path
import sys,json,hashlib,xml.etree.ElementTree as ET
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');SCALE=.95;K=3.4/7.6
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def normalize(im):return im.convert('RGBa').transform((512,768),Image.Transform.AFFINE,(1/SCALE,0,256-256/SCALE,0,1/SCALE,512-512/SCALE),Image.Resampling.BICUBIC).convert('RGBA')
assert not (HERE/'source-packet.json').exists();packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in ['south','east','north']:
    p=MOD/f'Textures/Things/Building/Production/TableMachining_{f}.png';im=read(p);refs[f]=dict(**private(p),frame=list(im.size),alpha_bounds=im.getbbox())
definition=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Production.xml');node=next(n for n in ET.parse(definition).getroot() if n.findtext('defName')=='TableMachining');bench=next(n for n in ET.parse(definition).getroot() if n.get('Name')=='BenchBase')
packet.update(previous_packet=ref(OLD/'source-packet.json'),directional_reference=dict(textures=refs,definition=private(definition),object=ET.tostring(node,encoding='unicode'),parent=ET.tostring(bench,encoding='unicode'),load_folders=private(MOD/'LoadFolders.xml'),graphic_class='Graphic_Multi',drawSize=[3.5,1.5],footprint=[3,1],mapping='Actual VTE S/N448x192 and E192x448 directional frames correspond to Core TableMachining texPath; draw frame rotates. Account for transparent margins, no Qud physical width from frame bounds.',role='Parallel cardinal metal work-surface convention, complete end volume and restrained wear only. No donor machinery, tools, L plan, production recipes or3x1footprint copied.'),
    camera=dict(classification='CARDINAL_SOURCE_BOUND',authored_width=13.7,authored_depth=7.6,top_depth_factor=K,top_height=9.15,apron_thickness=1.4,projection='u=8+rotated_x; v=16.9+(3.4/7.6)*rotated_y-z. Same elevation/physical dimensions for all directions.',dimension_provenance='Hidden depth/support extrusion and stock thickness/placement are authored estimates from source parts/front and actual donor camera, not native length fields or a fixed end/front ratio.',support_rule='Two source perforated plate supports extrude in depth. Square holes run front/back and remain visible in S/N; solid outer plate faces hide them in end views. Do not paste front holes onto end panel.',stock=dict(upright_x=[1.05,3.85],upright_y=[1.88,2.68],upright_z=[9.15,15.0],small_mark_center=[-.45,2.148,9.41],small_mark_radius=.26,identity='Unidentified native occupied marks. Plate thickness and round-form unseen placement are authored; no item/tool identity or crafting role inferred.'),west='Occupied stock must be separately projected: its plate and small mark change depth/overlap, not a whole mirrored occupied image.'),
    frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],normalization=dict(uniform_scale=SCALE,pivot=[8,16],scope='One whole-object transform for all empty bases and stock components in every view.',reason='Opposed view of high upright stock approaches original top border; uniform shared scale supplies reconstruction margin without per-state/view crop.'),rule='Same source cell, origin and scale for shared base and every stock component/role. No independent state/view bounds fitting.'),
    construction='Retain corrected source south base and stock material at uniform shared scale. Reverse symmetric empty bench for N, construct complete end plate volume and separately project stock in N/E/W, preserving front/back holes and opaque end faces. Unseen support extrusion and stock faces are authored.',native_acceptance='Pending full-set generation gate; native container/inventory/tile/detail choice,100-weight inorganic/non-takeable metal/cover/visibility, rare Animated fallback and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
for name,oldname in [('base','base-neutral-master.png'),('stock','stock-neutral-master.png')]:
    original=read(OLD/'registered'/oldname).convert('RGBa').resize((512,768),Image.Resampling.LANCZOS).convert('RGBA');original.save(HERE/f'retained-{name}-before-normalization.png');normalize(original).save(HERE/f'selected-south-{name}-neutral.png')
ImageOps.mirror(read(HERE/'selected-south-base-neutral.png')).save(HERE/'selected-north-base-neutral.png')
def wrap(body):return f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g transform="translate(8 16) scale({SCALE}) translate(-8 -16)" stroke-linejoin="round">'+body+'</g></svg>'
end=f'''<g stroke="#344247" stroke-width=".16"><path d="M4.2 11.96H11.8V19.8526H4.2Z" fill="#aaaaaa"/><path d="M4.2 4.6855H11.8V10.8145H4.2Z" fill="#c7c7c7"/><path d="M4.2 10.8145H11.8V12.2145H4.2Z" fill="#999999"/><path d="M4.5 12.6H11.5V19.55H4.5Z" fill="none" stroke="#777777" stroke-width=".08"/></g>'''
for f in ['east','west']:
    svg=wrap(end);(HERE/f'constructed-{f}-base.svg').write_bytes(svg.encode());(HERE/f'constructed-{f}-base.png').write_bytes(svg_to_bytes(svg_string=svg))
for f in ['south','north']:read(HERE/f'selected-{f}-base-neutral.png').save(HERE/f'constructed-{f}-base.png')
def p(x,y,z,f):
    x,y={'south':(x,y),'east':(-y,x),'north':(-x,-y),'west':(y,-x)}[f];return 8+x,16.9+K*y-z
def rectface(x0,x1,y,z0,z1,f):
    pts=[p(x0,y,z1,f),p(x1,y,z1,f),p(x1,y,z0,f),p(x0,y,z0,f)];return 'M'+' L'.join(f'{u:.5f} {v:.5f}' for u,v in pts)+'Z'
def polygon(points,f):return 'M'+' L'.join(f'{u:.5f} {v:.5f}' for u,v in [p(*q,f) for q in points])+'Z'
for f in ['east','north','west']:
    pieces=[];slot='';face=''
    if f=='north':
        y=1.88;face=rectface(1.05,3.85,y,9.15,15,f);slot=rectface(1.7,3.15,y,13.049,14.299,f)
    else:
        x=3.85 if f=='east' else 1.05;face=polygon([(x,1.88,15),(x,2.68,15),(x,2.68,9.15),(x,1.88,9.15)],f)
    top=polygon([(1.05,1.88,15),(3.85,1.88,15),(3.85,2.68,15),(1.05,2.68,15)],f)
    u,v=p(-.45,2.148,9.41,f);disc=f'<circle cx="{u}" cy="{v}" r=".26" fill="#d7c765" stroke="#756b32" stroke-width=".08"/>'
    opening=f'<mask id="slot"><rect width="16" height="24" fill="white"/><path d="{slot}" fill="black"/></mask>' if slot else ''
    plate=f'<g'+(' mask="url(#slot)"' if slot else '')+f'><path d="{face}" fill="#d7c765" stroke="#756b32" stroke-width=".14"/><path d="{top}" fill="#e5d88b" stroke="#756b32" stroke-width=".12"/></g>'
    # In E the plate is nearer and occludes the small mark; W sees the mark nearer.
    content=(disc+plate) if f=='east' else (plate+disc);svg=wrap('<defs>'+opening+'</defs>'+content);(HERE/f'constructed-{f}-stock.svg').write_bytes(svg.encode());(HERE/f'constructed-{f}-stock.png').write_bytes(svg_to_bytes(svg_string=svg))
read(HERE/'selected-south-stock-neutral.png').save(HERE/'constructed-south-stock-neutral.png')
stock=read(HERE/'selected-south-stock-neutral.png');a=np.array(stock);a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*np.array([1,.95,.4]));Image.fromarray(a).save(HERE/'constructed-south-stock.png')
for f in ['east','north','west']:
    a=np.array(read(HERE/f'constructed-{f}-stock.png'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].max(2)[:,:,None]));a[a[:,:,3]==0,:3]=0;Image.fromarray(a).save(HERE/f'constructed-{f}-stock-neutral.png')
empty=Image.new('RGBA',(1536,768));occupied=Image.new('RGBA',(1536,1536))
for i,f in enumerate(['south','east','north','west']):
    base=read(HERE/f'constructed-{f}-base.png');combined=base.copy();combined.alpha_composite(read(HERE/f'constructed-{f}-stock.png'));combined.save(HERE/f'constructed-{f}-occupied.png')
    if i<3:empty.alpha_composite(base,(i*512,0))
    x=(i%2)*768;y=(i//2)*768;panel=Image.new('RGBA',(768,768));panel.alpha_composite(combined,(128,0));occupied.alpha_composite(panel,(x,y))
empty.save(HERE/'empty-front-guided-turnaround.png');occupied.save(HERE/'occupied-manual-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,1250),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'METAL WORKBENCH / two actual source states > retained south / full end volume + separately projected stock',font=font,fill='#e3cf43');im=read(HERE.parent/'v1/native-states-comparison.png');im.thumbnail((800,560));plate.paste(im,(15,50),im)
for i,f in enumerate(['south','east','north']):
    im=read(Path(refs[f]['path']));im.thumbnail((170,220));plate.paste(im,(865+i*180,90),im);d.text((855+i*180,335),'ACTUAL VTE / '+f,font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north','west']):
    im=read(HERE/f'constructed-{f}-occupied.png').resize((288,432));plate.paste(im,(20+i*355,560),im);d.text((20+i*355,1020),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Actual VTE/Core TableMachining: Graphic_Multi, drawSize3.5x1.5, footprint3x1; machinery/tools/footprint not copied.',
 'Authored depth7.6; source square holes run front/back, so solid outer end plates hide them in E/W.',
 'Same empty base for both states; stock plate/round mark remain unidentified. E/W stock occlusion differs physically.',
 'One uniform0.95registration around8,16 for every component/state/view protects high reverse-stock margin.',
 'Steel c, occupied chosen C/w/y/W; extra views unbound. Native container/state/physics/rare Animated acceptance pending.']):d.text((18,1070+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference-construction.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Both states and complete source-based cardinal construction before refinement',review='Corrected parallel south retained at common0.95registration; symmetric empty reverse and full7.6depth end plate authored. S/N front/back support holes remain open; E/W outer faces solid by assumed extrusion. Stock plate and small mark projected separately with correct opposed position/occlusion, no tools/item identity. All frames/pivots/roles shared; extra directions unbound.'))
(HERE/'empty-turnaround-prompt.txt').write_bytes(f'''Use case: sketch-to-render. ONE Qud empty metal workbench, three strict cardinal map views. Image1 is1536x768 edit target, equal512x768columns: SOUTH selected front left, complete EAST end center, NORTH back right. Image2 actual VTE TableMachining_east only for cold-metal contours and map-facing volume; no machines, tools, L-worktop or donor footprint. Image3 actual Qud two-state source plate; request the EMPTY state only.
Description: {packet['description']} Preserve selected source rectangular top, shallow straight apron and two broad perforated plate supports. Shared authored width13.7/depth7.6/topheight9.15/apron1.4; projection u8+rotated_x,v16.9+(3.4/7.6)*rotated_y-z. Uniform0.95registration around8,16 already applied to every component/view. Keep all current positions, proportions, scale and parallel planes, no yaw, convergence or compressed end. S/N square support holes are genuine alpha openings; end outer face is solid because holes run along depth. No frontal supports/holes pasted onto side.
Gray neutral beaten chrome-steel across entire bench, restrained fine scratches, clean outline/subtle shading, no rust/decorative machinery. Keep selected S design; refine full E/N to match. No stock, tool, handle, circle, drawers, occupant or extra state in this EMPTY sheet. Same1536x768frame and full512x768panels, transparent exterior/under-bench/support holes, no backdrop/glow/drop shadow/text/labels. No separate bounds fitting or isolation.'''.encode())
print('Constructed complete shared empty bench and separately projected occupied stock, same uniform normalization in all views.')
