"""Wide-brimmed Hat: source palette and worn crown on a fixed human head."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, io, sys
import numpy as np
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def svg(x):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+x+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def path(d,fill='#dededb'):return '<path fill="'+fill+'" stroke="#202523" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" d="'+d+'"/>'
brims={
 'south':'M102 73 Q149 49 194 55 L315 55 Q365 47 410 73 Q400 100 256 102 Q110 101 102 73Z',
 'east':'M105 77 Q149 53 213 56 L316 57 Q375 56 417 82 Q380 99 260 100 Q148 100 105 77Z',
 'north':'M101 75 Q150 50 194 55 L315 55 Q365 48 411 75 Q398 100 256 102 Q111 101 101 75Z'}
crowns={
 'south':'M185 67 L193 20 Q206 5 234 15 L256 22 L282 13 Q311 12 321 27 L330 67 Q257 91 185 67Z',
 'east':'M181 67 L190 28 Q195 11 228 15 L285 18 Q308 16 317 32 L324 69 Q251 89 181 67Z',
 'north':'M184 67 L192 25 Q203 10 230 14 L260 18 L288 14 Q311 16 320 30 L329 67 Q256 88 184 67Z'}
bands={
 'south':'M186 56 Q255 77 329 57 L331 70 Q256 91 184 70Z',
 'east':'M183 56 Q251 76 323 58 L325 70 Q252 90 181 69Z',
 'north':'M185 56 Q256 74 328 57 L330 70 Q256 90 183 69Z'}
creases={
 'south':'M208 25 Q230 38 251 27 L257 33 Q280 23 305 31 M211 40 L205 53 M286 34 Q281 46 310 54 M120 77 Q141 84 165 83 M347 82 L380 77',
 'east':'M205 25 Q229 31 258 26 L287 28 M207 37 Q212 48 201 54 M292 34 L309 52 M123 80 Q144 84 159 82 M352 84 L388 80',
 'north':'M211 25 L235 29 L259 24 L282 28 L304 30 M218 40 L211 53 M282 38 L299 53 M119 79 L159 83 M350 82 L386 78'}
full=Image.new('RGBA',(1536,1024));neutral=full.copy();zoom=full.copy()
for i,f in enumerate(brims):
    pattern=svg(path(brims[f])+path(crowns[f])+path(bands[f],'#c9c9c6')+'<path fill="none" stroke="#797c78" stroke-width="3" stroke-linecap="round" d="'+creases[f]+'"/>')
    (HERE/f'pattern-{f}.svg').write_bytes(pattern.encode());hat=raster(pattern);hat.save(HERE/f'constructed-cloth-{f}.png')
    detail_svg=svg(path(bands[f],'white').replace('#202523','white'));(HERE/f'band-region-{f}.svg').write_bytes(detail_svg.encode());raster(detail_svg).getchannel('A').save(HERE/f'detail-region-{f}.png')
    # A hat covers the upper head. No original skin is painted above it.
    Image.new('L',(512,1024),0).save(HERE/f'body-visibility-{f}.png')
    body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');a=np.array(body);gray=a[:,:,:3].mean(2);a[:,:,:3]=np.uint8(np.round(gray[:,:,None]*np.array([1,.12,.16])));red=Image.fromarray(a)
    for target,base in [(full,red),(neutral,body)]:
        assembly=Image.alpha_composite(base,hat);target.paste(assembly,(i*512,0))
        if target is full:
            # Enlarged head/shoulder context only; the full registered body is retained.
            crop=assembly.crop((64,0,448,384)).resize((512,512),Image.Resampling.LANCZOS);zoom.paste(crop,(i*512,256))
full.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-head-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Wide-brimmed Hat')
assert sha(DONOR/original['reference_file'])==original['reference_sha256']
refs=[x for x in json.loads((DONOR/'apparel-textures.json').read_text()) if x['file'].startswith('worn-hat-')]
for r in refs:assert sha(DONOR/r['file'])==r['png_sha256']
bindings=[]
for actor in json.loads((ROOT/'art/village/sources.json').read_text())['actors']:
 for resident in actor['native_instances']:
  for part in resident['parts']:
   if (part.get('equipped') or {}).get('blueprint')=='Wide-brimmed Hat':bindings.append(dict(actor=actor['creature'],gender=resident['gender'],instance=resident['instance'],part=part))
packet=dict(entry='FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),item=original,observed_bindings=bindings,body=ref(BODY/'model.json'),donor_references=refs,
 reference_decision='Actual RimWorld CowboyHat SEN assets supply low crown/wide brim, shallow top visibility and directional convention. Native Qud worn papery creases and sweat/salt stains govern material and silhouette; no buckle, badge, feather or new costume.',
 design='Low worn/crushed crown, broad soft brim and simple lower-crown band. Source reference has a small lower detail stripe, expanded as a continuous band. Exact folds/stains are authored from description; no paper material type is asserted solely from papery creases.',
 palette=dict(foreground='y',detail='b',detail_assignment='Lower crown band; neutral material and separate band coverage retained.'),
 coverage='Whole hat sits above the unchanged head. Body-over-hat mask is explicitly zero: no bare head or copied forehead ink over the hat. Hair/mutation/outfit precedence remains native integration work.',
 frame=dict(canvas=[512,1024],contact=[256,950],hat_geometry_top=5,head_unchanged=True,zoom_crop=[64,0,448,384],zoom_scale=4/3,zoom_origin_y=256,facings=['south','east','north'],west='Mirror east; no handed ornament'),
 native_acceptance='Pending all-conversions generation gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
print('Prepared source-bound female hat: cardinal full geometry, separate blue-band region, unchanged head and zero skin overlay.')
