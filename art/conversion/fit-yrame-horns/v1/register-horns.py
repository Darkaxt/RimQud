"""Select per-facing bone material; retain full near/far horns and fixed head depth."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1152)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
def complete(gray,envelope,known):
    if not envelope.any():return gray,np.zeros(envelope.shape,bool)
    assert known.any(),'Every nonempty horn layer needs source material.'
    unknown=envelope&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(envelope.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<SIZE[1])&(nx>=0)&(nx<SIZE[0]));q=q[envelope[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
    gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs);assert np.isfinite(gray[envelope]).all()
    return gray,unknown
packet=json.loads((HERE/'source-packet.json').read_text());raw=np.array(read(HERE/'refined-red-context.png')).astype(float);bm=json.loads((BODY/'model.json').read_text());yy,xx=np.mgrid[0:SIZE[1],0:SIZE[0]].astype(float)
model=dict(item='Horns',blueprint='Horns',family='yrame',unmutated_body_family='human-female',slot='Head',laterality=0,canvas=list(SIZE),contact=[256,1078],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],actual_equipped_binding=packet['actual_head_binding'],frame_mapping=packet['frame'],views={},binding_scope=packet['scope'],policy='Independent natural-equipment horns; whole near/far sources retain their roots. Body/head occlusion is layer order, not destructive root cutout.',west_policy='Mirror authored east near/far layers and body; symmetric source pair with no unique side mark.',native_acceptance=packet['native_acceptance'])
groups={k:{} for k in ['assembly','palette','full','off','ownership']};decisions={}
for index,f in enumerate(['south','east','north']):
    mx=(xx+index*512)*raw.shape[1]/1536;my=yy*raw.shape[0]/640
    rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1);gray_base=rgb.mean(2)
    body=read(HERE/f'original-body-{f}.png');ba=np.array(body)[:,:,3]
    patterns={d:np.array(read(HERE/f'patched-constructed-{d}-{f}.png')) for d in ['near','far']};layers={};details={};stats={};rows=[]
    for depth in ['near','far']:
        pattern=patterns[depth];envelope=pattern[:,:,3]>0
        visible=envelope if depth=='near' else envelope&(ba<128)&(patterns['near'][:,:,3]<128)
        known=ndimage.binary_erosion(envelope,iterations=1)&visible&(np.ptp(rgb,axis=2)<15)&(gray_base>45)&(gray_base<250)
        gray,unknown=complete(gray_base.copy(),envelope,known);ink=pattern[:,:,:3].mean(2);gray[(ink<100)&envelope]=ink[(ink<100)&envelope]
        v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;item=Image.fromarray(np.dstack([v,v,v,pattern[:,:,3]]));item.save(HERE/f'intact-{depth}-{f}.png');Image.fromarray(np.uint8(unknown)*255).save(HERE/f'continued-{depth}-{f}.png')
        detail=item.copy();detail_alpha=np.uint8(np.round(pattern[:,:,3]*np.clip((gray-185)/45,0,1)));detail.putalpha(Image.fromarray(detail_alpha));a=np.array(detail);a[a[:,:,3]==0,:3]=0;detail=Image.fromarray(a);detail.save(HERE/f'detail-{depth}-{f}.png')
        layers[depth]=item;details[depth]=detail;stats[depth]=dict(known_visible_pixels=int(known.sum()),completed_hidden_pixels=int(unknown.sum()),full_alpha_unchanged=True)
        if envelope.any():
            for component,stem,role,layer in [(f'item-{depth}',f'intact-{depth}','equipment',-.0002 if depth=='far' else .0018),(f'item-{depth}-detail',f'detail-{depth}','equipment-detail',-.00019 if depth=='far' else .00181)]:
                path=HERE/f'{stem}-{f}.png';r=ref(path);row=dict(bm['views'][f][0]);pixel_z=row['height']/1024;row.update(component=component,file=f'yrame-horns-v1-{component}-{f}.png',public_file=r['path'],sha256=r['sha256'],size=list(SIZE),contact=[256,1078],height=pixel_z*1152,center_z=(1078-576)*pixel_z,equipment_key='horns@Head@0',color_role=role,layer=layer);rows.append(row)
    near=Image.alpha_composite(layers['near'],details['near']);far=Image.alpha_composite(layers['far'],details['far']);full=Image.alpha_composite(far,near)
    assembly=Image.alpha_composite(Image.alpha_composite(far,body),near);assembly.save(HERE/f'assembled-{f}.png');full.save(HERE/f'intact-item-{f}.png');off=Image.alpha_composite(body,full);off.save(HERE/f'depth-off-{f}.png')
    def color_layer(depth):return Image.alpha_composite(tint(layers[depth],tuple(bytes.fromhex(packet['palette']['primary_rgb']))),tint(details[depth],tuple(bytes.fromhex(packet['palette']['detail_rgb']))))
    colored=Image.alpha_composite(Image.alpha_composite(color_layer('far'),tint(body,(152,135,95))),color_layer('near'));colored.save(HERE/f'qud-palette-{f}.png')
    ownership=Image.alpha_composite(Image.alpha_composite(tint(layers['far'],(230,185,30)),body),tint(layers['near'],(40,165,220)))
    for key,im in [('assembly',assembly),('palette',colored),('full',full),('off',off),('ownership',ownership)]:groups[key][f]=im
    model['views'][f]=rows;decisions[f]=dict(layers=stats,original_body=ref(HERE/f'original-body-{f}.png'),body_model=ref(BODY/'model.json'),depth='far -> original body/head -> near',no_body_rescale=True,whole_roots_retained=True)
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(images,name,title):
    out=Image.new('RGB',(1152,750),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,576)),(16+i*284,54));d.text((16+i*284,660),f.upper(),font=font,fill='#e3cf43')
    d.text((18,708),'Original ordinary body, padded128px above; same physical pixel scale. Yrame native mutation/outfit acceptance pending.',font=font,fill='#e5e8d8');out.save(HERE/name)
for key,name,title in [('assembly','assembly-comparison.png','YRAME / independent great grooved horns / distinct profile overlap'),('palette','independent-palette-comparison.png','NATIVE PALETTE / primary w, detail W gold; body w independent'),('full','full-item-comparison.png','FULL HORNS / complete near/far bone before original head depth'),('off','depth-off-comparison.png','DEPTH OFF / roots before original head covers hidden surfaces'),('ownership','near-far-ownership-comparison.png','DEPTH GUIDE / near cyan, far gold; report colors only')]:plate(groups[key],name,title)
small=Image.new('RGB',(560,405),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,108),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);big=thumb.resize((96,216),Image.Resampling.NEAREST);small.paste(big,(i*140+20,150),big);d.text((i*140+4,380),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',dict(raw=ref(HERE/'refined-red-context.png'),structural_gate=ref(HERE/'first-refinement-structural-review.json'),manual_patch=ref(HERE/'manual-groove-correction.json'),views=decisions,sampling='Per-facing source coordinates scaled from actual raw dimensions to1536x640 context; only visible neutral bone samples. Complete hidden roots/far bone with harmonic continuation; exact selected full alpha/ink retained.',frame_mapping=packet['frame'],new_imagegen_calls=1,second_isolation_call=False,native_acceptance=model['native_acceptance']))
print('Registered full directional near/far horns and native w/W regions; original body and physical pixel scale preserved.')
