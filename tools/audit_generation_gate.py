"""Reconcile every current authoring requirement before the first full-set native acceptance run."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from enumerate_conversion_ledger import validate,enumerate_entries
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/generation-gate-reconciliation-20261021';read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));l=read(ROOT/'evidence/conversion-ledger.json');validate(l,enumerate_entries());idx={e['id']:e for e in l['entries']};audit=read(OUT/'final-artifact-audit.json');assert not audit['issues'];assert audit['ledger_sha256']==hashlib.sha256((ROOT/'evidence/conversion-ledger.json').read_bytes()).hexdigest();assert l['active_entry'] is None;rows=[];bindings=[];pending=[]
for e in l['entries']:
 assert e.get('generation_ready') and not e.get('advancement_blocker'),e['id'];generation=[]
 for step in e['required_steps']:
  if step.startswith('native_') or e['category']=='Equipment inventory' and step=='record_item_acceptance_from_all_fittings':
   pending.append(dict(entry=e['id'],step=step,owning_stage='Stage3 full-set native integration/acceptance',status='UNFINISHED'));continue
  logs=[x for x in e['process_log'] if x['step']==step];passes=[i for i,x in enumerate(logs) if x['result']=='PASS'];assert passes,(e['id'],step,'No generation PASS');assert not any(x['result'] in ['REJECTED','INVALIDATED','REQUIRES REWORK'] for x in logs[passes[-1]+1:]),(e['id'],step,'Later unresolved authoring rejection');generation.append(step)
 reg=e.get('current_registration');model=read(ROOT/reg['model']['path']) if reg else None
 if model and e['category']=='Equipment inventory':
  for f in model.get('fittings',[]):
   ident=f.get('entry');actual=(f.get('registration') or {}).get('model') or f.get('model');expected=idx[ident]['current_registration']['model'];assert actual==expected,(e['id'],ident,'Stale fitting');bindings.append(dict(owner=e['id'],dependency=ident,current_model=actual))
 if model and e['category'] in ['NPC assemblies','Creatures']:
  expected={ident:idx[ident].get('current_registration',{}).get('model') for ident in e['related_entries']}
  for item,b in model.get('equipment_bindings',{}).items():assert b['model'] in [v for k,v in expected.items() if k.startswith('FIT-')],(e['id'],item,'Stale actor fitting');bindings.append(dict(owner=e['id'],item=item,current_model=b['model']))
  if model.get('body_model'):assert model['body_model'] in [v for k,v in expected.items() if k.startswith('BODY-')],(e['id'],'Stale actor body')
 if e['category']=='Furniture':assert {'south','east','north'}<=set(e['furniture_views']['completed_views']),e['id']
 if e['required_variants'] and isinstance(e['required_variants'][0],dict) and 'mask' in e['required_variants'][0]:
  if model.get('kind')=='native_eight_neighbor_wall_variants':
   source=read(ROOT/model['native_state_evidence']['path'])
   assert model['native_state_order']==['N','NE','E','SE','S','SW','W','NW'],e['id']
   expected={format(n,'08b') for n in range(256)}
   assert len(model['states'])==256 and {x['native_suffix'] for x in model['states']}==expected,e['id']
   assert {x['native_suffix']:x['native_tile'].lower() for x in model['states']}=={x['native_suffix']:x['tile'].lower() for x in source['all_native_states']},e['id']
   cardinal={x['cardinal_mask']:x for x in model['states'] if 'cardinal_mask' in x}
   assert set(cardinal)==set(range(16)),e['id']
   assert model['cardinal_atlas']['bits']==dict(N=1,E=2,S=4,W=8),e['id']
   for mask,row in cardinal.items():
    assert row['native_suffix']==''.join('1' if bit and mask&bit else '0' for bit in [1,0,2,0,4,0,8,0]),(e['id'],mask)
    assert row['atlas_rect']==[mask%4*256,(3-mask//4)*256,256,256],(e['id'],mask)
  else:assert {x['mask'] for x in model['states']}==set(range(16)),e['id']
 if e['category']=='Baseline exclusion review' and not reg:assert e.get('scope_review') and read(ROOT/e['scope_review']['path'])['effective_render']['Visible']=='false',e['id']
 rows.append(dict(entry=e['id'],generation_steps_satisfied=generation,current_registration=reg,scope_review=e.get('scope_review'),native_acceptance='Pending complete-set acceptance; generation readiness is not overall completion'))
out=dict(recorded_at=datetime.now(timezone.utc).isoformat(),status='GENERATION GATE PASS / NATIVE INTEGRATION AND ACCEPTANCE UNFINISHED',scope='All156 current conversion ledger entries, actual authoring steps, registered artifacts, source exclusions and exact current equipment/actor dependencies. No new blanket visual sweep, game run or native acceptance.',ledger_sha256=audit['ledger_sha256'],artifact_audit=dict(path=(OUT/'final-artifact-audit.json').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((OUT/'final-artifact-audit.json').read_bytes()).hexdigest()),entries=rows,current_bindings=bindings,pending_native_steps=pending,remaining_stage3_requirements=['Wire the complete selected art/state/tint/visibility/body/equipment set into existing native path','Run authorized hidden command-driven full-set facing/contact/visibility/equip/palette/hurt/look/save-load/gameplay checks','Verify actual installed behavior and retain evidence; resolve serious confirmed failures','Honor user requested pause before procedure/body redesign after complete-set test'],native_activation=False,native_acceptance=False)
(OUT/'generation-gate.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print('Generation gate PASS:',len(rows),'entries;',len(bindings),'current aggregate/actor bindings;',len(pending),'native acceptance steps remain in Stage3.')
