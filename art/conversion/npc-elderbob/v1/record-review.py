"""Record Irudad's inspected four-item static assembly; native state review remains gated."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def arr(p):return np.array(Image.open(p).convert('RGBA'))
assert not (HERE/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='NPC-ELDERBOB'
entry=next(e for e in ledger['entries'] if e['id']=='NPC-ELDERBOB')
model=read(HERE/'model.json');packet=read(HERE/'assembly-source-packet.json');lineage=read(HERE/'dependency-lineage.json')
verified=set();historical=[]
old={('skills/qud-creature-conversion/SKILL.md','74d6f7498dad0e0079c152649b2b40143cbf201a748b48d0a5cd110a73975af2'),('skills/qud-creature-conversion/references/apparel-fitting.md','3549a1e4702f4b24dfcea5238880d092ef84a5809bd07bdcb6ececbf601f1f13')}
def walk(v):
    if isinstance(v,dict):
        key='path' if 'path' in v else ('public_file' if 'public_file' in v else None)
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p;actual=hashlib.sha256(p.read_bytes()).hexdigest()
            if actual!=v['sha256']:
                rel=p.relative_to(ROOT).as_posix();assert (rel,v['sha256']) in old,(str(p),actual,v['sha256'])
                commit='dde9ca991c35ddef2b47a970a571d696ee0443bb';assert hashlib.sha256(subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT)).hexdigest()==v['sha256']
                record=dict(path=rel,sha256=v['sha256'],commit=commit,current_sha256=actual,url='https://github.com/Darkaxt/RimQud/blob/'+commit+'/'+rel)
                if record not in historical:historical.append(record)
            verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,packet,lineage]:walk(v)
expected={'Black Robes':(539,196,'Body',0),'Spectacles':(540,198,'Face',0),'Walking Stick':(541,201,'Hand',6),'Sandals':(546,213,'Feet',0)}
assert {name:(b['equipped_instance'],b['part_id'],b['slot'],b['laterality']) for name,b in model['equipment_bindings'].items()}==expected
assert model['registration']['canvas']==[512,1264] and model['registration']['contact']==[256,1190]
assert not model['native_activation'] and not packet['native_activation']
body=read(ROOT/model['body_model']['path'])
for f,view in model['views'].items():
    assert view['body']==body['views'][f]
    canvas=Image.new('RGBA',(512,1264))
    for r in view['body']:canvas.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    assert np.array_equal(np.array(canvas),arr(HERE/f'base-{f}.png'))
    for b in view['equipment']:
        for r in b['components']:
            a=Image.open(ROOT/r['public_file']).convert('RGBA');original=Image.open(ROOT/r['source_component']['path']).convert('RGBA')
            if r['mirrored_from_east']:original=ImageOps.mirror(original)
            assert np.array_equal(np.array(a)[240:],np.array(original)) and not np.array(a)[:240].any()
            assert r['size']==[512,1264] and r['contact']==[256,1190]
            oldheight=r['height']*1024/1264;oldcenter=r['center_z']-120*oldheight/1024
            assert abs((r['center_z']+(632-1190)*r['height']/1264)-(oldcenter+(512-950)*oldheight/1024))<1e-12
    neutral=arr(HERE/f'full-neutral-{f}.png');assert np.array_equal(neutral[:,:,0],neutral[:,:,1]) and np.array_equal(neutral[:,:,1],neutral[:,:,2])
    assert not arr(HERE/f'hidden-{f}.png')[:,:,3].any()
decision=read(HERE/'hand-attachment-decision.json');assert decision['captured_part']==201 and decision['laterality']==6 and decision['captured_item']==541
now=datetime.now(timezone.utc).isoformat();write(HERE/'historical-instruction-versions.json',dict(verified=historical,rule='Original dependency events stay unchanged; these exact historical instruction bytes resolve in Git.'))
reason=('Inspected actual original source, metadata, separate body/mutation dependencies, every single item on the unclothed named body, staged assembly, all four full neutral/native views and intended-size evidence. '
        'Black Robes539 Body196, Spectacles540 Face198, Walking Stick541 changed Hand201/6 and Sandals546 Feet213 match the captured outfit. '
        'Current separate four-arm/hands-face/tail body and all item pixels remain unchanged; integer240px padding aligns old fittings to the larger named-body frame without altering physical scale, contact or masks. '
        'Robe coverage hides the tail root naturally while its full texture and exposed barbs remain independent. Local late body ownership preserves original hands without redrawing body over unrelated gear. '
        'Actual r/w body, K/K robe, y/Y spectacles, w/g stick and y/w sandals have independent palette roles; neutral bases remain gray. '
        'The existing static palm is explicitly associated with captured Hand201/6, without renaming the slot or treating grouped Hands/Face metadata as render bones. '
        'This is a disclosed fixed art choice, not native articulation or accepted resting/ready behavior; those remain at integrated Stage3 after full generation. '
        'No new ImageGen call, baked costume, mutation framework, game launch or native acceptance. Full input histories and two exact older instruction versions are retained.')
write(HERE/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete captured four-item static authoring assembly only',reason=reason,checked_dependency_files=len(verified),
    checks=dict(exact_four_equipped_instances_and_parts=True,current_separate_anatomy_reused=True,all_four_cardinal_views=True,all_single_item_views_reviewed=True,source_pixels_unchanged=True,
    padding_preserves_world_frame=True,per_item_late_ownership=True,neutral_equal_RGB=True,independent_captured_palettes=True,hand201_6_not_renamed=True,authored_static_anchor_disclosed=True,hidden_preview_empty=True,new_imagegen_calls=0,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][0],'Reconcile current actor507 anatomy, source palette and four equipped items after the separate mutation-art prerequisite was generated.',[],['assembly-source-packet.json','render-source-comparison.py','source-to-assembly.png'],'The original preflight remains history; current packet uses BODY-IRUDAD separate anatomy and exact actual item parts. No new race, invented age/mutation or profession costume.')
event(entry['required_steps'][1],'Verify all five current dependencies and retain actual source/reference/manual/refinement/secondary/patch/extraction histories.',['assembly-source-packet.json'],['dependency-lineage.json','dependency-evidence.html','historical-instruction-versions.json'],'Current model/component hashes verified. Older instruction inputs resolve to exact Git dde9ca9 bytes rather than being silently rehashed. No new generation call was required.')
event(entry['required_steps'][2],'Assemble all four source items with separate body/mutation textures and integer-padded original fittings.',['assembly-source-packet.json','dependency-lineage.json'],['assemble-irudad.py','preserve-padding-pixels.py','padding-correction.json','model.json','hand-attachment-decision.json','assembly-stages.png'],'Full body/item geometry and source slot binding unchanged. Exact integer RGBA paste preserves even hidden source RGB, correcting blank-canvas compositing without a visible/alpha change. The existing lower-in-image static palm is an explicit render-art association for Hand201/6, not a renamed lower mechanical hand or source-inferred bone. Native pose/state review remains separate.')
event(entry['required_steps'][3],'Review each item independently on the unclothed named body, then the complete outfit in every facing.',['model.json'],['black-robes-comparison.png','spectacles-comparison.png','walking-stick-comparison.png','sandals-comparison.png','full-neutral-comparison.png'],'Robe shoulder/cuff/hem, ordinary head spectacles, source hand grip, sandal height and tail/raised-arm occlusion visually inspected. Full cloth and tail retained, each item applies only its own original-body coverage at final composition; no unrelated body redraw.')
event(entry['required_steps'][4],'Review exact independent source palettes, shared registration and intended-size static assembly.',['model.json'],['full-native-comparison.png','game-scale-comparison.png','hidden-comparison.png','record-review.py','authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][5],'Retain integrated native anatomy/equipment/held-state/visibility/hurt/look/save review behind all-generation gate.',['model.json'],[],'Authoring hidden previews are empty; native behavior is untested. Actual Hand201/6 near/far, resting/ready grip/angle/state mapping and dynamic mutation/equipment semantics remain required integrated Stage3 work. Entry remains UNFINISHED.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'full-neutral-comparison.png')),
    registration_summary='Captured Irudad507: current separate older-human/mutation body plus Black Robes, Spectacles, Walking Stick and Sandals. All source pixels and physical scale/contact are retained through integer padding. Hand201/6 keeps its captured identity with an explicit static-art palm association; native articulation/held-state acceptance remains pending.',art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')))
entry['resolved_advancement_blocker']=dict(**entry.pop('advancement_blocker'),status='RESOLVED FOR GENERATION',evidence=[ref(HERE/'model.json'),ref(HERE/'hand-attachment-decision.json')])
entry['apparel_dependencies']['status']='Current robe, spectacles and sandals generation-ready; exact padded source pixels verified on separate named anatomy. Native outfit acceptance pending.'
next_entry=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert next_entry['id']=='NPC-JOPPAFARMERCONVERT'
next_entry.update(status='IN PROGRESS',current_step=next_entry['required_steps'][0]);ledger.update(active_entry=next_entry['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_dependency_files=len(verified),native_acceptance='pending')))
