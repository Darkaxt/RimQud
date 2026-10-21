"""Align the fixed foot pivot with integer translations; review full body art."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'registered-v2';OUT=HERE/'registered-v3';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def im(p):return Image.open(p).convert('RGBA')
def translate(image,dx):
 out=Image.new('RGBA',image.size);out.paste(image,(dx,0));return out
assert not (OUT/'authoring-review.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='BODY-RAY-CAT';e=next(e for e in l['entries'] if e['id']==l['active_entry']);m=deepcopy(read(OLD/'model.json'));reg=read(HERE/'registered/registration-decisions.json');checks={};groups={k:{} for k in ['neutral','native','detail']}
# Midpoint of near-contact source paws, excluding tail/head. S/N use combined
# paired-paw bounds, E the mean of the two separated near-paw bounds.
source_pivots=dict(south=559.5,east=624.25,north=626.5)
centers={}
for f in ['south','east','north']:
 v=reg['views'][f];current=256+(source_pivots[f]-v['source_landmarks']['contact_x'])*v['raster_scale'];dx=int(round(256-current));centers[f]=dict(measured_source_paw_midpoint_x=source_pivots[f],old_source_contact_x=v['source_landmarks']['contact_x'],old_registered_paw_midpoint=current,integer_translation_x=dx,new_registered_paw_midpoint=current+dx,residual_from_pivot=current+dx-256)
 assert abs(centers[f]['residual_from_pivot'])<=.5
 for row in m['views'][f]:
  source=ROOT/row['public_file'];assert ref(source)['sha256']==row['sha256'];out=translate(im(source),dx);p=OUT/Path(source).name;out.save(p);row.update(file='ray-cat-'+p.name,public_file=ref(p)['path'],sha256=ref(p)['sha256'],alignment_translation=[dx,0],source_before_centering=ref(source))
 for key,name in [('neutral','recomposed-neutral'),('native','native-palette'),('detail','detail-ownership')]:
  out=translate(im(OLD/f'{name}-{f}.png'),dx);out.save(OUT/f'{name}-{f}.png');groups[key][f]=out
 expected=translate(im(HERE/'registered'/f'full-neutral-{f}.png'),dx);actual=Image.new('RGBA',(512,512))
 for row in sorted(m['views'][f],key=lambda r:r['layer']):actual.alpha_composite(im(ROOT/row['public_file']))
 assert np.array_equal(np.array(actual),np.array(expected)) and np.array_equal(np.array(actual),np.array(groups['neutral'][f]))
 assert actual.getbbox()[0]>0 and actual.getbbox()[2]<512 and actual.getbbox()[1]>0 and actual.getbbox()[3]<512
 for row in m['views'][f]:
  a=np.array(im(ROOT/row['public_file']));assert not np.ptp(a[:,:,:3].astype(int),axis=2).any();assert not a[a[:,:,3]==0,:3].any()
  assert row['contact']==[256,448] and row['size']==[512,512]
 checks[f]=dict(neutral_rgba_exact_after_integer_translation=True,original_shape_alpha_retained=True,source_physical_scale_retained=True,no_resampling_during_centering=True,all_layers_same_pivot=True,neutral_grayscale=True,empty_rgb_zero=True,no_clipped_coverage=True)
for key in groups:groups[key]['west']=ImageOps.mirror(groups[key]['east']);groups[key]['west'].save(OUT/(dict(neutral='recomposed-neutral',native='native-palette',detail='detail-ownership')[key]+'-west.png'))
m['views']['west']=[]
for row in m['views']['east']:
 p=OUT/Path(row['public_file']).name.replace('-east.png','-west.png');ImageOps.mirror(im(ROOT/row['public_file'])).save(p);m['views']['west'].append(dict(row,file='ray-cat-'+p.name,public_file=ref(p)['path'],sha256=ref(p)['sha256'],already_mirrored_from_east=True))
assert np.array_equal(np.array(groups['neutral']['west']),np.array(ImageOps.mirror(groups['neutral']['east'])))
now=datetime.now(timezone.utc).isoformat();write(OUT/'centering-decisions.json',dict(recorded_at=now,source_registration=ref(HERE/'registered/registration-decisions.json'),method='Alpha>128 paw bounds in the last45 source pixels, excluding tail. Stable pair midpoint; integer whole-frame translations only. Per-facing resolution calibration/physical size is unchanged, no independent bounding-box scale.',views=centers,west='Mirror corrected east once. All body/head/tint pixels move together; source PNGs remain untouched.'))
m.update(centering=ref(OUT/'centering-decisions.json'),supersedes=ref(OLD/'model.json'));write(OUT/'model.json',m)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for key,name,title in [('neutral','assembly-comparison.png','RAY CAT / source shape and physical size retained; paired feet centered'),('native','native-palette-comparison.png','NATIVE m COAT / separate y PALE DETAILS; shared physical frame'),('detail','detail-comparison.png','DETAIL OWNERSHIP / exact same source shading and alpha')]:
 out=Image.new('RGB',(1200,440),'#142823');d=ImageDraw.Draw(out);d.text((15,15),title,font=font,fill='#e3cf43')
 for i,f in enumerate(['south','east','north','west']):
  bg=Image.new('RGBA',(512,512),'#20382d');bg.alpha_composite(groups[key][f]);out.paste(bg.resize((280,280),Image.Resampling.LANCZOS).convert('RGB'),(10+i*300,55));d.line((150+i*300,55,150+i*300,335),fill='#b2a94d');d.line((10+i*300,300,290+i*300,300),fill='#6b9d8a');d.text((15+i*300,360),f.upper(),font=font,fill='#e3cf43')
 d.text((15,407),'Preserved accepted design. Current ownership/registration only; native acceptance pending.',font=font,fill='#e5e8d8');out.save(OUT/name)
small=Image.new('RGB',(800,360),'#142823');d=ImageDraw.Draw(small)
for j,key in enumerate(['neutral','native']):
 for i,f in enumerate(['south','east','north','west']):
  img=groups[key][f].resize((64,64),Image.Resampling.LANCZOS);small.paste(img,(15+i*200,15+j*170),img);zoom=img.resize((128,128),Image.Resampling.NEAREST);small.paste(zoom,(75+i*200,15+j*170),zoom);d.text((15+i*200,150+j*170),f.upper(),font=font,fill='#e3cf43')
small.save(OUT/'game-scale-review.png')
reason='Inspected actual accepted source views and recovered north patch, manual anatomy/ownership plan, shared-frame neutral/native and intended-size plates. Compact feline cardinal views preserve four-foot/tail anatomy with natural pair overlap; north has no face and tail joins lower rump separately from skull. New body/head/tint layers reconstruct source grayscale and alpha exactly. Mathematical material partition corrects rejected opaque-only filter. Paw-midpoint integer shifts center the body without scaling, warping or clipping. No new ImageGen call or new species/mutation geometry.'
write(OUT/'authoring-review.json',dict(recorded_at=now,status='PASS',scope='Generation authoring only',reason=reason,checks=checks,source_history=ref(HERE/'historical-generation-provenance.json'),manual_plan=ref(HERE/'manual-ownership-controls.json'),centering=ref(OUT/'centering-decisions.json'),detail_partition=ref(OLD/'opaque-filter-rejection.json'),
 per_view=dict(south='Front feline head/paws low in donor map view; tail rises behind body. Compact face and paired fore paws are preserved; far hind pair occluded.',east='Complete right profile; head right, tail rooted at rump left, near paws at contact. Far paws overlap; no human template.',north='Rear skull and back of ears only. Tail root at lower rump and outside flank with transparent gap from skull; rear paws visible.',west='One exact east mirror for body/head/detail; no independent scaling or drawing.'),
 limitations=['Selected accepted art was historically generated before the current manual ownership plan. The report records this chronology and does not invent a past manual input.','Current pale muzzle/bib and sparse glass-detail placement are authored palette interpretation, not additional native anatomy.','Native age/size and active mutation state are unknown; no demographic or simulation change.','Independent head/tint behavior, look, palette changes, actual native facing and visibility await the full-generation gate.']))
write(HERE/'artifact-manifest.json',dict(recorded_at=now,entry=e['id'],artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
for step,names in [('register_required_layers_and_color_masks',['model.json','centering-decisions.json','detail-comparison.png']),('visual_review_anatomy_orientation_palette_all_views',['assembly-comparison.png','native-palette-comparison.png','game-scale-review.png','authoring-review.json'])]:
 e['process_log'].append(dict(timestamp=now,step=step,action=reason,inputs=[ref(HERE/'source-packet.json')],outputs=[ref(OUT/n) for n in names]+([ref(HERE/'artifact-manifest.json')] if step.startswith('visual_review') else []),review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_body_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')),current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'assembly-comparison.png')),registration_summary=reason)
n=next(x for x in l['entries'] if x['id']=='NPC-CTESIPHUS');assert not n.get('generation_ready');n.update(status='IN PROGRESS',current_step='resolve_individual_race_and_runtime_metadata');l.update(active_entry=n['id'],updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Ray Cat generation-ready with preserved design and exact alpha/tint split. NPC-CTESIPHUS is sole active entry.')
