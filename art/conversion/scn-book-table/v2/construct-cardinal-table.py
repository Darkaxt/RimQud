"""Low two-drawer table in parallel cardinal map projection."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');FACINGS=['south','east','north'];SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in FACINGS:
    p=MOD/f'Textures/Things/Building/Furniture/EndTable_{f}.png';im=Image.open(p).convert('RGBA');refs[f]=dict(**private(p),frame=list(im.size),alpha_bounds=list(im.getchannel('A').getbbox()))
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),source_camera_superseded=ref(OLD/'registered/registration-comparison.png'),
 directional_reference=dict(textures=refs,definition=private(Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Furniture.xml')),building_base=private(Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Base.xml')),load_folders=private(MOD/'LoadFolders.xml'),graphic_class='Graphic_Multi',xml_ancestry=['EndTable','TableBase','FurnitureWithQualityBase','FurnitureBase','BuildingBase'],draw_size=None,footprint=None,missing='No explicit drawSize/size in inspected XML ancestry; runtime defaults not exported. Texture dimensions are not physical dimensions.',role='Actual directional VTE EndTable surfaces establish parallel top edges and shallow map-camera visibility with front drawer seams, blank side/back panels. No stacked donor drawers, knobs, gameplay or footprint copied.'),
 camera=dict(projection='screen u8+cardinal_horizontal, v18-height-0.475*cardinal_depth. Parallel axes, same object scale/pivot throughout; no perspective convergence.',width=13.6,depth=8,height=8.4,depth_status='Authored estimate for Qud hidden depth; broad source width and low drawer housing retained. Actual donor camera informs planes, not recovered dimensions.',source_correction='Replace strongly converging trapezoid with rectangular tabletop in a fixed shallow cardinal map projection. Retain two side-by-side front drawers, low rail and short feet.',unseen='Plain side/back wood with understated puzzle-box joinery seams; no extra drawers, books, papers, switches or visible inventory.'),
 construction='One editable spatial wood body, broad independent tabletop, two equal side-by-side inset fronts with recessed pulls, low rail and short supports. S has two drawers; E complete plain end; N plain back. W mirrors E because geometry and markings are symmetric.',native_acceptance='Pending full-set generation gate; fixed source container/on inventory, non-solid organic furniture, rare Animated fallback and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
def project(p,f):
    x,y,z=p
    if f=='east':x,y=y,-x
    elif f=='north':x,y=-x,-y
    return 8+x,18-z-.475*y
def points(ps,f):return ' '.join(f'{u:.4f},{v:.4f}' for u,v in [project(p,f) for p in ps])
def scene(f,owner=False):
    ops=[]
    def poly(ps,color,detail=False,stroke='#303030',width=.13):
        if owner:color='#ffffff' if detail else '#000000';stroke=color
        ops.append(f'<polygon points="{points(ps,f)}" fill="{color}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>')
    def line(ps,color='#747474',width=.1,detail=False):
        if owner:color='#ffffff' if detail else '#000000'
        ops.append(f'<polyline points="{points(ps,f)}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
    def box(x0,x1,y0,y1,z0,z1,color,detail=False):
        ps=[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
        for i in range(4):
            p,q=ps[i],ps[(i+1)%4];a,b=project(p,f),project(q,f)
            if a[0]<b[0]:poly([p,q,(q[0],q[1],z0),(p[0],p[1],z0)],color,detail)
        poly(ps,color,detail)
    for x in [-6.3,6.3]:
        for y in [-3.65,3.65]:box(x-.22,x+.22,y-.22,y+.22,0,2.2,'#a6a6a6')
    box(-6.6,6.6,-3.9,3.9,1.8,2.35,'#bcbcbc')
    box(-6.5,6.5,-3.75,3.75,2.35,7.8,'#909090')
    if f=='south':
        for x0,x1 in [(-6.25,-1.15),(1.15,6.25)]:
            poly([(x0,-3.79,6.8),(x1,-3.79,6.8),(x1,-3.79,4.1),(x0,-3.79,4.1)],'#bdbdbd')
            line([(x0+.15,-3.8,6.6),(x1-.15,-3.8,6.6)],'#e0e0e0',.09)
            c=(x0+x1)/2;poly([(c-.65,-3.82,5.8),(c+.65,-3.82,5.8),(c+.65,-3.82,5.25),(c-.65,-3.82,5.25)],'#494949')
    elif f=='north':
        poly([(6.15,3.78,7.35),(-6.15,3.78,7.35),(-6.15,3.78,2.8),(6.15,3.78,2.8)],'#9b9b9b',stroke='#747474',width=.08)
    else:
        poly([(6.53,-3.35,7.35),(6.53,3.35,7.35),(6.53,3.35,2.8),(6.53,-3.35,2.8)],'#9b9b9b',stroke='#747474',width=.08)
    box(-6.8,6.8,-4,4,7.8,8.4,'#cfc041',True)
    line([(-6.55,-3.75,8.42),(6.55,-3.75,8.42),(6.55,3.75,8.42)],'#e7df92',.09,True)
    for y in [-1.7,1.2]:line([(-5,y,8.42),(5,y,8.42)],'#b5a838',.07,True)
    return ''.join(ops)
for f in FACINGS:
    for role in ['constructed','ownership']:
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{scene(f,role=="ownership")}</svg>';p=HERE/f'{role}-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,750),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'BOOK TABLE / parallel cardinal planes, side-by-side drawers and substantial complete end',font=font,fill='#e3cf43')
for i,f in enumerate(FACINGS):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((280,420),Image.Resampling.LANCZOS);plate.paste(im,(50+i*470,65),im);d.text((50+i*470,515),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Source broad top, two low front drawers, lower rail and short feet retained; no books or contents invented.',
 'Shared authored width13.6 / depth8; actual EndTable cardinal top is parallel, not a converging trapezoid.',
 'Complete end is broad enough for the source table depth. Blank side/rear panels do not acquire front drawers.',
 'One source16x24cell / pivot8,16; gold tabletop is only an ownership aid. Native activation pending.']):d.text((18,600+i*30),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Manual camera and complete side/back construction before refinement',review='Parallel top planes, common physical body and low drawer housing. Two S fronts only; complete E end and blank N back preserve actual source identity. Depth8 is authored; no default donor physical dimensions invented.'))
(HERE/'refine-front-prompt.txt').write_text('''Use case: sketch-to-render. Refine this exact Qud Book Table SOUTH cardinal map construction. Image1 is edit target; image2 actual VTE EndTable_south only for restrained wood shading/seams and map-camera convention. Keep image1 exact parallel rectangular tabletop, two side-by-side recessed drawer fronts with dark rectangular pulls, low housing/rail, short feet and full512x768portrait frame. Do not reintroduce the old trapezoid or converge the top edges. No three-quarter yaw, perspective convergence, diagonally sheared body or resized parts.
Canonical description: earth-cleft dwellers fashion tables in the style of puzzle boxes; drawers house the stenographic imagination. Use precise subtle wood joinery and modest grain, not invented gears or elaborate ornaments. Gray body/fronts/feet; muted gold tabletop including front lip is an ownership aid for native detail tint. No stacked drawers, knobs, books, papers, lamp, inventory, open drawers or mechanisms. Top and wood material remain opaque, leg gaps transparent. Subtle flat game-art shading, clean dark edges, low-relief bevel only. Transparent background, no glow/shadow/scene/text/labels; same positions and scale.''',encoding='utf-8')
print('Constructed source-bound parallel S/E/N table and recorded actual directional camera/depth evidence.')
