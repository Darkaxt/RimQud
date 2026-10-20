"""Keep the editable whole robe; transfer contextual cloth and restore fixed arms."""
from pathlib import Path
import hashlib, json
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists(), 'Keep registered versions immutable'

def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,data): (HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
def read(p): return Image.open(p).convert('RGBA')
def tint(im,color):
 a=np.array(im).copy();v=a[:,:,:3].mean(axis=2)
 a[:,:,:3]=np.uint8(np.round(v[:,:,None]*np.array(color)/255));return Image.fromarray(a)

def complete(gray,known,envelope):
 """Same contextual fabric, harmonic continuation only where hidden/invalid."""
 unknown=envelope & ~known; yy,xx=np.where(unknown);n=len(yy)
 ids=np.full(gray.shape,-1,np.int32);ids[yy,xx]=np.arange(n)
 deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512))
  q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0
  rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
 if n:
  matrix=sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg)
  gray[yy,xx]=spsolve(matrix,rhs)
 return gray,unknown

def plate(name,rows,title):
 out=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(out)
 d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284
  out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0')
  d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,620),'Fixed original body; intact cloth and curved visibility separate. Native acceptance awaits the full set.',font=FONT,fill='#e5e8d8')
 out.save(HERE/name)

body_model=json.loads((BODY/'model.json').read_text())
raw=read(HERE/'refined-red-context.png')
model=dict(item='Woven Tunic',blueprint='Woven Tunic',family='human-female',slot='Body',laterality=0,
 workflow='regional-curved-v1',views={},occlusion_sources={},layer_order='body -> head -> cloth .0012 -> exposed arm .0013',
 representation='Editable continuous robe geometry with contextual ImageGen material and independent original-body visibility',
 west_policy='Mirror east; plain symmetric robe, no handed attachments',native_acceptance='Pending final all-conversions generation gate')
record=dict(body=ref(BODY/'model.json'),context=ref(HERE/'refined-red-context.png'),views={},
 method='Transfer neutral fabric from the actual contextual output into the fixed body-matched editable pattern. Hidden/red/backdrop pixels completed before fitting. Retain original authored contours/cuff seams. Identity fit: no stretch needed for this pre-registered construction.',
 generated_body_used=False,second_isolation_call=False,cutoff_cloth_alpha=False,
 reconstruction='Same-output harmonic continuation is authored unseen fabric, not recovered hidden detail. Generated backdrop glow and mannequin are excluded. No raw donor pixels in published plates.')
groups={k:{} for k in ['assembly','cloth','mask','overlay','off','palette','continued']}
for i,f in enumerate(['south','east','north']):
 pattern=read(HERE/f'constructed-cloth-{f}.png');pa=np.array(pattern);envelope=pa[:,:,3]>0
 cell=np.array(raw.crop((i*512,0,(i+1)*512,1024)));rgb=cell[:,:,:3].astype(float)
 red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3)
 # Interior-only sampling avoids the generated background/contours. Preserve
 # the editable pattern ink instead of carrying generated body outlines over.
 known=ndimage.binary_erosion(envelope,iterations=10)&(rgb.max(axis=2)-rgb.min(axis=2)<35)&(rgb.mean(axis=2)>110)&(cell[:,:,3]>100)&~ndimage.binary_dilation(red,iterations=9)
 gray,unknown=complete(rgb.mean(axis=2),known,envelope)
 pg=pa[:,:,:3].mean(axis=2);ink=(pg<90)&envelope
 gray[ink]=pg[ink];v=np.uint8(np.clip(np.round(gray),0,255))
 cloth=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));cloth.save(HERE/f'intact-tunic-{f}.png')
 Image.fromarray(np.uint8(unknown)*255).save(HERE/f'authored-continuation-{f}.png')
 mask=Image.open(HERE/f'body-visibility-{f}.png').convert('L');body=read(BODY/f'selected-{f}.png')
 overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(mask)/255))))
 overlay.save(HERE/f'body-overlay-{f}.png')
 off=Image.alpha_composite(body,cloth);assembly=Image.alpha_composite(off,overlay)
 assembly.save(HERE/f'assembled-{f}.png');off.save(HERE/f'mask-off-{f}.png')
 colored=Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(cloth,(177,201,195))),tint(overlay,(119,191,207)))
 colored.save(HERE/f'palette-{f}.png')
 for key,im in [('assembly',assembly),('cloth',cloth),('mask',mask.convert('RGBA')),('overlay',overlay),('off',off),('palette',colored),('continued',Image.fromarray(np.uint8(unknown)*255).convert('RGBA'))]:groups[key][f]=im
 row=dict(body_model['views'][f][0]);row.update(component='item',file=f'human-female-woven-tunic-v1-{f}.png',public_file=ref(HERE/f'intact-tunic-{f}.png')['path'],sha256=ref(HERE/f'intact-tunic-{f}.png')['sha256'],equipment_key='woven-tunic@Body@0',color_role='equipment',layer=.0012)
 over=dict(row);over.update(component='body-overlay',file=f'human-female-woven-tunic-overlay-v1-{f}.png',public_file=ref(HERE/f'body-overlay-{f}.png')['path'],sha256=ref(HERE/f'body-overlay-{f}.png')['sha256'],color_role='foreground',layer=.0013)
 model['views'][f]=[row,over]
 model['occlusion_sources'][f]=dict(cloth=ref(HERE/f'intact-tunic-{f}.png'),mask=ref(HERE/f'body-visibility-{f}.png'),editable_mask=ref(HERE/f'body-visibility-{f}.svg'))
 record['views'][f]=dict(pattern=ref(HERE/f'pattern-{f}.svg'),body=ref(BODY/f'selected-{f}.png'),known_context_pixels=int(known.sum()),authored_continuation_pixels=int(unknown.sum()),continuation=ref(HERE/f'authored-continuation-{f}.png'),fit='Identity on common frame; original body unchanged; no independent bounds centering',**model['occlusion_sources'][f])
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
for key,name,title in [('assembly','assembly-comparison.png','ADULT FEMALE / one coarse flax Qud Woven Tunic on the fixed human body'),('cloth','intact-garment-comparison.png','FULL CLOTH / contextual material, editable outline; no limb cutouts'),('mask','body-mask-comparison.png','CURVED VISIBILITY / natural cuff tops and original anatomical arm ownership'),('overlay','body-overlay-comparison.png','ORIGINAL ARMS / separate from garment material and equipment tint'),('off','mask-off-comparison.png','MASK OFF / continuous cloth stays underneath the near arm'),('palette','independent-palette-comparison.png','PALETTE OWNERSHIP / illustrative body C; actual Woven Tunic y/y'),('continued','continuation-comparison.png','AUTHORED CONTINUATION / white fabric filled from the same contextual output')]:plate(name,groups[key],title)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
write('model.json',model);write('registration-decisions.json',record)
print('Prepared contextual material, full cloth, continuation, fixed body overlays and directional plates; visual authoring review pending.')
