"""Editable plain goat-wool robe, fitted to the existing adult dromad frame."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v1'
front='''<path d="M195 512 Q158 496 149 545 Q145 574 129 593 Q97 628 84 707 L126 737 L154 692 L139 884 Q256 911 371 884 L355 692 L384 737 L429 707 Q415 628 381 593 Q351 574 349 545 Q340 496 309 512Z"/>
<path d="M184 678 L169 865 M328 678 L343 865 M242 686 L235 879 M272 686 L279 879 M146 875 Q256 899 365 875" fill="none" stroke="#a0a39b" stroke-width="4"/>'''
back='''<path d="M256 493 Q181 485 159 548 Q147 579 129 593 Q97 628 84 707 L126 737 L154 692 L139 884 Q256 911 371 884 L355 692 L384 737 L429 707 Q415 628 381 593 Q361 579 353 548 Q331 485 256 493Z"/>
<path d="M184 678 L169 865 M328 678 L343 865 M255 602 L255 881 M146 875 Q256 899 365 875" fill="none" stroke="#a0a39b" stroke-width="4"/>'''
side='''<path d="M272 626 Q263 556 248 516 Q234 474 201 492 Q172 509 173 548 Q169 576 154 597 Q119 655 133 721 Q139 772 166 816 L155 891 Q272 910 390 889 L375 815 Q417 752 398 694 Q388 659 370 641Z"/>
<path d="M254 622 Q224 640 207 698 L211 728 L271 743 L289 692 Q286 655 276 644Z"/>
<path d="M178 821 L171 878 M355 824 L372 877 M161 883 Q270 901 383 881" fill="none" stroke="#a0a39b" stroke-width="4"/>'''
sheet=Image.new('RGBA',(1536,1088));isolated=Image.new('RGBA',sheet.size)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
for i,(facing,shape) in enumerate([('south',front),('east',side),('north',back)]):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g fill="#bfc2b8" stroke="#343b35" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'+shape+'</g></svg>'
    (HERE/f'constructed-{facing}.svg').write_bytes(svg.encode())
    (HERE/f'constructed-{facing}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{facing}.svg'),skip_system_fonts=True))
    garment=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA')
    cut=Image.open(BODY/f'head-{facing}.png').getchannel('A')
    if facing=='east':
        arm=Image.new('L',garment.size);d=ImageDraw.Draw(arm)
        d.polygon([(213,722),(276,736),(283,761),(285,790),(271,810),(244,815),(224,797),(221,771)],fill=255)
        d.ellipse((220,745,291,816),fill=255);cut=ImageChops.lighter(cut,arm)
    cut.save(HERE/f'constructed-cut-{facing}.png')
    garment.putalpha(ImageChops.multiply(garment.getchannel('A'),ImageChops.invert(cut)))
    garment.paste((0,0,0,0),mask=garment.getchannel('A').point(lambda v:255 if v==0 else 0));garment.save(HERE/f'constructed-{facing}.png')
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA');head=Image.open(BODY/f'head-{facing}.png').convert('RGBA')
    composed=Image.alpha_composite(Image.alpha_composite(body,garment),head);composed.save(HERE/f'constructed-fit-{facing}.png')
    sheet.alpha_composite(composed,(i*512,0));isolated.alpha_composite(garment,(i*512,0))
    for im in [sheet,isolated]:ImageDraw.Draw(im).text((i*512+110,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
sheet.save(HERE/'constructed-fit-comparison.png');isolated.save(HERE/'constructed-isolated-comparison.png')
