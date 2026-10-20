"""Record this source-bound profile correction and revisit its item aggregate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
lpath=ROOT/'evidence/conversion-ledger.json';data=json.loads(lpath.read_text());entry=next(e for e in data['entries'] if e['id']=='FIT-DROMAD-CLOTH-ROBE-BODY-0');assert data['active_entry']==entry['id'] and not entry['generation_ready']
prev=HERE.parent/'v6';model=json.loads((HERE/'model.json').read_text());old=json.loads((prev/'model.json').read_text())
assert model['views']['south']==old['views']['south'] and model['views']['north']==old['views']['north']
assert np.array_equal(np.array(Image.open(HERE/'intact-robe-east.png'))[:,:,3],np.array(Image.open(prev/'intact-robe-east.png'))[:,:,3])
for rows in model['views'].values():
 for row in rows:
  p=ROOT/row['public_file'];assert ref(p)['sha256']==row['sha256'];a=np.array(Image.open(p).convert('RGBA'));assert a.shape==(1024,512,4);opaque=a[:,:,3]>0;assert np.ptp(a[:,:,:3][opaque].astype(int),axis=1).max()==0
review='Inspected profile cuff close-up, all neutral facings, native w/W body and y cloth, and intended-size plate. Existing sleeve-opening ink supplies one editable quadratic for cuff rim and original-arm visibility. Complete cloth alpha unchanged; explicit neutral seam-ink repair is recorded rather than described as a stretch. Semantic original forearm/hand spans exclude adjacent torso from foreground paint. Fixed body untouched; front/back v6 art unchanged. Current front hump is already cloth-covered; old Shillelagh sheet used obsolete robe v1. No ImageGen or native testing.'
write(HERE/'authoring-review.json',dict(status='GENERATION READY',review=review,native_acceptance='Pending full-set gate'))
write(HERE/'artifact-manifest.json',dict(files=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
for step,action,outputs in [
 ('recompose_check_cuffs_attachment_occlusion_all_views','Corrected profile cuff and original-arm ownership through a shared source-opening curve; discarded the lower-mouth diagnostic because it exposed an excessive dark cavity. Current full source remains intact; no body redraw.', ['profile-cuff-comparison.png','assembly-comparison.png','registration-decisions.json']),
 ('review_game_scale_and_palette','Reviewed one robe over its unclothed base, independent actual Qud palette and intended-size preview. Preserved selected front/back and body/contact.', ['qud-palette-east.png','game-scale-review.png','authoring-review.json','artifact-manifest.json']),
 ('reprocess_under_regional_curved_v1','Recorded full source, explicit cuff ink, shared curve, original-body visibility and exact retained facings. Native and combined outfit acceptance remain pending.', ['model.json'])]:
 entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[ref(prev/'model.json'),ref(HERE/'align-profile-cuff.py')],outputs=[ref(HERE/n) for n in outputs],review=review,result='PASS',new_imagegen_call=False))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),art_review=dict(status='PASS',reason=review),registration_summary='v7 corrects profile cuff rim and arm visibility on one source-bound curve; front/back remain v6 including covered hump. Single robe over fixed unclothed body; native acceptance pending.')
entry['apparel_workflow']['status']='GENERATION READY'
n=next(e for e in data['entries'] if e['id']=='ITEM-CLOTH-ROBE');n.update(status='IN PROGRESS',generation_ready=False,current_step='verify_every_body_fitting_log');data['active_entry']=n['id'];data['updated_at']=datetime.now(timezone.utc).isoformat();write(lpath,data)
print('Robe profile correction recorded; item aggregate is sole active.')
