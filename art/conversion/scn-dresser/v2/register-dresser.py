"""Patched parallel cap, retained three-front wood, complete end/rear source masks."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
HELPER=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('wood_material',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());raw=read(HERE/'refined-turnaround-raw.png');views={};decisions={};groups={k:{} for k in ['neutral','native','detail','coverage']}
for i,f in enumerate(['south','east','north','west']):
    folder=OUT/f;folder.mkdir(exist_ok=True)
    if f=='west':master=ImageOps.mirror(read(OUT/'east/neutral-master.png'));own=np.array(ImageOps.mirror(read(HERE/'ownership-east.png')));stats=dict(rule='Mirror east; symmetric unmarked end/cap/feet, no side-specific fittings.')
    else:
        own=np.array(read(HERE/f'ownership-{f}.png'))
        if f=='south':master=read(HERE/'selected-front-neutral-clean.png');stats=dict(retained_body_and_patched_cap=ref(HERE/'cap-material-correction.json'))
        else:
            w,h=raw.size;sample=raw.crop((round(i*w/3),0,round((i+1)*w/3),h));a=np.array(sample);a[:,:,:3]=a[:,:,[2,1,0]];master,stats=helper.select(Image.fromarray(a),own,np.array(read(HERE/f'constructed-{f}.png')));stats={'case':stats['wood'],'cap_and_feet':stats['top']}
    master.save(folder/'neutral-master.png');primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png')
    mapped=Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(mapped)[:,:,0];coverage=a[:,:,3];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
    detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
    # Both native roles are w, but ownership is preserved independently.
    ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8);colors=fg[None,None,:]*(1-ratio[:,:,None])+fg[None,None,:]*ratio[:,:,None];rgb=np.uint8(np.round(colors*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-w-preview.png')
    view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
    decisions[f]=dict(material=stats,coverage='Patched parallel-cap S with retained lower body/feet, exact authored E/N geometry and symmetric mirrored W. Generated cap/frame drift and fringe excluded.',color='Independent cap/feet role and main case/fronts both receive native w. No visible gold/brass or baked cyan. Neutral luminance with one coverage alpha and separate role weight.')
    groups['neutral'][f]=primary;groups['native'][f]=native;groups['detail'][f]=detail;groups['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
model=dict(entry='SCN-DRESSER',kind='directional_source_dualcolor_furniture',blueprint='Dresser',source=ref(HERE/'source-packet.json'),views=views,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='w',detail='w',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),native_state=packet['native_state'],west_policy='Mirror east; symmetric unmarked closed end.',native_acceptance=packet['native_acceptance']);model.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(views=decisions,shared_material_sampler=ref(HELPER),channel_mapping='Temporary raw R/B swap maps cyan role to existing gold-role sampler; max(R,G) becomes original max(B,G), neutral wood mean/spread unchanged. Production output is grayscale.',new_imagegen_calls=1,second_isolation_call=False,cap_geometry_correction=ref(HERE/'cap-geometry-correction.json'),cap_edge_correction=ref(HERE/'cap-edge-correction.json'),cap_material_correction=ref(HERE/'cap-material-correction.json'),native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'DRESSER / {group.upper()} / three source fronts, parallel cap and complete end/back; native w/w',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=16+i*284;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,55));d.text((x,460),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
            thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,505),thumb)
    d.text((18,605),'Same16x24cell/pivot8,16. Internal brass not visible gold. One source tile; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print('Registered source dresser with parallel cap, retained fronts, complete end/back and independent w/w masks.')
