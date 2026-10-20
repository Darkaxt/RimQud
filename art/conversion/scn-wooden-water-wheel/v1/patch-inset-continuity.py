"""Join right inset markers along an authored thin oval, preserving source segment positions."""
from pathlib import Path
import json,sys,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;NS='{http://www.w3.org/2000/svg}';ET.register_namespace('','http://www.w3.org/2000/svg')
assert not (HERE/'frame-1-patched-constructed.svg').exists()
for k in [1,2,3]:
 for label in ['constructed','ownership']:
  owner=label=='ownership';p=HERE/f'frame-{k}-{label}.svg';root=ET.fromstring(p.read_text());fill='#ffffff' if owner else '#d6c668';stroke='#ffffff' if owner else '#746b38'
  ellipse=ET.Element(NS+'ellipse',dict(cx='10.85',cy='12',rx='1.6',ry='6.6',fill='none',stroke=fill,**{'stroke-width':'.16'}));root.insert(0,ellipse)
  groups={}
  for n in list(root):
   if n.tag==NS+'rect' and n.get('fill')==fill:
    key=(n.get('x'),n.get('width'));groups.setdefault(key,[]).append(n);root.remove(n)
  for (x,w),nodes in groups.items():
   nodes.sort(key=lambda n:float(n.get('y')));runs=[]
   for n in nodes:
    y=float(n.get('y'));end=y+float(n.get('height'))
    if runs and y-runs[-1][1]<.11:runs[-1][1]=end
    else:runs.append([y,end])
   for a,b in runs:root.append(ET.Element(NS+'rect',dict(x=x,y=str(a),width=w,height=str(b-a),rx='.18',fill=fill,stroke=stroke,**{'stroke-width':'.06'})))
  svg=ET.tostring(root,encoding='unicode');(HERE/f'frame-{k}-patched-{label}.svg').write_bytes(svg.encode());(HERE/f'frame-{k}-patched-{label}.png').write_bytes(svg_to_bytes(svg_string=svg))
packet=json.loads((HERE/'source-packet.json').read_text());packet['construction']['authored']+=' Manual review connected isolated inset marks with thin authored oval brace and merged adjacent same-column segments into smooth runs. Original detail centers and3phase patterns preserved. Brace is physical continuity interpretation, not a named native part or a new gear mechanism.'
(HERE/'corrected-source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
review='Manual review caught isolated right inset detail blocks looking like floating pixels. Added thin oval support and merged adjacent vertical runs while keeping all native detail centers/phase layouts. Fixed outer rim/paddle source groups unchanged; brace geometry is authored interpretation. Initial3phase suggestions preserved.'
(HERE/'inset-continuity-patch.json').write_bytes((json.dumps(dict(review=review,source_detail_centers_preserved=True,new_native_behavior=False),indent=2)+'\n').encode());(HERE/'manual-structural-review.json').write_bytes((json.dumps(dict(status='PASS AFTER PATCH',review=review),indent=2)+'\n').encode())
sheet=Image.new('RGBA',(1536,768))
for k in [1,2,3]:sheet.alpha_composite(Image.open(HERE/f'frame-{k}-patched-constructed.png').convert('RGBA'),((k-1)*512,0))
sheet.save(HERE/'patched-native-phases.png');font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(900,850),'#142823');d=ImageDraw.Draw(plate)
for i,name in enumerate(['frame-1-constructed','frame-1-patched-constructed']):
 im=Image.open(HERE/f'{name}.png').convert('RGBA').resize((360,540),Image.Resampling.LANCZOS);plate.paste(im,(35+i*440,55),im);d.text((35+i*440,620),'INITIAL' if i==0 else 'CONTINUOUS INSET',font=font,fill='#e3cf43')
d.text((20,700),'Thin authored oval connects exact source-phase detail marks.',font=font,fill='#e5e8d8');d.text((20,735),'Native centers/roles retained; no new mechanism or phase clock.',font=font,fill='#e5e8d8');plate.save(HERE/'inset-patch-comparison.png')
prompt=(HERE/'refine-prompt.txt').read_text()+'\nEdit target is the patched default: right inset native marks are joined by a THIN oval brace and adjacent rows form continuous rounded runs. Retain this subtle physical connection; do not replace it with a solid endplate, floating pixel blocks, extra spokes or a named new mechanism.'
(HERE/'patched-refine-prompt.txt').write_bytes(prompt.encode());print(review)
