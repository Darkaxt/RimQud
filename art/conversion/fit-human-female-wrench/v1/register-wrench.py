"""Select contextual metal inside fixed wrench geometry; complete hidden grip."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1024);FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
raw=np.array(read(HERE/'refined-red-context.png')).astype(float);pattern=np.array(read(HERE/'constructed-canonical.png'));envelope=pattern[:,:,3]>0
head=np.array(Image.open(HERE/'canonical-head-region.png').convert('L'));shaft=np.array(Image.open(HERE/'canonical-shaft-region.png').convert('L'))
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=248+(xx-256)*2;my=794+(yy-590)*2
rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1);gray=rgb.mean(2)
known=ndimage.binary_erosion(envelope,iterations=2)&(np.ptp(rgb,axis=2)<15)&(gray>45)&(gray<245)
assert (known&(head>128)).any() and (known&(shaft>128)&(head<128)).any(),'Both structural material regions require actual neutral source samples.'
unknown=envelope&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(envelope.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
    ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
ink=pattern[:,:,:3].mean(2);gray[(ink<90)&envelope]=ink[(ink<90)&envelope];assert np.isfinite(gray[envelope]).all()
v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;canonical=Image.fromarray(np.dstack([v,v,v,pattern[:,:,3]]));canonical.save(HERE/'intact-canonical.png')
detail=canonical.copy();detail.putalpha(Image.fromarray(np.uint8(np.round(np.minimum(pattern[:,:,3],shaft).astype(float)*(1-head/255)))));a=np.array(detail);a[a[:,:,3]==0,:3]=0;detail=Image.fromarray(a);detail.save(HERE/'shaft-canonical.png');Image.fromarray(np.uint8(unknown)*255).save(HERE/'canonical-continuation.png')
packet=json.loads((HERE/'source-packet.json').read_text());controls=json.loads((HERE/'fit-controls.json').read_text());bm=json.loads((BODY/'model.json').read_text());groups={k:{} for k in ['assembly','palette','full','off','grip']};registered={}
model=dict(item='Wrench',blueprint='Wrench',family='human-female',slot='Hand',laterality=1,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],observed_bindings=packet['observed_bindings'],weapon_metadata=packet['weapon_metadata'],views={},binding_scope='Female compatibility only; actual captured item is male Argyve519 ordinary Hand322/1. Side far-hand depth is an authoring proxy, not a new limb model.',policy='Complete hooked metal jaw/shaft with visible thread detail and lower grip. Head primary y, shaft detail c. Original body preserved; no decorative-prop size substitution or invented counterweight.',west_policy='Mirrored unmarked profile source for authoring; actual left/right near/far hand and native aim-state mapping pending.',pose='Stationary authoring display only. Ready one-handed side presentation must project forward/horizontally90deg to upright body; resting/ready/native offhand state remains unfinished.',native_acceptance='Pending full-set generation and native female compatibility, offhand and pose state.')
for facing,c in controls.items():
    def place(im):
        source=ImageOps.mirror(im) if c['mirror'] else im
        return source.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA')
    item=place(canonical);shaft_item=place(detail);item.save(HERE/f'intact-item-{facing}.png');shaft_item.save(HERE/f'item-detail-{facing}.png');body=read(BODY/f'selected-{facing}.png');hand=read(HERE/f'original-hand-{facing}.png');equipment=Image.alpha_composite(item,shaft_item)
    off=Image.alpha_composite(body,equipment);assembly=Image.alpha_composite(equipment,body) if facing!='south' else Image.alpha_composite(off,hand)
    assembly.save(HERE/f'assembled-{facing}.png');off.save(HERE/f'depth-off-{facing}.png')
    colored_item=Image.alpha_composite(tint(item,(177,201,195)),tint(shaft_item,(64,164,185)));body_color=tint(body,(119,191,207));hand_color=tint(hand,(119,191,207));colored=Image.alpha_composite(colored_item,body_color) if facing!='south' else Image.alpha_composite(Image.alpha_composite(body_color,colored_item),hand_color);colored.save(HERE/f'qud-palette-{facing}.png')
    for key,im in [('assembly',assembly),('palette',colored),('full',equipment),('off',off)]:groups[key][facing]=im
    gx,gy=c['grip'];groups['grip'][facing]=assembly.crop((gx-70,gy-160,gx+80,gy+95)).resize((240,408))
    rows=[]
    for component,stem,role,layer in [('item','intact-item','equipment',.0018 if facing=='south' else -.0002),('item-detail','item-detail','equipment-detail',.00181 if facing=='south' else -.00019),('body-overlay','original-hand','foreground',.0019)]:
        p=HERE/f'{stem}-{facing}.png';r=ref(p);row=dict(bm['views'][facing][0]);row.update(component=component,file=f'human-female-wrench-v1-{component}-{facing}.png',public_file=r['path'],sha256=r['sha256'],equipment_key='wrench@Hand@1',color_role=role,layer=layer);rows.append(row)
    model['views'][facing]=rows;registered[facing]=dict(inverse_affine=c['inverse_affine'],mirror=c['mirror'],item_space_grip=[256,590],body_hand_landmark=c['grip'],body=ref(BODY/f'selected-{facing}.png'),full_item=ref(HERE/f'intact-item-{facing}.png'),original_hand=ref(HERE/f'original-hand-{facing}.png'),body_pixels_changed=False)
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
def plate(images,name,title,zoom=False):
    out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,408 if zoom else 512)),(16+i*284,54));d.text((16+i*284,584),f.upper(),font=FONT,fill='#e3cf43')
    d.text((18,622),'Female compatibility only. Fixed body; armlength tool; native offhand/pose acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
for key,name,title,zoom in [('assembly','assembly-comparison.png','WRENCH / Qud hooked jaw and armlength shaft / female compatibility',False),('palette','independent-palette-comparison.png','PALETTE / primary head y, shaft c; body C illustrative and independent',False),('full','full-item-comparison.png','FULL METAL TOOL / complete jaw opening, neck, threaded iron and lower shaft',False),('off','depth-off-comparison.png','DEPTH OFF / full tool before original palm/body ownership',False),('grip','grip-comparison.png','GRIP / original front palm; side/back far tool under original body',True)]:plate(groups[key],name,title,zoom)
small=Image.new('RGB',(560,370),'#142823');draw=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*140+20,138),thumb);draw.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
write('model.json',model);write('registration-decisions.json',dict(raw=ref(HERE/'refined-red-context.png'),structural_gate=ref(HERE/'first-refinement-structural-review.json'),material_registration=dict(map_x='248+(x-256)*2',map_y='794+(y-590)*2',known_pixels=int(known.sum()),completed_pixels=int(unknown.sum()),method='Neutral samples from the same front contextual output inside fixed full tool. Harmonic hidden-grip completion; exact canonical alpha, jaw opening and constructed ink restored.',excluded='Red mannequin, glow/backdrop, accidental fill in the open jaw and generated body/edge changes.'),views=registered,new_imagegen_calls=1,second_isolation_call=False,pose_followup=model['pose']))
print('Registered full hooked wrench and separate y/c material; original body unchanged, authoring inspection pending.')
