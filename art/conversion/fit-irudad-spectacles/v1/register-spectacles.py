"""Register original almond-wire geometry with actual contextual metal and late rear depth."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male-older/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
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
 d.text((18,out.height-38),'Complete wire/glass retained; original head/body and contact. Rear depth separate; native pending.',font=FONT,fill='#e5e8d8');out.save(HERE/n)
raw=np.array(read(HERE/'refined-red-context.png'));assert raw.shape==(1024,1536,4);yy,xx=np.mgrid[0:1024,0:512].astype(float)
bm=json.loads((BODY/'model.json').read_text());packet=json.loads((HERE/'source-packet.json').read_text());model=dict(item='Spectacles',blueprint='Spectacles',family='irudad',unmutated_body_family='human-male-older',slot='Face',laterality=0,workflow='regional-curved-v1',body_source=ref(BODY/'model.json'),actual_equipped_binding=packet['actual_face_binding'],views={},occlusion_sources={},west_policy='Mirror east; symmetric pair, no handed ornament',native_acceptance='Pending full-set gate; Irudad mutation/body/outfit acceptance unfinished')
decisions=dict(context=ref(HERE/'refined-red-context.png'),body=ref(BODY/'model.json'),new_imagegen_call=True,second_isolation_call=False,generated_body_used=False,method='Keep full original almond-wire geometry, translucent glass and authored glints. Transfer neutral contextual metal through recorded per-view material registration only; reject red/backdrop and body placement drift. Missing/hidden wire continues the authored neutral source, never a body-colored or alpha cut. Rear original-head visibility is applied last.',fit='Original construction already matches the fixed head; freeze garment geometry/frame/contact. Material sampling is not body or garment deformation.',views={})
groups={k:{} for k in ['assembly','item','detail','off','overlay','palette','used']}
for i,f in enumerate(['south','east','north']):
 source=read(HERE/f'constructed-pattern-{f}.png');a=np.array(source);pg=a[:,:,:3].mean(2)
 if f=='south':mx=(xx-64)*4/3-6;my=yy*4/3+234;control=dict(map_x='(x-64)*4/3-6',map_y='y*4/3+234',role='Front wire material alignment; body/geometry fixed')
 elif f=='east':mx=(xx-64)*4/3+512-8+.17*(xx-220);my=yy*4/3+251-.15*(xx-220);control=dict(map_x='(x-64)*4/3+512-8+0.17*(x-220)',map_y='y*4/3+251-0.15*(x-220)',role='Temple endpoint material registration; no geometry deformation')
 else:mx=(xx-64)*4/3+1024+8;my=yy*4/3+233;control=dict(map_x='(x-64)*4/3+1024+8',map_y='y*4/3+233',role='Visible rear hook material only; concealed lenses retain full authored source')
 rgb=np.stack([ndimage.map_coordinates(raw[:,:,c].astype(float),[my,mx],order=1,mode='constant') for c in range(3)],-1);known=(a[:,:,3]>245)&(pg>75)&(rgb.max(2)-rgb.min(2)<18)&(rgb.mean(2)>75)
 if f in ['south','east']:assert known.sum()>30,(f,int(known.sum()))
 values=pg.copy();values[known]=rgb.mean(2)[known];v=np.uint8(np.round(np.clip(values,0,255)));item=Image.fromarray(np.dstack([v,v,v,a[:,:,3]]));item.save(HERE/f'intact-spectacles-{f}.png');detail=read(HERE/f'constructed-detail-region-{f}.png');assert np.ptp(np.array(detail)[:,:,:3].astype(int),axis=2).max()==0;detail.save(HERE/f'item-detail-{f}.png')
 body=read(BODY/f'selected-{f}.png');overlay=read(HERE/f'body-overlay-{f}.png');off=Image.alpha_composite(Image.alpha_composite(body,item),detail);assembly=Image.alpha_composite(off,overlay);off.save(HERE/f'mask-off-{f}.png');assembly.save(HERE/f'assembled-{f}.png');color=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(152,135,95)),tint(item,(177,201,195))),tint(detail,(255,255,255))),tint(overlay,(152,135,95)));color.save(HERE/f'palette-{f}.png');used=Image.fromarray(np.uint8(known)*255).convert('RGBA');used.save(HERE/f'context-surface-used-{f}.png')
 for k,im in [('assembly',assembly),('item',item),('detail',detail),('off',off),('overlay',overlay),('palette',color),('used',used)]:groups[k][f]=im
 rows=[]
 for component,filename,role,layer in [('item','intact-spectacles','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125),('body-overlay','body-overlay','foreground',.0013)]:
  row=dict(bm['views'][f][0]);row.update(component=component,file=f'irudad-spectacles-v1-{component}-{f}.png',public_file=ref(HERE/f'{filename}-{f}.png')['path'],sha256=ref(HERE/f'{filename}-{f}.png')['sha256'],equipment_key='spectacles@Face@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_item=ref(HERE/f'intact-spectacles-{f}.png'),body_visibility=ref(HERE/f'body-visibility-{f}.png'),original_head_overlay=ref(HERE/f'body-overlay-{f}.png'),glass_detail=ref(HERE/f'detail-region-{f}.svg'))
 decisions['views'][f]=dict(context_surface_pixels=int(known.sum()),material_map=control,complete_source_geometry=ref(HERE/f'pattern-{f}.svg'),original_body_unchanged=True,contact=[256,950],**model['occlusion_sources'][f])
for rows in groups.values():rows['west (mirror)']=ImageOps.mirror(rows['east'])
for k,n,title,heads in [('assembly','assembly-comparison.png','SPECTACLES / actual current item + detail + original-head depth',False),('assembly','headwear-comparison.png','SPECTACLES / paired almond glass, fine wire and correct rear visibility',True),('item','intact-garment-comparison.png','FULL ITEM / complete wire cups, bridge and transparent glass',True),('off','mask-off-comparison.png','MASK OFF / full source before original rear-head occlusion',True),('overlay','body-overlay-comparison.png','BODY OWNERSHIP / original rear head only; front/profile overlay empty',True),('detail','detail-comparison.png','DETAIL / neutral glass glints for independent native Y white',True),('palette','independent-palette-comparison.png','NATIVE COLORS / pale y wire/glass, Y glint; illustrative body w',True),('used','context-surface-comparison.png','MATERIAL / actual contextual wire highlights; other geometry authored',True)]:plate(n,groups[k],title,heads)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('registration-decisions.json',decisions);write('model.json',model);print('Registered source-bound Spectacles, transparent glass and original rear-head ownership; review pending.')
