"""Register the approved regional cloth and curved visibility; no new fitting."""
from pathlib import Path
import hashlib, json, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
BODY = ROOT/'art/conversion/body-dromad/v2'
assert not (HERE/'model.json').exists(), 'Preserve recorded versions'
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)


def ref(p):
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(p):
    return Image.open(p).convert('RGBA')


def tinted(im, rgb):
    gray = np.array(ImageOps.grayscale(im)).astype(float)
    rgba = np.array(im).copy()
    rgba[:, :, :3] = np.uint8(np.round(gray[:, :, None]*np.array(rgb)/255))
    return Image.fromarray(rgba)


def compose(body, cloth, mask):
    actual = np.array(body)[:, :, 3] > 0
    coverage = Image.fromarray(np.uint8(np.array(mask)*actual))
    return Image.composite(body, Image.alpha_composite(body, cloth), coverage)


def plate(name, images, title):
    out = Image.new('RGB', (1152, 660), '#142823'); d = ImageDraw.Draw(out)
    d.text((18, 14), title, font=FONT, fill='#e3cf43')
    for i, (f, im) in enumerate(images.items()):
        bg = Image.new('RGBA', im.size, '#20382d'); bg.alpha_composite(im)
        x = 16+i*284; out.paste(bg.convert('RGB').resize((256, 512)), (x, 54))
        d.line((x+128, 54, x+128, 565), fill='#e3cf43'); d.line((x, 529, x+255, 529), fill='#70b8b0')
        d.text((x, 584), f.upper(), font=FONT, fill='#e3cf43')
    d.text((18, 620), 'Regional-curved-v1 / authoring registration. Original body fixed; native acceptance pending full set.', font=FONT, fill='#e5e8d8')
    out.save(HERE/name)


model = json.loads((BASE/'v5/model.json').read_text())
body_model = json.loads((BODY/'model.json').read_text())
palette = json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text(encoding='utf-8'))['native_palette']
colors = {k: tuple(bytes.fromhex(v)) for k, v in palette.items()}
packet = json.loads((BASE/'v1/source-packet.json').read_text())
body_packet = json.loads((ROOT/'art/conversion/body-dromad/v1/source-packet.json').read_text())
appearance = body_packet['appearance']
body_key = (appearance.get('tileColor') or appearance['foreground']).lstrip('&')
detail_key = appearance['detailColor']
cloth_key = packet['original']['foreground'].lstrip('&')
model.update(workflow='regional-curved-v1', base_model=ref(BODY/'model.json')['path'], body_sha256=ref(BODY/'model.json')['sha256'],
    views={}, occlusion_sources={}, representation='Full cloth plus curved body visibility; final authoring compositor restores original body pixels once',
    state='Generation authoring registration; native integration pending', native_acceptance='Pending full-set generation gate',
    outfit_scope='Actual Cloth Robe on Body/0. Bare-arm overlay must respect actual gloves/held-item precedence at final native integration.')
record = {'workflow': 'regional-curved-v1', 'new_imagegen_call': False, 'new_deformation': False,
    'source': ref(BASE/'red-key-v1/dressed-red-output.png'), 'body': ref(BODY/'model.json'),
    'selection': 'User-approved nine-grid front/back cloth with natural curved cuffs; keep accepted profile unchanged',
    'palette': {'body': body_key, 'body_detail': detail_key, 'cloth': cloth_key, 'source': ref(ROOT/'evidence/joppa-anatomy-study.json')}, 'views': {}}
