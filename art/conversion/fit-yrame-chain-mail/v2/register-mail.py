"""Register contextual linked steel on continuous mail, then apply body visibility."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SIZE=(768,1152);FACES=['south','east','north']


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


def canonical(im):
    a=np.array(im);a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a)


def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255))
    return canonical(Image.fromarray(a))


def complete(gray,known,envelope,manual):
    labels,count=ndimage.label(envelope)
    authored_islands=0
    for k in range(1,count+1):
        component=labels==k
        if not (known&component).any():
            assert component.sum()<100,'A substantial cloth component has no observed metal'
            gray[component]=manual[component];known[component]=True;authored_islands+=int(component.sum())
    unknown=envelope&~known;yy,xx=np.where(unknown);n=len(yy)
    if not n:return gray,unknown,authored_islands
    ids=np.full(gray.shape,-1,dtype=np.int32);ids[yy,xx]=np.arange(n)
    degree=np.zeros(n);rhs=np.zeros(n);rows=[];cols=[]
    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<SIZE[1])&(nx>=0)&(nx<SIZE[0]));q=q[envelope[ny[q],nx[q]]]
        degree[q]+=1;adjacent=ids[ny[q],nx[q]];pending=adjacent>=0
        rows.extend(q[pending]);cols.extend(adjacent[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
    matrix=sparse.coo_matrix((-np.ones(len(rows)),(rows,cols)),shape=(n,n)).tocsr()+sparse.diags(degree)
    gray[yy,xx]=spsolve(matrix,rhs)
    assert np.isfinite(gray[envelope]).all()
    return gray,unknown,authored_islands


assert not (HERE/'model.json').exists()
packet=read(HERE/'source-packet.json');bm=read(ROOT/packet['body']['path']);assert ref(ROOT/packet['body']['path'])==packet['body']
assert read(HERE/'first-refinement-structural-review.json')['status']=='PASS FOR EXTRACTION/FITTING'
raw=np.array(image(HERE/'context-refinement-raw.png')).astype(float)
colors={k:tuple(bytes.fromhex(v)) for k,v in read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'].items()}
yy,xx=np.mgrid[0:SIZE[1],0:SIZE[0]].astype(float)
model=dict(item='Chain Mail',blueprint='Chain Mail',family='yrame',slot='Body',laterality=0,workflow='regional-curved-v1',
           canvas=list(SIZE),contact=bm['registration']['contact'],base_model=packet['body']['path'],body_sha256=packet['body']['sha256'],
           actual_equipped_binding=packet['actual_binding'],frame_mapping=bm['registration'],fit_contract=ref(HERE/'fit-contract.json'),views={},occlusion_sources={},
           policy='One source-bound centauroid mail shirt. Continuous metal and independent original-body visibility; no anatomy baked into garment and no body-shaped cloth cutouts.',
           layer_order='Original body/head -> full mail .0012 -> metal detail .00125 -> original arm/hand foreground .0013 and body-detail .00131.',
           mask_semantics='White selects original body above full garment; black none; gray geometric coverage. Mask always multiplied by actual source-body alpha.',
           west_policy='Mirror east cloth, body and masks together; plain source mail has no handed ornament.',
           native_acceptance='Pending full-generation gate, actual equipped-state and complete named outfit.')
groups={k:{} for k in ['assembly','cloth','mask','overlay','off','palette','detail','continued']};decisions={}
for i,f in enumerate(FACES):
    pattern=image(HERE/f'constructed-cloth-{f}.png');pa=np.array(pattern);envelope=pa[:,:,3]>0
    sx=(xx-144+i*480)*raw.shape[1]/1440;sy=(yy-240)*raw.shape[0]/540
    rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[sy,sx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
    source_alpha=ndimage.map_coordinates(raw[:,:,3],[sy,sx],order=1,mode='constant',cval=0)
    red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3)
    known=ndimage.binary_erosion(envelope,iterations=2)&(np.ptp(rgb,axis=2)<35)&(rgb.mean(2)>25)&(source_alpha>200)&~ndimage.binary_dilation(red,iterations=2)
    assert known.sum()>500,f
    gray,unknown,islands=complete(rgb.mean(2).copy(),known.copy(),envelope,pa[:,:,:3].mean(2))
    # Reduce texture contrast without blurring or changing the source geometry.
    gray=70+.65*gray
    manual=pa[:,:,:3].mean(2);gray[(manual<90)&envelope]=manual[(manual<90)&envelope]
    value=np.uint8(np.clip(np.round(gray),0,255));value[~envelope]=0
    cloth=canonical(Image.fromarray(np.dstack([value,value,value,pa[:,:,3]])));cloth.save(HERE/f'intact-mail-{f}.png')
    assert np.array_equal(np.array(cloth)[:,:,3],pa[:,:,3])
    Image.fromarray(np.uint8(unknown)*255).save(HERE/f'authored-continuation-{f}.png')
    ma=np.array(Image.open(HERE/f'body-visibility-ready-{f}.png').convert('L'))
    region=np.array(Image.open(HERE/f'detail-region-{f}.png').convert('L'))
    detail=np.array(cloth);detail[:,:,3]=np.where(pa[:,:,3]==255,region,0).astype('uint8')
    detail=canonical(Image.fromarray(detail));detail.save(HERE/f'item-detail-{f}.png')
    assert np.array_equal(np.array(Image.alpha_composite(cloth,detail)),np.array(cloth))
    body=Image.new('RGBA',SIZE);native_body=Image.new('RGBA',SIZE);overlays=[];overlay_all=Image.new('RGBA',SIZE);native_overlay=Image.new('RGBA',SIZE)
    rows=[]
    for component,name,role,layer in [('item','intact-mail','equipment',.0012),('item-detail','item-detail','equipment-detail',.00125)]:
        row=dict(bm['views'][f][0]);p=HERE/f'{name}-{f}.png';rr=ref(p)
        row.update(component=component,color_role=role,file=f'yrame-chain-mail-v2-{component}-{f}.png',public_file=rr['path'],sha256=rr['sha256'],layer=layer,equipment_key='chain-mail@Body@0')
        row.pop('native_part',None);row.pop('mutation_anatomy',None);rows.append(row)
    for source in sorted(bm['views'][f],key=lambda r:r['layer']):
        p=ROOT/source['public_file'];assert ref(p)['sha256']==source['sha256'];im=image(p);body.alpha_composite(im)
        role=source['color_role'];color=colors['B'] if role=='detail' else colors['w'];native_body.alpha_composite(tint(im,color))
        a=np.array(im);a[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*ma/255));overlay=canonical(Image.fromarray(a));overlay_all.alpha_composite(overlay);native_overlay.alpha_composite(tint(overlay,color))
        if np.array(overlay)[:,:,3].any():
            name='body-overlay-detail' if role=='detail' else 'body-overlay';p=HERE/f'{name}-{f}.png';overlay.save(p);rr=ref(p)
            row=dict(source);row.update(component=name,color_role=role,file=f'yrame-chain-mail-v2-{name}-{f}.png',public_file=rr['path'],sha256=rr['sha256'],layer=.00131 if role=='detail' else .0013,equipment_key='chain-mail@Body@0');row.pop('native_part',None);row.pop('mutation_anatomy',None);rows.append(row);overlays.append(rr)
    assert np.array_equal(np.array(body),np.array(image(HERE/f'original-body-{f}.png')))
    off=Image.alpha_composite(body,cloth);assembled=Image.alpha_composite(off,overlay_all)
    metal=Image.alpha_composite(tint(cloth,colors['y']),tint(detail,colors['Y']));native=Image.alpha_composite(Image.alpha_composite(native_body,metal),native_overlay)
    for k,im in [('assembly',assembled),('cloth',cloth),('mask',Image.fromarray(ma).convert('RGBA')),('overlay',overlay_all),('off',off),('palette',native),('detail',detail),('continued',Image.fromarray(np.uint8(unknown)*255).convert('RGBA'))]:
        im=canonical(im);groups[k][f]=im;im.save(HERE/f'{k}-{f}.png')
    model['views'][f]=rows
    model['occlusion_sources'][f]=dict(original_body=ref(HERE/f'original-body-{f}.png'),full_mail=ref(HERE/f'intact-mail-{f}.png'),visibility=ref(HERE/f'body-visibility-ready-{f}.png'),overlays=overlays,detail=ref(HERE/f'item-detail-{f}.png'))
    decisions[f]=dict(known_visible_steel_pixels=int(known.sum()),authored_continuation_pixels=int(unknown.sum()),tiny_authored_island_pixels=islands,
                      full_alpha_preserved=True,fit='Identity fit at body landmarks. No exterior stretch or internal warp required; full source constructed directly for this body.',
                      unchanged_body=ref(HERE/f'original-body-{f}.png'),mask=ref(HERE/f'body-visibility-ready-{f}.png'),
                      body_overlay_pixels=int(np.count_nonzero(np.array(overlay_all)[:,:,3])),
                      continuation='Harmonic continuation within complete manual garment for arm-hidden, excluded or edge-unsampled steel. Retain authored source ink. No unseen generated-body pixels copied.')

for values in groups.values():values['west (mirror)']=ImageOps.mirror(values['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)


def plate(key,name,title,torso=False):
    out=Image.new('RGB',(1200,650 if torso else 700),'#142823');d=ImageDraw.Draw(out);d.text((18,15),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(groups[key].items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im)
        if torso:
            box=(350,260,660,700) if f=='east' else ((108,260,418,700) if f.startswith('west') else (194,260,574,700))
            display=bg.crop(box);display.thumbnail((280,440),Image.Resampling.LANCZOS)
        else:display=bg.resize((280,420),Image.Resampling.LANCZOS)
        out.paste(display.convert('RGB'),(10+i*300,55));d.text((15+i*300,530 if torso else 500),f.upper(),font=font,fill='#e3cf43')
    d.text((18,out.height-55),'Fixed bare body, continuous mail and separate curved visibility. Native acceptance pending.',font=font,fill='#e5e8d8');out.save(HERE/name)


for key,name,title in [('assembly','assembly-comparison.png','YRAME / one Chain Mail shirt on selected centauroid body'),('cloth','intact-garment-comparison.png','FULL MAIL / no applied forearm or hand cutout'),('overlay','body-overlay-comparison.png','ORIGINAL BODY OVERLAY / forearms and hands, separate w / B roles'),('mask','body-mask-comparison.png','PAINTED BODY VISIBILITY / curved sleeve lips and exact hand ownership'),('off','mask-off-comparison.png','MASK OFF / intact mail before original-body visibility'),('palette','independent-palette-comparison.png','NATIVE PALETTE / body w / B; mail y / Y'),('detail','detail-comparison.png','Y DETAIL / bright linked steel near cuff ends and hem'),('continued','continuation-comparison.png','AUTHORED CONTINUATION / hidden, excluded and edge-unsampled steel')]:plate(key,name,title)
plate('assembly','torso-fit-comparison.png','PER-VIEW FIT / connected shoulders, curved cuffs and front/dorsal hems',True)
small=Image.new('RGB',(600,390),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((64,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*150+40,20),thumb);big=thumb.resize((128,192),Image.Resampling.NEAREST);small.paste(big,(i*150+10,140),big);d.text((i*150+5,360),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
now=datetime.now(timezone.utc).isoformat()
write('model.json',model)
write('registration-decisions.json',dict(recorded_at=now,source=ref(HERE/'context-refinement-raw.png'),first_structural_review=ref(HERE/'first-refinement-structural-review.json'),body=packet['body'],
     sampling=dict(context_crop=[144,240,624,720],input_sheet=[1440,540],actual_output=[raw.shape[1],raw.shape[0]],mapping='sx=(body_x-144+facing_index*480)*raw_width/1440; sy=(body_y-240)*raw_height/540'),
     material_tone_curve='gray=70+0.65*sampled/completed_gray; preserve manual ink below90. Contrast reduction only, no blur.',views=decisions,
     body_and_physical_frame_unchanged=True,full_source_before_fitting_and_visibility=True,second_isolation_call=False,
     deformation='Identity. Regional controls were needed for body-class cuff/hand visibility, not a forced garment warp.',native_acceptance=model['native_acceptance']))
ledger=read(ROOT/'evidence/conversion-ledger.json');entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert entry['id']==packet['entry']
for step,phase,names,text in [
 ('imagegen_refine_in_context_on_unchanged_body','Actual contextual linked-steel refinement reviewed',['generation-receipt.json','context-refinement-raw.png','first-refinement-solid-review.png','first-refinement-structural-review.json'],'One real contextual refinement; connected shoulders, curved sleeves, long front and short dorsal hem retained. Generated mannequin is reference only.'),
 ('retrieve_isolated_item_and_masks','Full mail completion then fixed-body late visibility',['register-mail.py','model.json','registration-decisions.json','intact-garment-comparison.png','body-mask-comparison.png','continuation-comparison.png'],'Actual neutral steel sampled from the same output. Hidden/excluded material completed inside the full manual garment before fitting; no body-shaped alpha holes and no second isolation generation. Original forearms/hands applied last. Final fit review pending.')]:
    entry['process_log'].append(dict(timestamp=now,step=step,phase=phase,action=text,inputs=[ref(HERE/'fit-contract.json'),ref(HERE/'context-refinement-raw.png')],outputs=[ref(HERE/n) for n in names],review=text,result='PASS'))
entry.update(current_step='recompose_check_cuffs_attachment_occlusion_all_views',generation_ready=False,current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
             art_review=dict(status='REQUIRES REVIEW',reason='Current centauroid mail, complete metal, separate body visibility and native tint candidate. Inspect all sleeves, shoulder coverage, front/dorsal hem and exact hand ownership before fit credit.'),
             registration_summary='Current v2 candidate on selected centauroid body. One mail shirt, long front/short dorsal hem, full metal and late original-body mask; final visual review pending.')
ledger['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Registered continuous mail and original-body overlays in the fixed physical frame; final assembled authoring review pending.')
