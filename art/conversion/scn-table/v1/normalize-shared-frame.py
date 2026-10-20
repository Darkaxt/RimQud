"""Recover high stock edge using one whole-object registration, never per-state/view fitting."""
from pathlib import Path
import json,hashlib,sys,xml.etree.ElementTree as ET
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SCALE=.92
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'registered-source-packet.json').exists();packet=json.loads((HERE/'source-packet.json').read_text());packet['previous_packet']=ref(HERE/'source-packet.json');packet['frame']['normalization']=dict(uniform_scale=SCALE,pivot=[8,16],scope='Every full base and stock component in every state/facing',reason='Initial occupied1E neck extends above original canvas at y≈-.6. Reproject original editable vector before rasterization, not scale already-clipped stock. Same base material scaled once for all states.');write(HERE/'registered-source-packet.json',packet);write(HERE/'shared-frame-correction.json',dict(before='occupied-1-front-guided-turnaround.png',after='occupied-1-normalized-turnaround.png',scale=SCALE,pivot=[8,16],cause='Authored tall stock above E edge after physical rotation; initial S/N fit did not prove shared frame sufficiency.',scope='One identical whole-object transform for base/material/stock in all states/facings. No local fitting or part size change relative to table.',new_imagegen_calls=0))
for f in ['south','east','north','west']:
 im=Image.open(HERE/f'selected-{f}-base-neutral.png').convert('RGBA');im=im.convert('RGBa').transform((512,768),Image.Transform.AFFINE,(1/SCALE,0,256-256/SCALE,0,1/SCALE,512-512/SCALE),Image.Resampling.BICUBIC).convert('RGBA');im.save(HERE/f'normalized-{f}-base-neutral.png')
 for k in range(1,5):
  state=f'occupied-{k}';root=ET.fromstring((HERE/f'{state}-{f}-stock.svg').read_text());group=ET.Element('{http://www.w3.org/2000/svg}g',dict(transform=f'translate(8 16) scale({SCALE}) translate(-8 -16)'))
  for child in list(root):root.remove(child);group.append(child)
  root.append(group);s=ET.tostring(root,encoding='unicode');(HERE/f'normalized-{state}-{f}-stock.svg').write_bytes(s.encode());(HERE/f'normalized-{state}-{f}-stock.png').write_bytes(svg_to_bytes(svg_string=s))
for k in range(1,5):
 state=f'occupied-{k}';sheet=Image.new('RGBA',(1536,1536))
 for i,f in enumerate(['south','east','north','west']):
  im=Image.open(HERE/f'normalized-{f}-base-neutral.png').convert('RGBA');im.alpha_composite(Image.open(HERE/f'normalized-{state}-{f}-stock.png').convert('RGBA'));im.save(HERE/f'{state}-{f}-normalized-context.png');sheet.alpha_composite(im,((i%2)*768+128,(i//2)*768))
 sheet.save(HERE/f'{state}-normalized-turnaround.png');prompt=(HERE/f'{state}-turnaround-prompt.txt').read_text()+'\nOne uniform0.92whole-object registration about native pivot8,16 is already applied to every base and stock view. Preserve that shared transformation; the formerly high E neck is complete with top margin. Do not undo normalization or fit any panel independently.';(HERE/f'{state}-normalized-prompt.txt').write_bytes(prompt.encode())
print('Recovered original vector stock beyond former frame and applied identical whole-object registration across complete set.')
