"""Verify and publish the four actual native-camera current-art captures."""
import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]


def build(root, revision=1):
    read = lambda name: json.loads((root / name).read_text(encoding='utf-8-sig'))
    result = read('current-four-views.json')
    frames = read('gameplay-frames.json')
    assert read('gameplay-finished.json')['exitCode'] == 0
    preservation = read('preservation.json')
    assert preservation['preferences_restored'] and not preservation['changed_save_or_settings_files']
    phases = ['day-revealed', 'night-revealed', 'day-fog', 'night-fog']
    assert {x['phase'] for x in result['phases']} == set(phases)
    assert len({json.dumps(x['player'],sort_keys=True) for x in frames}) == 1
    assert len({json.dumps(x['camera'],sort_keys=True) for x in frames}) == 1
    folder='current-game-rendering-20261021' if revision==1 else 'current-game-rendering-v2-20261021'
    out = ROOT / ('evidence/'+folder)
    out.mkdir(exist_ok=True)
    records, cards = [], []
    all_images = []
    for phase in phases:
        frame = next(x for x in frames if x['phase'] == 'current-' + phase)
        scenario = next(x for x in result['phases'] if x['phase'] == phase)
        assert frame['eligible'] and frame['overlayVisible'] and frame['nativeRenderersSuppressed']
        assert frame['submittedHash'] == frame['consumedHash'] and frame['insideBufferLock']
        assert frame['producerThread'] != frame['consumerThread']
        assert not any(x['mapped'] and (not x['visible'] or x['requiresOriginal']) for x in frame['cells'])
        assert any(x.get('currentArt') and str(x.get('assetFamily', '')).startswith('current:NPC-') for x in frame['cells']) if not scenario['fog'] else True
        assert scenario['nativeDay'] == phase.startswith('day')
        assert scenario['revealOverride'] != scenario['fog']
        files = {}
        for kind in ['original', 'replacement']:
            source = root / frame[kind]
            with Image.open(source) as image:
                assert image.size == (1280, 800)
                if kind == 'replacement': all_images.append(image.convert('RGB'))
            name = phase + '-' + kind + '.png'
            shutil.copy2(source, out / name)
            files[kind] = dict(path=(out/name).relative_to(ROOT).as_posix(), sha256=hashlib.sha256(source.read_bytes()).hexdigest())
        summary = dict(phase=phase, native=scenario, mapped=sum(x['mapped'] for x in frame['cells']),
                       current_actor_cells=[{k:x.get(k) for k in ['source','x','y','facing','assetFamily','mapped','artFallback']} for x in frame['cells'] if str(x.get('assetFamily','')).startswith('current:NPC-')],
                       fallback_sources=sorted({x['source'] for x in frame['cells'] if x.get('visible') and x.get('source') and not x['mapped']}),
                       accepted_frame_hash=frame['submittedHash'], files=files)
        records.append(summary)
        label=phase.replace('-', ' · ').title()
        cards.append(f'<figure><figcaption>{html.escape(label)} <span>{summary["mapped"]} converted cells</span></figcaption><a class="full" href="../{files["replacement"]["path"]}" target="_blank" rel="noopener"><img loading="lazy" width="1280" height="800" alt="Actual Qud game camera: {label}" data-replacement="../{files["replacement"]["path"]}" data-original="../{files["original"]["path"]}" src="../{files["replacement"]["path"]}"></a></figure>')
    assert len({x['accepted_frame_hash'] for x in records}) >= 2
    for i in range(4):
        for j in range(i):
            assert ImageChops.difference(all_images[i], all_images[j]).getbbox(), (phases[i], phases[j], 'identical captures')
    revealed = next(x for x in records if x['phase']=='day-revealed')
    fog = next(x for x in records if x['phase']=='day-fog')
    assert fog['mapped'] < revealed['mapped'], 'Native fog did not restrict converted rendering'
    source_hashes={}
    loaded=root/'profile/Local/Mods/RenderingTransplantProbe'
    for path in loaded.glob('*.cs'):
        source=(ROOT/'probe'/path.name).read_bytes()
        assert source==path.read_bytes(),path.name
        source_hashes['probe/'+path.name]=hashlib.sha256(source).hexdigest()
    evidence=dict(scope='Four real Qud native-camera rendering views; not complete lifecycle/full-ledger acceptance.',
                  records=records, preservation=preservation, source_sha256=source_hashes,
                  runtime_contract_sha256=hashlib.sha256((root/'selected/runtime/contract.json').read_bytes()).hexdigest(),
                  package_sha256=result['packageSha256'],cast_sha256=result['castSha256'],night_treatment=result['nightTreatment'],
                  full_ledger_native_acceptance=False)
    comparison=''
    if revision==2:
        shader=read('current-fog-shader.json')
        assert shader['supported'] and shader['shader']=='Custom/FogShader'
        fogs=[read('current-fog-current-'+phase+'.json') for phase in ['day-fog','night-fog']]
        assert all(x['nativeVisibility'] and x['nativeExploration'] and not x['hiddenObjectQueries'] and x['unknown']>0 for x in fogs)
        day=next(x for x in frames if x['phase']=='current-day-revealed')
        ponds=[x for x in day['cells'] if x['source']=='Pond' and x['visible']]
        assert ponds and all(x['waterSupported'] and x['mapped'] and x['waterLayer'] for x in ponds), 'Current brine conversion is not exercised'
        terrain=day['currentTerrain']
        assert terrain and all(x['textureWidth']==1024 and x['textureHeight']==1024 and x['wrapMode']=='Repeat' and x['worldPeriodCells']==16 for x in terrain), 'Terrain shader received cropped or clamped material'
        assert any(x['vertexAlphaMin']<x['vertexAlphaMax'] for x in terrain), 'Connected terrain boundary coverage is missing'
        assert all(x['plantScale']==2 for x in day['cells'] if x['source'] in ['Dogthorn Tree','Starapple Tree','Starapple Tree Ripe'] and x['mapped'])
        liquid=read('current-liquid-inputs.json')
        evidence.update(fog_shader=shader,fog_frames=fogs,liquid_inputs=liquid,terrain_materials=terrain)
        references=[('Original POC · RimWorld textures; different capture layout',Path('E:/Temp/qud-transplant-probe-pawns-20261019/joppa-baseline-replacement.png'),'poc-donor-full-map.png'),
                    ('Previous current-art rendering',ROOT/'evidence/current-game-rendering-20261021/day-revealed-replacement.png','previous-current-day.png')]
        comparison='<details><summary>Compare vegetation and ground with the original POC</summary><p>The POC is a style/scale reference from an earlier controlled capture. Its viewport and population differ.</p><section class="gallery">'
        for label,source,name in references:
            shutil.copy2(source,out/name)
            comparison+=f'<figure><figcaption>{label}</figcaption><a href="../evidence/{folder}/{name}" target="_blank" rel="noopener"><img loading="lazy" src="../evidence/{folder}/{name}" alt="{label}"></a></figure>'
        comparison+='</section></details>'
    (out/'verification.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8',newline='\n')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>RimQud · in-game day, night and fog</title>
