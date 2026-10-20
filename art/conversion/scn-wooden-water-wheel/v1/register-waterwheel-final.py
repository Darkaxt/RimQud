"""Reuse default wet wood/detail material in exact three source-frame constructions."""
from pathlib import Path
import json,hashlib,importlib.util
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered-final';OUT.mkdir(exist_ok=True)
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists();assert json.loads((HERE/'first-structural-review.json').read_text())['status']=='PASS FOR MATERIAL ONLY'
helper=HERE/'select-wet-wood-material.py';spec=importlib.util.spec_from_file_location('wet_material',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
pattern=np.array(read(HERE/'frame-1-patched-constructed.png'));own=np.array(read(HERE/'frame-1-patched-ownership.png'));own[:,:,3]=pattern[:,:,3];own[own[:,:,3]==0,:3]=0;default,stats=m.select(read(HERE/'refined-raw.png'),own,pattern);default.save(OUT/'default-material-master.png');base=np.array(default);luma=base[:,:,0].astype(float)
def extend(mask):
 inds=ndimage.distance_transform_edt(~mask,return_distances=False,return_indices=True);return luma[inds[0],inds[1]]
wood=extend((own[:,:,3]>128)&(own[:,:,0]<128));detail_interior=ndimage.binary_erosion((own[:,:,3]>250)&(own[:,:,0]>250),iterations=1)&(luma>145);assert detail_interior.any();detail=extend(detail_interior)
def paddle_mask(y):
 left=2.2 if y<5 or y>18 else 1.45;im=Image.new('1',(512,768));ImageDraw.Draw(im).polygon([(left*32,y*32),(7.6*32,y*32),(7.6*32,(y+3.3)*32),(5.5*32,(y+3.3)*32),(left*32,(y+.85)*32)],fill=1);return np.array(im)
source_paddle=paddle_mask(5.3);inds=ndimage.distance_transform_edt(~source_paddle,return_distances=False,return_indices=True);paddle_material=wood[inds[0],inds[1]]
yy,xx=np.indices(wood.shape);packet=json.loads((HERE/'corrected-source-packet.json').read_text());paddles=packet['construction']['paddle_band_tops'];palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex(palette['y']),dtype=np.uint8);frames=[];plates=[]
for k in [1,2,3]:
 pattern=np.array(read(HERE/f'frame-{k}-patched-constructed.png'));own=np.array(read(HERE/f'frame-{k}-patched-ownership.png'));own[:,:,3]=pattern[:,:,3];own[own[:,:,3]==0,:3]=0;Image.fromarray(own).save(OUT/f'frame-{k}-ownership-master.png')
 gray=wood.copy()
 for y in paddles[str(k)]:
  left=2.2 if y<5 or y>18 else 1.45;sx=1.45*32+(xx-left*32)*(7.6-1.45)/(7.6-left);sy=yy+(5.3-y)*32;mapped=ndimage.map_coordinates(paddle_material,[sy,sx],order=1,mode='nearest');mask=paddle_mask(y);gray[mask]=mapped[mask]
 weight=own[:,:,0].astype(float)/255;gray=gray*(1-weight)+detail*weight;ink=pattern[:,:,:3].mean(2);area=pattern[:,:,3]>0;marks=area&(ink<120);gray[marks]=np.minimum(ink[marks],gray[marks]*.7);v=np.uint8(np.clip(np.round(gray),0,255));v[~area]=0;master=Image.fromarray(np.dstack([v,v,v,pattern[:,:,3]]));master.save(OUT/f'frame-{k}-neutral-master.png')
 a=np.array(master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;neutral=Image.fromarray(a);neutral.save(OUT/f'frame-{k}-primary-neutral.png');coverage=a[:,:,3];r=np.array(Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'))[:,:,0];r[coverage==0]=0
 Image.fromarray(r).save(OUT/f'frame-{k}-detail-weight.png');Image.fromarray(coverage).save(OUT/f'frame-{k}-coverage.png');Image.fromarray(np.dstack([r,r,r,coverage])).save(OUT/f'frame-{k}-authored-dualcolor-mask.png');d=a.copy();d[:,:,3]=np.uint8(np.round(coverage.astype(float)*r/255));d[d[:,:,3]==0,:3]=0;Image.fromarray(d).save(OUT/f'frame-{k}-detail-neutral.png');Image.fromarray(d[:,:,3]).save(OUT/f'frame-{k}-detail-coverage.png');w=r.astype(float)/255;rgb=np.uint8(np.round((fg[None,None,:]*(1-w[:,:,None])+dc[None,None,:]*w[:,:,None])*a[:,:,:1]/255));rgb[coverage==0]=0;tint=Image.fromarray(np.dstack([rgb,coverage]));tint.save(OUT/f'frame-{k}-native-w-y.png')
 frames.append(dict(frame=k,native_tile=f'Items/sw_waterwheel_{k}.bmp',**{key:ref(OUT/f'frame-{k}-{name}') for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]}));plates.append((k,neutral,tint))
model=dict(entry='SCN-WOODEN-WATER-WHEEL',kind='source_dualcolor_native_three_phase_machine',blueprint='Wooden Water Wheel',source=ref(HERE/'corrected-source-packet.json'),registration=packet['frame'],camera=packet['construction']['camera'],palette=packet['palette'],native_state_owner=packet['native_state'],native_behavior=packet['native_behavior'],native_acceptance=packet['native_acceptance'],native_activation=False,view_policy='One source cardinal map face,3declared native phases; native HydroTurbine/liquid/charge/status/timing and rare Animated remain native.',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',frames=frames);write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(helper=ref(helper),selection=stats,wet_wood_floor=45,reason='Inspected raw mapped primary wood luminance quantiles10/50/90=15/56.67/80.67; standard105floor rejects wet-rot body.45floor selects actual damp gray wood while excluding darkest displaced ink. Gold detail retains150floor. Fixed alpha/ink excludes halo/background. No brightness normalization or baked donor brown.',phase_rule='Default primary/detail planes extend separately to avoid cross-role/halo contamination. One actual default paddle material maps locally by translation/width into each source-phase paddle group; fixed rim/spine use shared wood coordinates. Right detail material samples bright eroded interiors only, excluding old-pattern manual ink before transfer; each target restores its own edges. Exact source patterns and authored continuity brace remain. Output alpha/pivot/geometry remain per-phase editable construction. No independent generated frames or bounds fitting.',new_imagegen_calls=1,second_isolation_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1420,850),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'WOODEN WATER WHEEL / shared wet-rot material /3source paddle+detail phases / native w/y',font=font,fill='#e3cf43')
for i,(k,neutral,tint) in enumerate(plates):
 x=18+i*465
 for j,(label,im) in enumerate([('NEUTRAL',neutral),('SOURCE w/y',tint)]):
  im=im.resize((210,315),Image.Resampling.LANCZOS);plate.paste(im,(x+j*225,70),im);d.text((x+j*225,420),label,font=font,fill='#e3cf43')
 d.text((x,470),f'FRAME{k} / NATIVE OFFSET{(k-1)*100}',font=font,fill='#e3cf43')
 for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  thumb=tint.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+50+j*95,540),thumb)
for i,line in enumerate(['Fixed tall rim/spine, source-specific left paddle bands and right detail patterns; shared full cell/pivot/scale.', 'Wood remains dark with wet-rot; source w/y palette retained, no brown paint/glow/background or endplate fill.', 'Native length300/offsets0,100,200 and operational HydroTurbine/liquid/charge behavior retained.', 'Initial source guide, inset-continuity patch, one refinement and3controlled material phases logged. Native acceptance pending.']):d.text((18,680+i*35),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print(json.dumps(dict(result='Registered3native wheel appearances',selection=stats,native_activation=False)))
