"""Correct the actual sandal construction before retrying contextual refinement."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'v1'
def ref(p):
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
def write(p, data):
    p.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')

# Preserve the source procedure while producing a new, independently editable version.
script = (OLD/'prepare-source.py').read_text(encoding='utf-8')
script = script.replace("stroke=\"#202523\"", "stroke=\"#252525\"")
script = script.replace("replace('#202523','white')", "replace('#252525','white')")
old = "'east':path('M199 881 Q231 878 269 893 L272 904 Q234 891 198 894Z')+path('M202 899 L211 898 L219 937 L208 940Z')+path('M246 912 L259 912 L278 940 L265 943Z')+path('M290 925 L303 929 L315 945 L302 949Z'),"
new = "'east':path('M199 881 Q231 878 269 893 L272 904 Q234 891 198 894Z')+path('M202 891 L213 892 L222 938 Q217 943 207 940Z')+path('M261 876 Q268 881 274 888 L285 938 Q279 944 269 941 L259 908 Q256 895 257 884Z')+path('M289 897 Q299 900 308 905 L325 940 Q320 946 312 945 L299 920Z'),"
assert old in script
script = script.replace(old, new)
script = script.replace("Prepared female sandals:", "Prepared corrected female sandals v2:")
(HERE/'prepare-source.py').write_text(script, encoding='utf-8')
exec(compile(script, str(HERE/'prepare-source.py'), 'exec'), {'__file__': str(HERE/'prepare-source.py'), '__name__':'__main__'})

packet = json.loads((HERE/'source-packet.json').read_text(encoding='utf-8'))
packet.update(supersedes=ref(OLD/'source-packet.json'), correction={
    'cause':'The original manual profile placed instep/toe strips below the foot upper contour. ImageGen preserved the bad design and registration reused it; this was not caused by late masking.',
    'change':'Editable profile straps now run continuously from above the corresponding foot upper contour to the sole. Curved ankle/heel connections, crossed front and heel-back construction retained.',
    'body':'All original body pixels, framing, world mapping and contact remain unchanged.',
    'review_gate':'Inspect the retry for structural continuity, full foot-height coverage and anchors before any extraction or material registration.'})
write(HERE/'source-packet.json', packet)
for source, name in [
    (Path('C:/Users/darka/AppData/Local/Temp/codex-clipboard-f3ad121f-4f3d-43ab-8d0d-3c137df85af9.png'), 'user-rejected-palette.png'),
    (Path('C:/Users/darka/AppData/Local/Temp/codex-clipboard-39078b48-c025-4c22-be58-91cf5df4496c.png'), 'user-rejected-context.png')]:
    shutil.copyfile(source, HERE/name)
record = {
    'timestamp':datetime.now(timezone.utc).isoformat(),
    'reason':packet['correction']['cause'],
    'rejected_inputs':[ref(OLD/'pattern-east.svg'), ref(OLD/'refined-red-context.png'), ref(OLD/'independent-palette-comparison.png'), ref(HERE/'user-rejected-palette.png'),ref(HERE/'user-rejected-context.png')],
    'corrected_inputs':[ref(HERE/'prepare-source.py'),ref(HERE/'pattern-east.svg'), ref(HERE/'constructed-red-feet-context.png'), ref(HERE/'source-packet.json')],
    'retry_status':'NOT YET CALLED', 'native_validation':'Not performed; full-set generation gate remains in force.'}
write(HERE/'structural-correction.json', record)

ledger_file=ROOT/'evidence/conversion-ledger.json'
ledger=json.loads(ledger_file.read_text(encoding='utf-8'))
active='FIT-HUMAN-FEMALE-SANDALS-FEET-0'
reason='Profile straps terminate below the foot upper contour instead of wrapping over full foot height and reaching their anchors. Shared v1 source affects all four fits; previous authoring PASS is withdrawn.'
for entry in ledger['entries']:
    if 'SANDALS' not in entry['id']: continue
    entry['generation_ready']=False
    entry['status']='IN PROGRESS' if entry['id']==active else 'UNFINISHED'
    entry['current_step']='imagegen_refine_in_context_on_unchanged_body' if entry['id']==active else ('verify_every_body_fitting_log' if entry['id']=='ITEM-SANDALS' else 'construct_and_overlay_one_item')
    entry['art_review']={'status':'REJECTED','reason':reason}
    entry['apparel_workflow']['status']='REQUIRES STRUCTURAL CORRECTION'
    entry['registration_summary']='Superseded v1 candidate retained as history; structural strap correction is required before readiness.'
    if reason not in entry['known_issues']: entry['known_issues'].append(reason)
    entry['process_log'].append({'timestamp':record['timestamp'],'step':'structural_review_after_refinement',
        'action':'Withdraw v1 generation-ready credit following the user-identified shared strap construction defect.',
        'inputs':record['rejected_inputs'],'outputs':[ref(HERE/'structural-correction.json')],
        'review':reason+' No native acceptance performed. Each fit must be corrected and reviewed individually.', 'result':'INVALIDATED'})
knife=next(e for e in ledger['entries'] if e['id']=='FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2')
assert not knife['process_log'], 'Preserve any new knife work before changing active entry.'
knife['status']='UNFINISHED'
ledger['active_entry']=active
ledger['updated_at']=record['timestamp']
assert [e['id'] for e in ledger['entries'] if e['status']=='IN PROGRESS']==[active]
write(ledger_file,ledger)
print('Withdrew five shared-source readiness claims; only female sandal correction is active.')
