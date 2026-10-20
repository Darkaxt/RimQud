"""Collect the two actual monocle authoring records, including explicit west art."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
lp=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(lp.read_text());entry=next(e for e in ledger['entries'] if e['id']=='ITEM-TELESCOPIC-MONOCLE');assert ledger['active_entry']==entry['id'] and not entry['generation_ready']
fits=[e for e in ledger['entries'] if e['category']=='Body/equipment fittings' and entry['id'] in e['related_entries']];assert len(fits)==2
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);out=Image.new('RGB',(1152,770),'#142823');d=ImageDraw.Draw(out);d.text((18,14),'TELESCOPIC MONOCLE / one source, two original-body fits, explicit four facings',font=font,fill='#e3cf43')
for i,e in enumerate(fits):
 assert e['generation_ready'] and e['art_review']['status']=='PASS';passed={x['step'] for x in e['process_log'] if x.get('result')=='PASS'};assert set(e['required_steps'])-{'native_equipment_state_review'}<=passed
 p=ROOT/e['current_registration']['model']['path'];assert ref(p)==e['current_registration']['model'];m=json.loads(p.read_text());assert set(m['views'])=={'south','east','north','west'};folder=p.parent
 d.text((18,55+i*330),e['name'],font=font,fill='#e3cf43')
 for j,f in enumerate(['south','east','north','west']):
  im=Image.open(folder/f'assembly-{f}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+j*284;y=84+i*330;out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,y));d.text((x,y+268),f.upper(),font=font,fill='#e3cf43')
d.text((18,738),'Authoring only. Explicit west direction binding and native outfit acceptance remain pending.',font=font,fill='#e5e8d8');out.save(HERE/'body-fittings-comparison.png')
source=json.loads((ROOT/'art/conversion/fit-human-female-telescopic-monocle/v1/source-packet.json').read_text())
packet=dict(item='Telescopic Monocle',workflow='regional-curved-v1',source=source['item'],fittings=[dict(entry=e['id'],registration=e['current_registration'],authoring_review=e['art_review']) for e in fits],scope='All two enumerated Face/0 authoring fits reuse the same complete ocular/barrel/chain; male fit has target-original head-relative controls and visibility. No actor or native acceptance completion claimed.',expected_views=['south','east','north','west explicit'],native_acceptance='Pending full-set gate, explicit-west direction binding and combined outfit precedence')
(HERE/'fittings.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode());print('Collected both actual monocle authoring records; aggregate inspection pending.')
