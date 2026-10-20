"""Register contextual leather; retain precise wire and per-boot sources."""
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
def tint(im,col):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(col)/255));return Image.fromarray(a)
def complete(gray,known,envelope):
 unknown=envelope&~known;yy,xx=np.where(unknown);n=len(yy);ids=np.full(gray.shape,-1,np.int32);ids[yy,xx]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
 if n:
  labels,count=ndimage.label(envelope)
  for label in range(1,count+1):
   component=labels==label
   if not np.any(known&component):q=np.flatnonzero(component[yy,xx]);rhs[q]+=205;deg[q]+=1
  gray[yy,xx]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg),rhs)
 return gray,unknown
def plate(name,rows,title,feet=False):
 out=Image.new('RGB',(1152,470 if feet else 660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);x,y=16+i*284,75 if feet else 54
  if feet:out.paste(bg.crop((96,700,416,960)).convert('RGB').resize((256,208)),(x,y));label=310
  else:out.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(x,y));d.line((x+128,y,x+128,y+511),fill='#e3cf43');d.line((x,y+475,x+255,y+475),fill='#70b8b0');label=584
  d.text((x,label),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,out.height-38),'Closed boot covers original foot. Reusable art only; mutation placement/native acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
raw=read(HERE/'refined-red-context.png');assert raw.size==(1536,1024)
packet=json.loads((HERE/'source-packet.json').read_text());bm=json.loads((BODY/'model.json').read_text());colors={k:tuple(bytes.fromhex(v)) for k,v in json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'].items()}
model=dict(item='Leather Boots',blueprint='Leather Boots',family='yrame',slot='Feet',laterality=16,workflow='regional-curved-v1',canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],views={},individual_boots={},occlusion_sources={},actual_binding=packet['actual_binding'],
 policy='Reusable ordinary human footwear source for actual Yrame mutation-managed Feet297/16. No remap to Feet0 and no completed placement on extra legs.',layer_order='body -> full closed boot .0007 -> neutral wire detail .00075; no bare skin restored over boot',body_overlay='Zero: these closed boots cover the underlying foot.',west_policy='Mirror east; ordinary symmetric boot pair with reversible lace construction.',native_acceptance='Pending all-generation gate and actual mutation-specific foot placement')
record=dict(source=ref(HERE/'refined-red-context.png'),body=ref(BODY/'model.json'),new_imagegen_call=True,second_isolation_call=False,generated_anatomy_used=False,
 method='Map actual grayscale leather through fixed feet zoom, exclude glow/red/body outlines and a six-pixel wire neighborhood, then complete leather under the wire and excluded edges before source contour restoration. Wire retains deterministic constructed paths and a sampled contextual brightness. No shoe-shaped body cutouts, skin overlay, body transform or new isolation drawing.',
 zoom=dict(crop=[96,700,416,960],size=[512,416],origin=[0,304]),views={})
