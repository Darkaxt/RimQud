"""Reuse the canonical optical item with constrained original male-head fitting."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-telescopic-monocle/v1';SB=ROOT/'art/conversion/body-human-female/v2';BODY=ROOT/'art/conversion/body-human-male/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def tint(im,c):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
def plate(n,rows,title,heads=True):
 out=Image.new('RGB',(1152,460 if heads else 660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  x=16+i*284;bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
  if heads:
   out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');label=360
  else:
   out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');label=584
  d.text((x,label),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,out.height-38),'Same full optical item; original male head/body and contact. Explicit west depth; native pending.',font=FONT,fill='#e5e8d8');out.save(HERE/n)
bm=json.loads((BODY/'model.json').read_text());model=json.loads((SOURCE/'model.json').read_text());model.update(family='human-male',views={},occlusion_sources={})
decisions=dict(source=ref(SOURCE/'model.json'),source_body=ref(SB/'model.json'),target_body=ref(BODY/'model.json'),context=ref(SOURCE/'refined-red-context.png'),new_imagegen_call=False,second_isolation_call=False,generated_body_used=False,method='Uniformly scale the full ocular/barrel/chain and its detail by the original head-width ratio, then translate original head center/top to the male head landmarks. One premultiplied bitmap sample per layer; no body transform. Re-establish rear/far-side visibility from actual target head, not the source mask.',views={})
groups={k:{} for k in ['assembly','item','detail','off','overlay','palette']}
for f in ['south','east','north','west']:
 side='east' if f=='west' else f;sh=read(SB/f'head-{side}.png');th=read(BODY/f'head-{side}.png');body=read(BODY/f'selected-{side}.png')
 if f=='west':sh=ImageOps.mirror(sh);th=ImageOps.mirror(th);body=ImageOps.mirror(body)
 s=sh.getbbox();t=th.getbbox();scale=(t[2]-t[0])/(s[2]-s[0]);tx=(t[0]+t[2])/2-scale*(s[0]+s[2])/2;ty=t[1]-scale*s[1]
 def fit(im):return im.convert('RGBa').transform((512,1024),Image.Transform.AFFINE,(1/scale,0,-tx/scale,0,1/scale,-ty/scale),Image.Resampling.BICUBIC).convert('RGBA')
 item=fit(read(SOURCE/f'intact-monocle-{f}.png'));detail=fit(read(SOURCE/f'item-detail-{f}.png'));item.save(HERE/f'intact-monocle-{f}.png');detail.save(HERE/f'item-detail-{f}.png')
 for prefix in ['pattern','detail-region','glass']:
  xml=ET.fromstring((SOURCE/f'{prefix}-{f}.svg').read_text());content=''.join(ET.tostring(n,encoding='unicode') for n in xml)
  (HERE/f'fitted-{prefix}-{f}.svg').write_bytes(('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g transform="translate('+str(tx)+' '+str(ty)+') scale('+str(scale)+')">'+content+'</g></svg>').encode())
 overlay=th if f in ['north','west'] else Image.new('RGBA',(512,1024));overlay.save(HERE/f'body-overlay-{f}.png');overlay.getchannel('A').save(HERE/f'body-visibility-{f}.png')
 off=Image.alpha_composite(body,item);assembly=Image.alpha_composite(off,overlay);off.save(HERE/f'mask-off-{f}.png');assembly.save(HERE/f'assembled-{f}.png')
 palette=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(152,135,95)),tint(item,(119,191,207))),tint(detail,(255,255,255))),tint(overlay,(152,135,95)));palette.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('item',item),('detail',detail),('off',off),('overlay',overlay),('palette',palette)]:groups[k][f]=im
 rows=[]
 for component,filename,role,layer in [('item','intact-monocle','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125),('body-overlay','body-overlay','foreground',.0013)]:
  row=dict(bm['views'][side][0]);row.update(component=component,file=f'human-male-telescopic-monocle-v1-{component}-{f}.png',public_file=ref(HERE/f'{filename}-{f}.png')['path'],sha256=ref(HERE/f'{filename}-{f}.png')['sha256'],equipment_key='telescopic-monocle@Face@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_item=ref(HERE/f'intact-monocle-{f}.png'),body_visibility=ref(HERE/f'body-visibility-{f}.png'),original_head_overlay=ref(HERE/f'body-overlay-{f}.png'),detail=ref(HERE/f'fitted-detail-region-{f}.svg'))
 decisions['views'][f]=dict(source_head_bounds=s,target_head_bounds=t,uniform_scale=scale,translation_x=tx,translation_y=ty,body_transformed=False,contact=[256,950],**model['occlusion_sources'][f])
for k,n,title,heads in [('assembly','assembly-comparison.png','MALE / canonical single optical item on original male body',False),('assembly','headwear-comparison.png','FACINGS / head-relative fit with explicit rear/far-side depth',True),('item','intact-garment-comparison.png','FULL ITEM / complete ocular, barrel and hanging chain',True),('off','mask-off-comparison.png','MASK OFF / full source before original male-head visibility',True),('overlay','body-overlay-comparison.png','BODY OWNERSHIP / target original head, not the source mask',True),('palette','independent-palette-comparison.png','NATIVE COLORS / C optical frame, Y chain/glint; illustrative body w',True)]:plate(n,groups[k],title,heads)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
packet=json.loads((SOURCE/'source-packet.json').read_text());packet.update(entry='FIT-HUMAN-MALE-TELESCOPIC-MONOCLE-FACE-0',body=ref(BODY/'model.json'),canonical_registration=ref(SOURCE/'model.json'),context=ref(SOURCE/'refined-red-context.png'),new_imagegen_call=False,identity_boundary='Captured male Argyve ordinary Face part 317 / item 587 supports this shared male fitting. It is not completion of NPC-ARGYVE outfit assembly.',fit_controls=decisions['views'],runtime_limitation='Explicit west artwork/masks require final direction binding; no current native acceptance claimed.')
write('source-packet.json',packet);write('registration-decisions.json',decisions);write('model.json',model);print('Male full-item optical fitting prepared; authoring review pending.')
