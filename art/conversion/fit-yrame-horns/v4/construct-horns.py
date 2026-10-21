"""Editable horn-root correction on the unchanged selected Yrame body.

Authoring only. Fit contract is written before drawing; review is recorded by
the operator after inspecting the generated plates, never inferred from alpha.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SIZE = (768, 1152)
FACES = ['south', 'east', 'north']


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def write(p, v):
    p.write_bytes((json.dumps(v, indent=2, ensure_ascii=False) + '\n').encode())


def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())


assert not (HERE / 'fit-contract.json').exists(), 'Do not overwrite an observed attempt'
ledger = read(ROOT / 'evidence/conversion-ledger.json')
assert ledger['active_entry'] == 'FIT-YRAME-HORNS-HEAD-0'
entry = next(e for e in ledger['entries'] if e['id'] == ledger['active_entry'])
previous = read(HERE.parent / 'v3/source-packet.json')
bref = previous['base_body']
assert ref(ROOT / bref['path']) == bref
body = read(ROOT / bref['path'])
now = datetime.now(timezone.utc).isoformat()

# A common curve in a plane diverging from the sagittal plane. Its upper return
# ends above the flesh ears instead of wrapping around them. Coordinates describe
# the east projection; front/back use the same u/v samples at common scale.
segments = [
    [[510, 143], [507, 106], [474, 59], [434, 73]],
    [[434, 73], [385, 87], [387, 148], [416, 167]],
    [[416, 167], [438, 183], [468, 170], [468, 149]],
    [[468, 149], [468, 132], [451, 124], [441, 133]],
    [[441, 133], [432, 142], [440, 152], [449, 147]],
]
roots = dict(south=dict(left=[344, 125], right=[424, 125]),
             east=dict(near=[510, 143], far=[510, 143]),
             north=dict(left=[344, 141], right=[424, 141]))
descriptions = dict(
    south=dict(attachment='Broad paired upper anterolateral crown roots at x344/424, y125, each approximately30px wide; root interiors sit on the skull above the ears, not alongside it.',
               direction='Bone initially leaves upward/outward, sweeps backward into a returning curl above the flesh ear; the same local curve is foreshortened in this view.',
               visibility='Both root transitions and upper curls visible. Horns above the head surface; original ears remain flesh below and are not included in the bone.',
               depth='Original body/head then near paired horns.'),
    east=dict(attachment='Same upper anterolateral crown surface, root510,143, approximately30px across; anterior to and above the original ear near474,211.',
              direction='Broad root rises from the crown, curves upward/backward toward screen-left, then returns above the ear. Full profile reveals the loop; the root is not on the occipital contour.',
              visibility='Near curl visible, far curl naturally hidden by the corresponding near curl/head in exact profile. Flesh ear remains independently visible below the curl.',
              depth='Far horn then original body/head then near horn; far and near project to the same profile silhouette.'),
    north=dict(attachment='Rear projection of the same paired upper anterolateral crown roots at344/424,141, approximately30px wide. Anterior root interiors are occluded by the original skull.',
               direction='Same physical curls seen from behind, symmetric around the skull. Their returning tips remain above rather than around the ear lobes.',
               visibility='Posterior outer curls and tips visible above/lateral to the head where not occluded. Preserve all original ears in front of the bone; no ear contour becomes a horn.',
               depth='Whole paired horns then original body/head, including original ears.'),
    west=dict(attachment='Mirror the east attachment for the symmetric paired natural Head288/0 item; do not shift the root to make both horns visible.',
              direction='Mirror the exact east projection, retaining skull-relative growth and return direction.',
              visibility='Mirrored near/far occlusion and flesh-ear separation; west acceptance depends on the east review.',
              depth='Mirror east anatomy only; item slot/laterality stays unchanged.')
)
contract = dict(entry=entry['id'], recorded_at=now, status='PLANNED — visual comparison pending',
                body=bref, item_source=previous['native_source'], frame=previous['frame'],
                native_facts='Horns575, paired grooved bone natural equipment on Head288/0. Native data does not specify skull coordinates.',
                authored_estimates='Ram-like curl, size, anterolateral crown root surface, root breadth and yaw are authored interpretation. Selected bare body/head is fixed.',
                root_coordinates=roots, root_width=30.7, shared_segments=segments,
                front_projection_factor=.38, views=descriptions,
                root_rendering='Continuous filled ribbon with no flat cap outline at the skull junction. Entire hidden bone remains in its independent item layer.',
                review_gate='Inspect manual and first refined drawings against each facing before extraction; point containment is diagnostic only.')
write(HERE / 'fit-contract.json', contract)
packet = dict(previous)
packet.update(recorded_at=now, previous_rejected_attempt=ref(HERE.parent / 'v3/per-view-fit-review.json'),
              fit_contract=ref(HERE / 'fit-contract.json'),
              correction='Replace flat external caps and ear-wrapping coils with continuous broad crown roots and an upper returning curl; keep selected body unchanged.')
write(HERE / 'source-packet.json', packet)

samples = []
for segment in segments:
    p = np.array(segment, float)
    for t in np.linspace(0, 1, 32, endpoint=False):
        samples.append((1-t)**3*p[0] + 3*(1-t)**2*t*p[1] + 3*(1-t)*t*t*p[2] + t**3*p[3])
samples.append(np.array(segments[-1][-1], float))
samples = np.array(samples) - [510, 143]
fraction = np.linspace(0, 1, len(samples))
width = 30*(1-fraction)**.7 + .7


def project(facing, side):
    u, v = samples.T
    if facing == 'east':
        return np.stack([510+u, 143+v], 1)
    root = roots[facing]['right' if side == 1 else 'left']
    return np.stack([root[0] - side*u*.38, root[1]+v], 1)


def ribbon(p, w):
    tangent = np.gradient(p, axis=0)
    n = np.stack([-tangent[:, 1], tangent[:, 0]], 1)
    n /= np.linalg.norm(n, axis=1)[:, None]
    a, b = p+n*w[:, None]/2, p-n*w[:, None]/2
    return np.vstack([a, b[::-1]]), n


def path(p, close=True):
    return 'M' + ' L'.join(f'{x:.3f} {y:.3f}' for x, y in p) + (' Z' if close else '')


def make_svg(facing):
    shapes = []
    for i, side in enumerate([1] if facing == 'east' else [-1, 1]):
        p = project(facing, side)
        polygon, n = ribbon(p, width)
        outline = path(polygon)
        # No stroke across the base: it joins the crown rather than presenting a
        # detached flat-ended tube. The outer sides remain continuous to the tip.
        shapes.append(f'<clipPath id="h{i}"><path d="{outline}"/></clipPath><path d="{outline}" fill="url(#bone)"/><path d="{path(polygon,False)}" fill="none" stroke="#242424" stroke-width="4.5" stroke-linejoin="round"/>')
        high = path(ribbon(p+n*width[:, None]*.15, width*.23)[0])
        shapes.append(f'<g clip-path="url(#h{i})"><path d="{high}" fill="#e0e0e0"/>')
        arc = np.r_[0, np.cumsum(np.linalg.norm(np.diff(p, axis=0), axis=1))]
        for target in np.arange(14, arc[-1]-12, 17):
            j = np.argmin(abs(arc-target))
            a, b = p[j]+n[j]*width[j]*.40, p[j]-n[j]*width[j]*.40
            mid = p[j] + (p[min(j+2, len(p)-1)]-p[max(j-2, 0)])*.23
            shapes.append(f'<path d="M{a[0]:.2f} {a[1]:.2f} Q{mid[0]:.2f} {mid[1]:.2f} {b[0]:.2f} {b[1]:.2f}" fill="none" stroke="#999999" stroke-width="1.8"/>')
        shapes.append('</g>')
    return '<svg xmlns="http://www.w3.org/2000/svg" width="768" height="1152" viewBox="0 0 768 1152"><defs><linearGradient id="bone" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#aaaaaa"/><stop offset=".5" stop-color="#cfcfcf"/><stop offset="1" stop-color="#a8a8a8"/></linearGradient></defs>' + ''.join(shapes) + '</svg>'


for facing in FACES:
    svg = make_svg(facing)
    (HERE / f'horns-{facing}.svg').write_bytes(svg.encode())
    horn = Image.open(io.BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA')
    horn.save(HERE / f'horns-{facing}.png')
    base = Image.new('RGBA', SIZE)
    for r in sorted(body['views'][facing], key=lambda r:r['layer']):
        base.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    red = np.array(base)
    lum = red[:, :, :3].mean(2)
    red[:, :, 0] = np.uint8(np.maximum(lum, 48))
    red[:, :, 1] = np.uint8(lum*.065)
    red[:, :, 2] = np.uint8(lum*.065)
    red[red[:, :, 3] == 0, :3] = 0
    for name, background in [('constructed-assembly', base), ('red-context', Image.fromarray(red))]:
        image = Image.new('RGBA', SIZE)
        if facing == 'north':
            image.alpha_composite(horn)
        image.alpha_composite(background)
        if facing != 'north':
            image.alpha_composite(horn)
        image.save(HERE / f'{name}-{facing}.png')

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
boxes = dict(south=[184, 0, 584, 400], east=[307, 18, 707, 418], north=[184, 16, 584, 416])
for prefix, output in [('red-context', 'manual-context-turnaround'), ('constructed-assembly', 'manual-neutral-turnaround')]:
    sheet = Image.new('RGBA', (1200, 450))
    draw = ImageDraw.Draw(sheet)
    for i, (facing, box) in enumerate(boxes.items()):
        sheet.alpha_composite(Image.open(HERE/f'{prefix}-{facing}.png').crop(box), (i*400, 0))
        draw.text((i*400+15, 420), facing.upper(), font=font, fill='white')
    sheet.save(HERE / (output+'.png'))
write(HERE/'context-crops.json', dict(source_canvas=list(SIZE), sheet=[1200,450], view_boxes=boxes, policy='Crop-only matched display, no per-view scale changes.'))

# Review-only landmarks, with the complete root width rather than a lone point.
guide = Image.new('RGB', (1200, 450), '#142823')
draw = ImageDraw.Draw(guide)
for i, (facing, box) in enumerate(boxes.items()):
    r = next(r for r in body['views'][facing] if r['component']=='head')
    head = Image.open(ROOT/r['public_file']).convert('RGBA').crop(box)
    guide.paste(head, (i*400, 0), head)
    for key, (x,y) in roots[facing].items():
        if key == 'far':
            continue
        x, y = x-box[0]+i*400, y-box[1]
        draw.ellipse((x-16,y-12,x+16,y+12), outline='#e3cf43', width=2)
        draw.line((x,y-16,x,y-42), fill='#e3cf43', width=2)
    draw.text((i*400+15, 340), facing.upper()+' / proposed crown region', font=font, fill='#e3cf43')
    draw.text((i*400+15, 365), 'Gold = authored root extent', font=font, fill='#e5e8d8')
    draw.text((i*400+15, 390), 'Original head/ears unchanged', font=font, fill='#e5e8d8')
guide.save(HERE/'root-surface-guide.png')

plate = Image.new('RGB', (1200, 700), '#142823')
draw = ImageDraw.Draw(plate)
draw.text((20,15), 'QUD HORNS575 / original item + actual Core ram rendering references', font=font, fill='#e3cf43')
glyph = Image.open('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/horns-reference.png').convert('RGBA').resize((96,144),Image.Resampling.NEAREST)
plate.paste(glyph,(30,75),glyph)
for i, facing in enumerate(FACES):
    r = next(r for r in previous['references']['core_ram'] if r['name'].endswith(facing))
    im = Image.open(r['path']).convert('RGBA')
    im.thumbnail((220,180))
    plate.paste(im,(220+i*290,65),im)
    draw.text((220+i*290,255),facing.upper(),font=font,fill='#e3cf43')
draw.text((20,300),'References supply curl/material cues; selected human head is not replaced by a sheep head.',font=font,fill='#e5e8d8')
small = guide.resize((960,360),Image.Resampling.LANCZOS)
plate.paste(small,(120,325))
plate.save(HERE/'source-reference-construction.png')

outputs = [HERE/n for n in ['fit-contract.json','source-packet.json','construct-horns.py','root-surface-guide.png','manual-context-turnaround.png','manual-neutral-turnaround.png','source-reference-construction.png','context-crops.json']]
entry['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',phase='Corrected crown-root construction — review pending',
    action='Define each facing first, then reconstruct one shared returning curl with broad crown roots and a separate original flesh ear.',
    inputs=[bref,ref(HERE.parent/'v3/per-view-fit-review.json')],outputs=[ref(p) for p in outputs],
    review='Fit contract predates construction. Manual visual comparison pending; point containment is not acceptance.',result='REQUIRES REVIEW'))
entry['current_step']='construct_and_overlay_one_item'
ledger['updated_at']=now
write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Created per-view contract, corrected editable construction and contextual review plates; visual comparison pending.')
