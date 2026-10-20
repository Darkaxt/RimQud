"""Reconstruct the second grass paint from its native blade coverage and context."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reference=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Basic Grass 2')
donor=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='grass.png')
assert sha(DONOR/reference['reference_file'])==reference['reference_sha256']
assert sha(DONOR/'grass.png')==donor['png_sha256']
mask=Image.open(DONOR/'village-originals/basic-grass-2-mask.png').convert('RGBA')
visible=[dict(x=x,y=y,rgba=mask.getpixel((x,y))) for y in range(24) for x in range(16) if mask.getpixel((x,y))[3]]
packet=dict(entry='TILE-GRASS-2',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='Terrain/sw_grass2.bmp, native paint glyph; no independent creature/furniture blueprint or anatomy',
 description='No standalone Description.Short for a cell paint. Reference extraction labels it Basic Grass 2; do not invent a crop, reed, flower or tall grass species.',
 original=reference,visible_native_coverage=visible,
 mask_contract='All sixteen opaque native pixels are black: primary foreground coverage in the audited Kobold mask contract. There is no source detail-color region.',
 donor_reference=dict(**donor,role='Actual RimWorld GrassA supplies blade taper and plant/shading convention only. Its dense many-blade tuft is not the shape to copy.'),
 authored_interpretation='Three sparse shoots inferred from sixteen native coverage pixels: a long leftward blade, a taller middle/right-curving blade and a short rightward blade, with their distinct root heights. Preserve the sparse relative tips/root placement; fine blade width/shading is authored.',
 palette='Neutral equal-RGB production source with native primary tint at binding time. Green g/G previews use exact captured palette values; the reference packet did not export a universal runtime paint color. The same tile is used by orange ClamGrass elsewhere; that does not make Joppa paint a clam species or authorize adding its particle prefab.',
 source_usage_limit='Tile identity alone does not identify a universal plant color or biological species. Preserve per-cell native visibility and color; do not hardcode a green crop object.',
 frame=dict(canvas=[512,768],native_cell=[16,24],source_scale=32,nominal_anchor=[256,512],native_anchor=[8,16],
            policy='Sparse floor paint stays in its original rectangular cell frame. Do not independently crop/center alpha or give it a humanoid foot pivot.'),
 states='One fixed map view. Native grass variants 1 and 3 are separate ledger entries; no invented rotation, growth, flowering or wind animation here.',
 native_acceptance='Deferred until every required conversion is generated')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g stroke="#656c63" stroke-width=".15" stroke-linejoin="round"><path d="M5.08 15.02 Q4.7 12.9 3.8 11.4 Q2.65 9.8 1.95 8.92 Q4.09 10.1 4.91 11.96 Q5.66 13.35 5.89 15.02Z" fill="#c8ccc3"/><path d="M8.0 14.1 Q7.8 11.96 9.1 10.13 Q10.0 8.7 11.95 7.86 Q10.8 9.6 10.0 11.5 Q8.9 13.2 8.92 14.1Z" fill="#d2d6cc"/><path d="M9.9 16.05 Q10.0 14.3 11.3 13.1 Q12.1 12.5 12.98 11.91 Q12.05 13.8 11.36 14.9 Q11.13 15.7 10.9 16.05Z" fill="#bfc6bb"/></g><path d="M5.5 14.7 Q4.9 11.8 3.1 10.2 M8.5 13.8 Q8.5 11.3 10.8 9.0 M10.5 15.7 Q10.6 14.2 12.2 12.7" fill="none" stroke="#edf0e8" stroke-width=".1"/></svg>'''
(HERE/'constructed-grass.svg').write_bytes(svg.encode())
(HERE/'constructed-grass.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-grass.svg'),skip_system_fonts=True))
plate=Image.new('RGB',(1280,630),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((24,18),'BASIC GRASS 2 / native paint > sparse shoot geometry > blade shading reference',font=font,fill='#e3cf43')
original=Image.open(DONOR/reference['reference_file']).convert('RGBA').resize((256,384),Image.Resampling.NEAREST);plate.paste(original,(40,90),original)
constructed=Image.open(HERE/'constructed-grass.png').convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);plate.paste(constructed,(405,90),constructed)
ref=Image.open(DONOR/'grass.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);plate.paste(ref,(850,155),ref)
for xy,text in [((24,490),'Original 16 x 24 paint frame'),((385,490),'Editable sparse three-shoot suggestion'),((835,490),'Actual RimWorld GrassA'),((835,525),'Blade convention, not a dense bush')]:d.text(xy,text,font=font,fill='#e5e8d8')
for i,text in enumerate(['No named species/crop or unsupported animation inferred.',
                         'Neutral RGB + source primary tint. Native paint color/visibility stays cell-owned.']):d.text((24,555+i*28),text,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
