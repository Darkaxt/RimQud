"""Recover exact old authoring-guidance/registry evidence, without rolling back current guidance."""
from pathlib import Path
import json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'evidence/generation-gate-reconciliation-20261021';issues=json.loads((OUT/'resolved-path-artifact-audit.json').read_text())['issues'];extra=OUT/'current-artifact-audit.json';issues+=json.loads(extra.read_text())['issues'] if extra.exists() else [];pins=[];seen=set();HISTORY=OUT/'historical-provenance';HISTORY.mkdir(exist_ok=True)
def sha(data):return hashlib.sha256(data).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p.read_bytes()))
for row in issues:
 key=(row['path'],row['expected_sha256'])
 if key in seen:continue
 seen.add(key)
 if row['origin']=='art/conversion/fit-yrame-horns/v4/before-alpha-normalization/model.json':
  assert row['path'].startswith('art/conversion/fit-yrame-horns/v4/intact-item-') and row['path'].endswith('.png');selected=ROOT/'art/conversion/fit-yrame-horns/v4/before-alpha-normalization'/Path(row['path']).name;assert sha(selected.read_bytes())==row['expected_sha256'];source=dict(kind='Existing exact rejected/pre-normalization pixel archive',selected=ref(selected))
 elif row['path']=='evidence/blender-shape-ledger.json':
  assert row['origin']=='art/conversion/npc-warden-yrame/v3/dependency-lineage.json'
  matches=[p for p in (ROOT/'evidence/blender-shape-ledger-history').glob('v*.json') if sha(p.read_bytes())==row['expected_sha256']];assert len(matches)==1;selected=matches[0];source=dict(kind='Existing immutable registry snapshot',selected=ref(selected))
 else:
  assert row['origin']=='art/conversion/npc-warden-yrame/v3/dependency-lineage.json' and row['path'] in ['skills/qud-creature-conversion/SKILL.md','skills/qud-creature-conversion/references/apparel-fitting.md']
  revisions=subprocess.check_output(['git','log','--all','--format=%H','--',row['path']],cwd=ROOT,text=True).splitlines();found=None
  for rev in revisions:
   result=subprocess.run(['git','show',rev+':'+row['path']],cwd=ROOT,capture_output=True)
   if result.returncode:continue
   for label,data in [('Git stored bytes',result.stdout),('Working CRLF materialization',result.stdout.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))]:
    if sha(data)==row['expected_sha256']:found=(rev,label,data);break
   if found:break
  assert found,('Historical authoring source hash not recoverable',key);rev,label,data=found;selected=HISTORY/(row['expected_sha256']+'.md')
  if selected.exists():assert selected.read_bytes()==data
  else:selected.write_bytes(data)
  source=dict(kind='Exact historical authoring text recovered from version control',commit=rev,git_path=row['path'],byte_mapping=label,selected=ref(selected))
 pins.append(dict(origin=row['origin'],recorded_path=row['path'],expected_sha256=row['expected_sha256'],resolved=ref(selected),provenance=source,scope='Historical authoring provenance only; current skill/registry intentionally advanced. Never use this recovered text as active instructions or a current asset binding.'))
(OUT/'historical-reference-pins.json').write_text(json.dumps(dict(pins=pins,purpose='Exact historical context in immutable NPC lineage; no current guidance/model rollback.'),indent=2)+'\n',encoding='utf-8',newline='\n');print('Pinned exact historical references:',len(pins))
