"""Source-bound connected swimming-water material, independent of simulation."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,random,math,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/PhysicalPhenomena.xml')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
reference=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x.get('blueprint')=='Pond')
assert sha(DONOR/reference['reference_file'])==reference['reference_sha256']
assert sha(DONOR/'village-originals/pond-mask.png')==reference['native_mask_sha256']
donor=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='water-deep.png');assert sha(DONOR/donor['file'])==donor['png_sha256']
tree=ET.parse(NATIVE).getroot();names=['Water','Pond','SaltyWaterDeepPool','SaltyWaterExtraDeepPool']
definitions={n:ET.tostring(tree.find(f".//object[@Name='{n}']"),encoding='unicode') for n in names}
threshold_path=Path('E:/Temp/qud-transplant-probe-joppa-20261019/joppa-liquid-thresholds.json')
capture_path=ROOT/'docs/images/village-original.png';capture=Image.open(capture_path).convert('RGB');region=[930,136,1004,244]
colors=Counter(capture.crop(region).get_flattened_data());native_counts={k:colors[tuple(bytes.fromhex(palette[k]))] for k in ['b','B','c','C','k']}
packet=dict(entry='TILE-WATER-DEEP',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='Swimming-depth state of an actual visible open water-bearing LiquidVolume; not a new creature or a fixed volume inferred from the sprite',
 native_description='A pool of liquid.',original=reference,
 native_definitions=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=definitions),
 depth_evidence=dict(path=str(threshold_path),sha256=sha(threshold_path),observations=json.loads(threshold_path.read_text()),
  meaning='Historical native diagnostic: wading begins at200 and swimming at2000 drams in that tested state. Runtime predicates remain authoritative; do not reproduce threshold rules from this art file.'),
 liquid_identity='Pond declares water-600,salt-400 and500 drams. Deep pool declares4000,extra deep8000. Captured shallow Joppa pools do not prove a naturally occurring swimming-depth cell. Deep is a required authored supported state, not a new spawned pool.',
 native_capture=dict(**asset(capture_path),sample_rect=region,exact_palette_counts=native_counts,
  limit='Historical original Joppa pool patch, not a new capture or deep-water observation. Dynamic connected liquid display differs from the small default puddle sprite.'),
 donor_reference=dict(**donor,role='Actual WaterDeepRamp supplies restrained smooth tonal variation and connected-material presentation only. Its muted donor gray/blue, UV interpretation and water-depth simulation are not transplanted by this art conversion.'),
 source_palette=dict(base_role='b',base_hex=palette['b'],ripple_role='B',ripple_hex=palette['B'],
  interpretation='Native Water default foreground is b and the captured pool uses b/B. Separate b/B color roles preserve the source blue family; deeper subdued reflectance is authored, not a native physics statement.'),
 construction='Neutral smooth open-water plane with sparse flowing curved ripples, no repeated per-cell rim, pebbles, caustic bottom, foam border or opaque donor color. Deep texture should read darker/calmer than the later shallow state.',
 states='One world-continuous material, wet/dry shore coverage and independent deep/shallow blend coverage using native state ownership. Reuse compatible eight-neighbor geometry with water/depth semantics, not path rules.',
 frame='Flat top-down surface, no creature turnarounds, anatomy or equipment. Material is world-anchored, never independently cropped per water cell.',
 bindings='Actual open-volume visibility and water proportion select eligibility; other liquids, concealed/unsupported states retain native graphics. Depth uses IsSwimmingDepth/IsWadingDepth; no volume mutation or generic liquid-color inference.',
 adapter_evidence=dict(renderer=asset(ROOT/'art/conversion/tile-grassy-ground/v1/adapter-source/JoppaRenderer.cs'),capture=asset(ROOT/'art/conversion/tile-grassy-ground/v1/adapter-source/JoppaSimulation.cs'),
  note='Existing adapter has world-continuous water UV and native depth capture, but uses fixed tints/material selection and a four-cardinal perimeter. New neutral color roles, diagonal coverage and separate depth blending remain final integration work.'),
 native_acceptance='Deferred until every conversion is generation-ready')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
rng=random.Random(20519);defs=[];shapes=['<rect width="512" height="512" fill="#151515"/>']
for i in range(14):
 x,y=rng.uniform(0,512),rng.uniform(0,512);rx,ry=rng.uniform(70,150),rng.uniform(30,100)
 defs.append(f'<radialGradient id="m{i}"><stop stop-color="#666666" stop-opacity=".25"/><stop offset="1" stop-color="#666666" stop-opacity="0"/></radialGradient>')
 for dx in [-512,0,512]:
  for dy in [-512,0,512]:shapes.append(f'<ellipse cx="{x+dx:.1f}" cy="{y+dy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#m{i})"/>')
for i in range(33):
 x,y=rng.uniform(0,512),rng.uniform(0,512);length=rng.uniform(12,50);bend=rng.uniform(3,12);tone=rng.randint(80,165)
 for dx in [-512,0,512]:
  for dy in [-512,0,512]:
   shapes.append(f'<path d="M{x+dx:.1f} {y+dy:.1f} q{length*.5:.1f} {-bend:.1f} {length:.1f} 0" stroke="rgb({tone},{tone},{tone})" stroke-width="{rng.uniform(.7,1.5):.2f}" stroke-opacity=".6" stroke-linecap="round" fill="none"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><defs>'+''.join(defs)+'</defs>'+''.join(shapes)+'</svg>'
(HERE/'constructed-ripple-mask.svg').write_bytes(svg.encode());(HERE/'constructed-ripple-mask.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-ripple-mask.svg'),skip_system_fonts=True))
g=ImageOps.grayscale(Image.open(HERE/'constructed-ripple-mask.png'));lo=bytes.fromhex(palette['b']);hi=bytes.fromhex(palette['B'])
colored=Image.merge('RGB',tuple(g.point(lambda v,l=l,h=h:round(l+(h-l)*v/255)) for l,h in zip(lo,hi)));colored.save(HERE/'constructed-qud-preview.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,760),'#142823');d=ImageDraw.Draw(plate)
d.text((24,18),'SWIMMING WATER / native connected pool + source depth semantics > editable flowing surface',font=font,fill='#e3cf43')
plate.paste(capture.crop(region).resize((256,374),Image.Resampling.NEAREST),(24,80))
ref=Image.open(DONOR/'water-deep.png').convert('RGBA').resize((288,288),Image.Resampling.NEAREST);plate.paste(ref,(367,100),ref)
plate.paste(colored.resize((320,320),Image.Resampling.LANCZOS),(728,94));plate.paste(g.resize((288,288),Image.Resampling.LANCZOS).convert('RGB'),(1110,110))
for x,t in [(24,'Original shallow-pool context'),(365,'Actual WaterDeepRamp'),(728,'Manual native b/B surface'),(1100,'Editable neutral ripple mask')]:d.text((x,490),t,font=font,fill='#e5e8d8')
for i,t in enumerate(['Deep water is a supported authored state; the original Joppa crop is not evidence of deep water there.',
 'Native predicates own depth. Wet-neighbor coverage and deep-neighbor blend coverage must remain independent.',
 'Native blue base b #0048BD and ripple B #0096FF; no bottom caustics, white foam rim or per-cell water circles.',
 'World-continuous surface, separate source tint roles, no game/simulation changes during generation.']):d.text((24,558+i*33),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
