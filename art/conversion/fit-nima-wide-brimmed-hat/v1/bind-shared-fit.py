"""Bind Nima's actual ordinary Head/0 hat to the unchanged shared female fit."""
from pathlib import Path
import json, hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-wide-brimmed-hat/v1';BODY=ROOT/'art/conversion/body-human-female/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'model.json').exists()
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());actor=next(e for e in ledger['entries'] if e['id']=='NPC-NIMA-RUDA')
parts=[p for p in actor['metadata']['native_parts'] if p['type']=='Head'];assert len(parts)==1
part=parts[0];assert part['manager'] is None and part['laterality']==0;item=part['equipped'];sp=json.loads((SOURCE/'source-packet.json').read_text())
for key in ['blueprint','tile','foreground','detailColor']:assert item[key]==sp['item'][key]
model=json.loads((SOURCE/'model.json').read_text());model.update(family='nima',unmutated_body_family='human-female',body_source=ref(BODY/'model.json'),actual_equipped_binding=part,native_acceptance='Pending all-conversions gate; BODY-NIMA mutation assembly remains unfinished')
for rows in model['views'].values():
 for row in rows:
  assert ref(ROOT/row['public_file'])['sha256']==row['sha256'];row['file']=row['file'].replace('human-female-wide-brimmed-hat','nima-shared-human-female-wide-brimmed-hat')
packet=dict(entry='FIT-NIMA-WIDE-BRIMMED-HAT-HEAD-0',workflow='regional-curved-v1',creature='Nima Ruda',captured_gender=actor['metadata']['captured_gender'],actual_head_binding=part,original_item=sp['item'],original_reference_and_donor=ref(SOURCE/'source-packet.json'),body=ref(BODY/'model.json'),canonical_registration=ref(SOURCE/'model.json'),context=ref(SOURCE/'refined-red-context.png'),prompt=ref(SOURCE/'imagegen-prompt.txt'),new_imagegen_call=False,
 decision='Actual ordinary Head/0 and Wide-brimmed Hat share blueprint, sprite and y/b palette with the reviewed female base. Reuse exact complete hat/band pixels and zero body visibility, common frame/contact and original unmutated body. No redundant ImageGen call, fit or one-off anatomy.',
 mutations='No mutation-managed Head group captured. Other individual mutation requirements remain on BODY-NIMA and NPC-NIMA-RUDA; this hat does not complete them.',source_headwear_plate=ref(SOURCE/'headwear-comparison.png'),native_acceptance='Pending full-set generation gate')
write('source-packet.json',packet);write('model.json',model);write('registration-decisions.json',dict(exact_shared_fit=True,canonical_registration=ref(SOURCE/'model.json'),bound_registration=ref(HERE/'model.json'),original_body_unchanged=True,artwork_unchanged=True,contact=[256,950],equipped_part_id=part['id'],equipped_instance=item['instance'],new_imagegen_call=False))
print('Bound Nima actual Head',part['id'],'hat instance',item['instance'],'to the unchanged shared female fit; native actor work remains pending.')
