"""Construct one neutral south-facing normal catfish before asking for other views."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'front-controls.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='BODY-GLOWFISH';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
fins='''<g id="detail-fins" stroke="#363b3a" stroke-width="5" stroke-linejoin="round">
<path id="right-fin" d="M342 486 Q300 481 264 459 Q249 443 281 444 Q324 447 351 465Z" fill="#b0b0b0"/>
<path id="left-fin" d="M427 486 Q468 482 504 461 Q521 445 489 446 Q446 447 420 465Z" fill="#b0b0b0"/>
<path id="dorsal-fin" d="M354 444 Q320 411 324 362 Q344 381 363 372 Q382 385 379 417Z" fill="#a7a7a7"/>
<path id="tail-fin" d="M507 473 Q477 503 446 491 Q460 471 446 440 Q471 432 487 450Z" fill="#b6b6b6"/>
<path d="M269 452L329 475 M499 454L438 475 M336 380L362 420 M457 450L493 465 M456 483L493 465" fill="none" stroke="#8b9090" stroke-width="2.5"/>
</g>'''
body='''<g id="primary-body" stroke-linejoin="round" stroke-linecap="round">
<path d="M310 553 C304 510 333 488 345 450 C350 398 352 337 406 300 C460 257 535 281 558 330 C583 383 563 450 510 477 L482 449 C527 427 542 381 520 347 C500 317 462 321 443 350 C418 384 427 427 432 465 C438 493 468 515 461 551 C455 589 420 616 384 619 C348 615 317 590 310 553Z" fill="#cccccc" stroke="#353a39" stroke-width="6"/>
<path d="M325 548 C328 519 350 507 363 469 C378 423 365 359 414 323 C450 296 504 300 529 331" fill="none" stroke="#e5e5e5" stroke-width="13"/>
<path d="M452 523 Q445 578 399 600 Q431 574 432 542" fill="#adadad" stroke="none"/>
<path d="M327 573 Q312 551 324 533 M447 573 Q461 551 450 533" fill="none" stroke="#969c9b" stroke-width="3.5"/>
<ellipse cx="334" cy="548" rx="7" ry="8" fill="#292e2d"/><ellipse cx="434" cy="548" rx="7" ry="8" fill="#292e2d"/>
<path d="M337 591 Q384 608 432 591" fill="none" stroke="#4a504e" stroke-width="4"/>
<path d="M316 570 Q271 582 263 620 M453 570 Q496 581 505 620 M355 607 Q339 633 322 636 M413 607 Q430 633 446 636" fill="none" stroke="#343a38" stroke-width="7"/>
<path d="M316 570 Q271 582 263 620 M453 570 Q496 581 505 620 M355 607 Q339 633 322 636 M413 607 Q430 633 446 636" fill="none" stroke="#cccccc" stroke-width="3.5"/>
</g>'''
flecks='''<g id="detail-flecks" fill="#dedede"><circle cx="377" cy="525" r="5"/><circle cx="408" cy="480" r="4"/><circle cx="391" cy="445" r="4"/><circle cx="400" cy="368" r="4"/><circle cx="467" cy="311" r="4"/><circle cx="548" cy="382" r="4"/></g>'''
base='<svg xmlns="http://www.w3.org/2000/svg" width="768" height="768" viewBox="0 0 768 768">{}</svg>'
(HERE/'front-source-fragments.json').write_bytes((json.dumps(dict(fins=fins,body=body,flecks=flecks),indent=2)+'\n').encode())
svg=HERE/'front-south.svg';svg.write_text(base.format(fins+body+flecks),encoding='utf-8');(HERE/'front-south.png').write_bytes(svg_to_bytes(svg_string=svg.read_text()))
controls=dict(source=ref(HERE/'source-packet.json'),svg=ref(svg),front=ref(HERE/'front-south.png'),fragments=ref(HERE/'front-source-fragments.json'),canvas=[768,768],swim_pivot=[384,384],world_canvas=[1.2,1.2],
    facing='SOUTH/front: head and mouth towards lower edge, complete fish behind it in shallow dorsal/cardinal map view matching actual live fish reference.',
    intrinsic_anatomy='One broad flattened catfish head, normal paired barbels, one dorsal fin, one paired lateral-fin set, one tail fin on a long source-curled body. No limbs, clothes, extra mutation appendages or new articulated nodes.',
    interpretation='Source curl retained as a normal fish swimming-plane silhouette, not seahorse identity or extra tail. Exact barbel count(2long+2short), subtle gill slits, depth, fin shape and fleck positions are authored species cues, not Qud part counts.',
    palette='Equal-RGB neutral only. Fins/flecks will use C detail; main fish/ordinary face/barbels use m primary. No baked glow, water colour or fixed magenta/cyan.',
    registration='Trunk/swim pivot fixed at384,384; asymmetric tail may extend. Do not independently center alpha bounds. Whole animal body art with two tint channels; mechanical Head/Fin do not become separate render bones.',native_activation=False)
write(HERE/'front-controls.json',controls)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);im=Image.open(HERE/'front-south.png').convert('RGBA');plate=Image.new('RGB',(1050,850),'#142823');plate.paste(im,(0,35),im);d=ImageDraw.Draw(plate);d.text((20,15),'GLOWFISH / first neutral SOUTH front / ordinary catfish, source curl retained',font=font,fill='#e3cf43');d.line((384,40,384,790),fill='#837c41',width=1);d.line((20,419,748,419),fill='#837c41',width=1)
for i,line in enumerate(['ONE HEAD/FACE','ONE DORSAL FIN','PAIRED LATERAL FINS','ONE TAIL FIN','NO LEGS OR CLOTHES','m/C VIA MASKS LATER','TRUNK PIVOT(384,384)']):d.text((770,200+i*45),line,font=font,fill='#e5e8d8')
d.text((20,812),'Guides are report only. No side/back draft used to define this front. Unseen forms remain authored.',font=font,fill='#e3cf43');plate.save(HERE/'front-manual-suggestion.png')
prompt='''Use case: front-guided cardinal turnaround of normal Qud Glowfish/catfish, neutral game sprites.
IMAGE1 is the selected constructed SOUTH/front: head points down, broad catfish mouth/head, ordinary barbels, paired fins, one dorsal fin, one tail fin and a long curled body matching the Qud silhouette. IMAGE2 supplies exact original Qud mask/palette, runtime Fish metadata context and actual installed live-fish RimWorld S/E/N references plus catfish anatomical resource reference.
Qud species tag is CATFISH; description Luminescent flecks flit beneath the water's surface. Normal Fish body has head/face, back, ONE dorsal fin, paired right/left fins and ONE tail fin. No arms, hands, legs, feet, extra heads/tails or humanoid stance. Native Gills and DarkVision are behavior, not extra external mutation appendages. Keep fish out of clothes and do not add a handheld Bite item.
Generate ONLY two corresponding views alongside each other: EAST whole fish heading RIGHT on the left, NORTH whole fish heading UP on the right. Treat this as a fish swimming in the map plane, following the live fish-pawn cardinal reference; do not turn only the head, stand the fish upright, substitute a human back or show a three-quarter aquarium illustration. Rotate the entire same normal catfish form/curl/fin attachments into the specified facing. Keep the original curling body/tail instead of replacing it with a straight generic baitfish, eel or seahorse.
Use same gray shading, proportions, normal paired mouth barbels and fin count as front. Source cyan/magenta are REFERENCES ONLY: output pure grayscale neutral. Fins and six small fleck marks stay recognizable for separate C detail masking later; no baked cyan/purple, emission, water tint, halo, pool, ground/shadow, bubbles, extra fish, background, text, labels or frame.
Each view corresponds to a768x768common square with fixed trunk/swim pivot(384,384), common physical scale/worldcanvas1.2x1.2; do not crop independently to alpha bounds or resize body by facing. Fish tail may extend asymmetrically while trunk anchor remains fixed. Both objects complete on true transparent background. Quiet clean RimWorld-like outlines and restrained broad shading, not shiny photoreal scales. This generates E/N PROPOSALS from the front; canonical registration/anatomy corrections follow.'''
(HERE/'side-back-prompt.txt').write_text(prompt+'\n',encoding='utf-8');now=datetime.now(timezone.utc).isoformat()
def event(step,action,outs,review):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'source-reference.png')],outputs=[ref(HERE/n) for n in outs],review=review,result='PASS'))
event(entry['required_steps'][1],'Inspect actual Biomes! Islands live-fish S/E/N sprites and separate VFE catfish anatomy reference.',['front-controls.json'],'Live donor supplies whole-fish cardinal map convention and simple animal art, not straight-body identity/mechanics/scale. Catfish resource supplies anatomy only, not a live pose/turnaround. Installed versions and raw references retained with hashes; no mod installation/runtime claim.')
event(entry['required_steps'][2],'Construct a new neutral front first from catfish facts, Fish topology and curled Qud silhouette.',['construct-front.py','front-south.svg','front-south.png','front-manual-suggestion.png','front-source-fragments.json','side-back-prompt.txt'],'One catfish head, dorsal+paired+tail fins, normal barbels/gill cues and a curved swimming body. No old east-first art or fixed palette reused. Fins/flecks are separate authored ownership for later C tint. Common trunk pivot, no independently recentered bounds. Inspect before actual E/N generation.')
entry.update(current_step=entry['required_steps'][3],known_issues=['Neutral front constructed; inspect it and source references, then run actual ImageGen E/N from front and race facts. No generation-ready credit.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Constructed new front-first neutral catfish base and exact side/back generation prompt.')
