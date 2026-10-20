"""Source-bound alchemist furniture, cardinal projections of one authored assembly."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,math,re,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2';SIZE=(512,768)
assert not (HERE/'source-packet.json').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def private(p):return dict(file=str(p),sha256=sha(p),publication='Private installed reference, not copied as standalone donor art')
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def camera(f,p):
    x,z,h=p
    if f=='south':u,d=x,z
    elif f=='north':u,d=-x,-z
    elif f=='east':u,d=-z,x
    else:u,d=z,-x
    return (8+u,22.3-h-.24*d),d-.24*h
def point(f,p):return camera(f,p)[0]
def coords(points):return ' '.join(f'{x:.4f},{y:.4f}' for x,y in points)
def primitive(f,role,points,content,solid):
    return dict(depth=sum(camera(f,p)[1] for p in points)/len(points),role=role,content=content,solid=solid)
def polygon(f,role,points,fill,stroke='#393939',width=.13):
    xy=coords([point(f,p) for p in points]);return primitive(f,role,points,f'<polygon points="{xy}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round"/>',f'<polygon points="{xy}" fill="'+('white' if role=='glass' else 'black')+f'" stroke="'+('white' if role=='glass' else 'black')+f'" stroke-width="{width}" stroke-linejoin="round"/>')
def box(f,bounds):
    x0,x1,z0,z1,h0,h1=bounds
    faces=[([(x0,z0,h0),(x1,z0,h0),(x1,z0,h1),(x0,z0,h1)],'#a9a9a9'),
           ([(x1,z1,h0),(x0,z1,h0),(x0,z1,h1),(x1,z1,h1)],'#999999'),
           ([(x0,z1,h0),(x0,z0,h0),(x0,z0,h1),(x0,z1,h1)],'#8e8e8e'),
           ([(x1,z0,h0),(x1,z1,h0),(x1,z1,h1),(x1,z0,h1)],'#aeaeae'),
           ([(x0,z0,h1),(x1,z0,h1),(x1,z1,h1),(x0,z1,h1)],'#c4c4c4')]
    return [polygon(f,'wood',p,c) for p,c in faces]
def line(f,role,points,stroke,width,alpha=1):
    xy=coords([point(f,p) for p in points]);s=f'<polyline points="{xy}" fill="none" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" opacity="{alpha}"/>';flat=s.replace(stroke,'white' if role=='glass' else 'black');return primitive(f,role,points,s,flat)
def tube(f,points,width=.20):
    return [line(f,'glass',points,'#467f88',width+.11),line(f,'glass',points,'#77bfcf',width),line(f,'glass',[(x-.025,z-.015,h+.02) for x,z,h in points],'#d5eef3',width*.23)]
def ellipse(f,center,rx,rz,rh):
    xy,depth=camera(f,center);radius=rx if f in ['south','north'] else rz
    body=f'<ellipse cx="{xy[0]:.4f}" cy="{xy[1]:.4f}" rx="{radius}" ry="{rh}" fill="#77bfcf" fill-opacity=".27" stroke="#4d9bac" stroke-width=".17"/>'
    flat=body.replace('#77bfcf','white').replace('#4d9bac','white')
    return dict(depth=depth,role='glass',content=body,solid=flat)
assemblies={};geometry={}
for facing in ['south','east','north','west']:
    parts=[]
    # Two cross-depth trestles account for the two source-front supports.
    for x in [-4.7,4.7]:
        for z in [-2.45,2.45]:parts+=box(facing,(x-.25,x+.25,z-.23,z+.23,.15,7.4))
        parts+=box(facing,(x-.65,x+.65,-2.9,2.9,0,.3))
    parts+=box(facing,(-4.7,4.7,-.18,.18,1.45,1.9))
    parts+=box(facing,(-6.8,6.8,-3,3,7.3,8.0))
    for z in [-2.2,0,2.2]:parts.append(line(facing,'wood',[(-6.55,z,8.015),(6.55,z,8.015)],'#8b8b8b',.045))
    for i in range(13):
        t=i*math.tau/13;points=[(.2+.35*math.cos(t),.1+.35*math.sin(t),8.025),(.2+1.5*math.cos(t),.1+1.5*math.sin(t),8.025)]
        parts.append(line(facing,'wood',points,'#6f6f6f',.06,.8))
    # Three phial marks are an authored reading of the sparse rack glyph.
    for x in [-5.2,-3.7,-2.2]:
        parts+=tube(facing,[(x,-.95,14.3),(x,-.95,10.5),(x+.10,-.95,10.3),(x+.20,-.95,10.5),(x+.20,-.95,14.3)],.14)
    for z in [-1.45,-.4]:
        for x in [-5.85,-1.45]:parts+=box(facing,(x-.13,x+.13,z-.12,z+.12,8,12.8))
        for h in [8.55,12.25]:parts+=box(facing,(-5.98,-1.32,z-.15,z+.15,h,h+.36))
    # Alembic bulb is ellipsoidal; coil/tube depth is authored from the front glyph.
    parts.append(ellipse(facing,(3.1,.65,8.85),2.05,2.05,.85))
    parts+=tube(facing,[(3.0,.65,9.6),(3.0,.65,11.8),(3.25,.65,11.8),(3.25,.65,9.6)],.14)
    coil=[]
    for i in range(51):
        t=math.radians(-70+i*6.4);coil.append((-1.3+1.4*math.cos(t),.2+1.0*math.cos(t),19.6+1.25*math.sin(t)))
    parts+=tube(facing,coil,.18)
    outlet=[coil[-1],(-.2,.4,18.3),(.7,.5,17.8),(1.7,.5,17.8),(2.5,.6,18.3),(3.1,.6,19.1),(3.8,.6,19.7),(4.5,.7,19.8),(5.2,.8,19.2),(5.8,.9,18.6),(5.35,1,17.7),(4.7,1.05,18.0),(4.25,1.05,17.1),(3.15,.65,16.6),(3.15,.65,11.8)]
    parts+=tube(facing,outlet,.18)
    parts+=tube(facing,[(-.1,.4,18.3),(-1.6,.6,14.6),(-1.8,.7,9.55)],.13)
    # Stable painter order follows this single fixed shallow cardinal camera.
    parts.sort(key=lambda p:p['depth'],reverse=True)
    # Retain v2's explicit visible-front bulb/neck depth correction.
    bulbs=[p for p in parts if p['content'].startswith('<ellipse ')]
    necks=[p for p in parts if p['content'].startswith('<polyline ') and len(re.search(r'points="([^"]*)"',p['content']).group(1).split())==4]
    parts=[p for p in parts if p not in bulbs and p not in necks]+bulbs+necks
    content=''.join(p['content'] for p in parts);ownership=''.join(p['solid'] for p in parts)
    for stem,s in [('constructed',content),('ownership',ownership)]:
        text=svg(s);(HERE/f'{stem}-{facing}.svg').write_bytes(text.encode());raster(text).save(HERE/f'{stem}-{facing}.png')
    assemblies[facing]=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA')
    geometry[facing]=dict(facing=facing,projection='u=cardinal horizontal; v=22.3-height-.24*depth; parallel orthographic edges',camera_pitch=math.degrees(math.atan(.24)),native_binding=facing=='south',part_primitives=len(parts))
sheet=Image.new('RGBA',(2048,768))
for i,im in enumerate(assemblies.values()):sheet.paste(im,(i*512,0))
sheet.save(HERE/'constructed-turnaround.png')
old=json.loads((OLD/'source-packet.json').read_text());native=Path(old['native_definition']['path']);assert sha(native)==old['native_definition']['sha256']
mod=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');donors={f:mod/f'Textures/Things/Building/Production/TableDrugLab_{f}.png' for f in ['south','east','north']}
definition=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Production.xml');nodes=ET.parse(definition).getroot();lab=next(n for n in nodes.findall('ThingDef') if n.findtext('defName')=='DrugLab')
packet=dict(old);packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),supersedes=ref(OLD/'source-packet.json'),
    camera=dict(contract='Straight south/front, complete east/right end, straight north/back and separately authored west/left end. One fixed shallow map camera, no yaw or converging perspective.',projection=geometry,reference='Actual VTE TableDrugLab cardinal references provide consistent shallow visibility and chemical-glass shading; retain Qud upright wood/rack/alembic identity.'),
    donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',about=private(mod/'About/About.xml'),load_folders=private(mod/'LoadFolders.xml'),assets={f:private(p) for f,p in donors.items()},definition=private(definition),defName='DrugLab',texPath=lab.findtext('graphicData/texPath'),drawSize=lab.findtext('graphicData/drawSize'),role='Cardinal work-surface and glass readability only; donor layout, metal counter, size and drug/crafting mechanics are not imported.'),
    construction='One shared authored assembly: rectangular scorched wooden surface, two cross-depth trestles, left three-phial rack and tall glass alembic. Hidden trestle/rack joinery, apparatus depth and reverse glass surfaces are authored interpretation; not new native components.',
    frame=dict(native=[16,24],manual=list(SIZE),recipient=[256,256],authored_source_anchor=[8,16],floor_reference=[8,22.3],rule='All views and both color roles share same full source-cell mapping, scale and pivot. No independent bounds fitting. South is proposed replacement for existing fixed tile; E/N/W are unbound authoring assets.'),
    furniture_views=dict(required=['south','east','north'],additional='west explicitly authored because asymmetric rack/alembic makes blind east mirroring unreliable',native_rotation='Not implemented; later wall/table-facing decision remains open.'),
    states='Only the declared fixed Alchemist Table tile; inherited empty/full tile/detail tags deleted. Same described rack/alembic in every facing, no invented inventory appearance state.',
    native_acceptance='Pending full-set generation and integrated source-tile/physical-frame/visibility/container state acceptance.')
packet['proportion_correction']=dict(user_feedback='The side view is too narrow relative to RimWorld visual convention.',previous=ref(OLD/'source-packet.json'),bench_width=13.6,previous_depth=4,current_depth=6,side_to_front_width=6/13.6,donor_texture_frames=dict(south=[448,192],east=[192,448],ratio=192/448),donor_drawSize=lab.findtext('graphicData/drawSize'),donor_size=lab.findtext('size'),glass_volume=dict(flask_radii=[2.05,2.05,.85],coil_horizontal_radii=[1.4,1.0]),reason='Increase inferred furniture depth and glass volume in the source construction; do not stretch completed images or widen every side view indiscriminately. This is an authored unseen dimension, not native Qud footprint metadata. Preserve front layout and full-cell physical mapping.')
write('source-packet.json',packet);write('camera-and-geometry.json',geometry)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);board=Image.new('RGB',(1440,750),'#142823');d=ImageDraw.Draw(board);d.text((18,14),'ALCHEMIST TABLE / native icon -> fixed cardinal wood/rack/alembic -> actual donor convention',font=font,fill='#e3cf43')
original=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/packet['original_reference']['reference_file'];assert sha(original)==packet['original_reference']['reference_sha256']
for i,(p,label) in enumerate([(original,'QUD / source identity'),(HERE/'constructed-south.png','MANUAL / parallel tabletop'),(donors['south'],'ACTUAL VTE / glass style')]):
    im=Image.open(p).convert('RGBA');im.thumbnail((400,450),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS)
    if i==0:im=im.resize((256,384),Image.Resampling.NEAREST)
    board.paste(im,(i*480+30,80),im);d.text((i*480+18,580),label,font=font,fill='#e3cf43')
d.text((18,665),'One source fixture state; no imported drug-lab behavior. Apparatus asymmetry requires explicit west.',font=font,fill='#e5e8d8');board.save(HERE/'source-camera-comparison.png')
ledger_path=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(ledger_path.read_text());assert ledger['active_entry']=='SCN-ALCHEMIST-TABLE';e=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
for step,action,names in [('resolve_object_description_original_tile_palette_state','Recheck exact installed source definition/hash and original w/C fixture; retain deleted inherited empty/full tags and actual inventory boundary.',['source-packet.json']),('select_render_reference_or_document_no_equivalent','Select actual VTE drug-lab SEN textures and source Core definition as camera/glass convention only, preserving Qud wood/rack/alembic.',['source-camera-comparison.png']),('construct_faithful_shape','Correct converging front to a rectangular cardinal tabletop and construct one shared asymmetric apparatus, phial rack and trestle assembly.',['construct-cardinal-views.py','constructed-south.svg','constructed-south.png','camera-and-geometry.json']),('create_front_side_back_furniture_views','Prepare explicit S/E/N/W geometric proposals from one authored assembly; west is separate, native orientation behavior unchanged.',['constructed-turnaround.png','constructed-east.svg','constructed-north.svg','constructed-west.svg']),('create_required_state_neighbor_variants','Retain one source fixture state; child explicitly deletes empty/full tile/detail tags. No neighbor tiling or invented empty-lab state.',['source-packet.json'])]:
    e['process_log'].append(dict(timestamp=packet['recorded_at'],step=step,action=action,inputs=[ref(HERE/'source-packet.json')],outputs=[ref(HERE/n) for n in names],review='Shared whole-cell frame and cardinal axes. Wood/scorch and glass ownership stay separate. These are proposals pending refinement; unseen surfaces/joins are authored, not exported native dimensions or new functionality.',result='PASS'))
e['current_step']='refine_materials_and_form';ledger['updated_at']=packet['recorded_at'];ledger_path.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Constructed source-bound cardinal alchemist table with explicit asymmetric west and one unchanged native fixture state.')
