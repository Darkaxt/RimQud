"""Fixed source chest geometry with neutral wood/latch and independent bands."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1/registered';OUT=HERE/'registered-final';OUT.mkdir(exist_ok=True)
HELPER=HERE/'select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('surface_material',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());raw=read(HERE/'refined-turnaround-raw.png');views={};decisions={};groups={k:{} for k in ['neutral','native','detail','coverage']}
for i,f in enumerate(['south','east','north','west']):
    folder=OUT/f;folder.mkdir(exist_ok=True)
    if f=='west':master=ImageOps.mirror(read(OUT/'east/neutral-master.png'));own=np.array(ImageOps.mirror(read(HERE/'ownership-east.png')));primary=ImageOps.mirror(read(OUT/'east/primary-neutral.png'));stats=dict(rule='Mirror east; symmetric end/band return with no side-specific marks or handle.')
    else:
        own=np.array(read(HERE/f'ownership-{f}.png'))
        if f=='south':master=read(HERE/'selected-front-neutral.png');primary=read(OLD/'primary-neutral.png');stats=dict(retained_exact_front=ref(OLD/'primary-neutral.png'))
        else:
            w,h=raw.size;sample=raw.crop((round(i*w/3),0,round((i+1)*w/3),h));master,stats=helper.select(sample,own,np.array(read(HERE/f'constructed-{f}.png')));stats={'wood_and_hinge':stats['wood'],'reinforcing_band':stats['top']};primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA')
    master.save(folder/'neutral-master.png');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png')
    mapped=Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(mapped)[:,:,0];coverage=a[:,:,3];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
    detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
    ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('cfc041'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-W-preview.png')
    view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
    decisions[f]=dict(material=stats,coverage='Exact selected original front; fixed full closed-wood manual end/rear coverage, mirrored west. No generated silhouette, frame drift or exterior fringe.',color='Wood/latch/hinges remain primary w; source reinforcing bands and authored return only use W. Neutral luminance with independent role weight and one coverage alpha.')
    groups['neutral'][f]=primary;groups['native'][f]=native;groups['detail'][f]=detail;groups['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
model=dict(entry='SCN-CHEST1',kind='directional_source_dualcolor_furniture',blueprint='Chest1',source=ref(HERE/'source-packet.json'),views=views,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='w',detail='W',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),native_state=packet['native_state'],west_policy='Mirror east; symmetric unmarked end.',native_acceptance=packet['native_acceptance']);model.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(views=decisions,shared_material_sampler=ref(HELPER),new_imagegen_calls=1,second_isolation_call=False,front_retained=ref(OLD/'model.json'),shape_interpretation='Shouldered source lid retained as physical contour, not generic tapering perspective. Broad end and hinge/band routing are explicitly authored continuation. No new open/empty/full state.',native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'CHEST1 / {group.upper()} / source shouldered lid, primary latch and bright reinforcing bands',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=16+i*284;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,55));d.text((x,460),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
            thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,505),thumb)
    d.text((18,605),'Same16x24cell/pivot8,16; S retained. One source tile; extra directions unbound. Native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print('Registered retained chest front and complete end/rear, neutral material and independent native band tint.')
