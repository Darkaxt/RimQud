"""Fixed source-shaped stock material and shared wood: one alpha, independent native color."""
from pathlib import Path
import importlib.util,json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists();hp=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('material',hp);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def components(mask):
 labels,n=ndimage.label(mask);rows=[]
 for k in range(1,n+1):
  ys,xs=np.where(labels==k)
  if len(xs)>=5:rows.append((len(xs),(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)))
 return sorted(rows,reverse=True)
stockmasters={};selection={}
for k in range(1,5):
 state=f'occupied-{k}';jr=json.loads((HERE/f'{state}-first-structural-review.json').read_text());assert jr['status']=='PASS FOR STOCK MATERIAL';raw=read(HERE/f'refined-{state}-raw.png');stockmasters[state]={};selection[state]={}
 for i,f in enumerate(['south','east','north','west']):
  col,row=i%2,i//2;panel=raw.crop((round(col*raw.width/2),round(row*raw.height/2),round((col+1)*raw.width/2),round((row+1)*raw.height/2)));panel.save(HERE/f'{state}-{f}-raw-material-panel.png');a=np.array(panel).astype(float);gold=(a[:,:,0]-a[:,:,2]>12)&(a[:,:,1]-a[:,:,2]>12)&(a[:,:,3]>128);sources=components(gold);pattern=np.array(read(HERE/f'normalized-{state}-{f}-stock.png'));gray=pattern[:,:,:2].max(2);pattern[:,:,:3]=gray[:,:,None];pattern[pattern[:,:,3]==0,:3]=0;targets=components(pattern[:,:,3]>128);assert len(sources)>=len(targets),(state,f,len(sources),len(targets));mapped=Image.new('RGBA',(512,768));mapping=[]
  for (_,sb),(_,tb) in zip(sources,targets):
   mapped.alpha_composite(panel.crop(sb).resize((tb[2]-tb[0],tb[3]-tb[1]),Image.Resampling.LANCZOS),(tb[0],tb[1]));mapping.append(dict(source_material_bounds=sb,target_component_bounds=tb))
  mapped.save(HERE/f'{state}-{f}-mapped-material.png');own=pattern.copy();own[:,:,:3]=255;master,stats=m.select(mapped,own,pattern);master.save(HERE/f'selected-{state}-{f}-stock-neutral.png');stockmasters[state][f]=master;selection[state][f]=dict(mapping=mapping,selection=stats,source_gold_components=len(sources),target_visible_components=len(targets),rule='Component bounds remap RGB material only; fixed normalized vector alpha/outline/positions/openings stay authoritative. Occluded visible components need not equal underlying part count. Gold key neutralized; no second isolation.')
