"""Close the reviewed mask correction, keeping native acceptance pending."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v): p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
ledger=read(ROOT/'evidence/conversion-ledger.json'); assert ledger['active_entry']=='FIT-IRUDAD-BLACK-ROBES-BODY-0'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
model=read(HERE/'model.json'); old=read(HERE.parent/'v3/model.json')
review=read(HERE/'independent-ownership-review.json')
for r in review['inspected_images']: assert ref(ROOT/r['path'])['sha256']==r['sha256']
assert not review['findings']
assert model['body_source']==old['body_source'] and ref(ROOT/model['body_source']['path'])==model['body_source']
checks={}
for face,rows in model['views'].items():
    for row,previous in zip(rows,old['views'][face]):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        assert all(row[k]==previous[k] for k in ['size','contact','width','height','center_x','center_z','layer','color_role'])
        if face!='east' or row['component']!='body-overlay': assert row==previous
    assert model['occlusion_sources'][face]['full_cloth']==old['occlusion_sources'][face]['full_cloth']
    checks[face]=dict(full_cloth_unchanged=True,frame_unchanged=True)
body=np.array(Image.open(ROOT/'art/conversion/body-human-male-older/v2/selected-east.png').convert('RGBA'))
over=np.array(Image.open(HERE/'body-overlay-east.png').convert('RGBA'))
assert np.array_equal(body[:,:,:3],over[:,:,:3]) and np.all(over[:,:,3]<=body[:,:,3])
reason='Inspected all four cardinal compositions, original contour/source attribution, cuff closeups, native K/K palette and intended-size sheets. The v3 circle included adjacent torso pixels; v4 selects the actual original hand/wrist contour and removes the pale crescent. Fresh independent review confirms one continuous hand contour and cuff contact in east/mirrored west, with no demonstrated FIX NOW defect. Body RGB, complete wool, front/back ownership and registration remain unchanged. This is a mask correction on retained usable art, not a replacement garment design.'
now=datetime.now(timezone.utc).isoformat()
write(HERE/'authoring-review.json',dict(status='PASS',scope='Generation authoring only',reason=reason,
    independent_review=ref(HERE/'independent-ownership-review.json'),reviewer=dict(agent='/root/irudad_ownership_review',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override'),
    checks=checks,original_body_rgb_unchanged=True,native_acceptance='Pending full-set generation gate'))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
for step,action,names in [
    ('recompose_check_cuffs_attachment_occlusion_all_views','Trace the extra crescent to oversized original-body ownership, correct only that mask, and inspect all views.',['correction-decisions.json','hand-contour-controls.json','ownership-before-after.png','model.json']),
    ('review_game_scale_and_palette','Inspect native palette, intended-size output and independent structural findings; retain source/body/frame.',['independent-palette-comparison.png','game-scale-review.png','independent-ownership-review.json','authoring-review.json'])]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE.parent/'v3/model.json'),ref(HERE/'correct-ownership.py')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=['Native equipped state and outfit precedence remain behind the full generation gate.'],
    art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),
    current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
    registration_summary='Retained complete source wool and fixed older-human body; actual hand contour ownership removes the side crescent. Native acceptance pending.')
entry.pop('advancement_blocker',None)
if 'apparel_workflow' in entry: entry['apparel_workflow']['status']='GENERATION READY'
n=next(e for e in ledger['entries'] if e['id']=='ITEM-BLACK-ROBES'); assert not n['generation_ready']
n.update(status='IN PROGRESS',current_step=n['required_steps'][0]); ledger.update(active_entry=n['id'],updated_at=now)
write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Robe fitting generation-ready; Black Robes aggregate is sole active entry.')
