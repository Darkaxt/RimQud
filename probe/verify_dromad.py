"""Verify the complete source-bound Tam sample from one hidden native run."""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path

from PIL import Image, ImageChops


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();root=args.root
    repo=Path(__file__).resolve().parents[1]
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    launch=json.loads((root/'launch-pawns.json').read_text(encoding='utf-8-sig'))
    started=dt.datetime.fromisoformat(launch['start'].replace('Z','+00:00')).timestamp()
    assert launch['artSet']=='dromad' and launch['integrationStage']==4 and '-batchmode' in launch['arguments']
    def read(name):
        p=root/name;assert p.stat().st_mtime>=started,('Stale evidence',name)
        return json.loads(p.read_text(encoding='utf-8-sig'))
    assert read('gameplay-finished.json')['exitCode']==0
    result=read('dromad-result.json');assert all(result[k] for k in ['nativeSaveLoad','actualStartingEquipmentRestored','nativeEquipUnequip','nativeMovement'])
    assert result['operatingSystemInput'] is False
    runtime=read('runtime.json');assert runtime['audioPaused'] and runtime['listenerVolume']==runtime['masterVolume']==0
    assert not any(runtime[k] for k in ['musicEnabled','soundEnabled','ambientEnabled'])
    preservation=read('preservation.json');assert preservation['preferences_restored'] and not preservation['changed_save_or_settings_files']
    contract=json.loads((repo/'art/dromad/rebuilt/model.json').read_text())
    assert result['contract']==contract
    assert contract['authoring']=='Explicit SVG paths; resvg-py==0.5.0; no ImageGen'
    frames=read('gameplay-frames.json');by_phase={f['phase']:f for f in frames}
    assert len(frames)==16 and len(by_phase)==16
    def tam(phase):
        return next(c for c in by_phase[phase]['cells'] if c['source']=='Tam')
    native_images={}
    for frame in frames:
        assert frame['eligible'] and frame['overlayVisible'] and frame['nativeRenderersSuppressed']
        assert frame['audioPaused'] and frame['masterVolume']==0
        for key in ['original','replacement']:
            p=root/frame[key];assert p.stat().st_mtime>=started
            assert Image.open(p).size==(1280,800)
            native_images[p.name]=sha(p)
        cells=[c for c in frame['cells'] if c['source']=='Tam']
        if frame['phase']=='dromad-hidden':
            assert not cells;continue
        c=cells[0]
        if frame['phase']=='dromad-unsupported-anatomy':
            assert not c['mapped'] and c['artFallback']=='Unsupported dromad body topology';continue
        if frame['phase']=='dromad-late-equipment':
            assert not c['mapped'] and c['requiresOriginal'] and c['apparelFallback']=='Equipped appearance changed after observation';continue
        assert c['mapped'] and c['assetFamily']=='dromad' and c['nativeInputEnabled']
        assert (c['inputX'],c['inputY'])==(c['x'],c['y'])
        layers=c['art']['layers'];expected=5 if frame['phase'] in ['dromad-robe-removed','dromad-held-removed'] else 6
        assert len(layers)==c['foregroundLayers']==expected
        for layer in layers:
            assert abs(layer['contactX']-c['feetX'])<1e-4 and abs(layer['contactY']-c['feetY'])<1e-4
            assert abs(layer['width']/layer['height']-256/320)<1e-5
            assert layer['shader']=='Custom/Cutout'
            tint=c['detailColor'] if '-detail' in layer['name'] else c['foregroundColor'] if layer['name'].startswith('RimQudDromad:') else next(i['color'] for i in c['equipment'] if str(i['instance']) in layer['name'])
            assert all(abs(a-b)<1e-6 for a,b in zip(layer['color'],tint))
        assert ImageChops.difference(Image.open(root/frame['original']).convert('RGB'),Image.open(root/frame['replacement']).convert('RGB')).getbbox()
    for direction,facing in [('south',2),('east',1),('west',3),('north',0)]:
        c=tam('dromad-'+direction);assert c['facing']==facing
        expected_direction='east' if direction=='west' else direction
        assert all(layer['file'].endswith('-'+expected_direction+'.png') for layer in c['art']['layers'])
    assert {e['blueprint'] for e in tam('dromad-south')['equipment']}=={'Cloth Robe','Shillelagh'}
    assert {e['blueprint'] for e in tam('dromad-robe-removed')['equipment']}=={'Shillelagh'}
    assert {e['blueprint'] for e in tam('dromad-held-removed')['equipment']}=={'Cloth Robe'}
    assert tam('dromad-south')['equipment']==tam('dromad-loaded')['equipment']
    look=read('dromad-target-view.json');assert look['view']=='Looker' and not look['overlayVisible'] and look['nativeHiddenCells']==0
    assert read('dromad-target.json')['instance']==result['instance']
    damage=read('hurt-dromad-result.json');assert damage['hpBefore']-damage['hpAfter']==1 and damage['startTicks']==damage['endTicks']
    reactions=read('hurt-samples.json');assert [r['sample'] for r in reactions]==['start','mid','end']
    assert 0<=reactions[0]['visualTicks']<8 and 8<=reactions[1]['visualTicks']<16 and reactions[2]['finished']
    assert all(len(r['layers'])==6 and r['gameTicks']==damage['startTicks'] for r in reactions)
    for layer,base in zip(reactions[-1]['layers'],tam('dromad-restored')['art']['layers']):
        assert all(abs(a-b)<1e-6 for a,b in zip(layer['color'],base['color']))
    for reaction in reactions:
        p=root/reaction['image'];assert p.stat().st_mtime>=started;native_images[p.name]=sha(p)
    sources={p.name:sha(p) for p in (repo/'probe').glob('*.cs')}
    mod=root/'profile/Local/Mods/RenderingTransplantProbe'
    assert all(sha(mod/name)==digest for name,digest in sources.items())
    for direction,rows in contract['views'].items():
        for row in rows:
            assert sha(root/'donor'/row['file'])==row['sha256']
    evidence=dict(scope='One deterministically constructed adult dromad / actual Tam, inside isolated native Joppa; not complete village conversion',
        date=dt.datetime.now(dt.timezone.utc).isoformat(),authoring=contract['authoring'],
        paired_native_frames=len(frames),native_four_way_facing=True,native_equip_unequip=True,
        independent_foreground_detail_palette=True,actual_mesh_contact_and_uniform_scale=True,
        late_equipment_fallback=True,unsupported_topology_fallback=True,native_visibility=True,
        native_look=True,native_hurt_without_simulation_advance=True,native_save_load=True,
        saves_settings_preserved=True,operating_system_input=False,
        source_sha256=sources,model_sha256=sha(repo/'art/dromad/rebuilt/model.json'),
        native_image_sha256=native_images,launch_start=launch['start'],
        limitations=['Adult sample only; full village stage remains ACTIVE','Hand-authored directional vectors; not a 3D rig or full donor PawnRenderTree','Only Cloth Robe and Shillelagh supported for this body','Unseen surfaces are authored interpretation; personal cosmetic overlays postponed'])
    args.output.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
    print('Verified native Tam: registered four-way layers, actual equip/unequip, separate Qud palette, visibility/fallback, native look/hurt/save-load; profiles preserved.')


if __name__=='__main__':main()
