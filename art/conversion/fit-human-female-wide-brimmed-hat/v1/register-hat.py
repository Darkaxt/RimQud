"""Transfer the contextual hat surface into its fixed source-bound whole shape."""
from pathlib import Path
import json, hashlib
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve
from PIL import Image, ImageDraw, ImageFont, ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,color):
 a=np.array(im).copy();g=a[:,:,:3].mean(2);a[:,:,:3]=np.uint8(np.round(g[:,:,None]*np.array(color)/255));return Image.fromarray(a)
def complete(gray,known,envelope):
 unknown=envelope&~known;yy,xx=np.where(unknown);n=len(yy);ids=np.full(gray.shape,-1,np.int32);ids[yy,xx]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
 if n:
  matrix=sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg);gray[yy,xx]=spsolve(matrix,rhs)
 return gray,unknown
def plate(name,rows,title,heads=True):
 out=Image.new('RGB',(1152,460 if heads else 660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284
  if heads:
   out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');label=360
  else:
   out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');label=584
  d.text((x,label),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,out.height-38),'Full hat above unchanged head. Separate primary/band tint; no skin overlay. Native acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)

raw=read(HERE/'refined-red-context.png');assert raw.size==(1536,1024)
body_model=json.loads((BODY/'model.json').read_text());model=dict(item='Wide-brimmed Hat',blueprint='Wide-brimmed Hat',family='human-female',slot='Head',laterality=0,workflow='regional-curved-v1',views={},occlusion_sources={},layer_order='body -> head -> whole hat .0012 -> band detail .00125',body_overlay='Explicit zero: upper head stays behind this complete hat',west_policy='Mirror east; no handed ornament',native_acceptance='Pending final all-conversions gate')
record=dict(context=ref(HERE/'refined-red-context.png'),body=ref(BODY/'model.json'),new_imagegen_call=True,second_isolation_call=False,generated_body_used=False,method='Map actual enlarged-context surface back into the fixed editable whole hat; exclude red mannequin/background/ink and complete only missing surface before source contour restoration. Keep original head and full frame. No extra garment isolation.',zoom_mapping=dict(source_crop=[64,0,448,384],scale=4/3,origin_y=256),views={})
groups={k:{} for k in ['assembly','hat','detail','palette','continued','zero']}
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=(xx-64)*4/3;my=yy*4/3+256
for i,f in enumerate(['south','east','north']):
 pattern=read(HERE/f'constructed-cloth-{f}.png');pa=np.array(pattern);envelope=pa[:,:,3]>0;cell=np.array(raw.crop((i*512,0,(i+1)*512,1024))).astype(float)
 rgb=np.stack([ndimage.map_coordinates(cell[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
 red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3)
 known=ndimage.binary_erosion(envelope,iterations=2)&(rgb.max(2)-rgb.min(2)<35)&(rgb.mean(2)>75)&~ndimage.binary_dilation(red,iterations=1)
 assert known.sum()>1000,f
 gray,unknown=complete(rgb.mean(2),known,envelope);pg=pa[:,:,:3].mean(2);ink=(pg<85)&envelope;gray[ink]=pg[ink];v=np.uint8(np.clip(np.round(gray),0,255));hat=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));hat.save(HERE/f'intact-hat-{f}.png')
 Image.fromarray(np.uint8(unknown)*255).save(HERE/f'authored-continuation-{f}.png')
 detail=hat.copy();region=np.array(Image.open(HERE/f'detail-region-{f}.png').convert('L'));detail.putalpha(Image.fromarray(np.uint8(np.round(pa[:,:,3].astype(float)*region/255))));detail.save(HERE/f'item-detail-{f}.png')
 body=read(BODY/f'selected-{f}.png');mask=Image.open(HERE/f'body-visibility-{f}.png').convert('L');assert mask.getextrema()==(0,0);zero=Image.new('RGBA',(512,1024));zero.save(HERE/f'body-overlay-{f}.png')
 assembly=Image.alpha_composite(body,hat);assembly.save(HERE/f'assembled-{f}.png')
 color=Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(hat,(177,201,195))),tint(detail,(0,72,189)));color.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('hat',hat),('detail',detail),('palette',color),('continued',Image.fromarray(np.uint8(unknown)*255).convert('RGBA')),('zero',zero)]:groups[k][f]=im
 rows=[]
 for component,name,role,layer in [('item','intact-hat','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125)]:
  row=dict(body_model['views'][f][0]);row.update(component=component,file=f'human-female-wide-brimmed-hat-v1-{component}-{f}.png',public_file=ref(HERE/f'{name}-{f}.png')['path'],sha256=ref(HERE/f'{name}-{f}.png')['sha256'],equipment_key='wide-brimmed-hat@Head@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_hat=ref(HERE/f'intact-hat-{f}.png'),body_visibility=ref(HERE/f'body-visibility-{f}.png'),empty_overlay=ref(HERE/f'body-overlay-{f}.png'),band=ref(HERE/f'band-region-{f}.svg'))
 record['views'][f]=dict(source_surface_pixels=int(known.sum()),authored_continuation_pixels=int(unknown.sum()),pattern=ref(HERE/f'pattern-{f}.svg'),fit='Identity: keep body-matched full crown/brim placement and no head/body transform',**model['occlusion_sources'][f])
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
for k,name,title,heads in [('assembly','assembly-comparison.png','ADULT FEMALE / one Qud Wide-brimmed Hat on the fixed body',False),('assembly','headwear-comparison.png','HEADWEAR / crushed crown, stained wide brim and fixed head',True),('hat','intact-garment-comparison.png','FULL HAT / intact crown and brim; no generated body pixels',True),('detail','band-detail-comparison.png','DETAIL REGION / lower band, independent native blue b',True),('palette','independent-palette-comparison.png','NATIVE COLORS / hat y, band b; illustrative body C',True),('continued','continuation-comparison.png','CONTINUATION / excluded contour/mannequin/background pixels',True),('zero','body-overlay-comparison.png','BODY OVERLAY / intentionally empty, no bare head above hat',True)]:plate(name,groups[k],title,heads)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',record)
print('Registered full contextual hat surface, independent blue-band detail and unchanged body/head; authoring review pending.')
