"""Register complete pottery and independent source-slip ownership in one frame."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'model.json').exists()
full=np.array(Image.open(HERE/'raw-neutral-master.png').convert('RGBA'));full[:,:,:3]=np.uint8(np.round(full[:,:,:3].mean(2)))[:,:,None];full[full[:,:,3]==0,:3]=0
slip=np.array(Image.open(HERE/'raw-slip-pass.png').convert('RGBA'));dcov=np.minimum(slip[:,:,3],full[:,:,3]);a=np.array(Image.fromarray(full).resize((256,256),Image.Resampling.LANCZOS));a[a[:,:,3]<4]=0;d=np.minimum(np.array(Image.fromarray(dcov).resize((256,256),Image.Resampling.LANCZOS)),a[:,:,3]);weight=np.uint8(np.clip(np.round(np.divide(d.astype(float)*255,a[:,:,3],out=np.zeros(d.shape),where=a[:,:,3]>0)),0,255));detail=a.copy();detail[:,:,3]=d;detail[d==0,:3]=0
row=dict(native_tile='Items/sw_jug.bmp')
for key,im in dict(primary=Image.fromarray(a),detail=Image.fromarray(detail),coverage=Image.fromarray(a[:,:,3]),detail_weight=Image.fromarray(weight),detail_coverage=Image.fromarray(d),authored_dualcolor_mask=Image.fromarray(np.dstack([weight,weight,weight,a[:,:,3]]))).items():
 p=OUT/f'vase-{key}.png';im.save(p);row[key]=ref(p)
pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.array(list(bytes.fromhex(pal['w'])));dc=np.array(list(bytes.fromhex(pal['g'])))
def tint(p,w):
 n=p.copy();n[:,:,:3]=np.uint8(np.round(p[:,:,:3].astype(float)*((1-w[:,:,None])*fg+w[:,:,None]*dc)/255));n[n[:,:,3]==0,:3]=0;return Image.fromarray(n)
native=tint(a,weight.astype(float)/255);native.save(OUT/'native-w-g.png');bigw=np.divide(dcov.astype(float),full[:,:,3],out=np.zeros(dcov.shape),where=full[:,:,3]>0);big=tint(full,bigw)
source=json.loads((HERE.parent/'blender-v1/source-packet.json').read_text())
model=dict(entry='SCN-VASE',kind='source_dualcolor_hollow_pottery',blueprint='Vase',workflow='blender-first-v1',source=ref(HERE.parent/'blender-v1/source-packet.json'),blender_source=ref(HERE/'vase.blend'),blender_controls=ref(HERE/'model-controls.json'),registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One fixed full-cell registration, no alpha-bound fitting or per-layer placement.'),camera=source['per_view_contract'],palette=source['palette'],native_behavior=source['native_behavior'],native_state_owner='One Items/sw_jug.bmp tile. RandomColors keeps main w, random detail all; liquid filling/storage/leak behavior remains native.',view_policy='Fixed source map face with both handles. Angled hollow-wall proof is diagnostic, not a new game-facing sprite.',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',frames=[row],native_activation=False,native_acceptance='Pending full generation gate')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(detail_coverage_subset=bool(np.all(d<=a[:,:,3])),neutral_equal_rgb=bool(not np.ptp(a[:,:,:3].astype(int),axis=2).any()),single_coverage=True,source_frame_anchor_unchanged=True,new_imagegen_call=False,method='Whole direct Blender vessel and visible decorative-slip material pass share one full-cell transform. Slip alpha becomes conditional detail ownership; never an extra coverage layer.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1540,810),'#142823');dr=ImageDraw.Draw(plate)
native_mask=np.array(Image.open(source['original_mask']['path']).convert('RGBA'));mw=native_mask[:,:,0].astype(float)/255;original=np.dstack([np.uint8(np.round((1-mw[:,:,None])*fg+mw[:,:,None]*dc)),native_mask[:,:,3]])
items=[('ORIGINAL / w+g',Image.fromarray(original)),('MANUAL / full shape',Image.open(HERE.parent/'blender-v1/manual-neutral-master.png')),('REFINED / direct Blender',Image.fromarray(full)),('NATIVE w/g',big),('SLIP / independent role',Image.fromarray(np.dstack([dcov,dcov,dcov,full[:,:,3]])))]
for i,(title,im) in enumerate(items):
 im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((280,420),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS),(15+305*i,55));dr.text((15+305*i,18),title,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize(size,Image.Resampling.LANCZOS);plate.paste(small,(60+305*i+70*j,515),small)
for i,line in enumerate(['Same source vase: complete hollow pottery, long neck, two joined handles and two decorative slip bands.',
 'Source w/g is the default only: native RandomColors detail all and liquid storage/fill behavior remain native.',
 'Direct Blender material/outline finishing. No ImageGen refinement or isolation was performed.',
 'One full-cell frame and anchor. Intended-size authoring evidence only; native acceptance remains gated.']):dr.text((15,635+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Vase registered with one coverage and independent two-band slip tint.')
