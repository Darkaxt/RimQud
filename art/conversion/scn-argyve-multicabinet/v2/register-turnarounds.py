"""Material-only selection into full fixed geometry and one-alpha color roles."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';OUT=HERE/'registered-final';OUT.mkdir(exist_ok=True)
FACINGS=['south','east','north','west'];SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def material(raw,own,pattern):
    area=own[:,:,3]>0;role=own[:,:,0]>127;gray=np.where(role,raw[:,:,:2].max(2),raw[:,:,:3].mean(2));spread=np.ptp(raw[:,:,:3],axis=2);stats={}
    for name,region,colors in [('metal',area&~role,spread<24),('detail',area&role,(raw[:,:,0]-raw[:,:,2]>15)&(raw[:,:,1]-raw[:,:,2]>15))]:
        if not region.any():stats[name]=dict(selected=0,continued=0,unsampled=0);continue
        known=ndimage.binary_erosion(region,iterations=5)&(raw[:,:,3]>128)&(gray>105)&(gray<245)&colors
        labels,num=ndimage.label(region);unsampled=0
        for k in range(1,num+1):
            comp=labels==k
            if not (known&comp).any():gray[comp]=pattern[:,:,:3].mean(2)[comp];known|=comp;unsampled+=int(comp.sum())
        unknown=region&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(region.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
        for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<768)&(nx>=0)&(nx<512));q=q[region[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
        if n:gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
        stats[name]=dict(selected=int(known.sum())-unsampled,continued=n,unsampled=unsampled)
    ink=pattern[:,:,:3].mean(2);gray[area&(ink<125)]=ink[area&(ink<125)]
    assert np.isfinite(gray[area]).all()
    gray[~area]=0
    return np.uint8(np.clip(np.round(gray),0,255)),stats
assert not (OUT/'model.json').exists(),'Preserve registered evidence'
packet=json.loads((HERE/'source-packet.json').read_text());decisions={};variants=[];groups={name:[] for name in ['neutral','native','detail','coverage']}
for n in [1,2]:
    raw=read(HERE/f'variant-{n}-refined-turnaround-raw.png');actual_raw_size=list(raw.size)
    # Tool output1 is2046px wide despite requested2048. Normalize the complete
    # sheet once for material sampling, never fit individual alpha bounds.
    assert raw.height==768 and abs(raw.width-2048)<=2,raw.size
    if raw.size!=(2048,768):raw=raw.resize((2048,768),Image.Resampling.LANCZOS)
    views={};row={name:{} for name in groups};decisions[str(n)]={}
    for i,f in enumerate(FACINGS):
        folder=OUT/f'variant-{n}'/f;folder.mkdir(parents=True,exist_ok=True);own=np.array(read(HERE/f'variant-{n}-ownership-{f}.png'));pattern=np.array(read(HERE/f'variant-{n}-constructed-{f}.png'))
        if f=='south':
            master=read(HERE/f'variant-{n}-selected-front-neutral.png');primary=read(OLD/f'registered/variant-{n}-primary-neutral.png');stats=dict(retained_original_front=ref(OLD/f'registered/variant-{n}-primary-neutral.png'))
        else:
            sample=np.array(raw.crop((i*512,0,(i+1)*512,768))).astype(float);v,stats=material(sample,own,pattern);master=Image.fromarray(np.dstack([v,v,v,own[:,:,3]]));primary=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA')
        master.save(folder/'neutral-master.png');a=np.array(primary);v=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=v[:,:,None];a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/'primary-neutral.png')
        mapped=Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');weight=np.array(mapped)[:,:,0];coverage=a[:,:,3];weight[coverage==0]=0
        Image.fromarray(coverage).save(folder/'coverage.png');Image.fromarray(weight).save(folder/'detail-weight.png')
        detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weight/255));detail[detail[:,:,3]==0,:3]=0;detail=Image.fromarray(detail);detail.save(folder/'detail-neutral.png');detail.getchannel('A').save(folder/'detail-coverage.png')
        Image.fromarray(np.dstack([weight,weight,weight,coverage])).save(folder/'authored-dualcolor-mask.png')
        ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex(packet['palette']['native_primary_rgb']),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex(packet['palette']['native_detail_rgb']),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*v[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-c-W-preview.png')
        view={key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]}
        view.update(canvas=[256,256],authoring_canvas=[512,768],source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False);views[f]=view
        decisions[str(n)][f]=dict(material=stats,actual_raw_size=actual_raw_size,material_sheet_mapping='Whole generated sheet normalized once to2048x768 for four equal material panels; no independent alpha-bounds fitting. Fixed output geometry unchanged.',coverage='Existing selected alpha for retained south; exact fixed manual geometry for new E/N/W. One shared complete-cell mapping. No generated background/halo or changed seam geometry.',color='Equal-RGB luminance with independent source detail weight; one coverage alpha. No double-alpha overdraw at edges.',repairs='Manual seam/outline ink retained, unsupported tiny edge/bracket regions use explicitly reported constructed shade. Same-material harmonic continuation only, not garment warping.')
        row['neutral'][f]=primary;row['native'][f]=native;row['detail'][f]=detail;row['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
    variant=dict(variant=n,native_tile=f'Items/sw_multi_cabinet_{n}.bmp',views=views)
    variant.update({key:views['south'][key] for key in ['primary','detail','coverage','detail_weight','detail_coverage']});variants.append(variant)
    for group in groups:groups[group].append(row[group])
model=dict(entry='SCN-ARGYVE-MULTICABINET',kind='directional_source_dualcolor_furniture_variants',blueprint='Argyve Multicabinet',source=ref(HERE/'source-packet.json'),variants=variants,registration=packet['frame'],camera=packet['camera'],palette=dict(primary='c',detail='W',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background'),state_owner=packet['states'],inventory_boundary=packet['inventory_boundary'],native_behavior=packet['native_behavior'],west_policy='Explicit end views with front lip on opposite edges; no unexamined mirror assumption.',native_acceptance=packet['native_acceptance'])
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(variants=decisions,new_imagegen_calls=2,retained_actual_v1_front_refinements=2,second_isolation_call=False,structural_reviews=[ref(HERE/f'variant-{n}-structural-review.json') for n in [1,2]],material_patch='Initial transfer in sibling registered averaged gold RGB, darkening the topbox against retained front max(R,G) normalization. Final material uses max(R,G) for gold-owned surfaces, matching original front extraction. Geometry, alpha and body/frame are unchanged; no new ImageGen call.',superseded_material_plate=ref(HERE/'registered/all-layouts-native.png'),native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
for group,rows in groups.items():
    plate=Image.new('RGB',(1440,1160),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),f'MULTICABINET / {group.upper()} / two native layouts, cardinal S/E/N/W; source c/W roles',font=font,fill='#e3cf43')
    for row,ims in enumerate(rows):
        for i,(f,im) in enumerate(ims.items()):
            x=24+i*350;y=60+row*525;bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,384)),(x,y));d.text((x,y+398),f'LAYOUT{row+1} / {f.upper()}',font=font,fill='#e3cf43')
            for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
                thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+20+j*75,y+444),thumb)
    d.text((18,1125),'Shared cell/pivot; original fronts retained. Additional directions unbound. Native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-layouts-{group}.png')
print('Registered both layouts in S/E/N/W with preserved fronts and exact new-view coverage.')
