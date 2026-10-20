"""Close woven strip ends with rope binding; preserve frays and original construction."""
from pathlib import Path
import sys,math,json,hashlib
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];folder=HERE/'unhung'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'portable-end-correction.json').exists()
outputs=[];inputs=[];sheet=Image.new('RGBA',(1536,768))
for t,f in enumerate(['south','east','north','west']):
    for owner in [False,True]:
        src=folder/(f'ownership-{f}.png' if owner else f'constructed-{f}.svg');inputs.append(ref(src))
        data=(folder/f'constructed-{f}.svg').read_text() if not owner else None
        if owner:
            # Geometry/color ownership has the same path list and paint order.
            import xml.etree.ElementTree as ET
            old=ET.fromstring((folder/f'constructed-{f}.svg').read_text());ns={'s':'http://www.w3.org/2000/svg'};g=old.find('s:g',ns);parts=list(g)
            new=[]
            for i in range(0,len(parts),2):
                border,fill=parts[i:i+2];color='#ffffff' if fill.get('stroke')=='#8dd3dd' else '#000000';new.append(f'<path d="{border.get("d")}" stroke="{color}" stroke-width="{border.get("stroke-width")}"/>')
            data='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g fill="none" stroke-linecap="round" stroke-linejoin="round">'+''.join(new)+'</g></svg>'
        extra=[]
        for end in [0,1]:
            points=[]
            for v in np.linspace(-1,1,65):
                x=(-3.5+1.1*v) if end==0 else (3.5-1.1*v);y=.65*math.sin(math.pi*v/2)+(.35 if end==0 else -.35);z=5.5
                x,y=[(x,y),(-y,x),(-x,-y),(y,-x)][t];points.append((8+x,21+.35*y-z))
            d='M'+' L'.join(f'{x:.4f} {y:.4f}' for x,y in points)
            if owner:extra.append(f'<path d="{d}" stroke="#000000" stroke-width=".34"/>')
            else:extra.append(f'<path d="{d}" stroke="#343434" stroke-width=".34"/><path d="{d}" stroke="#bcbcbc" stroke-width=".21"/>')
        data=data.replace('</g></svg>',''.join(extra)+'</g></svg>');name=f'ownership-{f}-patched' if owner else f'constructed-{f}-patched';(folder/f'{name}.svg').write_bytes(data.encode());p=folder/f'{name}.png';p.write_bytes(svg_to_bytes(svg_string=data));outputs.extend([ref(folder/f'{name}.svg'),ref(p)])
    if t<3:sheet.alpha_composite(Image.open(folder/f'constructed-{f}-patched.png'),(t*512,0))
sheet.save(folder/'constructed-turnaround-patched.png');outputs.append(ref(folder/'constructed-turnaround-patched.png'))
record=dict(status='PASS',reason='Initial portable lattice had unbound cut strip edges above its pale frays. Added two narrow primary-role binding ropes across the actual ribbon end cross-sections; same projection/scale and every previous lattice/fray retained. No opaque backing or end caps.',inputs=inputs,outputs=outputs)
(HERE/'portable-end-correction.json').write_bytes((json.dumps(record,indent=2)+'\n').encode());print('Bound both portable lattice strip ends before contextual refinement.')
