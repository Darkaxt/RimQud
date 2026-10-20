"""Equivalent front/back walkthroughs, using existing artifacts only."""
from pathlib import Path
import json, hashlib, html, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 16)
small = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
original = json.loads((BASE/'pipeline-review-v1/pipeline-sources.json').read_text())
for facing, index in [('south', 0), ('north', 2)]:
    sheet = Image.new('RGB', (1120, 1310), '#142823')
    d = ImageDraw.Draw(sheet)
    d.text((18, 12), f'ACTUAL {facing.upper()} PIPELINE / 01-11 existing; 12 regional-fit proposal', font=font, fill='#e3cf43')
    refs = []
    for i, s in enumerate(original['steps']):
        rel = s['path'].replace('-east.png', '-'+facing+'.png')
        p = ROOT/rel
        im = Image.open(p).convert('RGBA')
        if s['east_crop']:
            im = im.crop((index*512, 0, (index+1)*512, 1024))
        x, y = 12+i%4*278, 48+i//4*414
        d.rectangle((x, y, x+264, y+400), fill='#20382d', outline='#526b5c')
        d.text((x+8, y+8), s['step'], font=font, fill='#e3cf43')
        bg = Image.new('RGBA', (512, 1024), '#20382d')
        bg.alpha_composite(im)
        if i == 11:
            lines = ImageDraw.Draw(bg)
            for yy, label, col in [(480, 'UPPER: ADJUST', '#eb8e74'), (650, 'TRANSITION', '#e3cf43'), (790, 'LOWER: FREEZE', '#70b8b0')]:
                lines.line((65, yy, 435, yy), fill=col, width=3)
                lines.text((65, yy+5), label, font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 21), fill=col)
        sheet.paste(bg.resize((160, 320)).convert('RGB'), (x+52, y+36))
        for j, line in enumerate(textwrap.wrap(s['note'], 33)):
            d.text((x+8, y+358+j*15), line, font=small, fill='#e5e8d8')
        refs.append({'step': s['step'], 'path': rel, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'note': s['note'], 'sheet_column': index if s['east_crop'] else None})
    name = f'pipeline-{facing}.png'
    sheet.save(HERE/name)
    (HERE/f'sources-{facing}.json').write_bytes((json.dumps({'facing': facing, 'steps': refs, 'status': 'Existing pipeline only; new regional fitting compared separately'}, indent=2)+'\n').encode())
    steps = ''.join('<li><strong>'+html.escape(s['step'])+'</strong><p>'+html.escape(s['note'])+' <a href="../'+s['path']+'">Actual source</a></p></li>' for s in refs)
    other = 'north' if facing == 'south' else 'south'
    content = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{facing.title()} clothing pipeline</title><style>body{{background:#142823;color:#e5e8d8;font:18px/1.55 Georgia,serif;margin:0}}main{{max-width:1150px;margin:auto;padding:28px 20px 70px}}a{{color:#e3cf43}}img{{width:100%;height:auto}}li{{margin:16px 0}}aside{{border-left:3px solid #e3cf43;padding-left:18px}}</style><main><p><a href="dromad-clothing-pipeline.html">Profile walkthrough</a> · <a href="dromad-clothing-pipeline-{other}.html">Other facing</a> · <a href="dromad-regional-fitting.html">Regional fitting comparison</a></p><h1>{'Front / south' if facing=='south' else 'Back / north'}: the existing pipeline</h1><p>The equivalent walkthrough uses actual saved intermediates, with the selected original body fixed. It records the pipeline before the new three-band/grid experiments; stage 12 is only its original proposal.</p><aside><p>Cloth-only stages expose the inherited hand notches and incomplete patches. Whole-image stretching, local cuff deformation, cloth reconstruction and final visibility are separate operations; the previous final assembly alone obscured this distinction. This robe remains unfinished.</p></aside><img src="../art/conversion/fit-dromad-cloth-robe/pipeline-review-v2/{name}" alt="Twelve actual pipeline stages for {facing}"><ol>{steps}</ol></main>'''
    (ROOT/f'docs/dromad-clothing-pipeline-{facing}.html').write_bytes(content.encode())
print('Front and back equivalent pipeline reports saved; original profile untouched.')
