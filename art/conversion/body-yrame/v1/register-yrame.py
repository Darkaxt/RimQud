"""Register source-exact female body and separate authored additional leg pair."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,re,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';SIZE=(512,1024)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not OUT.exists();OUT.mkdir()
packet=read(HERE/'source-packet.json');body=read(ROOT/packet['baseline']['path']);assert ref(ROOT/packet['baseline']['path'])==packet['baseline']
row=body['views']['south'][0];frame=dict(canvas=[512,1024],contact=[256,950],**{k:row[k] for k in ['width','height','center_x','center_z']},method='Exact original body/head pixels in their existing common frame. Added pair shares contact and physical scale; no independent bounding-box fitting.')
raw=np.array(Image.open(HERE/'composed-refinement-raw.png').convert('RGBA'));g=raw[:,:,:3].astype(float).mean(2);y,x=np.indices(g.shape);sample=(raw[:,:,3]>250)&(y>510)&(y<790)&(g>160)&(g<250)
low,high=np.percentile(g[sample],[15,80]);assert 160<low<high<251
first=read(HERE/'first-structural-review.json')['sampled_limb_luminance']
review=dict(status='USABLE FOUR-FOOT COMPOSED SURFACE REFERENCE; BASELINE REDRAW REJECTED',
    accepted='Both actual outputs retain four feet in front/back, human anatomy and strict cardinal facing. Composed output has restrained gray leg surfaces and rounded toes.',
    differences=['The second output again redraws the baseline head/body/ordinary legs and changes profile spacing/overlap; those pixels are not a replacement for the registered shared race body.','Generated text and transparent-edge noise are excluded from registered layers.'],
    registration='Keep the patched editable leg contours, original body/head RGBA and contact exactly. Transfer only measured neutral luminance range to added-leg gradients. No generated body extraction, new source anatomy or additional prompt loop.',
    sampled_limb_luminance=[float(low),float(high)],sample_region='alpha>250,y510:790,grayscale160:250 in actual composed output',native_activation=False)
write(HERE/'composed-structural-review.json',review)
receipts=[]
for prompt,raw_name,raw_file in [('secondary-views-prompt.txt','secondary-views-raw.png','exec-782d1a40-f5ff-42fa-8b6f-ae7d71f9a16e.png'),('composed-refinement-prompt.txt','composed-refinement-raw.png','exec-0b39b839-0628-4c8f-a686-89d314510b38.png')]:
    receipts.append(dict(tool='built-in image_gen.imagegen',prompt=ref(HERE/prompt),output=ref(HERE/raw_name),original_generated_filename=raw_file,transparent_background=True,
        referenced_images=[ref(HERE/('constructed-turnaround.png' if prompt.startswith('secondary') else 'patched-turnaround.png')),ref(HERE/'source-reference-baseline.png')]))
write(HERE/'generation-receipts.json',dict(actual_calls=receipts,new_calls=2,rule='Exact original outputs retained. Both are proposals; registration restores fixed source geometry rather than silently accepting baseline redraw.'))
roles=dict(captured_tile_color='w',captured_foreground='B',captured_detail='B',body_and_added_legs='foreground/tileColor w',
    detail_assignment='No body pixels assigned to native B detail during this phase. Exact semantic region is not exported. Rime-vein/icy-particle appearance is mutation/cosmetic work outside the initial body phase; B is retained for later native/effect mapping, not invented as permanent blue skin.',
    base_neutral='All production RGB is grayscale; no fixed biological skin colour or blue pixels.',native_activation=False)
write(HERE/'source-palette-roles.json',roles)
views={};groups={k:{} for k in ['neutral','native','extra-legs','extra-legs-alpha']};palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];color=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8)
for f in ['south','east','north','west']:
    source='east' if f=='west' else f;mirror=f=='west';rows=[]
    def add(p,component,layer,**metadata):
        rows.append(dict(component=component,file=p.name,public_file=p.relative_to(ROOT).as_posix(),sha256=ref(p)['sha256'],size=list(SIZE),contact=frame['contact'],color_role='foreground',
            **{k:frame[k] for k in ['width','height','center_x','center_z']},layer=layer,**metadata))
    for r in body['views'][source]:
        im=Image.open(ROOT/r['public_file']).convert('RGBA');im=ImageOps.mirror(im) if mirror else im;p=OUT/f'{r["component"]}-{f}.png';im.save(p)
        add(p,r['component'],r['layer'],original_component=dict(path=r['public_file'],sha256=r['sha256']),mirrored_from_east=mirror)
    svg=(HERE/f'patched-extra-legs-{source}.svg').read_text()
    # Replace just gradient stop values, retaining every path/outline and mask edge.
    stops=iter([round(low),round(high),round(low-5)])
    svg=re.sub(r'(<stop\b[^>]*stop-color=")#[0-9a-fA-F]{6}("/>)',lambda m:m[1]+'#'+f'{next(stops):02x}'*3+m[2],svg)
    editable_svg=svg.replace('</defs>','</defs><g transform="translate(512 0) scale(-1 1)">').replace('</svg>','</g></svg>') if mirror else svg
    (OUT/f'extra-legs-{f}.svg').write_bytes(editable_svg.encode())
    import io
    im=Image.open(io.BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA');im=ImageOps.mirror(im) if mirror else im
    p=OUT/f'extra-legs-{f}.png';im.save(p);add(p,'mutation-extra-legs',-.002,native_part=298,parent_part=287,manager='515::MultipleLegs::Add',baseline_feet_group=297,
        anatomy_role='One separate additional human leg/foot pair behind unchanged paired baseline legs. Full profile uses natural far-limb overlap.',mirrored_from_east=mirror)
    groups['extra-legs'][f]=im
    alpha=Image.new('RGBA',SIZE,'white');alpha.putalpha(im.getchannel('A'));alpha.save(OUT/f'extra-legs-alpha-{f}.png');groups['extra-legs-alpha'][f]=alpha
    views[f]=sorted(rows,key=lambda r:r['layer']);n=Image.new('RGBA',SIZE);c=Image.new('RGBA',SIZE)
    for r in views[f]:
        im=Image.open(ROOT/r['public_file']).convert('RGBA');n.alpha_composite(im);a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;c.alpha_composite(Image.fromarray(a))
    n.save(OUT/f'neutral-{f}.png');c.save(OUT/f'native-{f}.png');groups['neutral'][f]=n;groups['native'][f]=c
model=dict(entry='BODY-YRAME',kind='fixed_named_anatomy_with_separate_mutation_art',source=ref(HERE/'source-packet.json'),baseline_model=packet['baseline'],leg_geometry=ref(HERE/'leg-construction.json'),corrections=ref(HERE/'manual-corrections.json'),palette_roles=ref(HERE/'source-palette-roles.json'),views=views,registration=frame,
    separation='Exact original body/head retained. One additional paired-leg texture is separate mutation art, not a new human race baseline or an articulated limb framework.',
    source_anatomy=packet['anatomy'],west_policy='Mirror east for the symmetric ordinary body and added leg pair; longitudinal Feet groups remain unchanged, not reassigned by bitmap facing.',
    equipped_feet='Boots580 actually equip only original changed Feet297/16. Added Feet298/64 remain unequipped. Horns575 remain separate actual Head288 equipment, not part of this body.',
    refinement='Both actual outputs retained as coherent four-foot anatomy/shading proposals. Their baseline redraws are rejected; only measured neutral surface range informs fixed editable leg gradients.',
    native_activation=False,native_acceptance='Pending full-set generation gate: actual body/mutation/feet slots, four-item outfit, visibility/equip/hurt/look/save and source-supported held/native effect state review. No blue rime/particle effect is claimed by this body.')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(frame=frame,body_pixels='Original RGBA exact, including hidden RGB at alpha0; no resampling.',first_limb_luminance=first,composed_limb_luminance=[float(low),float(high)],
    editable_geometry='Rounded additional-foot contours and toe curves retained; gradient values alone derive from generated proposals. Original pelvis/arms/legs/head remain exact.',source_colour=roles,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for name,group in groups.items():
    sheet=Image.new('RGB',(1152,680),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / '+name+' / exact baseline + separate added pair',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(group.items()):
        xx=16+i*284;im=im.resize((256,512),Image.Resampling.LANCZOS);sheet.paste(im,(xx,55),im);d.line((xx+128,55,xx+128,567),fill='#a39846');d.line((xx,530,xx+256,530),fill='#75aaa0');d.text((xx,585),f.upper(),font=font,fill='#e3cf43')
    d.text((18,625),'FOUR feet total. Neutral base; no gear, cosmetic rime pattern or native acceptance.',font=font,fill='#e5e8d8');sheet.save(OUT/f'{name}-comparison.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / 48x96 frame, neutral then captured tileColor w',font=font,fill='#e3cf43')
for j,key in enumerate(['neutral','native']):
    yy=65+j*285
    for i,(f,im) in enumerate(groups[key].items()):
        small=im.resize((48,96),Image.Resampling.LANCZOS);sheet.paste(small,(20+i*200,yy),small);large=small.resize((72,144),Image.Resampling.NEAREST);sheet.paste(large,(95+i*200,yy),large);d.text((20+i*200,yy+185),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'B detail retained as source metadata; no invented permanent blue skin region.',font=font,fill='#e5e8d8');sheet.save(OUT/'game-scale-comparison.png')
print('Registered four facings, source-exact body/head and separate added leg pair; final visual review pending.')
