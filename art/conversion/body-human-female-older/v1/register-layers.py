"""Register this inspected refined sheet; masks are authored for its actual pixels."""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
source = Image.open(HERE / 'refined-patched-views.png').convert('RGBA')
assert source.size == (1489, 1056)
views = [('south', (0, 0, 512, 1024), (234, 965), [(202, 180), (267, 180), (270, 235), (199, 235)]),
         ('east', (512, 0, 1024, 1024), (744, 962), [(235, 166), (296, 181), (272, 236), (211, 215)]),
         ('north', (1024, 0, 1489, 1024), (1243, 965), [(185, 175), (253, 175), (253, 230), (185, 230)])]
contact = (256, 950)
scale = 1.21 / 941  # One physical pixel scale across all views and components.
model = dict(family='human-female-older', canvas=[512, 1024], pixel_world_scale=scale,
             physical_body_height=1.21, views={}, neutral_palette='Equal RGB grayscale; native foreground tint',
             geometry='Unmutated human: one head, two painted arms/hands and paired bare feet. West mirrors east.',
             age_policy='Authored older-adult variant; no villager demographics or life-stage selection changed.',
             registration=dict(version=1, contact=contact, method='Translate whole figure and ownership masks together; no view-dependent rescale.'),
             state='Generation authoring only; native acceptance deferred until all conversions are generated')
decisions = dict(source='refined-patched-views.png', source_size=source.size, contact=contact, views={})
assembled, ownership = [], []
for facing, region, old_contact, neck in views:
    raw = source.crop(region)
    image = Image.new('RGBA', (512, 1024)); image.paste(raw, (0, 0))
    alpha = image.getchannel('A').point(lambda v:0 if v < 16 else (255 if v >= 240 else v))
    gray = ImageOps.grayscale(image)
    image = Image.merge('RGBA', (gray, gray, gray, alpha))
    image.paste((0, 0, 0, 0), mask=alpha.point(lambda v:255 if v==0 else 0))
    head_mask = Image.new('L', image.size)
    draw = ImageDraw.Draw(head_mask); draw.rectangle((0, 0, 511, 195), fill=255); draw.polygon(neck, fill=255)
    body_mask = ImageChops.invert(head_mask).filter(ImageFilter.MaxFilter(5))
    dx, dy = contact[0] - (old_contact[0] - region[0]), contact[1] - old_contact[1]
    bounds = alpha.getbbox(); translated_bounds = tuple(v+(dx if i%2==0 else dy) for i,v in enumerate(bounds))
    assert 0 <= translated_bounds[0] < translated_bounds[2] <= 512
    assert 0 <= translated_bounds[1] < translated_bounds[3] <= 1024
    rows = []; composite = Image.new('RGBA', image.size); colored = Image.new('RGBA', image.size)
    for component, mask, color, layer in [('body', body_mask, '#739f96', 0), ('head', head_mask, '#d0bd66', .001)]:
        own = image.copy(); own.putalpha(ImageChops.multiply(alpha, mask))
        moved = Image.new('RGBA', image.size); moved.paste(own, (dx, dy))
        moved.paste((0, 0, 0, 0), mask=moved.getchannel('A').point(lambda v:255 if v==0 else 0))
        path = HERE / f'{component}-{facing}.png'; moved.save(path)
        moved_mask = Image.new('L', image.size); moved_mask.paste(mask, (dx, dy)); moved_mask.save(HERE / f'{component}-mask-{facing}.png')
        rows.append(dict(component=component, file=f'human-female-older-v1-{path.name}', public_file=path.relative_to(ROOT).as_posix(),
                         sha256=hashlib.sha256(path.read_bytes()).hexdigest(), size=[512,1024], contact=list(contact), color_role='foreground',
                         width=512*scale*1.5, height=1024*scale, center_x=0, center_z=(950-512)*scale, layer=layer))
        composite = Image.alpha_composite(composite, moved)
        tint = Image.new('RGBA', image.size, color); tint.putalpha(moved.getchannel('A')); colored = Image.alpha_composite(colored, tint)
    model['views'][facing] = rows
    composite.save(HERE / f'selected-{facing}.png'); assembled.append((facing, composite)); ownership.append(colored)
    decisions['views'][facing] = dict(region=region, source_contact=old_contact, translation=[dx,dy], head_mask_top=195, neck_polygon=neck,
                                     body_underlap_pixels=2, registered_bounds=translated_bounds)

font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
plate = Image.new('RGB', (1152, 650), '#142823'); draw = ImageDraw.Draw(plate)
draw.text((18, 12), 'human-female-older / common contact (256, 950)', font=font, fill='#e3cf43')
assembled.append(('west (mirror)', ImageOps.mirror(dict(assembled)['east'])))
for i, (facing, image) in enumerate(assembled):
    tile = Image.new('RGBA', image.size, '#20382d'); tile.alpha_composite(image)
    left, top = i*288+16, 54; plate.paste(tile.convert('RGB').resize((256,512), Image.Resampling.LANCZOS), (left,top))
    x,y=left+128,top+475;draw.line((x,top,x,top+511), fill='#cebc45');draw.line((left,y,left+255,y),fill='#70b8b0')
    draw.ellipse((x-4,y-4,x+4,y+4),outline='#fff6a0',width=2);draw.text((left,578),facing.upper(),font=font,fill='#e3cf43')
draw.text((18,610),'Gold: canvas center/pivot. Teal: ground. Guides are separate from production textures.',font=font,fill='#e5e8d8')
plate.save(HERE/'registration-comparison.png')
mask_plate=Image.new('RGBA',(1536,1024))
for i,image in enumerate(ownership):mask_plate.alpha_composite(image,(i*512,0))
mask_plate.save(HERE/'ownership-comparison.png')
small=Image.new('RGB',(480,340),'#142823');draw=ImageDraw.Draw(small)
for i,(facing,image) in enumerate(assembled):
    thumb=image.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*120+35,15),thumb)
    thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*120+12,125),thumb)
small.save(HERE/'game-scale-review.png')
for filename,data in [('model.json',model),('registration-decisions.json',decisions)]:
    (HERE/filename).write_bytes((json.dumps(data,indent=2)+'\n').encode())