assemblies = {}; cloths = {}; masks = {}; overlays = {}; off = {}; qud = {}
for f in ['south', 'east', 'north']:
    source_cloth = BASE/(f'late-mask-v3/fitted-full-texture-{f}.png' if f == 'east' else f'regional-fit-v1/nine-grid/full-cloth-{f}.png')
    source_mask = BASE/(f'late-mask-v3/body-over-cloth-mask-{f}.png' if f == 'east' else f'curved-mask-v1/body-visibility-{f}.png')
    source_assembly = BASE/(f'late-mask-v3/assembly-{f}.png' if f == 'east' else f'curved-mask-v1/assembly-{f}.png')
    for source, name in [(source_cloth, 'intact-robe'), (source_mask, 'body-visibility'), (source_assembly, 'assembled')]:
        shutil.copyfile(source, HERE/f'{name}-{f}.png')
    body = read(BODY/f'selected-{f}.png'); cloth = read(source_cloth)
    mask = Image.open(source_mask).convert('L')
    assembly = read(source_assembly)
    reconstructed = compose(body, cloth, mask)
    assert np.array_equal(np.array(assembly), np.array(reconstructed)), f
    overlay = body.copy()
    overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:, :, 3].astype(float)*np.array(mask)/255))))
    overlay.save(HERE/f'body-overlay-{f}.png')
    mask_off = Image.alpha_composite(body, cloth); mask_off.save(HERE/f'mask-off-{f}.png')
    colored_body = tinted(body, colors[body_key])
    for part in body_model['views'][f]:
        if part['component'] == 'head-detail':
            detail = tinted(read(ROOT/part['public_file']), colors[detail_key])
            colored_body = Image.alpha_composite(colored_body, detail)
    colored = compose(colored_body, tinted(cloth, colors[cloth_key]), mask)
    colored.save(HERE/f'qud-palette-{f}.png')
    assemblies[f], cloths[f], masks[f], overlays[f], off[f], qud[f] = assembly, cloth, mask.convert('RGBA'), overlay, mask_off, colored
    geometry = dict(body_model['views'][f][0])
    geometry.update(component='item', file=f'dromad-cloth-robe-v6-{f}.png', public_file=ref(HERE/f'intact-robe-{f}.png')['path'],
        sha256=ref(HERE/f'intact-robe-{f}.png')['sha256'], equipment_key='cloth-robe@Body@0', color_role='equipment', layer=.0007)
    over = dict(geometry)
    over.update(component='body-overlay', file=f'dromad-robe-overlay-v6-{f}.png', public_file=ref(HERE/f'body-overlay-{f}.png')['path'],
        sha256=ref(HERE/f'body-overlay-{f}.png')['sha256'], color_role='foreground', layer=.0008)
    model['views'][f] = [geometry, over]
    model['occlusion_sources'][f] = {'body': ref(BODY/f'selected-{f}.png'), 'intact_cloth': ref(HERE/f'intact-robe-{f}.png'), 'mask': ref(HERE/f'body-visibility-{f}.png')}
    record['views'][f] = {'source_cloth': ref(source_cloth), 'source_mask': ref(source_mask), 'approved_assembly': ref(source_assembly),
        'cloth_bytes_preserved': source_cloth.read_bytes() == (HERE/f'intact-robe-{f}.png').read_bytes(),
        'approved_assembly_bytes_preserved': source_assembly.read_bytes() == (HERE/f'assembled-{f}.png').read_bytes()}
for name, images in [('assembled', assemblies), ('intact-robe', cloths), ('body-visibility', masks), ('body-overlay', overlays), ('mask-off', off), ('qud-palette', qud)]:
    mirrored = ImageOps.mirror(images['east']); images['west (mirror)'] = mirrored
    mirrored.save(HERE/f'{name}-west.png')
plate('assembly-comparison.png', assemblies, 'REGISTERED / approved cloth and curved body visibility; side retained')
plate('intact-garment-comparison.png', cloths, 'RETAINED CLOTH / full material, independent of body visibility')
plate('body-mask-comparison.png', masks, 'BODY VISIBILITY / separate fixed-body depth masks')
plate('body-overlay-comparison.png', overlays, 'ORIGINAL BODY / derived exposed-body overlay; independent foreground tint')
plate('mask-off-comparison.png', off, 'MASK OFF / cloth retained behind the original exposed body')
plate('qud-palette-comparison.png', qud, 'QUD PALETTE / actual Tam w/W body/detail and Cloth Robe y')
small = Image.new('RGB', (560, 370), '#142823'); d = ImageDraw.Draw(small)
for i, (f, im) in enumerate(assemblies.items()):
    sprite = im.resize((48, 96), Image.Resampling.LANCZOS)
    small.paste(sprite, (i*140+45, 28), sprite)
    enlarged = sprite.resize((96, 192), Image.Resampling.NEAREST)
    small.paste(enlarged, (i*140+20, 142), enlarged)
    d.text((i*140+10, 344), f.upper(), font=FONT, fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
record['review'] = 'Pending complete authoring plate inspection; user-approved pixels copied without redrawing. Native acceptance remains pending.'
packet.update(workflow='regional-curved-v1', body=ref(BODY/'model.json'), selected_registration=record)
for name, value in [('model.json', model), ('source-packet.json', packet), ('registration-decisions.json', record)]:
    (HERE/name).write_bytes((json.dumps(value, indent=2)+'\n').encode())
print('Registered approved neutral views, full cloth, separate masks, mirrored west, actual Qud tints and intended-size plate.')
