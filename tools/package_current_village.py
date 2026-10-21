"""Stage the ledger-selected village assets for the complete-set native adapter.

This is a copy-only integration input: no generation, model fitting, state
selection, profile installation, game launch or native acceptance happens here.
The original selected model documents retain their exact bytes. The runtime can
resolve their public PNG references through the package's explicit asset index.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from package_village import topology

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / 'evidence/generation-gate-reconciliation-20261021/generation-gate.json'
FIXED_FAMILIES = {
    'Tam': 'dromad', 'Ctesiphus': 'ray-cat', 'Glowfish': 'glowfish',
    'ElderBob': 'irudad', 'Nima Ruda': 'nima', 'Warden Yrame': 'yrame',
}
BODY_FAMILIES = {
    'BODY-IRUDAD': 'irudad', 'BODY-NIMA': 'nima', 'BODY-YRAME': 'yrame',
}
# These three selected assembly procedures directly compose recorded depth
# layers. The remaining captured outfits use per-item late ownership. Keep the
# bounded native integration decision explicit instead of parsing prose as code.
DEPTH_ASSEMBLIES = {'NPC-CTESIPHUS', 'NPC-GLOWFISH', 'NPC-WARDEN-YRAME'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def verified(reference):
    path = (REPO / reference['path']).resolve()
    assert path.is_relative_to(REPO), reference
    data = path.read_bytes()
    assert sha(data) == reference['sha256'].lower(), reference
    return data


def image_references(value):
    """Read explicit hashed references, never infer production art from names."""
    if isinstance(value, dict):
        path = value.get('public_file') or value.get('path')
        if isinstance(path, str) and Path(path).suffix.lower() == '.png' and value.get('sha256'):
            yield dict(path=path, sha256=value['sha256'].lower())
        for child in value.values():
            yield from image_references(child)
    elif isinstance(value, list):
        for child in value:
            yield from image_references(child)


def prepare_cast(output, version):
    """Preserve the reviewed assembly transforms, especially explicit west art."""
    output = output.resolve()
    assert output.parent == Path('E:/Temp').resolve()
    assert output.name.startswith('qud-transplant-probe-')
    target = output.resolve() / 'selected'
    package_path = target / 'package.json'
    staged = read(package_path)
    ledger = read(target / 'ledger.json')
    assert sha((target / 'ledger.json').read_bytes()) == staged['ledger']['sha256']
    index = {entry['id']: entry for entry in ledger['entries']}
    sources = json.loads(verified(staged['actor_source']))
    captured = {native['instance']: (actor, native) for actor in sources['actors'] for native in actor['native_instances']}

    def model_for(ident):
        ref = staged['entries'][ident]['model']
        blob = (target / ref['package_file']).read_bytes()
        assert sha(blob) == ref['sha256']
        return json.loads(blob)

    def layer(row, mirror, item_key=None):
        copied = dict(row)
        image = staged['assets'][row['public_file']]
        assert image['sha256'] == row['sha256']
        copied['file'] = 'selected/' + image['package_file']
        # mirrored_from_east on a saved west PNG describes its provenance; it
        # does not request another mirror. Only the assembly operation does.
        copied['assembly_mirror'] = bool(mirror)
        if item_key:
            copied['equipment_key'] = item_key
        for name in ['size', 'contact', 'width', 'height', 'center_x', 'center_z', 'layer', 'color_role']:
            assert name in copied, (row['public_file'], name)
        return copied

    cast = {}
    for ident, reference in staged['assemblies'].items():
        entry = index[ident]
        model = model_for(ident)
        metadata = entry['metadata']
        instance = metadata['captured_instance']
        actor, native = captured[instance]
        assert metadata['native_parts'] == native['parts'], ident
        depth_composition = ident in DEPTH_ASSEMBLIES
        mode = 'authored_depth_layers' if depth_composition else 'per_item_late_ownership'
        views = {}
        for facing in ['south', 'east', 'north', 'west']:
            source = model['views'][facing]
            body = source['body']
            if isinstance(body, dict):
                body_rows = body['components']
                body_mirror = body.get('mirrored_from_east', False)
            else:
                body_rows = body
                body_mirror = source.get('body_mirror', False)
            rows = [layer(row, body_mirror) for row in body_rows]
            gear_groups = []
            for gear in source['equipment']:
                blueprint = gear.get('blueprint') or gear.get('name') or gear.get('captured_item', {}).get('blueprint')
                if not blueprint:
                    blueprint = model_for(gear['entry'])['blueprint']
                key = blueprint.lower().replace(' ', '-') + '@' + gear['slot'] + '@' + str(gear['laterality'])
                components = gear.get('components', gear.get('rows'))
                assert components is not None, (ident, blueprint)
                prepared = [layer(row, row.get('needs_assembly_mirror', gear.get('mirrored_from_east', False)), key) for row in components]
                rows.extend(prepared)
                gear_groups.append(dict(blueprint=blueprint, slot=gear['slot'], laterality=gear['laterality'], key=key, layers=prepared))
            ordered = sorted(rows, key=lambda row: row['layer'])
            for rank, row in enumerate(ordered):
                row['authored_layer'] = row['layer']
                row['layer'] = rank * .00001
            body_layers = [row for row in ordered if not row.get('equipment_key')]
            sequence = []
            if not depth_composition:
                far, near, worn, floating = [], [], [], []
                for gear in gear_groups:
                    primary = next(row for row in gear['layers'] if row['component'] == 'item')
                    operation = dict(
                        kind='item', key=gear['key'], slot=gear['slot'], components=gear['layers'],
                        color_composition='One primary alpha; min(detail_alpha,primary_alpha) partitions primary/detail premultiplied contributions; divide once by primary alpha.',
                        ownership='Multiply only this item alpha by (1-body_overlay_alpha) at composition. Never paint that overlay above unrelated items.',
                    )
                    if gear['slot'] == 'Hand':
                        (far if primary['authored_layer'] < 0 else near).append(operation)
                    elif gear['slot'] == 'Floating Nearby':
                        floating.append(operation)
                    else:
                        worn.append(({'Body': 0, 'Feet': 1, 'Head': 2, 'Face': 3}[gear['slot']], operation))
                sequence = far + [dict(kind='body', components=body_layers)] + [op for _, op in sorted(worn, key=lambda pair: pair[0])] + near + floating
            views[facing] = dict(body=body_layers, equipment=gear_groups, composition_mode=mode)
            if depth_composition:
                views[facing]['layers'] = ordered
            else:
                views[facing]['draw_sequence'] = sequence
        cast[ident] = dict(
            model=reference, blueprint=actor['creature'], captured_instance=instance,
            gender=native['gender'], species=actor['race'], anatomy=native['anatomy'],
            expected_topology=topology(native), views=views,
            body_model=model['body_model'],
            selection='Match native blueprint/gender/topology and compatible actual item/slot signatures. Captured instance is provenance, not a fresh-game ID requirement.',
        )
    assert len(cast) == 16
    result = dict(
        package_sha256=sha(package_path.read_bytes()), ledger=staged['ledger'], cast=cast,
        state='CURRENT CAST INPUTS PREPARED; NATIVE RENDERING, EQUIP AND LIFECYCLE ACCEPTANCE PENDING',
        mirror_policy='Explicit west pixels stay explicit; only recorded assembly mirror operations are applied. Native HFlip remains a separate final appearance transform.',
        depth_policy='Use each reviewed assembly procedure: stable depth layers where explicitly authored, otherwise far items, body, ordered worn items, near items and floating gear. Rank draw order within the actor; preserve contact and scale exactly.',
        native_activation=False, native_acceptance=False,
    )
    out = target / ('cast.json' if version == 1 else f'cast-v{version}.json')
    assert not out.exists(), 'Retain prior cast preparation evidence.'
    out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Prepared all16 current cast assemblies, including explicit west operations and actual equipment groups. Native acceptance remains pending.')
    return result


def package(output):
    output = output.resolve()
    # This is the existing probe's isolated scratch contract, not a normal mod.
    assert output.parent == Path('E:/Temp').resolve()
    assert output.name.startswith('qud-transplant-probe-')
    target = output / 'selected'
    assert not (target / 'package.json').exists(), 'Use a fresh package directory; retain prior evidence.'
    ledger_path = REPO / 'evidence/conversion-ledger.json'
    ledger_bytes = ledger_path.read_bytes()
    ledger = json.loads(ledger_bytes)
    gate = read(GATE)
    assert gate['ledger_sha256'] == sha(ledger_bytes)
    assert gate['status'] == 'GENERATION GATE PASS / NATIVE INTEGRATION AND ACCEPTANCE UNFINISHED'
    assert ledger['active_entry'] is None and all(e.get('generation_ready') for e in ledger['entries'])
    assert {e['entry'] for e in gate['entries']} == {e['id'] for e in ledger['entries']}

    assets = {}
    documents = {}
    entries = {}
    bodies = {}
    equipment = {}
    exclusions = {}
    scenery = {}
    assemblies = {}
    for entry in ledger['entries']:
        ident = entry['id']
        reference = entry.get('current_registration', {}).get('model')
        record = dict(category=entry['category'], related_entries=entry['related_entries'])
        if reference:
            data = verified(reference)
            model = json.loads(data)
            filename = reference['sha256'] + '.json'
            documents[filename] = data
            record['model'] = dict(**reference, package_file='models/' + filename)
            for image in image_references(model):
                blob = verified(image)
                previous = assets.get(image['path'])
                assert previous is None or previous['sha256'] == image['sha256'], image['path']
                assets[image['path']] = dict(**image, package_file='images/' + image['sha256'] + '.png', bytes=len(blob))
            if ident.startswith('BODY-'):
                family = BODY_FAMILIES.get(ident, model.get('family'))
                assert family and family not in bodies, ident
                bodies[family] = ident
            elif ident.startswith('FIT-'):
                family = model['family']
                key = model['blueprint'].lower().replace(' ', '-') + '@' + model['slot'] + '@' + str(model['laterality'])
                assert key not in equipment.setdefault(family, {}), ident
                equipment[family][key] = ident
            elif entry['category'] in ['NPC assemblies', 'Creatures']:
                assemblies[ident] = record['model']
            elif ident.startswith('SCN-') or ident in ['SCOPE-DIRTY', 'SCOPE-PONDDOWN']:
                scenery[ident] = record['model']
        elif entry['category'] == 'Equipment inventory':
            fittings = [key for key in entry['related_entries'] if key.startswith('FIT-')]
            assert fittings, ident
            record['inventory_aggregate'] = dict(fittings=fittings, note='Use the selected per-body fitting models; this inventory row has no separate runtime graphic.')
        else:
            reference = entry['scope_review']
            data = verified(reference)
            assert read(REPO / reference['path'])['effective_render']['Visible'] == 'false', ident
            filename = reference['sha256'] + '.json'
            documents[filename] = data
            record['exclusion'] = dict(**reference, package_file='models/' + filename)
            exclusions[ident] = record['exclusion']
        entries[ident] = record

    sources_ref = dict(path='art/village/sources.json', sha256=sha((REPO / 'art/village/sources.json').read_bytes()))
    sources = json.loads(verified(sources_ref))
    actors = {}
    for actor in sources['actors']:
        native = actor['native_instances'][0]
        family = FIXED_FAMILIES.get(actor['creature'], 'human')
        assert family in bodies or family == 'human' and {'human-male', 'human-female'} <= set(bodies)
        actors[actor['creature']] = dict(
            family=family, anatomy=native['anatomy'], species=actor['race'],
            expected_topology=topology(native),
            family_selection='native captured gender' if family == 'human' else 'explicit captured named/species family',
        )
    assert len(actors) == 10

    result = dict(
        schema=1,
        state='SELECTED INPUTS STAGED; CURRENT NATIVE ADAPTER AND COMPLETE-SET ACCEPTANCE PENDING',
        ledger=dict(path='evidence/conversion-ledger.json', sha256=sha(ledger_bytes)),
        generation_gate=dict(path=GATE.relative_to(REPO).as_posix(), sha256=sha(GATE.read_bytes())),
        actor_source=sources_ref,
        entries=entries, actors=actors, bodies=bodies, equipment=equipment,
        scenery=scenery, assemblies=assemblies, exclusions=exclusions, assets=assets,
        runtime_contract=dict(
            native_visibility=True, native_state_selection=True, native_palette=True,
            native_inventory_and_body=True, unknown_states='native fallback',
            retained_extra_views='authoring/diagnostic only unless an existing native selector requires them',
            unbound_age_templates='diagnostic only; no invented native life-stage selector',
            body_masks='separate, applied after fitting; preserve intact garments',
        ),
        native_activation=False, native_acceptance=False,
    )
    # Only materialize after the full read/identity preflight succeeds.
    (target / 'models').mkdir(parents=True, exist_ok=True)
    (target / 'images').mkdir(exist_ok=True)
    for filename, data in documents.items():
        (target / 'models' / filename).write_bytes(data)
    for row in assets.values():
        destination = target / row['package_file']
        if destination.exists():
            assert sha(destination.read_bytes()) == row['sha256']
        else:
            shutil.copyfile(REPO / row['path'], destination)
        assert sha(destination.read_bytes()) == row['sha256']
    for filename, data in documents.items():
        assert (target / 'models' / filename).read_bytes() == data
    (target / 'ledger.json').write_bytes(ledger_bytes)
    (target / 'generation-gate.json').write_bytes(GATE.read_bytes())
    (target / 'package.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f'Staged {len(entries)} ledger entries, {len(documents)} exact model/exclusion documents, {len(assets)} PNG references.')
    print('No game activation or native acceptance. Package:', target / 'package.json')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--prepare-cast', action='store_true', help='Prepare cast transforms from an already staged exact package; does not launch Qud.')
    parser.add_argument('--cast-version', type=int, default=2, help='Explicit immutable cast preparation version; previous diagnostics are retained.')
    args = parser.parse_args()
    if args.prepare_cast:
        assert args.cast_version >= 2, 'Version1 simple-stack preparation is rejected; retain it only as diagnostic evidence.'
        prepare_cast(args.root, args.cast_version)
    else:
        package(args.root)
