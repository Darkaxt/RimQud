"""Reconcile the Horns aggregate against the newly reviewed current fitting."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'fittings.json').exists();l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='ITEM-HORNS';entry=next(e for e in l['entries'] if e['id']==l['active_entry']);index={e['id']:e for e in l['entries']};now=datetime.now(timezone.utc).isoformat()
rows=[]
for ident in entry['related_entries']:
    e=index[ident];assert e['generation_ready'] and e['art_review']['status']=='PASS';reg=e['current_registration'];assert ref(ROOT/reg['model']['path'])==reg['model'];m=read(ROOT/reg['model']['path']);folder=(ROOT/reg['model']['path']).parent
    assert m['actual_equipped_binding']['equipped']['instance']==575 and m['slot']=='Head' and m['laterality']==0
    for f,parts in m['views'].items():
        for r in parts:assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
    rows.append(dict(entry=ident,registration=reg,source_packet=ref(folder/'source-packet.json'),fit_contract=ref(folder/'fit-contract.json'),authoring_review=ref(folder/'authoring-review.json'),native_acceptance=m['native_acceptance']))
old=read(HERE.parent/'v3/fittings.json');m=read(ROOT/rows[0]['registration']['model']['path']);out={**old,'recorded_at':now,'fittings':rows,'directional_art':'Actual Blender south/east/north/west of one complete paired volume, calibrated to unchanged body/head; independent native w/W material roles. West is an actual render, not a second mirror.','physical_frame':m['frame_mapping'],'supersedes':ref(HERE.parent/'v3/fittings.json'),'new_imagegen_calls_for_this_aggregate':0,'blender_source':m['blender_source']};write(HERE/'fittings.json',out)
write(HERE/'source-packet.json',dict(recorded_at=now,source_identity=old['source_identity'],native_source=old['source'],current_fittings=rows,whole_shape_policy='One canonical editable model; body-specific calibrated fit. Full hidden source retained.',native_acceptance=old['limits']))
reason='Verified the sole captured Horns575 natural Head288/0 fitting against current registered Blender model, source/fit/review hashes, four real facings, unchanged body frame, full source volume and independent w/W tint. Rounded root shading is minor polish after source-calibrated contact and fresh visual review; prior rejected flat/cut sources are superseded. No standalone duplicate item art or new ImageGen call. Native headgear/equipment state remains pending full-set generation.'
write(HERE/'authoring-review.json',dict(recorded_at=now,status='PASS',scope='Item aggregate generation only',reason=reason,all_required_fittings=rows,source_identity=old['source_identity'],native_acceptance=old['limits']))
write(HERE/'artifact-manifest.json',dict(recorded_at=now,artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
for step,action in [('resolve_item_identity_description_palette','Retain the captured Horns575 source description, natural Head288/0 binding and native w/W palette.'),('verify_every_body_fitting_log','Resolve and verify every current required fitting and direct Blender source.'),('record_item_acceptance_from_all_fittings','Record aggregate generation acceptance without implying native activation.')]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[r['registration']['model'] for r in rows],outputs=[ref(HERE/p) for p in ['fittings.json','source-packet.json','authoring-review.json','artifact-manifest.json']],review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='record_item_acceptance_from_all_fittings',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),current_item_manifest=ref(HERE/'fittings.json'));entry.pop('advancement_blocker',None)
n=index['NPC-WARDEN-YRAME'];assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step='resolve_actual_instance_and_equipped_parts' if 'resolve_actual_instance_and_equipped_parts' in n['required_steps'] else n['required_steps'][0]);l.update(active_entry=n['id'],updated_at=now);write(ROOT/'evidence/conversion-ledger.json',l)
print('Horns aggregate generation-ready; named Yrame assembly is the sole active entry.')
