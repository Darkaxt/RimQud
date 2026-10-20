"""Bounded adult-dromad robe experiment: continuous source, 3 bands, then 9 cells.

Body visibility is a final composition operation. No old cutoff alpha or earlier
isolated drawing is used as cloth. New concealed material is explicitly authored.
"""
from pathlib import Path
import argparse, hashlib, json, shutil
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
KEY = BASE/'red-key-v1'
BODY = ROOT/'art/conversion/body-dromad/v2'
MASK = BASE/'mask-fit-v4'
VIEWS = [('south', 0), ('north', 2)]
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)


def asset(p):
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(p):
    return Image.open(p).convert('RGBA')


def save_json(p, data):
    assert not p.exists(), 'Preserve recorded experiment: '+str(p)
    p.write_bytes((json.dumps(data, indent=2)+'\n').encode())


def components(mask):
    labels, _ = ndimage.label(mask)
    found = []
    for label, sl in enumerate(ndimage.find_objects(labels), 1):
        if sl is not None and np.count_nonzero(labels[sl] == label) > 200:
            found.append([sl[1].start, sl[0].start, sl[1].stop, sl[0].stop])
    return sorted(found, key=lambda box: box[0])


def harmonic(gray, known, envelope):
    unknown = envelope & ~known
    yy, xx = np.where(unknown)
    n = len(yy)
    if not n:
        return gray, unknown
    ids = np.full(gray.shape, -1, np.int32)
    ids[yy, xx] = np.arange(n)
    deg = np.zeros(n); rhs = np.zeros(n); rr = []; cc = []
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = yy+dy, xx+dx
        valid = (ny >= 0) & (ny < 1024) & (nx >= 0) & (nx < 512)
        q = np.flatnonzero(valid)
        q = q[envelope[ny[q], nx[q]]]
        deg[q] += 1
        neighbor = ids[ny[q], nx[q]]
        pending = neighbor >= 0
        rr.extend(q[pending].tolist()); cc.extend(neighbor[pending].tolist())
        rhs[q[~pending]] += gray[ny[q[~pending]], nx[q[~pending]]]
    matrix = sparse.coo_matrix((-np.ones(len(rr)), (rr, cc)), shape=(n, n)).tocsr()+sparse.diags(deg)
    gray[yy, xx] = spsolve(matrix, rhs)
    return gray, unknown


def prepare():
    assert not (HERE/'source-packet.json').exists()
    raw = read(KEY/'dressed-red-output.png')
    key = np.array(Image.open(KEY/'keyed-body-mask.png').convert('L'))
    affine = json.loads((BASE/'affine-fit-v1/result.json').read_text())
    packet = {'source': asset(KEY/'dressed-red-output.png'), 'body': asset(BODY/'model.json'),
              'method': 'Neutral cloth from one raw dressed generation; bridge exterior hand occlusion notches with straight side-edge segments between visible cloth rows, then harmonic same-source continuation before any fitting. The bridges are authored unseen cloth, not recovered detail.',
              'cutoff_alpha_used': False, 'old_isolated_drawing_used': False, 'views': {}}
    for facing, index in VIEWS:
        cell = np.array(raw.crop((index*512, 0, (index+1)*512, 1024)))
        rgb = cell[:, :, :3].astype(float)
        known = (rgb.max(axis=2)-rgb.min(axis=2) < 5) & (cell[:, :, 3] > 128)
        envelope = ndimage.binary_fill_holes(known)
        arms = [b for b in components(key[:, index*512:(index+1)*512] > 128) if 550 < b[1] < 800 and b[3] < 850]
        assert len(arms) == 2, (facing, arms)
        bridges = []
        for arm in arms:
            y0, y1 = arm[1]-8, arm[3]+8
            left = (arm[0]+arm[2])/2 < 256
            end_x = []
            for y in (y0, y1):
                occupied = np.flatnonzero(envelope[y])
                end_x.append(int(occupied[0] if left else occupied[-1]))
            for y in range(y0, y1+1):
                edge = int(round(np.interp(y, [y0, y1], end_x)))
                if left:
                    envelope[y, edge:256] = True
                else:
                    envelope[y, 256:edge+1] = True
            bridges.append({'side': 'left' if left else 'right', 'endpoint_rows': [y0, y1], 'endpoint_x': end_x})
        envelope = ndimage.binary_fill_holes(envelope)
        gray, continued = harmonic(rgb.mean(axis=2), known, envelope)
        alpha = np.where(envelope, 255, 0).astype('uint8')
        neutral = np.uint8(np.clip(gray, 0, 255))
        cloth = Image.fromarray(np.dstack([neutral, neutral, neutral, alpha]))
        cloth.save(HERE/f'full-source-{facing}.png')
        Image.fromarray(np.uint8(continued)*255).save(HERE/f'continued-source-{facing}.png')
        arm_paint = np.array(Image.open(BASE/'v5'/f'body-over-clothing-{facing}.png').convert('L'))
        body_alpha = np.array(read(BODY/f'body-{facing}.png'))[:, :, 3]
        target_arms = components((arm_paint > 128) & (body_alpha > 128))
        assert len(target_arms) == 2
        packet['views'][facing] = {'raw_column': index, 'full_source': asset(HERE/f'full-source-{facing}.png'),
            'continued_source': asset(HERE/f'continued-source-{facing}.png'), 'authored_bridges': bridges,
            'continued_pixels': int(continued.sum()), 'source_arm_bounds': arms, 'target_arm_bounds': target_arms,
            'whole_image_affine': affine['views'][facing]['red-cut'],
            'source_body': asset(BODY/f'selected-{facing}.png'), 'visibility_mask': asset(MASK/f'robe-expose-{facing}.png')}
    shutil.copyfile(BASE/'late-mask-v3/assembly-east.png', HERE/'accepted-profile-unchanged.png')
    packet['accepted_profile'] = asset(HERE/'accepted-profile-unchanged.png')
    save_json(HERE/'source-packet.json', packet)
    print('Prepared same-source cloth before fitting; authored hidden-material bridges recorded.')


