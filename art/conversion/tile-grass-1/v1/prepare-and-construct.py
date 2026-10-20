"""Reconstruct the first grass paint from its native blade coverage and context."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reference=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Basic Grass 1')
donor=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='grass.png')
assert sha(DONOR/reference['reference_file'])==reference['reference_sha256']
assert sha(DONOR/'grass.png')==donor['png_sha256']
mask=Image.open(DONOR/'village-originals/basic-grass-1-mask.png').convert('RGBA')
visible=[dict(x=x,y=y,rgba=mask.getpixel((x,y))) for y in range(24) for x in range(16) if mask.getpixel((x,y))[3]]
packet=dict(entry='TILE-GRASS-1',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='Terrain/sw_grass1.bmp, native paint glyph; no independent creature/furniture blueprint or anatomy',
 description='No standalone Description.Short for a cell paint. Reference extraction labels it Basic Grass 1; do not invent a crop, reed, flower or tall grass species.',
 original=reference,visible_native_coverage=visible,
 mask_contract='All ten opaque native pixels are black: primary foreground coverage in the audited Kobold mask contract. There is no source detail-color region.',
 donor_reference=dict(**donor,role='Actual RimWorld GrassA supplies blade taper and plant/shading convention only. Its dense many-blade tuft is not the shape to copy.'),
 authored_interpretation='Two sparse shoots inferred from ten native coverage pixels: one short leftward blade and one longer upward/right blade. Preserve the sparse relative tips/root placement; fine blade width/shading is authored.',
 palette='Neutral equal-RGB production source with native primary tint at binding time. Green g/G previews use exact captured palette values; the reference packet did not export a universal runtime paint color. The same tile can appear in cyan PrimalGrass elsewhere.',
 source_usage_limit='Tile identity alone does not identify a universal plant color or biological species. Preserve per-cell native visibility and color; do not hardcode a green crop object.',
 frame=dict(canvas=[512,768],native_cell=[16,24],source_scale=32,nominal_anchor=[256,512],native_anchor=[8,16],
            policy='Sparse floor paint stays in its original rectangular cell frame. Do not independently crop/center alpha or give it a humanoid foot pivot.'),
 states='One fixed map view. Native grass variants 2 and 3 are separate ledger entries; no invented rotation, growth, flowering or wind animation here.',
 native_acceptance='Deferred until every required conversion is generated')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g stroke="#555e55" stroke-width=".14" stroke-linejoin="round"><path d="M8.17 15.99 Q7.87 13.85 8.99 11.45 Q10.0 9.84 11.93 8.83 Q10.42 10.68 9.73 12.01 Q8.94 14.16 8.91 16.0Z" fill="#c4c9c0"/><path d="M6.21 14.1 Q6.31 12.43 4.95 10.91 Q6.92 11.75 7.02 13.91Z" fill="#a7b1a4"/></g><path d="M8.5 15.6 Q8.4 12.6 10.8 10.0 M6.6 13.7 Q6.7 12.8 5.8 11.8" fill="none" stroke="#e0e4d9" stroke-width=".08"/></svg>'''
(HERE/'constructed-grass.svg').write_bytes(svg.encode())
(HERE/'constructed-grass.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-grass.svg'),skip_system_fonts=True))
plate=Image.new('RGB',(1280,630),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((24,18),'BASIC GRASS 1 / native paint > sparse shoot geometry > blade shading reference',font=font,fill='#e3cf43')
original=Image.open(DONOR/reference['reference_file']).convert('RGBA').resize((256,384),Image.Resampling.NEAREST);plate.paste(original,(40,90),original)
constructed=Image.open(HERE/'constructed-grass.png').convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);plate.paste(constructed,(405,90),constructed)
ref=Image.open(DONOR/'grass.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);plate.paste(ref,(850,155),ref)
for xy,text in [((24,490),'Original 16 x 24 paint frame'),((385,490),'Editable sparse two-shoot suggestion'),((835,490),'Actual RimWorld GrassA'),((835,525),'Blade convention, not a dense bush')]:d.text(xy,text,font=font,fill='#e5e8d8')
for i,text in enumerate(['No named species/crop or unsupported animation inferred.',
                         'Neutral RGB + source primary tint. Native paint color/visibility stays cell-owned.']):d.text((24,555+i*28),text,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
