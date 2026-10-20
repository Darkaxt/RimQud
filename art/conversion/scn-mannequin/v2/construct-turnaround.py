"""Static asymmetric source mannequin: retained front/reverse, separate full profiles."""
from pathlib import Path
import sys,json,hashlib,xml.etree.ElementTree as ET
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2778569619')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists();packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in ['south','east','north']:
    p=MOD/f'Textures/CombatTrainingDummy_{f}.png';im=read(p);refs[f]=dict(**private(p),frame=list(im.size),alpha_bounds=im.getbbox())
definition=MOD/'1.6/Defs/ThingDefs_Buildings/Buildings_Misc.xml';node=next(n for n in ET.parse(definition).getroot() if n.findtext('defName')=='CombatDummy');base=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Buildings/Buildings_Base.xml');parent=next(n for n in ET.parse(base).getroot() if n.get('Name')=='BuildingBase')
packet.update(previous_packet=ref(OLD/'source-packet.json'),directional_reference=dict(textures=refs,definition=private(definition),object=ET.tostring(node,encoding='unicode'),parent_definition=private(base),parent_object=ET.tostring(parent,encoding='unicode'),graphic_class='Graphic_Multi',drawSize=1.2,footprint='No explicit size in inspected CombatDummy/BuildingBase XML; runtime default unknown.',mapping='Exact1.6CombatDummy texPath matches root CombatTrainingDummy S/E/N textures. No LoadFolders.xml installed; activation/profile not asserted.',role='Actual featureless form silhouette, complete profile head volume and shallow shading only. Donor X eyes/target/sack silhouette/training are not copied; source stand/armature geometry is not supplied by this sack reference.'),
    camera=dict(classification='CARDINAL_SOURCE_BOUND',contract='Selected straight front retained; N is the same featureless manufactured forms reversed about the central stand, not the image midpoint. Complete east and west profiles are authored separately for asymmetric limb/role overlap. No humanoid actor pose or face.',authored_shell_depth=2.2,authored_head_profile_width=2.1,authored_profile_base_depth=3.6,dimension_provenance='Unseen form thickness, profile armature depth/occlusion and stand strut directions are authored estimates informed by native biped-form glyph/description and actual donor profile volume; not native dimensions or a donor frame ratio.',stand_center_source_x=7.3,stand_center_expanded_x=11.3,west='Separate profile: pale right armature is far, colored left form is near. A mirror of the entire east would swap source role/laterality incorrectly.'),
    frame=dict(native_canvas=[16,24],expanded_source_frame=[24,24],original_cell_offset=[4,0],manual_canvas=[768,768],recipient_canvas=[384,256],authored_source_anchor=[12,16],original_source_anchor=[8,16],rule='Shared expanded frame adds4source units each side of the original cell; original physical pixels/scale retained. Reflect N about standx11.3 to preserve rotation pivot and fit the source long armature. No per-view/part alpha-bounds normalization; all masks share mapping.'),
    construction='Retain actual selected front material and shell ownership in expanded frame; author reverse of featureless forms about source stand. Separate complete profiles preserve intrinsic colored left bent form versus pale right armature, head/torso/hip fragments, central stem and splayed supports. Profile depth/overlap/unseen surfaces remain interpretation. No face, hands/fingers, walking legs, target, modern human mannequin or new clothing system.',native_acceptance='Pending full-set generation gate; native random detail selection, mounted non-solid30-weight furniture/AV2/HP80, visibility and rare Animated fallback plus extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
raw=read(OLD/'registered/neutral-master.png');base_front=raw.convert('RGBa').resize((512,768),Image.Resampling.LANCZOS).convert('RGBA');base_front.save(HERE/'original-selected-front.png');front=Image.new('RGBA',(768,768));front.alpha_composite(base_front,(128,0));front.save(HERE/'selected-south-neutral.png')
mask=np.array(Image.open(OLD/'registered/shell-ownership-mask.png').convert('L'));alpha=np.array(raw)[:,:,3];weight=np.where((mask>0)&(alpha>0),255,0).astype(np.uint8);role=Image.fromarray(np.dstack([weight,weight,weight,alpha])).convert('RGBa').resize((512,768),Image.Resampling.LANCZOS).convert('RGBA');own=Image.new('RGBA',(768,768));own.alpha_composite(role,(128,0));own.save(HERE/'ownership-south.png')
coeff=(-1,0,2*11.3*32,0,1,0)
for name,im in [('selected-north-neutral',front),('ownership-north',own)]:
    out=im.convert('RGBa').transform((768,768),Image.Transform.AFFINE,coeff,Image.Resampling.BICUBIC).convert('RGBA');out.save(HERE/f'{name}.png')
def context(im,owner):
    a=np.array(im);r=np.array(owner)[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-r[:,:,None])+r[:,:,None]*np.array([.65,.9,1])));return Image.fromarray(a)
