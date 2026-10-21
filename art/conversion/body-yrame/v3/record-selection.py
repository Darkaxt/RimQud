"""Record the actual user inputs, one refinement and inspected body registration."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered-v2'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='BODY-YRAME'
entry=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME')
model=read(OUT/'model.json');decisions=read(OUT/'registration-decisions.json')
base=ROOT/model['baseline_model']['path'];assert ref(base)==model['baseline_model']
for face,rows in model['views'].items():
    for r in rows:
        p=ROOT/r['public_file'];assert ref(p)['sha256']==r['sha256']
        a=np.array(Image.open(p).convert('RGBA'));assert (a[:,:,0]==a[:,:,1]).all() and (a[:,:,1]==a[:,:,2]).all()
        assert r['size']==[768,1152] and r['contact']==[384,1050]
    assert all(r['width']==model['registration']['width'] and r['height']==model['registration']['height'] for r in rows)
receipt=dict(tool='built-in image_gen.imagegen',actual_codex_calls=1,transparent_background=True,
    prompt=ref(HERE/'composed-refinement-prompt.txt'),
    referenced_images=[ref(HERE/'user-sheep-turnaround.png'),ref(HERE/'source-reference-alternatives.png')],
    output=ref(HERE/'composed-refinement-raw.png'),original_generated_filename='exec-3a1c26c1-1a82-4194-95e6-f7570d6a68cd.png',
    user_generations='Both original alternatives were supplied by the user. Their generation receipts/exact upload files are unknown; they are not counted as Codex tool calls.')
write(HERE/'generation-receipt.json',receipt)
reason=('Selected the user-created sheep-centauroid body plan and one actual contextual refinement. '
        'Continuous horizontal lower trunk replaces the rejected visible biped pelvis plus posterior extra pair. '
        'Forelegs sit beneath the upright torso/front trunk and hindlegs beneath the rear mass. '
        'Four hooves are distinct in south; the east far foreleg overlaps naturally and north forefeet are occluded by the hind pair. '
        'No extra legs are invented to make all four visible in every facing. Fleece is quieter, tail removed, blank head/two arms retained. '
        'Compact sheep-like coat and cloven hooves are explicitly authored interpretation, not a native sheep race. '
        'Actual Core human/sheep/horse assets supply only their documented rendering/mass roles. '
        'Neutral RGB is grayscale; w upper body/arms/head and B lower-body regions are separate tint planes on one logical body transform. '
        'Arm/hand ownership is retained; no frozen blue coat is baked into albedo. '
        'Shared768x1152 frame/contact384,1050 and common head-calibrated physical scale preserve the selected geometry across cardinal views. '
        'The head cut now lies inside the neck strip; initial shoulder-corner extraction is preserved as rejected registration. '
        'Recomposition RGB error0 and alpha error<=1. Saved alpha is genuinely transparent; remote low-alpha noise is removed, not the actual contour. '
        'Ordinary human female source remains unchanged. Horns575, mail574, boots580 and blade576 are absent and remain unfinished fitting work. '
        'Boots580 apply only to fore Feet297/16; added hind Feet298/64 is unequipped. No articulated limb nodes, mutation framework, game launch or native acceptance.')
write(OUT/'authoring-review.json',dict(status='PASS',scope='Generation-time art authoring only',reason=reason,
    inspected=['Original sprite and full metadata','Both supplied user alternatives','Actual directional Core reference images',
               'Actual refinement on opaque green background','Neutral/native and body/head/tint component plates in all facings',
               'Intended-size64x96 authoring thumbnails','Corrected head/neck split'],
    initial_registration=ref(HERE/'registered/model.json'),selected_registration=ref(OUT/'model.json'),
    initial_head_issue='Horizontal split at source225/224/225 included small shoulder corners; final211/205/210 stays in the neck strip.',
    native_acceptance='DEFERRED UNTIL ALL GENERATED'))
# Compare the old and new profile at the same world/pixel scale, not fitted bounds.
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
plate=Image.new('RGB',(1152,740),'#142823');d=ImageDraw.Draw(plate)
d.text((18,16),'YRAME / anatomy correction / common physical scale and ground',font=font,fill='#e3cf43')
for x,label,mp,ip in [(280,'SUPERSEDED BIPED + PAIR',HERE.parent/'v1/registered/model.json',HERE.parent/'v1/registered/neutral-east.png'),
                       (850,'SELECTED CENTAUROID',OUT/'model.json',OUT/'neutral-east.png')]:
    m=read(mp);r=m['views']['east'][0];im=Image.open(ip).convert('RGBA');unit=r['height']/r['size'][1];scale=365*unit
    resized=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    px=round(x-r['contact'][0]*scale);py=round(610-r['contact'][1]*scale);plate.paste(resized,(px,py),resized)
    d.line((x-250,610,x+250,610),fill='#79aaa0');d.text((x-220,655),label,font=font,fill='#e3cf43')
d.text((18,710),'Old body rejected. New body has a lower trunk supporting fore/hind legs; horn and gear fits remain pending.',font=font,fill='#e5e8d8')
plate.save(HERE/'before-after-anatomy.png')
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
now=datetime.now(timezone.utc).isoformat()
def event(step,action,ins,outs,review,result='PASS'):
 entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(p) for p in ins],outputs=[ref(p) for p in outs],review=review,result=result))
event(entry['required_steps'][4],'Execute and inspect one actual composed refinement of the user-selected compact centauroid direction.',
      [HERE/'user-sheep-turnaround.png',HERE/'source-reference-alternatives.png',HERE/'composed-refinement-prompt.txt'],
      [HERE/'generation-receipt.json',HERE/'composed-refinement-raw.png',HERE/'raw-composite-east.png'],
      'Actual saved RGBA has transparent background; gray halo was hidden RGB. Horizontal trunk and fore/hind attachments preserved, tail removed and fleece reduced. Retained full output and exact input/prompt provenance.')
event(entry['required_steps'][5],'Register common physical frame, recover only actual figure alpha and split body/head plus separate source tint roles.',
      [HERE/'composed-refinement-raw.png',HERE/'source-packet.json'],
      [HERE/'register-body-initial.py',HERE/'registered/model.json',HERE/'registered/head-comparison.png'],
      'Initial head boundary includes small shoulder corners; registration retained as rejected extraction experiment. Neutral recomposition itself remains intact.',result='REQUIRES REWORK')
event(entry['required_steps'][5],'Move head boundary into neck strip and retain the same body geometry and w/B ownership.',
      [HERE/'registered/model.json',HERE/'composed-refinement-raw.png'],
      [HERE/'register-body.py',HERE/'lower-body-ownership-south.svg',HERE/'lower-body-ownership-east.svg',HERE/'lower-body-ownership-north.svg',
       OUT/'model.json',OUT/'registration-decisions.json',OUT/'head-comparison.png',OUT/'body-foreground-comparison.png',OUT/'body-detail-comparison.png'],
      'Selected registration retains exact refined shape apart from remote low-alpha noise. Shared frame and one physical scale; no new arm/leg nodes. Separate tint planes reconstruct original neutral pixels to RGB0/alpha<=1; ordinary race source unchanged.')
event(entry['required_steps'][6],'Inspect corrected anatomy, orientations, neutral/native tint, components and intended-size previews.',
      [OUT/'model.json'],[OUT/'neutral-comparison.png',OUT/'native-comparison.png',HERE/'before-after-anatomy.png',OUT/'authoring-review.json',HERE/'record-selection.py',HERE/'artifact-manifest.json'],reason)
event(entry['required_steps'][-1],'Defer native body/mutation, equipment, visibility and lifecycle acceptance until the entire generation set is ready.',
      [OUT/'model.json'],[],'Generation-ready art is not native acceptance. Reopened Yrame equipment fits and assembly remain unfinished.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],
    current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-comparison.png')),
    registration_summary='Selected sheep-like centauroid interpretation from user-supplied turnaround plus one actual refinement. Shared stance pivot/scale, real alpha, independent upper w/lower B tint, bare body/head only. Ordinary human base unchanged; all Yrame equipment refitting and native acceptance remain pending.',
    art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
next_entry=next(e for e in ledger['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0')
assert not next_entry['generation_ready'];next_entry['status']='IN PROGRESS';next_entry['current_step']=next_entry['required_steps'][0]
ledger['active_entry']=next_entry['id'];ledger['updated_at']=now
assert [e['id'] for e in ledger['entries'] if e['status']=='IN PROGRESS']==[ledger['active_entry']]
write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Selected corrected BODY-YRAME generation-ready art; native acceptance pending. Sole next active entry: ram-horn fit. Ready count:',sum(bool(e.get('generation_ready')) for e in ledger['entries']))
