"""Translate only front/back staff grips inward; preserve source scale/profile."""
from pathlib import Path
import copy, hashlib, json
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PREV = HERE.parent / 'v1/registered'
BODY = ROOT / 'art/conversion/body-dromad/v2'
ROBE = ROOT / 'art/conversion/fit-dromad-cloth-robe/v6'
SIZE = (512, 1024)
FACES = ('south', 'east', 'north')

def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def write(p, value):
    p.write_bytes((json.dumps(value, indent=2) + '\n').encode())

def opened(p):
    return Image.open(p).convert('RGBA')

def plate(rows, title, filename, guides=True):
    out = Image.new('RGB', (288 * len(rows), 650), '#142823')
    d = ImageDraw.Draw(out)
    font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
    d.text((18, 12), title, font=font, fill='#e3cf43')
    for i, (label, im) in enumerate(rows):
        bg = Image.new('RGBA', SIZE, '#20382d')
        bg.alpha_composite(im)
        x, y = i * 288 + 16, 54
        out.paste(bg.convert('RGB').resize((256, 512), Image.Resampling.LANCZOS), (x, y))
        if guides:
            d.line((x + 128, y, x + 128, y + 511), fill='#cebc45')
            d.line((x, y + 475, x + 255, y + 475), fill='#70b8b0')
        d.text((x, 578), label.upper(), font=font, fill='#e3cf43')
    d.text((18, 610), 'Original body/robe; full staff retained; native acceptance pending.', font=font, fill='#e5e8d8')
    out.save(HERE / filename)

old_model = json.loads((PREV / 'model.json').read_text())
model = copy.deepcopy(old_model)
model.update(base_model=(BODY / 'model.json').relative_to(ROOT).as_posix(),
             body_sha256=ref(BODY / 'model.json')['sha256'],
             context_robe=(ROBE / 'model.json').relative_to(ROOT).as_posix(),
             axial_texture='../v1/registered/canonical-item.png; unchanged source and scale',
             policy='Actual Tam Hand 362/laterality 2; front/back grip moved inward without rotating or resizing item. Accepted profile retained.',
             native_acceptance='Pending full-set generation gate')
old_place = json.loads((HERE.parent / 'v1/placement-suggestion.json').read_text())
controls = dict(south=dict(dx=35, grip=[140, 777]), east=dict(dx=0, grip=[270, 777]), north=dict(dx=-34, grip=[374, 777]))
decisions = dict(source=ref(PREV / 'canonical-item.png'), body=ref(BODY / 'model.json'),
                 robe=ref(ROBE / 'model.json'), scale=1, rotation_change=0,
                 contact=[256, 950], new_imagegen_call=False, views={})
assemblies = {}; tinted = {}; items = {}; palms = {}
for facing in FACES:
    c = controls[facing]
    source = opened(PREV / f'unoccluded-{facing}.png')
    held = Image.new('RGBA', SIZE)
    held.paste(source, (c['dx'], 0))  # integer translation; no resampling
    held.save(HERE / f'intact-item-{facing}.png')
    pawn = opened(ROBE / f'assembled-{facing}.png')
    original_body = opened(BODY / f'selected-{facing}.png')
    mask = Image.open(PREV / f'hand-coverage-{facing}.png').convert('L')
    hand = original_body.copy()
    hand.putalpha(ImageChops.multiply(original_body.getchannel('A'), mask))
    hand.save(HERE / f'hand-overlay-{facing}.png')
    mask.save(HERE / f'hand-coverage-{facing}.png')
    if facing == 'east':
        # Preserve the previously accepted item pixels and original profile row.
        item = opened(PREV / 'item-east.png')
        combined = Image.alpha_composite(pawn, item)
        model['views'][facing] = copy.deepcopy(old_model['views'][facing])
        depth = 'Accepted profile item/attachment unchanged; existing hand coverage retained.'
    else:
        item = held
        row = copy.deepcopy(old_model['views'][facing][0])
        row.update(file=f'dromad-shillelagh-v2-{facing}.png', public_file=ref(HERE / f'intact-item-{facing}.png')['path'],
                   sha256=ref(HERE / f'intact-item-{facing}.png')['sha256'])
        model['views'][facing] = [row]
        if facing == 'south':
            combined = Image.alpha_composite(Image.alpha_composite(pawn, item), hand)
            overlay = copy.deepcopy(row)
            overlay.update(component='body-overlay', file=f'dromad-staff-hand-v2-{facing}.png',
                           public_file=ref(HERE / f'hand-overlay-{facing}.png')['path'],
                           sha256=ref(HERE / f'hand-overlay-{facing}.png')['sha256'], color_role='foreground', layer=.0019)
            model['views'][facing].append(overlay)
            depth = 'Full item above robe, original palm above grip; item alpha never cut around hand.'
        else:
            combined = Image.alpha_composite(item, pawn)
            depth = 'Full item behind original body/robe, including original gripping hand.'
    items[facing] = held
    assemblies[facing] = combined
    palms[facing] = hand
    combined.save(HERE / f'assembled-{facing}.png')
    # Native y/y equipment tint, kept independent from body and robe.
    gray = ImageOps.grayscale(item)
    color = ImageOps.colorize(gray, (0, 0, 0), (177, 201, 195)).convert('RGBA')
    color.putalpha(item.getchannel('A'))
    tinted[facing] = Image.alpha_composite(color, pawn) if facing == 'north' else Image.alpha_composite(pawn, color)
    if facing == 'south':
        tinted[facing] = Image.alpha_composite(tinted[facing], hand)
    decisions['views'][facing] = dict(previous_grip=old_place[facing]['grip'], grip=c['grip'],
        hand=old_place[facing]['hand'], translation=[c['dx'], 0], angle=old_place[facing]['angle'],
        depth=depth, full_item=ref(HERE / f'intact-item-{facing}.png'), original_hand=ref(HERE / f'hand-overlay-{facing}.png'))

assemblies['west (mirror)'] = ImageOps.mirror(assemblies['east'])
tinted['west (mirror)'] = ImageOps.mirror(tinted['east'])
plate(list(assemblies.items()), 'DROMAD / SHILLELAGH / inner-palm front/back grip', 'assembly-comparison.png')
plate(list(items.items()), 'FULL ITEM / translation only, no new isolation or hand-shaped cuts', 'intact-item-comparison.png')
plate(list(tinted.items()), 'SHILLELAGH / independent native y/y equipment tint', 'palette-comparison.png')
plate([('south before', opened(PREV / 'assembled-south.png')), ('south current', assemblies['south']),
       ('north before', opened(PREV / 'assembled-north.png')), ('north current', assemblies['north'])],
      'FRONT / BACK / old composition and corrected grip on current robe', 'before-after-comparison.png')
small = Image.new('RGB', (480, 340), '#142823')
for i, (_, im) in enumerate(assemblies.items()):
    thumb = im.resize((48, 96), Image.Resampling.LANCZOS)
    small.paste(thumb, (i * 120 + 35, 15), thumb)
    thumb = thumb.resize((96, 192), Image.Resampling.NEAREST)
    small.paste(thumb, (i * 120 + 12, 125), thumb)
small.save(HERE / 'game-scale-review.png')
write(HERE / 'model.json', model)
write(HERE / 'registration-decisions.json', decisions)
print('Front +35px, back -34px; scale and profile item/attachment unchanged; original hand foreground.')
