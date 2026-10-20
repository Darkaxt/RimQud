"""Fit the canonical whole hat to the male head; never transform body pixels."""
from pathlib import Path
import json, hashlib, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-wide-brimmed-hat/v1'
SB=ROOT/'art/conversion/body-human-female/v2'; BODY=ROOT/'art/conversion/body-human-male/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
def plate(name,rows,title,head=True):
 out=Image.new('RGB',(1152,460 if head else 660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  x=16+i*284;bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
  if head:
   out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');label=360
  else:
   out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');label=584
  d.text((x,label),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,out.height-38),'Canonical hat material; head-based scale/translation only. Original body/contact unchanged. Native pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
bm=json.loads((BODY/'model.json').read_text());model=json.loads((SOURCE/'model.json').read_text());model.update(family='human-male',views={},occlusion_sources={})
decisions=dict(source=ref(SOURCE/'model.json'),source_body=ref(SB/'model.json'),target_body=ref(BODY/'model.json'),new_imagegen_call=False,generated_body_used=False,second_isolation_call=False,method='Scale complete crown/brim and band together horizontally by the original head width ratio; translate by head-center and top differences. Keep vertical hat scale and full-body pivot/contact fixed. One premultiplied sample per item layer. No local warp, material change, sleeve mask or body transform.',views={})
groups={k:{} for k in ['assembly','hat','detail','palette','overlay']}
for f in ['south','east','north']:
 sh=read(SB/f'head-{f}.png');th=read(BODY/f'head-{f}.png');s=sh.getbbox();t=th.getbbox();sx=(t[2]-t[0])/(s[2]-s[0]);tx=(t[0]+t[2])/2-sx*(s[0]+s[2])/2;ty=t[1]-s[1]
 def fitted(im):return im.convert('RGBa').transform((512,1024),Image.Transform.AFFINE,(1/sx,0,-tx/sx,0,1,-ty),Image.Resampling.BICUBIC).convert('RGBA')
 whole=fitted(read(SOURCE/f'intact-hat-{f}.png'));detail=fitted(read(SOURCE/f'item-detail-{f}.png'));whole.save(HERE/f'intact-hat-{f}.png');detail.save(HERE/f'item-detail-{f}.png')
 for prefix,outname in [('pattern','fitted-pattern'),('band-region','fitted-band-region')]:
  svg=ET.fromstring((SOURCE/f'{prefix}-{f}.svg').read_text());children=''.join(ET.tostring(n,encoding='unicode') for n in svg)
  (HERE/f'{outname}-{f}.svg').write_bytes(('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g transform="translate('+str(tx)+' '+str(ty)+') scale('+str(sx)+' 1)">'+children+'</g></svg>').encode())
 body=read(BODY/f'selected-{f}.png');mask=Image.new('L',(512,1024));mask.save(HERE/f'body-visibility-{f}.png');empty=Image.new('RGBA',(512,1024));empty.save(HERE/f'body-overlay-{f}.png')
 assembly=Image.alpha_composite(body,whole);assembly.save(HERE/f'assembled-{f}.png');palette=Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(whole,(177,201,195))),tint(detail,(0,72,189)));palette.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('hat',whole),('detail',detail),('palette',palette),('overlay',empty)]:groups[k][f]=im
 rows=[]
 for component,filename,role,layer in [('item','intact-hat','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125)]:
  row=dict(bm['views'][f][0]);row.update(component=component,file=f'human-male-wide-brimmed-hat-v1-{component}-{f}.png',public_file=ref(HERE/f'{filename}-{f}.png')['path'],sha256=ref(HERE/f'{filename}-{f}.png')['sha256'],equipment_key='wide-brimmed-hat@Head@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_hat=ref(HERE/f'intact-hat-{f}.png'),body_visibility=ref(HERE/f'body-visibility-{f}.png'),empty_overlay=ref(HERE/f'body-overlay-{f}.png'),band=ref(HERE/f'fitted-band-region-{f}.svg'))
 decisions['views'][f]=dict(source_head=ref(SB/f'head-{f}.png'),target_head=ref(BODY/f'head-{f}.png'),source_head_bounds=s,target_head_bounds=t,scale_x=sx,scale_y=1,translation_x=tx,translation_y=ty,body_transformed=False,contact=[256,950],**model['occlusion_sources'][f])
for rows in groups.values():rows['west (mirror)']=ImageOps.mirror(rows['east'])
for k,name,title,head in [('assembly','assembly-comparison.png','MALE / same whole hat fitted to original male head',False),('assembly','headwear-comparison.png','HEADWEAR / source-bound crown, brim and separate band',True),('hat','intact-garment-comparison.png','FULL HAT / one head-relative scale and translation',True),('detail','band-detail-comparison.png','DETAIL / original band follows the same complete-hat transform',True),('palette','independent-palette-comparison.png','NATIVE COLORS / hat y, band b; illustrative body C',True),('overlay','body-overlay-comparison.png','BODY OWNERSHIP / empty overlay; skin stays behind this hat',True)]:plate(name,groups[k],title,head)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*140+20,138),thumb);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
packet=json.loads((SOURCE/'source-packet.json').read_text());packet.update(entry='FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0',body=ref(BODY/'model.json'),canonical_registration=ref(SOURCE/'model.json'),context=ref(SOURCE/'refined-red-context.png'),context_reuse='Same actual source-bound hat refinement, fitted to male head geometry. No new ImageGen call or generated body.',new_imagegen_call=False,fit_controls=decisions['views'],modifier_boundary='Captured painted/feathered item descriptions are retained above. All captured items use the same native sw_hat sprite/y-b colors. This shared base does not invent unobserved painting or feather placement, nor claim optional modifier art.')
write('source-packet.json',packet);write('model.json',model);write('registration-decisions.json',decisions)
print('Male head-relative hat fit prepared; authoring review pending.')
