"""Small folding knife: original geometry/pivot, contextual dull surface, late hand depth."""
from pathlib import Path
import hashlib,json
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
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=2*xx-280;my=2*yy-570
rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1);gray=rgb.mean(2)
known=ndimage.binary_erosion(envelope,iterations=3)&(np.ptp(rgb,axis=2)<12)&(gray>70)&(gray<225)
for component in ['blade','handle']:
 region=np.array(Image.open(HERE/f'canonical-{component}-region.png').convert('L'))>0
 assert np.any(known&region),component # Each material has an observed contextual boundary.
unknown=envelope&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(envelope.shape,-1,np.int32);ids[uy,ux]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
 ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg),rhs)
pg=pa[:,:,:3].mean(2);blade_region=np.array(Image.open(HERE/'canonical-blade-region.png').convert('L'));ink=((pg<90)|((pg<170)&(blade_region>0)))&envelope;gray[ink]=pg[ink];assert np.all(np.isfinite(gray[envelope]));v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;canonical=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));canonical.save(HERE/'intact-canonical.png')
region=np.array(Image.open(HERE/'canonical-handle-region.png').convert('L'));headregion=np.array(Image.open(HERE/'canonical-blade-region.png').convert('L'));detailitem=canonical.copy();detailitem.putalpha(Image.fromarray(np.uint8(np.round(np.minimum(pa[:,:,3],region).astype(float)*(1-headregion/255)))));da=np.array(detailitem);da[da[:,:,3]==0,:3]=0;detailitem=Image.fromarray(da);detailitem.save(HERE/'handle-canonical.png');Image.fromarray(np.uint8(unknown)*255).save(HERE/'canonical-continuation.png')
controls=json.loads((HERE/'fit-controls.json').read_text());bm=json.loads((BODY/'model.json').read_text());packet=json.loads((HERE/'source-packet.json').read_text());rows={};palette={};full={};grips={};registered={};off={}
model=dict(item='Steel Utility Knife',blueprint='Steel Utility Knife',family='human-female',slot='Hand',laterality=2,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],views={},observed_bindings=packet['observed_bindings'],weapon_metadata=packet['weapon_metadata'],binding_scope='Female compatibility template only. Source item is actual male Argyve588 on Hand320/2; no female equipped observation.',policy='One small folding knife, full open blade/handle/pivot, separate Y/y regions, original hand above full item. No imagined narrative painting or generated body.',west_policy='Mirrored opposite generic blade side; actual item-specific painted graphic not exported. Native hand/aim-state acceptance pending.',pose='Stationary authoring display, grip590 near lower handle. Ready side pose must project horizontally/forward90deg to upright body; native resting/ready states pending.',native_acceptance='Pending full-set generation gate, actual female compatibility/equipped and resting-ready state')
for f in FACES:
 c=controls[f];a=c['inverse_affine']
 def place(im):
  source=ImageOps.mirror(im) if c['mirror'] else im
  return source.transform(SIZE,Image.Transform.AFFINE,a,Image.Resampling.BICUBIC)
 item=place(canonical);hilt=place(detailitem);item.save(HERE/f'intact-item-{f}.png');hilt.save(HERE/f'item-detail-{f}.png');hand=read(HERE/f'original-hand-{f}.png');body=read(BODY/f'selected-{f}.png');equipment=Image.alpha_composite(item,hilt)
 allover=Image.alpha_composite(body,equipment);assembly=Image.alpha_composite(equipment,body) if f=='north' else Image.alpha_composite(allover,hand);assembly.save(HERE/f'assembled-{f}.png');allover.save(HERE/f'depth-off-{f}.png')
 bodycol=tint(body,(119,191,207));handcol=tint(hand,(119,191,207));itemcol=Image.alpha_composite(tint(item,(255,255,255)),tint(hilt,(177,201,195)));colored=Image.alpha_composite(itemcol,bodycol) if f=='north' else Image.alpha_composite(Image.alpha_composite(bodycol,itemcol),handcol);colored.save(HERE/f'qud-palette-{f}.png')
 rows[f]=assembly;palette[f]=colored;full[f]=equipment;off[f]=allover;cx,cy=c['grip'];grips[f]=assembly.crop((cx-65,cy-120,cx+80,cy+80)).resize((290,400),Image.Resampling.LANCZOS)
 model['views'][f]=[]
 for component,path,role,layer in [('item',HERE/f'intact-item-{f}.png','equipment',-.0002 if f=='north' else .0018),('item-detail',HERE/f'item-detail-{f}.png','equipment-detail',-.00019 if f=='north' else .00181),('body-overlay',HERE/f'original-hand-{f}.png','foreground',.0019)]:
  row=dict(bm['views'][f][0]);r=ref(path);row.update(component=component,file='human-female-steel-utility-knife-v1-'+component+'-'+f+'.png',public_file=r['path'],sha256=r['sha256'],equipment_key='steel-utility-knife@Hand@2',color_role=role,layer=layer);model['views'][f].append(row)
 registered[f]=dict(inverse_affine=a,mirror=c['mirror'],item_space_grip=[256,590],grip_relation='30px above handle end; independent original-body hand anchor',body_hand_landmark=c['grip'],body=ref(BODY/f'selected-{f}.png'),intact_item=ref(HERE/f'intact-item-{f}.png'),original_hand=ref(HERE/f'original-hand-{f}.png'),item_scale_changed=False,body_pixels_changed=False)
