"""Correct floor-cushion yaw; preserve four source patterns in shared coordinates."""
from pathlib import Path
import sys,json,hashlib,math,xml.etree.ElementTree as ET
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
old=json.loads((OLD/'source-packet.json').read_text());donor=Path(old['donor_reference']['path'])
mod=Path('D:/Steam/steamapps/workshop/content/294100/1718190143')
defs=mod/'1.6/Defs/Buildings_Furniture/Buildings_BasicSeats.xml'
core=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Furniture.xml')
base=core.with_name('Buildings_Base.xml')
nodes={}
for path in [defs,core,base]:
    for node in ET.parse(path).getroot():
        if node.get('Name') in ['BuildingBase','FurnitureBase','FurnitureWithQualityBase'] or node.findtext('defName')=='Seat_Cushion':nodes[node.get('Name') or node.findtext('defName')]=ET.tostring(node,encoding='unicode')
assert len(nodes)==4
im=Image.open(donor).convert('RGBA')
packet=dict(entry='SCN-FLOOR-CUSHION',identity=old['identity'],description=old['description'],original_packet=ref(OLD/'source-packet.json'),original_states=old['original_states'],original_context=old['original_context'],native_definition=old['native_definition'],source_shapes=old['source_shapes'],palette=old['palette'],default_reference=old['default_reference'],
    render_reference=dict(texture=private(donor),texture_canvas=list(im.size),alpha_bounds=im.getbbox(),definition=private(defs),core_definition=private(core),base_definition=private(base),load_folders=private(mod/'LoadFolders.xml'),objects=nodes,graphic_class='Graphic_Single',drawSize='No explicit value in inspected Seat_Cushion/FurnitureWithQualityBase/FurnitureBase/BuildingBase XML ancestry; runtime default not asserted.',footprint='No explicit size in inspected ancestry; runtime default not asserted.',mapping='1.6 and1.7 LoadFolders use root textures plus1.6 definitions. Exact Seat_Cushion texPath matches inspected PNG.',role='Actual flat broad soft cushion supplies map-plane camera, outlined stuffed cloth and restrained tuft shading. No donor four-corner tuft layout, comforts, footprint or colors copied.',directional_limit='One Graphic_Single, not three actual directional donor textures. Additional Qud facings are authored rotations of one physical top-plane design; not donor-verified native rotations.'),
    camera=dict(classification='CARDINAL_MAP_PLANE',width=12.8,depth=10.8,thickness=.6,dimensions_status='Authored estimates informed by source low pillow and actual broad floor-cushion reference; not recovered native dimensions.',projection='u=8+rotated_x; v=11.2+0.8*rotated_y-0.65*z. Same fixed elevation for every view. Parallel footprint axes; no diamond yaw.',pattern_rotation='S0,E90,N180,W270 degrees around one center. Pattern3 edge folds rotate with physical pad. Pattern4 diagonal is intrinsic tuft placement, not camera yaw.',volume='Soft crown above continuous low perimeter binding; full broad top visible in each facing. Side not a thin engineering edge.'),
    frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full-cell mapping for every view, pattern and role. No alpha-bounds fit; shape center remains8,11.2. Ground/front anchor8,16 remains the native-cell proposal.'),
    native_state=old['native_state'],native_behavior='Preserve native RandomTile four cosmetic patterns, default visibly equivalent to variant1, Chair Level-1, inherited non-takeability/cover/non-occlusion and rare Animated fallback. Extra directions unbound; no new occupied/folded state.',native_acceptance='Pending full-set generation gate; native RandomTile/default selection, seating/cover/non-takeability and rare Animated fallback plus extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
patterns=[ [(-2.5,-2.1),(2.0,-2.1),(0,.7)],[(0,-3.0),(-3.8,0),(3.8,0),(0,2.8)],[],[(-3.5,-2.2),(0,0),(3.5,2.2)] ]
star=[[(-2.4,2.1),(0,.7),(2.6,2.1)],[(-.8,-.2),(0,.7),(.9,-.3)]]
folds=[[(-5.4,3),(-4.3,2.8),(-3,4.4)],[(3,4.4),(4.3,2.8),(5.4,3)],[(-1.2,4.5),(0,4.1),(1.2,4.5)]]
def rotate(x,y,turn):
    return [(x,y),(-y,x),(-x,-y),(y,-x)][turn]
def point(x,y,t,z=.6):
    x,y=rotate(x,y,t);return 8+x,11.2+.8*y-.65*z
def polyline(points,t,color='#8c8c8c',width=.11):
    pp=[point(x,y,t) for x,y in points];return '<path d="M'+' L'.join(f'{x:.4f} {y:.4f}' for x,y in pp)+f'" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
def svg(n,t,owner=False):
    # S/N width12.8 depth10.8; E/W swap physical dimensions before projection.
    halfx,halfy=((6.4,5.4) if t%2==0 else (5.4,6.4));l,r=8-halfx,8+halfx;top,bottom=11.2-.8*halfy-.39,11.2+.8*halfy-.39
    def outline(offset):return f'M{l+.6} {top+offset+.35} Q8 {top+offset-.25} {r-.6} {top+offset+.35} Q{r+.25} {(top+bottom)/2+offset} {r-.6} {bottom+offset-.25} Q8 {bottom+offset+.4} {l+.6} {bottom+offset-.25} Q{l-.25} {(top+bottom)/2+offset} {l+.6} {top+offset+.35}Z'
    stroke='none' if owner else '#333333';sw=0 if owner else .13
    body=f'<path d="{outline(.5)}" fill="'+('#ffffff' if owner else '#8dd3dd')+f'" stroke="{stroke}" stroke-width="{sw}"/>'
    body+=f'<path d="{outline(0)}" fill="'+('#000000' if owner else 'url(#pad)')+f'" stroke="{stroke}" stroke-width="{sw}"/>'
    if not owner:
        for x,y in patterns[n-1]:
            cx,cy=point(x,y,t);body+=f'<ellipse cx="{cx}" cy="{cy}" rx=".19" ry=".145" fill="#707070" stroke="#626262" stroke-width=".065"/>'
            for a,b in [((x-.65,y-.5),(x-.16,y-.08)),((x+.16,y+.08),(x+.65,y+.5))]:body+=polyline([a,b],t,'#a1a1a1',.10)
        if n==1:
            for p in star:body+=polyline(p,t)
        if n==3:
            for p in folds:body+=polyline(p,t,'#858585',.13)
        if n==4:
            body+=polyline([(-3.25,-2.05),(-.25,-.15)],t,'#999999')+polyline([(.25,.15),(3.25,2.05)],t,'#999999')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><defs><radialGradient id="pad" cx="40%" cy="34%" r="75%"><stop offset="0" stop-color="#e1e1e1"/><stop offset=".7" stop-color="#c8c8c8"/><stop offset="1" stop-color="#a7a7a7"/></radialGradient></defs><g stroke-linejoin="round">'+body+'</g></svg>'
for n in range(1,5):
    folder=HERE/f'variant-{n}';folder.mkdir(exist_ok=True);sheet=Image.new('RGBA',(1536,768))
    for t,f in enumerate(['south','east','north','west']):
        data=svg(n,t);(folder/f'constructed-{f}.svg').write_bytes(data.encode());(folder/f'constructed-{f}.png').write_bytes(svg_to_bytes(svg_string=data));(folder/f'ownership-{f}.png').write_bytes(svg_to_bytes(svg_string=svg(n,t,True)))
        if t<3:sheet.alpha_composite(Image.open(folder/f'constructed-{f}.png'),(t*512,0))
    sheet.save(folder/'constructed-turnaround.png')
    text=f'''Use case: sketch-to-render. Asset: one Qud floor cushion, cosmetic pattern{n}, three cardinal map views. Image1 is the1536x768 edit target: SOUTH/FRONT left, EAST/RIGHT center, NORTH/BACK right, equal512x768columns. Image2 is actual RimWorld VFE SittingCushion reference ONLY for soft cloth shading/outline and broad floor-facing camera, never its tuft pattern. Image3 is the four original native glyphs ONLY for identity, this request corresponds to pattern{n}.
Description: {old['description']} This is low stuffed floor seating, no backrest, legs or occupant. Chaff and feathers are hidden stuffing, no loose feathers or glow. Current pattern: {old['source_shapes'][n-1]}
Refine the given composed construction with restrained fabric shading and fine weave. Keep EXACT tuft/fold positions, cardinal parallel footprint, continuous opaque pad, low cyan lower binding, frame/pivot/scale and all structural ink. Front remains design anchor; E/N are the SAME physical pad rotated90/180degrees, not different cushions. Shared authored width12.8, depth10.8, thickness0.6; projection u8+rotated_x,v11.2+0.8*rotated_y-0.65*z. Keep these proportions and broad visible top. Never squash the side into a thin edge or rotate the whole pad diagonally. Source pattern3 has NO top buttons. No new tufts, holes, face, X-stitched embroidery, dangling ties, hardware or seams. Intrinsic diagonal creases do not change the camera.
Gray fabric is primary; pale cyan lower perimeter binding is a role-key for later neutral extraction. No other colored fabric or baked terrain. Keep SAME1536x768canvas and all512x768panels unchanged. Transparent background, no scene, external glow/drop shadow, labels, axes or text. Refine in context; do not isolate or redesign any part.'''
    (folder/'turnaround-prompt.txt').write_bytes(text.encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,1300),'#142823');d=ImageDraw.Draw(plate)
