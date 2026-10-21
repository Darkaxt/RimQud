"""Partition partially transparent source alpha instead of discarding its detail."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageOps,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'registered';OUT=HERE/'registered-v2';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def im(p):return Image.open(p).convert('RGBA')
def norm(a):
 a=a.copy();a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
assert not (OUT/'model.json').exists()
m=read(OLD/'model.json');controls=read(HERE/'manual-ownership-controls.json');dec=read(OLD/'registration-decisions.json');now=datetime.now(timezone.utc).isoformat();stats={};groups={k:{} for k in ['neutral','native','detail','material']}
for f in ['south','east','north']:
 full=np.array(im(OLD/f'full-neutral-{f}.png'));mask=Image.new('L',(512,512));d=ImageDraw.Draw(mask)
 if f=='south':d.ellipse((228,371,279,396),fill=255);d.polygon([(230,394),(277,394),(271,420),(252,433),(233,421)],fill=255)
 elif f=='east':d.ellipse((439,284,470,311),fill=255);d.polygon([(394,319),(421,317),(411,352),(399,373),(386,347)],fill=255)
 R=np.array(mask.filter(ImageFilter.GaussianBlur(1.2)));roi=Image.new('L',(512,512));rd=ImageDraw.Draw(roi);v=dec['views'][f];p=v['source_landmarks'];s=v['raster_scale']
 def point(x,y):return ((x-p['contact_x'])*s+256,(y-p['contact_y'])*s+448)
 for x0,y0,x1,y1 in controls['highlight_regions_in_selected_source_pixels'][f]:rd.rectangle((*point(x0,y0),*point(x1,y1)),fill=255)
 bright=(full[:,:,:3].mean(2)>244)&(np.array(roi)>0)&(full[:,:,3]>128);R=np.maximum(R,np.uint8(bright)*255);mask=Image.fromarray(R);mask.save(OUT/f'material-region-{f}.png')
 layers=[];neutral=Image.new('RGBA',(512,512));native=Image.new('RGBA',(512,512));detailview=Image.new('RGBA',(512,512));partial=[]
 for component in ['body','head']:
  r=next(r for r in m['views'][f] if r['component']==component and r['color_role']=='foreground');a=np.array(im(ROOT/r['public_file']));A=a[:,:,3].astype(float)
  D=np.round(A*R/255);P=np.round(np.divide((A-D)*255,255-D,out=np.zeros_like(A),where=D<255))
  # D + P*(1-D) reconstructs original alpha after integer encoding.
  assert (P>=0).all() and (P<=255).all();partial.append(int(((A>0)&(A<255)).sum()))
  for role,alpha in [('foreground',P),('detail',D)]:
   b=a.copy();b[:,:,3]=np.uint8(alpha);img=norm(b);path=OUT/f'{component}-{role}-{f}.png';img.save(path);row=dict(r,file='ray-cat-'+path.name,public_file=ref(path)['path'],sha256=ref(path)['sha256'],color_role=role,layer=(0 if component=='body' else .001)+(0 if role=='foreground' else .0001));layers.append(row);neutral.alpha_composite(img)
   c=np.array(img);col=np.array([177,84,207] if role=='foreground' else [177,201,195]);c[:,:,:3]=np.uint8(np.round(c[:,:,:3].mean(2)[:,:,None]*col/255));native.alpha_composite(norm(c))
   if role=='detail':detailview.alpha_composite(img)
 assert np.array_equal(np.array(neutral),full),(f,'full neutral RGBA exact')
 for key,img in [('neutral',neutral),('native',native),('detail',detailview)]:groups[key][f]=img;norm(np.array(img)).save(OUT/(dict(neutral='recomposed-neutral',native='native-palette',detail='detail-ownership')[key]+f'-{f}.png'))
 mat=full.copy();mat[:,:,:3]=np.uint8(np.round(mat[:,:,:3].mean(2)[:,:,None]*np.where((R>128)[:,:,None],np.array([.4,1,.8]),np.array([1,.45,.4]))));groups['material'][f]=norm(mat)
 m['views'][f]=layers;stats[f]=dict(source_partial_alpha_pixels_by_part=partial,source_alpha_max=int(A.max()),detail_pixels=int((np.array(detailview)[:,:,3]>0).sum()),neutral_rgba_reconstruction_exact=True)
for key in groups:groups[key]['west']=ImageOps.mirror(groups[key]['east'])
m['views']['west']=[]
for row in m['views']['east']:
 path=OUT/Path(row['public_file']).name.replace('-east.png','-west.png');ImageOps.mirror(im(ROOT/row['public_file'])).save(path);m['views']['west'].append(dict(row,file='ray-cat-'+path.name,public_file=ref(path)['path'],sha256=ref(path)['sha256'],already_mirrored_from_east=True))
for key in ['neutral','native','detail']:groups[key]['west'].save(OUT/(dict(neutral='recomposed-neutral',native='native-palette',detail='detail-ownership')[key]+'-west.png'))
rejection=dict(recorded_at=now,status='REJECTED tint candidate',source_model=ref(OLD/'model.json'),reason='Opaque-only filtering suppressed nearly all detail because accepted ImageGen coat interiors are generally partially transparent. Same-source alpha partition is required rather than making the artwork opaque or enlarging its alpha.',correction='For desired detail weight R: D=round(A*R), P=round((A-D)/(1-D)). Store unchanged shade RGB in each plane. Both planes reconstruct full neutral RGBA exactly.',measurements=stats)
write(OUT/'opaque-filter-rejection.json',rejection);m.update(detail_partition=ref(OUT/'opaque-filter-rejection.json'),supersedes=ref(OLD/'model.json'),detail_policy='Current source-bound pale muzzle/bib and sparse existing glass strokes; mathematical alpha partition preserves selected neutral RGBA exactly, including partial-alpha edges.')
write(OUT/'model.json',m);write(OUT/'registration-decisions.json',dict(recorded_at=now,frame=m['registration'],spatial_registration=ref(OLD/'registration-decisions.json'),detail_partition=ref(OUT/'opaque-filter-rejection.json'),checks=stats,new_imagegen_calls=0))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for key,name,title in [('neutral','assembly-comparison.png','ACCEPTED RAY CAT / exact neutral reconstruction; common pivot and original scale'),('native','native-palette-comparison.png','NATIVE m COAT / y MUZZLE, BIB AND SPARSE GLASS STROKES'),('detail','detail-comparison.png','SEPARATE y DETAIL / same shade pixels; original partial alpha preserved'),('material','material-ownership-comparison.png','MANUAL MATERIAL OWNERSHIP / salmon primary; mint secondary; final art stays intact')]:
 out=Image.new('RGB',(1200,440),'#142823');d=ImageDraw.Draw(out);d.text((15,15),title,font=font,fill='#e3cf43')
 for i,f in enumerate(['south','east','north','west']):
  bg=Image.new('RGBA',(512,512),'#20382d');bg.alpha_composite(groups[key][f]);out.paste(bg.resize((280,280),Image.Resampling.LANCZOS).convert('RGB'),(10+i*300,55));d.line((150+i*300,55,150+i*300,335),fill='#b2a94d');d.line((10+i*300,300,290+i*300,300),fill='#6b9d8a');d.text((15+i*300,360),f.upper(),font=font,fill='#e3cf43')
 d.text((15,407),'Source image and body shape retained. Authoring only; native acceptance remains pending.',font=font,fill='#e5e8d8');out.save(OUT/name)
small=Image.new('RGB',(800,360),'#142823');d=ImageDraw.Draw(small)
for j,key in enumerate(['neutral','native']):
 for i,f in enumerate(['south','east','north','west']):
  img=groups[key][f].resize((64,64),Image.Resampling.LANCZOS);small.paste(img,(15+i*200,15+j*170),img);zoom=img.resize((128,128),Image.Resampling.NEAREST);small.paste(zoom,(75+i*200,15+j*170),zoom);d.text((15+i*200,150+j*170),f.upper(),font=font,fill='#e3cf43')
small.save(OUT/'game-scale-review.png')
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='BODY-RAY-CAT';e=next(e for e in l['entries'] if e['id']==l['active_entry']);reason='Reject opaque-only tint filter and partition original partial alpha exactly. Shared registered geometry, accepted source/world scale and head/body ownership are unchanged. Actual current tint/attachment review pending.'
e['process_log'].append(dict(timestamp=now,step='register_required_layers_and_color_masks',action=reason,inputs=[ref(OLD/'model.json')],outputs=[ref(OUT/n) for n in ['opaque-filter-rejection.json','registration-decisions.json','model.json','assembly-comparison.png','native-palette-comparison.png','detail-comparison.png','material-ownership-comparison.png','game-scale-review.png']],review=reason,result='REQUIRES REVIEW'));e.update(current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'assembly-comparison.png')));l['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Exact source-alpha material partition registered; tint review pending.')
