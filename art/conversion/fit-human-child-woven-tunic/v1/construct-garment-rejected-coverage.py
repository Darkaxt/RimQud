"""Construct one source-bound Woven Tunic over the fixed child mannequin."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-child/v1'
front='''<path fill-rule="evenodd" d="M218 426 Q256 416 294 426 Q324 427 350 453 L389 548 L351 568 L327 513 L335 744 Q256 760 177 744 L185 513 L161 568 L123 548 L162 453 Q188 427 218 426Z M218 408 L294 408 L294 426 Q256 450 218 426Z"/>
<path d="M188 609 Q256 619 326 609 M188 617 Q256 627 326 617" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M287 613 Q306 600 307 614 Q305 627 287 613 M291 617 L285 650 M299 619 L310 646" fill="none" stroke="#626962" stroke-width="4"/>
<path d="M205 463 L214 591 M307 463 L299 591 M211 641 L204 735 M305 641 L311 735" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
back=front[:front.index('<path d="M287')]+'''<path d="M210 455 Q256 472 302 455 M209 641 L204 735 M303 641 L309 735" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
side='''<path fill-rule="evenodd" d="M248 427 L300 438 Q333 462 340 499 L361 621 L360 744 Q285 756 207 744 L212 623 L217 486 Q218 451 248 427Z M245 404 L302 415 L300 438 Q269 443 248 427Z"/>
<path d="M255 454 Q283 445 304 465 L329 550 L294 568 L267 519 L249 495Z"/>
<path d="M216 614 Q285 631 357 620 M216 622 Q285 639 357 628" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M227 649 L220 736 M342 651 L347 737" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
sheet=Image.new('RGBA',(1536,1088));isolated=Image.new('RGBA',(1536,1088))
for index,(facing,shapes) in enumerate([('south',front),('east',side),('north',back)]):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g fill="#c8cdc2" stroke="#343c35" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'+shapes+'</g></svg>'
    (HERE/f'constructed-{facing}.svg').write_bytes(svg.encode())
    (HERE/f'constructed-{facing}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{facing}.svg'),skip_system_fonts=True))
    garment=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA')
    body=Image.open(BODY/f'selected-{facing}.png').convert('RGBA')
    composed=Image.alpha_composite(body,garment);composed.save(HERE/f'constructed-fit-{facing}.png')
    sheet.alpha_composite(composed,(index*512,0));isolated.alpha_composite(garment,(index*512,0))
    for image in [sheet,isolated]:ImageDraw.Draw(image).text((index*512+125,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
sheet.save(HERE/'constructed-fit-comparison.png');isolated.save(HERE/'constructed-isolated-comparison.png')