<style>:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#142823;color:#e5e8d8;font:17px/1.5 Georgia,serif}main{max-width:1450px;margin:auto;padding:24px}a{color:#e3cf43}h1{font-weight:normal;font-size:clamp(28px,4vw,42px);margin:16px 0}p{max-width:90ch}.controls{display:flex;flex-wrap:wrap;gap:16px;align-items:center;border-block:1px solid #526b5c;padding:14px 0;margin:24px 0}select{background:#20382d;color:inherit;padding:8px;font:inherit}.gallery{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:0;border:1px solid #526b5c;background:#20382d}figcaption{padding:10px 14px;color:#e3cf43;font:14px/1.5 Consolas,monospace}figcaption span{float:right;color:#b6c8ba;font-size:12px}img{display:block;width:100%;height:auto}small{color:#b6c8ba}a:focus-visible,select:focus-visible{outline:2px solid #e3cf43;outline-offset:4px}@media(max-width:850px){.gallery{grid-template-columns:1fr}main{padding:14px}}</style>
<main><a href="conversion-report.html">Conversion evidence</a> · <a href="current-integration-preview.html">Composition inspector</a><h1>Current art, rendered in Qud</h1>
<p>Four actual captures from Qud’s game camera, using the same generated Joppa layout, player position and current asset selections. Click an image for its full resolution.</p>
<p><strong>Day/night:</strong> the native clock drives Qud’s Daylight component. The adapter adds a blue night tint to converted art. Fully revealed views are diagnostic overrides; native fog views preserve line of sight, exploration and local light. Unsupported or hidden content keeps the native display.</p>
<div class="controls"><label for="display">Show</label><select id="display"><option value="replacement">Current converted art</option><option value="original">Original native rendering</option></select><small>Same camera and native frame</small></div><section class="gallery">__CARDS__</section>
__COMPARISON__<p><small>Native fallback is visible for the player, the newly generated male farmer (the captured template is female), and unsupported status/body states. Rendering comparison only; complete equipment/state/lifecycle acceptance remains pending. <a href="../evidence/__FOLDER__/verification.json">Capture verification</a></small></p></main>
<script>document.querySelector('#display').addEventListener('change',e=>{for(const image of document.querySelectorAll('img[data-replacement]')){image.src=image.dataset[e.target.value];image.closest('a').href=image.src;}});</script></html>'''.replace('__CARDS__',''.join(cards)).replace('__COMPARISON__',comparison).replace('__FOLDER__',folder)
    if revision==2:
        page=page.replace('The adapter adds a blue night tint to converted art.', 'The adapter applies the same night treatment to converted and retained native art.')
        page=page.replace('Unsupported or hidden content keeps the native display.', 'CAI5000’s actual fog shader renders Qud’s visibility/exploration mask. Unseen cells contain no hidden object identities; unsupported art retains the accepted native appearance.')
    (ROOT/'docs/current-game-rendering.html').write_text(page,encoding='utf-8',newline='\n')
    print(json.dumps([dict(phase=x['phase'],mapped=x['mapped'],actors=len(x['current_actor_cells'])) for x in records]))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',required=True,type=Path)
    parser.add_argument('--revision',type=int,choices=[1,2],default=1)
    args=parser.parse_args()
    build(args.root,args.revision)
