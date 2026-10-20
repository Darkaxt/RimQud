"""Render assembly evidence from saved previews without rerunning the constructor."""
from pathlib import Path
from html import escape
import json
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
FACES = ['south', 'east', 'north', 'west']
BG = '#142823'
GOLD = '#e3cf43'

out = Image.new('RGB', (800, 650), BG)
d = ImageDraw.Draw(out)
d.text((18, 15), 'ARGYVE / neutral then native / 48x96 and nearest enlarged 72x144', font=FONT, fill=GOLD)
for j, label in enumerate(['full-neutral', 'full-native']):
    y = 50 + j * 290
    d.text((18, y), label.upper(), font=FONT, fill=GOLD)
    for i, facing in enumerate(FACES):
        image = Image.open(HERE / f'{label}-{facing}.png').convert('RGBA')
        small = image.resize((48, 96), Image.Resampling.LANCZOS)
        large = small.resize((72, 144), Image.Resampling.NEAREST)
        out.paste(small, (i * 200 + 20, y + 35), small)
        out.paste(large, (i * 200 + 95, y + 35), large)
        d.text((i * 200 + 20, y + 200), facing.upper(), font=FONT, fill=GOLD)
d.text((18, 625), 'Authoring preview; stationary held-item poses. Native acceptance pending.', font=FONT, fill='#e5e8d8')
out.save(HERE / 'game-scale-review.png')

out = Image.new('RGB', (1152, 680), BG)
d = ImageDraw.Draw(out)
d.text((18, 15), 'ARGYVE / unchanged shared frame512x1024; pivot256 / ground950', font=FONT, fill=GOLD)
for i, facing in enumerate(FACES):
    x, y = 16 + i * 284, 55
    image = Image.open(HERE / f'full-native-{facing}.png').convert('RGBA').resize((256, 512), Image.Resampling.LANCZOS)
    out.paste(image, (x, y), image)
    d.line((x + 128, y, x + 128, y + 512), fill='#a39846')
    d.line((x, y + 475, x + 256, y + 475), fill='#75aaa0')
    d.text((x, 585), facing.upper(), font=FONT, fill=GOLD)
d.text((18, 625), 'Guides are report-only. Body, item pixels, physical size and attachment coordinates unchanged.', font=FONT, fill='#e5e8d8')
out.save(HERE / 'registration-comparison.png')

lineage = json.loads((HERE / 'dependency-lineage.json').read_text())
parts = ['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>Argyve: reused conversion evidence</title><style>body{background:#142823;color:#e5e8d8;font:18px/1.6 Georgia,serif;max-width:1100px;margin:35px auto;padding:0 20px}a{color:#e3cf43}section{border-top:1px solid #526b5c;padding:20px 0}li{margin:10px 0}code{overflow-wrap:anywhere}</style>',
         '<h1>Argyve: the body and five item conversions</h1><p>These are the actual earlier generation steps reused by this assembly. No new body, costume or ImageGen call was made for Argyve. Each linked entry retains its original shape, metadata, actual RimWorld reference, manual construction, refinement, secondary and patched views, extraction and fitting where applicable.</p>',
         '<p><a href="../../../../docs/conversion-entries/NPC-ARGYVE.html">Argyve assembly record</a> · <a href="source-packet.json">Captured identity and five equipped items</a></p>']
for dep in lineage['dependencies']:
    ident = dep['entry']
    parts.append(f'<section><h2>{escape(ident)}</h2><p><a href="../../../../{escape(dep["report"])}">Full conversion report with images and exact methods</a> · <a href="../../../../{escape(dep["model"]["path"])}">Exact reused model</a></p><ol>')
    for event in dep['reused_generation_evidence']:
        links = ' · '.join(f'<a href="../../../../{escape(r["path"])}">{escape(Path(r["path"]).name)}</a>' for r in event.get('outputs', []))
        parts.append(f'<li><strong>{escape(event["step"].replace("_", " "))}</strong> — {escape(event["result"])}<br>{escape(event["action"])}<br>{links}</li>')
    parts.append('</ol></section>')
parts.append('<p>Generation authoring only. Visibility, equipping, hurt, look, save/load and source-supported weapon state acceptance wait for the complete generation set.</p></html>')
(HERE / 'dependency-evidence.html').write_bytes(('\n'.join(parts) + '\n').encode())
print('Rendered readable dependency history, fixed-size scale plate and shared-frame guides; original crowded scale plate retained as rejected report history.')
