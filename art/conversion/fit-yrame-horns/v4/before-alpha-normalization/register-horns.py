"""Register the actual contextual refinement to the fixed crown landmarks.

No isolation generation. The red reference is removed by color ownership;
occluded north root interiors are restored from the editable physical item.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SIZE = (768,1152)
FACES = ['south','east','north']


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def image(p):
    return Image.open(p).convert('RGBA')


def write(name, value):
    (HERE/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())


def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def tint(im, color):
    a=np.array(im)
    a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255))
    return Image.fromarray(a)


assert not (HERE/'model.json').exists()
packet=read(HERE/'source-packet.json')
body_model=read(ROOT/packet['base_body']['path'])
assert ref(ROOT/packet['base_body']['path'])==packet['base_body']
raw=image(HERE/'context-refinement-raw.png')
a=np.array(raw); rgb=a[:,:,:3].astype(float)
# Bone is mildly warm in the refinement. Neutralize only after separation;
# red mannequin pixels (including dark-red outlines) are excluded beforehand.
ownership=(np.ptp(rgb,axis=2)<40)&(rgb[:,:,0]<rgb[:,:,1]*1.35+10)&(a[:,:,3]>30)
labels,n=ndimage.label(ownership)
selected=[]
for k in range(1,n+1):
    y,x=np.where(labels==k)
    if len(y)>1000:
        selected.append(dict(label=k,pixels=len(y),bbox=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]))
assert len(selected)==5, selected
# Each of the five bone components must lie completely in the upper contextual
# horn area. This check detects body-outline leakage; it does not crop a horn.
assert all(r['bbox'][3]<330 for r in selected)
keep=np.isin(labels,[r['label'] for r in selected])
lum=np.uint8(np.round(rgb.mean(2)))
separated=np.dstack([lum,lum,lum,np.where(keep,a[:,:,3],0).astype('uint8')])
separated[~keep,:3]=0
Image.fromarray(separated).save(HERE/'extracted-neutral-context.png')

controls=dict(common_source_to_body_scale=.5,
              calibration='Source paired crown landmarks160px apart map to80px target spacing. One common physical scale for all facings; per-view translation only. Source coordinates are authored registration measurements, not native anatomy.',
              south=dict(source_roots=[[300,225],[460,225]],target_roots=[[344,125],[424,125]],translation=[194,12.5],source_panel=[0,0,682,768]),
              east=dict(source_roots=[[1055,220]],target_roots=[[510,143]],translation=[-17.5,33],source_panel=[682,0,1365,768]),
              north=dict(source_roots=[[1605,223],[1765,223]],target_roots=[[344,141],[424,141]],translation=[-458.5,29.5],source_panel=[1365,0,2048,768]),
              policy='Uniformly register all extracted bone pixels and alpha together. Do not rescale the body, stretch a facing independently, or crop out body-shaped regions of the full item.')
write('registration-controls.json',controls)
now=datetime.now(timezone.utc).isoformat()
review=dict(recorded_at=now,status='PASS FOR REGISTRATION',contract=ref(HERE/'fit-contract.json'),
            evidence=ref(HERE/'refined-solid-review.png'),
            views=dict(south='Rounded broad bases meet the upper crown instead of floating outside; curls end above separate red ears.',
                       east='Root meets the upper/anterior crown. Full loop returns above the independent flesh ear; no posterior root or duplicate far horn.',
                       north='Head occludes anterior root interiors. Both flesh ears remain red below the coils, without bone-ear substitution.',
                       west='Symmetric paired item will mirror east; no separately generated west.'),
            registration_required='ImageGen enlarged the horn layout relative to the red head. Register the actual item to the fixed crown landmarks, then inspect it on the unchanged body before final fit credit.',
            red_reference_is_not_production_body=True,neutralization='Remove mild warm bone bias; preserve grayscale shading for independent native tint.')
write('first-refinement-structural-review.json',review)
write('generation-receipt.json',dict(recorded_at=now,entry=packet['entry'],tool='image_gen.imagegen',actual_calls=1,
      prompt=ref(HERE/'context-refinement-prompt.txt'),inputs=[ref(HERE/n) for n in ['manual-context-turnaround.png','source-reference-construction.png']],
      output=ref(HERE/'context-refinement-raw.png'),original_output='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-02c92c71-5a21-48fc-a64a-e9228a58b94e.png',
      transparent_background=True,output_size=list(raw.size),alpha_zero_pixels=int((a[:,:,3]==0).sum()),
      timestamp_note='recorded_at is receipt recording time; the exact tool-call timestamp is not retained here.',second_isolation_generation=False))

model=dict(item='Horns',blueprint='Horns',family='yrame',slot='Head',laterality=0,
           canvas=list(SIZE),contact=body_model['registration']['contact'],
           base_model=packet['base_body']['path'],body_sha256=packet['base_body']['sha256'],
           actual_equipped_binding=packet['actual_head_binding'],frame_mapping=body_model['registration'],
           fit_contract=ref(HERE/'fit-contract.json'),views={},
           policy='Intact independent bone; original body/head depth determines visibility. Full hidden north root interiors retained separately, not body-shaped destructive cutouts.',
           west_policy='Mirror exact east item and fixed bare anatomy; symmetric pair, same Head288/0 binding.',
           native_acceptance='Pending the full-set generation gate and integrated natural-equipment/headgear state review.')
groups={k:{} for k in ['assembly','palette','full','depth-off','ownership']}
decisions={}
for facing in FACES:
    base=Image.new('RGBA',SIZE)
    colored_body=Image.new('RGBA',SIZE)
    for row in sorted(body_model['views'][facing],key=lambda r:r['layer']):
        im=image(ROOT/row['public_file'])
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        base.alpha_composite(im)
        color=(0,150,255) if row['color_role']=='detail' else (152,135,95)
        colored_body.alpha_composite(tint(im,color))
    base.save(HERE/f'original-body-{facing}.png')
    plane=np.zeros_like(separated)
    left,top,right,bottom=controls[facing]['source_panel']
    plane[top:bottom,left:right]=separated[top:bottom,left:right]
    dx,dy=controls[facing]['translation']
    full=Image.fromarray(plane).transform(SIZE,Image.Transform.AFFINE,[2,0,-2*dx,0,2,-2*dy],Image.Resampling.BICUBIC)
    restored=0
    if facing=='north':
        manual=np.array(image(HERE/'horns-north.png'))
        full_array=np.array(full)
        head_row=next(r for r in body_model['views'][facing] if r['component']=='head')
        head=np.array(image(ROOT/head_row['public_file']))
        # Restore only occluded physical bone where the original skull is fully
        # opaque. No foreground hole is cut; head depth hides these root pixels.
        hidden=(head[:,:,3]==255)&(manual[:,:,3]>0)&(full_array[:,:,3]<manual[:,:,3])
        restored=int(hidden.sum())
        full_array[hidden]=manual[hidden]
        full=Image.fromarray(full_array)
        Image.fromarray(np.uint8(hidden)*255).save(HERE/'continued-hidden-north.png')
    full.save(HERE/f'intact-item-{facing}.png')
    fa=np.array(full)
    detail=fa.copy()
    weight=np.clip((fa[:,:,:3].mean(2)-190)/45,0,1)
    detail[:,:,3]=np.uint8(np.round(weight*255))
    detail[fa[:,:,3]<255,3]=0
    detail[detail[:,:,3]==0,:3]=0
    detail=Image.fromarray(detail)
    detail.save(HERE/f'detail-item-{facing}.png')
    neutral=Image.alpha_composite(full,detail)
    assert np.array_equal(np.array(neutral),np.array(full)), 'Neutral tint-plane split must reproduce the selected item'
    colored=Image.alpha_composite(tint(full,(152,135,95)),tint(detail,(207,192,65)))
    assembled=Image.alpha_composite(full,base) if facing=='north' else Image.alpha_composite(base,full)
    native=Image.alpha_composite(colored,colored_body) if facing=='north' else Image.alpha_composite(colored_body,colored)
    off=Image.alpha_composite(base,full)
    own=tint(full,(230,185,30) if facing=='north' else (40,165,220))
    ownership_plate=Image.alpha_composite(own,base) if facing=='north' else Image.alpha_composite(base,own)
    for group,im in [('assembly',assembled),('palette',native),('full',full),('depth-off',off),('ownership',ownership_plate)]:
        groups[group][facing]=im
        im.save(HERE/f'{group}-{facing}.png')
    rows=[]
    for component,role,path,layer in [('item-far' if facing=='north' else 'item-near','equipment',HERE/f'intact-item-{facing}.png',-.0002 if facing=='north' else .0018),
                                      ('item-far-detail' if facing=='north' else 'item-near-detail','equipment-detail',HERE/f'detail-item-{facing}.png',-.00019 if facing=='north' else .00181)]:
        row=dict(body_model['views'][facing][0]); r=ref(path)
        row.update(component=component,color_role=role,file=f'yrame-horns-v4-{component}-{facing}.png',public_file=r['path'],sha256=r['sha256'],layer=layer,equipment_key='horns@Head@0')
        row.pop('native_part',None);row.pop('mutation_anatomy',None)
        rows.append(row)
    model['views'][facing]=rows
    decisions[facing]=dict(unchanged_body=ref(HERE/f'original-body-{facing}.png'),occluded_root_pixels_restored=restored,
                            depth='item behind original head/body' if facing=='north' else 'item above original head/body',
                            extraction='Actual refined bone pixels and alpha; five connected bone components total. No body-outline or ear pixels selected.',
                            hidden_geometry='Manual root interiors only, entirely behind opaque original skull.' if facing=='north' else 'Full visible horn, including crown roots; no body-shaped clipping.')

for images in groups.values():
    images['west (mirror)']=ImageOps.mirror(images['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)


def plate(images,name,title,head_crop=False):
    height=500 if head_crop else 700
    out=Image.new('RGB',(1200,height),'#142823')
    d=ImageDraw.Draw(out)
    d.text((18,15),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im)
        if head_crop:
            if f=='east':box=(350,0,670,360)
            elif f.startswith('west'):box=(98,0,418,360)
            else:box=(224,0,544,360)
            display=bg.crop(box).resize((280,315),Image.Resampling.LANCZOS)
        else:
            display=bg.resize((280,420),Image.Resampling.LANCZOS)
        out.paste(display.convert('RGB'),(10+i*300,55))
        d.text((15+i*300,390 if head_crop else 490),f.upper(),font=font,fill='#e3cf43')
    d.text((18,height-55),'Original body/head and physical frame fixed. Natural Head288/0 item; native acceptance pending.',font=font,fill='#e5e8d8')
    out.save(HERE/name)


plate(groups['assembly'],'assembly-comparison.png','YRAME / actual refined horns on the unchanged selected bare body')
plate(groups['assembly'],'head-fit-comparison.png','CROWN ROOTS / front, right profile, back and mirrored left profile',True)
plate(groups['palette'],'independent-palette-comparison.png','NATIVE w / W bone regions; original w / B body regions remain independent')
plate(groups['full'],'full-item-comparison.png','WHOLE HORNS / root interiors retained; no destructive head-shaped cutout',True)
plate(groups['ownership'],'depth-ownership-comparison.png','DEPTH GUIDE / near cyan; rear gold; original head/ears unchanged',True)
small=Image.new('RGB',(600,390),'#142823'); d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((64,96),Image.Resampling.LANCZOS)
    small.paste(thumb,(i*150+40,20),thumb)
    enlarged=thumb.resize((128,192),Image.Resampling.NEAREST)
    small.paste(enlarged,(i*150+10,140),enlarged)
    d.text((i*150+5,360),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
write('model.json',model)
write('registration-decisions.json',dict(recorded_at=now,raw=ref(HERE/'context-refinement-raw.png'),controls=ref(HERE/'registration-controls.json'),
      selected_components=selected,views=decisions,body_files_verified_against_selected_model=True,
      neutral_base_and_detail_recompose_exactly=True,common_scale=.5,second_isolation_call=False,native_acceptance=model['native_acceptance']))
ledger=read(ROOT/'evidence/conversion-ledger.json'); entry=next(e for e in ledger['entries'] if e['id']==packet['entry'])
for step,phase,names,review_text in [
    ('imagegen_refine_in_context_on_unchanged_body','Actual contextual refinement: roots and flesh ears reviewed',['generation-receipt.json','context-refinement-raw.png','refined-solid-review.png','first-refinement-structural-review.json'],'Broad roots retain continuous crown attachment; original flesh ears remain separate. Source reference drift is corrected by explicit common-scale registration; production body is never replaced.'),
    ('retrieve_isolated_item_and_masks','Deterministic color-owned extraction and full-root registration',['register-horns.py','extracted-neutral-context.png','registration-controls.json','registration-decisions.json','full-item-comparison.png','model.json'],'Five bone components extracted without another generation. Full north root interiors restored only behind the opaque original skull. No head-shaped cutout; w/W tint planes recompose exactly to neutral. Final assembled fit review pending.')]:
    entry['process_log'].append(dict(timestamp=now,step=step,phase=phase,action=review_text,inputs=[ref(HERE/'fit-contract.json'),ref(HERE/'context-refinement-raw.png')],outputs=[ref(HERE/name) for name in names],review=review_text,result='PASS'))
entry.update(current_step='recompose_check_cuffs_attachment_occlusion_all_views',generation_ready=False,
             current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
             art_review=dict(status='REQUIRES REVIEW',reason='New actual refined horn registration on the selected bare centauroid. Inspect all root transitions, flesh ears and near/far depth before fit credit.'),
             registration_summary='v4 candidate on the current selected body: broad crown roots, separate original flesh ears, full hidden roots and shared physical scale. Final visual review pending.')
ledger['updated_at']=now
(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Registered actual refined bone and independent w/W planes on the fixed body; assembled visual review pending.')
