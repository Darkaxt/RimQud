"""Reconcile the single required blade fitting without inventing generation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];FIT=ROOT/'art/conversion/fit-yrame-vibro-blade/v2'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'fittings.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='ITEM-VIBRO-BLADE'
e=next(e for e in l['entries'] if e['id']==l['active_entry']);dep=next(e for e in l['entries'] if e['id']=='FIT-YRAME-VIBRO-BLADE-HAND-2');assert dep['generation_ready']
steps=[s for s in dep['required_steps'] if not s.startswith('native_')]
for s in steps:assert next(x for x in reversed(dep['process_log']) if x['step']==s)['result']=='PASS',s
for r in read(FIT/'artifact-manifest.json')['artifacts']:assert ref(ROOT/r['path'])==r
old=read(HERE.parent/'v1/fittings.json');now=datetime.now(timezone.utc).isoformat()
reason='Reconciled the sole required Vibro Blade fitting on current centauroid anatomy and actual right Hand292/2/item576. Existing complete matte blade/finger-rest art, original source glyph, actual Core reference and historical ImageGen call remain linked. Fresh ancestry/default evidence supports one-hand base class; actor slot demand and charge state remain unknown. Fixed physical size, low inward palm grip and explicit west far-side depth reviewed. No new ImageGen call. Native/held/resting-ready state acceptance stays pending.'
fittings=dict(recorded_at=now,item=old['item'],source=old['source'],installed_definition=old['installed_definition'],source_resolution=old['source_resolution'],
 fittings=[dict(entry=dep['id'],registration=dep['current_registration'],source_packet=ref(FIT/'source-packet.json'),fit_contract=ref(FIT/'fit-contract.json'),authoring_review=ref(FIT/'authoring-review.json'),registration_decisions=ref(FIT/'registration-decisions.json'))],
 physical_frame=read(FIT/'model.json')['frame_mapping'],reused_generation=read(FIT/'source-packet.json')['reused_generation'],handedness=ref(FIT/'handedness-evidence.json'),new_imagegen_calls_for_this_aggregate=0,scope=reason,pose_review=old['pose_review'],native_acceptance=old['native_acceptance'],supersedes=ref(HERE.parent/'v1/fittings.json'))
write('fittings.json',fittings);write('authoring-review.json',dict(recorded_at=now,status='PASS',scope='Generation authoring aggregation only',reason=reason,fitting_entries=[dep['id']],non_native_steps_reconciled=steps,native_acceptance=old['native_acceptance']))
write('artifact-manifest.json',dict(recorded_at=now,entry=e['id'],artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
for step,names in [('resolve_item_identity_description_palette',['source-packet.json','blueprint-ancestry.json','handedness-evidence.json','donor-definition-evidence.json']),('verify_every_body_fitting_log',['fit-contract.json','authoring-review.json','assembly-comparison.png','grip-comparison.png','game-scale-review.png'])]:
 e['process_log'].append(dict(timestamp=now,step=step,action=reason,inputs=[dep['current_registration']['model']],outputs=[ref(FIT/n) for n in names],review=reason,result='PASS'))
e['process_log'].append(dict(timestamp=now,step='record_item_acceptance_from_all_fittings',action='Aggregate authoring acceptance only; native item acceptance remains pending.',inputs=[dep['current_registration']['model']],outputs=[ref(HERE/n) for n in ['fittings.json','authoring-review.json','artifact-manifest.json']],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),current_registration=dict(model=ref(HERE/'fittings.json'),plate=dep['current_registration']['plate']),registration_summary=reason)
n=next(e for e in l['entries'] if e['id']=='NPC-WARDEN-YRAME');assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step='resolve_individual_race_and_runtime_metadata')
l.update(active_entry=n['id'],updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode())
print('Vibro Blade aggregate generation-ready; NPC-WARDEN-YRAME is the sole active entry.')
