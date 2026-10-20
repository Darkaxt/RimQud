"""Group split color-key material of one connected stock shape, without geometry changes."""
from pathlib import Path
import json,hashlib,shutil,importlib.util
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'registered';OUT=HERE/'registered-final'
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not OUT.exists();shutil.copytree(OLD,OUT);hp=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('material',hp);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);raw=read(HERE/'refined-occupied-4-raw.png');palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];records={}
for f,col in [('south',0),('east',1)]:
 panel=raw.crop((round(col*raw.width/2),0,round((col+1)*raw.width/2),round(raw.height/2)));a=np.array(panel).astype(float);gold=(a[:,:,0]-a[:,:,2]>12)&(a[:,:,1]-a[:,:,2]>12)&(a[:,:,3]>128);labels,n=ndimage.label(gold);members=[]
 for k in range(1,n+1):
  ys,xs=np.where(labels==k)
  if len(xs)>=5:members.append((int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1))
 assert len(members)==2;sb=(min(b[0] for b in members),min(b[1] for b in members),max(b[2] for b in members),max(b[3] for b in members));pattern=np.array(read(HERE/f'normalized-occupied-4-{f}-stock.png'));pattern[:,:,:3]=pattern[:,:,:2].max(2)[:,:,None];pattern[pattern[:,:,3]==0,:3]=0;tb=Image.fromarray(pattern).getbbox();mapped=Image.new('RGBA',(512,768));mapped.alpha_composite(panel.crop(sb).resize((tb[2]-tb[0],tb[3]-tb[1]),Image.Resampling.LANCZOS),(tb[0],tb[1]));mapped.save(HERE/f'corrected-stock4-{f}-mapped-material.png');own=pattern.copy();own[:,:,:3]=255;master,stats=m.select(mapped,own,pattern);sf=OUT/f/'occupied-4';master.save(sf/'stock-neutral-master.png');assert np.array_equal(np.array(master)[:,:,3],np.array(read(OLD/f/'occupied-4/stock-neutral-master.png'))[:,:,3]);s=np.array(master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));s[:,:,:3]=np.uint8(np.round(s[:,:,:3].mean(2)))[:,:,None];s[s[:,:,3]==0,:3]=0;Image.fromarray(s).save(sf/'stock-neutral.png');s=s.astype(float)/255;b=np.array(read(OUT/f/'base-neutral.png')).astype(float)/255;ast=s[:,:,3];ab=b[:,:,3];ls=s[:,:,0];lb=b[:,:,0];alpha=ast+ab*(1-ast);premult=ls*ast+lb*ab*(1-ast);lum=np.divide(premult,alpha,out=np.zeros_like(alpha),where=alpha>0);r=np.divide(ls*ast,premult,out=np.zeros_like(alpha),where=premult>0);r[(premult==0)&(ast>0)]=1;a=np.uint8(np.round(np.dstack([lum,lum,lum,alpha])*255));a[a[:,:,3]==0,:3]=0;w=np.uint8(np.clip(np.round(r*255),0,255));w[a[:,:,3]==0]=0;Image.fromarray(a).save(sf/'primary-neutral.png');Image.fromarray(a[:,:,3]).save(sf/'coverage.png');Image.fromarray(w).save(sf/'detail-weight.png');detail=a.copy();detail[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*w/255));detail[detail[:,:,3]==0,:3]=0;Image.fromarray(detail).save(sf/'detail-neutral.png');Image.fromarray(detail[:,:,3]).save(sf/'detail-coverage.png');Image.fromarray(np.dstack([w,w,w,a[:,:,3]])).save(sf/'authored-dualcolor-mask.png');errors={}
 for name,code in [('upper-c','C'),('lower-c','c'),('lower-y','y'),('upper-w','W')]:
  fg=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8).astype(float);dc=np.frombuffer(bytes.fromhex(palette[code]),dtype=np.uint8).astype(float);rr=w.astype(float)/255;rgb=np.uint8(np.round((fg[None,None,:]*(1-rr[:,:,None])+dc[None,None,:]*rr[:,:,None])*a[:,:,:1]/255));rgb[a[:,:,3]==0]=0;Image.fromarray(np.dstack([rgb,a[:,:,3]])).save(sf/f'native-primary-w-detail-{name}.png');exact=np.divide((ls*ast)[:,:,None]*dc+(lb*ab*(1-ast))[:,:,None]*fg,alpha[:,:,None],out=np.zeros((256,256,3)),where=alpha[:,:,None]>0);valid=a[:,:,3]>0;errors[code]=float(np.abs(exact[valid]-rgb[valid]).max())
 records[f]=dict(source_key_members=members,union_material_bounds=sb,target_material_extent=tb,selection=stats,max_palette_quantization_error=errors,unchanged_stock_alpha=True,unchanged_base=True)
