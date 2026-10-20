"""Whole-image recenter/stretch comparison, explicitly requested by the user.

One X scale, Y scale and translation per facing. No local warp, mesh, material
repair or body change. Compare red-cut cloth with retained complete cloth.
"""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps
import numpy as np
import json,hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v2'
KEY=HERE.parent/'red-key-v1'
MASK=HERE.parent/'mask-fit-v4'
FULL=HERE.parent/'v1/registered'
assert not (HERE/'result.json').exists(),'Preserve recorded experiment'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):return Image.open(p).convert('RGBA')
key=read(KEY/'extracted-visible-clothing-sheet.png')
record={'scope':'Whole-image stretch authoring experiment; adult dromad robe only','method':'For each source/facing, map its alpha>128 bounding rectangle to the existing robe target rectangle using one nonuniform scale and translation. Resample full RGBA once with bicubic interpolation. Apply existing body exposure mask separately for depth. No local deformation, texture fill, body rescale or additional ImageGen call.','target_masks':asset(MASK/'body-clothing-profiles.json'),'body':asset(BODY/'model.json'),'views':{},'native_acceptance':'Not attempted; all-generated gate unchanged'}
assemblies={'red-cut':{},'complete':{}}
before={}
for i,f in enumerate(['south','east','north']):
    body=read(BODY/f'selected-{f}.png')
    target=Image.open(MASK/f'robe-target-{f}.png').convert('L')
    exposure=Image.open(MASK/f'robe-expose-{f}.png').convert('L')
    target_box=target.point(lambda a:255 if a>128 else 0).getbbox()
    required=np.array(Image.open(MASK/f'robe-required-{f}.png').convert('L'))>128
    source=key.crop((512*i,0,512*(i+1),1024))
    before[f]=Image.alpha_composite(body,source)
    record['views'][f]={}
    for name,im in [('red-cut',source),('complete',read(FULL/f'registered-uncut-{f}.png'))]:
        box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox()
        sx=(target_box[2]-target_box[0])/(box[2]-box[0]);sy=(target_box[3]-target_box[1])/(box[3]-box[1])
        tx=target_box[0]-sx*box[0];ty=target_box[1]-sy*box[1]
        inverse=(1/sx,0,-tx/sx,0,1/sy,-ty/sy)
        stretched=im.transform((512,1024),Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC)
        stretched.save(HERE/f'{name}-stretched-{f}.png')
        visible=stretched.copy()
        visible.putalpha(ImageChops.multiply(stretched.getchannel('A'),ImageChops.invert(exposure)))
        visible.save(HERE/f'{name}-visible-{f}.png')
        composed=Image.alpha_composite(body,visible);composed.save(HERE/f'{name}-assembly-{f}.png');assemblies[name][f]=composed
        a=np.array(visible.getchannel('A'));ex=np.array(exposure)>250;ba=np.array(body.getchannel('A'))>250
        record['views'][f][name]={'source_alpha_bounds':list(box),'target_bounds':list(target_box),'scale_x':sx,'scale_y':sy,'translation':[tx,ty],'inverse_affine':list(inverse),'required_covered_pixels_with_alpha_below_128':int(np.count_nonzero(required&(a<128))),'exposed_body_interior_pixels_changed':int(np.count_nonzero(ex&ba&np.any(np.array(body)[:,:,:3]!=np.array(composed)[:,:,:3],axis=2))),'stretched_source':asset(HERE/f'{name}-stretched-{f}.png'),'visible':asset(HERE/f'{name}-visible-{f}.png')}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(name,rows,title):
    out=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(out);d.text((18,12),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(rows.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*288
        out.paste(bg.resize((256,512)).convert('RGB'),(x,48));d.line((x+128,48,x+128,559),fill='#e3cf43');d.line((x,523,x+255,523),fill='#70b8b0');d.text((x,578),f.upper(),font=font,fill='#e3cf43')
    d.text((18,618),'Body unchanged. One whole-image stretch per view; exposure mask controls depth. Art experiment only.',font=font,fill='#e5e8d8');out.save(HERE/name)
for name,ims in assemblies.items():
    plate(name+'-assembly-comparison.png',ims,'WHOLE-IMAGE STRETCH / '+name.upper()+' source; no local reshaping')
plate('profile-technique-comparison.png',{'direct red-cut':before['east'],'stretch red-cut':assemblies['red-cut']['east'],'stretch complete':assemblies['complete']['east'],'previous mesh':read(MASK/'fitted-assembly-east.png')},'PROFILE / same fixed body; translation and scale versus previous local mesh')
small=Image.new('RGB',(800,410),'#142823');d=ImageDraw.Draw(small)
for row,(name,ims) in enumerate(assemblies.items()):
    d.text((15,row*195+12),name.upper()+' / 48 x 96 canvas, then 2x nearest',font=font,fill='#e3cf43')
    for i,im in enumerate(ims.values()):
        t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*240+35,row*195+42),t)
        t=t.resize((72,144),Image.Resampling.NEAREST);small.paste(t,(i*240+102,row*195+35),t)
small.save(HERE/'small-sprite-comparison.png')
record['visual_review']='Pending actual image inspection; rectangle fitting does not prove shoulder/hump coverage or correct neckline/cuff placement.'
(HERE/'result.json').write_bytes((json.dumps(record,indent=2)+'\n').encode())
print(json.dumps(record['views'],indent=2))
