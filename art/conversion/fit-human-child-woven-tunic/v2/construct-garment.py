"""Reconstruct continuous shoulders on the unchanged registered child frame."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-child/v1'
DONOR=Path('D:/Steam/steamapps/workshop/content/294100/2016436324')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
front='''<path d="M218 410 Q256 432 294 410 Q330 413 356 439 L404 541 L365 563 L335 500 L343 744 Q256 760 169 744 L177 500 L147 563 L106 541 L154 439 Q184 413 218 410Z"/>
<path d="M188 610 Q256 624 325 610 M188 618 Q256 632 325 618" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M286 616 Q305 601 307 616 Q302 629 286 616 M291 621 L284 651 M299 621 L311 648" fill="none" stroke="#626962" stroke-width="4"/>
<path d="M200 458 L213 592 M313 458 L299 592 M209 645 L197 733 M305 645 L316 733" fill="none" stroke="#a5ada4" stroke-width="4"/>'''
back=front[:front.index('<path d="M286')]+'''<path d="M211 441 Q256 455 301 441 M209 645 L197 733 M305 645 L316 733" fill="none" stroke="#a5ada4" stroke-width="4"/>'''
side='''<path d="M244 410 L303 420 Q342 441 352 492 L376 619 L371 744 Q286 759 198 744 L204 619 L201 489 Q203 441 244 410Z"/>
<path d="M241 435 Q272 431 298 459 L322 543 L284 560 L261 510 L226 488Z"/>
<path d="M206 615 Q288 631 372 620 M206 623 Q288 639 372 628" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M222 650 L212 735 M351 651 L359 735" fill="none" stroke="#a5ada4" stroke-width="4"/>'''
# Actual painted near-arm contour below the cuff; no detached hand-circle punch.
# Keep this separate from the intact garment. It is a flat-layer ownership mask.
side_arm='''<path d="M225 548 Q229 578 243 612 L255 645 C244 656 246 676 261 685 C274 695 294 690 303 676 C315 658 304 644 294 639 L295 607 Q289 580 286 551Z"/>'''
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
sheet=Image.new('RGBA',(1536,1088));isolated=Image.new('RGBA',sheet.size)
for i,(facing,shapes) in enumerate([('south',front),('east',side),('north',back)]):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g fill="#c8cdc2" stroke="#343c35" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'+shapes+'</g></svg>'
    path=HERE/f'constructed-{facing}.svg';path.write_bytes(svg.encode())
    (HERE/f'constructed-{facing}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(path),skip_system_fonts=True))
    garment=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA')
    intact=garment.copy();intact.save(HERE/f'constructed-intact-{facing}.png')
    if facing=='east':
        masksvg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g fill="white">'+side_arm+'</g></svg>'
        (HERE/'near-arm-ownership.svg').write_bytes(masksvg.encode())
        (HERE/'near-arm-ownership.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'near-arm-ownership.svg'),skip_system_fonts=True))
        cut=Image.open(HERE/'near-arm-ownership.png').getchannel('A')
        garment.paste((0,0,0,0),mask=cut)
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA');head=Image.open(BODY/f'head-{facing}.png').convert('RGBA')
    # The collar owns its own edge over the neck; do not expose the head layer's
    # rectangular extraction boundary through an otherwise continuous shirt.
    composed=Image.alpha_composite(Image.alpha_composite(body,head),garment)
    composed.save(HERE/f'constructed-fit-{facing}.png')
    sheet.alpha_composite(composed,(i*512,0));isolated.alpha_composite(intact,(i*512,0))
    for im in [sheet,isolated]:ImageDraw.Draw(im).text((i*512+105,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
sheet.save(HERE/'constructed-fit-comparison.png');isolated.save(HERE/'constructed-intact-comparison.png')
packet=json.loads((HERE.parent/'v1/source-packet.json').read_text(encoding='utf-8'))
packet['correction']='Continuous covered shoulders; intact garment art distinct from precise flat-layer near-arm ownership. Fixed body/frame unchanged.'
packet['body_sha256']=sha(BODY/'model.json')
packet['donor_reference']={'package':'Vanilla Textures Expanded','about':str(DONOR/'About/About.xml'),'about_sha256':sha(DONOR/'About/About.xml'),'assets':[],'role':'Actual child apparel cardinal shading, compact material read and separate-layer convention only. It is sleeveless; it does not govern Qud tunic sleeve coverage.'}
plate=Image.new('RGB',(1050,420),'#142823');d=ImageDraw.Draw(plate)
d.text((20,15),'SOURCE / Woven Tunic: coarse flax, watervine hemp waist rope',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    p=DONOR/f'Textures/Things/Pawn/Humanlike/Apparel/KidShirt/KidShirt_Child_{f}.png'
    packet['donor_reference']['assets'].append({'path':str(p),'sha256':sha(p)})
    im=Image.open(p).convert('RGBA');plate.paste(im,(i*340+40,70),im)
    d.text((i*340+30,340),'VTE child shirt / '+f,font=font,fill='#e5e8d8')
d.text((20,385),'Reference role: cardinal material/outline; not Qud clothing identity.',font=font,fill='#e5e8d8')
plate.save(HERE/'reference-comparison.png')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
