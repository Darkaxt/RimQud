"""Register two open-lattice states/four facings, neutral fiber and native tile roles."""
from pathlib import Path
import importlib.util,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
HELPER=ROOT/'art/conversion/scn-book-table/v2/select-material.py';spec=importlib.util.spec_from_file_location('surface_sampling',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());states=[];decisions=[];images={key:[] for key in ['native','neutral','detail','coverage']}
def rectify(raw,owner):
    a=np.array(raw).astype(float);gray=a[:,:,:3].mean(2);spread=np.ptp(a[:,:,:3],axis=2);cyan=(a[:,:,1]-a[:,:,0]>12)&(a[:,:,2]-a[:,:,0]>12)
    accepted=(a[:,:,3]>=240)&(gray>120)&(gray<252)&((spread<35)|cyan)
    yy,xx=np.where(accepted);assert len(xx)>30;src=[float(xx.min()),float(yy.min()),float(xx.max()+1),float(yy.max()+1)]
    o=np.array(owner);yy,xx=np.where(o[:,:,3]>128);dst=[float(xx.min()),float(yy.min()),float(xx.max()+1),float(yy.max()+1)]
    sx=(src[2]-src[0])/(dst[2]-dst[0]);sy=(src[3]-src[1])/(dst[3]-dst[1]);tx=src[0]-sx*dst[0];ty=src[1]-sy*dst[1]
    mapped=raw.transform((512,768),Image.Transform.AFFINE,(sx,0,tx,0,sy,ty),Image.Resampling.BICUBIC)
    return mapped,dict(inverse_material_sampling_affine=[sx,0,tx,0,sy,ty],generated_opaque_fiber_extent=src,fixed_constructed_frame_extent=dst,scope='Generated fiber RGB sampling coordinates only; reject colored/transparent exterior before range detection. No production crop/bounds fitting: output alpha, contours, camera, scale, role and pivot are exact source construction.')
for state,tile in [('unhung','Items/sw_shawl.bmp'),('hanging','Items/sw_hammock.bmp')]:
    source=HERE/state;raw=read(source/'refined-turnaround-raw.png');jr=json.loads((source/'first-structural-review.json').read_text());assert jr['status']=='PASS FOR ROPE MATERIAL ONLY';views={};sampling={};row={key:{} for key in images}
    for i,f in enumerate(['south','east','north','west']):
        suffix='-patched' if state=='unhung' else '';own=read(source/f'ownership-{f}{suffix}.png');pattern=read(source/f'constructed-{f}{suffix}.png');w,h=raw.size
        index=i if i<3 else 1;panel=raw.crop((round(index*w/3),0,round((index+1)*w/3),h));panel=ImageOps.mirror(panel) if f=='west' else panel;mapped,landmarks=rectify(panel,own)
        folder=OUT/state/f;folder.mkdir(parents=True,exist_ok=True);mapped.save(folder/'mapped-material-source.png');sample=np.array(mapped);sample[:,:,:3]=sample[:,:,[2,1,0]]
        master,stats=helper.select(Image.fromarray(sample),np.array(own),np.array(pattern));master.save(folder/'neutral-master.png')
        primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png');coverage=a[:,:,3]
        role=own.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(role)[:,:,0];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png')
        detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
        ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('b1c9c3'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('ffffff'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-y-Y-preview.png')
        view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
        sampling[f]=dict(material_rectification=landmarks,rope=stats['wood'],bright_strands=stats['top'],west_material='Reused reflected homogeneous east fiber only; actual west geometry/role painted from270-degree model, no mirrored sling geometry or fourth ImageGen call.' if f=='west' else 'Actual generated same-state facing.',coverage='Exact editable ropes and open holes; generated backdrop/fill/fringe/geometry excluded. Same-material harmonic continuation; constructed ink retained. Tiny disconnected fiber components lacking samples are counted as constructed shading.');row['neutral'][f]=primary;row['native'][f]=native;row['detail'][f]=detail;row['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
    item=dict(state=state,native_tile=tile,views=views);item.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});states.append(item);decisions.append(dict(state=state,views=sampling))
    for key in images:images[key].append(row[key])
model=dict(entry='SCN-HAMMOCK',kind='directional_source_dualcolor_furniture_states',blueprint='Hammock',source=ref(HERE/'source-packet.json'),states=states,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='Explicit TileColor y',detail='Y',glyph_only_ColorString='Y',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),state_owner=packet['native_state'],native_behavior='Native Hangable owns support, Entered/LeftCell and zone lifecycle; Bed,2-weight organic/takeable/non-solid and HP5 retained. No trees/frame/occupant/fishing mechanics. Extra views unbound.',west_policy='Independently projected270-degree state surface and role; east homogeneous fiber reuse only.',native_acceptance=packet['native_acceptance'])
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(states=decisions,material_sampler=ref(HELPER),channel_mapping='Temporary R/B permutation maps cyan owner material to existing gold classifier; output equal-RGB and original owner alpha untouched.',new_imagegen_calls=2,second_isolation_call=False,old_preview_correction='V1 preview alpha-composited detail over primary and changed opacity at rope edges. This version uses independent role weight and exactly one coverage alpha; no extra coverage from white strands.',native_acceptance=packet['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,rows in images.items():
    plate=Image.new('RGB',(1152,1190),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'HAMMOCK / {group.upper()} / two native states, each with shared-model cardinal directions',font=font,fill='#e3cf43')
    for n,row in enumerate(rows):
        y=50+n*530
        for i,(f,im) in enumerate(row.items()):
            x=16+i*284;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,y));d.text((x,y+405),('UNHUNG' if n==0 else 'HANGING')+' / '+f.upper(),font=font,fill='#e3cf43')
            for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
                thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,y+440),thumb)
    d.text((18,1140),'Open lattice, same full source cell/pivot, TileColor y / Y. Extra facings unbound; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print('Registered both native states and all four cardinal facings, exact open lattice and single-coverage y/Y roles.')
