"""Record the inspected inner-palm correction; resume the unfinished apron."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]

def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def write(p, data):
    p.write_bytes((json.dumps(data, indent=2) + '\n').encode())

lp = ROOT / 'evidence/conversion-ledger.json'
data = json.loads(lp.read_text())
entry = next(e for e in data['entries'] if e['id'] == 'FIT-DROMAD-SHILLELAGH-HAND-2')
assert data['active_entry'] == entry['id'] and not entry['generation_ready']
model = json.loads((HERE / 'model.json').read_text())
previous = json.loads((HERE.parent / 'v1/registered/model.json').read_text())
assert model['views']['east'] == previous['views']['east']
assert model['canvas'] == [512, 1024] and model['contact'] == [256, 950]
for rows in model['views'].values():
    for row in rows:
        p = ROOT / row['public_file']
        assert ref(p)['sha256'] == row['sha256']
        pixels = np.array(Image.open(p).convert('RGBA'))
        assert pixels.shape == (1024, 512, 4)
        opaque = pixels[:, :, 3] > 0
        assert np.max(np.ptp(pixels[:, :, :3][opaque].astype(int), axis=1)) == 0
review = ('Inspected full front/profile/back/west, separate intact item, native equipment y/y tint and 48x96 intended-size plate. '
          'Front shaft grip moved from (105,777) to (140,777), toward body from palm center (126,777); '
          'back from (408,777) to (374,777), toward body from palm center (388,777). '
          'Both now pass inside the palm with original hand foreground. Integer translation only: same complete source, length and angle. '
          'Accepted east item bytes/attachment unchanged; west remains its mirror. '
          'Preview now uses the already selected unchanged v2 body/v6 robe instead of obsolete robe v1. '
          'No new ImageGen call, isolation, anatomy change or native game test. Native attachment/outfit acceptance remains pending.')
write(HERE / 'authoring-review.json', dict(status='GENERATION READY', review=review,
    current_model=ref(HERE / 'model.json'), profile_item_unchanged=True,
    native_acceptance='Pending all-generation gate; authoring correction only'))
write(HERE / 'artifact-manifest.json', dict(files=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'artifact-manifest.json']))

def event(step, action, inputs, outputs):
    entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(), step=step, action=action,
        inputs=[ref(p) for p in inputs], outputs=[ref(p) for p in outputs], review=review, result='PASS', new_imagegen_call=False))

event('construct_and_overlay_one_item', 'Corrected front/back grip by integer translation of the identical full staff. Preserve scale/rotation and accepted profile. Original actual hand supplies foreground, separately from intact item.',
      [HERE.parent / 'v1/registered/model.json', HERE.parent / 'v1/placement-suggestion.json', HERE / 'refit-grip.py'],
      [HERE / 'registration-decisions.json', HERE / 'intact-item-comparison.png', HERE / 'before-after-comparison.png'])
event('recompose_check_cuffs_attachment_occlusion_all_views', 'Reviewed inner-palm grip and original-hand ownership in every required facing on the current fixed body/robe. Full front staff remains uncut; rear staff remains behind original body. Profile item and attachment unchanged.',
      [HERE / 'model.json', ROOT / 'art/conversion/body-dromad/v2/model.json', ROOT / 'art/conversion/fit-dromad-cloth-robe/v6/model.json'],
      [HERE / 'assembly-comparison.png', HERE / 'hand-overlay-south.png', HERE / 'hand-overlay-north.png'])
event('review_game_scale_and_palette', 'Inspected intended-size held silhouette and independent y/y equipment tint; original body/robe/contact unchanged. Skill now records inner-palm attachment and original gripping-hand foreground.',
      [HERE / 'model.json', ROOT / 'skills/qud-creature-conversion/SKILL.md'],
      [HERE / 'palette-comparison.png', HERE / 'game-scale-review.png', HERE / 'authoring-review.json', HERE / 'artifact-manifest.json'])
entry.update(status='UNFINISHED', generation_ready=True, current_step='native_equipment_state_review',
    current_registration=dict(model=ref(HERE / 'model.json'), plate=ref(HERE / 'assembly-comparison.png')),
    art_review=dict(status='PASS', reason=review),
    registration_summary='Front/back shaft translated to the inner palm with original gripping hand above it. Full staff, scale and accepted profile preserved. Current v2 body/v6 robe context; historical v1 retained.',
    known_issues=['Actual native held-state and full outfit acceptance remain pending the full-set generation gate. Authored staff length is preserved; no new user size acceptance claimed.'],
    native_acceptance='Pending final all-conversions validation gate')
nxt = next(e for e in data['entries'] if e['id'] == 'FIT-NIMA-LEATHER-APRON-BODY-0')
assert nxt['status'] == 'UNFINISHED' and not nxt['generation_ready']
nxt.update(status='IN PROGRESS', current_step='source_identity_description_slot_laterality')
data['active_entry'] = nxt['id']
data['updated_at'] = datetime.now(timezone.utc).isoformat()
write(lp, data)
print('Staff authoring correction recorded; Nima apron resumes as sole active entry. Native gate unchanged.')
