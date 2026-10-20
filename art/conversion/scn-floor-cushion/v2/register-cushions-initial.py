"""Sample cloth into fixed cardinal geometry; keep one coverage and color weight."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
HELPER=ROOT/'art/conversion/scn-book-table/v2/select-material.py';spec=importlib.util.spec_from_file_location('surface_sampling',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());variants=[];decisions=[];images={key:[] for key in ['native','neutral','detail','coverage']}
def locate(im,owner=False):
    a=np.array(im).astype(float);h,w=a.shape[:2];cy=(a[:,:,0]>127)&(a[:,:,3]>128) if owner else (a[:,:,1]-a[:,:,0]>12)&(a[:,:,2]-a[:,:,0]>12)&(a[:,:,3]>240)
    yy,xx=np.where(cy);assert len(yy)>0,'No actual binding material landmark'
    seam=float(np.median(yy));center=w//2;ys=np.where(a[:,center,3]>240)[0];assert len(ys)>0
    top=float(ys[0]);mid=int(round((top+seam)/2));xs=np.where(a[mid,:,3]>240)[0];assert len(xs)>0
    return dict(top=top,binding_center=seam,left=float(xs[0]),right=float(xs[-1]),width=w,height=h)
def material_map(raw,owner):
    src=locate(raw);dst=locate(owner,True)
    sx=(src['right']-src['left'])/(dst['right']-dst['left']);sy=(src['binding_center']-src['top'])/(dst['binding_center']-dst['top']);tx=src['left']-sx*dst['left'];ty=src['top']-sy*dst['top']
    mapped=raw.transform((512,768),Image.Transform.AFFINE,(sx,0,tx,0,sy,ty),Image.Resampling.BICUBIC)
    return mapped,dict(raw_landmarks=src,constructed_landmarks=dst,inverse_material_affine=[sx,0,tx,0,sy,ty],scope='Only generated RGB sampling coordinates change. Output coverage, physical scale, camera, pivot, pattern ink and role masks remain exact construction; no production bounds fitting.')
for n in range(1,5):
    source=HERE/f'variant-{n}';raw=read(source/'refined-turnaround-raw.png');review=json.loads((source/'first-structural-review.json').read_text());assert review['status']=='PASS FOR MATERIAL SELECTION';views={};sampling={};mapped_views={};row={key:{} for key in images}
    for i,f in enumerate(['south','east','north','west']):
        own=read(source/f'ownership-{f}.png');pattern=read(source/f'constructed-{f}.png')
        if f=='west':
            mapped=ImageOps.mirror(mapped_views['east']);landmarks=dict(scope='Reflected east RGB surface only; west contour, tufts/folds and role are independently rendered from270-degree physical coordinates. No fourth AI generation claimed.')
        else:
            w,h=raw.size;panel=raw.crop((round(i*w/3),0,round((i+1)*w/3),h));mapped,landmarks=material_map(panel,own);mapped_views[f]=mapped
        folder=OUT/f'variant-{n}'/f;folder.mkdir(parents=True,exist_ok=True);mapped.save(folder/'mapped-material-source.png');sample=np.array(mapped);sample[:,:,:3]=sample[:,:,[2,1,0]]
        # Existing sampler's gold classifier becomes cyan under temporary R/B permutation.
        master,stats=helper.select(Image.fromarray(sample),np.array(own),np.array(pattern));master.save(folder/'neutral-master.png')
        primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png');coverage=a[:,:,3]
        role=own.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(role)[:,:,0];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
        detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
        ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('b1c9c3'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-y-preview.png')
        view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
        sampling[f]=dict(material_landmarks=landmarks,cloth=stats['wood'],binding=stats['top'],coverage='Exact constructed silhouette and opaque tufts/folds, no generated frame/shape/fringe or cyan baked into production. Same-material harmonic continuation and fixed dark ink.');row['neutral'][f]=primary;row['native'][f]=native;row['detail'][f]=detail;row['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
    variant=dict(variant=n,native_tile=f'Items/sw_cushion{n}.bmp',views=views);variant.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});variants.append(variant);decisions.append(dict(variant=n,views=sampling))
    for key in images:images[key].append(row[key])
model=dict(entry='SCN-FLOOR-CUSHION',kind='directional_source_dualcolor_furniture_variants',blueprint='Floor Cushion',source=ref(HERE/'source-packet.json'),variants=variants,default_tile_binding=dict(native_tile='Items/sw_floor_cushion.png',variant=1,reason='Captured default and RandomTile variant1 have identical alpha and shader-relevant R at covered pixels; invisible RGB differs.'),registration=packet['frame'],camera=packet['camera'],palette=dict(primary='w',detail='y',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),native_behavior=packet['native_behavior'],west_policy='Authored270-degree pattern rotation, not a geometry/feature mirror; reflected east material only.',native_acceptance=packet['native_acceptance'])
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(variants=decisions,material_sampler=ref(HELPER),new_imagegen_calls=4,second_isolation_call=False,channel_mapping='Temporary R/B permutation for existing gold-role material classifier. Gray production, original ownership/coverage unchanged.',native_acceptance=packet['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,rows in images.items():
    plate=Image.new('RGB',(1152,1810),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'FLOOR CUSHION / {group.upper()} / four actual cosmetic patterns, each with cardinal directions',font=font,fill='#e3cf43')
    for n,row in enumerate(rows,1):
        y=50+(n-1)*420
        for i,(f,im) in enumerate(row.items()):
            x=16+i*284;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,y));d.text((x,y+335),f'PATTERN{n} / {f.upper()}',font=font,fill='#e3cf43')
            for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
                thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,y+350),thumb)
    d.text((18,1760),'Same source cell/pivot; gray fabric w + lower binding y. Extra views unbound; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print('Registered all four cosmetic patterns in S/E/N/W with fixed constructed geometry, neutral material and independent lower binding.')
