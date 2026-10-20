"""Source-bound bed material with fixed cardinal geometry and expanded frame."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('bed_material',HERE/'select-material.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());raw=read(HERE/'refined-turnaround-raw.png');views={};decisions={};groups={k:{} for k in ['neutral','native','detail','coverage']}
for index,f in enumerate(['south','east','north','west']):
    folder=OUT/f;folder.mkdir(exist_ok=True)
    if f=='west':
        master=ImageOps.mirror(read(OUT/'east/neutral-master.png'));own=np.array(ImageOps.mirror(read(HERE/'ownership-east.png')));stats=dict(rule='Mirror east, symmetric bed structure with no asymmetric markings; common physical pivot retained.')
    else:
        own=np.array(read(HERE/f'ownership-{f}.png'))
        if f=='south':master=read(HERE/'selected-front-neutral.png');stats=dict(selection=ref(HERE/'front-material-selection.json'))
        else:
            w,h=raw.size;sample=raw.crop((round(index*w/3),0,round((index+1)*w/3),h));master,stats=helper.select(sample,own,np.array(read(HERE/f'constructed-{f}.png')))
    master.save(folder/'neutral-master.png');primary=master.convert('RGBa').resize((384,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png')
    mapped=Image.fromarray(own).convert('RGBa').resize((384,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(mapped)[:,:,0];coverage=a[:,:,3];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
    detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
    ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('ffffff'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-Y-preview.png')
    view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[384,256],authoring_canvas=[768,768],source_cell=[16,24],authoring_extent=[24,24],source_cell_offset=[4,0],authored_anchor=[12,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
    decisions[f]=dict(material=stats,coverage='Exact shared spatial construction alpha; original open headboard and leg gaps. Expanded frame mapping explicit, no per-facing geometry normalization.',color='One coverage alpha and independent wood/fabric weight; no baked cyan and no double-alpha material overdraw.')
    groups['neutral'][f]=primary;groups['native'][f]=native;groups['detail'][f]=detail;groups['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
model=dict(entry='SCN-BED',kind='directional_source_dualcolor_furniture',blueprint='Bed',source=ref(HERE/'source-packet.json'),views=views,registration=packet['registration'],camera=packet['camera'],palette=dict(primary='w',detail='Y',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),native_state=packet['native_state'],west_policy='Mirror east; symmetric construction, no asymmetric markings.',native_acceptance=packet['native_acceptance'])
model.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(views=decisions,new_imagegen_calls=2,second_isolation_call=False,manual_geometry='Fixed shared3D bed and cardinal map projection. Material-only sampling corrects raw size and compressed east pad without changing accepted geometry.',native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1560,700),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'HILLFOLK BED / {group.upper()} / cardinal map camera, fixed source-shaped wood + stuffed fabric',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=20+i*385;bg=Image.new('RGBA',(384,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((360,360)),(x,65));d.text((x,445),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(24,24),(36,36),(48,48)]):
            thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+30+j*100,500),thumb)
    for i,line in enumerate(['Same24x24 extent, original16x24 cell offset4x; recipient384x256. No per-facing bbox scaling.',
     'Actual source wood w / fabric Y. One fixed source tile; sleep/occupant/animated fallback remain native.',
     'Extra directions and expanded physical-frame mapping await native acceptance after the full generation set.']):d.text((18,595+i*30),line,font=font,fill='#e5e8d8')
    plate.save(OUT/f'all-views-{group}.png')
print('Registered cardinal bed views, source palette/coverage and explicit common expanded frame.')
