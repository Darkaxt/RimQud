"""Register source-controlled wood/glass coverage for all authored cardinal views."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';SIZE=(512,768)
assert not (OUT/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def material(raw,mask,pattern):
    envelope=mask[:,:,3]>0;glass=envelope&(mask[:,:,0]>32);gray=raw[:,:,:3].mean(2);neutral=np.ptp(raw[:,:,:3],axis=2)<20;cyan=(raw[:,:,1]-raw[:,:,0]>5)&(raw[:,:,2]-raw[:,:,0]>5);stats={}
    for name,area,colors in [('wood',envelope&~glass,neutral),('glass',glass,cyan|(neutral&(raw[:,:,:3].min(2)>180)))]:
        known=ndimage.binary_erosion(area,iterations=1)&colors&(raw[:,:,3]>96)&(gray>115)&(gray<245)
        labels,nlabels=ndimage.label(area);unsupported=0
        for lab in range(1,nlabels+1):
            component=labels==lab
            if not (known&component).any():gray[component]=pattern[:,:,:3].mean(2)[component];known|=component;unsupported+=int(component.sum())
        unknown=area&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(area.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
        for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<768)&(nx>=0)&(nx<512));q=q[area[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
        if n:gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
        assert np.isfinite(gray[area]).all();stats[name]=dict(selected_interior=int(known.sum())-unsupported,continued=int(unknown.sum()),tiny_unsampled_geometry_pixels=unsupported)
    return gray,stats
packet=json.loads((HERE/'source-packet.json').read_text());raw=read(HERE/'refined-turnaround-raw.png');views={};decisions={};groups={k:{} for k in ['neutral','native','detail','coverage']}
model=dict(entry='SCN-ALCHEMIST-TABLE',kind='directional_source_dualcolor_furniture',blueprint='Alchemist Table',native_tiles=['Items/sw_alchemist_table.bmp'],source=ref(HERE/'source-packet.json'),views={},registration=packet['frame'],palette=dict(primary='w',detail='C',formula='coverage * luminance * ((1-detail_weight)*foreground + detail_weight*detail) + (1-coverage)*background',translucency='Use one coverage and independent detail weight. Isolated detail-alpha plates are inspection derivatives, not a second opaque pass that adds opacity to glass.'),state_owner=packet['states'],fixture_boundary=packet['inventory_boundary'],native_behavior=packet['native_behavior'],west_policy='Explicit authored west; asymmetric apparatus is not blindly mirrored.',native_acceptance=packet['native_acceptance'])
for index,f in enumerate(['south','east','north','west']):
    folder=OUT/f;folder.mkdir(exist_ok=True);mask=np.array(read(HERE/f'ownership-{f}.png'));pattern=np.array(read(HERE/f'constructed-{f}.png'));envelope=mask[:,:,3]>0
    if f=='south':gray=np.array(read(HERE/'front-clean/selected-front-neutral.png'))[:,:,0].astype(float);stats=dict(shared_front_selection=ref(HERE/'front-clean/material-correction.json'))
    else:
        w,h=raw.size;sample=np.array(raw.crop((round(index*w/4),0,round((index+1)*w/4),h)).resize(SIZE,Image.Resampling.LANCZOS)).astype(float);gray,stats=material(sample,mask,pattern)
    ink=pattern[:,:,:3].mean(2);gray[envelope&(ink<120)]=ink[envelope&(ink<120)];v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0
    master=Image.fromarray(np.dstack([v,v,v,mask[:,:,3]]));master.save(folder/'neutral-master.png');read(HERE/f'ownership-{f}.png').save(folder/'ownership-master.png')
    neutral=master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(neutral);level=np.uint8(np.round(a[:,:,:3].mean(2)));a[:,:,:3]=level[:,:,None];a[a[:,:,3]==0,:3]=0;neutral=Image.fromarray(a);neutral.save(folder/'primary-neutral.png')
    own=Image.fromarray(mask).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');m=np.array(own);coverage=a[:,:,3];weights=m[:,:,0];weights[coverage==0]=0;Image.fromarray(coverage).save(folder/'coverage.png');Image.fromarray(weights).save(folder/'detail-weight.png')
    detail=a.copy();detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*weights/255));detail[detail[:,:,3]==0,:3]=0;detail_im=Image.fromarray(detail);detail_im.save(folder/'detail-neutral.png');Image.fromarray(detail[:,:,3]).save(folder/'detail-coverage.png')
    role=np.repeat(weights[:,:,None],3,axis=2);Image.fromarray(np.dstack([role,coverage])).save(folder/'authored-dualcolor-mask.png')
    fraction=weights.astype(float)/255;foreground=np.frombuffer(bytes.fromhex(packet['palette']['native_primary_rgb']),dtype=np.uint8).astype(float);secondary=np.frombuffer(bytes.fromhex(packet['palette']['native_detail_rgb']),dtype=np.uint8).astype(float);colors=foreground[None,None,:]*(1-fraction[:,:,None])+secondary[None,None,:]*fraction[:,:,None];rgb=np.uint8(np.round(colors*level[:,:,None]/255));rgb[coverage==0]=0;native=Image.fromarray(np.dstack([rgb,coverage]));native.save(folder/'native-w-C-preview.png')
    model['views'][f]=dict(primary=ref(folder/'primary-neutral.png'),detail=ref(folder/'detail-neutral.png'),coverage=ref(folder/'coverage.png'),detail_weight=ref(folder/'detail-weight.png'),detail_coverage=ref(folder/'detail-coverage.png'),authored_dualcolor_mask=ref(folder/'authored-dualcolor-mask.png'),canvas=[256,256],authoring_canvas=list(SIZE),source_cell=[16,24],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False)
    decisions[f]=dict(raw=ref(HERE/('refined-front-raw.png' if f=='south' else 'refined-turnaround-raw.png')),material=stats,coverage='Exact manual source coverage, resized once with premultiplied alpha; no generated halo, background or filled coil loop retained.',detail='Explicit source construction wood/glass role; pale highlights remain glass-owned. Native tint uses independent weight and one alpha.',fixed_frame=True)
    groups['neutral'][f]=neutral;groups['native'][f]=native;groups['detail'][f]=detail_im;groups['coverage'][f]=Image.fromarray(np.dstack([coverage,coverage,coverage,np.full(coverage.shape,255,np.uint8)]))
model.update(primary=model['views']['south']['primary'],detail=model['views']['south']['detail'],coverage=model['views']['south']['coverage'],detail_weight=model['views']['south']['detail_weight'],detail_coverage=model['views']['south']['detail_coverage'])
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(views=decisions,first_refinement=ref(HERE/'first-front-structural-review.json'),secondary_refinement=ref(HERE/'secondary-structural-review.json'),source_geometry=ref(HERE/'camera-and-geometry.json'),native_state_owner='One fixed fixture tile, no empty/full variants',new_imagegen_calls=2,second_isolation_call=False,native_acceptance=model['native_acceptance']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(images,name,title):
    out=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        # Restore rectangular source-cell aspect for authoring display.
        bg=Image.new('RGBA',(256,256),'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,384)),(16+i*284,60));d.text((16+i*284,470),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
            thumb=im.resize((w,h),Image.Resampling.LANCZOS);out.paste(thumb,(30+i*284+j*75,520),thumb)
    d.text((18,606),'One shared cell/pivot; E/N/W unbound authoring. Native source state, transparency and placement acceptance pending.',font=font,fill='#e5e8d8');out.save(OUT/name)
for key,name,title in [('neutral','all-views-neutral.png','ALCHEMIST TABLE / registered neutral front, complete side, back and explicit west'),('native','all-views-native-palette.png','SOURCE PALETTE / scorched wood w, glass C; generated glow excluded'),('detail','all-views-glass-ownership.png','GLASS ROLE / phials, coil, tubing and flask; wooden rack bars remain wood'),('coverage','all-views-coverage.png','EXACT COVERAGE / original construction; no background or glow')]:plate(groups[key],name,title)
compare=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(compare);d.text((18,14),'DEPTH CORRECTION / shared geometry changed, no side-image stretching',font=font,fill='#e3cf43')
inputs=[(HERE.parent/'v2/constructed-east.png','V2 / superseded thin end'),(HERE/'constructed-east.png','V3 / fuller manual end'),(OUT/'east/native-w-C-preview.png','SELECTED / source w-C'),(OUT/'west/native-w-C-preview.png','EXPLICIT WEST / asymmetric')]
for i,(p,label) in enumerate(inputs):
    im=read(p);im=im.resize((256,384),Image.Resampling.LANCZOS);compare.paste(im,(16+i*284,60),im);d.text((16+i*284,480),label,font=font,fill='#e3cf43')
d.text((18,555),'Authored depth6 / width13.6. Actual donor draw frame3.5 /1.5 is guidance, not a native Qud footprint.',font=font,fill='#e5e8d8');compare.save(OUT/'depth-before-after.png')
print('Registered all four source-bound views, neutral surfaces, exact coverage and independent native glass weight.')
