"""Author this fixed-body tunic as intact cloth plus editable limb-depth masks.

No game binding, generated anatomy, cloth RGB repair, or cloth-alpha cutouts.
Run once per recorded version; corrections belong in a new sibling version.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps
import resvg_py

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'v1' / 'registered'
BODY = ROOT / 'art/conversion/body-dromad/v1'
assert not (HERE / 'model.json').exists(), 'Preserve recorded versions'

def asset(p, role=None):
    d = {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
    if role:
        d['role'] = role
    return d

def save_json(name, data):
    (HERE / name).write_bytes((json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode())

def painted_mask(facing, path):
    # SVG alpha is paint coverage. Save an ordinary white-on-black grayscale mask.
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'
           '<path fill="white" d="' + path + '"/></svg>')
    p = HERE / f'body-over-clothing-{facing}.svg'
    p.write_bytes(svg.encode())
    coverage = Image.open(__import__('io').BytesIO(resvg_py.svg_to_bytes(svg_path=str(p), skip_system_fonts=True))).getchannel('A')
    coverage.save(HERE / f'body-over-clothing-{facing}.png')
    return coverage

def tinted(im, rgb):
    gray = ImageOps.grayscale(im)
    channels = [gray.point(lambda v, c=c: round(v*c/255)) for c in rgb]
    return Image.merge('RGBA', (*channels, im.getchannel('A')))

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
def plate(name, images, title, guides=False):
    out = Image.new('RGB', (1152, 660), '#142823')
    d = ImageDraw.Draw(out)
    d.text((18, 14), title, font=font, fill='#e3cf43')
    for i, (facing, im) in enumerate(images.items()):
        bg = Image.new('RGBA', im.size, '#20382d')
        bg.alpha_composite(im)
        x = 16 + i * 288
        out.paste(bg.convert('RGB').resize((256, 512)), (x, 54))
        if guides:
            d.line((x+128, 54, x+128, 565), fill='#cebc45')
            d.line((x, 529, x+255, 529), fill='#70b8b0')
        d.text((x, 584), facing.upper(), font=font, fill='#e3cf43')
    d.text((18, 620), 'Authoring only. Same body, intact cloth and contact; native acceptance waits for the full set.', font=font, fill='#e5e8d8')
    out.save(HERE / name)

body_model = json.loads((BODY / 'model.json').read_text())
model = json.loads((OLD / 'model.json').read_text())
model['views'] = {}
model['representation'] = 'Intact garment plus per-facing painted body-over-clothing mask; original-body overlay is a derived export'
model['layer_order'] = 'body 0 -> intact robe .0007 -> masked original body .0008 -> head .001 -> head detail .0011; held Shillelagh remains separate above arm' 
model['mask_semantics'] = 'white selects original body above garment; black none; gray antialias; overlay alpha = body alpha * mask'
model['native_acceptance'] = 'Deferred until all conversions generated; generic-layer binding and outfit precedence not tested'
model['occlusion_sources'] = {}
model['outfit_scope'] = 'This authored template wears only this tunic. Do not bind its exposed-hand overlay above gloves/other hand gear; resolve actual outfit precedence at final native integration.'
record = {
    'timestamp': datetime.now(timezone.utc).isoformat(),
    'body': asset(BODY / 'model.json'),
    'cloth_identity': 'Cloth Robe: goat wool with shale freckles; actual equipped Body part 357, laterality 0 on Tam',
    'sources': [],
    'new_imagegen_call': False,
    'refinement_provenance': 'Reuse the actually logged v1 contextual refinement and isolated garment; this version changes composition representation only.',
    'ownership': 'Paint original exposed forearms/hands above intact rear cuff surfaces. Cover shoulders with cloth. No source body or cloth pixels/alpha changed.',
    'native_acceptance': 'Pending all-generated gate',
    'views': {},
}
assembled, off, overlays, masks, garments, colors = {}, {}, {}, {}, {}, {}
front = 'M88 674 L148 712 L172 725 L164 749 L160 758 C175 770 170 794 153 806 C131 819 102 808 94 789 Q87 776 102 758 L96 720Z M424 674 L364 712 L340 725 L348 749 L352 758 C337 770 342 794 359 806 C381 819 410 808 418 789 Q425 776 410 758 L416 720Z'
side = 'M196 693 Q225 681 250 684 Q273 685 291 696 L288 715 L282 745 L280 755 Q295 769 291 787 Q288 804 273 812 Q247 824 225 808 Q212 798 216 777 L219 766 Q206 751 201 730 Q194 710 196 693Z'
for facing in ['south', 'east', 'north']:
    source = OLD / f'registered-uncut-{facing}.png'
    target = HERE / f'intact-robe-{facing}.png'
    shutil.copyfile(source, target)
    cloth = Image.open(target).convert('RGBA')
    body = Image.open(BODY / f'body-{facing}.png').convert('RGBA')
    selected = Image.open(BODY / f'selected-{facing}.png').convert('RGBA')
    coverage = painted_mask(facing, side if facing == 'east' else front)
    overlay = body.copy()
    overlay.putalpha(ImageChops.multiply(body.getchannel('A'), coverage))
    overlay.save(HERE / f'body-overlay-{facing}.png')
    mask_off = Image.alpha_composite(selected, cloth)
    composed = Image.alpha_composite(mask_off, overlay)
    head = Image.open(BODY / f'head-{facing}.png').convert('RGBA')
    composed = Image.alpha_composite(composed, head)
    mask_off = Image.alpha_composite(mask_off, head)
    composed.save(HERE / f'assembled-{facing}.png')
    mask_off.save(HERE / f'mask-off-{facing}.png')
    # Deliberately distinct body/cloth tints demonstrate ownership, not actor colors.
    color = Image.alpha_composite(tinted(selected, (119,191,207)), tinted(cloth, (177,201,195)))
    color = Image.alpha_composite(color, tinted(overlay, (119,191,207)))
    color = Image.alpha_composite(color, tinted(head, (119,191,207)))
    color.save(HERE / f'independent-tint-{facing}.png')
    assembled[facing], off[facing], overlays[facing], garments[facing], colors[facing] = composed, mask_off, overlay, cloth, color
    masks[facing] = Image.merge('RGBA', (coverage, coverage, coverage, Image.new('L', coverage.size, 255)))
    row = dict(body_model['views'][facing][0])
    row.update(component='item', file=f'dromad-cloth-robe-v2-{facing}.png', public_file=target.relative_to(ROOT).as_posix(), sha256=asset(target)['sha256'], color_role='equipment', equipment_key='cloth-robe@Body@0', layer=.0007)
    over = dict(row)
    over.update(component='body-overlay', file=f'dromad-robe-body-overlay-v2-{facing}.png', public_file=(HERE/f'body-overlay-{facing}.png').relative_to(ROOT).as_posix(), sha256=asset(HERE/f'body-overlay-{facing}.png')['sha256'], color_role='foreground', layer=.0008)
    model['views'][facing] = [row, over]
    model['occlusion_sources'][facing] = {'body': asset(BODY / f'body-{facing}.png'), 'intact_cloth': asset(target), 'editable_mask': asset(HERE / f'body-over-clothing-{facing}.svg'), 'mask': asset(HERE / f'body-over-clothing-{facing}.png')}
    record['sources'].append(asset(source))
    record['views'][facing] = {'cloth_byte_identical': source.read_bytes() == target.read_bytes(), **model['occlusion_sources'][facing], 'derived_overlay': asset(HERE/f'body-overlay-{facing}.png')}

for images in [assembled, off, overlays, masks, garments, colors]:
    images['west (mirror)'] = ImageOps.mirror(images['east'])
plate('assembly-comparison.png', assembled, 'MASK ON / original exposed arms over intact robe', True)
plate('intact-garment-comparison.png', garments, 'CANONICAL CLOTH / byte-identical refined v1; no limb-shaped alpha cutouts')
plate('painted-mask-comparison.png', masks, 'PAINTED MASK / white draws original body above this garment')
plate('body-overlay-comparison.png', overlays, 'DERIVED BODY OVERLAY / original body pixels, clipped by original body alpha')
plate('mask-off-comparison.png', off, 'MASK OFF / intact sleeve interior crosses the exposed arm')
plate('independent-tint-comparison.png', colors, 'COLOR OWNERSHIP / illustrative Qud C body; actual item y cloth (not actor assignment)')

comparison = Image.new('RGB', (1020, 700), '#142823')
d = ImageDraw.Draw(comparison)
for x, im, label in [(20, off['east'], 'MASK OFF / intact cuff'), (520, assembled['east'], 'MASK ON / original arm above')]:
    crop = im.crop((195,485,345,705)).resize((420,616), Image.Resampling.NEAREST)
    comparison.paste(crop, (x,50), crop)
    d.text((x,15),label,font=font,fill='#e3cf43')
comparison.save(HERE / 'cuff-mask-off-on-comparison.png')
small = Image.new('RGB', (480,340), '#142823')
for i, im in enumerate(assembled.values()):
    t = im.resize((48,96),Image.Resampling.LANCZOS)
    small.paste(t,(i*120+35,15),t)
    t = t.resize((96,192),Image.Resampling.NEAREST)
    small.paste(t,(i*120+12,125),t)
small.save(HERE / 'game-scale-review.png')
save_json('model.json',model)
save_json('composition-decisions.json',record)
packet = json.loads((OLD.parent/'source-packet.json').read_text())
packet['representation_update'] = record
save_json('source-packet.json',packet)
print(json.dumps({'output': str(HERE), 'new_imagegen_call': False, 'body_changed': False, 'cloth_changed': False}))
