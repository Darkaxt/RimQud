"""Record Tam review while preserving exact constructor and historical instruction inputs."""
from pathlib import Path
import importlib.util,json,hashlib,subprocess
import numpy as np
from PIL import Image
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('tam_assembly_method',HERE/'assembly-method.py')
method=importlib.util.module_from_spec(spec);spec.loader.exec_module(method)
read,write,ref,digest,rgba,resolve,view,load=(getattr(method,n) for n in ['read','write','ref','digest','rgba','resolve','view','load'])
SIZE=method.SIZE

def historical_instruction(root,rel,expected):
    assert rel in ['skills/qud-creature-conversion/SKILL.md','skills/qud-creature-conversion/references/apparel-fitting.md']
    if expected in ['74d6f7498dad0e0079c152649b2b40143cbf201a748b48d0a5cd110a73975af2','3549a1e4702f4b24dfcea5238880d092ef84a5809bd07bdcb6ececbf601f1f13']:
        commit='dde9ca991c35ddef2b47a970a571d696ee0443bb';transformation='Unmodified Git blob'
    else:
        assert rel.endswith('/SKILL.md') and expected in ['0168b8e281b81f758c01cd3c2256a0193d6305aad65cd9eae699b3c1d317c414','10f273adafdd19c554bc4cf32f1beaa22bda03c8f929330fff19002d83b74add']
        commit='a2a8571e3b5af2276b163db10e94a647d91f0fac';transformation='Unmodified Git blob'
    data=subprocess.check_output(['git','show',commit+':'+rel],cwd=root)
    if expected=='10f273adafdd19c554bc4cf32f1beaa22bda03c8f929330fff19002d83b74add':
        start=data.index(b'The primary fitting/report composition');end=data.index(b'\nFor garments,',start)
        data=data[:start]+data[end:]
        transformation='Reconstruct intermediate instruction by removing the subsequently added single-item-preview paragraph from a2a8571. Reconstructed bytes match the original recorded SHA256 exactly; original event remains unchanged.'
    return commit,data,transformation

