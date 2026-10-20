"""Collect the actual three generation-ready headwear fitting records."""
from pathlib import Path
import json, hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());entry=next(e for e in ledger['entries'] if e['id']=='ITEM-WIDE-BRIMMED-HAT')
assert ledger['active_entry']==entry['id'] and not entry['generation_ready']
fits=[e for e in ledger['entries'] if e['category']=='Body/equipment fittings' and entry['id'] in e['related_entries']]
assert len(fits)==3
out=Image.new('RGB',(1152,1080),'#142823');d=ImageDraw.Draw(out);d.text((18,14),'WIDE-BRIMMED HAT / actual Head/0 fittings; one canonical item',font=FONT,fill='#e3cf43')
for i,e in enumerate(fits):
 assert e['generation_ready'] and e['art_review']['status']=='PASS'
 passed={ev['step'] for ev in e['process_log'] if ev.get('result')=='PASS'};assert set(e['required_steps'])-{'native_equipment_state_review'}<=passed
 model_path=ROOT/e['current_registration']['model']['path'];assert ref(model_path)==e['current_registration']['model'];model=json.loads(model_path.read_text())
 d.text((18,55+i*330),e['name'],font=FONT,fill='#e3cf43')
 for j,f in enumerate(['south','east','north']):
  p=ROOT/model['views'][f][0]['public_file'];body=ROOT/('art/conversion/body-human-male/v2' if model['family']=='human-male' else 'art/conversion/body-human-female/v2')/f'selected-{f}.png'
  image=Image.alpha_composite(Image.open(body).convert('RGBA'),Image.open(p).convert('RGBA'));bg=Image.new('RGBA',image.size,'#20382d');bg.alpha_composite(image)
  x=18+j*378;y=84+i*330;out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,y));d.text((x,y+268),f.upper(),font=FONT,fill='#e3cf43')
d.text((18,1050),'Authoring only. Named mutation assemblies and native equip/unequip remain pending full-set gate.',font=FONT,fill='#e5e8d8');out.save(HERE/'body-fittings-comparison.png')
source=json.loads((ROOT/'art/conversion/fit-human-female-wide-brimmed-hat/v1/source-packet.json').read_text())
packet=dict(item='Wide-brimmed Hat',workflow='regional-curved-v1',source=source['item'],scope='All three enumerated Head/0 authoring fits. Female canonical contextual item, male whole-hat head-relative fit, exact shared Nima female binding. No modifier/mutation body completion or native acceptance claimed.',fittings=[dict(entry=e['id'],registration=e['current_registration'],authoring_review=e['art_review']) for e in fits],native_acceptance='Pending full-set generation gate',expected_views=['south','east','north','west mirror review'])
(HERE/'fittings.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode());print('Collected three actual generation-ready fittings; aggregate plate awaits inspection.')
