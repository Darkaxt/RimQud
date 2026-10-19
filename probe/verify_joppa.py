"""Verify the complete native-map experiment against actual frame and GPU output."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops


def read(root, name):
    return json.loads((root / name).read_text(encoding='utf-8'))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--output', type=Path)
    ap.add_argument('--stage', type=int, choices=[1, 3], default=1)
    args = ap.parse_args()
    root = args.root
    assert read(root, 'joppa-finished.json')['exitCode'] == 0
    scene = read(root, 'joppa-map.json')
    assert (scene['width'], scene['height'], scene['placements']) == (80, 25, 996)
    assert scene['fill'] == 'DirtFloor' and not scene['normalWorldGeneration']
    for name in ['Mehmet', 'Argyve', 'Tam', 'Warden Yrame', 'JoppaReshephShrine']:
        assert scene['objects'][name] == 1
    data = read(root, 'joppa-results.json')
    phases = ['baseline', 'liquid-depth-deep', 'liquid-depth-restored', 'actor-moved', 'visibility-changed', 'late-buffer-mutation',
              'replacement-disabled', 'unrelated-view', 'other-zone', 'zone-reentered', 'baseline-restored']
    if args.stage == 3:
        phases[1:1] = ['coverage-props-placed', 'coverage-props-south', 'coverage-props-east',
                       'coverage-props-north', 'coverage-unsupported-flip', 'coverage-props-restored',
                       'coverage-door-open', 'coverage-door-closed']
        launch = read(root, 'launch-joppa.json')
        assert launch['integrationStage'] == 3 and launch['mode'] == 'joppa'
        started = dt.datetime.fromisoformat(launch['start'].replace('Z', '+00:00')).timestamp()
        for name in ['joppa-finished.json', 'joppa-map.json', 'joppa-results.json', 'preservation.json']:
            assert (root/name).stat().st_mtime >= started, ('Stale', name)
    frames = data['frames']
    assert [f['phase'] for f in frames] == phases
    assert [f['generation'] for f in frames] == list(range(1, len(phases)+1))
    images, summaries = {}, []
    for f in frames:
        assert f['insideBufferLock'] and f['submittedHash'] == f['consumedHash']
        assert f['producerThread'] != f['consumerThread'] == 1
        assert len(f['cells']) == 2000
        assert len({(c['x'], c['y']) for c in f['cells']}) == 2000
        assert not any(c['mapped'] and (not c['visible'] or c['requiresOriginal']) for c in f['cells'])
        assert not any(c['source'] is not None for c in f['cells'] if not c['visible'])
        assert not any(c['waterLayer'] and (not c['visible'] or c['requiresOriginal']) for c in f['cells'])
        assert not any(c['grassDrawn'] and (not c['nativeGrassPaint'] or c['kind'] != 'ground') for c in f['cells'])
        pair = []
        for key in ['original', 'replacement']:
            if args.stage == 3:
                assert (root/f[key]).stat().st_mtime >= started, ('Stale image', f[key])
            with Image.open(root / f[key]) as image:
                assert image.size == (1920, 900)
                pair.append(image.convert('RGB'))
        images[f['phase']] = pair
        diff = ImageChops.difference(*pair)
        pixels = sum(pixel != (0, 0, 0) for pixel in diff.get_flattened_data())
        mapped = sum(f['mappedByKind'].values())
        if f['eligible']:
            assert mapped > 1500 and pixels > 500000
            assert f['mappedByKind']['wall'] == sum(f['wallMasks']) == (185 if args.stage == 3 else 161)
            assert f['mappedByKind']['crop'] >= 130
            assert f['grassClumps'] > 100 and f['waterLayerCells'] > 30
        else:
            assert mapped == 0 and pixels == 0 and f['originalFallbackCells'] == 2000
        summaries.append(dict(phase=f['phase'], generation=f['generation'], eligible=f['eligible'],
                              mapped_cells=mapped, original_cells=f['originalFallbackCells'],
                              mapped_by_kind=f['mappedByKind'], changed_pixels=pixels,
                              offscreen_capture_ms=f['offscreenMilliseconds'],
                              grass_clumps=f['grassClumps'], water_cells=f['waterLayerCells'],
                              shallow_water=f['shallowWaterCells'], deep_water=f['deepWaterCells'],
                              accepted_consumed_match=True, view=f['view']))
    by_phase = {f['phase']: f for f in frames}
    cell = lambda phase, x, y: by_phase[phase]['cells'][x + 80*y]
    assert cell('baseline', 40, 12)['source'] == 'WatervineFarmerJoppa'
    assert cell('actor-moved', 40, 12)['source'] != 'WatervineFarmerJoppa'
    assert cell('actor-moved', 41, 12)['source'] == 'WatervineFarmerJoppa'
    assert cell('baseline-restored', 40, 12)['source'] == 'WatervineFarmerJoppa'
    assert cell('late-buffer-mutation', 40, 12)['requiresOriginal']
    assert not cell('late-buffer-mutation', 40, 12)['mapped']
    assert all(not cell('visibility-changed', x, y)['mapped']
               for y in range(2, 6) for x in range(2, 10))
    assert by_phase['unrelated-view']['view'] == 'Popup:Text'
    assert not by_phase['other-zone']['eligible']
    assert by_phase['zone-reentered']['eligible']
    assert ImageChops.difference(images['baseline'][1], images['actor-moved'][1]).getbbox()
    assert ImageChops.difference(images['actor-moved'][1], images['visibility-changed'][1]).getbbox()
    baseline = by_phase['baseline']
    assert baseline['waterLayerCells'] == baseline['shallowWaterCells'] == 51
    assert baseline['deepWaterCells'] == 0
    assert by_phase['liquid-depth-deep']['deepWaterCells'] == 1
    assert by_phase['liquid-depth-restored']['deepWaterCells'] == 0
    assert ImageChops.difference(images['baseline'][1], images['liquid-depth-deep'][1]).getbbox()
    assert read(root, 'joppa-liquid-thresholds.json') == [
        dict(volume=199, wading=False, swimming=False), dict(volume=200, wading=True, swimming=False),
        dict(volume=1999, wading=True, swimming=False), dict(volume=2000, wading=True, swimming=True)]
    for c in baseline['cells']:
        if c['waterLayer']:
            assert 200 <= c['waterVolume'] < 2000 and c['waterDepth'] == 2
    # Actual GPU land centers should now have a clearly greener marsh base.
    green_ground = 0
    for c in baseline['cells']:
        if c['mapped'] and c['kind'] == 'ground' and not c['grassDrawn']:
            r, g, b = images['baseline'][1].getpixel((c['x']*24+12, c['y']*36+18))
            green_ground += g > r+5 and g > b+5
    assert green_ground > 300, green_ground
    preservation = read(root, 'preservation.json')
    assert preservation['preferences_restored'] and not preservation['changed_save_or_settings_files']
    result = dict(map='Joppa.rpm', dimensions=[80, 25], authored_placements=996,
                  normal_world_generation=False, background_fill='DirtFloor',
                  frames=summaries, preserved_saves_settings=True, unity_preferences_restored=True,
                  runtime_diagnostics=preservation['diagnostic_changes'],
                  gameplay_verified=False,
                  marsh_ground_centers_verified=green_ground,
                  liquid_depth_source='Qud IsWadingDepth / IsSwimmingDepth; all baseline cells are wading depth',
                  limitations=['Controlled native-map simulation during MainMenu boot',
                               'Shrine initialization requires missing world history',
                               'Original sprites retained for unmapped content',
                               'Capture timings include scene creation and PNG readback, not gameplay frame times'])
    result['images'] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                        for f in frames for name in (f['original'], f['replacement'])}
    if args.stage == 3:
        config = read(root, 'joppa-coverage.json')
        rules = {r['blueprint']: r for r in config['entries']}
        expected = {r['blueprint'] for r in config['entries'] if r['baseline_selected']}
        selected = {c['source'] for c in baseline['cells'] if c['source']}
        assert len(expected) == 67 and selected == expected
        decisions = []
        for name in sorted(expected):
            rule = rules[name]; hits = [c for c in baseline['cells'] if c['source'] == name]
            replaced = rule['render_kind'] != 'original'
            assert all(c['mapped'] == replaced for c in hits), name
            assert all(c['kind'] == rule['render_kind'] for c in hits), name
            decisions.append(dict(blueprint=name, decision=rule['decision'], reason=rule['reason'],
                mapped=replaced, selected_cells=len(hits), observed_tiles=sorted({c['tile'] for c in hits if c['tile']})))
        fixture = read(root, 'coverage-prop-fixture.json')
        assert set(fixture) == set(config['assets'])
        for family, identity in fixture.items():
            for name, facing in [('south', 2), ('east', 1), ('north', 0)]:
                hits = [c for c in by_phase['coverage-props-'+name]['cells'] if c['instance'] == identity]
                assert len(hits) == 1
                c = hits[0]
                assert c['mapped'] and c['kind'] == 'prop' and c['assetFamily'] == family and c['facing'] == facing
            original = next(c for c in baseline['cells'] if c['instance'] == identity)
            restored = next(c for c in by_phase['coverage-props-restored']['cells'] if c['instance'] == identity)
            assert (original['x'], original['y']) == (restored['x'], restored['y']) and restored['mapped']
        flipped = [c for c in by_phase['coverage-unsupported-flip']['cells'] if c['vFlip'] and c['instance'] in fixture.values()]
        assert len(flipped) == 1 and not flipped[0]['mapped'] and flipped[0]['foregroundLayers'] == 0
        opened = [c for c in by_phase['coverage-door-open']['cells'] if c['source'] == 'Door' and c['doorOpen']]
        assert opened
        for c in opened:
            closed = cell('coverage-door-closed', c['x'], c['y'])
            assert c['mapped'] and closed['mapped'] and not closed['doorOpen'] and c['tile'] != closed['tile']
            region = (max(0,c['x']*24-24), max(0,c['y']*36-36), min(1920,(c['x']+2)*24), min(900,(c['y']+2)*36))
            difference = ImageChops.difference(images['coverage-door-open'][1].crop(region), images['coverage-door-closed'][1].crop(region))
            assert sum(any(p) for p in difference.get_flattened_data()) > 20
        textures = read(root/'donor', 'coverage-textures.json')
        for texture in textures:
            assert hashlib.sha256((root/'donor'/texture['file']).read_bytes()).hexdigest() == texture['png_sha256']
        assert next(t for t in textures if t['file'] == 'fence.png')['source_id'] == 1474
        assert sum(r['mapped'] for r in decisions) == 26
        result['coverage'] = dict(baseline_selected_types=67, temporary_replacement_types=26,
            native_fallback_types=41, decisions=decisions, prop_direction_families=sorted(fixture),
            unsupported_flip_native_fallback=True, native_door_open_close=True,
            individual_faithful_art_complete=False)
        result['stage'] = 3
        result['mapping_sha256'] = hashlib.sha256((root/'joppa-coverage.json').read_bytes()).hexdigest()
        result['source_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (root/'profile/Local/Mods/RenderingTransplantProbe').glob('*.cs')}
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
