"""One scratchy Pocketed Vest: source identity, editable whole cloth and body paint."""
from pathlib import Path
from datetime import datetime, timezone
import io, sys, json, hashlib
import numpy as np
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2042613316')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def raster(svg):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg,skip_system_fonts=True))).convert('RGBA')
def svg(content):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+content+'</svg>'

paths={
 'south':'M191 232 L222 220 Q256 260 289 220 L320 235 Q337 245 340 269 Q321 297 330 337 L341 409 L366 552 Q255 578 144 552 L169 409 L181 337 Q191 297 172 269 Q169 245 191 232Z',
 'east':'M213 215 L267 232 Q315 270 340 321 Q348 350 325 380 L329 440 L333 553 Q255 574 175 553 L167 525 Q162 492 188 448 Q201 421 195 394 L179 313 Q171 259 213 215Z',
 'north':'M188 232 L220 220 Q253 240 286 220 L317 235 Q334 245 337 269 Q318 297 327 337 L338 409 L363 552 Q252 578 141 552 L166 409 L178 337 Q188 297 169 269 Q166 245 188 232Z'}
panels={
 'south':'<rect x="201" y="329" width="48" height="59" rx="7"/><rect x="263" y="329" width="48" height="59" rx="7"/><rect x="184" y="443" width="65" height="77" rx="8"/><rect x="263" y="443" width="65" height="77" rx="8"/>',
 'east':'<path d="M302 324 L331 337 L327 387 L301 379Z M302 445 L330 449 L329 520 L300 522Z"/>',
 'north':''}
stitches={
 'south':'<path d="M222 220 Q256 263 289 220 M256 269 L256 546 M201 344 L249 344 M263 344 L311 344 M184 460 L249 460 M263 460 L328 460 M155 548 Q255 568 355 548"/>',
 'east':'<path d="M213 215 Q243 227 267 232 M304 339 L331 351 M302 460 L330 463 M185 549 Q255 568 322 549"/>',
 'north':'<path d="M220 220 Q253 243 286 220 M253 251 L253 550 M151 548 Q252 568 352 548"/>'}
contexts=[Image.new('RGBA',(1536,1024)) for _ in range(2)]
for i,f in enumerate(paths):
    drawing=svg('<g stroke="#202523" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"><path fill="#dededb" d="'+paths[f]+'"/><g fill="#c7c7c4">'+panels[f]+'</g><g fill="none">'+stitches[f]+'</g></g>')
    (HERE/f'pattern-{f}.svg').write_bytes(drawing.encode());cloth=raster(drawing);cloth.save(HERE/f'constructed-cloth-{f}.png')
    detail_svg=svg('<g fill="white">'+panels[f]+'</g>');(HERE/f'detail-region-{f}.svg').write_bytes(detail_svg.encode());raster(detail_svg).getchannel('A').save(HERE/f'detail-region-{f}.png')
    body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');a=np.array(body);g=a[:,:,:3].mean(axis=2);a[:,:,:3]=np.uint8(np.round(g[:,:,None]*np.array([1,.12,.16])));key=Image.fromarray(a)
    key.save(HERE/f'red-body-{f}.png')
    lower=Image.open(ROOT/f'art/conversion/fit-human-female-cloth-robe/v1/body-visibility-{f}.png').convert('L')
    if f=='east':upper='M198 248 Q231 237 254 258 Q274 276 273 310 Q273 331 270 350 Q269 372 267 390 Q278 414 279 450 L283 508 L242 518 L231 476 Q218 448 214 420 L210 389 Q194 362 187 329 Q178 285 198 248Z'
    else:
        left='M128 248 Q151 231 177 249 Q192 268 186 302 L174 340 Q161 374 161 414 L92 414 L105 358 L119 302Z'
        upper='<path d="'+left+'"/><g transform="translate(512 0) scale(-1 1)"><path d="'+left+'"/></g>'
    if f=='east':upper='<path d="'+upper+'"/><circle cx="268" cy="536" r="33"/>'
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
    p=MOD/f'Textures/Things/Pawn/Humanlike/Apparel/FlakVest/FlakVest_Female_{f}.png'
    refs.append(dict(private_path=p.as_posix(),sha256=sha(p),facing=f,role='Installed Retextured Apparel cardinal vest silhouette/spacing only; not armor, fabric or literal color.'))
bindings=[]
for actor in json.loads((ROOT/'art/village/sources.json').read_text())['actors']:
 for resident in actor['native_instances']:
  for part in resident['parts']:
   if (part.get('equipped') or {}).get('blueprint')=='Pocketed Vest':bindings.append(dict(actor=actor['creature'],gender=resident['gender'],instance=resident['instance'],part=part))
packet=dict(entry='FIT-HUMAN-FEMALE-POCKETED-VEST-BODY-0',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),item=original,observed_bindings=bindings,
 body=ref(BODY/'model.json'),body_metadata=ref(BODY.parent/'v1/source-packet.json'),donor=dict(package='Retextured Apparel',about_sha256=sha(MOD/'About/About.xml'),assets=refs),
 design='Scratchy cloth sleeveless kirtle/vest fitted with four mirrored practical front pockets and narrow front-edge profile pockets. Plain back. No armor, lapels, zips or straps imported from donor. Pocket number/placement and seam details are authored from the description and small sprite.',
 palette=dict(foreground='y',detail='K',detail_assignment='Pocket panels, authored placement. Neutral cloth and neutral panel layer retained; equipment-detail tint is independent of body.'),
 coverage='True sleeveless openings are garment construction, not destructive limb-shaped cutoffs. Full profile cloth remains under the original near arm. Front/back reuse validated lower-arm paint with item-specific upper arms; profile follows its actual original arm contour and round hand instead of extending the former sleeve mask into the torso.',
 frame=dict(canvas=[512,1024],contact=[256,950],facings=['south','east','north'],west='Mirror east: paired front pockets and symmetric construction, no handed detail'),native_acceptance='Pending all-conversions generation gate; outfit precedence not yet native-tested')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
print('Prepared female Pocketed Vest: full editable cloth, separate pocket tint region and original-arm ownership.')
