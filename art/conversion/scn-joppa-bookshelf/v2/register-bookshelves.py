"""Retain patched fronts; register dark wood and whole-book roles for all directions."""
from pathlib import Path
import sys,importlib.util,json,re
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
HELPER=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('surface_sampling',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);ref,read,write=helper.ref,helper.read,helper.write
assert not (OUT/'model.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());variants=[];decisions=[];images={key:[] for key in ['neutral','stocked','empty','detail','coverage']};profile=[]
def panels(raw):
    a=np.array(raw).astype(float);gray=a[:,:,:3].mean(2);spread=np.ptp(a[:,:,:3],axis=2);accepted=(a[:,:,3]>240)&(gray>85)&(spread<45);labels,num=ndimage.label(accepted.sum(0)>8);runs=[]
    for k in range(1,num+1):
        xx=np.where(labels==k)[0];runs.append((int(xx.min()),int(xx.max()+1)))
    runs=sorted(sorted(runs,key=lambda r:r[1]-r[0],reverse=True)[:3]);assert len(runs)==3
    info={}
    for f,(lo,hi) in zip(['south','east','north'],runs):
        q=gray[:,lo:hi][accepted[:,lo:hi]];ys,xs=np.where(accepted[:,lo:hi]);info[f]=dict(bounds=[lo,int(ys.min()),hi,int(ys.max()+1)],wood_luminance_quantiles=np.quantile(q,[.05,.25,.5,.75,.95]).tolist())
    return info
def map_material(raw,bounds,owner):
    a=np.array(owner);yy,xx=np.where(a[:,:,3]>128);dst=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];sx=(bounds[2]-bounds[0])/(dst[2]-dst[0]);sy=(bounds[3]-bounds[1])/(dst[3]-dst[1]);tx=bounds[0]-sx*dst[0];ty=bounds[1]-sy*dst[1];mapped=raw.transform((512,768),Image.Transform.AFFINE,(sx,0,tx,0,sy,ty),Image.Resampling.BICUBIC)
    return mapped,dict(source_material_bounds=bounds,constructed_reference_bounds=dst,inverse_RGB_sampling_affine=[sx,0,tx,0,sy,ty],scope='Material coordinates only. Generated figures are not evenly spaced. Production alpha/geometry/scale/pivot and role boundaries remain fixed construction; no output bounds fit.')
