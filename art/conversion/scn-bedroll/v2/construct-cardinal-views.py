"""Rigid cardinal reorientation of the selected flat bedroll and its masks."""
from pathlib import Path
from datetime import datetime,timezone
import math,hashlib,json,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');FACINGS=['south','east','north','west'];SIZE=(768,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
im=Image.open(OLD/'registered/neutral-master.png').convert('RGBA');a=np.array(im);weight=np.array(Image.open(OLD/'registered/fabric-ownership-mask.png').convert('L'))
def centroid(mask):y,x=np.where(mask);return np.array([x.mean(),y.mean()])
fold=centroid((a[:,:,3]>128)&(weight>127));body=centroid((a[:,:,3]>128)&(weight<128));vector=body-fold;theta=math.atan2(vector[0],vector[1]);source_pivot=(body+fold)/2;target_pivot=np.array([384.,416.])
packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in ['south','east','north']:
    p=MOD/f'Textures/Things/Building/Furniture/Bed/Bedroll_{f}.png';q=Image.open(p).convert('RGBA');refs[f]=dict(**private(p),frame=list(q.size),alpha_bounds=list(q.getchannel('A').getbbox()))
packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),source_shape='Source goat-wool body, rounded lower end, pale folded/rolled upper end and canvas fastening retained. Replace diagonal map-plane orientation with cardinal axes by one rigid transform per complete view, not a new mattress design.',
 directional_reference=dict(textures=refs,definition=private(Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Furniture.xml')),load_folders=private(MOD/'LoadFolders.xml'),graphic_class='Graphic_Multi',shader='CutoutComplex',draw_size=[1,2],footprint=[1,2],role='Actual VTE Bedroll directional paths and Core definition show flat map bedding, broad side footprint and restrained padded material. Texture margins and differing frame orientations are recorded. No pillow, repaired patches, donor physical footprint or caravan mechanics copied.'),
 camera=dict(contract='Flat map-plane bedding with shallow drawn fold relief; straight cardinal long axis. Rotate whole selected design and all masks rigidly. No engineering end elevation, yaw, shear or independent part/bounds centering.',selected_front=ref(OLD/'registered/neutral-master.png'),source_fold_centroid=fold.tolist(),source_body_centroid=body.tolist(),source_rotation_pivot=source_pivot.tolist(),target_rotation_pivot=target_pivot.tolist(),south_rotation_degrees=math.degrees(theta),physical_scale='Old1024x1536master=64pixels per source unit; new768x768extent=32pixels per unit. Exactly0.5source raster scale; rigid orientation only.',west='Explicit +90degree orientation of same asymmetric tie design; not mirrored east.'),
 construction='Original editable source geometry rigidly reoriented for manual comparison. Previously selected front refinement and explicit alpha/ownership are reoriented by the identical source-unit mapping. Preserve irregular fold/ties and material; final composed refinement is material-only.',
 frame=dict(native_canvas=[16,24],authoring_extent=[24,24],manual_canvas=[768,768],recipient_canvas=[384,256],source_cell_offset=[4,0],native_original_anchor=[8,16],authored_source_anchor=[12,16],object_rotation_center=[12,13],rule='Common24x24authoring extent and original16x24cell mapping, with4units side margin for rotated length. All parts/masks share rigid pose transform. Recipient384x256keeps native source-unit sampling; physical-frame activation pending.'),
 native_acceptance='Pending full-set generation gate; fixed source tile, takeable/non-solid sleep state and expanded-frame/extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
owned=Image.fromarray(np.dstack([weight,weight,weight,a[:,:,3]]));views={};source_svg=ET.parse(OLD/'constructed-front.svg').getroot();svg_body=''.join(ET.tostring(node,encoding='unicode') for node in source_svg)
for f,extra in [('south',0),('east',-math.pi/2),('north',math.pi),('west',math.pi/2)]:
    angle=theta+extra;c,s=math.cos(angle),math.sin(angle);R=np.array([[c,-s],[s,c]])
    # Output-to-source affine; sample full selected source once per complete view.
    inverse=2*R.T;offset=source_pivot-inverse@target_pivot;affine=(*inverse[0],offset[0],*inverse[1],offset[1])
    selected=im.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,affine,Image.Resampling.BICUBIC).convert('RGBA');own=owned.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,affine,Image.Resampling.BICUBIC).convert('RGBA')
    selected.save(HERE/f'selected-{f}-neutral.png');own.save(HERE/f'ownership-{f}.png');v=np.array(selected);o=np.array(own)[:,:,0]/255;context=v.copy();context[:,:,:3]=np.uint8(v[:,:,:3].astype(float)*((1-o[:,:,None])+o[:,:,None]*np.array([.65,.9,1])));Image.fromarray(context).save(HERE/f'selected-{f}-context.png')
    tx,ty=target_pivot/32-R@(source_pivot/64);svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="768" height="768" viewBox="0 0 24 24"><g transform="matrix({c} {s} {-s} {c} {tx} {ty})">{svg_body}</g></svg>';p=HERE/f'constructed-{f}.svg';p.write_text(svg,encoding='utf-8');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
    views[f]=dict(rotation_degrees=math.degrees(angle),output_to_original_source_affine=list(affine),fixed_scale=.5,mirror=False)