yy,xx=np.mgrid[0:1024,0:512].astype(float);mx=(xx-96)*1.6;my=(yy-700)*1.6+304
groups={k:{} for k in ['assembly','item','detail','zero','off','palette','continued']}
for i,f in enumerate(FACES):
 pattern=read(HERE/f'constructed-cloth-{f}.png');pa=np.array(pattern);envelope=pa[:,:,3]>0;wire_alpha=np.array(Image.open(HERE/f'detail-region-{f}.png').convert('L'))
 cell=np.array(raw.crop((i*512,0,(i+1)*512,1024))).astype(float);rgb=np.stack([ndimage.map_coordinates(cell[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
 red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3);wire_neighborhood=ndimage.binary_dilation(wire_alpha>0,iterations=6)
 known=ndimage.binary_erosion(envelope,iterations=3)&(rgb.max(2)-rgb.min(2)<25)&(rgb.mean(2)>70)&~ndimage.binary_dilation(red,iterations=2)&~wire_neighborhood;assert known.sum()>1000,f
 gray,unknown=complete(rgb.mean(2),known,envelope);pg=pa[:,:,:3].mean(2);gray[(pg<85)&envelope]=pg[(pg<85)&envelope];assert np.all(np.isfinite(gray[envelope]));v=np.uint8(np.clip(np.round(gray),0,255));item=Image.fromarray(np.dstack([v,v,v,pa[:,:,3]]));item.save(HERE/f'intact-boot-{f}.png')
 wire_samples=rgb.mean(2)[(wire_alpha>128)&~red];wire_value=int(np.clip(np.percentile(wire_samples,85),210,245)) if len(wire_samples) else None
 wire=Image.new('RGBA',SIZE,(wire_value or 235,)*3+(0,));wire.putalpha(Image.fromarray(wire_alpha));wire.save(HERE/f'item-detail-{f}.png')
 Image.fromarray(np.uint8(unknown)*255).save(HERE/f'authored-continuation-{f}.png')
 body=read(BODY/f'selected-{f}.png');zero=Image.new('RGBA',SIZE);zero.save(HERE/f'body-overlay-{f}.png');assert Image.open(HERE/f'body-visibility-{f}.png').getextrema()==(0,0)
 full=Image.alpha_composite(item,wire);assembly=Image.alpha_composite(body,full);assembly.save(HERE/f'assembled-{f}.png')
 colored=Image.alpha_composite(Image.alpha_composite(tint(body,colors['w']),tint(item,colors['w'])),tint(wire,colors['y']));colored.save(HERE/f'qud-palette-{f}.png')
 b=np.array(body);skin=(yy>=800)&(b[:,:,3]>200)&(b[:,:,:3].mean(2)>120)&(pa[:,:,3]<200);assert np.count_nonzero(skin)==0,f
 for k,im in [('assembly',assembly),('item',full),('detail',wire),('zero',zero),('off',Image.alpha_composite(body,item)),('palette',colored),('continued',Image.fromarray(np.uint8(unknown)*255).convert('RGBA'))]:groups[k][f]=im
 rows=[]
 for component,name,role,layer in [('item','intact-boot','equipment',.0007),('item-detail','item-detail','equipment-detail',.00075)]:
  row=dict(bm['views'][f][0]);row.update(component=component,file=f'yrame-leather-boots-v1-{component}-{f}.png',public_file=ref(HERE/f'{name}-{f}.png')['path'],sha256=ref(HERE/f'{name}-{f}.png')['sha256'],equipment_key='leather-boots@Feet@16',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(body=ref(BODY/f'selected-{f}.png'),full_boot=ref(HERE/f'intact-boot-{f}.png'),wire=ref(HERE/f'item-detail-{f}.png'),visibility=ref(HERE/f'body-visibility-{f}.png'),empty_overlay=ref(HERE/f'body-overlay-{f}.png'))
 model['individual_boots'][f]={}
 for name,region_ref in packet['individual_boot_regions'][f].items():
  region=np.array(Image.open(ROOT/region_ref['path']).convert('L'))>0
  for label,im in [('boot',item),('wire',wire)]:
   part=im.copy();a=np.array(part.getchannel('A'));a[~region]=0;part.putalpha(Image.fromarray(a));part.save(HERE/f'individual-{name}-{label}-{f}.png')
  model['individual_boots'][f][name]=dict(full=ref(HERE/f'individual-{name}-boot-{f}.png'),detail=ref(HERE/f'individual-{name}-wire-{f}.png'),frame='Unchanged 512x1024 authoring frame. Mutation placement must derive actual part attachment later; no native foot anchor inferred.')
 record['views'][f]=dict(known_surface_pixels=int(known.sum()),authored_continuation_pixels=int(unknown.sum()),wire_brightness=wire_value,wire_geometry='Original editable constructed cord; raw wire excluded from leather to avoid a shifted highlight fringe',full_source_alpha_unchanged=np.array_equal(np.array(item)[:,:,3],pa[:,:,3]),uncovered_bright_foot_pixels=int(skin.sum()),fit='Identity on fixed feet; original body/contact unchanged',**model['occlusion_sources'][f])
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
for k,name,title,feet in [('assembly','assembly-comparison.png','YRAME / Leather Boots only on ordinary fixed human base',False),('assembly','footwear-comparison.png','CLOSED BOOTS / covered feet, natural cuffs and no back laces',True),('item','intact-garment-comparison.png','FULL BOOTS / complete leather plus separately owned wire',True),('detail','wire-detail-comparison.png','WIRE y / neutral laces; rear view intentionally empty',True),('zero','body-overlay-comparison.png','BODY OVERLAY / zero; closed boots remain above skin',True),('continued','continuation-comparison.png','CONTINUATION / leather completed beneath wire and excluded edges',True),('palette','independent-palette-comparison.png','SOURCE COLORS / Yrame body w; leather w / wire y',True)]:plate(name,groups[k],title,feet)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',record)
print('Registered closed boots, independent wire, zero skin overlay and individual boot sources. Mutation placement and authoring review pending.')