def record(root, ident, folder, review_path):
    assert not (folder/'authoring-review.json').exists()
    ledger, entry, source, actor, dependencies, body_key, body, items, fits, frame = resolve(root, ident)
    notes = read(review_path)
    assert notes['entry'] == ident and notes['captured_instance'] == actor['instance'] and notes['status'] == 'PASS'
    assert notes['reviewed_all_single_item_views'] and notes['reviewed_neutral_native_and_game_scale']
    model = read(folder/'model.json'); packet = read(folder/'source-packet.json'); lineage = read(folder/'dependency-lineage.json')
    verified = set(); historical = []
    old = {('skills/qud-creature-conversion/SKILL.md', '74d6f7498dad0e0079c152649b2b40143cbf201a748b48d0a5cd110a73975af2'), ('skills/qud-creature-conversion/references/apparel-fitting.md', '3549a1e4702f4b24dfcea5238880d092ef84a5809bd07bdcb6ececbf601f1f13')}
    def walk(v):
        if isinstance(v, dict):
            key = 'path' if 'path' in v else ('public_file' if 'public_file' in v else None)
            if key and 'sha256' in v:
                p = Path(v[key]); p = p if p.is_absolute() else root/p
                if digest(p) != v['sha256']:
                    rel = p.relative_to(root).as_posix()
                    commit, historical_bytes, transformation = historical_instruction(root, rel, v['sha256'])
                    assert hashlib.sha256(historical_bytes).hexdigest() == v['sha256']
                    resolved = dict(path=rel, sha256=v['sha256'], commit=commit, current_sha256=digest(p), url='https://github.com/Darkaxt/RimQud/blob/'+commit+'/'+rel, transformation=transformation)
                    if resolved not in historical: historical.append(resolved)
                verified.add(str(p))
            for x in v.values(): walk(x)
        elif isinstance(v, list):
            for x in v: walk(x)
    for value in [model, packet, lineage]: walk(value)
    assert model['body_model'] == dependencies[body_key][0]['current_registration']['model']
    assert not model['native_activation'] and not packet['native_activation']
    for f, current in model['views'].items():
        expected = Image.new('RGBA', SIZE)
        assert current['body']['components'] == view(body, f)[0] and current['body']['mirrored_from_east'] == view(body, f)[1]
        for r in current['body']['components']: expected.alpha_composite(load(root, r, current['body']['mirrored_from_east']))
        assert np.array_equal(np.array(expected), np.array(rgba(folder/f'base-{f}.png')))
        for binding in current['equipment']:
            part = next(p for p in actor['parts'] if p['id'] == binding['part_id'])
            assert (part['type'], part['laterality'], part['equipped']['instance']) == (binding['slot'], binding['laterality'], binding['instance'])
        n = np.array(rgba(folder/f'full-neutral-{f}.png'))
        assert np.array_equal(n[:, :, 0], n[:, :, 1]) and np.array_equal(n[:, :, 1], n[:, :, 2])
        assert not np.array(rgba(folder/f'hidden-{f}.png'))[:, :, 3].any()
    write(folder/'historical-instruction-versions.json', dict(verified=historical,rule='Original dependency events remain unchanged. Historical instruction bytes are verified in Git.'))
    now = datetime.now(timezone.utc).isoformat()
    write(folder/'authoring-review.json', dict(timestamp=now, **notes, checked_dependency_files=len(verified), new_imagegen_calls=0, native_activation=False, native_acceptance=model['native_acceptance']))
    write(folder/'artifact-manifest.json', dict(artifacts=[ref(root, p) for p in sorted(folder.rglob('*')) if p.is_file() and p != folder/'artifact-manifest.json']))
    slug = lambda s: s.lower().replace(' ', '-').replace('/', '-')
    def event(step, action, outputs, review, result='PASS'):
        entry['process_log'].append(dict(timestamp=now, step=step, action=action, inputs=[ref(root, folder/'model.json')], outputs=[ref(root, folder/n) for n in outputs], review=review, result=result))
    event(entry['required_steps'][3], 'Inspect all four directions and every actual item separately on the unclothed fixed body, then the complete outfit.', [slug(n)+'-comparison.png' for n in items]+['full-neutral-comparison.png'], notes['summary'])
    event(entry['required_steps'][4], 'Inspect exact independent source palettes, original registration and game-size full assembly.', ['record-review.py', 'full-native-comparison.png', 'game-scale-comparison.png', 'hidden-comparison.png', review_path.name, 'historical-instruction-versions.json', 'authoring-review.json', 'artifact-manifest.json'], notes['palette_and_scale'])
    event(entry['required_steps'][5], 'Keep native visibility/equipment/hurt/look/save and supported held-state acceptance behind the complete generation gate.', [], 'Static authoring only. Empty hidden preview is not a native visibility test. No game launch or harness validation. Entry remains UNFINISHED pending integrated Stage3 acceptance.', 'DEFERRED UNTIL ALL GENERATED')
    entry.update(status='UNFINISHED', generation_ready=True, current_step=entry['required_steps'][-1], known_issues=[], current_registration=dict(model=ref(root, folder/'model.json'), plate=ref(root, folder/'full-neutral-comparison.png')),
                 registration_summary='Captured actor'+str(actor['instance'])+' assembled from its unchanged shared dromad body and exact source-equipped items. Each item remains independent; neutral/native palettes, single-item/staged views and complete dependency histories are recorded. Static display only; native acceptance pending.',
                 art_review=dict(status='PASS', reason=notes['summary'], record=ref(root, folder/'authoring-review.json')))
    if entry.get('apparel_dependencies'): entry['apparel_dependencies']['status'] = 'Current generation-ready fittings and exact instance/part bindings verified in this static assembly. Native outfit acceptance pending.'
    following = next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'))
    assert following['status'] == 'UNFINISHED'
    following.update(status='IN PROGRESS', current_step=following['required_steps'][0])
    ledger.update(active_entry=following['id'], updated_at=now)
    assert sum(e['status'] == 'IN PROGRESS' for e in ledger['entries']) == 1
    write(root/'evidence/conversion-ledger.json', ledger)
    print(json.dumps(dict(entry=ident, generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']), total=len(ledger['entries']), active_entry=following['id'], verified_dependency_files=len(verified), native_acceptance='pending')))

if __name__=='__main__':
    record(ROOT,'NPC-TAM',HERE,HERE/'visual-review-notes.json')
