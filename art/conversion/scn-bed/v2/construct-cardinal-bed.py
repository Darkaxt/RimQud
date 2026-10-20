"""Reconstruct source bed in a fixed cardinal map camera, replacing diagonal v1."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324')
FACINGS=['south','east','north'];SIZE=(768,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
packet=json.loads((OLD/'source-packet.json').read_text());measurements={}
for f in FACINGS:
    p=MOD/f'Textures/Things/Building/Furniture/Bed/Bed_{f}.png';im=Image.open(p).convert('RGBA');measurements[f]=dict(**private(p),frame=list(im.size),alpha_bounds=list(im.getchannel('A').getbbox()))
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),source_shape='Preserve source open wooden headboard with repeated shallow curves/bars, low foot rail, short supports and single chaff-stuffed fabric pad; replace source oblique camera with actual donor cardinal map view. No pillow, blanket subdivision or modern spring mattress.',
 source_camera_superseded=ref(OLD/'registered/registration-comparison.png'),directional_reference=dict(textures=measurements,definition=private(Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Furniture.xml')),load_folders=private(MOD/'LoadFolders.xml'),resolved_bed=dict(graphic_class='Graphic_Multi',draw_size=[2,2],footprint=[1,2],shader='CutoutComplex'),role='Actual VTE textures replace Core Bed paths. Fixed cardinal overhead/map camera and directional footprint swap; fabric/wood rendering only. No donor pillow, blanket, mechanics or physical footprint copied.'),
 camera=dict(projection='Parallel cardinal map projection: screen u12+rotated_x, v14+rotated_y-0.75*z. No yaw, x/y shear or perspective convergence. S sleeping plane vertical, E horizontal, N vertical reversed.',authored_dimensions=dict(width=8,length=14,headboard_height=3.5,pad_height=1.4),uncertainty='Source identity/proportions guide authored dimensions; no hidden Qud measurements available. VTE map-view camera guides projection, not imported bed definition.'),
 construction='One shared spatial bed: wooden slats/rails and four short supports; open curved headboard, low foot rail and one continuous chaff-stuffed fabric pad. Rotating this geometry gives E/N; west mirrors east because there are no asymmetric markings or fittings.',
 registration=dict(native_canvas=[16,24],authoring_extent=[24,24],manual_canvas=[768,768],recipient_canvas=[384,256],source_cell_offset=[4,0],authored_source_anchor=[12,16],native_original_anchor=[8,16],recipient_anchor=[192,170.6666666667],proposed_physical_frame_in_cells=[1.5,1],rule='Add4units transparent margin to both horizontal sides of original16x24cell. All views use common24x24frame and source16x24cell mapping;384x256recipient preserves same pixels per source unit as256x256native cell. No independently fitted bounds or per-view scale. Expanded frame is authoring; native physical-frame acceptance pending.'),
 native_acceptance='Pending full-set generation gate; source fixed tile/sleeping/animated fallback and expanded-frame mapping acceptance unfinished.')
write(HERE/'source-packet.json',packet)
def project(p,f):
    x,y,z=p
    if f=='east':x,y=y,-x
    elif f=='north':x,y=-x,-y
    return (12+x,14+y-.75*z)
def points(ps,f):return ' '.join(f'{u:.4f},{v:.4f}' for u,v in [project(p,f) for p in ps])
def scene(f,owner=False):
    operations=[]
    def poly(ps,fill,role=0,stroke=True):
        color=('#ffffff' if role else '#000000') if owner else fill;ink='#000000' if owner else '#303030'
        operations.append(f'<polygon points="{points(ps,f)}" fill="{color}" stroke="{ink if stroke else color}" stroke-width=".13" stroke-linejoin="round"/>')
    def line(ps,color='#999999',width=.24,role=0):
        color=('#ffffff' if role else '#000000') if owner else color
        operations.append(f'<polyline points="{points(ps,f)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>')
    def block(x0,x1,y0,y1,z0,z1,color):
        # Camera-facing walls and top; all edges parallel in cardinal frame.
        corners=[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
        for j in range(4):
            p,q=corners[j],corners[(j+1)%4];u,v=project(p,f),project(q,f)
            if u[0]<v[0]:poly([p,q,(q[0],q[1],z0),(p[0],p[1],z0)],'#858585')
        poly(corners,color)
    def headboard():
        for x in [-4,4]:block(x-.17,x+.17,-7.18,-6.82,0,3.5,'#b6b6b6')
        line([(-4,-7,1.7),(4,-7,1.7)],'#bcbcbc',.3)
        for x in [-1.35,1.35]:line([(x,-7,1.7),(x,-7,2.8)],'#a5a5a5',.22)
        # Shallow repeated curved upper rail represented by cubic spatial samples.
        import math
        line([(x,-7,3.15-.34*abs(math.sin((x+4)*math.pi/2.66))) for x in [-4+i*8/96 for i in range(97)]],'#c2c2c2',.28)
    # Occlusion changes with facing: far board first, near board last.
    if f=='south':headboard()
    for x in [-3.8,3.8]:
        for y in [-6.8,6.8]:block(x-.18,x+.18,y-.18,y+.18,0,1.1,'#a6a6a6')
    for y in [-6+i*2 for i in range(7)]:block(-3.8,3.8,y-.18,y+.18,.65,.85,'#a8a8a8')
    for x in [-4,3.65]:block(x,x+.35,-7,7,.65,1.15,'#b6b6b6')
    poly([(-3.68,-6.65,1.4),(3.68,-6.65,1.4),(3.68,6.7,1.4),(-3.68,6.7,1.4)],'#a7d4dc',1)
    line([(-3.48,-6.45,1.4),(-3.48,6.45,1.4),(3.48,6.45,1.4)],'#d7edf0',.1,1)
    for x,y in [(-1.8,-3.8),(1.3,-.9),(-1.1,2.6)]:line([(x-.5,y,1.4),(x,y+.12,1.4),(x+.55,y,1.4)],'#8cbdc6',.09,1)
    block(-4.05,4.05,6.8,7.18,.55,1.55,'#bcbcbc')
    if f in ['east','north']:headboard()
    return ''.join(operations)
for f in FACINGS:
    for role in ['constructed','ownership']:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="768" height="768" viewBox="0 0 24 24">{scene(f,role=="ownership")}</svg>';p=HERE/f'{role}-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,750),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'BED / source identity in corrected cardinal map camera; one shared bed geometry',font=font,fill='#e3cf43')
for i,f in enumerate(FACINGS):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((400,400),Image.Resampling.LANCZOS);plate.paste(im,(25+i*470,90),im);d.text((25+i*470,520),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Open wooden headboard, low foot rail and one chaff-stuffed pad; no copied pillow or modern blanket.',
 'Same width8 / length14 physical geometry. No diagonal shear; east uses broad side footprint, not thin edge-on elevation.',
 'Common24x24 authoring extent adds transparent margin for rotated length; native mapping remains pending.',
 'Cyan identifies fabric only. Production wood/fabric remain neutral with independent native w/Y roles.']):d.text((18,600+i*30),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png')
(HERE/'refine-front-prompt.txt').write_text('''Use case: sketch-to-render. Refine this one source-faithful Caves of Qud hillfolk bed in the exact cardinal SOUTH map view.
Image1 is the fixed editable bed construction, edit target. Image2 is actual installed VTE Bed_south, camera/material reference only. Keep image1 placement, scale, straight vertical long axis, parallel side rails, rectangular sleeping pad, open headboard with shallow curved upper rail and vertical bars, low foot rail and short supports. Canonical description: fabrics stuffed with watervine chaff laid across wooden slats. Preserve open headboard gaps. Do not introduce diagonal shear, yaw or converging edges. Use actual overhead/cardinal map camera, not thin engineering elevation or a perspective display model.
Refine restrained flat outlined game-art wood grain and soft chaff-fabric creases. Gray wood; pale cyan fabric is only an ownership aid, including its edges/highlights. No pillow, extra blanket subdivision, spring mattress, upholstery buttons, occupant, rug, objects, ornate carvings or donor metal caps. Plain modest hillfolk construction. Same768x768square canvas and exact positions/margins. Transparent background and board/support gaps; no shadow, glow, scene, text or labels. Full bed visible. Do not crop or independently center the fabric.''',encoding='utf-8')
write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Manual cardinal reconstruction',review='Single shared bed geometry rotates without x/y shear. Source open rail, bars, low foot and chaff pad retained. Actual donor directional map camera supports wide horizontal E sleeping surface. Expanded common frame/physical mapping explicit; native acceptance pending.'))
print('Reconstructed cardinal S/E/N bed and explicit common expanded frame.')