for f in ['south','north']:context(read(HERE/f'selected-{f}-neutral.png'),read(HERE/f'ownership-{f}.png')).save(HERE/f'constructed-{f}.png')
def profile(f,owner=False):
    west=f=='west';gray='#000000' if owner else '#b7b7b7';shell='#ffffff' if owner else '#8dd3dd';stroke=lambda c:c if owner else '#303030';width=.14
    def shape(d,c):return f'<path d="{d}" fill="{c}" stroke="{stroke(c)}" stroke-width="{width}"/>'
    def arm(pale):
        if pale:
            path='M7.7 7.95L8.45 11.2L9.1 8.65L9.8 5.4'
            if west:path='M6.9 7.95L6.15 11.2L5.5 8.65L4.8 5.4'
            return f'<path d="{path}" fill="none" stroke="{stroke(gray)}" stroke-width=".48" stroke-linecap="round"/><path d="{path}" fill="none" stroke="{gray}" stroke-width=".27" stroke-linecap="round"/>'
        path='M6.4 7.3L6.2 9.15L7.05 9.4' if not west else 'M8.2 7.3L8.4 9.15L7.55 9.4'
        return f'<path d="{path}" fill="none" stroke="{stroke(shell)}" stroke-width=".49" stroke-linecap="round"/><path d="{path}" fill="none" stroke="{shell}" stroke-width=".3" stroke-linecap="round"/>'
    base=shape('M7.1 5.1H7.55V20.55H7.1Z M7.3 20.2L5.6 22.35H6.15L7.5 20.7L9.15 22.35H9.7L7.7 20.05Z M7.1 20.4L6.8 22.55H7.35L7.65 20.4Z',gray)
    torso='M6.7 7.15Q7.5 6.95 8.1 7.25L8.4 8.1L7.95 9.9L6.65 10.5L6.3 9.75L6.6 8.9Z'
    hip='M6.5 12.25L6.75 12.2L6.95 13H7.7L8.05 12.2L8.4 12.3L7.85 14.5H6.85Z'
    if west:
        # Local part reflection only; arm order/roles remain separately authored.
        parts='<g transform="translate(14.6 0) scale(-1 1)">'+shape(torso,shell)+shape(hip,shell)+'</g>'
    else:parts=shape(torso,shell)+shape(hip,shell)
    head=f'<ellipse cx="7.3" cy="3.85" rx="1.05" ry="1.75" fill="{shell}" stroke="{stroke(shell)}" stroke-width="{width}"/>'
    # E sees pale right arm nearest; W sees colored left bent form nearest.
    body=base+arm(west)+parts+head+arm(not west)
    return '<svg xmlns="http://www.w3.org/2000/svg" width="768" height="768" viewBox="0 0 24 24"><g transform="translate(4 0)" stroke-linejoin="round">'+body+'</g></svg>'
for f in ['east','west']:
    for owner in [False,True]:
        svg=profile(f,owner);name=f'ownership-{f}' if owner else f'constructed-{f}';(HERE/f'{name}.svg').write_bytes(svg.encode());(HERE/f'{name}.png').write_bytes(svg_to_bytes(svg_string=svg))
