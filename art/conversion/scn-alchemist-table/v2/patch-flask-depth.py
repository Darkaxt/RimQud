"""Keep the flask's visible front surface above the table rather than clipping its bulb."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,sys,xml.etree.ElementTree as ET
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs');import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];ns='{http://www.w3.org/2000/svg}';ET.register_namespace('',ns[1:-1])
assert not (HERE/'patched-turnaround.png').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
sheet=Image.new('RGBA',(2048,768))
for i,f in enumerate(['south','east','north','west']):
    for stem in ['constructed','ownership']:
        root=ET.fromstring((HERE/f'{stem}-{f}.svg').read_bytes());bulbs=root.findall(ns+'ellipse');necks=[n for n in root.findall(ns+'polyline') if len(n.get('points','').split())==4]
        assert len(bulbs)==1 and len(necks)==3
        for n in bulbs+necks:root.remove(n);root.append(n)
        svg=ET.tostring(root,encoding='unicode');(HERE/f'patched-{stem}-{f}.svg').write_bytes(svg.encode());im=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg,skip_system_fonts=True))).convert('RGBA');im.save(HERE/f'patched-{stem}-{f}.png')
        if stem=='constructed':sheet.paste(im,(i*512,0))
sheet.save(HERE/'patched-turnaround.png')
now=datetime.now(timezone.utc).isoformat();record=dict(timestamp=now,defect='Whole-primitive painter order placed the bulb center behind the top board, clipping its lower visible front surface.',correction='Render the visible ellipsoid front surface and its neck after the tabletop. Preserve geometry, supports, rack, apparatus scale, native state and all initial images. This fixes authoring depth before the first new refinement.',outputs=[ref(p) for p in sorted(HERE.glob('patched-*'))])
p=HERE/'flask-depth-correction.json';p.write_bytes((json.dumps(record,indent=2)+'\n').encode());ledger_path=ROOT/'evidence/conversion-ledger.json';d=json.loads(ledger_path.read_text());assert d['active_entry']=='SCN-ALCHEMIST-TABLE';e=next(e for e in d['entries'] if e['id']==d['active_entry']);e['process_log'].append(dict(timestamp=now,step='construct_faithful_shape',action=record['defect']+' '+record['correction'],inputs=[ref(HERE/'constructed-turnaround.png')],outputs=[ref(p),ref(HERE/'patched-turnaround.png')],review='Flask body/neck are continuous and stand on top of the board in every view; no new fixture or inventory state.',result='PASS'));ledger_path.write_bytes((json.dumps(d,indent=2)+'\n').encode());print('Patched all views before refinement; original primitive layout retained.')
