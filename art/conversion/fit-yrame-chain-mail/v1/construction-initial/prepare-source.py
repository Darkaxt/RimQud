"""Construct Qud linked-loop mail on the ordinary female human base."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');MOD=Path('D:/Steam/steamapps/workshop/content/294100/1814988282');SIZE=(512,1024);FACES=['south','east','north']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
paths={
 'south':'M221 220 Q255 250 289 220 L319 235 Q360 235 374 274 L409 385 Q383 410 350 396 L329 353 Q323 414 344 475 L369 638 Q257 668 137 638 L164 475 Q184 414 181 353 L160 396 Q127 410 101 385 L138 274 Q152 235 193 235Z',
 'east':'M213 215 Q246 214 269 237 Q293 264 314 301 Q348 333 326 363 L320 435 Q329 483 326 537 L319 641 Q257 663 185 641 L170 544 Q164 496 195 443 Q204 421 201 397 Q177 342 179 295 Q180 243 213 215Z',
 'north':'M221 220 Q255 239 289 220 L319 235 Q360 235 374 274 L409 385 Q383 410 350 396 L329 353 Q323 414 344 475 L369 638 Q257 668 137 638 L164 475 Q184 414 181 353 L160 396 Q127 410 101 385 L138 274 Q152 235 193 235Z'}
seams={
 'south':'M221 220 Q255 250 289 220 M181 353 Q173 327 173 290 M329 353 Q337 327 337 290 M160 396 Q127 410 101 385 M350 396 Q383 410 409 385 M145 635 Q257 661 361 635',
 'east':'M213 215 Q246 218 269 237 M220 246 Q200 262 205 300 L215 394 Q244 414 281 400 L276 308 M215 394 Q244 414 281 400 M193 638 Q257 656 311 638',
 'north':'M221 220 Q255 239 289 220 M181 353 Q173 327 173 290 M329 353 Q337 327 337 290 M160 396 Q127 410 101 385 M350 396 Q383 410 409 385 M145 635 Q257 661 361 635'}
detail_paths={
 'south':'M91 363 Q127 389 173 378 L176 413 Q125 435 85 397Z M337 378 Q383 389 419 363 L425 397 Q385 435 334 413Z M121 602 Q257 632 385 602 L390 680 L115 680Z',
 'east':'M204 373 Q244 392 289 379 L295 419 Q243 434 204 413Z M168 605 Q257 636 339 605 L343 680 L164 680Z',
 'north':'M91 363 Q127 389 173 378 L176 413 Q125 435 85 397Z M337 378 Q383 389 419 363 L425 397 Q385 435 334 413Z M121 602 Q257 632 385 602 L390 680 L115 680Z'}
sheet=Image.new('RGBA',(1536,1024));neutral=sheet.copy();zoom=sheet.copy()
for i,f in enumerate(FACES):
 defs='<defs><pattern id="rings" width="12" height="10" patternUnits="userSpaceOnUse"><rect width="12" height="10" fill="#cccccc"/><g fill="none" stroke="#929292" stroke-width="1.3"><ellipse cx="3" cy="2" rx="4" ry="2.5"/><ellipse cx="9" cy="7" rx="4" ry="2.5"/></g></pattern></defs>'
 pattern=svg(defs+f'<path d="{paths[f]}" fill="url(#rings)" stroke="#252525" stroke-width="6" stroke-linejoin="round"/>'+f'<path d="{seams[f]}" fill="none" stroke="#343434" stroke-width="4" stroke-linecap="round"/>')
 (HERE/f'pattern-{f}.svg').write_text(pattern,encoding='utf-8');cloth=raster(pattern);cloth.save(HERE/f'constructed-cloth-{f}.png')
 detail=raster(svg(f'<path d="{detail_paths[f]}" fill="white"/>')).getchannel('A');detail.save(HERE/f'detail-region-{f}.png')
 body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');ba=np.array(body)
 if f=='east':
  q='M211 396 Q244 414 284 400 L284 481 L291 506 Q312 528 297 555 Q282 581 255 568 Q230 560 231 536 L237 509 L220 460Z'
 else:q='M82 378 L101 388 Q127 413 160 399 L179 389 L171 565 L64 565Z M333 389 L350 399 Q383 413 409 388 L433 378 L448 565 L332 565Z'
 mask=raster(svg(f'<path d="{q}" fill="white"/>')).getchannel('A');ma=np.array(mask)
 if f!='east':
  ownership=np.zeros(ba.shape[:2],dtype=np.uint8)
  for y in range(375,568):
   z=np.pad(ba[y,:,3]>80,(1,1)).astype(int);edges=np.diff(z);runs=[(a,b) for a,b in zip(np.flatnonzero(edges==1),np.flatnonzero(edges==-1)) if b-a>5]
   if len(runs)==3:
    ownership[y,:(runs[0][1]+runs[1][0])//2]=255;ownership[y,(runs[1][1]+runs[2][0])//2:]=255
  ma=np.minimum(ma,ownership)
 else:
  # Original forearm and hand contours separate this limb from the adjacent torso.
  for y in range(410,568):
   dark=(ba[y,:,:3].mean(1)<90)&(ba[y,:,3]>128)
   right=np.flatnonzero(dark[260:303])+260
   if len(right):ma[y,int(right[-1])+2:325]=0
 ma[:241]=255;mask=Image.fromarray(ma);mask.save(HERE/f'body-visibility-{f}.png');(HERE/f'body-visibility-{f}.svg').write_text(svg(f'<path d="{q}" fill="white"/>'),encoding='utf-8')
 red=ba.copy();red[:,:,:3]=np.uint8(np.round(ba[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
 for target,base in [(sheet,Image.fromarray(red)),(neutral,body)]:
  effective=Image.fromarray(np.uint8(ma*(ba[:,:,3]>0)));assembled=Image.composite(base,Image.alpha_composite(base,cloth),effective);target.paste(assembled,(i*512,0))
  if target is sheet:
   zoom.paste(assembled.crop((64,190,448,750)).resize((461,672),Image.Resampling.LANCZOS),(i*512+25,176))
sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-torso-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Chain Mail');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actor=next(a for a in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if a['creature']=='Warden Yrame');resident=actor['native_instances'][0];binding=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Chain Mail')
refs=[]
for f in FACES:
 p=MOD/f'Textures/Things/Apparel/Chainmail/Chainmail_Female_{f}.png';refs.append(dict(file=str(p),sha256=sha(p),facing=f,mod='Vanilla Armour Expanded',workshop_id='1814988282',about_sha256=sha(MOD/'About/About.xml'),role='Actual directional mail asset: linked loops, neutral metal highlights and cardinal silhouette. Tall neck/sleeveless cut are not copied onto the Qud interpretation.'))
write(HERE/'source-packet.json',dict(entry='FIT-YRAME-CHAIN-MAIL-BODY-0',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Warden Yrame',race='Human; ordinary female baseline; named morphology/mutations separate',item=original,actual_binding=binding,captured_resident=resident,body=ref(BODY/'model.json'),donor_references=refs,
 design='A shiny steel linked-loop mail shirt with short sleeves, plain round neckline and thigh-length hem. Broad upper body and highlighted sleeve/hem regions follow the Qud glyph. No padded plates, hood, belt, straps, coat lining or other equipment. Sleeve length/hem contour are authored interpretations of the sparse source.',
 palette=dict(foreground='y',detail='Y',detail_assignment='Highlighted linked-ring zones at sleeve ends and lower hem, following original detail regions. These are metal highlights, not contrasting cloth trim.'),
 frame=dict(canvas=[512,1024],contact=[256,950],camera='Strict front/south, right profile/east, straight back/north; west mirrors east',torso_zoom_crop=[64,190,448,750],torso_zoom_size=[461,672],torso_zoom_origin=[25,176]),
 mutations='Actual ordinary Body287/0 is not mutation-managed. Yrame horns, extra feet, altered limb topology and Big named silhouette remain on BODY-YRAME/NPC-WARDEN-YRAME; this garment authoring fit does not complete them.',native_acceptance='Pending full-set generation gate'))
plate=Image.new('RGB',(1536,1080),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);d.text((24,18),'YRAME > ORDINARY HUMAN BASE > CHAIN MAIL / source, actual mod and own construction',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);plate.paste(orig,(24,95),orig)
for y,t in [(355,'Qud original tile / normalized colors'),(385,'Shiny linked loops; reclaimed steel'),(415,'Actual Body287 / item574 / laterality0'),(445,'Native y primary / Y bright detail'),(475,'No plates, hood, belt or named mutations')]:d.text((24,y),t,font=font,fill='#e5e8d8')
for i,(f,r) in enumerate(zip(FACES,refs)):
 im=Image.open(r['file']).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();im=im.crop(box);im.thumbnail((240,240));plate.paste(im,(535+i*330,100),im);d.text((535+i*330,365),'MOD MAIL / '+f.upper(),font=font,fill='#e3cf43')
 im=neutral.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,440));d.text((535+i*330,980),'CONSTRUCTED / '+f.upper(),font=font,fill='#e3cf43')
d.text((24,1025),'Manual Qud mail interpretation; one item on original ordinary body. Extra feet/horns and actual native acceptance remain pending.',font=font,fill='#e5e8d8');plate.save(HERE/'source-comparison.png')
print('Prepared source-bound chain mail, actual mod SEN references, shared cuff geometry and fixed original body.')
