"""Read-only authoring evidence reconciliation; never a native/game acceptance test."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--historical-pins');args=p.parse_args();ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());cache={};seen_json=set();issues=[];current=[];historical=[];resolved_historical=[]
pins=json.loads((ROOT/args.historical_pins).read_text())['pins'] if args.historical_pins else []
def check(ref,owner,origin,current_scope):
 path=Path(ref['path']);expected=ref['sha256'].lower()
 if not path.is_absolute():
  if path.parts[0] in ['art','evidence','skills','docs','tools','probe']:path=ROOT/path
  elif str(origin).endswith('.json') and 'independent-' in Path(origin).name:
   # Older bounded review packets use explicit version-root or packet-relative paths.
   parent=(ROOT/origin).parent;path=(parent.parent/path if path.parts[0].startswith('blender-') else parent/path).resolve()
  else:path=ROOT/path
 key=(str(path),expected)
 if str(path) not in cache:
  cache[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
 actual=cache[str(path)];record=dict(entry=owner,path=ref['path'],resolved_path=str(path),expected_sha256=expected,actual_sha256=actual,origin=origin)
 if actual!=expected:
  pin=next((p for p in pins if p['origin']==origin and p['recorded_path']==ref['path'] and p['expected_sha256']==expected),None)
  if pin:
   assert ref['path'] in ['skills/qud-creature-conversion/SKILL.md','skills/qud-creature-conversion/references/apparel-fitting.md','evidence/blender-shape-ledger.json'] or (origin=='art/conversion/fit-yrame-horns/v4/before-alpha-normalization/model.json' and ref['path'].startswith('art/conversion/fit-yrame-horns/v4/intact-item-') and ref['path'].endswith('.png'))
   selected=ROOT/pin['resolved']['path'];assert hashlib.sha256(selected.read_bytes()).hexdigest()==expected
   resolved_historical.append(dict(**record,historical_exact_reference=pin['resolved'],scope=pin['scope']));path=selected;actual=expected;record.update(resolved_path=str(path),current_mutable_sha256=record['actual_sha256'],actual_sha256=expected,historical_provenance=True)
 if actual!=expected:
  record['issue']='MISSING' if actual is None else 'HASH MISMATCH';issues.append(record);return
 (current if current_scope else historical).append(record)
 if current_scope and path.suffix=='.json' and key not in seen_json:
  seen_json.add(key)
  try:walk(json.loads(path.read_text(encoding='utf-8-sig')),owner,ref['path'],True)
  except (json.JSONDecodeError,UnicodeDecodeError) as ex:issues.append(dict(entry=owner,path=ref['path'],issue='Unreadable JSON',reason=str(ex)))
def walk(v,owner,origin,current_scope):
 if isinstance(v,dict):
  if v.get('entry') in {e['id'] for e in ledger['entries']}:owner=v['entry']
  if isinstance(v.get('path'),str) and isinstance(v.get('sha256'),str) and len(v['sha256'])==64:check(v,owner,origin,current_scope)
  if isinstance(v.get('public_file'),str) and isinstance(v.get('sha256'),str) and len(v['sha256'])==64:check(dict(path=v['public_file'],sha256=v['sha256']),owner,origin,current_scope)
  if isinstance(v.get('base_model'),str) and isinstance(v.get('body_sha256'),str) and len(v['body_sha256'])==64:check(dict(path=v['base_model'],sha256=v['body_sha256']),owner,origin,current_scope)
  for value in v.values():walk(value,owner,origin,current_scope)
 elif isinstance(v,list):
  for value in v:walk(value,owner,origin,current_scope)
for e in ledger['entries']:
 walk(e.get('current_registration',{}),e['id'],'current_registration',True)
 walk(e.get('persistent_3d_sources',{}),e['id'],'persistent_3d_sources',True)
 walk(e.get('scope_review',{}),e['id'],'scope_review',True)
 for log in e['process_log']:walk(log.get('outputs',[]),e['id'],log['step'],False)
print('Authoring references scanned:',len(cache),'unique files;',len(issues),'issues',flush=True)
out=dict(recorded_at=datetime.now(timezone.utc).isoformat(),scope='Current registration/dependency JSON references plus actual historical process output hashes. Read-only authoring audit; no native activation or acceptance.',ledger_sha256=hashlib.sha256((ROOT/'evidence/conversion-ledger.json').read_bytes()).hexdigest(),entries=len(ledger['entries']),generation_ready_flags=sum(bool(e.get('generation_ready')) for e in ledger['entries']),active_entry=ledger['active_entry'],unique_files=len(cache),current_reference_checks=len(current),historical_output_checks=len(historical),historical_exact_resolutions=resolved_historical,issues=issues,native_acceptance=False)
target=ROOT/args.output;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps(issues[:20],indent=2),flush=True)