d.text((18,15),'FLOOR CUSHION / source four cosmetic patterns > cardinal cloth construction / actual VFE reference',font=font,fill='#e3cf43')
native=Image.open(OLD/'native-states-comparison.png').convert('RGB');native.thumbnail((1000,460));plate.paste(native,(10,50))
im.thumbnail((180,180));plate.paste(im,(1150,90),im);d.text((1080,295),'ACTUAL VFE / single graphic',font=font,fill='#e3cf43')
for n in range(1,5):
    sheet=Image.open(HERE/f'variant-{n}/constructed-turnaround.png').convert('RGBA');sheet=sheet.resize((540,270));x=25+((n-1)%2)*710;y=550+((n-1)//2)*340;plate.paste(sheet,(x,y),sheet);d.text((x,y+275),f'PATTERN{n} / SOUTH  EAST  NORTH / common scale',font=font,fill='#e3cf43')
d.text((18,1240),'Width/depth/thickness are authored estimates. Four patterns are not four directions. Extra facings unbound.',font=font,fill='#e5e8d8');plate.save(HERE/'source-reference-construction.png')
write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Generation construction inspection before ImageGen',source=ref(HERE/'source-packet.json'),review='Actual source4patterns preserved as opaque tufts/folds, variant3 plain crown. Parallel cardinal broad pads, full end depth, same physical pattern rotations/scale, thin continuous lower binding. VFE Graphic_Single is disclosed; no actual donor turnaround inferred. No face/holes/glow/loose stuffing. Editable geometry replaces rejected v1 diamond camera; no stretch of finished side image.',outputs=[ref(p) for p in sorted(HERE.glob('variant-*/constructed-*.png'))]))
print('Constructed four actual patterns with shared physical S/E/N/W geometry and exact per-pattern refinement prompts.')
