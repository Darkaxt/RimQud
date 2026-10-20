"""Record hand-column alignment and the complete source-bound opal authoring."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SOURCE = HERE.parent / 'v1'
BODY = ROOT / 'art/conversion/body-human-female/v2'
IDENT = 'FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0'

def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def write(p, value):
    p.write_bytes((json.dumps(value, indent=2) + '\n').encode())

def read(p):
    return Image.open(p).convert('RGBA')

assert not (HERE / 'authoring-review.json').exists()
model = json.loads((HERE / 'model.json').read_text())
controls = json.loads((HERE / 'fit-controls.json').read_text())
packet = json.loads((HERE / 'source-packet.json').read_text())
for name in ['intact-canonical.png', 'detail-canonical.png', 'optional-halo-canonical.png']:
    assert (HERE / name).read_bytes() == (SOURCE / name).read_bytes()
    a = np.array(read(HERE / name))
    assert np.array_equal(a[:, :, 0], a[:, :, 1]) and np.array_equal(a[:, :, 1], a[:, :, 2])
assert np.array_equal(np.array(read(HERE / 'intact-canonical.png'))[:, :, 3],
                      np.array(read(HERE / 'constructed-canonical.png'))[:, :, 3])
binding = model['actual_equipped_binding']
assert binding['id'] == 195 and binding['type'] == 'Floating Nearby' and binding['manager'] is None
assert model['source_state']['LightSource']['Radius'] == '8'
assert model['source_state']['AnimatedMaterialGeneric']['AnimationLength'] == '200'
checks = {}
for facing, c in controls.items():
    assert c['center'][0] == c['palm_landmark'][0] and c['center'][1] < c['palm_landmark'][1]
    body = read(BODY / f'selected-{facing}.png')
    item = read(HERE / f'intact-item-{facing}.png')
    detail = read(HERE / f'item-detail-{facing}.png')
    halo = read(HERE / f'optional-halo-{facing}.png')
    expected = Image.alpha_composite(Image.alpha_composite(halo, body), Image.alpha_composite(item, detail))
    assert np.array_equal(np.array(expected), np.array(read(HERE / f'assembled-{facing}.png')))
    for row in model['views'][facing]:
        assert row['contact'] == [256, 950] and row['size'] == [512, 1024]
        assert ref(ROOT / row['public_file'])['sha256'] == row['sha256']
    checks[facing] = dict(sphere_center=c['center'], palm=c['palm_landmark'], horizontal_offset=0,
                          original_body=True, exact_recomposition=True, item_scale_unchanged=True)
east = controls['east']
checks['west'] = dict(sphere_center=[511-east['center'][0], east['center'][1]],
                      palm=[511-east['palm_landmark'][0], east['palm_landmark'][1]],
                      horizontal_offset=0, mirrored_with_body=True)

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
guide = Image.new('RGB', (1152, 665), '#142823')
draw = ImageDraw.Draw(guide)
draw.text((18, 14), 'HAND ALIGNMENT / sphere center and palm share the same vertical line', font=font, fill='#e3cf43')
for i, (facing, c) in enumerate(checks.items()):
    image = read(HERE / f'assembled-{facing}.png') if facing != 'west' else ImageOps.mirror(read(HERE / 'assembled-east.png'))
    panel = Image.new('RGBA', image.size, '#20382d')
    panel.alpha_composite(image)
    d = ImageDraw.Draw(panel)
    x, y = c['sphere_center']; px, py = c['palm']
    d.line((x, y, px, py), fill='#e3cf43', width=2)
    for lx, ly in [c['sphere_center'], c['palm']]:
        d.ellipse((lx-5, ly-5, lx+5, ly+5), outline='#e3cf43', width=2)
    guide.paste(panel.convert('RGB').resize((256, 512)), (16+i*284, 54))
    draw.text((16+i*284, 584), f'{facing.upper()} / x {x} / offset 0', font=font, fill='#e3cf43')
draw.text((18, 622), 'Guides are report-only. Source slot remains Floating Nearby; no new hand pose or native orbit claim.', font=font, fill='#e5e8d8')
guide.save(HERE / 'hand-alignment-guide.png')

reason = ('Inspected the same complete palm-size opal, independent detail region, optional halo, all cardinal '
          'display facings, source color keys and intended-size plate. Sphere center matches one existing '
          'palm column in every facing, including mirrored west. Only display translations changed; selected '
          'material, full alpha, physical size and original body remain unchanged. Source Floating Nearby195/0 '
          'binding, light radius8 and animated color keys are preserved. Profile torso overlap is projection '
          'of the separate foreground item, not a body edit or new supporting hand. Native state/orbit and '
          'Nima mutation/outfit acceptance remain pending the full generation set.')
review = dict(timestamp=datetime.now(timezone.utc).isoformat(), status='PASS', scope='Generation authoring only',
              reason=reason, checks=checks, correction=ref(HERE / 'hand-alignment-correction.json'),
              structural_gate=ref(SOURCE / 'first-refinement-structural-review.json'),
              new_imagegen_calls_for_placement=0, no_second_isolation=True,
              native_acceptance=model['native_acceptance'])
write(HERE / 'authoring-review.json', review)
write(HERE / 'artifact-manifest.json', dict(artifacts=[ref(p) for p in sorted(HERE.iterdir())
                                                     if p.is_file() and p.name != 'artifact-manifest.json']))
path = ROOT / 'evidence/conversion-ledger.json'
ledger = json.loads(path.read_text())
assert ledger['active_entry'] == IDENT
entry = next(e for e in ledger['entries'] if e['id'] == IDENT)
for step, action, outputs in [
    ('retrieve_isolated_item_and_masks',
     'Register neutral material from the one contextual refinement into fixed complete opal alpha; retain independent detail and optional halo. No second generative isolation.',
     ['register-aligned-glowsphere.py', 'registration-decisions.json', 'full-item-comparison.png', 'detail-region-comparison.png', 'optional-halo-comparison.png']),
    ('recompose_check_cuffs_attachment_occlusion_all_views',
     'Apply user-directed vertical alignment over one ordinary palm per facing; preserve fixed body and actual floating slot. Recompose the same separate full sphere without hand cutouts.',
     ['model.json', 'assembly-comparison.png', 'hand-alignment-guide.png', 'halo-off-comparison.png']),
    ('review_game_scale_and_palette',
     'Inspect palm-relative physical size, all source color-animation keys, independent neutral layers and intended-size views. Native light/orbit/animation acceptance stays gated.',
     ['independent-palette-comparison.png', 'native-color-keys-comparison.png', 'game-scale-review.png', 'authoring-review.json', 'artifact-manifest.json'])]:
    entry['process_log'].append(dict(timestamp=review['timestamp'], step=step, action=action,
        inputs=[ref(HERE / 'source-packet.json'), ref(SOURCE / 'refined-red-context.png'),
                ref(SOURCE / 'first-refinement-structural-review.json')],
        outputs=[ref(HERE / n) for n in outputs], review=reason, result='PASS'))
entry.update(status='UNFINISHED', generation_ready=True, current_step='native_equipment_state_review',
             known_issues=[], art_review=dict(status='PASS', reason=reason),
             current_registration=dict(model=ref(HERE / 'model.json'), plate=ref(HERE / 'assembly-comparison.png')),
             registration_summary='Palm-size floating opal, vertically above one baseline palm in every view; unchanged physical size/material, independent native color region and optional separate halo. Actual Nima Floating Nearby195/0 retained; native orbit/light/color-state and individual assembly pending.',
             native_acceptance=model['native_acceptance'])
next_id = 'ITEM-FLOATING-GLOWSPHERE'
next_entry = next(e for e in ledger['entries'] if e['id'] == next_id)
next_entry.update(status='IN PROGRESS', current_step='source_identity_description_slot_laterality')
ledger.update(active_entry=next_id, updated_at=review['timestamp'])
assert [e['id'] for e in ledger['entries'] if e['status'] == 'IN PROGRESS'] == [next_id]
write(path, ledger)
print('Floating opal authoring ready with zero horizontal palm offset in all facings; native acceptance pending.')
