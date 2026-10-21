"""Transfer actual leather to intact fore boots; apply cuff/body depth last."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(768,1152);FACES=['south','east','north']


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


def canonical(im):
    a=np.array(im);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)


def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255));return canonical(Image.fromarray(a))


def complete(gray,known,envelope):
    labels,count=ndimage.label(envelope)
    for k in range(1,count+1):
        q=labels==k;assert (known&q).any(),'Each physical boot needs actual leather samples'
    unknown=envelope&~known;yy,xx=np.where(unknown);n=len(yy)
    if not n:return gray,unknown
    ids=np.full(gray.shape,-1,dtype=np.int32);ids[yy,xx]=np.arange(n)
    degree=np.zeros(n);rhs=np.zeros(n);rows=[];cols=[]
    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<SIZE[1])&(nx>=0)&(nx<SIZE[0]));q=q[envelope[ny[q],nx[q]]]
        degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rows.extend(q[pending]);cols.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
    matrix=sparse.coo_matrix((-np.ones(len(rows)),(rows,cols)),shape=(n,n)).tocsr()+sparse.diags(degree)
    gray[yy,xx]=spsolve(matrix,rhs);assert np.isfinite(gray[envelope]).all();return gray,unknown


assert not (HERE/'model.json').exists()
packet=read(HERE/'source-packet.json');bm=read(ROOT/packet['body']['path']);assert ref(ROOT/packet['body']['path'])==packet['body']
assert read(HERE/'first-refinement-structural-review.json')['status']=='PASS FOR MATERIAL REGISTRATION'
raw=np.array(image(HERE/'context-refinement-raw.png')).astype(float)
palette={k:tuple(bytes.fromhex(v)) for k,v in read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'].items()}
yy,xx=np.mgrid[0:SIZE[1],0:SIZE[0]].astype(float)
controls=dict(south_left=[181,286,347,603],south_right=[364,285,531,603],east_pair=[1233,266,1471,602],north_plain_leather=[1245,305,1290,520],
 policy='Per-part source texture coordinates only; target geometry/alpha and body physical frame do not change. Source figure scaling/repositioning is not used as production anatomy.',
 north='Hidden heel surfaces use actual profile plain leather, without front wire; source rear construction supplies the heel seam. This is authored continuation, not recovered hidden detail.')
write('material-sampling-controls.json',controls)
model=dict(item='Leather Boots',blueprint='Leather Boots',family='yrame',slot='Feet',laterality=16,workflow='regional-curved-v1',canvas=list(SIZE),contact=bm['registration']['contact'],
 base_model=packet['body']['path'],body_sha256=packet['body']['sha256'],actual_equipped_binding=packet['actual_binding'],frame_mapping=bm['registration'],fit_contract=ref(HERE/'fit-contract.json'),views={},occlusion_sources={},
 policy='One complete physical boot pair on equipped fore Feet297/16 only. Added hind Feet298/64 remains bare. Preserve full boot sources and toe/sole coverage; no bare hoof overlay.',
 layer_order='South body -> paired fore boots -> original shin entry; east body -> far fore boot -> near fore boot -> shin entry; north intact fore boots behind original hind legs/body.',
 mask_semantics='White selects original cuff-entry shin pixels in south/east; north original body depth occludes intact fore boots. No boot-shaped holes in body and no body-shaped holes in boots.',
 west_policy='Mirror exact east body, pair and cuff masks; same Feet297/16 binding and physical size.',native_acceptance='Pending full-set generation gate, actual Feet297/16 equipment/unequip and complete Yrame outfit.')
groups={k:{} for k in ['assembly','palette','full','off','mask','overlay','wire','continued']};decisions={}
for f in FACES:
    pattern=image(HERE/f'constructed-boots-{f}.png');pa=np.array(pattern)
    parts={}
    if f=='east':parts={name:image(HERE/f'boot-{name}-east.png') for name in ['far','near']}
    else:
        for name,lo,hi in [('left',0,384),('right',384,768)]:
            a=pa.copy();a[:,:lo]=0;a[:,hi:]=0;parts[name]=Image.fromarray(a)
    complete_parts={};wire_parts={};stats={};rows=[];all_continued=np.zeros((SIZE[1],SIZE[0]),dtype='uint8')
    for name,part in parts.items():
        a=np.array(part);envelope=a[:,:,3]>0;ty,tx=np.where(envelope);target=[int(tx.min()),int(ty.min()),int(tx.max()+1),int(ty.max()+1)]
        # Each physical source owns its own wire. In profile the combined wire
        # mask would incorrectly stamp the near laces onto the hidden far boot.
        part_wire=np.clip((a[:,:,:3].mean(2)-197)/41,0,1)*255
        if f=='south':source=controls['south_'+name];domain=target
        elif f=='east':source=controls['east_pair'];domain=list(pattern.getbbox())
        else:source=controls['north_plain_leather'];domain=target
        x0,y0,x1,y1=domain;s0,t0,s1,t1=source
        sx=s0+(xx-x0)*(s1-s0)/(x1-x0);sy=t0+(yy-y0)*(t1-t0)/(y1-y0)
        rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[sy,sx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
        source_alpha=ndimage.map_coordinates(raw[:,:,3],[sy,sx],order=1,mode='constant',cval=0)
        gray=rgb.mean(2);red=(rgb[:,:,0]>rgb[:,:,1]*1.3)&(rgb[:,:,0]>rgb[:,:,2]*1.3)
        known=ndimage.binary_erosion(envelope,iterations=2)&(np.ptp(rgb,axis=2)<30)&(gray>40)&(gray<232)&(source_alpha>200)&~ndimage.binary_dilation(red,iterations=2)&(part_wire<20)
        if f=='east' and name=='far':known&=np.array(parts['near'])[:,:,3]<128
        assert known.sum()>100,(f,name)
        gray,unknown=complete(gray.copy(),known,envelope);gray=10+.9*gray
        manual=a[:,:,:3].mean(2);gray[(manual<105)&envelope]=manual[(manual<105)&envelope]
        region=np.where(envelope,part_wire,0).astype(float)/255
        gray=gray*(1-region)+236*region
        value=np.uint8(np.clip(np.round(gray),0,255));value[~envelope]=0
        boot=canonical(Image.fromarray(np.dstack([value,value,value,a[:,:,3]])));boot.save(HERE/f'intact-{name}-{f}.png')
        detail=np.array(boot);detail[:,:,3]=np.where(a[:,:,3]==255,np.uint8(np.round(region*255)),0)
        detail=canonical(Image.fromarray(detail));detail.save(HERE/f'wire-{name}-{f}.png')
        assert np.array_equal(np.array(Image.alpha_composite(boot,detail)),np.array(boot))
        complete_parts[name]=boot;wire_parts[name]=detail;all_continued=np.maximum(all_continued,np.uint8(unknown)*255)
        stats[name]=dict(known_leather_pixels=int(known.sum()),continued_pixels=int(unknown.sum()),source_box=source,target_texture_domain=domain,geometry_bounds=target,
                        full_alpha_preserved=bool(np.array_equal(np.array(boot)[:,:,3],a[:,:,3])),sample_role='actual profile plain leather with authored rear seam' if f=='north' else 'actual contextual visible neutral leather, bright wire excluded')
        layer=-.0002 if f=='north' else (.0014 if name=='near' else .0012)
        for component,p,role,depth in [(f'item-{name}',HERE/f'intact-{name}-{f}.png','equipment',layer),(f'item-{name}-detail',HERE/f'wire-{name}-{f}.png','equipment-detail',layer+.00001)]:
            if role=='equipment-detail' and not np.array(detail)[:,:,3].any():continue
            row=dict(bm['views'][f][0]);rr=ref(p);row.update(component=component,color_role=role,file=f'yrame-leather-boots-v2-{component}-{f}.png',public_file=rr['path'],sha256=rr['sha256'],layer=depth,equipment_key='leather-boots@Feet@16');row.pop('native_part',None);row.pop('mutation_anatomy',None);rows.append(row)
    full=Image.new('RGBA',SIZE);colored_boots=Image.new('RGBA',SIZE);wire_all=Image.new('RGBA',SIZE)
    for name in complete_parts:
        full.alpha_composite(complete_parts[name]);wire_all.alpha_composite(wire_parts[name]);colored_boots.alpha_composite(Image.alpha_composite(tint(complete_parts[name],palette['w']),tint(wire_parts[name],palette['y'])))
    full.save(HERE/f'intact-boots-{f}.png');Image.fromarray(all_continued).save(HERE/f'authored-continuation-{f}.png')
    base=image(HERE/f'original-body-{f}.png');native_body=Image.new('RGBA',SIZE);overlay=Image.new('RGBA',SIZE);native_overlay=Image.new('RGBA',SIZE);overlay_refs=[]
    mask=np.array(Image.open(HERE/f'body-visibility-{f}.png').convert('L'))
    for original in sorted(bm['views'][f],key=lambda r:r['layer']):
        source=image(ROOT/original['public_file']);assert ref(ROOT/original['public_file'])['sha256']==original['sha256'];color=palette['B'] if original['color_role']=='detail' else palette['w'];native_body.alpha_composite(tint(source,color))
        if f=='north':continue
        a=np.array(source);a[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*mask/255));part=canonical(Image.fromarray(a));overlay.alpha_composite(part);native_overlay.alpha_composite(tint(part,color))
        if np.array(part)[:,:,3].any():
            name='body-overlay-detail' if original['color_role']=='detail' else 'body-overlay';p=HERE/f'{name}-{f}.png';part.save(p);rr=ref(p)
            row=dict(original);row.update(component=name,file=f'yrame-leather-boots-v2-{name}-{f}.png',public_file=rr['path'],sha256=rr['sha256'],layer=.00161 if original['color_role']=='detail' else .0016,equipment_key='leather-boots@Feet@16');row.pop('native_part',None);row.pop('mutation_anatomy',None);rows.append(row);overlay_refs.append(rr)
    off=Image.alpha_composite(base,full)
    if f=='north':assembly=Image.alpha_composite(full,base);native=Image.alpha_composite(colored_boots,native_body);overlay=base.copy();a=np.array(overlay);a[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*mask/255));overlay=canonical(Image.fromarray(a))
    else:assembly=Image.alpha_composite(off,overlay);native=Image.alpha_composite(Image.alpha_composite(native_body,colored_boots),native_overlay)
    for k,im in [('assembly',assembly),('palette',native),('full',full),('off',off),('mask',Image.fromarray(mask).convert('RGBA')),('overlay',overlay),('wire',wire_all),('continued',Image.fromarray(all_continued).convert('RGBA'))]:
        im=canonical(im);groups[k][f]=im;im.save(HERE/f'{k}-{f}.png')
    model['views'][f]=rows;model['occlusion_sources'][f]=dict(original_body=ref(HERE/f'original-body-{f}.png'),full_boots=ref(HERE/f'intact-boots-{f}.png'),visibility=ref(HERE/f'body-visibility-{f}.png'),overlays=overlay_refs,
        depth='original body/hind legs after intact fore boots; no extra overlay node' if f=='north' else 'far then near boots above body, cuff-entry original body last')
    decisions[f]=dict(parts=stats,full_physical_pair_retained=True,hind_feet_equipped=False,body_unchanged=True,fit='Constructed identity fit on selected forelegs; material sampling changes no garment geometry.',
                     depth=model['occlusion_sources'][f]['depth'])

for values in groups.values():values['west (mirror)']=ImageOps.mirror(values['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)


def plate(key,name,title,feet=False):
    out=Image.new('RGB',(1200,480 if feet else 700),'#142823');d=ImageDraw.Draw(out);d.text((18,15),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(groups[key].items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im)
        display=bg.crop((100,740,700,1100)).resize((280,168),Image.Resampling.LANCZOS) if feet else bg.resize((280,420),Image.Resampling.LANCZOS)
        out.paste(display.convert('RGB'),(10+i*300,60));d.text((15+i*300,280 if feet else 500),f.upper(),font=font,fill='#e3cf43')
    d.text((18,out.height-55),'Fore Feet297/16 only; hind Feet298/64 remains bare. Fixed body/frame; native acceptance pending.',font=font,fill='#e5e8d8');out.save(HERE/name)


for key,name,title,feet in [('assembly','assembly-comparison.png','YRAME / closed leather boots on actual equipped fore pair',False),('assembly','footwear-comparison.png','MATCHED-SCALE FOOTWEAR / original bare hind pair and natural fore overlap',True),('full','intact-boots-comparison.png','FULL BOOTS / hidden rear sources retained before original body depth',True),('off','depth-off-comparison.png','DEPTH OFF / full physical fore boots before hind legs hide them',True),('mask','body-mask-comparison.png','BODY VISIBILITY / curved cuff entries; rear body occlusion',True),('overlay','body-overlay-comparison.png','ORIGINAL BODY OWNERSHIP / no bare fore hoof restored over closed leather',True),('wire','wire-detail-comparison.png','SOURCE y DETAIL / front wire only; plain rear heel seams',True),('palette','independent-palette-comparison.png','NATIVE w/y BOOTS / original B lower body remains independent',False),('continued','continuation-comparison.png','CONTINUED LEATHER / hidden, wire-excluded and unsampled material',True)]:plate(key,name,title,feet)
small=Image.new('RGB',(600,390),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((64,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*150+40,20),thumb);big=thumb.resize((128,192),Image.Resampling.NEAREST);small.paste(big,(i*150+10,140),big);d.text((i*150+5,360),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
now=datetime.now(timezone.utc).isoformat();write('model.json',model)
write('registration-decisions.json',dict(recorded_at=now,contextual_source=ref(HERE/'context-refinement-raw.png'),first_structural_review=ref(HERE/'first-refinement-structural-review.json'),material_controls=ref(HERE/'material-sampling-controls.json'),body=packet['body'],views=decisions,
 material='Actual visible neutral leather; exclude red anatomy and bright source wire. Harmonic completion within full manual boot alpha. Restore explicit source seams/soles and editable wire. North hidden heels share actual profile plain leather.',
 tone_curve='leather_gray=10+0.9*sampled/completed_gray; original source ink<105 retained; wire236 mixed using editable region.',
 body_and_physical_frame_unchanged=True,full_source_before_depth=True,second_isolation_call=False,native_acceptance=model['native_acceptance']))
ledger=read(ROOT/'evidence/conversion-ledger.json');entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert entry['id']==packet['entry']
for step,phase,names,text in [
 ('imagegen_refine_in_context_on_unchanged_body','Actual boot refinement: fore/hind ownership reviewed',['generation-receipt.json','context-refinement-raw.png','first-refinement-solid-review.png','first-refinement-structural-review.json'],'One actual contextual refinement. Closed fore pair, naturally partial far boot and bare hind hooves retained; original body remains production source.'),
 ('retrieve_isolated_item_and_masks','Complete leather and wire before original-body cuff/rear depth',['register-boots.py','material-sampling-controls.json','registration-decisions.json','model.json','intact-boots-comparison.png','wire-detail-comparison.png','continuation-comparison.png'],'Actual leather registered to intact fixed boot geometry. Wire excluded from leather sampling and retained separately. Full hidden fore boots preserved; no second isolation generation, bare-hoof overlay or body-shaped alpha cutout. Final fit review pending.')]:
    entry['process_log'].append(dict(timestamp=now,step=step,phase=phase,action=text,inputs=[ref(HERE/'fit-contract.json'),ref(HERE/'context-refinement-raw.png')],outputs=[ref(HERE/n) for n in names],review=text,result='PASS'))
entry.update(current_step='recompose_check_cuffs_attachment_occlusion_all_views',generation_ready=False,current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
 art_review=dict(status='REQUIRES REVIEW',reason='Current actual fore boot pair on selected body. Inspect complete foot coverage, cuff entry, near/far depth, bare hind hooves and separate wire before fit credit.'),
 registration_summary='Current v2 fore Feet297/16 candidate: full closed leather/wire sources on fixed selected centauroid; added hind pair bare. Curved cuff entry and rear body depth separate; final authoring review pending.')
ledger['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Registered actual leather on full physical fore boot pair; final all-view coverage/depth/palette review pending.')