write(HERE/'stock-material-selection.json',dict(helper=ref(hp),states=selection,internal_role_mapping=dict(top='all source stock',wood='unused'),generated_base='Never used: exact selected normalized empty base reused for every state.'))
packet=json.loads((HERE/'registered-source-packet.json').read_text());palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];states=['empty']+[f'occupied-{k}' for k in range(1,5)];views={f:dict(states={}) for f in ['south','east','north','west']};checks={};images={state:{g:{} for g in ['neutral','stock','detail-weight','native-upper-c','native-lower-c','native-lower-y','native-upper-w']} for state in states}
def production(im):
 a=np.array(im.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
for f in ['south','east','north','west']:
 folder=OUT/f;folder.mkdir(exist_ok=True);base_master=read(HERE/f'normalized-{f}-base-neutral.png');base_master.save(folder/'base-neutral-master.png');base=production(base_master);base.save(folder/'base-neutral.png');b=np.array(base).astype(float)/255;lb=b[:,:,0];ab=b[:,:,3];views[f].update(shared_base=ref(folder/'base-neutral.png'),canvas=[256,256],authoring_canvas=[512,768],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);checks[f]={}
 for state in states:
  sf=folder/state;sf.mkdir(exist_ok=True);stock=Image.new('RGBA',(256,256)) if state=='empty' else production(stockmasters[state][f]);stock.save(sf/'stock-neutral.png')
  if state!='empty':stockmasters[state][f].save(sf/'stock-neutral-master.png')
  s=np.array(stock).astype(float)/255;ls=s[:,:,0];ast=s[:,:,3];alpha=ast+ab*(1-ast);premult=ls*ast+lb*ab*(1-ast);lum=np.divide(premult,alpha,out=np.zeros_like(alpha),where=alpha>0);weight=np.divide(ls*ast,premult,out=np.zeros_like(alpha),where=premult>0);weight[(premult==0)&(ast>0)]=1
  a=np.array(base) if state=='empty' else np.uint8(np.round(np.dstack([lum,lum,lum,alpha])*255));w=np.uint8(np.clip(np.round(weight*255),0,255));w[a[:,:,3]==0]=0;a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(sf/'primary-neutral.png');Image.fromarray(a[:,:,3]).save(sf/'coverage.png');Image.fromarray(w).save(sf/'detail-weight.png');detail=a.copy();detail[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*w/255));detail[detail[:,:,3]==0,:3]=0;Image.fromarray(detail).save(sf/'detail-neutral.png');Image.fromarray(detail[:,:,3]).save(sf/'detail-coverage.png');Image.fromarray(np.dstack([w,w,w,a[:,:,3]])).save(sf/'authored-dualcolor-mask.png');view={key:ref(sf/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png'),('stock','stock-neutral.png')]};view['native_tile']='Assets_Content_Textures_Tiles_sw_table.bmp' if state=='empty' else f'Items/sw_table{state[-1]}.bmp';views[f]['states'][state]=view;images[state]['neutral'][f]=primary;images[state]['stock'][f]=stock;images[state]['detail-weight'][f]=Image.fromarray(np.dstack([w,w,w,a[:,:,3]]));errors={}
  for name,code in [('upper-c','C'),('lower-c','c'),('lower-y','y'),('upper-w','W')]:
   fg=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8).astype(float);dc=np.frombuffer(bytes.fromhex(palette[code]),dtype=np.uint8).astype(float);r=w.astype(float)/255;rgb=np.uint8(np.round((fg[None,None,:]*(1-r[:,:,None])+dc[None,None,:]*r[:,:,None])*a[:,:,:1]/255));rgb[a[:,:,3]==0]=0;im=Image.fromarray(np.dstack([rgb,a[:,:,3]]));im.save(sf/f'native-primary-w-detail-{name}.png');images[state][f'native-{name}'][f]=im;exact=np.divide((ls*ast)[:,:,None]*dc+(lb*ab*(1-ast))[:,:,None]*fg,alpha[:,:,None],out=np.zeros((256,256,3)),where=alpha[:,:,None]>0);valid=a[:,:,3]>0;errors[code]=float(np.abs(exact[valid]-rgb[valid]).max())
  edge=a[:,:,3];checks[f][state]=dict(edge_alpha_sum=int(edge[0].sum()+edge[-1].sum()+edge[:,0].sum()+edge[:,-1].sum()),max_palette_quantization_error=errors,unchanged_selected_base=True,detail_pixels=int((w>0).sum()))
model=dict(entry='SCN-TABLE',kind='directional_inventory_state_dualcolor_furniture',blueprint='Table',source=ref(HERE/'registered-source-packet.json'),views=views,states=views['south']['states'],registration=packet['frame'],camera=packet['camera'],palette=packet['palette'],native_behavior=packet['native_behavior'],state_owner=packet['native_state'],native_acceptance=packet['native_acceptance'],west_policy='Symmetric empty E base mirrored; each occupied W is physically projected separately with its stock position/handle edge and near/far overlap.',color_formula='A*L*((1-R)*foreground+R*detail)+(1-A)*background; stock role R is stock premultiplied luminance divided by total premultiplied luminance, preserving component tint through overlap with one coverage.')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(checks=checks,new_imagegen_calls=5,second_isolation_call=False,material_selection=ref(HERE/'stock-material-selection.json'),shared_frame_correction=ref(HERE/'shared-frame-correction.json'),native_state='5actual source shapes,4independent occupied color choices; masks permit16shape/color combinations without new generated variants. Native Inventory owns actual selection.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for state,groups in images.items():
 for name,group in groups.items():
  if state=='empty' and name not in ['neutral','native-upper-c','detail-weight']:continue
  plate=Image.new('RGB',(1440,650),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),f'TABLE / {state.upper()} / {name.upper()} / exact shared wood base, separate stock and native colors',font=font,fill='#e3cf43')
  for i,(f,im) in enumerate(group.items()):
   x=18+i*355;large=im.resize((320,480),Image.Resampling.LANCZOS);plate.paste(large,(x,50),large);d.text((x,535),f.upper(),font=font,fill='#e3cf43')
   for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+45+j*90,565),thumb)
  d.text((18,625),'Native Inventory selects actual tile + independent detail C,c,y,W. Common0.92registration; extra views/native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{state}-{name}.png')
plate=Image.new('RGB',(1440,2050),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'ORDINARY TABLE / five exact source appearances / native w wood + illustrative C stock / common source frame',font=font,fill='#e3cf43')
for row,state in enumerate(states):
 y=55+row*390;d.text((18,y),state.upper(),font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(images[state]['native-upper-c'].items()):
  x=18+i*355;large=im.resize((235,352),Image.Resampling.LANCZOS);plate.paste(large,(x+45,y+20),large);d.text((x,y+350),f.upper(),font=font,fill='#e3cf43')
d.text((18,2020),'All appearances share the exact same selected wood; extra stock directions unbound. Native state/color/physics acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/'all-states-native-upper-c.png');print('Registered5source states in4views, one unchanged base and independent single-alpha native stock colors.');print('Maximum edge alpha:',max(c['edge_alpha_sum'] for f in checks.values() for c in f.values()));print('Maximum color quantization error:',max(max(c['max_palette_quantization_error'].values()) for f in checks.values() for c in f.values()))
