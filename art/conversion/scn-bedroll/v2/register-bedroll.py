"""Refined material in rigid source geometry; explicit west and dual-color roles."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
# Reuse the already recorded same-material768-square sampler, with bedroll
# role names mapped explicitly. It changes material only, not garment geometry.
HELPER=ROOT/'art/conversion/scn-bed/v2/select-material.py'
spec=importlib.util.spec_from_file_location('material_sampling',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());raw=read(HERE/'refined-turnaround-raw.png');views={};decisions={};groups={k:{} for k in ['neutral','native','detail','coverage']}
for i,f in enumerate(['south','east','north','west']):
    folder=OUT/f;folder.mkdir(exist_ok=True);own=np.array(read(HERE/f'ownership-{f}.png'));pattern=np.array(read(HERE/f'selected-{f}-neutral.png'))
    if f!='west':
        w,h=raw.size;sample=raw.crop((round(i*w/3),0,round((i+1)*w/3),h));master,stats=helper.select(sample,own,pattern);stats['material']={'main_wool_and_ties':stats['material']['wood'],'folded_end':stats['material']['fabric']}
    else:
        # Exact+90degree pose from the common object center12,13. No mirror.
        south=read(OUT/'south/neutral-master.png');sample=south.convert('RGBa').transform((768,768),Image.Transform.AFFINE,(0,1,-32,-1,0,800),Image.Resampling.BICUBIC).convert('RGBA');sa=np.array(sample);v=sa[:,:,0].copy();missing=(own[:,:,3]>0)&(sa[:,:,3]==0);v[missing]=pattern[:,:,0][missing];v[own[:,:,3]==0]=0;master=Image.fromarray(np.dstack([v,v,v,own[:,:,3]]));stats=dict(source=ref(OUT/'south/neutral-master.png'),rule='Rotate selected south material+90degrees about common384,416center, then retain exact explicit-west geometry alpha; no reflection.',retained_original_edge_pixels=int(missing.sum()))
    master.save(folder/'neutral-master.png');primary=master.convert('RGBa').resize((384,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png')
    mapped=Image.fromarray(own).convert('RGBa').resize((384,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(mapped)[:,:,0];coverage=a[:,:,3];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
    detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
    ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('b1c9c3'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-y-preview.png')
    view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[384,256],authoring_canvas=[768,768],source_cell=[16,24],authoring_extent=[24,24],source_cell_offset=[4,0],authored_anchor=[12,16],object_rotation_center=[12,13],native_bound_proposal=f=='south',native_activation=False,mirror=False);views[f]=view
    decisions[f]=dict(material=stats,coverage='Rigidly reoriented full selected-source alpha/ownership. No generated silhouette, changed fold/strap boundaries or exterior fringe.',color='Main wool/canvas w and folded-end y remain independent. Equal-RGB production material, one alpha with independent detail weight; no baked cyan.')
    groups['neutral'][f]=primary;groups['native'][f]=native;groups['detail'][f]=detail;groups['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
model=dict(entry='SCN-BEDROLL',kind='directional_source_dualcolor_furniture',blueprint='Bedroll',source=ref(HERE/'source-packet.json'),views=views,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='w',detail='y',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),native_state=packet['native_state'],west_policy='Explicit rotated west preserves tie/fold asymmetry; no blind mirror.',native_acceptance=packet['native_acceptance']);model.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(views=decisions,shared_material_sampler=ref(HELPER),new_imagegen_calls=1,retained_front_generation=ref(HERE.parent/'v1/refined-proposal.png'),second_isolation_call=False,correction='Whole selected source is rigidly reoriented before one composed material refinement. Soft irregular fold/tie contours remain intrinsic; there is no shear, local mesh, finished-view width stretch or independent bounds fit.',native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1560,700),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'GOAT-WOOL BEDROLL / {group.upper()} / rigid cardinal orientations, source w/y roles',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=20+i*385;bg=Image.new('RGBA',(384,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((360,360)),(x,65));d.text((x,445),f.upper()+' / ROTATED',font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(24,24),(36,36),(48,48)]):
            thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+30+j*100,500),thumb)
    for i,line in enumerate(['One source design and common24x24extent around original16x24cell; no per-facing silhouette deformation.',
     'Fold/ties remain source-bound. West is explicitly rotated, not mirrored. Native takeable/non-solid sleep state unchanged.',
     'Extra directions and expanded frame are unbound authoring; native acceptance waits for full-set generation.']):d.text((18,595+i*30),line,font=font,fill='#e5e8d8')
    plate.save(OUT/f'all-views-{group}.png')
print('Registered cardinal bedroll material, exact rigid coverage and separate native wool/fold roles.')
