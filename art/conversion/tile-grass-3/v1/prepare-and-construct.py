"""Reconstruct the third grass paint from its native blade coverage and context."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reference=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Basic Grass 3')
donor=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='grass.png')
assert sha(DONOR/reference['reference_file'])==reference['reference_sha256']
assert sha(DONOR/'grass.png')==donor['png_sha256']
mask=Image.open(DONOR/'village-originals/basic-grass-3-mask.png').convert('RGBA')
visible=[dict(x=x,y=y,rgba=mask.getpixel((x,y))) for y in range(24) for x in range(16) if mask.getpixel((x,y))[3]]
packet=dict(entry='TILE-GRASS-3',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='Terrain/sw_grass3.bmp, native paint glyph; no independent creature/furniture blueprint or anatomy',
 description='No standalone Description.Short for a cell paint. Reference extraction labels it Basic Grass 3; do not invent a crop, reed, flower or tall grass species.',
 original=reference,visible_native_coverage=visible,
 mask_contract='All twelve opaque native pixels are black: primary foreground coverage in the audited Kobold mask contract. There is no source detail-color region.',
 donor_reference=dict(**donor,role='Actual RimWorld GrassA supplies blade taper and plant/shading convention only. Its dense many-blade tuft is not the shape to copy.'),
 authored_interpretation='Two sparse shoots inferred from twelve native coverage pixels: a longer leftward-curving blade rooted low, and a shorter rightward-curving blade whose tip and root both sit higher. Preserve the sparse relative tips/root placement; fine blade width/shading is authored.',
 palette='Neutral equal-RGB production source with native primary tint at binding time. Green g/G previews use exact captured palette values; the reference packet did not export a universal runtime paint color. No universal native paint color is established by the reference packet; preview hues do not assign a species or biome.',
 source_usage_limit='Tile identity alone does not identify a universal plant color or biological species. Preserve per-cell native visibility and color; do not hardcode a green crop object.',
 frame=dict(canvas=[512,768],native_cell=[16,24],source_scale=32,nominal_anchor=[256,512],native_anchor=[8,16],
            policy='Sparse floor paint stays in its original rectangular cell frame. Do not independently crop/center alpha or give it a humanoid foot pivot.'),
 states='One fixed map view. Native grass variants 1 and 2 are separate ledger entries; no invented rotation, growth, flowering or wind animation here.',
 native_acceptance='Deferred until every required conversion is generated')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g stroke="#656c63" stroke-width=".15" stroke-linejoin="round"><path d="M6.08 16.0 Q5.8 13.4 4.9 11.7 Q3.8 9.9 2.94 8.93 Q5.08 10.28 5.9 12.34 Q6.75 14.1 6.93 16.0Z" fill="#c8ccc3"/><path d="M8.95 13.1 Q9.0 11.25 10.1 9.8 Q11.0 8.7 12.95 7.88 Q11.68 9.38 10.88 11.22 Q9.9 12.5 9.86 13.1Z" fill="#d2d6cc"/></g><path d="M6.5 15.7 Q5.8 12.0 4.0 10.2 M9.4 12.8 Q9.5 10.6 11.9 8.9" fill="none" stroke="#edf0e8" stroke-width=".1"/></svg>'''
(HERE/'constructed-grass.svg').write_bytes(svg.encode())
(HERE/'constructed-grass.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-grass.svg'),skip_system_fonts=True))
plate=Image.new('RGB',(1280,630),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((24,18),'BASIC GRASS 3 / native paint > sparse shoot geometry > blade shading reference',font=font,fill='#e3cf43')
original=Image.open(DONOR/reference['reference_file']).convert('RGBA').resize((256,384),Image.Resampling.NEAREST);plate.paste(original,(40,90),original)
constructed=Image.open(HERE/'constructed-grass.png').convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);plate.paste(constructed,(405,90),constructed)
ref=Image.open(DONOR/'grass.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);plate.paste(ref,(850,155),ref)
for xy,text in [((24,490),'Original 16 x 24 paint frame'),((385,490),'Editable sparse two-shoot suggestion'),((835,490),'Actual RimWorld GrassA'),((835,525),'Blade convention, not a dense bush')]:d.text(xy,text,font=font,fill='#e5e8d8')
for i,text in enumerate(['No named species/crop or unsupported animation inferred.',
                         'Neutral RGB + source primary tint. Native paint color/visibility stays cell-owned.']):d.text((24,555+i*28),text,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
