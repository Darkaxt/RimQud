"""Resolve a non-substantiated screening finding without changing usable art."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='SCN-DOGTHORN-TREE';e=next(e for e in l['entries'] if e['id']==l['active_entry'])
r=read(HERE/'closer-inspection.json')
for x in r['inputs']:assert ref(ROOT/x['path'])['sha256']==x['sha256']
assert not r['consequential_issues']
diagnostic=read(HERE/'alpha-continuity-diagnostics.json');assert all(x['same_nonzero_component'] for x in diagnostic['checks'])
assert ref(ROOT/e['current_registration']['model']['path'])==e['current_registration']['model']
m=read(ROOT/e['current_registration']['model']['path'])
for row in m['states']:
    for key in ['primary','detail','coverage','detail_coverage']:assert ref(ROOT/row[key]['path'])==row[key]
now=datetime.now(timezone.utc).isoformat()
reason='Closer actual-alpha inspection corrects the earlier screening conclusion: the highest variant2 cluster overlaps the upper-right neighboring foliage, which continues toward the visible rising branch. Background beneath the tuft does not fully isolate it. Fresh independent inspection found no demonstrated consequential detachment. Solid alpha remains connected through two-pixel erosion at thresholds128/240, supporting the visible overlap but not proving hidden wood anatomy. Requiring exposed wood through all foliage would invent a requirement. Retain existing two source variants, palette masks, frame and pixels; no crown repair or new model is justified solely by this allegation.'
write(HERE/'authoring-review.json',dict(status='PASS',reason=reason,disposition='Earlier FIX NOW allegation NOT SUBSTANTIATED on closer inspection',
    independent_review=ref(HERE/'closer-inspection.json'),diagnostics=ref(HERE/'alpha-continuity-diagnostics.json'),
    reviewer=dict(agent='/root/dogthorn_crown_inspection',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override'),
    no_art_changes=True,new_blender_model=False,new_imagegen_call=False,
    naming_note='Folder reserved for prospective Blender correction; closer inspection established no correction was warranted. No Blender stage is claimed.',native_acceptance='Pending full generation gate'))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
e['process_log'].append(dict(timestamp=now,step='visual_review_identity_and_connections_at_game_scale',action='Inspect original-alpha crown closeup, full variants and isolated wood; reconsider screening finding before modifying source.',
    inputs=[e['current_registration']['model']],outputs=[ref(HERE/'crown-source-closeup.png'),ref(HERE/'closer-inspection.json'),ref(HERE/'alpha-continuity-diagnostics.json'),ref(HERE/'authoring-review.json')],review=reason,result='PASS / PRIOR FINDING NOT SUBSTANTIATED'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')))
e.pop('advancement_blocker',None)
e['retrospective_finding_reconsideration']=ref(HERE/'authoring-review.json')
l['current_structural_correction_queue']['ordered_entries']=[x for x in l['current_structural_correction_queue']['ordered_entries'] if x!=e['id']]
l.setdefault('resolved_structural_corrections',[]).append(dict(entry=e['id'],recorded_at=now,disposition='NOT SUBSTANTIATED / source retained',review=ref(HERE/'authoring-review.json')))
n=next(e for e in l['entries'] if e['id']=='SCN-WATERVINE');assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);l.update(active_entry=n['id'],updated_at=now)
write(ROOT/'evidence/conversion-ledger.json',l)
print('Dogthorn source retained after closer inspection; Watervine sole active entry.')
