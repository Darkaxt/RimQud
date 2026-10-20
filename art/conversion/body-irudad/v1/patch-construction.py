"""Correct visible tail attachment/depth before any refinement; preserve first proposal."""
from pathlib import Path
import json, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,1264)
source=(HERE/'tail-east.svg').read_text()
old='M169 868 Q78 918 71 1023 Q66 1100 103 1145 L126 1134 L117 1165 L127 1185 L100 1171 L80 1180 L84 1152 Q29 1089 36 1017 Q45 909 154 848 Z'
new='M232 872 Q81 913 71 1023 Q66 1100 103 1145 L126 1134 L117 1165 L127 1185 L100 1171 L80 1180 L84 1152 Q29 1089 36 1017 Q45 895 224 842 Z'
assert old in source
source=source.replace(old,new)
(HERE/'patched-tail-east.svg').write_bytes(source.encode());(HERE/'patched-tail-east.png').write_bytes(svg_to_bytes(svg_string=source))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
out=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'IRUDAD / tail root repaired; north tail now belongs above rear surface',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.new('RGBA',SIZE)
    tail=Image.open(HERE/('patched-tail-east.png' if f=='east' else f'tail-{f}.png')).convert('RGBA')
    if f!='north':im.alpha_composite(tail)
    im.alpha_composite(Image.open(HERE/f'raised-arms-{f}.png').convert('RGBA'))
    im.alpha_composite(Image.open(HERE/f'baseline-{f}.png').convert('RGBA'))
    if f=='north':im.alpha_composite(tail)
    im.alpha_composite(Image.open(HERE/f'hands-face-{f}.png').convert('RGBA'))
    im.save(HERE/f'patched-construction-{f}.png');small=im.resize((240,593),Image.Resampling.LANCZOS);out.paste(small,(40+i*330,55),small);d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Baseline untouched. Front selected as anchor; no mouth or rear eyes on the joined-hand face.',font=font,fill='#e5e8d8');out.save(HERE/'patched-construction-turnaround.png')
(HERE/'construction-corrections.json').write_bytes((json.dumps(dict(status='PATCHED FOR REVIEW',rejected='constructed-turnaround.png',changes=['Side tail root floated clear of the hip: extend its hidden root into the unchanged posterior pelvis.','North tail was mostly hidden behind the legs: render the posterior tail above the camera-facing rear body; front/side remain behind.'],unchanged='All baseline body/head pixels, registration, scale, arm/hand-face geometry and front anchor.'),indent=2)+'\n').encode())
print('Patched only the disconnected side tail root and north tail depth; initial construction retained.')
