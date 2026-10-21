"""Construct a source-bound mail shirt on the selected Yrame centauroid.

The long front and short dorsal hem are an authored garment adaptation, not a
native anatomical fact or a new barding item. Full metal and late body masks
remain separate. Review the resulting facings before contextual refinement.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import io
import json
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SIZE=(768,1152)
FACES=['south','east','north']


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def write(name,v):
    (HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


def svg(s):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="768" height="1152" viewBox="0 0 768 1152">'+s+'</svg>'


def raster(s):
    return Image.open(io.BytesIO(svg_to_bytes(svg_string=s))).convert('RGBA')


assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json')
assert ledger['active_entry']=='FIT-YRAME-CHAIN-MAIL-BODY-0'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
be=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME')
assert be['generation_ready']
bref=be['current_registration']['model'];assert ref(ROOT/bref['path'])==bref
body=read(ROOT/bref['path'])
previous=read(HERE.parent/'v1/source-packet.json')
for donor in previous['donor_references']:
    assert hashlib.sha256(Path(donor['file']).read_bytes()).hexdigest()==donor['sha256']
glyph=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/chain-mail-reference.png')
assert hashlib.sha256(glyph.read_bytes()).hexdigest()==previous['item']['reference_sha256']
now=datetime.now(timezone.utc).isoformat()
paths=dict(
 south='M348 286 Q384 318 420 286 L448 299 Q484 302 500 340 L537 420 Q508 451 468 432 L455 403 Q450 462 488 510 L556 625 Q384 660 212 625 L280 510 Q318 462 313 403 L300 432 Q262 451 231 420 L266 340 Q281 302 320 299Z',
 east='M473 293 Q501 298 524 310 Q545 345 571 366 Q610 385 601 419 L595 465 Q604 510 615 545 L629 630 Q571 655 519 631 Q472 593 416 552 Q403 540 419 511 Q445 488 450 458 Q449 420 439 387 Q426 343 449 314Z',
 north='M351 300 Q384 321 417 300 L445 315 Q483 316 499 352 L531 431 Q506 456 467 441 L454 411 Q448 472 484 513 L507 552 Q384 574 261 552 L283 513 Q320 472 313 411 L300 441 Q262 456 235 431 L268 352 Q283 316 323 315Z')
seams=dict(
 south='M348 286 Q384 318 420 286 M313 403 Q302 377 300 341 M455 403 Q466 377 468 341 M231 420 Q262 451 300 432 M468 432 Q508 451 537 420 M220 623 Q384 652 548 623',
 east='M473 293 Q501 300 524 310 M475 328 Q454 353 459 388 L465 430 Q491 453 525 440 L521 369 M465 430 Q491 453 525 440 M420 549 Q474 588 523 627 Q571 650 623 628',
 north='M351 300 Q384 321 417 300 M313 411 Q302 386 300 351 M454 411 Q466 386 467 351 M235 431 Q262 456 300 441 M467 441 Q506 456 531 431 M269 550 Q384 568 499 550')
mask_paths=dict(
 south='M228 416 Q262 451 304 430 L288 474 L273 507 L254 536 Q247 545 245 560 Q249 589 222 598 Q194 606 178 581 Q163 552 189 535 L208 497 L219 462Z M464 430 Q508 451 541 416 L549 462 L562 497 L579 535 Q605 552 590 581 Q574 606 546 598 Q519 589 523 560 Q521 545 514 536 L495 507 L480 474Z',
 east='M463 426 Q491 453 527 439 L536 508 L546 550 Q561 555 567 574 Q577 599 552 616 Q524 632 501 613 Q478 596 491 572 Q496 561 500 555 L483 511 L468 478Z',
 north='M231 427 Q262 456 304 440 L294 478 L278 513 L260 542 L248 566 Q249 586 237 601 Q220 622 195 610 Q168 596 180 573 Q187 559 201 555 L214 516 L223 477Z M463 440 Q506 456 535 427 L544 477 L554 516 L567 555 Q581 559 588 573 Q600 596 573 610 Q548 622 531 601 Q519 586 520 566 L508 542 L490 513 L474 478Z')
detail_paths=dict(
 south='M220 402 Q262 435 310 418 L312 450 Q260 472 214 432Z M458 418 Q506 435 548 402 L554 432 Q508 472 456 450Z M202 594 Q384 630 566 594 L573 680 L195 680Z',
 east='M454 414 Q491 437 537 425 L540 456 Q492 470 457 447Z M403 524 Q472 570 529 611 Q571 636 641 610 L646 673 L507 674 L392 568Z',
 north='M222 415 Q263 442 310 428 L312 459 Q261 480 218 446Z M458 428 Q507 442 543 415 L548 446 Q508 480 455 459Z M250 524 Q384 549 518 524 L525 596 L242 596Z')
contracts=dict(
 south=dict(attachment='Plain round neckline around base of the original neck, endpoints348/420 at y286. Connected shoulder coverage follows the upper torso; short sleeves wrap the upper arms.',
            openings='Left cuff231,420 to300,432 and right468,432 to537,420 use smooth transverse curves. Entire original forearms and hands show below the cuff lips.',
            coverage='Mail covers chest, waist and the front forequarter surface, flaring to a long front hem around y625..643. Head/neck opening, lower legs and hooves remain exposed.',
            depth='Original body/head, intact full mail, then original exposed arms/hands selected by the curved body-class mask. Shirt owns shoulder coverage; it cannot contain red mannequin contours.'),
 east=dict(attachment='Same neck/shoulder fit in full right profile. The near upper-arm sleeve ends at curved mouth465,430 to525,440; original arm lies in front of the torso.',
           openings='Restore the actual forearm/hand only, bounded by its source outlines, below the curved sleeve lip. Keep mail sleeve rim visible; do not restore a torso strip beside the arm.',
           coverage='Short dorsal hem meets the upright-torso/animal-back junction near416,552. The same mail continues downward over the front chest to629,630; no new blanket over the hindquarters.',
           depth='Full mail is continuous behind the near arm. Original body visibility is applied last, with a curved cuff and semantic arm boundaries. Rear fleece and all lower legs stay exposed.'),
 north=dict(attachment='Round back neckline351/417 at y300, continuous shoulders and the same two short sleeves.',
            openings='Back-view cuff lips235,431 to300,441 and467,441 to531,431. Original complete forearms/hands emerge below them.',
            coverage='Mail covers upright back and ends in a short curved dorsal hem around552..563, where the upper torso joins the animal back. Rear fleece remains visible; no human skirt or new barding item.',
            depth='Original body/head, intact mail and bright metal zones, then original exposed arm/hand mask. No missing shoulder patches or baked anatomy contours.'),
 west=dict(attachment='Mirror the exact east garment/body/mask together; plain source mail has no laterality-specific ornament.',
           openings='Mirrored curved sleeve opening and original foreground arm ownership.',
           coverage='Same long anterior drop and short dorsal hem in body-relative coordinates.',
           depth='Same late body visibility as east; actual Body287/0 item binding stays unchanged.'))
contract=dict(entry=entry['id'],recorded_at=now,status='PLANNED — visual comparison pending',body=bref,
              item_source=ref(HERE.parent/'v1/source-packet.json'),frame=body['registration'],
              native_facts='Chain Mail574, Body287/0. Shiny mesh of linked loops sourced from reclaimed steel. Native y primary/Y bright detail. No native tailoring coordinates exported.',
              authored_estimates='Short sleeves, round neck, long front drop and short dorsal hem adapt the existing shirt interpretation to the selected centauroid. This is one mail shirt, not a newly inferred barding blueprint.',
              views=contracts,garment_paths=paths,cuff_seams=seams,body_visibility_paths=mask_paths,
              fit='Construct directly at selected body landmarks; any subsequent deformation must retain full continuous mail and use the minimum needed regional adjustment.',
              gate='Review each actual facing against the recorded coverage and openings before refinement and before extraction. Native validation remains behind the all-generation gate.')
write('fit-contract.json',contract)
packet=dict(entry=entry['id'],workflow='regional-curved-v1',recorded_at=now,creature='Warden Yrame',
            race='Human-based named mutant; selected compact sheep-like centauroid variant, separate from reusable ordinary human body.',
            item=previous['item'],actual_binding=previous['actual_binding'],body=bref,frame=body['registration'],
            previous_superseded_source=ref(HERE.parent/'v1/source-packet.json'),donor_references=previous['donor_references'],
            fit_contract=ref(HERE/'fit-contract.json'),palette=previous['palette'],
            design='One connected linked-steel short-sleeve mail shirt. Round natural neckline, longer front forequarter drop and short dorsal hem at the animal-back junction. No belt, hood, plates, rear blanket, horns or weapon in the primary preview.',
            native_acceptance='Pending full-set generation gate, actual equipped-state and complete named outfit.')
write('source-packet.json',packet)

for facing in FACES:
    base=Image.new('RGBA',SIZE)
    for row in sorted(body['views'][facing],key=lambda r:r['layer']):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        base.alpha_composite(Image.open(ROOT/row['public_file']).convert('RGBA'))
    assert np.array_equal(np.array(base),np.array(Image.open(HERE/f'original-body-{facing}.png').convert('RGBA')))
    defs='<defs><pattern id="rings" width="16" height="12" patternUnits="userSpaceOnUse"><rect width="16" height="12" fill="#c6c6c6"/><g fill="none" stroke="#929292" stroke-width="1.2"><ellipse cx="4" cy="2" rx="4.7" ry="3"/><ellipse cx="12" cy="8" rx="4.7" ry="3"/></g></pattern></defs>'
    content=defs+f'<path d="{paths[facing]}" fill="url(#rings)" stroke="#262626" stroke-width="5" stroke-linejoin="round"/><path d="{seams[facing]}" fill="none" stroke="#343434" stroke-width="3.5" stroke-linecap="round"/>'
    source=svg(content);(HERE/f'pattern-{facing}.svg').write_bytes(source.encode())
    cloth=raster(source);cloth.save(HERE/f'constructed-cloth-{facing}.png')
    mask_source=svg(f'<path d="{mask_paths[facing]}" fill="white"/>')
    (HERE/f'body-visibility-{facing}.svg').write_bytes(mask_source.encode())
    ma=np.array(raster(mask_source).getchannel('A'))
    ba=np.array(base)
    if facing=='east':
        # Explicit near-arm region: the body outline at the back and the torso
        # to the right are not part of this foreground limb.
        for y in range(439,557):
            dark=(ba[y,:,:3].mean(1)<85)&(ba[y,:,3]>128)
            right=np.flatnonzero(dark[510:552])+510
            if len(right):
                start=int(right[0]); end=start
                while end<551 and dark[end]:end+=1
                ma[y,end+1:]=0
            expected=np.interp(y,[439,475,500,525,550,556],[472,474,483,494,505,506])
            low,high=int(expected)-8,int(expected)+8
            left=np.flatnonzero(dark[low:high])+low
            if len(left):ma[y,:int(left[0])]=0
    ma[ba[:,:,3]==0]=0
    Image.fromarray(ma).save(HERE/f'body-visibility-{facing}.png')
    detail=raster(svg(f'<path d="{detail_paths[facing]}" fill="white"/>')).getchannel('A')
    detail.save(HERE/f'detail-region-{facing}.png')
    red=ba.copy();lum=ba[:,:,:3].mean(2)
    red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
    for name,im in [('constructed-neutral',base),('constructed-red',Image.fromarray(red))]:
        with_cloth=Image.alpha_composite(im,cloth)
        result=Image.composite(im,with_cloth,Image.fromarray(ma))
        result.save(HERE/f'{name}-{facing}.png')

font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
# One common crop/scale: do not normalize the enlarged side silhouette to fit a
# narrow portrait panel. It includes the naked rear back for coverage context.
boxes=dict(south=[144,240,624,720],east=[144,240,624,720],north=[144,240,624,720])
for prefix,name in [('constructed-red','manual-context-turnaround.png'),('constructed-neutral','manual-neutral-turnaround.png')]:
    sheet=Image.new('RGBA',(1440,540));d=ImageDraw.Draw(sheet)
    for i,facing in enumerate(FACES):
        sheet.alpha_composite(Image.open(HERE/f'{prefix}-{facing}.png').convert('RGBA').crop(boxes[facing]),(i*480,0))
        d.text((i*480+15,510),facing.upper(),font=font,fill='white')
    sheet.save(HERE/name)
write('context-crops.json',dict(canvas=list(SIZE),sheet=[1440,540],view_boxes=boxes,policy='Same480px square physical crop per view, at original scale. Transparent margins and the same body contact are retained in production.'))
plate=Image.new('RGB',(1440,900),'#142823');d=ImageDraw.Draw(plate)
d.text((20,15),'YRAME / CHAIN MAIL574 / original glyph + actual directional VAE mail + constructed centauroid fit',font=font,fill='#e3cf43')
im=Image.open(glyph).convert('RGBA').resize((96,144),Image.Resampling.NEAREST);plate.paste(im,(40,70),im)
for i,donor in enumerate(previous['donor_references']):
    im=Image.open(donor['file']).convert('RGBA');im.thumbnail((220,220));plate.paste(im,(265+i*370,55),im)
    d.text((265+i*370,285),donor['facing'].upper()+' / VAE',font=font,fill='#e3cf43')
d.text((20,335),'Native: linked steel, y/Y; authored: round neck, short sleeves, long anterior drop, short dorsal hem.',font=font,fill='#e5e8d8')
context=Image.open(HERE/'manual-neutral-turnaround.png').convert('RGBA')
plate.paste(context,(0,360),context);plate.save(HERE/'source-reference-construction.png')
for step,phase,names,review in [
 ('source_identity_description_slot_laterality','Current-body mail source and actual Body287/0 binding',['source-packet.json','fit-contract.json'],'Source item574 identity and y/Y linked-steel roles retained; named body selection explicitly replaces old ordinary-human fitting.'),
 ('select_correct_body_and_references','Current selected centauroid and actual directional mail references',['bare-body-landmark-review.png','source-reference-construction.png'],'Current body and private donor reference hashes verified. Source cut is interpreted, not recovered tailoring metadata.'),
 ('construct_and_overlay_one_item','Continuous centauroid shirt and curved body-class visibility — review pending',['construct-mail.py','manual-neutral-turnaround.png','manual-context-turnaround.png','context-crops.json'],'Per-view coverage/openings contract recorded before drawing. Full mail and late semantic curved masks retained independently; manual review pending.')]:
    entry['process_log'].append(dict(timestamp=now,step=step,phase=phase,action=review,inputs=[bref,ref(HERE.parent/'v1/source-packet.json')],outputs=[ref(HERE/n) for n in names],review=review,result='REQUIRES REVIEW' if step.startswith('construct') else 'PASS'))
entry['current_step']='construct_and_overlay_one_item'
entry['apparel_workflow']['status']='IN PROGRESS'
ledger['updated_at']=now
(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Defined centauroid shirt fit before construction; manual full-mail and curved-mask review pending.')
