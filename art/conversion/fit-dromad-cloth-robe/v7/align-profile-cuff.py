"""Give the profile sleeve rim and original-arm visibility one shared curve."""
from pathlib import Path
import copy, hashlib, json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
import io

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREV = HERE.parent / 'v6'
BODY = ROOT / 'art/conversion/body-dromad/v2'
SIZE = (512, 1024)

def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def write(p, data):
    p.write_bytes((json.dumps(data, indent=2) + '\n').encode())

def read(p):
    return Image.open(p).convert('RGBA')

def plate(name, rows, title):
    out = Image.new('RGB', (288 * len(rows), 650), '#142823'); d = ImageDraw.Draw(out)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
    d.text((18, 12), title, font=font, fill='#e3cf43')
    for i, (f, im) in enumerate(rows.items()):
        bg = Image.new('RGBA', SIZE, '#20382d'); bg.alpha_composite(im)
        x, y = 16+i*288, 54
        out.paste(bg.convert('RGB').resize((256, 512), Image.Resampling.LANCZOS), (x, y))
        d.line((x+128, y, x+128, y+511), fill='#cebc45')
        d.line((x, y+475, x+255, y+475), fill='#70b8b0')
        d.text((x, 578), f.upper(), font=font, fill='#e3cf43')
    d.text((18, 610), 'Original body fixed; shared profile cuff curve; native acceptance pending.', font=font, fill='#e5e8d8')
    out.save(HERE/name)

cloth = read(PREV/'intact-robe-east.png')
rgba = np.array(cloth)
samples = []
for x in range(205, 291, 5):
    dark = np.flatnonzero((rgba[670:700, x, :3].mean(1) < 90) & (rgba[670:700, x, 3] > 128))
    assert len(dark), x
    samples.append([x, int(dark[0])+670])
samples = np.array(samples)
coeff = np.polynomial.polynomial.polyfit(samples[:, 0], samples[:, 1], 2)
# The existing drawn opening is the landmark. Move four pixels inside its ink,
# rather than fitting a second independent ellipse to the anatomical arm.
x0, x2 = 193., 296.
y0 = np.polynomial.polynomial.polyval(x0, coeff)+4
y2 = np.polynomial.polynomial.polyval(x2, coeff)+4
x1 = (x0+x2)/2
ym = np.polynomial.polynomial.polyval(x1, coeff)+4
y1 = 2*ym-(y0+y2)/2
path = f'M{x0} {y0} Q{x1} {y1} {x2} {y2}'
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><path d="{path}" fill="none" stroke="#272727" stroke-width="6" stroke-linecap="round"/></svg>'
(HERE/'profile-cuff-rim.svg').write_text(svg+'\n', encoding='utf-8')
rim = Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True))).convert('RGBA')
# Cloth remains complete; this is an explicit seam-ink repair, not an alpha cut.
new_cloth = Image.alpha_composite(cloth, rim)
new_cloth.putalpha(cloth.getchannel('A'))
new_cloth.save(HERE/'intact-robe-east.png')
old_mask = np.array(Image.open(PREV/'body-visibility-east.png').convert('L'))
new_mask = old_mask.copy()
ts = np.linspace(0, 1, 513)
curve = [(float((1-t)**2*x0+2*t*(1-t)*x1+t*t*x2), float((1-t)**2*y0+2*t*(1-t)*y1+t*t*y2+3)) for t in ts]
high = Image.new('L', (2048, 4096)); draw = ImageDraw.Draw(high)
draw.polygon([(round(x*4), round(y*4)) for x,y in curve]+[(round(x2*4), 750*4), (round(x0*4), 750*4)], fill=255)
gate = np.array(high.resize(SIZE, Image.Resampling.LANCZOS))
new_mask[670:745, 193:297] = gate[670:745, 193:297]
body = read(BODY/'selected-east.png')
body_pixels = np.array(body)
arm_spans = []
for y in range(685, 816):
    dark = (body_pixels[y,:,:3].mean(1)<90) & (body_pixels[y,:,3]>128)
    left = np.flatnonzero(dark[185:241])+185
    right = np.flatnonzero(dark[265:306])+265
    if len(left) and len(right):
        lo, hi = int(left[0])-1, int(right[-1])+1
        new_mask[y,180:lo] = 0
        new_mask[y,hi+1:315] = 0
        arm_spans.append([y,lo,hi])
