"""Register the fixed full optical item with same-output metal and late head visibility."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def tint(im,c):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
def plate(n,rows,title,head=True):
 out=Image.new('RGB',(1152,460 if head else 660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  x=16+i*284;bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
  if head:
   out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');label=360
  else:
   out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');label=584
  d.text((x,label),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,out.height-38),'Fixed full item/body/contact. Rear and far-side head visibility applied last. Native binding pending.',font=FONT,fill='#e5e8d8');out.save(HERE/n)
raw=np.array(read(HERE/'refined-red-context.png'));assert raw.shape==(1024,1536,4)
yy,xx=np.mgrid[0:1024,0:512].astype(float)
groups={k:{} for k in ['assembly','item','detail','off','overlay','palette','used','completion']}
bm=json.loads((BODY/'model.json').read_text());model=dict(item='Telescopic Monocle',blueprint='Telescopic Monocle',family='human-female',slot='Face',laterality=0,workflow='regional-curved-v1',views={},occlusion_sources={},west_policy='Explicit far-side west artwork and original-head depth; never mirror the completed east assembly',native_acceptance='Pending full-set gate, including explicit-west direction binding currently absent from probe/VillageArt.cs')
decisions=dict(context=ref(HERE/'refined-red-context.png'),body=ref(BODY/'model.json'),new_imagegen_call=True,second_isolation_call=False,generated_body_used=False,method='Use actual contextual metal shading only within the full editable ocular/barrel geometry. Redrawn body, shifted placement, halo and invented top knob are excluded. Keep authored transparent glass, original chain links/ink and complete behind-head item. No further generative isolation or body reshape.',views={})
for f in ['south','east','north','west']:
 original=read(HERE/f'constructed-pattern-{f}.png');a=np.array(original);pg=a[:,:,:3].mean(2);v=pg.copy();used=np.zeros((1024,512),bool)
 if f in ['south','east']:
  if f=='south':
   # Refined circle bounds [144,310,247,414] map to the fixed original ocular.
   mx=(xx-222)*(103/64)+195.5;my=(yy-98)*(104/64)+362;region=((xx-222)**2+(yy-98)**2<34**2)&(a[:,:,3]>245);control=dict(source_bounds=[144,310,247,414],target_center=[222,98],target_diameter=64)
  else:
   # Avoid the extra generated top knob; only the compact side barrel is sampled.
   mx=(xx-320)*(111/69)+865;my=(yy-74)*(73/51)+330;region=(xx>=318)&(xx<=391)&(yy>=73)&(yy<=126)&(a[:,:,3]>245);control=dict(source_bounds=[865,330,976,403],target_bounds=[320,74,389,125])
  rgb=np.stack([ndimage.map_coordinates(raw[:,:,c].astype(float),[my,mx],order=1,mode='constant') for c in range(3)],-1)
  valid=(rgb.max(2)-rgb.min(2)<22)&(rgb.mean(2)>45)&(pg>75)&region
  v[valid]=rgb.mean(2)[valid];used=valid
 elif f=='north':
  # The full rear ocular is retained behind the head; canonical same-item rim material.
  south=groups['item']['south'];sa=np.array(south);mx=xx-64;my=yy
  transfer=np.stack([ndimage.map_coordinates(sa[:,:,c].astype(float),[my,mx],order=1,mode='constant') for c in range(4)],-1)
  region=((xx-286)**2+(yy-98)**2<34**2)&(a[:,:,3]>245)&(transfer[:,:,3]>245)&(pg>75)
  v[region]=transfer[:,:,:3].mean(2)[region];used=region;control=dict(source='completed south ocular',translation_x=64,translation_y=0,behind_original_head=True)
 else:
  item=ImageOps.mirror(groups['item']['east']);used=np.fliplr(np.array(groups['used']['east'])[:,:,0]>0);control=dict(source='completed east full item',mirror_geometry=True,completed_assembly_mirrored=False,original_near_head_overlaid_last=True)
 if f!='west':
  values=np.uint8(np.clip(np.round(v),0,255));item=Image.fromarray(np.dstack([values,values,values,a[:,:,3]]))
 item.save(HERE/f'intact-monocle-{f}.png')
 # Detail is the authored chain/glass coverage, never a red/skin-colored patch.
 detail=read(HERE/f'constructed-detail-region-{f}.png');detail.save(HERE/f'item-detail-{f}.png')
 body=read(BODY/f'selected-{"east" if f=="west" else f}.png')
 if f=='west':body=ImageOps.mirror(body)
 overlay=read(HERE/f'body-overlay-{f}.png');mask=Image.open(HERE/f'body-visibility-{f}.png').convert('L')
 off=Image.alpha_composite(body,item);assembly=Image.alpha_composite(off,overlay);off.save(HERE/f'mask-off-{f}.png');assembly.save(HERE/f'assembled-{f}.png')
 palette=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(152,135,95)),tint(item,(119,191,207))),tint(detail,(255,255,255))),tint(overlay,(152,135,95)));palette.save(HERE/f'palette-{f}.png')
 used_image=Image.fromarray(np.uint8(used)*255).convert('RGBA');used_image.save(HERE/f'context-surface-used-{f}.png');completion=Image.fromarray(np.uint8((a[:,:,3]>0)&~used)*255).convert('RGBA');completion.save(HERE/f'authored-continuation-{f}.png')
 for k,im in [('assembly',assembly),('item',item),('detail',detail),('off',off),('overlay',overlay),('palette',palette),('used',used_image),('completion',completion)]:groups[k][f]=im
 rows=[]
 for component,filename,role,layer in [('item','intact-monocle','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125),('body-overlay','body-overlay','foreground',.0013)]:
  row=dict(bm['views']['east' if f=='west' else f][0]);row.update(component=component,file=f'human-female-telescopic-monocle-v1-{component}-{f}.png',public_file=ref(HERE/f'{filename}-{f}.png')['path'],sha256=ref(HERE/f'{filename}-{f}.png')['sha256'],equipment_key='telescopic-monocle@Face@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_item=ref(HERE/f'intact-monocle-{f}.png'),body_visibility=ref(HERE/f'body-visibility-{f}.png'),original_head_overlay=ref(HERE/f'body-overlay-{f}.png'),detail=ref(HERE/f'detail-region-{f}.svg'))
 decisions['views'][f]=dict(material_map=control,actual_context_surface_pixels=int(used.sum()),body_transformed=False,item_geometry='Full original construction retained; transparent optical glass and chain are authored completion',**model['occlusion_sources'][f])
for k,n,title,head in [('assembly','assembly-comparison.png','MONOCLE / one source-bound optical item on the unchanged body',False),('assembly','headwear-comparison.png','FACINGS / single ocular, explicit rear/far-side visibility',True),('item','intact-garment-comparison.png','FULL ITEM / no head-shaped permanent cutouts',True),('detail','detail-comparison.png','DETAIL / neutral chain and glass; native white tint',True),('off','mask-off-comparison.png','MASK OFF / complete item before original-head depth',True),('overlay','body-overlay-comparison.png','BODY OWNERSHIP / original head only in rear/far-side views',True),('palette','independent-palette-comparison.png','NATIVE COLORS / cyan C optical frame, white Y chain/glint; body w',True),('used','context-surface-comparison.png','SOURCE / exact same-output metal material coverage',True),('completion','authored-continuation-comparison.png','CONTINUATION / full source geometry, glass, chain and ink retained',True)]:plate(n,groups[k],title,head)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('registration-decisions.json',decisions);write('model.json',model)
print('Registered complete optical item, original-head masks and explicit west art; review pending.')
