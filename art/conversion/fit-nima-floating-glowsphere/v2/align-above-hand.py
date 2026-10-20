"""Apply the user's vertical hand alignment without redrawing the floating item."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=HERE.parent/'v1';BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1024)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
for name in ['canonical-pattern.svg','constructed-canonical.png','canonical-detail-region.png','detail-region.svg','intact-canonical.png','detail-canonical.png','optional-halo-canonical.png','halo-light-marks.svg']:
    shutil.copyfile(SOURCE/name,HERE/name);assert (SOURCE/name).read_bytes()==(HERE/name).read_bytes()
palms={'south':[395,525],'east':[267,535],'north':[111,525]}
controls={f:dict(center=[palm[0],330],palm_landmark=palm,inverse_affine=[1,0,256-palm[0],0,1,512-330]) for f,palm in palms.items()}
write('fit-controls.json',controls)
packet=json.loads((SOURCE/'source-packet.json').read_text());packet.update(recorded_at=datetime.now(timezone.utc).isoformat(),source_version=ref(SOURCE/'source-packet.json'),shared_refinement=dict(context=ref(SOURCE/'refined-red-context.png'),prompt=ref(SOURCE/'imagegen-prompt.txt'),structural_review=ref(SOURCE/'first-refinement-structural-review.json'),new_imagegen_call=False))
packet['frame'].update(centers={f:c['center'] for f,c in controls.items()},placement='User-directed vertical alignment above the chosen ordinary baseline Hand/1 display palm. Match sphere center x to palm x in every facing; retain common sphere center y330, physical size and source slot.',palm_landmarks=palms,native_slot_preserved='Actual Nima Floating Nearby195/0; no change to Hand and no mutation attachment inferred.')
write('source-packet.json',packet)
sheet=Image.new('RGBA',(1536,1024));canonical=Image.open(HERE/'constructed-canonical.png').convert('RGBA')
for i,(f,c) in enumerate(controls.items()):
    item=canonical.transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC);item.save(HERE/f'constructed-item-{f}.png');body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');sheet.paste(Image.alpha_composite(body,item),(i*512,0))
sheet.save(HERE/'constructed-neutral-context.png')
write('hand-alignment-correction.json',dict(timestamp=packet['recorded_at'],user_requirement='Floating sphere should lie vertically above one of the hands.',supersedes=ref(SOURCE/'model.json'),prior_centers=json.loads((SOURCE/'fit-controls.json').read_text()),corrected_controls=controls,unchanged=['Complete opal geometry and selected refined surface','Internal color region and optional halo source','Physical size, body/ground frame and every original body pixel','Actual Floating Nearby slot, native light radius8 and material color keys'],new_imagegen_calls=0,projection='Alignment may put the floating item in front of the torso in profile. Keep it a separate foreground item; do not cut the body or invent a supporting arm/hand pose. Native orbit coordinates were not exported.'))
f=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(f.read_text());assert ledger['active_entry']=='FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
entry['process_log'].append(dict(timestamp=packet['recorded_at'],step='construct_and_overlay_one_item',action='User correction: align the same floating sphere vertically above one ordinary baseline palm in each facing. Change display anchors only; preserve source Floating Nearby binding and surface.',inputs=[ref(SOURCE/'model.json'),ref(SOURCE/'intact-canonical.png')],outputs=[ref(HERE/'fit-controls.json'),ref(HERE/'constructed-neutral-context.png'),ref(HERE/'hand-alignment-correction.json'),ref(HERE/'source-packet.json')],review='South395, east267 and north111 match the existing ordinary palm x coordinates; common y330 retained. West will mirror both east palm and sphere. No new ImageGen call or hand/slot remapping.',result='PASS'))
f.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Aligned sphere center horizontally to palm x in all body facings; actual Floating Nearby slot preserved.')
