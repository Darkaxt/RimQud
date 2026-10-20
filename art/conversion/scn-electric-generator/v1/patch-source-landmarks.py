"""Retain wider left bar and upper wheel rail visible in native sparse linework."""
from pathlib import Path
import json,hashlib,sys,xml.etree.ElementTree as ET
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];NS='{http://www.w3.org/2000/svg}'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'patched-constructed.png').exists()
for label in ['constructed','ownership']:
 root=ET.fromstring((HERE/f'{label}.svg').read_text());group=list(root)[0];marks=[n for n in group if n.tag==NS+'rect' and n.get('x')=='2.6'];assert len(marks)==4
 for node,y in zip(marks,[9.5,13.5,15.5,17.5]):node.set('y',str(y))
 owner=label=='ownership';ET.SubElement(group,NS+'rect',dict(x='2.6',y='11.1',width='4.0',height='.65',rx='.06',fill='#000000' if owner else '#c4c4c4'));ET.SubElement(group,NS+'path',dict(d='M7.15 10.85V9.45H13.5V10.85H13.15V9.8H7.5V10.85Z',fill='#000000' if owner else '#c4c4c4'));svg=ET.tostring(root,encoding='unicode');(HERE/f'patched-{label}.svg').write_bytes(svg.encode());(HERE/f'patched-{label}.png').write_bytes(svg_to_bytes(svg_string=svg))
write(HERE/'source-landmark-patch.json',dict(reason='First manual comparison missed native wider primary bar at left around row11 and partial primary rail above right wheel. Four actual short left marks were also evenly spaced rather than source rows9/13/15/17.',correction='Preserve4shortmarks at source positions, add wider left primary bar and short primary hood/rail above wheel. Case/wheel/frame/palette roles/pivot unchanged.',new_imagegen_calls=0))
packet=json.loads((HERE/'source-packet.json').read_text());packet['previous_packet']=ref(HERE/'source-packet.json');packet['source_shape']='Raised upper rectangular frame/inset bar/open gap, four short left marks at native rows9/13/15/17, a wider left bar around row11, partial primary rail above lower-right detail ring/central point, and low full-width primary rail.';packet['construction']['source_landmark_patch']=ref(HERE/'source-landmark-patch.json');write(HERE/'corrected-source-packet.json',packet);prompt=(HERE/'refine-prompt.txt').read_text();prompt=prompt.replace('four short recessed marks down left','four short recessed marks down left at source rows9/13/15/17, a wider left bar around row11 and partial primary rail above wheel');(HERE/'patched-refine-prompt.txt').write_bytes(prompt.encode());print('Patched missing primary source bars and corrected mark spacing; same case/wheel/frame/roles.')
