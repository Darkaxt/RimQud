"""Reconcile the current outfit after its sole robe ownership correction."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
def arr(p):return np.array(Image.open(p).convert('RGBA'))
assert not (HERE/'authoring-review.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='NPC-ELDERBOB'
e=next(e for e in l['entries'] if e['id']==l['active_entry']);idx={e['id']:e for e in l['entries']}
m=read(HERE/'model.json');old=read(HERE.parent/'v1/model.json');body=read(ROOT/m['body_model']['path'])
assert m['body_model']==old['body_model'] and m['registration']==old['registration']
expected={'Black Robes':(539,196,'Body',0),'Spectacles':(540,198,'Face',0),'Walking Stick':(541,201,'Hand',6),'Sandals':(546,213,'Feet',0)}
assert {n:(b['equipped_instance'],b['part_id'],b['slot'],b['laterality']) for n,b in m['equipment_bindings'].items()}==expected
for ident in e['related_entries']:
    d=idx[ident];assert d['generation_ready'] and ref(ROOT/d['current_registration']['model']['path'])==d['current_registration']['model']
checks={}
for face,view in m['views'].items():
    assert view['body']==body['views'][face]
    canvas=Image.new('RGBA',(512,1264))
    for r in view['body']:
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];canvas.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    assert np.array_equal(np.array(canvas),arr(HERE/f'base-{face}.png'))
    assert np.array_equal(arr(HERE/f'base-{face}.png'),arr(HERE.parent/f'v1/base-{face}.png'))
    for binding in view['equipment']:
        for r in binding['components']:
            assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
            source=Image.open(ROOT/r['source_component']['path']).convert('RGBA')
            if r['mirrored_from_east']:source=ImageOps.mirror(source)
            padded=arr(ROOT/r['public_file']);assert np.array_equal(padded[240:],np.array(source)) and not padded[:240].any()
            assert r['size']==[512,1264] and r['contact']==[256,1190]
    for label in ['spectacles','walking-stick','sandals']:
        assert np.array_equal(arr(HERE/f'{label}-{face}.png'),arr(HERE.parent/f'v1/{label}-{face}.png'))
    if face in ['south','north']:
        assert np.array_equal(arr(HERE/f'full-neutral-{face}.png'),arr(HERE.parent/f'v1/full-neutral-{face}.png'))
        assert np.array_equal(arr(HERE/f'full-native-{face}.png'),arr(HERE.parent/f'v1/full-native-{face}.png'))
    neutral=arr(HERE/f'full-neutral-{face}.png');assert not np.ptp(neutral[:,:,:3].astype(int),axis=2).any()
    checks[face]=dict(body_exact=True,padded_components_exact=True,unrelated_single_items_exact=True,front_back_unchanged=face in ['south','north'])
assert not m['native_activation']
reason='Inspected refreshed single-robe, complete neutral/native outfit and intended-size views. Corrected robe ownership removes the profile hand crescent while retaining wrist/cuff contact. Current original named body/mutations, spectacles, sandals, walking-stick source/grip, slot bindings and physical frame are unchanged. Exact pixel checks show unchanged front/back full assemblies and all unrelated single-item previews. Complete source garment remains separate. Static display pose only; native equip/unequip, mutation/held-state and animation acceptance remain behind the full generation gate.'
now=datetime.now(timezone.utc).isoformat()
write(HERE/'authoring-review.json',dict(status='PASS',scope='Generation authoring only',reason=reason,checks=checks,
    supersedes=ref(HERE.parent/'v1/model.json'),corrected_fitting=idx['FIT-IRUDAD-BLACK-ROBES-BODY-0']['current_registration'],native_acceptance=m['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
for step in e['required_steps']:
    native=step.startswith('native_')
    e['process_log'].append(dict(timestamp=now,step=step,action='Refresh the exact captured outfit from current dependencies and inspect the corrected ownership.' if not native else 'Retain native acceptance behind the full generation gate.',
        inputs=[ref(HERE.parent/'v1/model.json'),idx['FIT-IRUDAD-BLACK-ROBES-BODY-0']['current_registration']['model']],
        outputs=[] if native else [ref(HERE/'model.json'),ref(HERE/'full-neutral-comparison.png'),ref(HERE/'full-native-comparison.png'),ref(HERE/'authoring-review.json')],review=reason,result='DEFERRED UNTIL ALL GENERATED' if native else 'PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step=e['required_steps'][-1],known_issues=[],
    current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'full-neutral-comparison.png')),
    art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),
    registration_summary='Current separate Irudad body/mutations and four exact equipment bindings, with corrected side robe hand ownership. Native acceptance pending.')
e.pop('advancement_blocker',None)
resolved=['FIT-YRAME-HORNS-HEAD-0','FIT-IRUDAD-BLACK-ROBES-BODY-0']
q=l['current_structural_correction_queue'];q['ordered_entries']=[x for x in q['ordered_entries'] if x not in resolved]
records=l.setdefault('resolved_structural_corrections',[])
records.append(dict(recorded_at=now,entry='FIT-IRUDAD-BLACK-ROBES-BODY-0',reason=reason,fit=idx['FIT-IRUDAD-BLACK-ROBES-BODY-0']['current_registration'],aggregate=idx['ITEM-BLACK-ROBES']['current_item_manifest'],assembly=e['current_registration']))
n=idx['SCN-DOOR'];assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);l.update(active_entry=n['id'],updated_at=now)
assert sum(x['status']=='IN PROGRESS' for x in l['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',l)
print('Irudad generation assembly refreshed; SCN-DOOR sole active entry. Native acceptance pending.')
