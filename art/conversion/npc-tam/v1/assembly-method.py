"""Compose captured Tam from current dromad body and both real items from generation-ready body/item records.

Art authoring only: exact existing components, independent item ownership/palettes,
single-item evidence and lazy-report lineage. Review is a separate explicit action.
"""
from pathlib import Path
from datetime import datetime, timezone
from html import escape
import argparse, hashlib, json, shutil, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

FACES = ['south', 'east', 'north', 'west']
SIZE = (512, 1024)
CONTACT = [256, 950]

def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def write(path, data): path.write_bytes((json.dumps(data, indent=2, ensure_ascii=False)+'\n').encode())
def rgba(path): return Image.open(path).convert('RGBA')
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def ref(root, path): return dict(path=path.relative_to(root).as_posix(), sha256=digest(path))
def view(model, facing):
    if facing in model['views']: return model['views'][facing], False
    assert facing == 'west' and 'east' in model['views']
    return model['views']['east'], True
def load(root, row, mirror):
    image = rgba(root/row['public_file'])
    return ImageOps.mirror(image) if mirror else image

def resolve(root, ident):
    ledger = read(root/'evidence/conversion-ledger.json')
    assert ledger['stage'] == 'Stage 3 ACTIVE' and ledger['active_entry'] == ident
    entry = next(e for e in ledger['entries'] if e['id'] == ident)
    assert entry['category'] == 'NPC assemblies' and entry['status'] == 'IN PROGRESS'
    sources = read(root/'art/village/sources.json')
    source = next(r for r in sources['actors'] if r['creature'] in entry['source_targets'])
    actor = next(a for a in source['native_instances'] if a['instance'] == entry['metadata']['captured_instance'])
    assert actor['parts'] == entry['metadata']['native_parts']
    assert sources['runtime_catalogue_sha256'] == entry['metadata']['source_snapshot']
    assert ident == 'NPC-TAM' and actor['instance'] == 525
    assert actor['species'] == 'dromad' and actor['anatomy'] == 'Humanoid'
    assert not any(p['manager'] for p in actor['parts']), 'Mutation-managed anatomy requires its own source-bound assembly.'
    assert len([p for p in actor['parts'] if p['type'] == 'Arm']) == 2
    dependencies = {}
    for key in entry['related_entries']:
        dep = next(e for e in ledger['entries'] if e['id'] == key)
        assert dep.get('generation_ready'), key
        record = dep['current_registration']['model']
        assert digest(root/record['path']) == record['sha256']
        model = read(root/record['path'])
        for rows in model['views'].values():
            for row in rows:
                assert digest(root/row['public_file']) == row['sha256']
                assert row['size'] == list(SIZE) and row['contact'] == CONTACT
        dependencies[key] = (dep, model)
    body_keys = [k for k in dependencies if k.startswith('BODY-')]
    assert len(body_keys) == 1 and body_keys[0] == 'BODY-DROMAD'
    body_key = body_keys[0]
    assert actor['gender'] == 'male'
    body = dependencies[body_key][1]
    items = {p['equipped']['blueprint']: (p, p['equipped']) for p in actor['parts'] if p.get('equipped')}
    fits = {m['blueprint']: (dep, m) for key, (dep, m) in dependencies.items() if key != body_key}
    assert set(items) == set(fits) == {'Cloth Robe', 'Shillelagh'}
    assert [(items[n][1]['instance'], items[n][0]['id']) for n in ['Cloth Robe','Shillelagh']] == [(604,357),(524,362)]
    frame = {k: body['views']['south'][0][k] for k in ['size', 'contact', 'width', 'height', 'center_x', 'center_z']}
    for name, (_, model) in fits.items():
        part, item = items[name]
        assert (model['slot'], model['laterality']) == (part['type'], part['laterality'])
        assert model['slot'] in ['Body', 'Feet', 'Head', 'Face', 'Hand']
        for rows in model['views'].values():
            for row in rows: assert {k: row[k] for k in frame} == frame
    return ledger, entry, source, actor, dependencies, body_key, body, items, fits, frame