def ownership(folder,f,pattern):
    if f=='south':return read(folder/'ownership-south.png'),dict(rule='Retained actual whole-spine ownership from selected front, combined with corrected cap alpha; original lower front/book material unchanged.')
    svg=(folder/f'ownership-{f}.svg').read_text();svg=re.sub(r'fill="(#[0-9a-fA-F]{6})" stroke="none" stroke-width="0"',lambda m:f'fill="{m.group(1)}" stroke="{m.group(1)}" stroke-width="0.12"',svg);im=Image.open(__import__('io').BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA');a=np.array(im);a[:,:,3]=np.array(pattern)[:,:,3];a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a),dict(rule='Whole book shape including0.12outline is detail-owned; wood outlines primary. Role painting is independent from physical coverage, which is copied exactly from actual corrected construction. No background layer or book/wood alpha subtraction.')
for n in range(1,4):
    source=HERE/f'variant-{n}';raw=read(source/'refined-turnaround-raw.png');review=json.loads((source/'first-structural-review.json').read_text());assert review['status']=='PASS FOR MATERIAL SELECTION';panel_info=panels(raw);profile.append(dict(variant=n,panels=panel_info));views={};sampling={};row={key:{} for key in images}
    for f in ['south','east','north','west']:
        folder=OUT/f'variant-{n}'/f;folder.mkdir(parents=True,exist_ok=True)
        if f=='west':
            master=ImageOps.mirror(read(OUT/f'variant-{n}/east/neutral-master.png'));own=ImageOps.mirror(read(OUT/f'variant-{n}/east/fixed-ownership-master.png'));stats=dict(rule='Mirror closed unmarked east end; no asymmetric side fittings or visible book faces.');role_review=dict(rule='Mirror complete east role/alpha with material.')
        else:
            pattern=read(source/(f'constructed-{f}.png' if f!='north' else 'constructed-north-patched.png'))
            own,role_review=ownership(source,f,pattern)
            if f=='south':master=read(source/'selected-front-neutral.png');stats=dict(rule='Retained selected patched front; generated south redraw is historical composed context, not replacement material.')
            else:
                mapped,mapping=map_material(raw,panel_info[f]['bounds'],own);mapped.save(folder/'mapped-material-source.png');master,values=helper.select(mapped,np.array(own),np.array(pattern));stats=dict(mapping=mapping,wood=values['wood'],book_surfaces=values['top'])
        own.save(folder/'fixed-ownership-master.png');master.save(folder/'neutral-master.png');primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png');coverage=a[:,:,3]
        role=own.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(role)[:,:,0];weight[coverage==0]=0;Image.fromarray(weight).save(folder/'detail-weight.png');Image.fromarray(coverage).save(folder/'coverage.png');detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png');Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
        previews={};ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8)
        for state,hexcode in [('stocked','cfc041'),('empty','0f3b3a')]:
            dc=np.frombuffer(bytes.fromhex(hexcode),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;im=Image.fromarray(np.dstack([rgb,coverage]));im.save(folder/(state+'-native-preview.png'));previews[state]=im
        view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
        sampling[f]=dict(material=stats,ownership=role_review,coverage='Single full physical alpha and independent book weight. Identical production bytes for stocked/empty: only detail color changes. Generated fringe/geometry/additional nails/marks excluded; no second isolation.');row['neutral'][f]=primary;row['stocked'][f]=previews['stocked'];row['empty'][f]=previews['empty'];row['detail'][f]=detail;row['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
    item=dict(variant=n,native_tile=f'Items/sw_bookshelf{n}.bmp',views=views);item.update({k:views['south'][k] for k in ['primary','detail','coverage','detail_weight','detail_coverage']});variants.append(item);decisions.append(dict(variant=n,views=sampling))
    for key in images:images[key].append(row[key])
model=dict(entry='SCN-JOPPA-BOOKSHELF',kind='inventory_tinted_directional_furniture_variants',blueprint='Joppa Bookshelf',source=ref(HERE/'source-packet.json'),variants=variants,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='w',stocked_detail='W',empty_detail='k',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),state_owner=packet['native_state'],native_behavior=packet['native_behavior'],west_policy='Mirror plain closed east end, no side-specific fittings/book detail visible.',native_acceptance=packet['native_acceptance'])
write(OUT/'model.json',model);write(HERE/'material-selection-basis.json',dict(source_profiles=profile,selection='Inspected generated E wood median122..129, N121..133: bright wood cutoff150would discard most grain. Reuse existing105wood/150gold sampler with exact fixed construction ink and same-material continuation.',helper=ref(HELPER)));write(OUT/'registration-decisions.json',dict(variants=decisions,material_sampler=ref(HELPER),selection_basis=ref(HERE/'material-selection-basis.json'),new_imagegen_calls=3,second_isolation_call=False,preview_correction='V1 alpha-composited detail over primary. Current previews apply one coverage alpha plus independent whole-book weight; full/empty never changes geometry or populates actual items.',native_acceptance=packet['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,rows in images.items():
    plate=Image.new('RGB',(1152,1840),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'JOPPA BOOKSHELF / {group.upper()} / three source layouts, complete cardinal wood and book roles',font=font,fill='#e3cf43')
    for n,row in enumerate(rows,1):
        y=50+(n-1)*560
        for i,(f,im) in enumerate(row.items()):
            x=16+i*284;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,y));d.text((x,y+405),f'LAYOUT{n} / {f.upper()}',font=font,fill='#e3cf43')
            for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
                thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,y+450),thumb)
    d.text((18,1770),'Same full cell/pivot; source w frame, full W / empty k books. No book removal or inventory identity implied.',font=font,fill='#e5e8d8');d.text((18,1800),'Additional directions unbound; native mounted inventory/support/visibility acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print('Registered all3source layouts in S/E/N/W, retained patched fronts and exact single-alpha full/empty book tint.')
