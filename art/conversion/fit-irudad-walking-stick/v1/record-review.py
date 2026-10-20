"""Record walking-stick generation evidence without claiming mutation integration."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male-older/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
assert not (HERE/'authoring-review.json').exists()
model=json.loads((HERE/'model.json').read_text());a=np.array(read(HERE/'intact-canonical.png'));pattern=np.array(read(HERE/'constructed-canonical.png'))
assert np.array_equal(a[:,:,3],pattern[:,:,3]) and a[453,220,3]==0,'Crook return remains open.'
assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2])
part=model['actual_equipped_binding']['part'];assert part['id']==201 and part['parent']==200 and part['laterality']==6 and part['manager']=='507::MultipleArms::Change'
checks={}
for f,rows in model['views'].items():
    body=read(BODY/f'selected-{f}.png');item=read(HERE/f'intact-item-{f}.png');detail=read(HERE/f'item-detail-{f}.png');hand=read(HERE/f'original-hand-{f}.png');equipment=Image.alpha_composite(item,detail)
    expected=Image.alpha_composite(equipment,body) if f=='north' else Image.alpha_composite(Image.alpha_composite(body,equipment),hand)
    assert np.array_equal(np.array(expected),np.array(read(HERE/f'assembled-{f}.png')))
    b=np.array(body);h=np.array(hand);visible=h[:,:,3]>0;assert np.array_equal(b[visible,:3],h[visible,:3])
    for row in rows:assert ref(ROOT/row['public_file'])['sha256']==row['sha256'] and row['contact']==[256,950] and row['size']==[512,1024]
    checks[f]=dict(original_body_and_palm=True,exact_recomposition=True,full_crook_and_stalk_retained=True,source_mutation_binding_preserved=True,actual_mutation_attachment_accepted=False)
reason=('Inspected complete dried brinestalk/crook, unobstructed return, stalk continuity, original-palm depth, SEN/mirrored west, source w/g palette and intended-size appearance. One actual contextual refinement supplies neutralized wood surface; hidden grip completed before depth, original alpha/ink/body retained. Actual Hand201/6 under Arm200 with MultipleArms::Change is preserved verbatim. Ordinary older-body palm is only an authoring compatibility proxy, not mutation attachment acceptance. Stationary support grip is near crook; ready horizontal weapon presentation and individual Irudad assembly remain pending.')
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',scope='Generation authoring only',reason=reason,checks=checks,structural_gate=ref(HERE/'first-refinement-structural-review.json'),new_imagegen_calls=1,second_isolation_call=False,native_acceptance=model['native_acceptance'])
write(HERE/'authoring-review.json',review);write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
path=ROOT/'evidence/conversion-ledger.json';d=json.loads(path.read_text());ident='FIT-IRUDAD-WALKING-STICK-HAND-6';assert d['active_entry']==ident;e=next(e for e in d['entries'] if e['id']==ident)
for step,action,names in [
 ('retrieve_isolated_item_and_masks','Select the same contextual wood luminance into complete fixed crook/stalk alpha; complete hidden grip and retain separate source g accent without a second isolation call.',['register-stick.py','registration-decisions.json','full-item-comparison.png','canonical-continuation.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Recompose original older body with complete cane and original palm/body depth; retain exact mutation binding separately from baseline proxy.',['model.json','assembly-comparison.png','depth-off-comparison.png','grip-comparison.png']),
 ('review_game_scale_and_palette','Inspect source w/g roles, authored walking-cane size and all cardinal display views at intended size; no native mutation/state acceptance.',['independent-palette-comparison.png','game-scale-review.png','authoring-review.json','artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'refined-red-context.png'),ref(HERE/'first-refinement-structural-review.json')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),registration_summary='Dried brinestalk crook and full shaft, separate w/g native roles, unchanged ordinary older base and original-palm depth. Actual mutation-managed Hand201/6 retained; baseline palm is a display proxy, native mutation/pose and Irudad assembly unfinished.',native_acceptance=model['native_acceptance'])
next_id='ITEM-WALKING-STICK';next_e=next(e for e in d['entries'] if e['id']==next_id);next_e.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette');d.update(active_entry=next_id,updated_at=review['timestamp']);assert [e['id'] for e in d['entries'] if e['status']=='IN PROGRESS']==[next_id];write(path,d)
print('Walking-stick art generation-ready, mutation attachment not accepted; item aggregate is sole active entry.')
