"""Select the isolated staff fit as primary evidence; keep outfit history."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
p=ROOT/'evidence/conversion-ledger.json';data=json.loads(p.read_text());entry=next(e for e in data['entries'] if e['id']=='FIT-DROMAD-SHILLELAGH-HAND-2');assert data['active_entry']==entry['id'] and not entry['generation_ready']
model=json.loads((HERE/'model.json').read_text());old=json.loads((HERE.parent/'v2/model.json').read_text());assert model['views']==old['views'] and model['context_robe'] is None
review='Inspected single-item primary preview: fixed unclothed dromad body v2 plus corrected inward-grip Shillelagh only, in all required facings. Staff item geometry/scale/attachment and original gripping-hand foreground unchanged from v2; no robe or other equipment included. Independent y/y staff tint and intended-size plates retained. Earlier outfit compositions remain historical evidence; no native/outfit acceptance claimed.'
write(HERE/'authoring-review.json',dict(status='GENERATION READY',review=review,native_acceptance='Pending full-set generation gate'))
write(HERE/'artifact-manifest.json',dict(files=[ref(f) for f in sorted(HERE.iterdir()) if f.is_file() and f.name!='artifact-manifest.json']))
for step,action,outs in [('recompose_check_cuffs_attachment_occlusion_all_views','Recomposed unchanged registered staff on current fixed unclothed base, with no unrelated robe. This is the primary fitting evidence; old outfit sheets stay historical.',['composition-inputs.json','assembly-comparison.png']),('review_game_scale_and_palette','Reviewed single-item neutral and independent equipment tint plus intended-size views; no other equipment or new generation.',['palette-comparison.png','game-scale-review.png','authoring-review.json','artifact-manifest.json'])]:
 entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[ref(HERE/'compose-single-item.py'),ref(HERE.parent/'v2/model.json'),ref(ROOT/'skills/qud-creature-conversion/SKILL.md')],outputs=[ref(HERE/n) for n in outs],review=review,result='PASS',new_imagegen_call=False))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),art_review=dict(status='PASS',reason=review),registration_summary='Primary evidence: Shillelagh alone over fixed unclothed dromad v2. Front/back shaft grips lie inward inside actual palms; original hands own grip foreground. Item scale/profile unchanged. Earlier outfit sheets retained only as history.')
n=next(e for e in data['entries'] if e['id']=='FIT-NIMA-LEATHER-APRON-BODY-0');assert n['status']=='UNFINISHED';n.update(status='IN PROGRESS',current_step='source_identity_description_slot_laterality');data['active_entry']=n['id'];data['updated_at']=datetime.now(timezone.utc).isoformat();write(p,data)
print('Single-item staff evidence selected; Nima apron resumes; native gate unchanged.')
