"""Remove torso pixels admitted by v3's oversized hand ownership circle.

This corrects a selection mask on retained art; it does not redesign a garment.
The row bounds follow the actual dark hand/wrist contour in this exact body.
They are not a reusable coordinate template for other bodies or clothing.
"""
from pathlib import Path
import copy, hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'v3'
BODY = ROOT / 'art/conversion/body-human-male-older/v2'

def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def write(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')

def read(p):
    return Image.open(p).convert('RGBA')

def tint(im, color):
    a = np.array(im).copy()
    a[:,:,:3] = np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255))
    return Image.fromarray(a)

assert not (HERE/'model.json').exists(), 'Preserve reviewed versions; create a new version for further changes.'
model = copy.deepcopy(json.loads((OLD/'model.json').read_text()))
body = read(BODY/'selected-east.png')
a = np.array(body)
mask = np.zeros(a.shape[:2], float)
bounds = []
xx = np.arange(512)
for y in range(516, 590):
    # Fixed, inspected wrist/hand ROI excludes the distant torso outline.
    xs = np.where(a[y,202:280,:3].mean(1) < 65)[0]+202
    if len(xs):
        left, right = float(xs.min())-.15, float(xs.max())+.15
        bounds.append(dict(y=y, left=left, right=right))
        mask[y] = np.minimum(np.clip(xx-left+.5, 0, 1), np.clip(right-xx+.5, 0, 1))
visibility = np.uint8(np.round(mask*255))
Image.fromarray(visibility).save(HERE/'body-visibility-east.png')
overlay = body.copy()
overlay.putalpha(Image.fromarray(np.uint8(np.round(a[:,:,3]*mask))))
overlay.save(HERE/'body-overlay-east.png')
assert np.array_equal(np.array(overlay)[:,:,:3], a[:,:,:3])
assert np.all(np.array(overlay)[:,:,3] <= a[:,:,3])
write('hand-contour-controls.json', dict(source=ref(BODY/'selected-east.png'), threshold=65,
    roi=[202,516,280,590], horizontal_edge_margin=.15, bounds=bounds,
    purpose='Original wrist/hand ownership only. No body recoloring, translation, scale or garment cut.'))
for row in model['views']['east']:
    if row['component'] == 'body-overlay':
        row.update(public_file=ref(HERE/'body-overlay-east.png')['path'],
                   sha256=ref(HERE/'body-overlay-east.png')['sha256'],
                   file='irudad-black-robes-v4-body-overlay-east.png')
model['occlusion_sources']['east'].update(body_visibility=ref(HERE/'body-visibility-east.png'),
    original_body_overlay=ref(HERE/'body-overlay-east.png'), contour_controls=ref(HERE/'hand-contour-controls.json'))
model['occlusion_sources']['east'].pop('curved_wrist_svg', None)
model['correction'] = 'v3 circle admitted adjacent pale torso beyond the original hand ink. v4 follows the actual wrist/hand contour; intact garment, body pixels, front/back ownership and physical registration are unchanged.'
write('model.json', model)
groups = {k:{} for k in ['assembly', 'palette', 'overlay']}
for face in ['south','east','north']:
    b = read(BODY/f'selected-{face}.png')
    cloth = read(ROOT/model['occlusion_sources'][face]['full_cloth']['path'])
    o = read(ROOT/model['occlusion_sources'][face]['original_body_overlay']['path'])
    assembly = Image.alpha_composite(Image.alpha_composite(b, cloth), o)
    native = Image.alpha_composite(Image.alpha_composite(tint(b,(152,135,95)), tint(cloth,(21,83,82))), tint(o,(152,135,95)))
    for kind, im in [('assembly',assembly), ('palette',native), ('overlay',o)]:
        groups[kind][face] = im
        im.save(HERE/f'{kind}-{face}.png')
for rows in groups.values():
    rows['west (mirror)'] = ImageOps.mirror(rows['east'])
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for kind, name, title in [('assembly','assembly-comparison.png','BLACK ROBES / one original hand contour; retained complete wool'),
    ('palette','independent-palette-comparison.png','NATIVE COLORS / K/K wool and independent original body w'),
    ('overlay','body-overlay-comparison.png','OWNERSHIP / exact hand and wrist; adjacent torso excluded')]:
    out = Image.new('RGB',(1152,660),'#142823'); d = ImageDraw.Draw(out)
    d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(face,im) in enumerate(groups[kind].items()):
        bg=Image.new('RGBA',im.size,'#20382d'); bg.alpha_composite(im); x=16+i*284
        out.paste(bg.convert('RGB').resize((256,512)),(x,54))
        d.line((x+128,54,x+128,565),fill='#e3cf43'); d.line((x,529,x+255,529),fill='#70b8b0')
        d.text((x,584),face.upper(),font=font,fill='#e3cf43')
    d.text((18,620),'Ownership correction only. Original body, whole cloth, frame and contact fixed. Native acceptance pending.',font=font,fill='#e5e8d8')
    out.save(HERE/name)
out=Image.new('RGB',(960,410),'#20382d'); d=ImageDraw.Draw(out)
for i,(title,im) in enumerate([('BARE BODY',body),('v3 OVERSIZED MASK',read(OLD/'body-overlay-east.png')),
    ('v3 COMPOSITION',read(OLD/'assembly-east.png')),('v4 COMPOSITION',groups['assembly']['east'])]):
    crop=im.crop((195,485,305,610)); bg=Image.new('RGBA',crop.size,'#20382d'); bg.alpha_composite(crop)
    out.paste(bg.convert('RGB').resize((220,250)),(i*240,45)); d.text((i*240+3,15),title,font=font,fill='#e3cf43')
d.text((10,335),'Cloth source has no hand. The extra pale crescent was torso admitted by the body mask.',font=font,fill='white')
out.save(HERE/'ownership-before-after.png')
out=Image.new('RGB',(560,370),'#142823'); d=ImageDraw.Draw(out)
for i,(face,im) in enumerate(groups['assembly'].items()):
    small=im.resize((48,96),Image.Resampling.LANCZOS); out.paste(small,(i*140+45,20),small)
    zoom=small.resize((96,192),Image.Resampling.NEAREST); out.paste(zoom,(i*140+20,138),zoom)
    d.text((i*140+4,344),face.upper(),font=font,fill='#e3cf43')
out.save(HERE/'game-scale-review.png')
write('correction-decisions.json', dict(previous=ref(OLD/'model.json'), cause=model['correction'],
    source_attribution=ref(HERE/'source-attribution-closeups.png'), controls=ref(HERE/'hand-contour-controls.json'),
    new_imagegen_call=False, new_blender_model=False,
    method_reason='Mask-selection defect on retained usable artwork, not revised object design. No replacement garment or speculative remodeling.',
    original_body_rgb_unchanged=True, full_cloth_sources_unchanged=True,
    front_back_components_unchanged=model['views']['south']==json.loads((OLD/'model.json').read_text())['views']['south'] and model['views']['north']==json.loads((OLD/'model.json').read_text())['views']['north'],
    side_overlay_changed_pixels=int(np.any(np.array(read(OLD/'body-overlay-east.png'))!=np.array(overlay),axis=2).sum()),
    native_acceptance='Pending full-set generation gate'))
print('Ownership-only correction rendered; independent authoring review pending.')
