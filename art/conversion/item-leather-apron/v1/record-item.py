"""Reconcile the Leather Apron inventory entry against its only enumerated fit."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
lp=ROOT/'evidence/conversion-ledger.json';data=json.loads(lp.read_text());entry=next(e for e in data['entries'] if e['id']=='ITEM-LEATHER-APRON');assert data['active_entry']==entry['id'] and not entry['generation_ready']
fits=[next(e for e in data['entries'] if e['id']==ident) for ident in entry['related_entries']];assert len(fits)==1
for fit in fits:
 assert fit['generation_ready'] and fit['art_review']['status']=='PASS'
 latest={e['step']:e for e in fit['process_log']}
 assert all(latest[s]['result']=='PASS' for s in fit['required_steps'] if s!='native_equipment_state_review')
 for asset in fit['current_registration'].values():assert ref(ROOT/asset['path'])['sha256']==asset['sha256']
packet=dict(item='Leather Apron',workflow='regional-curved-v1',source=entry['metadata']['original_reference'],fittings=[dict(entry=e['id'],registration=e['current_registration'],authoring_review=e['art_review']) for e in fits],scope='Only enumerated fit: actual Nima Body176/0. No duplicate generic garment or named mutant-body completion.',native_acceptance='Pending full-set generation gate and actual outfit/equipped state')
write(HERE/'fittings.json',packet);shutil.copyfile(ROOT/fits[0]['current_registration']['plate']['path'],HERE/'body-fittings-comparison.png')
review='Verified exact Leather Apron identity/description/w-W palette against the source-bound Nima fit, actual Body176/item529/0, recorded original/mod/manual/context/material/masks/facings/palette evidence and current model/plate hashes. No other enumerated fits. Generation-only item aggregate; no native/actor completion.'
for step,action in [('resolve_item_identity_description_palette','Reconciled actual boar-hide apron source description, original glyph and w/W palette.'),('verify_every_body_fitting_log','Reconciled the one enumerated Nima apron fit, including all authoring steps and exact registered assets.')]:
 entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[e['current_registration']['model'] for e in fits],outputs=[ref(HERE/'fittings.json'),ref(HERE/'body-fittings-comparison.png')],review=review,result='PASS',new_imagegen_call=False))
entry.update(status='UNFINISHED',generation_ready=True,current_step='record_item_acceptance_from_all_fittings',current_registration=dict(model=ref(HERE/'fittings.json'),plate=ref(HERE/'body-fittings-comparison.png')),art_review=dict(status='PASS',reason=review),registration_summary='Leather Apron item identity and its only enumerated Nima ordinary-body fit are generation-ready. Exact w/W hide roles and original-body depth retained; named mutation/outfit/native acceptance pending.',native_acceptance='Pending full-set generation gate and actual outfit/equipped state',known_issues=['Native item acceptance and named Nima mutation/outfit assembly remain unfinished.']);entry['apparel_workflow']['status']='GENERATION READY'
n=next(e for e in data['entries'] if e['id']=='FIT-YRAME-CHAIN-MAIL-BODY-0');assert n['status']=='UNFINISHED' and not n['generation_ready'];n.update(status='IN PROGRESS',current_step='source_identity_description_slot_laterality');data['active_entry']=n['id'];data['updated_at']=datetime.now(timezone.utc).isoformat();write(lp,data)
print('Leather Apron item aggregate generation-ready; Yrame Chain Mail is sole active. Full goal remains unfinished.')