def sample(source, mx, my):
    """One premultiplied sampling pass avoids dark RGB from transparent pixels."""
    rgba = np.array(source).astype(float)/255
    a = ndimage.map_coordinates(rgba[:, :, 3], [my, mx], order=1, mode='constant', cval=0)
    rgb = np.stack([ndimage.map_coordinates(rgba[:, :, c]*rgba[:, :, 3], [my, mx], order=1, mode='constant', cval=0) for c in range(3)], axis=-1)
    rgb = np.divide(rgb, a[:, :, None], out=np.zeros_like(rgb), where=a[:, :, None] > 0)
    return Image.fromarray(np.uint8(np.clip(np.dstack([rgb, a])*255, 0, 255)+.5))


def compose(body, cloth, mask):
    off = Image.alpha_composite(body, cloth)
    actual = np.array(body)[:, :, 3] > 0
    coverage = Image.fromarray(np.uint8(np.array(mask)*actual))
    return Image.composite(body, off, coverage), off


def transform(mode):
    packet = json.loads((HERE/'source-packet.json').read_text())
    dest = HERE/mode
    dest.mkdir(exist_ok=False)
    report = {'mode': mode, 'source_packet': asset(HERE/'source-packet.json'), 'body_unchanged': True,
              'mask_application': 'Only after complete fitting; retained cloth is never body-cut', 'views': {}}
    for facing, _ in VIEWS:
        info = packet['views'][facing]
        source = read(HERE/f'full-source-{facing}.png')
        body = read(BODY/f'selected-{facing}.png')
        mask = Image.open(MASK/f'robe-expose-{facing}.png').convert('L')
        p = info['whole_image_affine']; sx, sy = p['scale_x'], p['scale_y']; tx, ty = p['translation']
        gy, gx = np.mgrid[0:1024, 0:512].astype(float)
        base_x, base_y = (gx-tx)/sx, (gy-ty)/sy
        baseline = sample(source, base_x, base_y)
        sa, ta = info['source_arm_bounds'], info['target_arm_bounds']
        bounds = source.getbbox()
        rows = np.array([bounds[1], np.mean([a[1] for a in sa]), max(a[3] for a in sa)+28, bounds[3]], float)
        target_rows = rows*sy+ty
        target_rows[1] = np.mean([a[1] for a in ta])
        source_columns = np.array([0, 512], float) if mode == 'three-band' else np.array([0, sa[0][2], sa[1][0], 512], float)
        grid = np.tile(source_columns*sx+tx, (4, 1))
        if mode == 'three-band':
            sc = [(a[0]+a[2])/2 for a in sa]; tc = [(a[0]+a[2])/2 for a in ta]
            upper_scale = (tc[1]-tc[0])/(sc[1]-sc[0])
            upper_tx = np.mean(tc)-upper_scale*np.mean(sc)
            grid[1] = source_columns*upper_scale+upper_tx
        else:
            left_scale = (ta[0][2]-ta[0][0])/(sa[0][2]-sa[0][0])
            right_scale = (ta[1][2]-ta[1][0])/(sa[1][2]-sa[1][0])
            grid[1] = [ta[0][0]-left_scale*sa[0][0], ta[0][2], ta[1][0], ta[1][2]+right_scale*(512-sa[1][2])]
        assert np.all(np.diff(rows) > 0) and np.all(np.diff(target_rows) > 0)
        assert np.all(np.diff(grid, axis=1) > 0), 'No folded cells permitted'
        my = base_y.copy(); mx = base_x.copy()
        for y in range(1024):
            if target_rows[0] <= y < target_rows[2]:
                my[y] = np.interp(y, target_rows, rows)
                columns = np.array([np.interp(y, target_rows, grid[:, c]) for c in range(len(source_columns))])
                mx[y] = np.interp(gx[y], columns, source_columns)
        fitted = sample(source, mx, my)
        freeze_from = int(np.ceil(target_rows[2]))
        # The fixed region is exactly the same-source baseline, not another drawing.
        pixels = np.array(fitted); original = np.array(baseline)
        pixels[freeze_from:] = original[freeze_from:]
        fitted = Image.fromarray(pixels)
        final, off = compose(body, fitted, mask)
        baseline_final, _ = compose(body, baseline, mask)
        for name, image in [('full-cloth', fitted), ('mask-off', off), ('assembly', final), ('whole-image-baseline', baseline), ('whole-image-assembly', baseline_final)]:
            image.save(dest/f'{name}-{facing}.png')
        guides = off.copy(); draw = ImageDraw.Draw(guides)
        for r, y in enumerate(target_rows):
            draw.line((grid[r, 0], y, grid[r, -1], y), fill='#e3cf43', width=2)
        for c in range(len(source_columns)):
            draw.line([(grid[r, c], target_rows[r]) for r in range(4)], fill='#70b8b0', width=2)
        guides.save(dest/f'controls-{facing}.png')
        ba, fa, mask_a = np.array(body), np.array(final), np.array(mask)
        exposed = (mask_a == 255) & (ba[:, :, 3] > 0)
        controls = {'source_rows': rows.tolist(), 'target_rows': target_rows.tolist(), 'source_columns': source_columns.tolist(), 'target_grid_x': grid.tolist(), 'freeze_from_destination_y': freeze_from,
                    'one_resampling_pass': True, 'shared_boundaries': True,
                    'source': asset(HERE/f'full-source-{facing}.png')}
        save_json(dest/f'controls-{facing}.json', controls)
        report['views'][facing] = {'controls': asset(dest/f'controls-{facing}.json'), 'full_cloth': asset(dest/f'full-cloth-{facing}.png'), 'assembly': asset(dest/f'assembly-{facing}.png'),
            'lower_region_changed_pixels': int(np.count_nonzero(np.any(pixels[freeze_from:] != original[freeze_from:], axis=2))),
            'selected_body_rgba_changed_pixels': int(np.count_nonzero(exposed & np.any(ba != fa, axis=2))),
            'minimum_cell_horizontal_scale': float(np.min(np.diff(grid, axis=1)/np.diff(source_columns))),
            'minimum_band_vertical_scale': float(np.min(np.diff(target_rows)/np.diff(rows)))}
    shutil.copyfile(HERE/'accepted-profile-unchanged.png', dest/'assembly-east.png')
    report['profile_unchanged'] = asset(dest/'assembly-east.png')['sha256'] == packet['accepted_profile']['sha256']
    save_json(dest/'result.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['prepare', 'three-band', 'nine-grid'])
    args = parser.parse_args()
    prepare() if args.mode == 'prepare' else transform(args.mode)
