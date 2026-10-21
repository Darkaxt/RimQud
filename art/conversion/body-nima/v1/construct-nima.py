"""Construct Nima's separate four-arm/spiral-tail art over the exact female base."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,1264);PAD=240;CONTACT=[256,1190]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='BODY-NIMA'
base_entry=next(e for e in ledger['entries'] if e['id']=='BODY-HUMAN-FEMALE');assert base_entry['generation_ready']
base_ref=base_entry['current_registration']['model'];assert ref(ROOT/base_ref['path'])==base_ref;base=json.loads((ROOT/base_ref['path']).read_text())
sources=json.loads((ROOT/'art/village/sources.json').read_text());row=next(r for r in sources['actors'] if r['creature']=='Nima Ruda');actor=next(a for a in row['native_instances'] if a['instance']==506)
preflight=json.loads((ROOT/'art/conversion/npc-nima-ruda/v1/source-packet.json').read_text());assert actor==preflight['captured_actor']
original=next(r for r in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if r['blueprint']=='Nima Ruda')
donor=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');mask=donor/original['reference_file'].replace('-reference','-mask');assert private(mask)['sha256']==original['native_mask_sha256']
mod=Path('D:/Steam/steamapps/workshop/content/294100/1055485938');tailref=mod/'Textures/Things/Pawn/Animal/Pulmonoscorpius'
references=[dict(**private(donor/f'human-body-female-{f}.png'),role='Actual Core ordinary female body cardinal presentation and outline/shading only.') for f in ['south','east','north']]
references += [dict(**private(tailref/f'megafauna_pulmonoscorpius_{f}.png'),role='Megafauna Pulmonoscorpius: segmented tail surface, joints and stinger readability only. Do not copy whole scorpion anatomy, purple palette, animal size, claws or game behavior.') for f in ['south','east','north']]
qud=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Creatures.xml')
fragment=re.search(r'<object\s+Name="Nima Ruda"[^>]*>.*?</object>',qud.read_text(encoding='utf-8-sig'),re.S).group()
old=base['views']['south'][0];sx=old['width']/512;sz=old['height']/1024
frame=dict(canvas=list(SIZE),padding_top=PAD,contact=CONTACT,baseline_canvas=[512,1024],baseline_contact=[256,950],width=old['width'],height=old['height']*1264/1024,center_x=0,center_z=old['center_z']+120*sz,
           method='Exact RGBA paste at integer y+240. No body resampling; physical pixel scale and ground remain identical. All equipment must inherit the same padding.')
packet=dict(entry='BODY-NIMA',recorded_at=datetime.now(timezone.utc).isoformat(),identity_chain=row['lineage'],race_description=row['race_input'],captured_actor=actor,
    source=ref(ROOT/'art/village/sources.json'),source_snapshot=sources['runtime_catalogue_sha256'],preflight=ref(ROOT/'art/conversion/npc-nima-ruda/v1/source-packet.json'),
    original=dict(**original,private_mask=private(mask)),native_definition=dict(**private(qud),fragment=fragment),baseline=base_ref,
    baseline_history=ref(ROOT/'art/conversion/body-human-female/v1/source-packet.json'),donor_references=references,mod=dict(name='Megafauna',package_id='Spino.Megafauna',workshop_id='1055485938',about=private(mod/'About/About.xml'),active_load_state='Not established; installed artwork reference only.'),
    anatomy=dict(baseline='Existing unmutated adult female body/head with two arms/hands and two feet, unchanged.',additions='Exactly one additional arm/hand pair plus one great segmented spiral Tail193/Stinger climbing from posterior pelvis over the back/neck. No extra legs, head, hands-face or scorpion claws.',
    native_parts=actor['parts'],part_mapping='Arm/Hand IDs and managers are retained as mechanical anatomy/equipment data, not render bones. Extra pair artwork is a neutral authored posture. Actual Pestle Hand181/6 and FloatingNearby195 remain individual assembly work.'),
    scope=preflight['scope_notes'],frame=frame,authored_interpretation='Tail length/radius, one ascending turn, segment count, facets, limb placement and unseen surfaces are authored from great/spiral/jeweled source cues. Segments are surface construction, not additional mechanical body parts. Do not infer exact dimensions or count from the tiny glyph.',
    depth='All tail views derive from one 3D centreline with cardinal orthographic projection. Split tail geometry by near/far side of the fixed body plane; retain the complete tail independently of final clothing masks.',
    native_activation=False,native_acceptance='Pending full-set generation and actual named anatomy/equipment/visibility/hurt/look/save/native held-state review.')
write(HERE/'source-packet.json',packet)
def svg(parts):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1264" viewBox="0 0 512 1264">'+''.join(parts)+'</svg>'
def save(name,parts):
    s=svg(parts);(HERE/(name+'.svg')).write_bytes(s.encode());(HERE/(name+'.png')).write_bytes(svg_to_bytes(svg_string=s))
def path(d,fill='#e3e3e3',stroke='#2b2b2b',width=8):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
left='M205 590 Q145 585 105 642 Q49 716 31 818 L23 899 Q33 919 55 907 L69 824 Q89 755 139 708 L208 665 Z'
right='M307 590 Q367 585 407 642 Q463 716 481 818 L489 899 Q479 919 457 907 L443 824 Q423 755 373 708 L304 665 Z'
arms_front=[path(left),path(right),'<ellipse cx="40" cy="923" rx="21" ry="22" fill="#e8e8e8" stroke="#2b2b2b" stroke-width="8"/><ellipse cx="472" cy="923" rx="21" ry="22" fill="#e8e8e8" stroke="#2b2b2b" stroke-width="8"/>']
arms_side=[path('M256 593 Q205 602 185 660 Q173 725 195 799 L210 897 Q204 918 184 917 L166 810 Q135 735 150 663 Q163 604 217 567 Z',fill='#cccccc'),
           path('M225 591 Q170 594 141 662 Q109 737 128 816 L141 905 Q155 925 176 912 L165 810 Q157 751 184 705 L245 657 Z'),
           '<ellipse cx="151" cy="930" rx="21" ry="22" fill="#e8e8e8" stroke="#2b2b2b" stroke-width="8"/><ellipse cx="198" cy="930" rx="18" ry="21" fill="#cccccc" stroke="#2b2b2b" stroke-width="7"/>']
# One world-space centreline, sampled by arclength; no per-view independent tail fitting.
t=np.linspace(0,1,160)[:,None];p0=np.array([.02,-.16,.55]);p1=np.array([-.20,-.23,.78]);p2=np.array([-.24,-.18,1.05]);p3=np.array([-.24,0,1.18])
rise=(1-t)**3*p0+3*(1-t)**2*t*p1+3*(1-t)*t**2*p2+t**3*p3
theta=np.linspace(np.pi,3*np.pi,400);coil=np.column_stack([.24*np.cos(theta),.24*np.sin(theta),np.linspace(1.18,1.43,len(theta))])
dense=np.concatenate([rise,coil[1:]]);arc=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(dense,axis=0),axis=1))]);samples=np.linspace(0,arc[-1],25)
centres=np.column_stack([np.interp(samples,arc,dense[:,j]) for j in range(3)])
write(HERE/'tail-construction.json',dict(centreline=centres.tolist(),units='Authored world units matched to existing body pixel/world mapping',segments=24,source_count='Native has one Tail193;24surface segments is an authored interpretation, not a metadata count.',projection='S:(x,z),E:(y,z),N:(-x,z),W:(-y,z); depth respectively y,x,-y,-x',source_dimensions='Unknown; great/spiral/segmented are native descriptions. Radius0.24 and height1.43 authored relative to the unchanged body.',frame=frame))
def projection(points,f):
    p=np.array(points);x=p[:,0] if f=='south' else (p[:,1] if f=='east' else -p[:,0]);depth=p[:,1] if f=='south' else (p[:,0] if f=='east' else -p[:,1])
    return np.column_stack([256+x/sx,1190-p[:,2]/sz]),depth
light=np.array([-.4,.25,.85]);light/=np.linalg.norm(light)
for f in ['south','east','north']:
    parts={'back':[],'front':[]};jewels={'back':[],'front':[]};polys=[]
    for index,(a,b) in enumerate(zip(centres[:-1],centres[1:])):
        axis=b-a;axis/=np.linalg.norm(axis);guide=np.array([0,0,1.]) if abs(axis[2])<.9 else np.array([1.,0,0]);u=np.cross(axis,guide);u/=np.linalg.norm(u);v=np.cross(axis,u)
        radius=.033-.009*index/23;angles=np.arange(8)*np.pi/4
        ring0=np.array([a+radius*(np.cos(w)*u+np.sin(w)*v) for w in angles]);ring1=np.array([b+radius*.94*(np.cos(w)*u+np.sin(w)*v) for w in angles])
        for k in range(8):
            points=np.array([ring0[k],ring0[(k+1)%8],ring1[(k+1)%8],ring1[k]])
            xy,depth=projection(points,f);normal=np.cos(angles[k]+np.pi/8)*u+np.sin(angles[k]+np.pi/8)*v
            luminance=int(np.clip(213+27*np.dot(normal,light),180,244));coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy)
            face=f'<polygon points="{coords}" fill="rgb({luminance},{luminance},{luminance})" stroke="#393939" stroke-width="2.5" stroke-linejoin="round"/>'
            key='front' if depth.mean()>0 else 'back';polys.append((float(depth.mean()),key,face))
        # Small pale facet suggests source jeweled segments; each is surface detail only.
        centre=(a+b)/2;xy,depth=projection([centre],f);x,y=xy[0];key='front' if depth[0]>0 else 'back'
        jewel=f'<path d="M{x:.2f} {y-6:.2f} L{x+5:.2f} {y:.2f} L{x:.2f} {y+6:.2f} L{x-5:.2f} {y:.2f}Z" fill="#f5f5f5" stroke="#777777" stroke-width="1.5"/>'
        jewels[key].append(jewel)
    for _,key,face in sorted(polys,key=lambda r:r[0]):parts[key].append(face)
    # The one hooked stinger and tiny bead are attached to the final tail point.
    tip=np.array([[-.24,0,1.43],[-.20,.07,1.425],[-.16,.11,1.39],[-.13,.12,1.32],[-.19,.095,1.375],[-.25,.015,1.40]])
    xy,depth=projection(tip,f);coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy);key='front' if depth.mean()>0 else 'back'
    parts[key].append(f'<polygon points="{coords}" fill="#d2d2d2" stroke="#2b2b2b" stroke-width="5" stroke-linejoin="round"/>')
    bead=np.array([[-.13,.12,1.302]]);xy,depth=projection(bead,f);x,y=xy[0];beadshape=f'<ellipse cx="{x:.3f}" cy="{y:.3f}" rx="4.5" ry="7" fill="#fafafa" stroke="#555555" stroke-width="2"/>'
    parts[key].append(beadshape);jewels[key].append(beadshape)
    for layer in ['back','front']:
        save(f'tail-{layer}-{f}',parts[layer]+jewels[layer]);save(f'tail-detail-{layer}-{f}',jewels[layer])
    save('extra-arms-'+f,arms_side if f=='east' else arms_front)
    baseline=Image.new('RGBA',SIZE)
    for r in base['views'][f]:
        p=ROOT/r['public_file'];assert ref(p)['sha256']==r['sha256'];baseline.alpha_composite(Image.open(p).convert('RGBA'),(0,PAD))
    baseline.save(HERE/f'baseline-{f}.png')
    out=Image.new('RGBA',SIZE)
    for name in ['tail-back','extra-arms']:out.alpha_composite(Image.open(HERE/f'{name}-{f}.png').convert('RGBA'))
    out.alpha_composite(baseline);out.alpha_composite(Image.open(HERE/f'tail-front-{f}.png').convert('RGBA'));out.save(HERE/f'constructed-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
out=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'NIMA / original female base + separate extra arms and one projected spiral tail',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((240,593),Image.Resampling.LANCZOS);out.paste(im,(40+i*330,55),im);d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Manual proposal; one shared 3D tail, fixed cardinal body and unchanged physical ground/scale.',font=font,fill='#e5e8d8');out.save(HERE/'constructed-turnaround.png')
print('Constructed current source packet, exact padded base, separate extra arm pair and shared-world spiral-tail views; review pending.')
