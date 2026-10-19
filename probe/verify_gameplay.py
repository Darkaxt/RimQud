"""Verify one fresh isolated native-game integration run and its GPU readbacks."""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--mode', choices=['gameplay', 'pawns'], default='gameplay')
    ap.add_argument('--stage', type=int, choices=[1, 2, 3, 4], default=1)
    args = ap.parse_args()
    root = args.root
    launch = json.loads((root / ('launch-' + args.mode + '.json')).read_text(encoding='utf-8-sig'))
    started = dt.datetime.fromisoformat(launch['start'].replace('Z', '+00:00')).timestamp()

    def read(name):
        file = root / name
        assert file.stat().st_mtime >= started, f'Stale evidence: {name}'
        return json.loads(file.read_text(encoding='utf-8-sig'))

    assert read('gameplay-finished.json')['exitCode'] == 0
    runtime = read('runtime.json')
    assert runtime['mode'] == args.mode and runtime['audioPaused']
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
    look_target = read('pawn-target.json') if args.mode == 'pawns' else dict(x=result['targetX'], y=result['targetY'])
    assert (target['x'], target['y']) == (look_target['x'], look_target['y'])
    frames = read('gameplay-frames.json')
    expected = ['baseline', 'moved', 'look-returned', 'menu-returned', 'disabled',
                'reenabled', 'loaded', 'continuous-returned']
    if args.mode == 'pawns':
        expected[1:1] = ['pawn-west', 'pawn-east', 'animal-east', 'animal-north', 'pawn-hidden', 'pawn-visible',
                         'pawn-late-change', 'pawn-restored', 'pawn-tint',
                         'pawn-tint-restored', 'prop-front', 'prop-behind']
        expected.insert(expected.index('menu-returned'), 'pawn-look-returned')
        if args.stage >= 2:
            expected[expected.index('moved')+1:expected.index('moved')+1] = [
                'native-move-back', 'native-move-forward', 'hurt-human-ended', 'hurt-animal-ended']
        if args.stage >= 4:
            expected[expected.index('disabled'):expected.index('disabled')] = [
                'apparel-inventory-only', 'apparel-equipped', 'apparel-hat-removed', 'apparel-swapped',
                'apparel-tint', 'apparel-tint-restored', 'apparel-late-change', 'apparel-late-restored',
                'apparel-west', 'apparel-east', 'apparel-north', 'apparel-south', 'apparel-look-returned',
                'hurt-equipped-ended', 'apparel-unsupported-item', 'apparel-supported-restored',
                'apparel-unsupported-anatomy']
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
        assert before.size == after.size == ((1280, 800) if args.mode == 'pawns' else (640, 480))
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
    pawn_summary = None
    if args.mode == 'pawns':
        fixture = read('pawn-fixture.json')
        ids = [fixture[k] for k in ['human', 'animal', 'prop']]
        assert len(set(ids)) == 3 and all(i > 0 for i in ids)

        def cell(phase, identity):
            hits = [c for c in by_phase[phase]['cells'] if c['instance'] == identity]
            assert len(hits) == 1, (phase, identity, len(hits))
            return hits[0]

        for name, kind, layers in [('human', 'human', 2), ('animal', 'animal', 1), ('prop', 'prop', 1)]:
            c = cell('baseline', fixture[name])
            assert c['mapped'] and c['kind'] == kind and c['foregroundLayers'] == layers
            assert c['groundKind'] in ['ground', 'path', 'water']
            assert (c['inputX'], c['inputY']) == (c['x'], c['y'])
            assert c['nativeInputEnabled']
            assert c['feetX'] == c['x'] + .5 and abs(c['feetY'] - c['y'] - .86) < .001
        human_id = fixture['human']
        assert cell('pawn-west', human_id)['facing'] == 3
        assert cell('pawn-east', human_id)['facing'] == 1
        assert cell('animal-east', fixture['animal'])['facing'] == 1
        assert cell('animal-north', fixture['animal'])['facing'] == 0
        assert not any(c['instance'] == human_id for c in by_phase['pawn-hidden']['cells'])
        assert cell('pawn-visible', human_id)['mapped']
        changed = cell('pawn-late-change', human_id)
        assert changed['requiresOriginal'] and not changed['mapped'] and changed['foregroundLayers'] == 0
        assert cell('pawn-restored', human_id)['mapped']
        for f in frames:
            for c in f['cells']:
                if not c['visible']:
                    assert c['instance'] == 0 and c['groundKind'] is None
        tint = cell('pawn-tint', human_id)
        restored = cell('pawn-tint-restored', human_id)
        assert tint['foregroundColor'][0] > 2 * tint['foregroundColor'][1]
        assert tint['foregroundColor'] != restored['foregroundColor']
        cam = by_phase['pawn-tint']['camera']
        assert cam == by_phase['pawn-tint-restored']['camera'] and cam['nativeLayoutReady']
        cx, cy = round(tint['screenX']), cam['height'] - round(tint['screenY'])
        assert 0 <= cx < cam['width'] and 0 <= cy < cam['height'], (cx, cy)
        crop = (cx - 18, cy - 48, cx + 18, cy + 24)
        a = Image.open(root / by_phase['pawn-tint']['replacement']).convert('RGB').crop(crop)
        b = Image.open(root / by_phase['pawn-tint-restored']['replacement']).convert('RGB').crop(crop)
        tint_pixels = sum(any(pixel) for pixel in ImageChops.difference(a, b).get_flattened_data())
        assert tint_pixels > 5, tint_pixels
        red = lambda image: sum(r > 20 and r > 1.4 * g and r > 1.2 * b for r, g, b in image.get_flattened_data())
        red_tint, red_restored = red(a), red(b)
        assert red_tint > red_restored + 8, (red_tint, red_restored)
        assert cell('prop-front', fixture['prop'])['foregroundDepth'] > cell('prop-front', human_id)['foregroundDepth']
        assert cell('prop-behind', fixture['prop'])['foregroundDepth'] < cell('prop-behind', human_id)['foregroundDepth']
        assert look_target['nativeLook'] and look_target['instance'] == human_id
        pawn_summary = dict(layered_human=True, directional_animal=True, prop=True,
                            known_ground_beneath=True, native_binding=True, directional_change=True,
                            hidden_identity_excluded=True, late_change_fallback=True,
                            tint_changed_pixels=tint_pixels, red_tinted_pixels=red_tint,
                            restored_red_pixels=red_restored, mapped_overlap_order=True,
                            native_npc_targeting=True)
        if args.stage >= 2:
            native_back, native_forward = [by_phase[name] for name in ['native-move-back', 'native-move-forward']]
            assert native_back['player'] == initial and native_forward['player'] == moved
            for f in [native_back, native_forward]:
                at = next(c for c in f['cells'] if (c['x'], c['y']) == (f['player']['x'], f['player']['y']))
                assert at['mapped'] and at['kind'] == 'human'
                dx, dy = moved['x']-initial['x'], moved['y']-initial['y']
                facing = (1 if dx > 0 else 3) if dx else (2 if dy > 0 else 0)
                assert at['facing'] == (facing if f is native_forward else (facing+2) % 4)
            samples = read('hurt-samples.json')
            hurt_summary = {}
            for name in (['human', 'animal', 'equipped'] if args.stage >= 4 else ['human', 'animal']):
                damage = read('hurt-'+name+'-result.json')
                assert damage['actualQudDamage'] and damage['hpBefore']-damage['hpAfter'] == 1
                assert damage['startTicks'] == damage['endTicks'] and not damage['simulationAdvanced']
                sequence = [s for s in samples if s['fixture'] == name]
                assert [s['sample'] for s in sequence] == ['start', 'mid', 'end'], sequence
                start, mid, end = sequence
                assert 0 <= start['visualTicks'] < mid['visualTicks'] < 16 <= end['visualTicks']
                assert not start['finished'] and not mid['finished'] and end['finished']
                assert end['offsetX'] == end['offsetY'] == 0
                assert .14 < math.hypot(start['offsetX'], start['offsetY']) <= .171
                assert math.hypot(mid['offsetX'], mid['offsetY']) < math.hypot(start['offsetX'], start['offsetY'])
                assert all(s['gameTicks'] == damage['startTicks'] for s in sequence)
                assert all(s['instance'] == damage['instance'] for s in sequence)
                first_cell = cell('hurt-'+name+'-ended', damage['instance'])
                cam = by_phase['hurt-'+name+'-ended']['camera']
                cx, cy = round(first_cell['screenX']), cam['height']-round(first_cell['screenY'])
                region = (cx-18, cy-48, cx+18, cy+24)
                red_counts = []
                for s in sequence:
                    p = root / s['image']; assert p.stat().st_mtime >= started
                    images[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
                    red_counts.append(red(Image.open(p).convert('RGB').crop(region)))
                assert red_counts[0] > red_counts[-1]+5, (name, red_counts)
                if name == 'equipped':
                    assert len(start['layers']) == len(end['layers']) == 6
                    assert all(layer['color'][0] > .9 and max(layer['color'][1:3]) < .1 for layer in start['layers'])
                    equipped = first_cell['equipment']
                    for item in equipped:
                        layer = next(layer for layer in end['layers'] if layer['name'] == f"RimQudEquipped:{item['instance']}:{item['slot']}")
                        assert all(abs(a-b)<.00001 for a,b in zip(layer['color'], item['color']))
                hurt_summary[name] = dict(actual_hp_loss=1, no_game_tick_advance=True,
                    red_pixels=red_counts, visual_ticks=[s['visualTicks'] for s in sequence],
                    finite_flash=True, finite_impact_offset=True)
            assert by_phase['loaded']['world'] > by_phase['hurt-animal-ended']['world']
            pawn_summary['native_reactions'] = hurt_summary
            pawn_summary['native_movement_facing'] = True
            pawn_summary['world_rebuilt_after_load'] = True
        if args.stage >= 4:
            fixture = read('apparel-fixture.json'); identity = fixture['instance']
            inventory, full, removed, swapped = [cell(name, identity) for name in [
                'apparel-inventory-only', 'apparel-equipped', 'apparel-hat-removed', 'apparel-swapped']]
            assert inventory['mapped'] and inventory['equipment'] == [] and inventory['foregroundLayers'] == 2
            assert full['mapped'] and full['foregroundLayers'] == 6 and full['apparelFallback'] is None
            expected_items = {'Woven Tunic':'Body','Leather Cloak':'Back','Wide-brimmed Hat':'Head','Long Sword':'Hand'}
            assert {e['blueprint']:e['slot'] for e in full['equipment']} == expected_items
            assert [e['layer'] for e in full['equipment']] == [20,32,70,80]
            assert all(e['instance'] == fixture['items'][e['blueprint']] for e in full['equipment'])
            assert removed['mapped'] and removed['foregroundLayers'] == 5
            assert not any(e['slot'] == 'Head' for e in removed['equipment'])
            assert swapped['mapped'] and swapped['foregroundLayers'] == 6
            assert any(e['blueprint'] == 'Cloth Robe' and e['family'] == 'robe' for e in swapped['equipment'])
            assert not any(e['blueprint'] == 'Woven Tunic' for e in swapped['equipment'])
            tint, restored = [cell(name, identity) for name in ['apparel-tint','apparel-tint-restored']]
            assert tint['foregroundColor'] == restored['foregroundColor']
            for item in tint['equipment']:
                original = next(e for e in restored['equipment'] if e['instance'] == item['instance'])
                if item['blueprint'] == 'Cloth Robe':
                    assert item['color'][0] > 2*item['color'][1] and item['color'] != original['color']
                else:
                    assert item['color'] == original['color']
            cam = by_phase['apparel-tint']['camera']
            cx,cy = round(tint['screenX']),cam['height']-round(tint['screenY'])
            region = (cx-22,cy-48,cx+22,cy+24)
            red_tint = red(Image.open(root/by_phase['apparel-tint']['replacement']).convert('RGB').crop(region))
            red_restored = red(Image.open(root/by_phase['apparel-tint-restored']['replacement']).convert('RGB').crop(region))
            assert red_tint > red_restored+5, (red_tint,red_restored)
            late = cell('apparel-late-change',identity)
            assert late['requiresOriginal'] and not late['mapped'] and late['equipment'] == []
            assert 'changed after observation' in late['apparelFallback']
            assert cell('apparel-late-restored',identity)['mapped']
            for name,facing in [('west',3),('east',1),('north',0),('south',2)]:
                c = cell('apparel-'+name,identity)
                assert c['mapped'] and c['foregroundLayers'] == 6 and c['facing'] == facing and c['nativeInputEnabled']
                assert (c['inputX'],c['inputY']) == (c['x'],c['y'])
            south = cell('apparel-south',identity)
            assert (south['x'],south['y']) == (full['x'],full['y'])
            assert cell('apparel-west',identity)['x'] == full['x']-1
            assert cell('apparel-north',identity)['y'] == full['y']-1
            unsupported = cell('apparel-unsupported-item',identity)
            assert unsupported['kind'] == 'original' and not unsupported['mapped'] and unsupported['foregroundLayers'] == 0
            assert 'Leather Boots' in unsupported['apparelFallback']
            assert cell('apparel-supported-restored',identity)['mapped']
            before_save, loaded = read('apparel-before-save.json'), read('apparel-load.json')
            assert before_save['residentEquipmentUnchanged'] and before_save['carriedTunicUnworn']
            assert before_save['anatomyArms'] == 3
            anatomy = cell('apparel-unsupported-anatomy',before_save['unsupportedAnatomyInstance'])
            assert not anatomy['mapped'] and 'Unsupported anatomy' in anatomy['apparelFallback'] and 'Arm=3' in anatomy['bodyShape']
            assert loaded['nativeSaveLoad'] and loaded['outfit'] == before_save['outfit'] and loaded['instance'] == identity
            after_load = cell('loaded',identity)
            assert after_load['mapped'] and after_load['foregroundLayers'] == 6 and len(after_load['equipment']) == 4
            assert after_load['equipment'] == swapped['equipment']
            targeted = read('apparel-target.json'); target_view = read('apparel-target-view.json')
            assert targeted['instance'] == identity and targeted['nativeLook']
            assert (targeted['x'],targeted['y']) == (south['x'],south['y'])
            assert target_view['view'] == 'Looker' and not target_view['overlayVisible'] and target_view['nativeHiddenCells'] == 0
            assert all(not c['equipment'] and c['bodyShape'] is None for f in frames for c in f['cells'] if not c['visible'])
            pawn_summary['equipped_items'] = dict(actual_native_slots=expected_items, inventory_is_not_equipment=True,
                native_equip_remove_swap=True, item_tint_pixels=[red_tint,red_restored],
                late_equipment_change_fallback=True,native_npc_movement_facing=True,layered_hurt=True,
                native_save_load=True,native_targeting=True,resident_equipment_unchanged=True,
                unsupported_item_native_fallback=True,unsupported_anatomy_native_fallback=True)
    preservation = read('preservation.json')
    assert preservation['preferences_restored'] and not preservation['changed_save_or_settings_files']
    # Old failed attempts remain diagnostic evidence; they must not belong to this run.
    for name in ['gameplay-failure.json', 'joppa-render-failure.json', 'gameplay-capture-failure.json', 'reaction-failure.json']:
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
    if pawn_summary:
        output['stage'] = args.stage
        output['pawn_scene'] = pawn_summary
        output['scope'] += '; layered human/animal/prop fixture with native fallback and known ground'
    output['source_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in (root / 'profile/Local/Mods/RenderingTransplantProbe').iterdir() if p.suffix == '.cs'}
    args.output.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print('Verified real Joppa presentation, movement, look, inventory, save/load and three continuous native turns.')


if __name__ == '__main__':
    main()
