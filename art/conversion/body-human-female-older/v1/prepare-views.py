"""Recorded neutralization and shared-frame placement for this proposal only."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
source = Image.open(HERE / 'secondary-views.png').convert('RGBA')
scale = 0.97  # One common scale for all three views; preserve relative proportions.
views = [('south', (120, 0, 570, 1024), (333, 991)),
         ('east', (600, 0, 930, 1024), (744, 984)),
         ('north', (970, 0, 1420, 1024), (1197, 984))]
sheet = Image.new('RGBA', (1536, 1088))
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 20)
decisions = {'source': 'secondary-views.png', 'common_scale': scale, 'contact': [256, 950], 'views': {}}
for index, (facing, region, contact) in enumerate(views):
    image = source.crop(region)
    alpha = image.getchannel('A').point(lambda v: 0 if v < 16 else (255 if v >= 240 else v))
    gray = ImageOps.grayscale(image)
    image = Image.merge('RGBA', (gray, gray, gray, alpha))
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    image.paste((0, 0, 0, 0), mask=image.getchannel('A').point(lambda v:255 if v==0 else 0))
    anchor = (round((contact[0] - region[0]) * scale), round(contact[1] * scale))
    translation = (256 - anchor[0], 950 - anchor[1])
    canvas = Image.new('RGBA', (512, 1024)); canvas.paste(image, translation)
    canvas.save(HERE / f'patched-{facing}.png')
    sheet.alpha_composite(canvas, (index * 512, 0))
    draw.text((index * 512 + 130, 1040), {'south':'FRONT / SOUTH', 'east':'RIGHT SIDE / EAST', 'north':'BACK / NORTH'}[facing], font=font, fill='#b9b9b9')
    decisions['views'][facing] = {'region': region, 'source_contact': contact, 'translation': translation, 'registered_bounds': canvas.getchannel('A').getbbox()}
sheet.save(HERE / 'patched-views.png')
(HERE / 'patch-decisions.json').write_bytes((json.dumps(decisions, indent=2) + '\n').encode())
