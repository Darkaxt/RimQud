"""Retain complete source-bound wool and original body ownership in all facings."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male-older/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
def complete(gray,known,envelope):
 unknown=envelope&~known;yy,xx=np.where(unknown);n=len(yy);ids=np.full(gray.shape,-1,np.int32);ids[yy,xx]=np.arange(n);deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
 if n:gray[yy,xx]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg),rhs)
 return gray,unknown
def plate(n,rows,title):
 out=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  x=16+i*284;bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,620),'Complete wool, original body and separate curved wrist/hand ownership. Native mutation/outfit acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/n)
raw=read(HERE/'refined-red-context.png');assert raw.size==(1536,1024);data={};white_samples=[]
for i,f in enumerate(['south','east','north']):
 a=np.array(read(HERE/f'constructed-cloth-{f}.png'));rgb=np.array(raw.crop((i*512,0,(i+1)*512,1024)))[:,:,:3].astype(float);env=a[:,:,3]>0;distance=ndimage.distance_transform_edt(env);red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3);known=(distance>10)&~ndimage.binary_dilation(red,iterations=2)&(rgb.max(2)-rgb.min(2)<25)&(rgb.mean(2)>50);assert known.sum()>20000,f;white_samples.append(rgb.mean(2)[known]);data[f]=(a,rgb,env,distance,known)
whitepoint=float(np.percentile(np.concatenate(white_samples),95));gain=235/whitepoint
bm=json.loads((BODY/'model.json').read_text());model=dict(item='Black Robes',blueprint='Black Robes',family='irudad',unmutated_body_family='human-male-older',slot='Body',laterality=0,workflow='regional-curved-v1',body_source=ref(BODY/'model.json'),actual_equipped_binding=json.loads((HERE/'source-packet.json').read_text())['actual_body_binding'],views={},occlusion_sources={},west_policy='Mirror east; symmetric plain robe',native_acceptance='Pending full-set gate; Irudad mutation/body/outfit assembly remains unfinished')
decisions=dict(context=ref(HERE/'refined-red-context.png'),body=ref(BODY/'model.json'),new_imagegen_call=True,second_isolation_call=False,generated_body_used=False,source_whitepoint_95=whitepoint,global_material_gain=gain,method='Use neutral same-output cloth inside the corrected editable whole envelope; exclude red/background, continue missing edges/hidden material before fitting. Preserve actual refined internal folds and restore only the constructed exterior ink. Shared material whitepoint makes native dark K tint readable without baking color.',fit='Identity to the corrected body-relative pattern: neckline/shoulders/cuffs/hem were constructed to the fixed original body; freeze all geometry. No unnecessary regional warp or body transform.',views={})
groups={k:{} for k in ['assembly','cloth','off','overlay','mask','palette','continued']}
for f,(a,rgb,env,distance,known) in data.items():
 gray,unknown=complete(rgb.mean(2),known,env);gray=np.clip(gray*gain,0,255);pg=a[:,:,:3].mean(2);ink=(distance<=3.5)&(pg<85)&env;gray[ink]=pg[ink];v=np.uint8(np.clip(np.round(gray),0,255));cloth=Image.fromarray(np.dstack([v,v,v,a[:,:,3]]));cloth.save(HERE/f'intact-robes-{f}.png');continued=Image.fromarray(np.uint8(unknown)*255);continued.save(HERE/f'authored-continuation-{f}.png')
 body=read(BODY/f'selected-{f}.png');overlay=read(HERE/f'body-overlay-{f}.png');mask=Image.open(HERE/f'body-visibility-{f}.png').convert('L');off=Image.alpha_composite(body,cloth);assembly=Image.alpha_composite(off,overlay);off.save(HERE/f'mask-off-{f}.png');assembly.save(HERE/f'assembled-{f}.png');palette=Image.alpha_composite(Image.alpha_composite(tint(body,(152,135,95)),tint(cloth,(21,83,82))),tint(overlay,(152,135,95)));palette.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('cloth',cloth),('off',off),('overlay',overlay),('mask',mask.convert('RGBA')),('palette',palette),('continued',continued.convert('RGBA'))]:groups[k][f]=im
 rows=[]
 for component,filename,role,layer in [('item','intact-robes','equipment',.0012),('body-overlay','body-overlay','foreground',.0013)]:
  row=dict(bm['views'][f][0]);row.update(component=component,file=f'irudad-black-robes-v2-{component}-{f}.png',public_file=ref(HERE/f'{filename}-{f}.png')['path'],sha256=ref(HERE/f'{filename}-{f}.png')['sha256'],equipment_key='black-robes@Body@0',color_role=role,layer=layer);rows.append(row)
 model['views'][f]=rows;model['occlusion_sources'][f]=dict(full_cloth=ref(HERE/f'intact-robes-{f}.png'),body_visibility=ref(HERE/f'body-visibility-{f}.png'),curved_wrist_svg=ref(HERE/f'body-visibility-{f}.svg'),original_body_overlay=ref(HERE/f'body-overlay-{f}.png'))
 decisions['views'][f]=dict(context_surface_pixels=int(known.sum()),authored_continuation_pixels=int(unknown.sum()),pattern=ref(HERE/f'pattern-{f}.svg'),original_body_unchanged=True,contact=[256,950],**model['occlusion_sources'][f])
for rows in groups.values():rows['west (mirror)']=ImageOps.mirror(rows['east'])
for k,n,title in [('assembly','assembly-comparison.png','BLACK ROBES / complete wool with unchanged original older-human body'),('cloth','intact-garment-comparison.png','FULL CLOTH / neckline, covered shoulders and intact long sleeves'),('off','mask-off-comparison.png','MASK OFF / complete source before original wrists/hands'),('overlay','body-overlay-comparison.png','OWNERSHIP / actual original wrists and complete hands only'),('mask','body-mask-comparison.png','CURVED WRIST MASKS / independent from continuous wool'),('palette','independent-palette-comparison.png','NATIVE COLORS / dark K/K wool; illustrative body w independent'),('continued','authored-continuation-comparison.png','CONTINUATION / source edge/hidden material completed before fitting')]:plate(n,groups[k],title)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',decisions);print('Registered full wool, actual native K tint and late curved wrist ownership; review pending.')
