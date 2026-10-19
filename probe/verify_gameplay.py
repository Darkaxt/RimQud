"""Verify one fresh isolated native-game integration run and its GPU readbacks."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    root = args.root
    launch = json.loads((root / 'launch-gameplay.json').read_text(encoding='utf-8-sig'))
    started = dt.datetime.fromisoformat(launch['start'].replace('Z', '+00:00')).timestamp()

    def read(name):
        file = root / name
        assert file.stat().st_mtime >= started, f'Stale evidence: {name}'
        return json.loads(file.read_text(encoding='utf-8-sig'))

    assert read('gameplay-finished.json')['exitCode'] == 0
    runtime = read('runtime.json')
    assert runtime['mode'] == 'gameplay' and runtime['audioPaused']
    assert runtime['listenerVolume'] == runtime['masterVolume'] == runtime['ambientVolume'] == 0
    assert not any(runtime[k] for k in ['musicEnabled', 'soundEnabled', 'ambientEnabled'])
    boot = read('gameplay-boot.json')
    assert boot['running'] and boot['historyInitialized']
    assert boot['zone'] == 'JoppaWorld.11.22.1.1.10'
    result = read('gameplay-result.json')
    assert all(result[k] for k in ['nativeMovement', 'nativeLook', 'nativeInventory', 'nativeSaveLoad'])
    assert result['continuousNativeTurns'] == 3 and result['endTicks'] > result['startTicks']
    assert result['operatingSystemInput'] is False
    target = read('gameplay-target.json')
    menu = read('gameplay-menu.json')
    assert target['view'] == 'Looker' and menu['view'] == 'StatusScreensScreen' and menu['screen'] == 2
    for view in [target, menu]:
        assert not view['overlayVisible'] and view['nativeHiddenCells'] == 0
    assert (target['x'], target['y']) == (result['targetX'], result['targetY'])
    frames = read('gameplay-frames.json')
    expected = ['baseline', 'moved', 'look-returned', 'menu-returned', 'disabled',
                'reenabled', 'loaded', 'continuous-returned']
    assert [f['phase'] for f in frames] == expected
    assert result['frames'] == len(frames)
    summaries, images = [], {}
    previous = 0
    for f in frames:
        assert f['generation'] > previous
        previous = f['generation']
        assert f['submittedHash'] == f['consumedHash'] and len(f['submittedHash']) == 64
        assert f['insideBufferLock'] and f['producerThread'] != f['consumerThread'] == 1
        assert f['nativeCamera'] == 'Main Camera' and f['view'] == 'Stage'
        assert f['nativeRenderersSuppressed'] and f['audioPaused']
        assert f['masterVolume'] == f['listenerVolume'] == 0
        assert len(f['cells']) == 2000
        assert all(not c['mapped'] and c['source'] is None for c in f['cells'] if not c['visible'])
        for c in f['cells']:
            if c['requiresOriginal']:
                assert not c['mapped']
        binding = f['targetBinding']
        assert (binding['x'], binding['y']) == (result['targetX'], result['targetY'])
        assert binding['enabled'] and binding['colliders'] == 1
        paths = [root / f[k] for k in ['original', 'replacement']]
        for path in paths:
            assert path.stat().st_mtime >= started, path
            images[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        before, after = [Image.open(p).convert('RGB') for p in paths]
        assert before.size == after.size == (640, 480)
        difference = ImageChops.difference(before, after)
        changed = sum(any(pixel) for pixel in difference.get_flattened_data())
        if f['phase'] == 'disabled':
            assert changed == f['nativeHiddenCells'] == 0 and not f['overlayVisible'] and not f['eligible']
        else:
            assert changed > 10000 and f['nativeHiddenCells'] > 500 and f['overlayVisible'] and f['eligible']
            assert f['mappedByKind']['ground'] > 300 and f['mappedByKind']['path'] > 100
        summaries.append({k: f[k] for k in ['phase', 'generation', 'mappedByKind', 'nativeHiddenCells',
                                           'overlayVisible', 'player', 'offscreenMilliseconds']}
                         | dict(changed_pixels=changed, accepted_consumed_match=True))
    by_phase = {f['phase']: f for f in frames}
    initial, moved = by_phase['baseline']['player'], by_phase['moved']['player']
    assert abs(initial['x']-moved['x']) + abs(initial['y']-moved['y']) == 1
    assert moved == by_phase['loaded']['player'] == dict(x=result['targetX'], y=result['targetY'])
    preservation = read('preservation.json')
    assert preservation['preferences_restored'] and not preservation['changed_save_or_settings_files']
    # Old failed attempts remain diagnostic evidence; they must not belong to this run.
    for name in ['gameplay-failure.json', 'joppa-render-failure.json']:
        file = root / name
        assert not file.exists() or file.stat().st_mtime < started, f'Current failure: {name}'
    output = dict(scope='Real generated Joppa; native map-camera presentation and internal game inputs',
                  native_movement=True, native_targeting=True, native_modern_inventory=True,
                  native_save_load=True, continuous_native_turns=3,
                  physical_input_verified=False, foreground_desktop_used=False,
                  silent=True, saves_settings_preserved=True, unity_preferences_restored=True,
                  frames=summaries, images=images,
                  limitations=['Native map-camera readbacks omit separate HUD canvases',
                               'Three continuous turns are not a long-session stability or FPS benchmark',
                               'Known asset mappings only; native sprites remain for unmapped content',
                               'Physical mouse/keyboard and final foreground review remain pending'],
                  runtime_diagnostics=preservation['diagnostic_changes'])
    args.output.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print('Verified real Joppa presentation, movement, look, inventory, save/load and three continuous native turns.')


if __name__ == '__main__':
    main()
