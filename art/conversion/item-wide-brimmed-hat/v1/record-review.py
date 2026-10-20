"""Close only the hat aggregate authoring gate after all three fits were inspected."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
lp=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(lp.read_text());entry=next(e for e in ledger['entries'] if e['id']=='ITEM-WIDE-BRIMMED-HAT')
assert ledger['active_entry']==entry['id'] and not entry['generation_ready']
packet=json.loads((HERE/'fittings.json').read_text());inputs=[x['registration']['model'] for x in packet['fittings']]
review='Inspected the three-body SEN hat comparison and reconciled all required authoring steps against each recorded fitting. Female source is complete neutral crown/brim plus independent band, male fit keeps the same item with explicit head-landmark controls, Nima reuses exact current female art with actual Head part 177/item 530. All preserve unmutated original bodies, shared contact and zero skin-over-hat masks. Named mutation assembly, item modifiers without observed geometry and native equip/unequip/outfit acceptance are not claimed.'
for step,action in [('resolve_item_identity_description_palette','Resolved original wide-brimmed worn hat, crushed crown/sweat-salt stains, actual sw_hat source and pale y/blue b palette.'),('verify_every_body_fitting_log','Reconciled required authoring evidence on all three enumerated fits; reviewed canonical material, male head-relative transformation and exact shared Nima binding.'),('reprocess_under_regional_curved_v1','Aggregated actual current full-source, class-specific visibility, cardinal-facing and independent-palette evidence. No blanket historical credit or native validation.')]:
 entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=inputs+[ref(HERE/'aggregate-fittings.py'),ref(HERE/'record-review.py')],outputs=[ref(HERE/'fittings.json'),ref(HERE/'body-fittings-comparison.png')],review=review,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='record_item_acceptance_from_all_fittings',art_review=dict(status='PASS',reason=review),native_acceptance='Pending final all-conversions gate');entry['apparel_workflow']['status']='GENERATION READY'
for e in ledger['entries']:
 if e['id'] in [x['entry'] for x in packet['fittings']]+[entry['id']]:e['known_issues']=['Native equipment/outfit acceptance awaits the full-set generation gate. Historical generic candidates are superseded by the current source-bound hat records.']
nxt=next(e for e in ledger['entries'] if e['id']=='FIT-HUMAN-FEMALE-TELESCOPIC-MONOCLE-FACE-0');assert not nxt['generation_ready'] and nxt['status']=='UNFINISHED';nxt.update(status='IN PROGRESS',current_step='source_identity_description_slot_laterality');ledger['active_entry']=nxt['id'];ledger['updated_at']=datetime.now(timezone.utc).isoformat();lp.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Hat aggregate authoring recorded; female Telescopic Monocle is the sole active entry.')