model=json.loads((OLD/'model.json').read_text())
def update(v):
 if isinstance(v,dict):
  if 'path' in v and 'sha256' in v and v['path'].startswith(OLD.relative_to(ROOT).as_posix()+'/'):v.update(ref(ROOT/v['path'].replace('/registered/','/registered-final/')))
  else:
   for x in v.values():update(x)
 elif isinstance(v,list):
  for x in v:update(x)
update(model);write(OUT/'model.json',model);write(HERE/'stock4-key-group-correction.json',dict(reason='Stock4S/E is one connected constructed form but generated gold-key classifier separates body/frame at dark outlines. Initial largest-component sampling omitted valid upper bar material. Use union of both actual key members for one RGB material mapping.',views=records,helper=ref(hp),initial=ref(OLD/'model.json'),final=ref(OUT/'model.json'),all_other_views_states_unchanged=True,new_imagegen_calls=0,second_isolation_call=False));decisions=json.loads((OLD/'registration-decisions.json').read_text());decisions['stock4_key_group_correction']=ref(HERE/'stock4-key-group-correction.json')
for f,r in records.items():decisions['checks'][f]['occupied-4']['max_palette_quantization_error']=r['max_palette_quantization_error']
write(OUT/'registration-decisions.json',decisions);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,filename in [('neutral','primary-neutral.png'),('stock','stock-neutral.png'),('detail-weight','authored-dualcolor-mask.png')]+[(f'native-{n}',f'native-primary-w-detail-{n}.png') for n in ['upper-c','lower-c','lower-y','upper-w']]:
 plate=Image.new('RGB',(1440,650),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),f'TABLE / OCCUPIED-4 / {group.upper()} / complete source key group sampled, exact geometry and wood retained',font=font,fill='#e3cf43')
 for i,f in enumerate(['south','east','north','west']):
  im=read(OUT/f/'occupied-4'/filename);x=18+i*355;large=im.resize((320,480),Image.Resampling.LANCZOS);plate.paste(large,(x,50),large);d.text((x,535),f.upper(),font=font,fill='#e3cf43')
  for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+45+j*90,565),thumb)
 d.text((18,625),'Same fixed alpha/positions/frame. Stock material only; native Inventory/color and extra-view acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-occupied-4-{group}.png')
plate=Image.new('RGB',(1440,2050),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'ORDINARY TABLE / five source appearances / native w wood + illustrative C stock / one shared normalized frame',font=font,fill='#e3cf43')
for row,state in enumerate(['empty']+[f'occupied-{k}' for k in range(1,5)]):
 y=55+row*390;d.text((18,y),state.upper(),font=font,fill='#e3cf43')
 for i,f in enumerate(['south','east','north','west']):
  im=read(OUT/f/state/'native-primary-w-detail-upper-c.png').resize((235,352),Image.Resampling.LANCZOS);x=18+i*355;plate.paste(im,(x+45,y+20),im);d.text((x,y+350),f.upper(),font=font,fill='#e3cf43')
d.text((18,2020),'Same wood pixels across all5appearances; independent native stock colors. Extra views unbound; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/'all-states-native-upper-c.png')
comparison=Image.new('RGB',(1440,650),'#142823');d=ImageDraw.Draw(comparison);d.text((18,15),'STOCK4 MATERIAL / initial largest-key-region versus corrected complete key group / geometry and wood identical',font=font,fill='#e3cf43')
for i,(f,folder) in enumerate([('south',OLD),('south',OUT),('east',OLD),('east',OUT)]):
 im=read(folder/f/'occupied-4/stock-neutral.png').resize((320,480),Image.Resampling.LANCZOS);comparison.paste(im,(18+i*355,55),im);d.text((18+i*355,550),f.upper()+' / '+('INITIAL' if folder==OLD else 'CORRECTED'),font=font,fill='#e3cf43')
comparison.save(HERE/'stock4-key-group-comparison.png');print('Corrected stock4S/E material-key grouping only; initial evidence preserved, same base and coverage.')