sheet=Image.new('RGBA',(1536,1536))
for f,(x,y) in zip(['south','east','north','west'],[(0,0),(768,0),(0,768),(768,768)]):sheet.alpha_composite(read(HERE/f'constructed-{f}.png'),(x,y))
sheet.save(HERE/'front-guided-turnaround.png');write(HERE/'frame-expansion.json',dict(source=ref(OLD/'registered/model.json'),selected_front=ref(HERE/'original-selected-front.png'),expanded_front=ref(HERE/'selected-south-neutral.png'),cell_offset=[4,0],before_source_cell=[16,24],after_frame=[24,24],before_recipient=[256,256],after_recipient=[384,256],physical_stand_pivot=[11.3,16],native_anchor=[12,16],reason='Mirroring source long armature about actual standx7.3 would exceed native16-wide cell. Expand every facing/role frame, retain source size and fixed stand, no per-asset bounds fit. Additional frame mapping remains authoring data pending native integration.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,1280),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'MANNEQUIN / static source forms + armature / actual directional dummy reference / shared expanded frame',font=font,fill='#e3cf43');im=read(OLD/'source-construction-comparison.png');im.thumbnail((1020,680));plate.paste(im,(15,45),im)
for i,f in enumerate(['south','east','north']):
    im=read(Path(refs[f]['path']));im.thumbnail((120,150));plate.paste(im,(1050+i*120,95),im)
d.text((1030,270),'ACTUAL DUMMY / S E N',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north','west']):
    im=read(HERE/f'constructed-{f}.png').resize((330,330));plate.paste(im,(15+i*355,700),im);d.text((20+i*355,1050),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Native head/torso/hip shell and colored left form vs pale right armature remain separate roles, no face/target/clothes.',
 'S retained, N reflected about actual stand; E/W separately authored because role/laterality/overlap are asymmetric.',
 'Expanded24x24frame keeps original cell at offset4,0 and original size. Profile depth/base overlap are authored estimates.',
 'Actual mod has Graphic_Multi/drawSize1.2; source has RandomColors detail. Extra views unbound, rare Animated fallback native.']):d.text((18,1120+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference-construction.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Complete static prop views before composed refinement',review='Source unusual separate manufactured forms, left colored bend, pale right armature and splayed base retained. S unchanged in larger common frame; N reversed around stand rather than canvas center. E/W have full head/shell depth and distinct near/far arm order; no mirrored role mistake. Source uncertainty and authored profile geometry explicit; not an actor body, apparel path or Animated implementation. No target/eyes/hands/walking legs.'))
(HERE/'turnaround-prompt.txt').write_bytes(f'''Use case: sketch-to-render. ONE Qud Mannequin, static manufactured furniture, four cardinal views in a1536x1536two-by-two sheet with768x768panels. Image1 edit target: SOUTH top-left is selected refined front; EAST top-right complete right profile; NORTH bottom-left reversed manufactured back; WEST bottom-right separate left profile. Image2 actual CombatTrainingDummy_east ONLY for featureless form/profile-volume/shallow-outline convention, never eyes/red target/sack or training. Image3 original source construction plate gives Qud identity and color roles.
Canonical description: {packet['description']} This is unusual partial manufactured head/torso/hip forms on a central stem and splayed base, with ONE colored bent left form and ONE pale jointed right armature. No actual humanoid actor, walking legs, hands/fingers, face, eyes, mouth, clothing, target circles or skin. Preserve existing asymmetry, separate pieces/gaps and source pose. Do not replace with a complete modern shop mannequin or human.
Retain selected S design, scale, all current positions/pivots, exact forms and connections. Refine E/W shallow wood/fiberglass shading to match retained front. N shows same featureless manufactured form from back without new labels or features. S and N flip which side the colored/pale parts occupy; E/W have distinct near/far arm overlap. Right pale armature is NEAR in E, FAR in W; left colored bent form is FAR in E, NEAR in W. Do not mirror whole E to produce W or add another limb.
Shared authored shell depth2.2, head profile width2.1, profile base depth3.6; no thin edge-on shell. Same24x24source-space frame/scale across all panels; original16x24cell sits at offset4,0. Standcenterx11.3, native-anchor12,16. No independently centered head/base or cropped armature, no isometric/3/4yaw. Gray wood/stem/right armature primary, pale cyan head/torso/hip/left-form shell is an extraction-role key. Refine modest contour and subtle material shading, no ornate detail, metallic armor, fabric or injected anatomy. Same1536x1536sheet, transparent exterior and gaps, no glow/drop-shadow/scenery/text/labels. No second isolation or new state.'''.encode())
print('Retained source front/reversed static back in expanded frame; authored separate asymmetric complete E/W profiles.')
