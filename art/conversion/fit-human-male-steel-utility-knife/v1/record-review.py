"""Record the inspected male knife fit, shared refinement and rear correction."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-steel-utility-knife/v1';BODY=ROOT/'art/conversion/body-human-male/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,data):p.write_bytes((json.dumps(data,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
model=json.loads((HERE/'model.json').read_text());metadata=json.loads((HERE/'weapon-metadata.json').read_text());bm=json.loads((BODY/'model.json').read_text());fb=json.loads((ROOT/'art/conversion/body-human-female/v2/model.json').read_text())
for name in ['constructed-canonical.png','intact-canonical.png','handle-canonical.png']:
    assert (HERE/name).read_bytes()==(SOURCE/name).read_bytes(),name
for axis in ['width','height']:assert abs(bm['views']['south'][0][axis]*model['item_raster_scale']-fb['views']['south'][0][axis])<1e-12
checks={}
for facing,rows in model['views'].items():
    body=read(BODY/f'selected-{facing}.png');item=read(HERE/f'intact-item-{facing}.png');detail=read(HERE/f'item-detail-{facing}.png');hand=read(HERE/f'original-hand-{facing}.png')
    a=np.array(item);assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2])
    equipment=Image.alpha_composite(item,detail)
    expected=Image.alpha_composite(equipment,body) if facing=='north' else Image.alpha_composite(Image.alpha_composite(body,equipment),hand)
    assert np.array_equal(np.array(expected),np.array(read(HERE/f'assembled-{facing}.png')))
    b=np.array(body);h=np.array(hand);visible=h[:,:,3]>0;assert np.array_equal(b[visible,:3],h[visible,:3])
    for row in rows:
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        assert row['contact']==[256,950] and row['size']==[512,1024]
    unobscured=int(((a[:,:,3]>128)&(b[:,:,3]<128)).sum())
    if facing=='north':assert unobscured>0,'Rear display must retain readable blade beyond original arm.'
    checks[facing]=dict(original_body_and_palm_preserved=True,neutral_item=True,exact_recomposition=True,registered_hashes_match=True,unobscured_item_pixels=unobscured,contact=[256,950])
reason='Inspected source comparison, full item, palm close-ups, strict SEN/mirrored west, native c/Y/y colors, intended-size and cross-body scale. Identical canonical knife geometry/material reused; male scale compensates world mapping instead of enlarging the knife. Lower grip retained. North display angle corrected from-15 to-40 so blade is readable beyond rear arm, preserving failed initial preview. No new ImageGen call, body redraw, narrative painting or native ready/resting acceptance.'
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',scope='Authoring only',reason=reason,checks=checks,shared_canonical=ref(SOURCE/'intact-canonical.png'),shared_refinement=ref(SOURCE/'refined-red-context.png'),shared_prompt=ref(SOURCE/'imagegen-prompt.txt'),new_imagegen_calls=0,handedness='Source one-hand base declaration; runtime actor slot-demand remains null.',native_acceptance=model['native_acceptance'])
write(HERE/'authoring-review.json',review)
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
f=ROOT/'evidence/conversion-ledger.json';d=json.loads(f.read_text());ident='FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2';assert d['active_entry']==ident
e=next(e for e in d['entries'] if e['id']==ident)
for step,action,outputs in [
 ('source_identity_description_slot_laterality','Resolve actual Argyve519 item588 on ordinary Hand320/2, complete source description and original tile/palette. Recheck inherited one-hand metadata; retain unknown actor-specific slot demand.',[HERE/'source-packet.json',HERE/'weapon-metadata.json']),
 ('select_correct_body_and_references','Select the registered male baseline and actual VWE CombatKnife outline reference; retain folding Qud identity rather than military guard/fixed blade.',[HERE/'source-comparison.png']),
 ('construct_and_overlay_one_item','Fit identical manual canonical knife at unchanged physical size with male palm/scale/depth controls on fixed unclothed body.',[HERE/'fit-shared-knife.py',HERE/'canonical-pattern.svg',HERE/'constructed-comparison.png',HERE/'fit-controls.json']),
 ('imagegen_refine_in_context_on_unchanged_body','Reuse the selected exact knife contextual refinement/material and original prompt from compatibility fitting. No new call or new male drawing is claimed.',[SOURCE/'imagegen-prompt.txt',SOURCE/'refined-red-context.png',SOURCE/'registration-decisions.json',HERE/'intact-canonical.png']),
 ('retrieve_isolated_item_and_masks','Retain full blade/pivot/handle and independent Y/y material regions, then place them with the original palm mask. No generative isolation or destructive hand cutout.',[HERE/'model.json',HERE/'registration-decisions.json',HERE/'full-item-comparison.png',HERE/'depth-off-comparison.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Inspect all facing grips and fixed-body depth; correct only the fully hidden initial north display angle and preserve the initial evidence.',[HERE/'rear-display-correction.json',HERE/'initial-rear-hidden/grip-comparison.png',HERE/'grip-comparison.png',HERE/'assembly-comparison.png']),
 ('review_game_scale_and_palette','Review intended-size and source-specific palette; verify canonical identity, common physical mapping, original pixels and complete registered recomposition.',[HERE/'independent-palette-comparison.png',HERE/'game-scale-review.png',HERE/'cross-body-scale-comparison.png',HERE/'authoring-review.json',HERE/'artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(SOURCE/'source-packet.json'),ref(SOURCE/'intact-canonical.png'),ref(BODY/'model.json')],outputs=[ref(p) for p in outputs],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),registration_summary='Small folding knife reused at identical physical size on actual male Argyve Hand/2 baseline; lower grip, independent c/Y/y, readable rear display. Native equipment/ready-resting and named actor assembly pending.',native_acceptance=model['native_acceptance'])
next_id='ITEM-STEEL-UTILITY-KNIFE';next_e=next(e for e in d['entries'] if e['id']==next_id);next_e['status']='IN PROGRESS'
d.update(active_entry=next_id,updated_at=review['timestamp']);assert [e['id'] for e in d['entries'] if e['status']=='IN PROGRESS']==[next_id]
write(f,d);print('Male utility knife generation-ready; only utility-knife aggregate is active.')
