"""Register three direct Blender phases under the existing dual-color contract."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'model.json').exists()
model=copy.deepcopy(json.loads((OLD/'registered-final/model.json').read_text()));previews={};checks={}
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.array(list(bytes.fromhex(palette['w'])));dc=np.array(list(bytes.fromhex(palette['y'])))
for row in model['frames']:
    k=row['frame'];im=Image.open(HERE/f'frame-{k}-neutral-master.png').convert('RGBA');a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;neutral=Image.fromarray(a)
    detail=np.array(Image.open(HERE/f'frame-{k}-detail-pass.png').convert('RGBA'));detail_alpha=np.minimum(detail[:,:,3],a[:,:,3]);detail_coverage=Image.fromarray(detail_alpha)
    primary=neutral.resize((256,256),Image.Resampling.LANCZOS);pa=np.array(primary);pa[pa[:,:,3]<4]=0;primary=Image.fromarray(pa)
    da=np.minimum(np.array(detail_coverage.resize((256,256),Image.Resampling.LANCZOS)),pa[:,:,3])
    weight=np.uint8(np.clip(np.round(np.divide(da.astype(float)*255,pa[:,:,3],out=np.zeros(da.shape),where=pa[:,:,3]>0)),0,255))
    detail_layer=pa.copy();detail_layer[:,:,3]=da;detail_layer[da==0,:3]=0
    mask=np.dstack([weight,weight,weight,pa[:,:,3]])
    files={'primary':primary,'detail':Image.fromarray(detail_layer),'coverage':primary.getchannel('A'),'detail_weight':Image.fromarray(weight),'detail_coverage':Image.fromarray(da),'authored_dualcolor_mask':Image.fromarray(mask)}
    for key,image in files.items():
        p=OUT/f'frame-{k}-{key}.png';image.save(p);row[key]=ref(p)
    w=weight.astype(float)/255;colors=(1-w[:,:,None])*fg+w[:,:,None]*dc;native=pa.copy();native[:,:,:3]=np.uint8(np.round(pa[:,:,:3].astype(float)*colors/255));native[native[:,:,3]==0,:3]=0
    Image.fromarray(native).save(OUT/f'frame-{k}-native-w-y.png')
    # High-resolution proof uses the same one-coverage formula.
    wm=np.divide(detail_alpha.astype(float),a[:,:,3],out=np.zeros(detail_alpha.shape),where=a[:,:,3]>0);big=a.copy();big[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float)*((1-wm[:,:,None])*fg+wm[:,:,None]*dc)/255));big[big[:,:,3]==0,:3]=0
    previews[k]=(neutral,Image.fromarray(big));checks[k]=dict(common_full_frame=[512,768],recipient_frame=[256,256],anchor=[8,16],detail_coverage_subset=True,neutral_equal_rgb=True)
model.update(workflow='blender-first-v1',blender_source=ref(HERE/'wheel.blend'),blender_controls=ref(HERE/'model-controls.json'),
    authored_support_interpretation='Two rear wet-wood crossmembers attach the inset carrier to existing spine/rim. Detail runs keep source-bound positions and connect to this carrier. Supports are authored, not recovered native topology.',
    native_acceptance='Pending full generation gate; no native activation')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(method='Common full source-cell projection for all three native phases. Same registration/clock/behavior fields retained.',checks=checks,
    source_selection='Direct neutral Blender geometry with simple material/contour. No new ImageGen call or 2D isolation.',
    color_formula='A*L*((1-weight)*foreground+weight*detail); detail coverage is conditional ownership, never an added coverage layer.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1420,835),'#142823');d=ImageDraw.Draw(plate)
d.text((18,15),'WOODEN WATER WHEEL / direct Blender / authored supported inset / native three phases',font=font,fill='#e3cf43')
for i,k in enumerate([1,2,3]):
    for j,(title,im) in enumerate(zip(['NEUTRAL','SOURCE w/y'],previews[k])):
        x=18+i*465+j*225;bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((208,312)),(x,65));d.text((x,410),title,font=font,fill='#e3cf43')
    d.text((18+i*465,460),f'FRAME{k} / NATIVE OFFSET{(k-1)*100}',font=font,fill='#e3cf43')
    for t,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
        small=previews[k][1].resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(70+i*465+t*95,530),small)
for i,line in enumerate(['Rear wood braces make the source inset belong to the existing spine and rim; hidden depth/supports are authored.',
    'Exact source-bound detail runs and three paddle arrangements retained; no invented axle, motor, water or new mechanics.',
    'Simple wet-wood shading and black contour. Native w/y roles use one coverage and independent detail ownership.',
    'Same source frame, anchor and native phase timing. Static authoring only; native acceptance remains pending.']):d.text((18,665+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
print('Three Blender wheel phases registered with supported inset and one-coverage native tint.')
