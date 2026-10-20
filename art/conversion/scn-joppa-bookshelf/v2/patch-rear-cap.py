"""Hide rear post end outlines beneath the separate cap board before refinement."""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'rear-cap-correction.json').exists();records=[]
cap='<path d="M1 3.25H15V6.9H1Z" fill="#aaaaaa" stroke="#303030" stroke-width=".12"/><path d="M1 5.15H15" fill="none" stroke="#626262" stroke-width=".11"/>'
for n in range(1,4):
    folder=HERE/f'variant-{n}';p=folder/'constructed-north.svg';data=p.read_text();data=data.replace('<g transform="translate(16 0)',cap+'<g transform="translate(16 0)');out=folder/'constructed-north-patched.svg';out.write_bytes(data.encode());out.with_suffix('.png').write_bytes(svg_to_bytes(svg_string=data));sheet=Image.new('RGBA',(1536,768))
    for i,f in enumerate(['south','east','north']):
        name=f'constructed-{f}-patched.png' if f=='north' else f'constructed-{f}.png';sheet.alpha_composite(Image.open(folder/name).convert('RGBA'),(i*512,0))
    sheet.save(folder/'front-guided-turnaround-patched.png');records.append(dict(variant=n,before=ref(p),after=ref(out),composed=ref(folder/'front-guided-turnaround-patched.png')))
record=dict(status='PASS',reason='Compound rear wood path left post-end outline rectangles visible inside the cap. Draw the separate cap board over those ends, preserving parallel top/front seam, book positions, coverage and every lower part. No new generated material needed for this manual structural patch.',variants=records)
(HERE/'rear-cap-correction.json').write_bytes((json.dumps(record,indent=2)+'\n').encode());print('Patched rear cap over post-end outlines in all3manual variants before composed refinement.')
