"""One editable Woven Tunic fitting over the fixed child-dromad body."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad-child/v1'
front='''<path d="M205 574 Q171 573 167 605 Q165 623 173 640 Q134 656 118 695 L105 738 L150 761 L170 721 L162 868 Q256 888 350 868 L342 721 L364 761 L407 738 Q390 670 354 646 Q337 633 329 607 Q322 580 307 576Z"/>
<path d="M167 807 Q256 823 347 807 M166 815 Q256 831 348 815" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M294 815 Q314 802 315 815 Q312 827 294 815 M298 819 L292 850 M306 821 L318 847" fill="none" stroke="#626962" stroke-width="4"/>
<path d="M187 688 L194 789 M324 688 L317 789 M198 834 L190 862 M313 834 L322 862" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
back='''<path d="M256 559 Q196 550 177 604 Q172 630 153 649 Q129 673 118 695 L105 738 L150 761 L170 721 L162 868 Q256 888 350 868 L342 721 L364 761 L407 738 Q390 670 359 649 Q340 630 335 604 Q316 550 256 559Z"/>
<path d="M167 807 Q256 823 347 807 M166 815 Q256 831 348 815" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M187 688 L194 789 M324 688 L317 789 M198 834 L190 862 M313 834 L322 862" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
side='''<path d="M254 650 Q239 600 228 572 Q211 534 182 553 Q166 568 166 603 Q162 625 148 644 Q122 686 127 734 Q133 778 156 818 L164 873 Q270 895 365 873 L356 824 Q388 780 376 727 Q369 695 353 673Z"/>
<path d="M257 646 Q231 660 218 704 L218 730 L269 742 L282 701 Q279 675 278 666Z"/>
<path d="M151 803 Q252 835 367 809 M153 811 Q252 843 365 817" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M180 837 L176 866 M340 838 L347 866" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
sheet=Image.new('RGBA',(1536,1088));isolated=Image.new('RGBA',(1536,1088));font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
for index,(facing,shapes) in enumerate([('south',front),('east',side),('north',back)]):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g fill="#c8cdc2" stroke="#343c35" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'+shapes+'</g></svg>'
    (HERE/f'constructed-{facing}.svg').write_bytes(svg.encode());(HERE/f'constructed-{facing}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{facing}.svg'),skip_system_fonts=True))
    garment=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA')
    head_mask=Image.open(BODY/f'head-mask-{facing}.png').convert('L');garment.putalpha(ImageChops.multiply(garment.getchannel('A'),ImageChops.invert(head_mask)))
    cut=Image.new('L',garment.size)
    if facing=='east':
        draw=ImageDraw.Draw(cut);draw.polygon([(218,730),(269,742),(277,772),(281,785),(276,809),(253,824),(232,813),(223,793),(225,774),(219,758)],fill=255)
        draw.ellipse((224,764,288,828),fill=255);garment.paste((0,0,0,0),mask=cut)
    cut.save(HERE/f'constructed-arm-cut-{facing}.png');garment.save(HERE/f'constructed-{facing}.png')
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA');head=Image.open(BODY/f'head-{facing}.png').convert('RGBA')
    composed=Image.alpha_composite(Image.alpha_composite(body,garment),head);composed.save(HERE/f'constructed-fit-{facing}.png')
    sheet.alpha_composite(composed,(index*512,0));isolated.alpha_composite(garment,(index*512,0))
    for image in [sheet,isolated]:ImageDraw.Draw(image).text((index*512+125,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
sheet.save(HERE/'constructed-fit-comparison.png');isolated.save(HERE/'constructed-isolated-comparison.png')
