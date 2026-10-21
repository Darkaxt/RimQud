"""Close Yrame's separate leg-art generation only and return to actual outfit assembly."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='BODY-YRAME' and ledger['stage']=='Stage 3 ACTIVE'
entry=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME');npc=next(e for e in ledger['entries'] if e['id']=='NPC-WARDEN-YRAME')
model=read(OUT/'model.json');packet=read(HERE/'source-packet.json');base=read(ROOT/packet['baseline']['path']);receipts=read(HERE/'generation-receipts.json')
parts=packet['captured_actor']['parts'];feet=[p for p in parts if p['type']=='Feet']
assert len([p for p in parts if p['type']=='Arm'])==2 and len([p for p in parts if p['type']=='Hand'])==2
assert [(p['id'],p['laterality'],p['manager']) for p in feet]==[(297,16,'515::MultipleLegs::Change'),(298,64,'515::MultipleLegs::Add')]
assert feet[0]['equipped']['instance']==580 and feet[1]['equipped'] is None
assert receipts['new_calls']==2 and len(receipts['actual_calls'])==2
verified=set()
def walk(v):
    if isinstance(v,dict):
        key='path' if 'path' in v else ('public_file' if 'public_file' in v else None)
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,packet,receipts]:walk(v)
assert not model['native_activation'] and model['baseline_model']==packet['baseline']
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];color=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8)
for f,rows in model['views'].items():
    source='east' if f=='west' else f
    assert len(rows)==3
    for component in ['body','head']:
        row=next(r for r in rows if r['component']==component);old=next(r for r in base['views'][source] if r['component']==component)
        im=Image.open(ROOT/old['public_file']).convert('RGBA');im=ImageOps.mirror(im) if f=='west' else im
        assert np.array_equal(np.array(im),rgba(ROOT/row['public_file']))
        for k in ['size','contact','width','height','center_x','center_z']:assert row[k]==old[k]
    extra=next(r for r in rows if r['component']=='mutation-extra-legs')
    assert (extra['native_part'],extra['parent_part'],extra['manager'],extra['baseline_feet_group'])==(298,287,'515::MultipleLegs::Add',297)
    assert extra['mirrored_from_east']==(f=='west')
    neutral=Image.new('RGBA',(512,1024));native=Image.new('RGBA',(512,1024))
    for r in rows:
        a=rgba(ROOT/r['public_file']);assert a.shape==(1024,512,4) and r['contact']==[256,950]
        assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2])
        assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any()
        neutral.alpha_composite(Image.fromarray(a));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;native.alpha_composite(Image.fromarray(a))
    assert np.array_equal(np.array(neutral),rgba(OUT/f'neutral-{f}.png')) and np.array_equal(np.array(native),rgba(OUT/f'native-{f}.png'))
    if f in ['south','north']:
        # A horizontal slice through the forefeet demonstrates four separated contours.
        xs=np.flatnonzero(np.array(neutral)[930,:,3]>128);runs=np.split(xs,np.flatnonzero(np.diff(xs)>1)+1);assert len([r for r in runs if len(r)])==4
assert np.array_equal(rgba(OUT/'extra-legs-west.png'),np.array(ImageOps.mirror(Image.open(OUT/'extra-legs-east.png').convert('RGBA'))))
now=datetime.now(timezone.utc).isoformat()
reason=('Inspected original w/B glyph and full native description/body tree, actual Core female directional references, unchanged reusable base, editable front/profile/back construction, both actual ImageGen outputs, patched feet and final four-view neutral/native/component/intended-size plates. '
        'Two plural Feet groups with Mobility2 and native hind/foreleg prose support four physical feet; level6 is not six appendages. Original two arms/hands/head/body and paired baseline legs remain exact. '
        'Additional leg pair is a separate texture bound as art to added Feet298/64, parent Body287, manager515::MultipleLegs::Add. Changed Feet297/16 retains Boots580; added group remains unequipped. Horns575 remain separate equipment, not baseline anatomy. '
        'Both generated proposals preserve four-foot anatomy but redraw baseline pixels. Keep only measured neutral surface range in fixed editable added-leg gradients; no generated baseline replacement or AI isolation. '
        'Rounded feet and subtle toe curves retained. Final12px outward spacing in front/back separates toe silhouettes without changing body, contact, leg lengths, physical frame or accepted profiles; previous registration retained. '
        'Neutral RGB is grayscale. Native body preview uses captured tileColor w. B detail remains documented but has no guessed permanent-skin region; icy/rime cosmetics and natural Icy Vapor effect are outside the initial body phase. '
        'West mirrors the symmetric east body/leg geometry. No new human race, centaur/horse anatomy, general mutation framework, gear, fixed skin color, personal cosmetics or native activation. Actual four-item Yrame assembly and full native acceptance remain unfinished.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Separate Yrame additional-leg generation only',reason=reason,verified_source_files=len(verified),
    checks=dict(two_native_paired_feet_groups=True,four_separate_front_back_foot_contours=True,unchanged_source_body_head_RGBA=True,one_additional_leg_pair_separate=True,
    actual_boots297_not_duplicated_to298=True,horns_remain_equipment=True,exact_original_frame_scale_contact=True,neutral_equal_RGB=True,captured_w_tint_independent=True,B_detail_unassigned_explicitly=True,
    west_mirror_supported=True,two_actual_imagegen_outputs_retained=True,manual_geometry_and_surface_mapping_disclosed=True,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][4],'Run actual composed ImageGen refinement after editable foot patches, then inspect structural invariants.',['composed-refinement-prompt.txt','patched-turnaround.png','source-reference-baseline.png'],['composed-refinement-raw.png','composed-structural-review.json','generation-receipts.json'],'Four-foot anatomy remains coherent. Baseline redraw and changed profile spacing rejected; useful neutral surface range retained. No third prompt loop or generated-body isolation.')
event(entry['required_steps'][5],'Register exact source body/head and separate additional leg pair; correct final front/back toe clearance without source rescaling.',['source-packet.json','manual-corrections.json','composed-structural-review.json'],['register-yrame.py','source-palette-roles.json','registered/model.json','registered/registration-decisions.json','registered/extra-legs-comparison.png','registered/extra-legs-alpha-comparison.png','separate-foot-contours.py','foot-clearance-correction.json','registration-before-foot-clearance.png'],'Original RGBA, world dimensions and ground unchanged. Front/back added pair moves outward12px to avoid merged forefeet; accepted profile unchanged. Editable west geometry and bitmap both face left. Native B retained without guessed skin mask.')
event(entry['required_steps'][6],'Inspect all four complete anatomy/component/palette views and intended-size silhouettes.',['registered/model.json'],['registered/neutral-comparison.png','registered/native-comparison.png','registered/game-scale-comparison.png','record-review.py','registered/authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Keep real native body/part/equipment/visibility/hurt/look/save acceptance behind the full-generation gate.',['registered/model.json'],[],'No native activation or game/harness run. Complete actual four-item NPC assembly next; body remains UNFINISHED pending integrated native acceptance.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-comparison.png')),
    registration_summary='Yrame515 source-exact shared female body/head with one separate added human leg pair. Four foot contours, captured Feet297/298 managers, source frame/contact and independent neutral/native metadata retained. Boots and horns remain separate actual items; native acceptance pending.',
    art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
assert npc['status']=='UNFINISHED' and not npc.get('generation_ready')
npc.update(status='IN PROGRESS',current_step=npc['required_steps'][1],known_issues=['Separate BODY-YRAME is generation-ready. Assemble actual mail, horns, blade and Boots580 only on changed Feet297; added Feet298 remains unequipped. Respect horn near/far ownership and unchanged source-body frame.'])
npc['advancement_blocker']['reason']=npc['known_issues'][0];npc['advancement_blocker']['resolution']='Finish four-item source-bound assembly with correct horn depth and single booted Feet group; preserve source slots and keep native state acceptance gated.'
ledger.update(active_entry=npc['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_source_files=len(verified),native_acceptance='pending')))
