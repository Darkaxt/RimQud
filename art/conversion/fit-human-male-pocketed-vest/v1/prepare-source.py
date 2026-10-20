"""One scratchy Pocketed Vest: source identity, editable whole cloth and body paint."""
from pathlib import Path
from datetime import datetime, timezone
import io, sys, json, hashlib
import numpy as np
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-male/v2'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2042613316')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def raster(svg):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg,skip_system_fonts=True))).convert('RGBA')
def svg(content):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+content+'</svg>'

paths={
 'south':'M190 265 L221 250 Q255 290 289 250 L322 265 Q340 276 343 300 Q329 330 339 365 L347 435 L368 591 Q256 610 144 591 L165 435 L177 365 Q187 330 169 300 Q167 276 190 265Z',
 'east':'M209 235 L274 255 Q323 300 333 335 L329 435 L334 590 Q256 612 175 590 L167 555 Q163 511 190 469 Q203 441 195 402 L173 329 Q163 275 209 235Z',
 'north':'M188 265 L220 250 Q255 270 290 250 L324 265 Q342 276 345 300 Q331 330 341 365 L349 435 L370 591 Q256 610 142 591 L163 435 L175 365 Q185 330 167 300 Q165 276 188 265Z'}
panels={
 'south':'<rect x="198" y="358" width="51" height="61" rx="7"/><rect x="263" y="358" width="51" height="61" rx="7"/><rect x="184" y="479" width="65" height="83" rx="8"/><rect x="263" y="479" width="65" height="83" rx="8"/>',
 'east':'<path d="M302 354 L331 363 L329 414 L301 409Z M303 485 L333 489 L332 559 L300 562Z"/>',
 'north':''}
stitches={
 'south':'<path d="M221 250 Q255 293 289 250 M256 296 L256 585 M198 374 L249 374 M263 374 L314 374 M184 497 L249 497 M263 497 L328 497 M155 586 Q256 605 357 586"/>',
 'east':'<path d="M209 235 Q241 247 274 255 M304 370 L331 377 M303 502 L333 506 M185 586 Q256 606 323 586"/>',
 'north':'<path d="M220 250 Q255 273 290 250 M255 279 L255 586 M153 586 Q256 605 359 586"/>'}
contexts=[Image.new('RGBA',(1536,1024)) for _ in range(2)]
for i,f in enumerate(paths):
    drawing=svg('<g stroke="#202523" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"><path fill="#dededb" d="'+paths[f]+'"/><g fill="#c7c7c4">'+panels[f]+'</g><g fill="none">'+stitches[f]+'</g></g>')
    (HERE/f'pattern-{f}.svg').write_bytes(drawing.encode());cloth=raster(drawing);cloth.save(HERE/f'constructed-cloth-{f}.png')
    detail_svg=svg('<g fill="white">'+panels[f]+'</g>');(HERE/f'detail-region-{f}.svg').write_bytes(detail_svg.encode());raster(detail_svg).getchannel('A').save(HERE/f'detail-region-{f}.png')
    body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');a=np.array(body);g=a[:,:,:3].mean(axis=2);a[:,:,:3]=np.uint8(np.round(g[:,:,None]*np.array([1,.12,.16])));key=Image.fromarray(a)
    key.save(HERE/f'red-body-{f}.png')
    lower=Image.open(ROOT/f'art/conversion/fit-human-male-cloth-robe/v2/body-visibility-{f}.png').convert('L')
    if f=='east':upper='<path d="M205 265 Q228 250 252 275 Q273 295 278 330 L281 350 Q280 381 274 410 Q279 435 284 450 L294 512 L291 532 L250 535 L242 514 Q220 474 212 430 Q203 389 199 351 Q192 302 205 265Z"/><circle cx="279" cy="555" r="36"/>'
    else:
        left='M124 285 Q147 263 175 280 Q185 310 181 344 L169 390 Q159 423 163 448 L94 448 L103 386 L116 337Z'
        upper='<path d="'+left+'"/><g transform="translate(512 0) scale(-1 1)"><path d="'+left+'"/></g>'
    upper_svg=svg('<g fill="white">'+upper+'</g>');(HERE/f'upper-arm-visibility-{f}.svg').write_bytes(upper_svg.encode())
    painted=np.array(raster(upper_svg).getchannel('A'))
    mask=Image.fromarray(painted if f=='east' else np.maximum(np.array(lower),painted));mask.save(HERE/f'body-visibility-{f}.png')
    for out,base in zip(contexts,[key,body]):
        composed=Image.composite(base,Image.alpha_composite(base,cloth),mask);out.paste(composed,(i*512,0))
contexts[0].save(HERE/'constructed-red-context.png');contexts[1].save(HERE/'constructed-neutral-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Pocketed Vest')
assert sha(DONOR/original['reference_file'])==original['reference_sha256']
refs=[]
for f in paths:
    p=MOD/f'Textures/Things/Pawn/Humanlike/Apparel/FlakVest/FlakVest_Male_{f}.png'
    refs.append(dict(private_path=p.as_posix(),sha256=sha(p),facing=f,role='Installed Retextured Apparel cardinal vest silhouette/spacing only; not armor, fabric or literal color.'))
bindings=[]
for actor in json.loads((ROOT/'art/village/sources.json').read_text())['actors']:
 for resident in actor['native_instances']:
  for part in resident['parts']:
   if (part.get('equipped') or {}).get('blueprint')=='Pocketed Vest':bindings.append(dict(actor=actor['creature'],gender=resident['gender'],instance=resident['instance'],part=part))
packet=dict(entry='FIT-HUMAN-MALE-POCKETED-VEST-BODY-0',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),item=original,observed_bindings=bindings,
 body=ref(BODY/'model.json'),body_metadata=ref(BODY.parent/'v1/source-packet.json'),donor=dict(package='Retextured Apparel',about_sha256=sha(MOD/'About/About.xml'),assets=refs),
 design='Scratchy cloth sleeveless kirtle/vest fitted with four mirrored practical front pockets and narrow front-edge profile pockets. Plain back. No armor, lapels, zips or straps imported from donor. Pocket number/placement and seam details are authored from the description and small sprite.',
 palette=dict(foreground='y',detail='K',detail_assignment='Pocket panels, authored placement. Neutral cloth and neutral panel layer retained; equipment-detail tint is independent of body.'),
 coverage='True sleeveless openings are garment construction, not destructive limb-shaped cutoffs. Full profile cloth remains under the original near arm. Front/back reuse validated lower-arm paint with item-specific upper arms; profile follows its actual original arm contour and round hand instead of extending the former sleeve mask into the torso.',
 frame=dict(canvas=[512,1024],contact=[256,950],facings=['south','east','north'],west='Mirror east: paired front pockets and symmetric construction, no handed detail'),native_acceptance='Pending all-conversions generation gate; outfit precedence not yet native-tested')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
print('Prepared male Pocketed Vest: full editable cloth, separate pocket tint region and original-arm ownership.')
