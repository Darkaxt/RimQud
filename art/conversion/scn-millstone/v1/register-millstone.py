"""One material refinement, fixed lower stone/hub and three controlled upper phase textures."""
from pathlib import Path
import json,hashlib,importlib.util,math
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists();assert json.loads((HERE/'first-structural-review.json').read_text())['status']=='PASS FOR MATERIAL ONLY'
helper=ROOT/'art/conversion/scn-book-table/v2/select-material.py';spec=importlib.util.spec_from_file_location('fixed_material',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
raw=read(HERE/'refined-raw.png');pattern=np.array(read(HERE/'frame-1-constructed.png'));own=np.array(read(HERE/'frame-1-ownership.png'));own[:,:,3]=pattern[:,:,3];own[own[:,:,3]==0,:3]=0;Image.fromarray(own).save(OUT/'ownership-master.png')
default,stats=m.select(raw,own,pattern);default.save(OUT/'default-material-master.png')
upattern=np.array(read(HERE/'upper.png'));uown=np.zeros_like(upattern);uown[:,:,3]=upattern[:,:,3];upper,ustats=m.select(raw,uown,upattern);u=np.array(upper);ink=upattern[:,:,:3].mean(2);mark=(ink<160)&(upattern[:,:,3]>0);u[mark,:3]=np.uint8(ink[mark])[:,None];upper=Image.fromarray(u);upper.save(OUT/'upper-material-master.png')
base=np.array(default);alpha=upattern[:,:,3];gray=u[:,:,0].astype(float);valid=alpha>128;nearest=ndimage.distance_transform_edt(~valid,return_distances=False,return_indices=True);extended=gray[nearest[0],nearest[1]]
yy,xx=np.indices(gray.shape);cx=8*32;cy=9.1*32;ratio=4.9/6.6;tx=xx-cx;ty=(yy-cy)/ratio
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.frombuffer(bytes.fromhex(palette['y']),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8)
packet=json.loads((HERE/'source-packet.json').read_text());frames=[];plates=[]
for k,angle in [(1,0),(2,40),(3,-40)]:
 theta=math.radians(angle);sx=cx+math.cos(theta)*tx+math.sin(theta)*ty;sy=cy+ratio*(-math.sin(theta)*tx+math.cos(theta)*ty)
 v=np.uint8(np.clip(np.round(ndimage.map_coordinates(extended,[sy,sx],order=1,mode='nearest')),0,255));layer=np.dstack([v,v,v,alpha]);assembled=Image.alpha_composite(default,Image.fromarray(layer));a=np.array(assembled)
 # Hub role is invariant; never turn generated gold pixels or a duplicate gray ring with the stone.
 hub=own[:,:,0]>0;a[hub]=base[hub];a[:,:,3]=pattern[:,:,3];a[a[:,:,3]==0,:3]=0
 master=Image.fromarray(a);master.save(OUT/f'frame-{k}-neutral-master.png')
 a=np.array(master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0
 neutral=Image.fromarray(a);neutral.save(OUT/f'frame-{k}-primary-neutral.png');coverage=a[:,:,3]
 r=np.array(Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'))[:,:,0];r[coverage==0]=0
 Image.fromarray(r).save(OUT/f'frame-{k}-detail-weight.png');Image.fromarray(coverage).save(OUT/f'frame-{k}-coverage.png');Image.fromarray(np.dstack([r,r,r,coverage])).save(OUT/f'frame-{k}-authored-dualcolor-mask.png')
 detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*r/255));detail[detail[:,:,3]==0,:3]=0;Image.fromarray(detail).save(OUT/f'frame-{k}-detail-neutral.png');Image.fromarray(detail[:,:,3]).save(OUT/f'frame-{k}-detail-coverage.png')
 weight=r.astype(float)/255;rgb=np.uint8(np.round((fg[None,None,:]*(1-weight[:,:,None])+dc[None,None,:]*weight[:,:,None])*a[:,:,:1]/255));rgb[coverage==0]=0;tint=Image.fromarray(np.dstack([rgb,coverage]));tint.save(OUT/f'frame-{k}-native-y-w.png')
 frames.append(dict(frame=k,native_tile=f'Items/sw_millstone_{k}.bmp',authored_material_angle_degrees=angle,**{key:ref(OUT/f'frame-{k}-{name}') for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]}));plates.append((k,neutral,tint))
model=dict(entry='SCN-MILLSTONE',kind='source_dualcolor_native_three_phase_machine',blueprint='Millstone',source=ref(HERE/'source-packet.json'),registration=packet['frame'],camera=packet['construction']['camera'],palette=packet['palette'],native_state_owner=packet['native_state'],native_behavior=packet['native_behavior'],native_acceptance=packet['native_acceptance'],native_activation=False,view_policy='One fixed source/cardinal map face,3source-declared phases. Native operational gate/subject-ignore/timing/recipes/container remain native; no new direction/rotation clock.',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',frames=frames);write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(helper=ref(helper),default_material_selection=stats,gray_upper_without_hub_selection=ustats,helper_roles=dict(wood='limestone slabs',top='central hub only; no wood/top material semantics'),phase_rule='Default whole material supplies fixed lower slab/hub. Separate gray upper material excludes gold hub by chroma and same-material continuation; manual carved seams restored. Rigid inverse ellipse-plane texture mapping at authored0,+40,-40degrees changes only upper RGB, never output coverage/center/scale. Hub pixels restored identically. Nearest valid upper surface extends sampling across antialias edge; no halo/background. Original3source masks retain native frame identities; angles are authored estimates.',new_imagegen_calls=1,second_isolation_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1420,850),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'QUD MILLSTONE / fixed lower slab + hub / three upper material phases / source y + w',font=font,fill='#e3cf43')
for i,(k,neutral,tint) in enumerate(plates):
 x=18+i*465
 for j,(label,im) in enumerate([('NEUTRAL',neutral),('SOURCE y/w',tint)]):
  large=im.resize((210,315),Image.Resampling.LANCZOS);plate.paste(large,(x+j*225,70),large);d.text((x+j*225,420),label,font=font,fill='#e3cf43')
 d.text((x,470),f'FRAME{k} / NATIVE OFFSET{(k-1)*100}',font=font,fill='#e3cf43')
 for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  thumb=tint.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+50+j*95,540),thumb)
for i,line in enumerate(['Same full cell, stone bounds and hub mask in every frame. Lower slab and hub material remain fixed.', 'Only upper material/carved seams rotate in authored ellipse-plane phases; native angles/timing are not inferred from pixels.', 'Original native animation length300/offsets0,100,200 and operational Mill gate/subject-ignore retained.', 'No generated halo, new dust/grain props, stand/motor, independent generated phases or native activation. Native acceptance pending.']):d.text((18,680+i*35),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print(json.dumps(dict(result='Registered3native millstone appearances',default_material=stats,upper_material=ustats,native_activation=False)))