for group in [rows,palette,full,grips,off]:group['west (mirror)']=ImageOps.mirror(group['east'])
def plate(images,name,title,zoom=False):
 out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(images.items()):
  bg=Image.new('RGBA',im.size if zoom else SIZE,'#20382d');bg.alpha_composite(im);bg=bg.resize((256,353) if zoom else (256,512),Image.Resampling.LANCZOS);x,y=16+i*284,54;out.paste(bg.convert('RGB'),(x,y));d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,622),'Female compatibility only; stationary authoring display. Actual equipped/ready/resting state pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
plate(rows,'assembly-comparison.png','FEMALE COMPATIBILITY / STEEL UTILITY KNIFE / small folding blade and lower grip')
plate(palette,'independent-palette-comparison.png','SOURCE PALETTE / illustrative body C; steel blade Y and handle y')
plate(full,'full-item-comparison.png','FULL KNIFE / open blade, pivot and handle before original-body depth')
plate(off,'depth-off-comparison.png','DEPTH OFF / full tool over base; compare original hand/body ownership')
plate(grips,'grip-comparison.png','GRIP CLOSE-UP / original palm over lower handle / source folding pivot',True)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(rows.items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',dict(raw=ref(HERE/'refined-red-context.png'),material_registration=dict(column='south only; one reusable knife',map_x='2*x-280',map_y='2*y-570',known_pixels=int(known.sum()),completed_pixels=int(unknown.sum()),method='Neutral dull/smudged surface in exact constructed alpha; hidden handle continuation, original contour/thumb nick/pivot. Handle detail excludes blade. Full source before body depth.',excluded='Opaque glow, red mannequin/reflections, altered generated contours/body. No imagined painting or fold mechanic.',implementation_correction='An inherited axe guard demanded7000 sampled pixels, exceeding this entire4683-pixel knife. Actual1687 neutral pixels sample both blade and handle; corrected helper requires observed material for each component. This was an implementation diagnostic, not native validation or a changed art acceptance criterion.'),views=registered,new_imagegen_calls=1,second_isolation_call=False,pose_followup=model['pose']))
print('Registered small folding knife and female compatibility grip; original body/pivot preserved, native states pending.')
# Same registered body frame, one item per panel. This compares tool sizes, not outfits.
comparison=Image.new('RGB',(900,670),'#142823');d=ImageDraw.Draw(comparison);d.text((18,14),'SAME FEMALE BASE / independent weapon sizes / stationary display only',font=FONT,fill='#e3cf43');versions=[]
for i,(name,folder) in enumerate([('UTILITY KNIFE v1',HERE),('VIBRO BLADE v1',ROOT/'art/conversion/fit-yrame-vibro-blade/v1'),('VINEREAPER v1',ROOT/'art/conversion/fit-human-female-iron-vinereaper/v1')]):
 cm=json.loads((folder/'model.json').read_text());assert cm['base_model']==ref(BODY/'model.json')['path'] and cm['canvas']==[512,1024] and cm['contact']==[256,950];im=read(folder/'assembled-south.png');bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);comparison.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(18+i*300,55));d.text((18+i*300,585),name,font=FONT,fill='#e3cf43');versions.append(dict(label=name,model=ref(folder/'model.json'),assembly=ref(folder/'assembled-south.png')))
d.text((18,626),'No equal-bounds normalization; estimates use source/class/proportions, not weight as length.',font=FONT,fill='#e5e8d8');comparison.save(HERE/'weapon-scale-comparison.png');write('scale-comparison-inputs.json',dict(body=ref(BODY/'model.json'),versions=versions,scope='One item per panel, unchanged common body frame; no combined outfit or native scale acceptance.'))
