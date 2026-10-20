"""Shallow source-water state from shared native facts and its own donor/design."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,random,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
DEEP=ROOT/'art/conversion/tile-water-deep/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
shared=json.loads((DEEP/'source-packet.json').read_text())
assert sha(Path(shared['native_definitions']['path']))==shared['native_definitions']['sha256']
assert sha(Path(shared['depth_evidence']['path']))==shared['depth_evidence']['sha256']
reference=shared['original'];assert sha(DONOR/reference['reference_file'])==reference['reference_sha256']
donor=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='water-shallow.png');assert sha(DONOR/donor['file'])==donor['png_sha256']
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
packet=dict(entry='TILE-WATER-SHALLOW',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='Visible open water-bearing liquid below native swimming depth; wading and thin puddle states retain native predicates/ownership',
 native_description='A pool of liquid.',original=reference,
 shared_source=dict(entry='TILE-WATER-DEEP',**asset(DEEP/'source-packet.json'),
  reuse='Same installed Water/Pond inheritance, native pool original, exact b/B palette/capture and historical depth-predicate observations; reread hashes now. This does not reuse the deep-water material or its authoring acceptance.'),
 native_definitions=shared['native_definitions'],depth_evidence=shared['depth_evidence'],native_capture=shared['native_capture'],
 native_state='Pond declares500drams of water-600,salt-400. Historical diagnostic is wading at200 and swimming at2000 in the tested state. Actual IsWadingDepth/IsSwimmingDepth remain authoritative. A thin puddle is not automatically wading; no fluid amount or traversability change is authorized by art.',
 donor_reference=dict(**donor,role='Actual WaterShallowRamp supplies gentle overhead surface variation only; donor hue, apparent depth, material UV semantics and simulation do not establish Qud behavior.'),
 source_palette=dict(base_role='b',base_hex=palette['b'],ripple_role='B',ripple_hex=palette['B'],
  interpretation='Native Water foreground is b and the retained pool capture contains b/B. The shallower state uses more B coverage and finer broken ripples than deep; this distinction is authored rather than a claim that native depth changes hue.'),
 construction='Separate editable brighter shallow surface with small irregular ripple loops/broken wavelets, quiet water between them and no opaque gray donor color. Preserve source blue family; no underwater pebbles, caustic polygon web or foam grid.',
 required_states='One world-continuous shallow material; wet/dry shoreline from all eligible wet neighbors; deep-over-shallow blend from swimming neighbors. Shared geometric masks have distinct predicates. Compose against selected deep material only after this shallow art is authored.',
 frame='Single flat overhead surface. No creature turnarounds, body metadata or clothing applies. Texture UV is world-continuous; no rim per cell.',
 color_contract='Separate neutral white base and ripple-alpha layers with actual source liquid colors. Native mixtures or unsupported color states retain original graphics; preview b/B does not generalize all liquids.',
 native_acceptance='Deferred until every conversion is generation-ready')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
rng=random.Random(20520);defs=[];shapes=['<rect width="512" height="512" fill="#777777"/>']
for i in range(18):
 x,y=rng.uniform(0,512),rng.uniform(0,512);rx,ry=rng.uniform(45,120),rng.uniform(25,75)
 tone=rng.choice(['#bbbbbb','#444444'])
 defs.append(f'<radialGradient id="m{i}"><stop stop-color="{tone}" stop-opacity=".4"/><stop offset="1" stop-color="{tone}" stop-opacity="0"/></radialGradient>')
 for dx in [-512,0,512]:
  for dy in [-512,0,512]:shapes.append(f'<ellipse cx="{x+dx:.1f}" cy="{y+dy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#m{i})"/>')
for i in range(110):
 x,y=rng.uniform(0,512),rng.uniform(0,512);length=rng.uniform(6,23);bend=rng.uniform(1.5,5);tone=rng.randint(165,235)
 for dx in [-512,0,512]:
  for dy in [-512,0,512]:
   shapes.append(f'<path d="M{x+dx:.1f} {y+dy:.1f} q{length*.45:.1f} {-bend:.1f} {length:.1f} 0" stroke="rgb({tone},{tone},{tone})" stroke-width=".9" stroke-opacity=".7" stroke-linecap="round" fill="none"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><defs>'+''.join(defs)+'</defs>'+''.join(shapes)+'</svg>'
(HERE/'constructed-ripple-mask.svg').write_bytes(svg.encode());(HERE/'constructed-ripple-mask.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-ripple-mask.svg'),skip_system_fonts=True))
g=ImageOps.grayscale(Image.open(HERE/'constructed-ripple-mask.png'));lo=bytes.fromhex(palette['b']);hi=bytes.fromhex(palette['B'])
colored=Image.merge('RGB',tuple(g.point(lambda v,l=l,h=h:round(l+(h-l)*v/255)) for l,h in zip(lo,hi)));colored.save(HERE/'constructed-qud-preview.png')
plate=Image.new('RGB',(1440,745),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
d.text((24,18),'SHALLOW / native Pond and wading state > smaller broken ripples > separate native blue roles',font=font,fill='#e3cf43')
native=Image.open(ROOT/shared['native_capture']['path']).crop(shared['native_capture']['sample_rect']).convert('RGB');plate.paste(native.resize((256,374),Image.Resampling.NEAREST),(24,80))
ref=Image.open(DONOR/'water-shallow.png').convert('RGBA').resize((288,288),Image.Resampling.NEAREST);plate.paste(ref,(367,100),ref)
plate.paste(colored.resize((320,320),Image.Resampling.LANCZOS),(728,94));plate.paste(g.resize((288,288),Image.Resampling.LANCZOS).convert('RGB'),(1110,110))
for x,t in [(24,'Original shallow-pool context'),(365,'Actual WaterShallowRamp'),(728,'Manual brighter b/B surface'),(1100,'Editable neutral ripple mask')]:d.text((x,490),t,font=font,fill='#e5e8d8')
for i,t in enumerate(['Reuse source facts with provenance; the shallow material and grain are authored separately from the deep state.',
 'Native wading/swimming predicates are separate from image color. Do not change liquid volume or movement rules.',
 'Fine shallow wavelets and more bright-blue coverage distinguish it from the calm deep-water surface.',
 'No per-cell water rims, bottom caustics, foam, plants or third-party simulation mechanics.']):d.text((24,555+i*33),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
