"""Same contextual stone surface, immutable body, item-space grip and late depth."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1024);FACES=['south','east','north'];FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
 a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
pa=np.array(read(HERE/'constructed-canonical.png'));envelope=pa[:,:,3]>0;raw=np.array(read(HERE/'refined-red-context.png')).astype(float);assert raw.shape==(1024,1536,4)
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=225+(xx-256)*2.48;my=270+(yy-450)*2.48
rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
detail=np.array(Image.open(HERE/'canonical-detail.png').convert('L'));gray=rgb.mean(2)
# Refinement shifted/scaled the picture and made a glow: sample neutral stone only,
# then keep exact authored alpha/outline. Exclude its bright powder from base stone.
known=ndimage.binary_erosion(envelope,iterations=3)&(np.ptp(rgb,axis=2)<9)&(gray>85)&(gray<225)&~ndimage.binary_dilation(detail>0,iterations=3)
assert known.sum()>1000
unknown=envelope&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(envelope.shape,-1,np.int32);ids[uy,ux]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
 ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg),rhs)
pg=pa[:,:,:3].mean(2);gray[(pg<70)&envelope]=pg[(pg<70)&envelope];assert np.all(np.isfinite(gray[envelope]));v=np.uint8(np.clip(np.round(gray),0,255));canonical=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));canonical.save(HERE/'intact-canonical.png')
dv=np.full_like(v,239);detailitem=Image.fromarray(np.dstack([dv,dv,dv,np.uint8(np.round(pa[:,:,3].astype(float)*detail/255))]));detailitem.save(HERE/'powder-canonical.png');Image.fromarray(np.uint8(unknown)*255).save(HERE/'canonical-continuation.png')
controls=json.loads((HERE/'fit-controls.json').read_text());bm=json.loads((BODY/'model.json').read_text());packet=json.loads((HERE/'source-packet.json').read_text());rows={};palette={};full={};grips={};registered={}
model=dict(item='Pestle',blueprint='Pestle',family='nima',slot='Hand',laterality=6,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],views={},observed_binding=packet['observed_binding'],binding_scope='Reusable complete item plus ordinary-hand illustrative source. Does not place actual mutation-managed Hand181/6.',policy='Fixed body; one item; explicit item-space lower grip; original hand above full tool. No clothing or per-limb model invention.',west_policy='Profile mirror illustrates the ordinary base only; actual mutation-hand handedness unresolved.',pose='Provisional ordinary resting display. Ready/drafted pose/state mapping pending Stage 3 final assembly.',native_acceptance='Pending full-set generation gate, mutation hand placement and actual equipment/pose state')
for f in FACES:
 c=controls[f];a=list(c['inverse_affine']);a[5]+=20 # source contact (256,585), 30px above lower end; body hand unchanged
 if f=='north':
  # Avoid hiding the entire bulb behind the forearm in this illustrative resting pose.
  angle=math.radians(-20);co,si=math.cos(angle),math.sin(angle);gx,gy=c['grip'];a=[co,-si,256-co*gx+si*gy,si,co,585-si*gx-co*gy]
 def place(im):return im.transform(SIZE,Image.Transform.AFFINE,a,Image.Resampling.BICUBIC)
 item=place(canonical);powder=place(detailitem);item.save(HERE/f'intact-item-{f}.png');powder.save(HERE/f'item-detail-{f}.png');hand=read(HERE/f'original-hand-{f}.png');body=read(BODY/f'selected-{f}.png')
 equipment=Image.alpha_composite(item,powder);assembly=Image.alpha_composite(equipment,body) if f=='north' else Image.alpha_composite(Image.alpha_composite(body,equipment),hand);assembly.save(HERE/f'assembled-{f}.png')
 bodycol=tint(body,(0,148,3));handcol=tint(hand,(0,148,3));itemcol=Image.alpha_composite(tint(item,(177,201,195)),powder);colored=Image.alpha_composite(itemcol,bodycol) if f=='north' else Image.alpha_composite(Image.alpha_composite(bodycol,itemcol),handcol);colored.save(HERE/f'qud-palette-{f}.png')
 rows[f]=assembly;palette[f]=colored;full[f]=equipment;cx,cy=c['grip'];grips[f]=assembly.crop((cx-55,cy-150,cx+75,cy+85)).resize((260,470),Image.Resampling.LANCZOS)
 model['views'][f]=[]
 for component,path,role,layer in [('item',HERE/f'intact-item-{f}.png','equipment',-.0002 if f=='north' else .0018),('item-detail',HERE/f'item-detail-{f}.png','equipment-detail',-.00019 if f=='north' else .00181),('body-overlay',HERE/f'original-hand-{f}.png','foreground',.0019)]:
  row=dict(bm['views'][f][0]);r=ref(path);row.update(component=component,file='nima-pestle-v1-'+component+'-'+f+'.png',public_file=r['path'],sha256=r['sha256'],equipment_key='pestle@Hand@6',color_role=role,layer=layer);model['views'][f].append(row)
 registered[f]=dict(inverse_affine=a,item_space_grip=[256,585],original_context_grip=[256,565],body_hand_landmark=c['grip'],north_angle_correction='20 degrees outward; avoids total forearm occlusion in ordinary preview' if f=='north' else None,body=ref(BODY/f'selected-{f}.png'),intact_item=ref(HERE/f'intact-item-{f}.png'),original_hand=ref(HERE/f'original-hand-{f}.png'),item_scale_changed=False,body_pixels_changed=False)
for group in [rows,palette,full,grips]:group['west (mirror)']=ImageOps.mirror(group['east'])
def plate(images,name,title,zoom=False):
 out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(images.items()):
  if zoom:bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);bg=bg.resize((256,463),Image.Resampling.LANCZOS)
  else:bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);bg=bg.resize((256,512),Image.Resampling.LANCZOS)
  x,y=16+i*284,54;out.paste(bg.convert('RGB'),(x,y));d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,622),'Ordinary-base illustration; actual extra-hand placement and native weapon poses remain pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
plate(rows,'assembly-comparison.png','PESTLE / lower handle grip / one item over fixed ordinary human base')
plate(palette,'independent-palette-comparison.png','SOURCE PALETTE / body g; stone y; powder Y / independent roles')
plate(full,'full-item-comparison.png','COMPLETE PESTLE / full stone and powder before body/hand occlusion')
plate(grips,'grip-comparison.png','GRIP CLOSE-UP / original hand over shaft / lower item-space contact',True)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(rows.items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',dict(raw=ref(HERE/'refined-red-context.png'),material_registration=dict(column='south only; axially symmetric reusable source',canonical_anchor=[256,450],generated_anchor=[225,270],scale=2.48,known_pixels=int(known.sum()),completed_pixels=int(unknown.sum()),method='Neutral contextual stone only; harmonic continuation of hidden grip, own outline and complete alpha; separate powder geometry',excluded='Opaque red glow, generated body/hand, shifted geometry and bright generated powder'),views=registered,new_imagegen_calls=1,second_isolation_call=False,pose_followup=model['pose']))
print('Registered full neutral pestle and lower grip, separate powder, original hands; mutation/pose acceptance pending.')
