"""Keep source-bound mail geometry; register actual contextual linked-steel surface."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2'
FACES=['south','east','north'];SIZE=(512,1024);FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,col):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(col)/255));return Image.fromarray(a)
def complete(gray,known,envelope):
 unknown=envelope&~known;yy,xx=np.where(unknown);n=len(yy);ids=np.full(gray.shape,-1,np.int32);ids[yy,xx]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
 if n:
  # Each connected cloth component needs a known material boundary. Tiny hidden
  # components without a sampled pixel use the constructed neutral metal as authored material.
  labels,count=ndimage.label(envelope)
  for label in range(1,count+1):
   component=labels==label
   if not np.any(known&component):
    q=np.flatnonzero(component[yy,xx]);rhs[q]+=220;deg[q]+=1
  matrix=sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg);gray[yy,xx]=spsolve(matrix,rhs)
 return gray,unknown
def plate(name,rows,title):
 out=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);x,y=16+i*284,54;out.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(x,y));d.line((x+128,y,x+128,y+511),fill='#e3cf43');d.line((x,y+475,x+255,y+475),fill='#70b8b0');d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,622),'One mail shirt on fixed base. Full metal source and body depth separate; native acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)

raw=read(HERE/'refined-red-context.png');assert raw.size==(1536,1024)
packet=json.loads((HERE/'source-packet.json').read_text());bm=json.loads((BODY/'model.json').read_text())
model=dict(item='Chain Mail',blueprint='Chain Mail',family='yrame',slot='Body',laterality=0,workflow='regional-curved-v1',canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],views={},occlusion_sources={},
 policy='Actual Yrame Body287/item574, ordinary group0. One mail shirt on unmutated human base; named shape/mutations and full outfit remain unfinished.',
 layer_order='body/head -> full mail .0012 -> bright-loop detail .00125 -> selected original forearms/hands .0013; shirt owns its natural neckline',
 mask_semantics='white original body above item; black none; gray geometric edge coverage',
 west_policy='Mirror east; plain mail has no source-handed marking',native_acceptance='Pending all-conversions generation gate')
record=dict(source=ref(HERE/'refined-red-context.png'),body=ref(BODY/'model.json'),new_imagegen_call=True,second_isolation_call=False,generated_body_used=False,
 method='Sample neutral linked-steel material only from actual contextual output through recorded torso zoom. Complete concealed/excluded surface on full authored mail before fitting. Restore source seams/scars, retain full source alpha and apply original-body ownership last. Identity fit; constructed mail already matches fixed body landmarks.',
 exclusions='Opaque glow, red mannequin, colored reflections, generated contours/anatomy and dark foreign body ink are not registered as metal. Tiny isolated hidden components without observed surface retain authored neutral construction.',
 zoom=dict(crop=[64,190,448,750],size=[461,672],origin=[25,176]),views={})
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=(xx-64)*(461/384)+25;my=(yy-190)*1.2+176
groups={k:{} for k in ['assembly','cloth','overlay','mask','detail','continued','off','palette']}
colors={k:tuple(bytes.fromhex(v)) for k,v in json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'].items()}
for i,f in enumerate(FACES):
 pattern=read(HERE/f'constructed-cloth-{f}.png');pa=np.array(pattern);envelope=pa[:,:,3]>0
 cell=np.array(raw.crop((i*512,0,(i+1)*512,1024))).astype(float)
 rgb=np.stack([ndimage.map_coordinates(cell[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
 red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3)
 known=ndimage.binary_erosion(envelope,iterations=3)&(rgb.max(2)-rgb.min(2)<35)&(rgb.mean(2)>20)&~ndimage.binary_dilation(red,iterations=2)
 assert known.sum()>500,f
 gray,unknown=complete(rgb.mean(2),known,envelope);pg=pa[:,:,:3].mean(2);gray[(pg<90)&envelope]=pg[(pg<90)&envelope]
 assert np.all(np.isfinite(gray[envelope])),f
 v=np.uint8(np.clip(np.round(gray),0,255));cloth=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));cloth.save(HERE/f'intact-mail-{f}.png')
 Image.fromarray(np.uint8(unknown)*255).save(HERE/f'authored-continuation-{f}.png')
 region=np.array(Image.open(HERE/f'detail-region-{f}.png').convert('L'));detail=cloth.copy();detail.putalpha(Image.fromarray(np.uint8(np.round(pa[:,:,3].astype(float)*region/255))));detail.save(HERE/f'item-detail-{f}.png')
 body=read(BODY/f'selected-{f}.png');ba=np.array(body);mask=Image.open(HERE/f'body-visibility-{f}.png').convert('L');ma=np.array(mask)
 overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(ba[:,:,3].astype(float)*ma/255))));overlay.save(HERE/f'body-overlay-{f}.png')
 effective=Image.fromarray(np.uint8(ma*(ba[:,:,3]>0)));off=Image.alpha_composite(body,cloth);assembly=Image.composite(body,off,effective);assembly.save(HERE/f'assembled-{f}.png');off.save(HERE/f'mask-off-{f}.png')
 body_col=tint(body,colors['w']);equipment_col=Image.alpha_composite(tint(cloth,colors['y']),tint(detail,colors['Y']));colored=Image.composite(body_col,Image.alpha_composite(body_col,equipment_col),effective);colored.save(HERE/f'qud-palette-{f}.png')
 for k,im in [('assembly',assembly),('cloth',cloth),('overlay',overlay),('mask',mask.convert('RGBA')),('detail',detail),('continued',Image.fromarray(np.uint8(unknown)*255).convert('RGBA')),('off',off),('palette',colored)]:groups[k][f]=im
 rows=[]
 for component,name,role,layer in [('item','intact-mail','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125),('body-overlay','body-overlay','foreground',.0013)]:
  row=dict(bm['views'][f][0]);row.update(component=component,file=f'yrame-chain-mail-v1-{component}-{f}.png',public_file=ref(HERE/f'{name}-{f}.png')['path'],sha256=ref(HERE/f'{name}-{f}.png')['sha256'],equipment_key='chain-mail@Body@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(body=ref(BODY/f'selected-{f}.png'),full_mail=ref(HERE/f'intact-mail-{f}.png'),visibility=ref(HERE/f'body-visibility-{f}.png'),overlay=ref(HERE/f'body-overlay-{f}.png'),detail=ref(HERE/f'item-detail-{f}.png'))
 record['views'][f]=dict(known_surface_pixels=int(known.sum()),authored_continuation_pixels=int(unknown.sum()),pattern=ref(HERE/f'pattern-{f}.svg'),fit='Identity on fixed unmutated base; no body rescale or new mesh',body_restore_changed_pixels=int(np.count_nonzero((ma==255)&(ba[:,:,3]>0)&np.any(ba!=np.array(assembly),axis=2))),**model['occlusion_sources'][f])
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
for k,name,title in [('assembly','assembly-comparison.png','YRAME / one Chain Mail shirt on fixed ordinary human base'),('cloth','intact-garment-comparison.png','FULL MAIL / continuous linked-loop source, no applied limb cutouts'),('overlay','body-overlay-comparison.png','ORIGINAL BODY / complete forearms and hands; independent tint'),('mask','body-mask-comparison.png','BODY OWNERSHIP / curved sleeves and semantic original forearms'),('detail','detail-comparison.png','DETAIL Y / linked-metal highlights at sleeve ends and hem'),('continued','continuation-comparison.png','AUTHORED CONTINUATION / concealed or excluded contextual surface'),('off','mask-off-comparison.png','MASK OFF / full mail before late original-body visibility'),('palette','independent-palette-comparison.png','SOURCE COLORS / Yrame foreground w; mail y and bright detail Y')]:plate(name,groups[k],title)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',record)
print('Registered linked steel, complete mail, bright cuff/hem regions and original-body visibility. Authoring review pending.')
