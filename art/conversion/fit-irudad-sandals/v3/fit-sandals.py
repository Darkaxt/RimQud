"""Contextual material samples on registered soles/straps; original feet stay fixed."""
from pathlib import Path
import json, hashlib, io, sys, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0,"E:/Temp/rimqud-conversion-runtime/python-libs")
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-male-older/v2'
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

SOURCE=ROOT/'art/conversion/fit-human-female-sandals/v3'
source_body=ROOT/'art/conversion/body-human-female/v2'
body_model=json.loads((BODY/'model.json').read_text());base_model=json.loads((SOURCE/'model.json').read_text())
model=dict(base_model);model.update(family='irudad',views={},occlusion_sources={})
record=dict(workflow='regional-curved-v1',canonical_source=ref(SOURCE/'model.json'),context=ref(SOURCE/'refined-red-context.png'),source_body=ref(source_body/'model.json'),target_body=ref(BODY/'model.json'),new_imagegen_call=False,method='Reuse the structurally corrected source-bound Sandals refinement and continuous canonical soles/straps. Fit each complete foot horizontally to the target original foot footprint; vertical frame/contact stay fixed. One premultiplied bitmap sampling pass per foot, same map for detail and visibility. No body deformation or new garment drawing.',views={})
groups={k:{} for k in ['assembly','cloth','detail','mask','overlay','off','palette']}
for f in ['south','east','north']:
 body=read(BODY/f'selected-{f}.png');src_body=read(source_body/f'selected-{f}.png');canonical=read(SOURCE/f'intact-sandals-{f}.png');canonical_detail=read(SOURCE/f'item-detail-{f}.png')
 whole=Image.new('RGBA',(512,1024));detail=whole.copy();strapmask=Image.new('L',(512,1024));controls=[]
 parts=[(0,512)] if f=='east' else [(0,256),(256,512)]
 pattern=ET.fromstring((SOURCE/f'pattern-{f}.svg').read_text());strap_svg=ET.fromstring((SOURCE/f'strap-coverage-{f}.svg').read_text())
 svg_start='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'
 sketches=[];straps=[]
 for i,(left,right) in enumerate(parts):
  def footprint(im):
   a=np.array(im)[:,:,3]>128;yy,xx=np.where(a[885:950,left:right]);return [int(xx.min()+left),int(xx.max()+left+1)]
  sb,tb=footprint(src_body),footprint(body);sx=(tb[1]-tb[0])/(sb[1]-sb[0]);tx=tb[0]-sx*sb[0]
  controls.append(dict(source_x=sb,target_x=tb,scale_x=sx,translation_x=tx,scale_y=1,translation_y=0,source_region=[left,0,right,1024],contact_y=950))
  def fitted(im):
   cut=Image.new('RGBA',im.size);cut.paste(im.crop((left,0,right,1024)),(left,0));return cut.convert('RGBa').transform((512,1024),Image.Transform.AFFINE,(1/sx,0,-tx/sx,0,1,0),Image.Resampling.BICUBIC).convert('RGBA')
  whole=Image.alpha_composite(whole,fitted(canonical));detail=Image.alpha_composite(detail,fitted(canonical_detail))
  mask_rgba=Image.new('RGBA',(512,1024),'white');mask_rgba.putalpha(Image.open(SOURCE/f'detail-region-{f}.png').convert('L'));sm=fitted(mask_rgba).getchannel('A');strapmask=Image.fromarray(np.maximum(np.array(strapmask),np.array(sm)))
  clip='<defs><clipPath id="part'+str(i)+'" clipPathUnits="userSpaceOnUse"><rect x="'+str(left)+'" y="0" width="'+str(right-left)+'" height="1024"/></clipPath></defs>'
  def construct(root):return clip+'<g transform="translate('+str(tx)+' 0) scale('+str(sx)+' 1)"><g clip-path="url(#part'+str(i)+')">'+''.join(ET.tostring(child,encoding='unicode') for child in root)+'</g></g>'
  sketches.append(construct(pattern));straps.append(construct(strap_svg))
 (HERE/f'fitted-pattern-{f}.svg').write_bytes((svg_start+''.join(sketches)+'</svg>').encode());(HERE/f'fitted-strap-region-{f}.svg').write_bytes((svg_start+''.join(straps)+'</svg>').encode())
 whole.save(HERE/f'intact-sandals-{f}.png');detail.save(HERE/f'item-detail-{f}.png');strapmask.save(HERE/f'detail-region-{f}.png')
 foot=Image.new('L',(512,1024));ImageDraw.Draw(foot).rectangle((96,800,415,952),fill=255);mask=Image.fromarray(np.uint8(np.round(np.array(foot).astype(float)*(1-np.array(strapmask)/255))));mask.save(HERE/f'body-visibility-{f}.png')
 overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(mask)/255))));overlay.save(HERE/f'body-overlay-{f}.png')
 off=Image.alpha_composite(body,whole);assembly=Image.alpha_composite(off,overlay);assembly.save(HERE/f'assembled-{f}.png');off.save(HERE/f'mask-off-{f}.png')
 color=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(whole,(177,201,195))),tint(detail,(152,135,95))),tint(overlay,(119,191,207)));color.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('cloth',whole),('detail',detail),('mask',mask.convert('RGBA')),('overlay',overlay),('off',off),('palette',color)]:groups[k][f]=im
 rows=[]
 for component,name,role,layer in [('item','intact-sandals','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125),('body-overlay','body-overlay','foreground',.0013)]:
  row=dict(body_model['views'][f][0]);row.update(component=component,file=f'irudad-sandals-v3-{component}-{f}.png',public_file=ref(HERE/f'{name}-{f}.png')['path'],sha256=ref(HERE/f'{name}-{f}.png')['sha256'],equipment_key='sandals@Feet@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_sandal=ref(HERE/f'intact-sandals-{f}.png'),mask=ref(HERE/f'body-visibility-{f}.png'),strap_region=ref(HERE/f'fitted-strap-region-{f}.svg'))
 record['views'][f]=dict(controls=controls,pattern=ref(HERE/f'fitted-pattern-{f}.svg'),**model['occlusion_sources'][f])
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
for k,name,title,feet in [('assembly','assembly-comparison.png','IRUDAD / Sandals on the unmutated older-human base',False),('assembly','footwear-comparison.png','FOOTWEAR / same Sandals source fitted as whole soles and straps',True),('cloth','intact-garment-comparison.png','INTACT SOURCE / complete sandals fitted without limb cutouts',True),('overlay','body-overlay-comparison.png','BODY OWNERSHIP / original older-human feet, skin outside straps',True),('off','mask-off-comparison.png','MASK OFF / complete sandals before original foot restoration',True),('palette','independent-palette-comparison.png','NATIVE COLORS / sole y, strap detail w; body C illustrative',True)]:plate(name,groups[k],title,feet)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
packet=json.loads((SOURCE/'source-packet.json').read_text());packet.update(entry='FIT-IRUDAD-SANDALS-FEET-0',body=ref(BODY/'model.json'),canonical_registration=ref(SOURCE/'model.json'),context_reuse='Actual Sandals contextual refinement/material source reused, then whole-item fitting to unchanged older-human feet. No new ImageGen call claimed.',fit_controls=record['views'])
packet.update(creature='ElderBob (Irudad)',baseline_body_entry='BODY-HUMAN-MALE-OLDER',observed_binding=next(x for x in packet['observed_bindings'] if x['actor']=='ElderBob'),authoring_limits='Fitting on the selected unmutated older-human body only. Native ordinary Feet group is not mutation-managed. Extra arms, hands-face, tail and full BODY-IRUDAD assembly remain separate pending work; no individual mutation anatomy is baked into this shoe fit.')
write('source-packet.json',packet);write('model.json',model);write('registration-decisions.json',record)
print('Fitted canonical Sandals to older-human feet; original body/contact and garment source retained. Authoring review pending.')
