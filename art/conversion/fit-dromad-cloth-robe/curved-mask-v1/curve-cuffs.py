"""Hold nine-grid cloth fixed; fit smooth body-visibility cuff curves.

The cuff is a quadratic Bezier cross-section following the garment's dark
opening. No garment pixels or original body pixels are redrawn or blurred.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
REGIONAL = BASE/'regional-fit-v1'
assert not (HERE/'result.json').exists(), 'Preserve recorded art'
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)


def asset(p):
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(p):
    return Image.open(p).convert('RGBA')


def background(im):
    bg = Image.new('RGBA', im.size, '#20382d')
    bg.alpha_composite(im)
    return bg.convert('RGB')


def compose(body, cloth, mask):
    mask = np.array(mask)
    coverage = Image.fromarray(np.uint8(mask*(np.array(body)[:, :, 3] > 0)))
    return Image.composite(body, Image.alpha_composite(body, cloth), coverage)


packet = json.loads((REGIONAL/'source-packet.json').read_text())
result = {'scope': 'Smooth natural cuff body masks, front/back only; nine-grid cloth fixed',
          'method': 'Sample dark cuff-opening entry near the existing cuff; fit a quadratic Bezier boundary, rasterize at 4x resolution and replace only the upper-arm visibility band. Body alpha clips the overlay. Hands and all regions below the cuff band retain their previous mask.',
          'views': {}, 'native_validation': 'Not performed'}
for facing in ['south', 'north']:
    body_path = ROOT/f'art/conversion/body-dromad/v2/selected-{facing}.png'
    cloth_path = REGIONAL/f'nine-grid/full-cloth-{facing}.png'
    body = read(body_path); cloth = read(cloth_path)
    rgba = np.array(cloth); luminance = rgba[:, :, :3].mean(axis=2)
    old_path = BASE/f'mask-fit-v4/robe-expose-{facing}.png'
    old = np.array(Image.open(old_path).convert('L'))
    new = old.copy(); curves = []; paths = []
    for side, box in zip(['left', 'right'], packet['views'][facing]['target_arm_bounds']):
        # Keep samples away from the sleeve's outside outline and torso seam.
        xa, xb = (box[0]+16, box[2]-6) if side == 'left' else (box[0]+6, box[2]-16)
        samples = []
        old_tops = []
        for x in np.linspace(xa, xb, 13).astype(int):
            ys = np.flatnonzero(old[640:750, x] > 128)
            if not len(ys):
                continue
            top = int(ys[0])+640; old_tops.append(top)
            y0, y1 = max(660, top-22), min(750, top+14)
            dark = np.flatnonzero((luminance[y0:y1, x] < 80) & (rgba[y0:y1, x, 3] > 128))
            if len(dark):
                samples.append([int(x), int(dark[0])+y0])
        assert len(samples) >= 6, (facing, side, samples)
        samples = np.array(samples, float)
        x0, x2 = float(box[0]-4), float(box[2]+4)
        t = (samples[:, 0]-x0)/(x2-x0)
        coeff = np.polynomial.polynomial.polyfit(t, samples[:, 1], 2)
        # Polynomial-to-Bezier conversion: explicit editable geometric controls.
        y0 = coeff[0]; y1 = coeff[0]+coeff[1]/2; y2 = coeff.sum()
        controls = [[x0, float(y0)], [(x0+x2)/2, float(y1)], [x2, float(y2)]]
        ts = np.linspace(0, 1, 257)
        curve = (1-ts[:, None])**2*np.array(controls[0])+2*(1-ts[:, None])*ts[:, None]*np.array(controls[1])+ts[:, None]**2*np.array(controls[2])
        join_y = min(748, int(max(old_tops)+18))
        # A broad authoring region is clipped by the original body at display.
        # Retain the old inner-arm limit to avoid exposing adjacent torso cloth.
        left_limit = int(box[0]-8) if side == 'left' else int(box[0])
        right_limit = int(box[2]) if side == 'left' else int(box[2]+8)
        high = Image.new('L', (512*4, 1024*4))
        draw = ImageDraw.Draw(high)
        polygon = curve.tolist()+[[x2, join_y+1], [x0, join_y+1]]
        draw.polygon([(round(x*4), round(y*4)) for x, y in polygon], fill=255)
        gate = np.array(high.resize((512, 1024), Image.Resampling.LANCZOS))
        lower_y = max(640, int(np.floor(curve[:, 1].min()))-2)
        # Replace the angular top, not a blurred copy of the existing mask.
        new[lower_y:join_y, left_limit:right_limit] = gate[lower_y:join_y, left_limit:right_limit]
        paths.append('M '+str(controls[0][0])+' '+str(controls[0][1])+' Q '+str(controls[1][0])+' '+str(controls[1][1])+' '+str(controls[2][0])+' '+str(controls[2][1]))
        curves.append({'side': side, 'dark_cuff_samples': samples.tolist(), 'quadratic_bezier': controls,
                       'rasterization_scale': 4, 'unchanged_below_y': join_y,
                       'edited_x_limits': [left_limit, right_limit]})
    visibility = Image.fromarray(new)
    visibility.save(HERE/f'body-visibility-{facing}.png')
    final = compose(body, cloth, visibility)
    final.save(HERE/f'assembly-{facing}.png')
    overlay = body.copy()
    overlay.putalpha(Image.fromarray(np.uint8(np.array(body)[:, :, 3].astype(float)*new/255)))
    overlay.save(HERE/f'body-overlay-{facing}.png')
    paint = np.array(body).copy()
    shade = paint[:, :, :3].mean(axis=2)/255
    red = np.stack([64+191*shade, 20*shade, 16*shade], axis=2)
    blue = np.stack([20*shade, 100+120*shade, 100+155*shade], axis=2)
    color = np.where((new > 128)[:, :, None], red, blue)
    paint[:, :, :3] = np.uint8(color)
    Image.fromarray(paint).save(HERE/f'painted-body-{facing}.png')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024">'+''.join('<path d="'+p+'" fill="none" stroke="#e3cf43" stroke-width="2"/>' for p in paths)+'</svg>'
    (HERE/f'cuff-curves-{facing}.svg').write_bytes(svg.encode())
    out = Image.new('RGB', (1152, 660), '#142823'); d = ImageDraw.Draw(out)
    d.text((18, 12), facing.upper()+' / identical nine-grid cloth; body-mask geometry only changes', font=FONT, fill='#e3cf43')
    for i, (label, im) in enumerate([
        ('POLYGON MASK', read(REGIONAL/f'nine-grid/assembly-{facing}.png')),
        ('CURVED CUFF MASK', final),
        ('PAINTED BODY', Image.fromarray(paint)),
        ('NEW VISIBILITY', visibility.convert('RGBA'))]):
        x = 16+i*284; out.paste(background(im).resize((256, 512)), (x, 48)); d.text((x, 578), label, font=FONT, fill='#e3cf43')
    d.text((18, 620), 'Red exposed body; cyan covered body. Curve follows sleeve opening; no texture or body redraw.', font=FONT, fill='#e5e8d8')
    out.save(HERE/f'comparison-{facing}.png')
    close = Image.new('RGB', (1440, 480), '#142823'); d = ImageDraw.Draw(close)
    d.text((18, 12), 'SAME CLOTH / natural curved cuff boundary versus inherited polygon', font=FONT, fill='#e3cf43')
    for i, (label, im) in enumerate([('OLD MASK', read(REGIONAL/f'nine-grid/assembly-{facing}.png')), ('CURVED BODY MASK', final)]):
        close.paste(background(im).crop((70, 620, 440, 825)).resize((666, 369)), (18+i*720, 75))
        d.text((18+i*720, 48), label, font=FONT, fill='#e3cf43')
    close.save(HERE/f'cuffs-{facing}.png')
    ba, fa = np.array(body), np.array(final)
    original_final = np.array(read(REGIONAL/f'nine-grid/assembly-{facing}.png'))
    unchanged_below = max(c['unchanged_below_y'] for c in curves)
    result['views'][facing] = {'body': asset(body_path), 'cloth': asset(cloth_path), 'old_mask': asset(old_path),
        'new_mask': asset(HERE/f'body-visibility-{facing}.png'), 'curves': curves,
        'body_pixels_changed_in_fully_selected_region': int(np.count_nonzero((new == 255) & (ba[:, :, 3] > 0) & np.any(ba != fa, axis=2))),
        'lower_composition_changed_pixels': int(np.count_nonzero(np.any(fa[unchanged_below:] != original_final[unchanged_below:], axis=2)))}
result['visual_review'] = 'Pending actual image inspection; not generation-ready.'
(HERE/'result.json').write_bytes((json.dumps(result, indent=2)+'\n').encode())
print(json.dumps(result['views'], indent=2))
