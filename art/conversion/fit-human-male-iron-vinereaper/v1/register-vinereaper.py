"""Keep original crescent/shaft geometry; same contextual iron, male hand depth."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male/v2';SIZE=(512,1024);FACES=['south','east','north'];FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
 a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
packet=json.loads((HERE/'source-packet.json').read_text());item_scale=packet['frame']['item_scale'];pa=np.array(read(HERE/'constructed-canonical.png'));envelope=pa[:,:,3]>0;raw=np.array(read(HERE/'refined-red-context.png')).astype(float);assert raw.shape==(1024,1536,4)
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=276+(xx-256)*2*item_scale;my=790+(yy-580)*2*item_scale
rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1);gray=rgb.mean(2)
known=ndimage.binary_erosion(envelope,iterations=3)&(np.ptp(rgb,axis=2)<12)&(gray>70)&(gray<225)
assert known.sum()>7000
unknown=envelope&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(envelope.shape,-1,np.int32);ids[uy,ux]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
 ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg),rhs)
pg=pa[:,:,:3].mean(2);gray[(pg<90)&envelope]=pg[(pg<90)&envelope];assert np.all(np.isfinite(gray[envelope]));v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;canonical=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));canonical.save(HERE/'intact-canonical.png')
region=np.array(Image.open(HERE/'canonical-shaft-region.png').convert('L'));headregion=np.array(Image.open(HERE/'canonical-head-region.png').convert('L'));detailitem=canonical.copy();detailitem.putalpha(Image.fromarray(np.uint8(np.round(np.minimum(pa[:,:,3],region).astype(float)*(1-headregion/255)))));detailarray=np.array(detailitem);detailarray[detailarray[:,:,3]==0,:3]=0;detailitem=Image.fromarray(detailarray);detailitem.save(HERE/'shaft-canonical.png');Image.fromarray(np.uint8(unknown)*255).save(HERE/'canonical-continuation.png')
controls=json.loads((HERE/'fit-controls.json').read_text());bm=json.loads((BODY/'model.json').read_text());packet=json.loads((HERE/'source-packet.json').read_text());rows={};palette={};full={};grips={};registered={};off={}
model=dict(item='Iron Vinereaper',blueprint='Iron Vinereaper',family='human-male',slot='Hand',laterality=2,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],views={},observed_bindings=packet['observed_bindings'],weapon_metadata=packet['weapon_metadata'],item_raster_scale=item_scale,binding_scope='Five actual ordinary male Hand/2 bindings, no mutation managers. Shared base fit does not complete named NPC cosmetics/outfits.',policy='Full forged crescent and shaft; same canonical physical size as female fitting; separate material regions and original gripping hand. No unrelated costume/generated body.',west_policy='Mirrored east, opposite unmarked metal surface; actual native hand/aim-state acceptance pending final assembly.',pose='Provisional stationary authoring display, grip580 near lower shaft end. Ready side pose must project forward/horizontally about90deg to upright body; actual resting/ready poses pending final assembly.',native_acceptance='Pending full-set generation gate and actual native equipment/pose state')
for f in FACES:
 c=controls[f];a=c['inverse_affine']
 def place(im):
  source=ImageOps.mirror(im) if c['mirror'] else im
  return source.transform(SIZE,Image.Transform.AFFINE,a,Image.Resampling.BICUBIC)
 item=place(canonical);hilt=place(detailitem);item.save(HERE/f'intact-item-{f}.png');hilt.save(HERE/f'item-detail-{f}.png');hand=read(HERE/f'original-hand-{f}.png');body=read(BODY/f'selected-{f}.png');equipment=Image.alpha_composite(item,hilt)
 allover=Image.alpha_composite(body,equipment);assembly=Image.alpha_composite(equipment,body) if f=='north' else Image.alpha_composite(allover,hand);assembly.save(HERE/f'assembled-{f}.png');allover.save(HERE/f'depth-off-{f}.png')
 bodycol=tint(body,(207,192,65));handcol=tint(hand,(207,192,65));itemcol=Image.alpha_composite(tint(item,(177,201,195)),tint(hilt,(177,201,195)));colored=Image.alpha_composite(itemcol,bodycol) if f=='north' else Image.alpha_composite(Image.alpha_composite(bodycol,itemcol),handcol);colored.save(HERE/f'qud-palette-{f}.png')
 rows[f]=assembly;palette[f]=colored;full[f]=equipment;off[f]=allover;cx,cy=c['grip'];grips[f]=assembly.crop((cx-65,cy-120,cx+80,cy+80)).resize((290,400),Image.Resampling.LANCZOS)
 model['views'][f]=[]
 for component,path,role,layer in [('item',HERE/f'intact-item-{f}.png','equipment',-.0002 if f=='north' else .0018),('item-detail',HERE/f'item-detail-{f}.png','equipment-detail',-.00019 if f=='north' else .00181),('body-overlay',HERE/f'original-hand-{f}.png','foreground',.0019)]:
  row=dict(bm['views'][f][0]);r=ref(path);row.update(component=component,file='human-male-iron-vinereaper-v1-'+component+'-'+f+'.png',public_file=r['path'],sha256=r['sha256'],equipment_key='iron-vinereaper@Hand@2',color_role=role,layer=layer);model['views'][f].append(row)
 registered[f]=dict(inverse_affine=a,mirror=c['mirror'],item_space_grip=[256,580],grip_relation='38px above shaft end; independent original-body hand anchor',body_hand_landmark=c['grip'],body=ref(BODY/f'selected-{f}.png'),intact_item=ref(HERE/f'intact-item-{f}.png'),original_hand=ref(HERE/f'original-hand-{f}.png'),item_scale_relative_to_canonical=item_scale,physical_item_scale_changed=False,body_pixels_changed=False)
for group in [rows,palette,full,grips,off]:group['west (mirror)']=ImageOps.mirror(group['east'])
def plate(images,name,title,zoom=False):
 out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(images.items()):
  bg=Image.new('RGBA',im.size if zoom else SIZE,'#20382d');bg.alpha_composite(im);bg=bg.resize((256,353) if zoom else (256,512),Image.Resampling.LANCZOS);x,y=16+i*284,54;out.paste(bg.convert('RGB'),(x,y));d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,622),'Fixed ordinary base; stationary authoring display only. Native resting/ready pose acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
plate(rows,'assembly-comparison.png','MALE / IRON VINEREAPER / fixed crescent and lower grip / stationary display')
plate(palette,'independent-palette-comparison.png','SOURCE PALETTE / Mehmet522 W example; iron head y and shaft y')
plate(full,'full-item-comparison.png','FULL TOOL / complete crescent and shaft before original-body depth')
plate(off,'depth-off-comparison.png','DEPTH OFF / full tool over base; compare original hand/body ownership')
plate(grips,'grip-comparison.png','GRIP CLOSE-UP / original palm over lower shaft / independent tool source',True)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(rows.items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',dict(raw=ref(HERE/'refined-red-context.png'),material_registration=dict(column='south only; same reusable flat tool',map_x='276+(x-256)*2*item_scale',map_y='790+(y-580)*2*item_scale',item_scale=item_scale,known_pixels=int(known.sum()),completed_pixels=int(unknown.sum()),method='Actual neutral iron surface within constructed geometry; hidden-grip harmonic continuation, exact original alpha/ink. Shaft detail excludes overlapping head region. Full item before body depth.',excluded='Opaque glow, red mannequin/reflection, changed generated anatomy/geometry. No new wood or bindings inferred.'),views=registered,new_imagegen_calls=1,second_isolation_call=False,pose_followup=model['pose']))
print('Registered full iron crescent/shaft and lower male grip; body unchanged, native pose acceptance pending.')
female_body=json.loads((ROOT/'art/conversion/body-human-female/v2/model.json').read_text());male_body=bm
for axis in ['width','height']:assert abs(male_body['views']['south'][0][axis]*item_scale-female_body['views']['south'][0][axis])<1e-12
scaleplate=Image.new('RGB',(1152,690),'#142823');d=ImageDraw.Draw(scaleplate);d.text((18,12),'ONE CANONICAL VINEREAPER / shared physical mapping, different body/hand landmarks',font=FONT,fill='#e3cf43')
for i,(family,f) in enumerate([('female','south'),('male','south'),('female','east'),('male','east')]):
 folder=HERE if family=='male' else ROOT/'art/conversion/fit-human-female-iron-vinereaper/v1';im=read(folder/f'assembled-{f}.png');factor=male_body['pixel_world_scale']/female_body['pixel_world_scale'] if family=='male' else 1;im=im.resize((round(256*factor),round(512*factor)),Image.Resampling.LANCZOS);x=16+i*284+(256-im.width)//2;y=560-round(475*factor);bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);scaleplate.paste(bg.convert('RGB'),(x,y));d.line((16+i*284,560,271+i*284,560),fill='#70b8b0');d.text((16+i*284,592),family.upper()+' / '+f.upper(),font=FONT,fill='#e3cf43')
d.text((18,628),'Male raster scale0.9828877005 compensates its larger world/pixel factor; item world size unchanged.',font=FONT,fill='#e5e8d8');d.text((18,653),'Authoring/world-coordinate comparison only; native equipped-state and ready/resting poses pending.',font=FONT,fill='#e5e8d8');scaleplate.save(HERE/'cross-body-scale-comparison.png')
