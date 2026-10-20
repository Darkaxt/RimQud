"""Construct one source-bound Cloth Robe on the registered adult female body."""
from pathlib import Path
import hashlib, io, json, sys
from datetime import datetime, timezone
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BODY = ROOT/'art/conversion/body-human-female/v2'
DONOR = Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(), sha256=sha(p))
def write(name, data): (HERE/name).write_bytes((json.dumps(data, indent=2)+'\n').encode())
def raster(svg): return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True))).convert('RGBA')

# These are authored garment contours, not changes to the body silhouette.
# The cuff edge is a continuous quadratic cross-section and the skirt is intact.
paths = {
 'south': 'M221 220 Q255 250 289 220 L319 235 Q360 235 374 274 L418 402 Q388 426 347 409 L328 362 Q324 414 344 478 L382 877 Q256 916 130 877 L168 478 Q188 414 184 362 L165 409 Q124 426 94 402 L138 274 Q152 235 193 235Z',
 'east': 'M213 215 Q246 214 269 237 Q293 264 314 301 Q348 333 326 363 L320 435 Q329 483 326 537 L313 882 Q258 900 187 882 L170 544 Q164 496 195 443 Q204 421 201 397 Q177 342 179 295 Q180 243 213 215Z',
 'north': 'M220 220 Q253 239 286 220 L316 235 Q357 235 371 274 L415 402 Q385 426 344 409 L325 362 Q321 414 341 478 L379 877 Q253 916 127 877 L165 478 Q185 414 181 362 L162 409 Q121 426 91 402 L135 274 Q149 235 190 235Z'
}
seams = {
 'south': '<path d="M221 220 Q255 252 289 220 M184 362 Q177 333 175 291 M328 362 Q335 333 337 291 M165 409 Q128 427 94 402 M347 409 Q384 427 418 402 M142 874 Q256 904 370 874"/><path opacity=".3" stroke-width="3" d="M191 446 Q183 666 165 860 M320 446 Q327 666 345 860 M256 468 L256 874"/>',
 'east': '<path d="M213 215 Q245 218 269 237 M220 246 Q200 262 205 300 L215 394 Q244 413 281 400 L276 308 M215 394 Q244 414 281 400 M197 877 Q255 891 302 877"/><path opacity=".3" stroke-width="3" d="M213 569 Q222 713 217 859 M300 565 L287 858"/>',
 'north': '<path d="M220 220 Q253 241 286 220 M181 362 Q174 333 172 291 M325 362 Q332 333 334 291 M162 409 Q125 427 91 402 M344 409 Q381 427 415 402 M139 874 Q253 904 367 874"/><path opacity=".3" stroke-width="3" d="M188 446 Q180 666 162 860 M317 446 Q324 666 342 860 M253 468 L253 874"/>'
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
    q = 'M70 397 Q129 426 179 407 L171 565 L64 565Z M333 407 Q383 426 433 397 L448 565 L332 565Z' if f!='east' else 'M211 396 Q244 414 284 400 L284 481 L291 506 Q312 528 297 555 Q282 581 255 568 Q230 560 231 536 L237 509 L220 460Z'
    mask_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+q+'"/></svg>'
    (HERE/f'body-visibility-{f}.svg').write_bytes(mask_svg.encode())
    mask = raster(mask_svg).getchannel('A')
    if f != 'east':
        # Below the cuffs the original silhouette separates into three row
        # runs. Keep only the two outer anatomical arms, never the hips behind.
        ba = np.array(body)[:,:,3]
        ownership = np.zeros(ba.shape,dtype=np.uint8)
        for y in range(390,565):
            z = np.pad(ba[y]>80,(1,1)).astype(int); edges=np.diff(z)
            runs=[(l,r) for l,r in zip(np.flatnonzero(edges==1),np.flatnonzero(edges==-1)) if r-l>5]
            if len(runs)==3:
                ownership[y,:(runs[0][1]+runs[1][0])//2]=255
                ownership[y,(runs[1][1]+runs[-1][0])//2:]=255
        mask=Image.fromarray(np.minimum(np.array(mask),ownership))
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
write('source-packet.json',dict(entry='FIT-HUMAN-FEMALE-CLOTH-ROBE-BODY-0',workflow='regional-curved-v1',
 recorded_at=datetime.now(timezone.utc).isoformat(),item=original,observed_cloth_robe_bindings=bindings,
 body=ref(BODY/'model.json'),body_metadata=ref(BODY.parent/'v1/source-packet.json'),
 donor_references=old['donor_references'],
 reference_decision='Actual RimWorld Duster references supply outline/shading and cardinal presentation only. Qud closed goat-wool robe identity takes precedence. Male donor silhouette is not female anatomy or an open-coat design.',
 design='Loose closed long goat-wool robe, simple rounded neckline, short broad sleeves, sparse shale freckles. No belt, trousers, coat lapels, jewelry or changes to the body. Description-derived freckles are tonal in neutral production art; native item foreground/detail both y.',
 coordinates=dict(canvas=[512,1024],contact=[256,950],facings=['south','east','north'],west='mirror east; plain garment symmetric'),
 authored_limits='Tiny source does not establish sleeve length/seams. These are explicit interpretations. The template is unmutated; native named mutation outfit precedence remains pending.',
 native_acceptance='Pending all-conversions generation gate'))
print('Prepared adult female Cloth Robe: source metadata, continuous editable SEN patterns and unchanged red body context.')
