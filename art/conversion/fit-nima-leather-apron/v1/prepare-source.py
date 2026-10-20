"""Source-bound boar-hide apron: one item on the unchanged ordinary human base."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/1814987817')
SIZE=(512,1024);FACES=['south','east','north']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def shape(d,fill='#dddddd',stroke='#252525',width=5):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
# Continuous full item, including physically hidden front panel when seen from back.
panels={
 'south':'M211 303 Q254 312 299 303 L307 383 Q322 410 343 422 L354 717 Q257 747 153 717 L164 423 Q190 410 203 383Z',
 'east':'M278 284 Q310 298 329 326 L314 389 Q309 410 319 445 L320 713 Q280 735 218 719 L208 437 Q239 418 253 393 L262 316Z',
 'north':'M211 303 Q254 312 299 303 L307 383 Q322 410 343 422 L354 717 Q257 747 153 717 L164 423 Q190 410 203 383Z'}
loops={
 'south':'M222 223 Q254 203 285 224 L304 318 L287 322 L272 236 Q253 228 236 236 L221 322 L204 318Z',
 'east':'M215 224 Q240 210 265 228 L287 292 L275 302 L253 239 Q234 229 224 239Z',
 'north':'M221 223 Q254 239 285 223 L282 236 Q254 251 224 236Z'}
ties={
 'south':'M162 426 Q254 440 344 425 L345 439 Q254 454 161 440Z',
 'east':'M207 425 Q253 432 318 422 L319 438 Q258 447 208 441Z M213 433 Q188 421 184 435 Q183 450 210 444 M207 441 L186 471 M214 442 L206 477',
 'north':'M161 425 Q254 439 344 425 L345 441 Q254 455 161 441Z M249 440 Q217 422 214 438 Q215 454 249 444 M255 440 Q283 420 290 439 Q288 456 255 446 M250 445 L231 486 M255 445 L272 483'}
marks={
 'south':'M228 344 L239 362 M236 344 L228 363 M287 460 L296 451 M281 466 L287 460 M205 624 L228 615 M210 631 L233 621 M302 658 Q312 653 315 660 M193 505 Q201 497 205 506',
 'east':'M292 346 L305 355 M302 342 L295 357 M287 491 L306 484 M284 500 L299 493 M274 638 Q284 628 291 639 M248 678 L258 670',
 'north':'M228 601 L238 612 M291 647 Q299 639 306 645'}
folds={
 'south':'M216 380 L207 419 M293 383 L305 421 M185 463 Q198 566 183 691 M325 462 Q312 569 330 693 M246 469 Q254 594 247 708',
 'east':'M283 371 L273 411 M306 458 Q295 565 306 697 M235 467 Q248 584 240 705',
 'north':'M185 463 Q198 566 183 691 M325 462 Q312 569 330 693'}
redsheet=Image.new('RGBA',(1536,1024));neutralsheet=redsheet.copy();zoom=redsheet.copy()
for i,f in enumerate(FACES):
 panel=shape(panels[f]);loop=shape(loops[f]);tie=shape(ties[f],fill='#cccccc')
 crease=f'<path d="{folds[f]}" fill="none" stroke="#aaaaaa" stroke-width="3" stroke-linecap="round"/>'
 wear=f'<path d="{marks[f]}" fill="none" stroke="#777777" stroke-width="3" stroke-linecap="round"/>'
 pattern=svg(loop+panel+tie+crease+wear);(HERE/f'pattern-{f}.svg').write_text(pattern,encoding='utf-8');apron=raster(pattern);apron.save(HERE/f'constructed-cloth-{f}.png')
 detail=Image.new('L',SIZE);ImageDraw.Draw(detail).rectangle((0,590,512,1024),fill=255);detail.save(HERE/f'detail-region-{f}.png')
 # Open-back neck band/ties are over the body; the front panel is retained behind it.
 back_visible=raster(svg(loop+tie)) if f=='north' else Image.new('RGBA',SIZE)
 back_visible.getchannel('A').save(HERE/f'back-visible-{f}.png')
 if f=='north':mask=Image.fromarray(255-np.array(back_visible.getchannel('A')))
 else:
  mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask);d.rectangle((0,0,512,240),fill=255)
  if f=='east':
   arm_path='M222 240 Q200 265 204 300 Q209 347 214 390 Q211 420 225 450 L244 512 L277 515 L276 454 Q273 418 263 391 L268 314 Q274 268 248 248Z'
   arm=raster(svg(shape(arm_path,'white','white',2)+'<circle cx="267" cy="535" r="35" fill="white"/>')).getchannel('A')
   mask=Image.fromarray(np.maximum(np.array(mask),np.array(arm)))
 mask.save(HERE/f'body-visibility-{f}.png')
 body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');ba=np.array(body);red=ba.copy();red[:,:,:3]=np.uint8(np.round(ba[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
 for target,base in [(neutralsheet,body),(redsheet,Image.fromarray(red))]:
  effective=Image.fromarray(np.uint8(np.array(mask)*(ba[:,:,3]>0)))
  assembly=Image.composite(base,Image.alpha_composite(base,apron),effective);target.paste(assembly,(i*512,0))
  if target is redsheet:
   crop=assembly.crop((64,190,448,830)).resize((461,768),Image.Resampling.LANCZOS);zoom.paste(crop,(i*512+25,128))
neutralsheet.save(HERE/'constructed-neutral-context.png');redsheet.save(HERE/'constructed-red-context.png');zoom.save(HERE/'constructed-red-torso-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Leather Apron');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actor=next(a for a in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if a['creature']=='Nima Ruda');resident=actor['native_instances'][0];binding=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Leather Apron')
refs=[]
for f in FACES:
 p=MOD/f'Textures/Things/Apparel/Apron/Apron_Female_{f}.png';refs.append(dict(file=str(p),sha256=sha(p),facing=f,mod='Vanilla Apparel Expanded',workshop_id='1814987817',role='Cardinal apron construction: neck loop, front bib/skirt, side waist tie and open back. Pockets are excluded because Qud does not specify them.'))
write(HERE/'source-packet.json',dict(entry='FIT-NIMA-LEATHER-APRON-BODY-0',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Nima Ruda',race='Human; ordinary female base, mutation anatomy separate',item=original,actual_binding=binding,captured_resident=resident,body=ref(BODY/'model.json'),donor_references=refs,
 design='Long work apron with a neck loop, front bib, waist ties and scarred/burned boar hide. Lower primary/detail division follows the glyph; no pockets, sleeves, jewelry, invented tool belt or other outfit. Back is open: retained front panel behind original body, neck band/ties visible over it. Hand/arm ownership is independent.',
 palette=dict(foreground='w',detail='W',original_reference='Normalized primary pale225/229/216 and detail143/160/138; actual palette is separate.',detail_assignment='Lower hide field, following original rows17..21. Authored location at y590; not a claim of a second physical material.'),
 frame=dict(canvas=[512,1024],contact=[256,950],camera='Strict south/front, east/right profile, north/back; west mirrors east',torso_zoom_crop=[64,190,448,830],torso_zoom_size=[461,768],torso_zoom_origin=[25,128]),
 mutations='Captured extra mutation-managed parts remain in the source packet. This fit uses only the unmutated ordinary body/Body0; added limbs and named full outfit remain unfinished.',native_acceptance='Pending full-set generation gate'))
# Contextual provenance plate publishes references in comparison, not raw donor assets.
plate=Image.new('RGB',(1536,1080),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
d.text((24,18),'NIMA > HUMAN BASE > LEATHER APRON / actual source and directional reference',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA');plate.paste(orig.resize((160,240),Image.Resampling.NEAREST),(24,95),orig.resize((160,240),Image.Resampling.NEAREST))
for y,text in [(355,'Qud original tile / normalized colors'),(385,'Boar hide: knife scars and tong burns'),(415,'Actual Body 176 / item529 / laterality0'),(445,'Native primary w / lower detail W'),(475,'No inferred pockets or full-back robe')]:d.text((24,y),text,font=font,fill='#e5e8d8')
for i,(f,r) in enumerate(zip(FACES,refs)):
 im=Image.open(r['file']).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();im=im.crop(box);im.thumbnail((240,240));plate.paste(im,(535+i*330,100),im);d.text((535+i*330,365),'MOD APRON / '+f.upper(),font=font,fill='#e3cf43')
 context=neutralsheet.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(context);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,440));d.text((535+i*330,980),'CONSTRUCTED / '+f.upper(),font=font,fill='#e3cf43')
d.text((24,1025),'Manual cardinal construction; one item on original unmutated body. Reference camera/structure only; no native acceptance.',font=font,fill='#e5e8d8');plate.save(HERE/'source-comparison.png')
print('Prepared exact apron source packet, original/mod comparison, neutral construction, red torso context and separate per-facing body visibility.')
