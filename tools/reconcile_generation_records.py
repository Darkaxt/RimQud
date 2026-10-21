"""Reconcile two stale authoring-step records against unchanged selected production exports."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/generation-gate-reconciliation-20261021';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry'] is None;idx={e['id']:e for e in l['entries']};records=[]
for ident,step in [('FIT-DROMAD-CHILD-TEMPLATE-TUNIC','extract_register_palette_masks'),('ITEM-LEATHER-APRON','reprocess_under_regional_curved_v1')]:
 e=idx[ident];reg=e['current_registration'];assert ref(ROOT/reg['model']['path'])==reg['model'];assert ref(ROOT/reg['plate']['path'])==reg['plate'];now=datetime.now(timezone.utc).isoformat();e.update(status='IN PROGRESS',generation_ready=False,current_step=step);l['active_entry']=ident;write(ROOT/'evidence/conversion-ledger.json',l);model=read(ROOT/reg['model']['path']);assert model['workflow']=='regional-curved-v1'
 if ident.startswith('FIT-'):
  assert {'south','east','north'}<=model['views'].keys();checks=[]
  for view,layers in model['views'].items():
   assert {'item','body-overlay'}<={r['component'] for r in layers}
   for layer in layers:
    p=ROOT/layer['public_file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==layer['sha256'];im=Image.open(p);assert list(im.size)==model['canvas'];assert layer['contact']==model['contact'];checks.append(dict(view=view,component=layer['component'],path=layer['public_file'],sha256=layer['sha256'],size=list(im.size),contact=layer['contact']))
  assert any(x['step']=='reprocess_under_regional_curved_v1' and x['result']=='PASS' for x in e['process_log']);reason='The older extraction step was left at REQUIRES REWORK when baked-cut exports were invalidated. Later regional-curved-v1 v4 successfully rebuilt complete tunic art and separate natural body visibility, with PASS authoring/retrospective review. This reconciliation checks the exact currently selected v4 model and all3view item/body-overlay export hashes, fixed512x1024 canvas and contact. It records current extraction PASS against that superseding export; it does not accept the rejected baked-cut source, change art, imply a native child selector or invent a new refinement.'
 else:
  checks=[]
  for f in model['fittings']:
   dep=idx[f['entry']];assert dep['generation_ready'] and f['registration']==dep['current_registration'];dm=read(ROOT/f['registration']['model']['path']);assert dm['workflow']=='regional-curved-v1';assert any(x['step']=='reprocess_under_regional_curved_v1' and x['result']=='PASS' for x in dep['process_log']);checks.append(dict(fitting=f['entry'],current_registration=f['registration'],workflow=dm['workflow']))
  reason='The Leather Apron aggregate already selects the exact completed regional-curved-v1 Nima fitting, complete cloth and separate original-body masks, but its aggregate reprocess step retained only the earlier INVALIDATED event. Exact current fitting/model hashes and the fitting reprocess PASS are inspected here; record generation-only aggregate workflow reconciliation without new art or native acceptance. Named outfit/equipped-state acceptance remains required in final Stage3 native review.'
 report=dict(entry=ident,step=step,scope='Generation evidence reconciliation only; unchanged selected art',model=reg['model'],checks=checks,reason=reason,new_generation_calls=0,native_acceptance=False);p=OUT/(ident.lower()+'-authoring-record.json');write(p,report);e['process_log'].append(dict(timestamp=now,step=step,action='Reconcile stale authoring-step record to exact selected superseding production exports.',inputs=[reg['model']],outputs=[ref(p),reg['plate']],review=reason,result='PASS'));e.update(status='UNFINISHED',generation_ready=True,current_step=e['required_steps'][-1]);l.update(active_entry=None,updated_at=now);write(ROOT/'evidence/conversion-ledger.json',l);records.append(ref(p))
write(OUT/'authoring-record-reconciliations.json',dict(records=records,native_acceptance=False));print('Two stale generation-step records reconciled from exact existing exports; no art or native acceptance changed.')
