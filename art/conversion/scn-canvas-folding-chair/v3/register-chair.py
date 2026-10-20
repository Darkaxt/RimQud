"""Retain exact selected front; register complete side/rear sling material."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2/registered-corrected';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
HELPER=ROOT/'art/conversion/scn-book-table/v2/select-material.py';spec=importlib.util.spec_from_file_location('surface_sampling',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());raw=read(HERE/'refined-turnaround-raw.png');views={};decisions={};groups={k:{} for k in ['neutral','native','detail','coverage']}
for i,f in enumerate(['south','east','north','west']):
    folder=OUT/f;folder.mkdir(exist_ok=True)
    if f=='west':master=ImageOps.mirror(read(OUT/'east/neutral-master.png'));own=np.array(ImageOps.mirror(read(HERE/'ownership-east.png')));primary=ImageOps.mirror(read(OUT/'east/primary-neutral.png'));stats=dict(rule='Mirror east; no asymmetric markings, source fittings or side-specific cloth design.')
    else:
        own=np.array(read(HERE/f'ownership-{f}.png'))
        if f=='south':master=read(HERE/'selected-front-neutral.png');primary=read(OLD/'primary-neutral.png');stats=dict(retained_exact_front=ref(OLD/'primary-neutral.png'))
        else:
            w,h=raw.size;sample=raw.crop((round(i*w/3),0,round((i+1)*w/3),h));a=np.array(sample);a[:,:,:3]=a[:,:,[2,1,0]]
            # The existing surface sampler classifies gold role. Swapping R/B
            # maps cyan to that role exactly: max(R,G) becomes original max(B,G),
            # while neutral-wood mean and spread are invariant. Output is gray.
            master,stats=helper.select(Image.fromarray(a),own,np.array(read(HERE/f'constructed-{f}.png')));stats={'wood':stats['wood'],'knit_sling':stats['top']};primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA')
    master.save(folder/'neutral-master.png');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png')
    mapped=Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(mapped)[:,:,0];coverage=a[:,:,3];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
    detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
    ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('b1c9c3'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-y-preview.png')
    view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
    decisions[f]=dict(material=stats,coverage='Exact existing corrected south pixels/alpha; fixed manual side/rear geometry and derived mirrored west. Generated changed rod thickness, bounds and fringe excluded.',color='Neutral wood w and knit sling y, independent source role weight with one coverage alpha; no double-opacity cloth overdraw or baked cyan.')
    groups['neutral'][f]=primary;groups['native'][f]=native;groups['detail'][f]=detail;groups['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
model=dict(entry='SCN-CANVAS-FOLDING-CHAIR',kind='directional_source_dualcolor_furniture',blueprint='Canvas Folding Chair',source=ref(HERE/'source-packet.json'),views=views,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='w',detail='y',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),native_state=packet['native_state'],west_policy='Mirror east; symmetric unmarked side geometry.',native_acceptance=packet['native_acceptance']);model.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(views=decisions,shared_material_sampler=ref(HELPER),channel_mapping='Temporary R/B permutation of raw cyan-role material for existing gold-role sampler. Neutral gray output, original owner/coverage unchanged. This is sampling normalization, not production hue.',new_imagegen_calls=1,retained_front_generation=ref(HERE.parent/'v2/refined-front.png'),second_isolation_call=False,native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'CANVAS FOLDING CHAIR / {group.upper()} / source jointed wood and knit sling in cardinal views',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=16+i*284;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,55));d.text((x,460),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
            thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,505),thumb)
    d.text((18,605),'Same16x24cell/pivot8,16; S retained. One deployed source state; extra views unbound. Native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print('Registered retained front and complete side/back sling chair, with fixed coverage and separate source tint.')