def construct(root, ident, folder):
    assert not (folder/'model.json').exists(), 'Do not overwrite existing assembly evidence.'
    data = resolve(root, ident)
    ledger, entry, source, actor, dependencies, body_key, body, items, fits, frame = data
    folder.mkdir(parents=True, exist_ok=True)
    assert Path(__file__).resolve() == (folder/'assembly-method.py').resolve()
    palette = read(root/'evidence/joppa-anatomy-study.json')['native_palette']
    color = lambda c: np.frombuffer(bytes.fromhex(palette[c.replace('&', '').replace('^', '')[0]]), dtype=np.uint8)
    def body_layer(row, mirror, native):
        im = load(root, row, mirror)
        if not native: return im
        a = np.array(im)
        a[:, :, :3] = np.uint8(np.round(a[:, :, :3].astype(float).mean(2)[:, :, None]*color(actor['detailColor'] if row.get('color_role') == 'detail' else (actor.get('tileColor') or actor['foreground']))/255))
        a[a[:, :, 3] == 0, :3] = 0
        return Image.fromarray(a)
    def item_layer(name, facing, native):
        rows, mirror = view(fits[name][1], facing)
        primary = next(r for r in rows if r['component'] == 'item')
        a = np.array(load(root, primary, mirror)).astype(float)
        alpha = a[:, :, 3]/255
        detail = next((r for r in rows if r['component'] == 'item-detail'), None)
        d = np.array(load(root, detail, mirror)).astype(float) if detail else np.zeros_like(a)
        da = np.minimum(d[:, :, 3]/255, alpha)
        item = items[name][1]
        pc = color(item.get('tileColor') or item['foreground']) if native else np.array([255, 255, 255])
        dc = color(item.get('detailColor') or item.get('tileColor') or item['foreground']) if native else np.array([255, 255, 255])
        premul = a[:, :, :3]*pc/255*(alpha-da)[:, :, None] + d[:, :, :3]*dc/255*da[:, :, None]
        out = np.zeros_like(a, dtype=np.uint8)
        out[:, :, :3] = np.uint8(np.clip(np.round(np.divide(premul, alpha[:, :, None], out=np.zeros_like(premul), where=alpha[:, :, None] > 0)), 0, 255))
        out[:, :, 3] = np.uint8(np.round(alpha*255))
        overlay = next((r for r in rows if r['component'] == 'body-overlay'), None)
        if overlay:
            ownership = np.array(load(root, overlay, mirror))[:, :, 3].astype(float)/255
            out[:, :, 3] = np.uint8(np.round(out[:, :, 3].astype(float)*(1-ownership)))
        out[out[:, :, 3] == 0, :3] = 0
        return Image.fromarray(out), primary['layer']
    def compose(facing, native=False, enabled=None):
        enabled = list(items) if enabled is None else enabled
        far, near, worn = [], [], []
        for name in enabled:
            im, depth = item_layer(name, facing, native)
            slot = fits[name][1]['slot']
            if slot == 'Hand': (far if depth < 0 else near).append(im)
            else: worn.append(({'Body': 0, 'Feet': 1, 'Head': 2, 'Face': 3}[slot], im))
        out = Image.new('RGBA', SIZE)
        for im in far: out.alpha_composite(im)
        rows, mirror = view(body, facing)
        for row in sorted(rows, key=lambda r: r['layer']): out.alpha_composite(body_layer(row, mirror, native))
        for _, im in sorted(worn, key=lambda x: x[0]): out.alpha_composite(im)
        for im in near: out.alpha_composite(im)
        return out
    slug = lambda s: s.lower().replace(' ', '-').replace('/', '-')
    groups = {key: {} for key in ['base', 'worn', 'full-neutral', 'full-native', 'hidden']+list(items)}
    for facing in FACES:
        cases = [('base', False, []), ('worn', False, [n for n in items if fits[n][1]['slot'] != 'Hand']), ('full-neutral', False, None), ('full-native', True, None)]
        cases += [(name, False, [name]) for name in items]
        for key, native, enabled in cases:
            im = compose(facing, native, enabled)
            im.save(folder/f'{slug(key)}-{facing}.png')
            groups[key][facing] = im
        hidden = Image.new('RGBA', SIZE)
        hidden.save(folder/f'hidden-{facing}.png')
        groups['hidden'][facing] = hidden
    lineage = [dict(entry=key, model=dep['current_registration']['model'], report='docs/conversion-entries/'+key+'.html',
                    plate=dep['current_registration']['plate'], reused_generation_evidence=dep['process_log'], new_imagegen_calls=0)
               for key, (dep, _) in dependencies.items()]
    write(folder/'dependency-lineage.json', dict(dependencies=lineage, rule='Reuse exact earlier source/reference/manual/refinement/secondary/patch/extraction histories; no new body, profession pose, costume or ImageGen call.'))
    original = next(r for r in read(root/'evidence/village-reference-index.json')['entries'] if r['blueprint'] == actor['blueprint'])
    mask = Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'].replace('-reference', '-mask')
    assert digest(mask) == original['native_mask_sha256']
    bindings = {name: dict(entry=fits[name][0]['id'], model=fits[name][0]['current_registration']['model'],
                          instance=item['instance'], part_id=p['id'], parent=p['parent'], slot=p['type'], laterality=p['laterality'], manager=p['manager'], captured_item=item)
                for name, (p, item) in items.items()}
    packet = dict(entry=ident, source=ref(root, root/'art/village/sources.json'), source_snapshot=entry['metadata']['source_snapshot'],
                  identity_chain=source['lineage'], race_description=source['race_input'], captured_actor=actor,
                  original=dict(**original, private_mask=dict(path=mask.as_posix(), sha256=digest(mask))),
                  body_model=dependencies[body_key][0]['current_registration']['model'], equipment_bindings=bindings,
                  frame=frame, new_imagegen_calls=0, method=ref(root, folder/'assembly-method.py'),
                  boundaries=dict(anatomy='Captured ordinary Humanoid attached tree; unavailable active mutation list/age are unknown, not inferred.',
                                  description='Keep full prose as metadata. Do not invent a profession costume, biological skin color, personal cosmetics or unexported equipment from that prose. Actual captured equipped items govern this assembly.',
                                  palette='Body authoring preview uses the captured actor Render palette, independently of each real item palette; this is not native biological skin metadata.',
                                  ownership='Late original-body coverage is local to each item. Retain whole item textures and full body; never draw a whole-body overlay above unrelated equipment.',
                                  pose='Existing stationary item display only; source-supported resting/ready grip/angle/native state acceptance waits for integrated Stage3 after full generation.'), native_activation=False)
    write(folder/'source-packet.json', packet)
    model = dict(entry=ident, kind='captured_actor_layered_assembly', source=ref(root, folder/'source-packet.json'), body_model=packet['body_model'], equipment_bindings=bindings,
                 views={f: dict(body=dict(components=view(body, f)[0], mirrored_from_east=view(body, f)[1]),
                                equipment=[dict(**bindings[n], components=view(fits[n][1], f)[0], mirrored_from_east=view(fits[n][1], f)[1]) for n in items],
                                neutral_preview=ref(root, folder/f'full-neutral-{f}.png'), native_palette_preview=ref(root, folder/f'full-native-{f}.png')) for f in FACES},
                 registration=frame, native_activation=False,
                 native_acceptance='Pending full-set generation gate: real visibility/equipment/near-far hands/held state/hurt/look/save-load. Static authoring only.')
    write(folder/'model.json', model)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
    for key, group in groups.items():
        out = Image.new('RGB', (1152, 680), '#142823'); d = ImageDraw.Draw(out)
        d.text((18, 15), ident+' / '+key+' / captured body and independent items', font=font, fill='#e3cf43')
        for i, (f, im) in enumerate(group.items()):
            x = 16+i*284; small = im.resize((256, 512), Image.Resampling.LANCZOS)
            out.paste(small, (x, 55), small); d.line((x+128, 55, x+128, 567), fill='#a39846'); d.line((x, 530, x+256, 530), fill='#75aaa0')
            d.text((x, 585), f.upper(), font=font, fill='#e3cf43')
        d.text((18, 625), 'Original body/items unchanged. Static display; native acceptance pending.', font=font, fill='#e5e8d8')
        out.save(folder/f'{slug(key)}-comparison.png')
    out = Image.new('RGB', (1152, 680), '#142823'); d = ImageDraw.Draw(out)
    d.text((18, 15), ident+' / source outfit assembly in stages', font=font, fill='#e3cf43')
    stages = [('BODY', []), ('BODY GARMENT', [n for n in items if fits[n][1]['slot'] == 'Body']),
              ('WORN', [n for n in items if fits[n][1]['slot'] != 'Hand']), ('FULL', None)]
    for i, (label, enabled) in enumerate(stages):
        im = compose('south', True, enabled).resize((256, 512), Image.Resampling.LANCZOS)
        out.paste(im, (16+i*284, 55), im); d.text((16+i*284, 585), label, font=font, fill='#e3cf43')
    d.text((18, 625), 'Same shared body; source-equipped items stay separate and independently tinted.', font=font, fill='#e5e8d8'); out.save(folder/'assembly-stages.png')
    out = Image.new('RGB', (800, 650), '#142823'); d = ImageDraw.Draw(out)
    d.text((18, 15), ident+' / 48x96 and nearest enlarged72x144', font=font, fill='#e3cf43')
    for j, key in enumerate(['full-neutral', 'full-native']):
        y = 65+j*285
        for i, (f, im) in enumerate(groups[key].items()):
            small = im.resize((48, 96), Image.Resampling.LANCZOS); out.paste(small, (20+i*200, y), small)
            large = small.resize((72, 144), Image.Resampling.NEAREST); out.paste(large, (95+i*200, y), large)
            d.text((20+i*200, y+185), f.upper(), font=font, fill='#e3cf43')
    d.text((18, 620), 'Neutral then actual independent Render palettes; native acceptance pending.', font=font, fill='#e5e8d8'); out.save(folder/'game-scale-comparison.png')
    a = np.array(rgba(mask)); w = a[:, :, :1].astype(float)/255
    original_image = Image.fromarray(np.dstack([np.uint8(np.round((1-w)*color(actor.get('tileColor') or actor['foreground'])+w*color(actor['detailColor']))), a[:, :, 3]]))
    out = Image.new('RGB', (1400, 850), '#142823'); d = ImageDraw.Draw(out)
    d.text((18, 15), ident+' / original > shared race/body > captured outfit', font=font, fill='#e3cf43')
    for im, x, y, size in [(original_image, 40, 90, (160, 240)), (groups['base']['south'], 340, 55, (240, 480)), (groups['full-neutral']['south'], 690, 55, (240, 480)), (groups['full-native']['south'], 1040, 55, (240, 480))]:
        small = im.resize(size, Image.Resampling.NEAREST if im is original_image else Image.Resampling.LANCZOS); out.paste(small, (x, y), small)
    for x, label in [(25, 'ORIGINAL SOURCE'), (325, 'SHARED BODY'), (670, 'NEUTRAL OUTFIT'), (1020, 'CAPTURED PALETTES')]: d.text((x, 575), label, font=font, fill='#e3cf43')
    for j, line in enumerate(['Actor'+str(actor['instance'])+' / '+actor['species']+' / '+actor['gender']+' / '+str(len(items))+' actual equipped objects; full description and parts retained.',
                               'Body and each item retain actual original, RimWorld reference, manual, refined and patched evidence in linked histories.',
                               'Canvas512x1024 / contact256,950 / unchanged physical source geometry and palettes. No new generation call.',
                               'Render palette is not biological skin metadata. Prose does not create extra items or a baked profession costume.',
                               'Stationary display only; native equip/visibility/pose/hurt/look/save acceptance waits for all generation.']):
        d.text((18, 635+j*32), line, font=font, fill='#e5e8d8')
    out.save(folder/'source-to-assembly.png')
    parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Captured resident conversion lineage</title><style>body{background:#142823;color:#e5e8d8;font:18px/1.6 Georgia,serif;max-width:1100px;margin:35px auto;padding:0 20px}a{color:#e3cf43}section{border-top:1px solid #526b5c;padding:20px 0}li{margin:10px 0}</style><h1>'+escape(ident)+': actual reused generation steps</h1><p>No new race body, costume or ImageGen call. The source descriptions, original shapes and actual references remain in these exact component histories.</p>']
    for dep in lineage:
        parts.append('<section><h2>'+escape(dep['entry'])+'</h2><p><a href="../../../../'+escape(dep['report'])+'">Full illustrated conversion history</a> · <a href="../../../../'+escape(dep['model']['path'])+'">Exact model</a></p><ol>')
        for event in dep['reused_generation_evidence']:
            links = ' · '.join('<a href="../../../../'+escape(r['path'])+'">'+escape(Path(r['path']).name)+'</a>' for r in event.get('outputs', []))
            parts.append('<li><strong>'+escape(event['step'].replace('_', ' '))+'</strong> — '+escape(event['result'])+'<br>'+escape(event['action'])+'<br>'+links+'</li>')
        parts.append('</ol></section>')
    parts.append('<p>Native acceptance remains pending the complete generation gate.</p></html>')
    (folder/'dependency-evidence.html').write_bytes(('\n'.join(parts)+'\n').encode())
    now = datetime.now(timezone.utc).isoformat()
    def event(step, action, outputs, review):
        entry['process_log'].append(dict(timestamp=now, step=step, action=action, inputs=[ref(root, root/'art/village/sources.json')],
                                        outputs=[ref(root, folder/n) for n in outputs], review=review, result='PASS'))
    assert not entry['process_log']
    event(entry['required_steps'][0], 'Resolve exact captured dromad instance, race, description, body tree, source shape/palette and actual equipped parts.', ['source-packet.json', 'source-to-assembly.png'], 'Actual export matches this ledger instance/body tree. No mutation or demographic change inferred; narrative-only cosmetics/props are retained as metadata rather than invented equipment.')
    event(entry['required_steps'][1], 'Verify the current body and all equipped fitting dependencies; preserve their performed generation histories.', ['dependency-lineage.json', 'dependency-evidence.html'], 'Every current model/component hash and physical frame matches. Natural default equipment and inventory do not become extra worn items; no new generation call.')
    event(entry['required_steps'][2], 'Compose exact separate body/item pixels with independent palettes and per-item late original-body ownership.', ['assembly-method.py', 'model.json', 'assembly-stages.png'], 'Far/near held depth follows current source fittings. No whole-body overlay can erase unrelated gear. These are source-bound static previews; visual review still pending.')
    entry['current_step'] = entry['required_steps'][3]; ledger['updated_at'] = now
    write(root/'evidence/conversion-ledger.json', ledger)
    print(json.dumps(dict(entry=ident, captured_instance=actor['instance'], items=list(items), outputs=folder.as_posix(), visual_review='PENDING', new_imagegen_calls=0)))

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
                    rel = p.relative_to(root).as_posix(); assert (rel, v['sha256']) in old, str(p)
                    commit = 'dde9ca991c35ddef2b47a970a571d696ee0443bb'
                    assert hashlib.sha256(subprocess.check_output(['git', 'show', commit+':'+rel], cwd=root)).hexdigest() == v['sha256']
                    resolved = dict(path=rel, sha256=v['sha256'], commit=commit, current_sha256=digest(p), url='https://github.com/Darkaxt/RimQud/blob/'+commit+'/'+rel)
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
    event(entry['required_steps'][4], 'Inspect exact independent source palettes, original registration and game-size full assembly.', ['full-native-comparison.png', 'game-scale-comparison.png', 'hidden-comparison.png', review_path.name, 'historical-instruction-versions.json', 'authoring-review.json', 'artifact-manifest.json'], notes['palette_and_scale'])
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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['construct','record'])
    parser.add_argument('--root',required=True,type=Path)
    parser.add_argument('--entry',required=True)
    parser.add_argument('--folder',required=True,type=Path)
    parser.add_argument('--review',type=Path)
    args=parser.parse_args();root=args.root.resolve();folder=(root/args.folder).resolve()
    assert folder.is_relative_to(root/'art/conversion')
    if args.action=='construct':construct(root,args.entry,folder)
    else:
        assert args.review
        review_path=(root/args.review).resolve();assert review_path.parent==folder
        record(root,args.entry,folder,review_path)

if __name__=='__main__':main()
