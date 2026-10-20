"""Index the completed floating-opal authoring; retain native state ownership."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FIT = ROOT / 'art/conversion/fit-nima-floating-glowsphere/v2'

def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def write(p, value):
    p.write_bytes((json.dumps(value, indent=2) + '\n').encode())

path = ROOT / 'evidence/conversion-ledger.json'
ledger = json.loads(path.read_text())
assert ledger['active_entry'] == 'ITEM-FLOATING-GLOWSPHERE'
entry = next(e for e in ledger['entries'] if e['id'] == ledger['active_entry'])
fits = [next(e for e in ledger['entries'] if e['id'] == ident) for ident in entry['related_entries']]
assert len(fits) == 1 and all(e.get('generation_ready') and e['art_review']['status'] == 'PASS' for e in fits)
model = json.loads((FIT / 'model.json').read_text())
for rows in model['views'].values():
    for row in rows:
        assert ref(ROOT / row['public_file'])['sha256'] == row['sha256']
record = dict(item='Floating Glowsphere', source=entry['metadata']['original_reference'],
    fittings=[dict(entry=fits[0]['id'], registration=fits[0]['current_registration'],
                   source_packet=ref(FIT / 'source-packet.json'), authoring_review=ref(FIT / 'authoring-review.json'),
                   alignment=ref(FIT / 'hand-alignment-correction.json'))],
    scope='Actual Nima item538 on ordinary Floating Nearby195/0; reusable unmutated female body. Named mutations and outfit remain separate.',
    source_identity='Palm-size floating phosphorescent opal. Full neutral sphere, independent native color region and separately retained optional halo.',
    placement='User-directed display alignment vertically above one ordinary palm in every facing; same material/scale, no hand-slot reassignment or supporting-limb invention.',
    native_state=model['source_state'],
    limits='Authoring only. Native floating placement/orbit, material timing units, light radius8 behavior, optional halo support and individual Nima assembly remain pending full-set integration.',
    new_imagegen_calls=0)
write(HERE / 'fittings.json', record)
reason = ('Reviewed the sole required fitting and its corrected hand-column placement, complete source/refinement '
          'chain, original body/frame, neutral layers, independent palette and intended-size views. Actual '
          'Floating Nearby binding retained; no new generation or native state acceptance claimed.')
now = datetime.now(timezone.utc).isoformat()
for step, action in [
    ('resolve_item_identity_description_palette', 'Resolve actual palm-size floating opal, captured Floating Nearby slot, independent primary/detail color keys and native light metadata.'),
    ('verify_every_body_fitting_log', 'Reconcile the sole listed fitting and user-corrected vertical alignment in every facing; preserve full unchanged sphere and exact original body.'),
    ('record_item_acceptance_from_all_fittings', 'Index generation-ready authoring only; retain pending native floating/color/light state and individual assembly.')]:
    entry['process_log'].append(dict(timestamp=now, step=step, action=action,
        inputs=[fits[0]['current_registration']['model'], ref(FIT / 'authoring-review.json')],
        outputs=[ref(HERE / 'fittings.json'), ref(FIT / 'assembly-comparison.png'), ref(FIT / 'hand-alignment-guide.png')],
        review=reason, result='PASS'))
entry.update(status='UNFINISHED', generation_ready=True, known_issues=[],
             current_step='record_item_acceptance_from_all_fittings', art_review=dict(status='PASS', reason=reason),
             current_registration=dict(model=ref(HERE / 'fittings.json'), plate=ref(FIT / 'assembly-comparison.png')),
             registration_summary='Authoring index for Nima floating opal: sphere vertically above one palm, separate native color region and optional halo. Source Floating Nearby binding retained; native acceptance pending.',
             native_acceptance=model['native_acceptance'])
next_id = 'FIT-IRUDAD-WALKING-STICK-HAND-6'
next_entry = next(e for e in ledger['entries'] if e['id'] == next_id)
next_entry.update(status='IN PROGRESS', current_step='source_identity_description_slot_laterality')
ledger.update(active_entry=next_id, updated_at=now)
assert [e['id'] for e in ledger['entries'] if e['status'] == 'IN PROGRESS'] == [next_id]
write(path, ledger)
print('Floating Glowsphere authoring indexed; native acceptance pending. Next sole active entry: Irudad Walking Stick.')
