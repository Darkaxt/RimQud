"""Verify the complete bounded Joppa cast/environment conversion in native Qud."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    root=a.root;repo=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    launch=json.loads((root/'launch-pawns.json').read_text(encoding='utf-8-sig'));started=dt.datetime.fromisoformat(launch['start'].replace('Z','+00:00')).timestamp()
    assert launch['artSet']=='village' and launch['integrationStage']==4 and '-batchmode' in launch['arguments']
    def read(name):
        p=root/name;assert p.stat().st_mtime>=started,('Stale native evidence',name)
        return json.loads(p.read_text(encoding='utf-8-sig'))
    assert read('gameplay-finished.json')['exitCode']==0
    result=read('village-result.json');contract=json.loads((repo/'art/village/model.json').read_text(encoding='utf-8'))
    assert contract==result['contract'] and len(contract['actors'])==10
    assert result['residentCount']==16 and set(result['actorBlueprints'])==set(contract['actors'])
    assert all(result[k] for k in ['nativeSaveLoad','nativeEquipUnequip','originalOutfitsRestored','diagnosticFullReveal','diagnosticPlacementForFacing'])
    assert not result['operatingSystemInput']
    runtime=read('runtime.json');assert runtime['audioPaused'] and runtime['listenerVolume']==runtime['masterVolume']==0
    assert not any(runtime[k] for k in ['musicEnabled','soundEnabled','ambientEnabled'])
    preservation=read('preservation.json');assert preservation['preferences_restored'] and not preservation['changed_save_or_settings_files']
    frames=read('gameplay-frames.json');phases={f['phase']:f for f in frames};assert len(frames)==len(phases)==16
    residents=read('village-residents.json')['actors'];ids={r['instance'] for r in residents}
    native_images={};all_mapped=set();scenery=set(contract['scenery']['entries'])
    def cell(phase,name):return next(c for c in phases[phase]['cells'] if c['source']==name)
    for f in frames:
        assert f['eligible'] and f['overlayVisible'] and f['nativeRenderersSuppressed'] and f['audioPaused'] and f['masterVolume']==0
        assert f['insideBufferLock'] and f['submittedHash']==f['consumedHash']
        for key in ['original','replacement']:
            p=root/f[key];assert p.stat().st_mtime>=started and Image.open(p).size==(1280,800);native_images[p.name]=sha(p)
        assert ImageChops.difference(Image.open(root/f['original']).convert('RGB'),Image.open(root/f['replacement']).convert('RGB')).getbbox()
        for c in f['cells']:
            if c['mapped']:all_mapped.add(c['source'])
            if c['instance'] not in ids and c['source'] not in scenery:continue
            if not c['mapped']:
                if f['phase']=='village-late-item':assert c['apparelFallback']=='Equipped appearance changed after observation';continue
                if f['phase']=='village-unsupported-body':assert c['source']=='Nima Ruda' and c['artFallback']=='Unsupported village body topology';continue
                raise AssertionError(('Unexpected village fallback',f['phase'],c['source'],c['artFallback']))
            assert c['artFallback'] is None and c['apparelFallback'] is None
            if not c['art']:continue  # linked wall/fence/door/bridge use shared geometry
            d='north' if c['facing']==0 else 'south' if c['facing']==2 else 'east'
            if c['instance'] in ids:
                assert c['nativeInputEnabled'] and (c['inputX'],c['inputY'])==(c['x'],c['y'])
                family=c['assetFamily'].split(':',1)[1];rows=list(contract['bodies'][family]['views'][d])
                for item in c['equipment']:rows+=contract['equipment'][family][item['family']]['views'][d]
            else:rows=contract['scenery']['entries'][c['source']]['views'][d]
            actual=c['art']['layers'];assert len(actual)==len(rows)==c['foregroundLayers']
            assert {l['file'] for l in actual}=={p['file'] for p in rows}
            for l in actual:
                row=next(p for p in rows if p['file']==l['file'])
                assert abs(l['contactX']-c['feetX'])<1e-4 and abs(l['contactY']-c['feetY'])<1e-4
                assert abs(l['width']-row['width']*2/3)<1e-5 and abs(l['height']-row['height'])<1e-5
                assert abs(l['width']/l['height']-row['size'][0]/row['size'][1])<1e-5
                role=l['role'];tint=[1,1,1,1] if role=='fixed' else c['detailColor'] if role=='detail' else c['backgroundColor'] if c['nativeChar'] else c['foregroundColor']
                if role.startswith('equipment'):tint=next(i['detail' if role=='equipment-detail' else 'color'] for i in c['equipment'] if i['family']==l['equipmentKey'])
                assert all(abs(x-y)<1e-6 for x,y in zip(l['color'],tint)),(f['phase'],c['source'],l)
                assert l['shader']=='Custom/Cutout'
    assert set(contract['actors'])|scenery|{'DirtFloor','DirtPath','Pond'}<=all_mapped
    for phase in ['village-native-layout','village-loaded']:
        assert {c['instance'] for c in phases[phase]['cells'] if c['mapped'] and c['instance'] in ids}==ids
    assert not any(c['source']=='Nima Ruda' for c in phases['village-hidden']['cells'])
    for direction,facing in [('east',1),('west',3),('north',0),('south',2)]:
        actors=[c for c in phases['village-'+direction]['cells'] if c['instance'] in ids]
        assert len(actors)==16 and all(c['mapped'] and c['facing']==facing for c in actors)
    for r in residents:
        base=next(c for c in phases['village-native-layout']['cells'] if c['instance']==r['instance'])
        loaded=next(c for c in phases['village-loaded']['cells'] if c['instance']==r['instance'])
        assert base['equipment']==loaded['equipment']
        removed=next(c for c in phases['village-garments-removed']['cells'] if c['instance']==r['instance'])
        assert all(e['slot']!='Body' for e in removed['equipment'])
        assert {e['instance'] for e in removed['equipment']}=={e['instance'] for e in base['equipment'] if e['slot']!='Body'}
    normal=phases['village-native-layout'];deep=phases['village-deep-water']
    assert normal['shallowWaterCells']>0 and normal['deepWaterCells']==0 and deep['deepWaterCells']>0
    assert phases['village-loaded']['deepWaterCells']==0 and normal['grassClumps']>0
    look=read('gameplay-target.json');assert look['view']=='Looker' and not look['overlayVisible'] and look['nativeHiddenCells']==0
    target=read('village-target.json');assert target['instance']==cell('village-restored','Nima Ruda')['instance']
    damage=read('hurt-village-result.json');assert damage['hpBefore']-damage['hpAfter']==1 and damage['startTicks']==damage['endTicks']
    reactions=read('hurt-samples.json');assert [r['sample'] for r in reactions]==['start','mid','end']
    assert 0<=reactions[0]['visualTicks']<8 and 8<=reactions[1]['visualTicks']<16 and reactions[2]['finished']
    for reaction in reactions:
        assert reaction['gameTicks']==damage['startTicks'];p=root/reaction['image'];assert p.stat().st_mtime>=started;native_images[p.name]=sha(p)
    base=cell('village-restored','Nima Ruda')['art']['layers'];assert len(base)==len(reactions[-1]['layers'])
    assert all(all(abs(x-y)<1e-6 for x,y in zip(l['color'],b['color'])) for l,b in zip(reactions[-1]['layers'],base))
    for group in [*[m['views'] for m in contract['bodies'].values()],*[m['views'] for f in contract['equipment'].values() for m in f.values()],*[m['views'] for m in contract['scenery']['entries'].values()]]:
        for rows in group.values():
            for row in rows:assert sha(root/'donor'/row['file'])==row['sha256']==sha(repo/row['public_file'])
    for filename in [*contract['scenery']['surfaces'].values(),*[f for pair in contract['scenery']['walls'].values() for f in pair]]:assert (root/'donor'/filename).is_file()
    sources={p.name:sha(p) for p in (repo/'probe').glob('*.cs')};mod=root/'profile/Local/Mods/RenderingTransplantProbe'
    assert all(sha(mod/name)==digest for name,digest in sources.items())
    out=dict(scope='The captured 16-resident Joppa cast and 57 selected environment types; source-bound art, not a general mod/NPC converter',date=dt.datetime.now(dt.timezone.utc).isoformat(),
        resident_count=16,actor_blueprints=sorted(contract['actors']),selected_scenery_types=57,mapped_isolated_scenery_types=len(scenery),paired_native_frames=len(frames),
        native_four_way_facing=True,native_equipment_removal_restore=True,actual_equipped_palette=True,registered_mesh_contact_scale=True,native_visibility=True,late_equipment_fallback=True,unsupported_topology_fallback=True,
        native_look=True,native_hurt_without_simulation_advance=True,native_save_load=True,native_shallow_deep_water=True,native_basic_grass=True,saves_settings_preserved=True,operating_system_input=False,
        diagnostic_full_reveal=True,diagnostic_placement_for_facing=True,source_sha256=sources,model_file='art/village/model.json',model_sha256=sha(repo/'art/village/model.json'),native_image_sha256=native_images,launch_start=launch['start'],
        limitations=['Fixed named mutation silhouettes, no generic mutation/clothing resolver','Flat body/head/apparel graphics, no independent limb rig or full donor PawnRenderTree',
        'Unseen surfaces and shading are authored interpretation; source glyph/palette remains the reference','Child templates are fully clothed authoring variants, unbound because selected native actors have no established age selector','Personal cosmetic overlays postponed; unknown equipment/anatomy/posture retains native art','Deep-water fixture changes one isolated pond volume then restores it; the generated Joppa ponds are naturally wading-depth'])
    a.output.write_bytes((json.dumps(out,indent=2)+'\n').encode());print('Verified complete native Joppa batch: 16 residents, 10 actor blueprints, 57 environment types, actual equipment/facing/palette/contact, visibility/fallback, water depths, look/hurt/save-load and profile preservation.')
if __name__=='__main__':main()
