"""Bind Nima's actual Sandals to the unchanged shared unmutated female fit."""
from pathlib import Path
import json, hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-sandals/v2'
BODY=ROOT/'art/conversion/body-human-female/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,data):(HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
assert not (HERE/'model.json').exists()
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text())
actor=next(e for e in ledger['entries'] if e['id']=='NPC-NIMA-RUDA')
parts=[p for p in actor['metadata']['native_parts'] if p['type']=='Feet']
assert len(parts)==1 and parts[0]['manager'] is None and parts[0]['laterality']==0
part=parts[0];item=part['equipped'];source_packet=json.loads((SOURCE/'source-packet.json').read_text())
assert item['blueprint']=='Sandals'
for k in ['blueprint','tile','foreground','detailColor']:assert item[k]==source_packet['item'][k]
model=json.loads((SOURCE/'model.json').read_text());model.update(family='nima',unmutated_body_family='human-female',body_source=ref(BODY/'model.json'),actual_equipped_binding=part,native_acceptance='Pending all-conversions gate; BODY-NIMA mutation assembly remains unfinished')
for facing,rows in model['views'].items():
 for row in rows:
  assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
  row['file']=row['file'].replace('human-female-sandals','nima-shared-human-female-sandals')
packet=dict(entry='FIT-NIMA-SANDALS-FEET-0',workflow='regional-curved-v1',creature='Nima Ruda',captured_gender=actor['metadata']['captured_gender'],actual_foot_binding=part,
 original_item=source_packet['item'],original_reference_and_donor=ref(SOURCE/'source-packet.json'),body=ref(BODY/'model.json'),canonical_registration=ref(SOURCE/'model.json'),
 decision='Nima uses the selected unmutated female base. Her ordinary Feet/0 and actual Sandals share blueprint, sprite and palette with the structurally corrected shared fit. Reuse its full sole/strap art and exact masks; no new drawing, fit, body generation, demographic assignment or ImageGen call.',
 mutations='No mutation-managed Feet group is captured. Other individual mutation/body requirements remain on BODY-NIMA and NPC-NIMA-RUDA; this shoe registration does not complete them.',
 context=ref(SOURCE/'refined-red-context.png'),prompt=ref(SOURCE/'imagegen-prompt.txt'),new_imagegen_call=False,
 source_footwear_plate=ref(SOURCE/'footwear-comparison.png'),native_acceptance='Pending all-conversions generation gate')
write('source-packet.json',packet);write('model.json',model)
write('registration-decisions.json',dict(exact_shared_fit=True,canonical_registration=ref(SOURCE/'model.json'),bound_registration=ref(HERE/'model.json'),body_unchanged=True,artwork_unchanged=True,contact=[256,950],equipped_part_id=part['id'],equipped_instance=item['instance'],new_imagegen_call=False))
print('Bound Nima actual Sandals/Feet to the identical shared female art, mask and body; mutation actor work remains separate.')