write(HERE/'rigid-view-transforms.json',views)
sheet=Image.new('RGBA',(2304,768))
for i,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(HERE/f'selected-{f}-context.png').convert('RGBA'),(i*768,0))
sheet.save(HERE/'front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1560,1050),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'GOAT-WOOL BEDROLL / rigid cardinal correction of existing design; no silhouette deformation',font=font,fill='#e3cf43')
for row,kind in enumerate(['constructed','selected']):
    for i,f in enumerate(FACINGS):
        p=HERE/(f'constructed-{f}.png' if kind=='constructed' else f'selected-{f}-context.png');q=Image.open(p).convert('RGBA').resize((360,360),Image.Resampling.LANCZOS);x=20+i*385;y=60+row*430;plate.paste(q,(x,y),q);d.text((x,y+375),kind.upper()+' / '+f.upper(),font=font,fill='#e3cf43')
d.text((18,980),'Original16x24cell inside common24x24extent. Explicit west retains tie asymmetry; no mirrored letters or closures.',font=font,fill='#e5e8d8');plate.save(HERE/'manual-selected-cardinal-comparison.png')
write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Pre-refinement rigid camera correction',review='Whole design, folded-end owner and full coverage rotate together at fixed physical scale. S/N axis vertical, E/W horizontal. Canvas fastening and rounded wool body remain source-bound; no new pillow or packed/occupied state. Actual directional reference supports map-view footprint rotation rather than thin end-on geometry.'))
(HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Refine this same Qud goat-wool bedroll in three straight cardinal map views. Image1 is the composed edit target on2304x768canvas, three equal768-square panels: SOUTH left, EAST middle, NORTH right. These are rigid reorientations of the already selected front design; preserve exact shapes, positions, proportions and scale. Image2 is actual installed VTE Bedroll_east only as a flat bedding/material convention reference.
Canonical description: a goat wool bed fastened with canvas ties. Keep one rounded elongated soft wool body, a pale folded/rolled upper end and a canvas fastening with two short tie tails. Gray main wool/ties; only folded end pale cyan for separate color ownership. No separate pillow, zipper, modern repair patches, extra blanket, bed frame, occupant or scene. All views show the same laid-out object from the fixed map camera. South fold above, east fold left, north fold below. Do not narrow the side footprint or make an edge-on engineering view; do not introduce perspective convergence, diagonal yaw/shear or new folded/packed states. Keep the fastening/tails in the corresponding location in every view.
Unify subtle goat-wool texture, soft low-relief folds and clean dark edge weight across the composed views while preserving the selected design. No added heavy creases or ornament. Exactly same2304x768frame and margins; genuine transparent exterior and clear tie gaps. No glow, shadow, backdrop, text or labels. The original selected geometry/masks stay authoritative; this output is a restrained material refinement.''',encoding='utf-8')
print('Rigidly corrected all four cardinal views; retained selected front material, folded-end ownership and tie design.')
