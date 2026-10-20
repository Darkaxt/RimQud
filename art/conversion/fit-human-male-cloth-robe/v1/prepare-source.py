"""Construct one source-bound Cloth Robe on the registered adult male body."""
from pathlib import Path
import hashlib, io, json, sys
from datetime import datetime, timezone
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BODY = ROOT/'art/conversion/body-human-male/v2'
DONOR = Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p))
def write(name, data): (HERE/name).write_bytes((json.dumps(data, indent=2)+'\n').encode())
def raster(svg): return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True))).convert('RGBA')

# These are authored garment contours, not changes to the body silhouette.
# The cuff edge is a continuous quadratic cross-section and the skirt is intact.
paths = {
 'south': 'M221 250 Q255 278 289 250 L319 253 Q370 248 383 311 L427 425 Q393 451 348 432 L331 389 Q328 465 345 512 L386 886 Q256 920 126 886 L166 512 Q183 465 179 389 L162 432 Q123 451 84 425 L127 311 Q140 248 191 253Z',
 'east': 'M209 235 Q246 236 274 255 Q320 292 330 334 L327 452 Q340 505 328 575 L328 888 Q256 910 181 888 L170 561 Q160 509 191 456 Q201 430 192 402 Q168 359 167 311 Q170 263 209 235Z',
 'north': 'M218 250 Q255 269 292 250 L321 253 Q373 243 386 311 L429 425 Q395 451 350 432 L333 389 Q330 465 347 512 L388 886 Q256 920 124 886 L164 512 Q181 465 177 389 L160 432 Q121 451 82 425 L124 311 Q137 243 189 253Z'
}
seams = {
 'south': '<path d="M221 250 Q255 279 289 250 M179 389 Q174 354 176 326 M331 389 Q336 354 334 326 M162 432 Q123 451 84 425 M348 432 Q393 451 427 425 M138 882 Q256 912 374 882"/><path opacity=".3" stroke-width="3" d="M191 473 L163 866 M320 473 L348 866 M256 485 L256 885"/>',
 'east': '<path d="M209 235 Q246 239 274 255 M219 260 Q201 279 204 321 L219 421 Q254 442 294 425 L279 329 M219 421 Q254 443 294 425 M192 885 Q256 901 317 885"/><path opacity=".3" stroke-width="3" d="M210 599 L210 866 M308 601 L298 866"/>',
 'north': '<path d="M218 250 Q255 272 292 250 M177 389 Q172 354 174 326 M333 389 Q338 354 336 326 M160 432 Q121 451 82 425 M350 432 Q395 451 429 425 M136 882 Q256 912 376 882"/><path opacity=".3" stroke-width="3" d="M189 473 L161 866 M322 473 L350 866 M256 485 L256 885"/>'
}
sheet = Image.new('RGBA', (1536,1024))
neutral = Image.new('RGBA', (1536,1024))
for i, f in enumerate(paths):
    path = paths[f].replace('344 478','377 478').replace('168 478','135 478').replace('341 478','374 478').replace('165 478','132 478')
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g stroke="#202523" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"><path fill="#dededb" d="'+path+'"/><g fill="none">'+seams[f]+'</g></g></svg>'
    (HERE/f'pattern-{f}.svg').write_bytes(svg.encode())
    cloth = raster(svg); cloth.save(HERE/f'constructed-cloth-{f}.png')
    body = Image.open(BODY/f'selected-{f}.png').convert('RGBA')
    a = np.array(body); v = a[:,:,:3].mean(axis=2)
    a[:,:,:3] = np.uint8(np.round(v[:,:,None]*np.array([1,.12,.16])))
    keyed = Image.fromarray(a); keyed.save(HERE/f'red-body-{f}.png')
    # Mask is not cut into this cloth. Forearms shown in the context are the
    # unchanged source body above it, using an explicit separate region.
    left = 'M91 422 Q128 448 174 430 L161 488 L153 523 C171 537 171 572 149 588 C124 605 93 587 87 561 Q84 541 101 527 L91 480Z'
    q = left+' M421 422 Q384 448 338 430 L351 488 L359 523 C341 537 341 572 363 588 C388 605 419 587 425 561 Q428 541 411 527 L421 480Z' if f!='east' else 'M213 425 Q254 445 300 428 L297 524 L251 531 L222 475Z M279 519 C299 519 315 535 315 555 C315 575 299 592 279 592 C259 592 243 575 243 555 C243 535 259 519 279 519Z'
    mask_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+q+'"/></svg>'
    (HERE/f'body-visibility-{f}.svg').write_bytes(mask_svg.encode())
    mask = raster(mask_svg).getchannel('A')
    mask.save(HERE/f'body-visibility-{f}.png')
    for out, base in [(sheet,keyed),(neutral,body)]:
        composition = Image.alpha_composite(base,cloth)
        composition = Image.composite(base,composition,mask)
        out.paste(composition,(i*512,0))
sheet.save(HERE/'constructed-red-context.png')
neutral.save(HERE/'constructed-neutral-context.png')

old = json.loads((ROOT/'art/conversion/fit-dromad-cloth-robe/v1/source-packet.json').read_text())
original = old['original']
assert sha(DONOR/original['reference_file']) == original['reference_sha256']
for r in old['donor_references']: assert sha(DONOR/r['file']) == r['png_sha256']
sources = json.loads((ROOT/'art/village/sources.json').read_text())
bindings=[]
for actor in sources['actors']:
 for resident in actor['native_instances']:
  for part in resident['parts']:
   if (part.get('equipped') or {}).get('blueprint')=='Cloth Robe':
    bindings.append(dict(actor=actor['creature'],gender=resident['gender'],instance=resident['instance'],part=part))
write('source-packet.json',dict(entry='FIT-HUMAN-MALE-CLOTH-ROBE-BODY-0',workflow='regional-curved-v1',
 recorded_at=datetime.now(timezone.utc).isoformat(),item=original,observed_cloth_robe_bindings=bindings,
 body=ref(BODY/'model.json'),body_metadata=ref(BODY.parent/'v1/source-packet.json'),
 donor_references=old['donor_references'],
 reference_decision='Actual RimWorld Duster references supply outline/shading and cardinal presentation only. Qud closed goat-wool robe identity takes precedence. Male donor silhouette is not male anatomy or an open-coat design.',
 design='Loose closed long goat-wool robe, simple rounded neckline, short broad sleeves, sparse shale freckles. No belt, trousers, coat lapels, jewelry or changes to the body. Description-derived freckles are tonal in neutral production art; native item foreground/detail both y.',
 coordinates=dict(canvas=[512,1024],contact=[256,950],facings=['south','east','north'],west='mirror east; plain garment symmetric'),
 authored_limits='Tiny source does not establish sleeve length/seams. These are explicit interpretations. The template is unmutated; native named mutation outfit precedence remains pending.',
 native_acceptance='Pending all-conversions generation gate'))
print('Prepared adult male Cloth Robe: source metadata, continuous editable SEN patterns and unchanged red body context.')
