"""Contextual material samples on registered soles/straps; original feet stay fixed."""
from pathlib import Path
import json, hashlib
import numpy as np
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
def texture(sample):
 # At 1.6x refinement zoom, return material to the original authoring scale.
 patch=ImageOps.grayscale(sample).resize((max(1,round(sample.width/1.6)),max(1,round(sample.height/1.6))),Image.Resampling.LANCZOS)
 a=np.array(patch);return np.tile(a,(1024//a.shape[0]+1,512//a.shape[1]+1))[:1024,:512]
def plate(name,rows,title,feet=False):
 out=Image.new('RGB',(1152,460 if feet else 660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  x=16+i*284;bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
  if feet:
   crop=bg.crop((96,640,416,960)).resize((256,256));out.paste(crop.convert('RGB'),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');d.line((x,328,x+255,328),fill='#70b8b0');label_y=360
  else:
   out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');label_y=584
  d.text((x,label_y),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,out.height-38),'Original body/contact fixed. Full soles, separate straps and foot ownership; native acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)

raw=read(HERE/'refined-red-context.png');boxes=dict(strap=[100,650,125,660],sole=[100,751,125,754]);samples={}
for key,box in boxes.items():
 im=raw.crop(tuple(box));rgb=np.array(im)[:,:,:3].astype(int);assert (rgb.max(2)-rgb.min(2)<35).all(),key
 im.save(HERE/f'contextual-{key}-swatch.png');samples[key]=texture(im)
body_model=json.loads((BODY/'model.json').read_text());model=dict(item='Sandals',blueprint='Sandals',family='human-female',slot='Feet',laterality=0,workflow='regional-curved-v1',views={},occlusion_sources={},structural_review=ref(HERE/'first-refinement-structural-review.json'),layer_order='body -> whole sandal .0012 -> strap detail .00125 -> exposed original foot .0013',west_policy='Mirror east; paired symmetrical sandals',native_acceptance='Pending final all-conversions gate')
record=dict(body=ref(BODY/'model.json'),context=ref(HERE/'refined-red-context.png'),sample_boxes=boxes,method='Generated contextual material only. Retain body-matched sole/strap geometry and original foot. Identity geometry fit, no body/foot resampling or generated body reused. Full sole material continues beneath foot; real straps cover skin and have independent native detail tint.',generated_body_used=False,second_isolation_call=False,views={})
groups={k:{} for k in ['assembly','cloth','detail','mask','overlay','off','palette']}
for f in ['south','east','north']:
 pattern=read(HERE/f'constructed-cloth-{f}.png');pa=np.array(pattern);strap=np.array(Image.open(HERE/f'detail-region-{f}.png').convert('L'))/255
 gray=samples['sole']*(1-strap)+samples['strap']*strap;ink=(pa[:,:,:3].mean(2)<85)&(pa[:,:,3]>0);gray[ink]=pa[:,:,:3].mean(2)[ink]
 v=np.uint8(np.round(gray));cloth=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));cloth.save(HERE/f'intact-sandals-{f}.png')
 detail=cloth.copy();detail.putalpha(Image.fromarray(np.uint8(np.round(pa[:,:,3].astype(float)*strap))));detail.save(HERE/f'item-detail-{f}.png')
 body=read(BODY/f'selected-{f}.png');mask=Image.open(HERE/f'body-visibility-{f}.png').convert('L');overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(mask)/255))));overlay.save(HERE/f'body-overlay-{f}.png')
 off=Image.alpha_composite(body,cloth);assembly=Image.alpha_composite(off,overlay);assembly.save(HERE/f'assembled-{f}.png');off.save(HERE/f'mask-off-{f}.png')
 color=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(cloth,(177,201,195))),tint(detail,(152,135,95))),tint(overlay,(119,191,207)));color.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('cloth',cloth),('detail',detail),('mask',mask.convert('RGBA')),('overlay',overlay),('off',off),('palette',color)]:groups[k][f]=im
 rows=[]
 for component,image,role,layer in [('item',HERE/f'intact-sandals-{f}.png','equipment',.0012),('item-detail',HERE/f'item-detail-{f}.png','equipment-detail',.00125),('body-overlay',HERE/f'body-overlay-{f}.png','foreground',.0013)]:
  row=dict(body_model['views'][f][0]);row.update(component=component,file=f'human-female-sandals-v2-{component}-{f}.png',public_file=ref(image)['path'],sha256=ref(image)['sha256'],equipment_key='sandals@Feet@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_sandal=ref(HERE/f'intact-sandals-{f}.png'),mask=ref(HERE/f'body-visibility-{f}.png'),foot_region=ref(HERE/f'foot-body-region-{f}.svg'),strap_region=ref(HERE/f'strap-coverage-{f}.svg'))
 record['views'][f]=dict(pattern=ref(HERE/f'pattern-{f}.svg'),body=ref(BODY/f'selected-{f}.png'),fit='Original body-matched soles/straps unchanged. Sole bottom/contact y950.',**model['occlusion_sources'][f])
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
for k,name,title,feet in [('assembly','assembly-comparison.png','ADULT FEMALE / actual separate Sandals on the fixed human body',False),('assembly','footwear-comparison.png','FOOTWEAR / complete soles and straps around original feet',True),('cloth','intact-garment-comparison.png','FULL SANDALS / soles remain intact underneath the original foot',True),('detail','strap-detail-comparison.png','DETAIL OWNERSHIP / actual strap tint w, independent of primary sole',True),('overlay','body-overlay-comparison.png','ORIGINAL FOOT / body above sole, except where straps cover skin',True),('off','mask-off-comparison.png','MASK OFF / complete sandal before exposed body restoration',True),('palette','independent-palette-comparison.png','NATIVE COLORS / sole y, straps w; illustrative body C',True)]:plate(name,groups[k],title,feet)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',record)
print('Registered contextual sole/strap material on unchanged sandal geometry and original feet; authoring review pending.')
