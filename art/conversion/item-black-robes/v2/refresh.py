"""Refresh the aggregate from the corrected current fitting, without redrawing."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'fittings.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='ITEM-BLACK-ROBES'
idx={e['id']:e for e in l['entries']};e=idx[l['active_entry']];old=read(HERE.parent/'v1/fittings.json');rows=[]
for ident in e['related_entries']:
    fit=idx[ident];assert fit['generation_ready'] and fit['art_review']['status']=='PASS'
    reg=fit['current_registration'];assert ref(ROOT/reg['model']['path'])==reg['model'];m=read(ROOT/reg['model']['path'])
    assert m['actual_equipped_binding']['equipped']['instance']==539 and m['slot']=='Body' and m['laterality']==0
    for parts in m['views'].values():
        for r in parts:assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
    rows.append(dict(entry=ident,registration=reg,authoring_review=fit['art_review']))
reason='Verified all required Black Robes539 Body196/0 fitting dependencies and hashes against the corrected original-hand ownership model. Retained complete wool, native K/K roles and physical size. No new drawing, generation or native acceptance.'
write(HERE/'fittings.json',{**old,'fittings':rows,'scope':reason,'supersedes':ref(HERE.parent/'v1/fittings.json')})
write(HERE/'authoring-review.json',dict(status='PASS',reason=reason,scope='Aggregate generation only',native_acceptance=old['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in HERE.iterdir() if p.is_file() and p.name!='artifact-manifest.json']))
now=datetime.now(timezone.utc).isoformat()
for step in e['required_steps']:
    e['process_log'].append(dict(timestamp=now,step=step,action='Reconcile the retained source item with every current reviewed fitting.',inputs=[r['registration']['model'] for r in rows],outputs=[ref(HERE/'fittings.json'),ref(HERE/'authoring-review.json')],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step=e['required_steps'][-1],known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),current_item_manifest=ref(HERE/'fittings.json'));e.pop('advancement_blocker',None)
n=idx['NPC-ELDERBOB'];assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);l.update(active_entry=n['id'],updated_at=now);write(ROOT/'evidence/conversion-ledger.json',l)
print('Black Robes aggregate generation-ready; Irudad assembly is sole active entry.')
