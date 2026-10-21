"""Register reviewed Blender states in one full cell and explicit single-coverage tint contract."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def read(p):return json.loads(p.read_text())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
r=read(HERE/'independent-structural-review.json');assert r['recommendation']=='pass' and not r['fix_now']
for a in r['inputs']:assert ref(ROOT/a['path'])==a
assert not (OUT/'model.json').exists();OUT.mkdir(exist_ok=True);STATES=OUT/'states';STATES.mkdir(exist_ok=True)
source=read(HERE.parent/'blender-v1/source-packet.json');controls=read(HERE/'model-controls.json');idx=read(HERE.parent/'blender-v1/native-state-index.json');pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.array(list(bytes.fromhex(pal['w'])));dt=np.array(list(bytes.fromhex(pal['r'])));rows=[];atlases={k:Image.new('RGBA' if k in ['primary','detail','authored_dualcolor_mask'] else 'L',(1024,1024)) for k in ['primary','detail','coverage','detail_weight','authored_dualcolor_mask']}
for st in idx['originals']:
 mask=st['mask'];p=np.array(Image.open(HERE/f'{mask:02d}-map-neutral.png').convert('RGBA'));p[:,:,:3]=np.uint8(np.round(p[:,:,:3].mean(2)))[:,:,None];p[p[:,:,3]==0,:3]=0;p=np.array(Image.fromarray(p).resize((256,256),Image.Resampling.LANCZOS));p[p[:,:,3]<4]=0
 da=np.array(Image.open(HERE/f'{mask:02d}-map-detail.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS))[:,:,3];da=np.minimum(da,p[:,:,3]);w=np.uint8(np.round(np.divide(da.astype(float)*255,p[:,:,3],out=np.zeros_like(da,dtype=float),where=p[:,:,3]>0)));ims=dict(primary=Image.fromarray(p),detail=Image.fromarray(p),coverage=Image.fromarray(p[:,:,3]),detail_weight=Image.fromarray(w),detail_coverage=Image.fromarray(da),authored_dualcolor_mask=Image.fromarray(np.dstack([w,w,w,p[:,:,3]])))
 xy=(mask%4*256,(3-mask//4)*256);row=dict(mask=mask,neighbors=[d for b,d in [(1,'N'),(2,'E'),(4,'S'),(8,'W')] if mask&b],native_tile=st['tile'],atlas_rect=[*xy,256,256])
 for key,im in ims.items():
  path=STATES/f'{mask:02d}-{key}.png';im.save(path);row[key]=ref(path)
  if key in atlases:atlases[key].paste(im,xy)
 tint=p.copy();tint[:,:,:3]=np.uint8(np.round(p[:,:,:3].astype(float)*((1-w[:,:,None]/255)*fg+w[:,:,None]/255*dt)/255));tint[tint[:,:,3]==0,:3]=0;Image.fromarray(tint).save(STATES/f'{mask:02d}-native-w-r.png');rows.append(row)
atlas_refs={}
for k,im in atlases.items():p=OUT/f'{k}-atlas.png';im.save(p);atlas_refs[k]=ref(p)
model=dict(kind='connected_wall_atlas',blueprint='CanvasWall',entry='SCN-CANVASWALL',workflow='blender-first-v1',source=ref(HERE.parent/'blender-v1/source-packet.json'),blender_source=ref(HERE/'canvas.blend'),controls=ref(HERE/'model-controls.json'),**atlas_refs,states=rows,atlas_size=[1024,1024],tile_size=[256,256],grid=[4,4],row_policy='Recipient bottom-origin mask order:col=mask%4,row=3-floor(mask/4)',bits=dict(N=1,E=2,S=4,W=8),registration=controls['registration'],palette=source['palette'],native_behavior=source['native_behavior'],connections=source['connections'],attachment_anchors=controls['attachment_anchors'],native_states=ref(HERE.parent/'blender-v1/native-state-index.json'),formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',alpha_contract='One coverage only. Primary and detail share equal neutral luminance/coverage; detail_weight determines tint ownership. Do not alpha-over the two complete layers, multiply edge coverage twice or freeze preview colors.',sampling_contract='Mask-selected atlas cell only; point filtering/texel-center sampling prevents packed-neighbor bleed.',native_activation=False,native_acceptance='Pending full generation gate')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(common_frame=True,per_state_bounds_fit=False,connected_side_crop_only=True,full_neutral_layers=True,single_coverage=True,exact_source_binary_alpha=False,source_translation='Complete subtly tensioned cloth replaces symbolic stepped tears/gaps; substantial irregular E/W red fold group and NS2pixel width retained. Hidden thickness and supporting continuations are authored.',gate_and_items=source['connections'],authoring_only=True,native_activation=False))
# Current registered proof uses saved production files, including palette and intended sizes.
plate=Image.new('RGB',(1408,1110),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for m in range(16):
 x=m%4*352;y=m//4*270;im=Image.open(STATES/f'{m:02d}-native-w-r.png').convert('RGBA');bg=Image.new('RGBA',(210,210),'#20382d');bg.alpha_composite(im.resize((210,210),Image.Resampling.LANCZOS));plate.paste(bg.convert('RGB'),(x+70,y+28));d.text((x+15,y+6),f'{m:02d} '+''.join(rows[m]['neighbors']),font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize(size,Image.Resampling.LANCZOS);plate.paste(small,(x+110+j*60,y+242),small)
d.text((15,1085),'Registered single-coverage w/r proof. Self-join16 masks; native item groups unchanged. Game acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/'registration-comparison.png')
print('Registered16 reviewed common-frame canvas states and semantic atlases; no native activation.')
