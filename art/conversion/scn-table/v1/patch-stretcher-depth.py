"""Correct draw ownership of central crossbar hidden behind outside trestle boards."""
from pathlib import Path
import xml.etree.ElementTree as ET,json,sys
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent
assert not (HERE/'patched-empty-front-guided-turnaround.png').exists();empty=Image.new('RGBA',(1536,768));states={f'occupied-{k}':Image.new('RGBA',(1536,1536)) for k in range(1,5)}
for i,f in enumerate(['south','east','north','west']):
    root=ET.fromstring((HERE/f'constructed-{f}-base.svg').read_text());groups=list(root);assert len(groups)==6;root.remove(groups[4]);root.insert(0,groups[4]);svg=ET.tostring(root,encoding='unicode');(HERE/f'patched-{f}-base.svg').write_bytes(svg.encode());(HERE/f'patched-{f}-base.png').write_bytes(svg_to_bytes(svg_string=svg));base=Image.open(HERE/f'patched-{f}-base.png').convert('RGBA')
    if i<3:empty.alpha_composite(base,(i*512,0))
    for state,sheet in states.items():
        panel=base.copy();panel.alpha_composite(Image.open(HERE/f'{state}-{f}-stock.png').convert('RGBA'));panel.save(HERE/f'{state}-{f}-patched-manual.png');sheet.alpha_composite(panel,((i%2)*768+128,(i//2)*768))
empty.save(HERE/'patched-empty-front-guided-turnaround.png')
for state,sheet in states.items():sheet.save(HERE/f'{state}-patched-manual-turnaround.png')
(HERE/'stretcher-depth-patch.json').write_bytes((json.dumps(dict(reason='Initial manual end view drew central stretcher over near outside end board. Move the same crossbar behind both end boards so it remains visible only through the actual open front/back gap.',method='Change cuboid painter order only, no geometry/stock/dimensions/frame/scale changes.',new_imagegen_calls=0),indent=2)+'\n').encode());s=(HERE/'empty-turnaround-prompt.txt').read_text();(HERE/'patched-empty-turnaround-prompt.txt').write_bytes((s+'\nThe central stretcher is behind the outside trestle end board. Preserve patched occlusion: E end is solid board without a pasted central vertical stretcher stripe.').encode());print('Corrected shared base occlusion in every direction and all source stock contexts.')