mask = Image.fromarray(new_mask)
mask.save(HERE/'body-visibility-east.png')
overlay = body.copy(); overlay.putalpha(ImageChops.multiply(body.getchannel('A'), mask))
overlay.save(HERE/'body-overlay-east.png')
effective = Image.fromarray(np.uint8(new_mask*(np.array(body)[:, :, 3] > 0)))
assembly = Image.composite(body, Image.alpha_composite(body, new_cloth), effective)
assembly.save(HERE/'assembled-east.png')
ImageOps.mirror(assembly).save(HERE/'assembled-west.png')
palette = json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
colors = {key: tuple(bytes.fromhex(value)) for key, value in palette.items()}
def tint(im, color):
    out = ImageOps.colorize(ImageOps.grayscale(im), (0,0,0), color).convert('RGBA')
    out.putalpha(im.getchannel('A'))
    return out
colored_body = tint(body, colors['w'])
body_model = json.loads((BODY/'model.json').read_text())
for row in body_model['views']['east']:
    if row['component'] == 'head-detail':
        colored_body = Image.alpha_composite(colored_body, tint(read(ROOT/row['public_file']), colors['W']))
colored = Image.composite(colored_body, Image.alpha_composite(colored_body, tint(new_cloth, colors['y'])), effective)
colored.save(HERE/'qud-palette-east.png')
model = json.loads((PREV/'model.json').read_text())
for row in model['views']['east']:
    p = HERE/('intact-robe-east.png' if row['component']=='item' else 'body-overlay-east.png')
    row.update(public_file=ref(p)['path'], sha256=ref(p)['sha256'], file='dromad-robe-v7-'+row['component']+'-east.png')
model['occlusion_sources']['east'] = dict(body=ref(BODY/'selected-east.png'), intact_cloth=ref(HERE/'intact-robe-east.png'), mask=ref(HERE/'body-visibility-east.png'))
model['profile_cuff'] = 'One sampled/edited opening curve owns both fabric rim and original-arm foreground. Front/back art unchanged from v6.'
write(HERE/'model.json', model)
assemblies = dict(south=read(PREV/'assembled-south.png'), east=assembly, north=read(PREV/'assembled-north.png'))
assemblies['west (mirror)'] = ImageOps.mirror(assembly)
plate('assembly-comparison.png', assemblies, 'CURRENT ROBE / front hump covered; shared profile cuff and arm boundary')
close = Image.new('RGB', (1000, 700), '#142823'); d=ImageDraw.Draw(close)
for i, (label, im) in enumerate([('v6: independent arm boundary', read(PREV/'assembled-east.png')), ('v7: shared cuff curve / original arm', assembly)]):
    bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im)
    close.paste(bg.crop((175,645,320,825)).resize((435,540)),(25+i*500,65))
    d.text((25+i*500,25),label,fill='#e3cf43')
close.save(HERE/'profile-cuff-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for i,im in enumerate(assemblies.values()):
    t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*120+35,15),t)
    t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*120+12,125),t)
small.save(HERE/'game-scale-review.png')
write(HERE/'registration-decisions.json', dict(body=ref(BODY/'model.json'), previous_model=ref(PREV/'model.json'),
    cloth_source=ref(PREV/'intact-robe-east.png'), source_opening_samples=samples.tolist(),
    quadratic_coefficients=coeff.tolist(), rim_quadratic=[[x0,y0],[x1,y1],[x2,y2]],
    mask_offset_below_rim=3, mask_edited_region=[193,670,297,745],
    semantic_forearm_spans=arm_spans,
    method='Complete cloth alpha retained; explicit neutral cuff ink and body visibility use the same source-opening curve. No whole image stretch or body deformation.',
    front_back='Existing v6 pixels retained, including covered front hump; old staff sheet used obsolete robe v1.',
    new_imagegen_call=False, native_acceptance='Pending full-set gate'))
print('Profile cuff/arm boundary registered from shared source-opening curve; front/back unchanged.')
