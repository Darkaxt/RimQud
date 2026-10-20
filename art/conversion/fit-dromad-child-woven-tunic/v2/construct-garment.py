"""Editable tunic pattern around the unchanged juvenile dromad neck/hump."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageChops
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-dromad-child/v1'
front='''<path d="M202 574 Q179 582 170 616 Q166 636 151 650 Q121 674 105 739 L150 761 L170 720 L162 868 Q256 888 350 868 L342 720 L364 761 L407 739 Q392 674 361 650 Q345 636 340 616 Q331 582 312 574 L310 635 Q308 663 257 665 Q210 663 207 635Z"/>
<path d="M167 807 Q256 823 347 807 M166 815 Q256 831 348 815" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M294 815 Q314 802 315 815 Q312 827 294 815 M298 819 L292 850 M306 821 L318 847" fill="none" stroke="#626962" stroke-width="4"/>
<path d="M187 688 L194 789 M324 688 L317 789 M198 834 L190 862 M313 834 L322 862" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
back='''<path d="M201 567 Q256 545 311 567 Q334 581 340 616 Q345 636 361 650 Q392 674 407 739 L364 761 L342 720 L350 868 Q256 888 162 868 L170 720 L150 761 L105 739 Q121 674 151 650 Q166 636 170 616 Q177 582 201 567Z"/>
<path d="M201 571 Q256 591 311 571 M167 807 Q256 823 347 807 M166 815 Q256 831 348 815" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M187 688 L194 789 M324 688 L317 789 M198 834 L190 862 M313 834 L322 862" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
side='''<path d="M258 550 Q236 534 208 550 Q174 566 168 605 Q166 625 149 646 Q120 686 127 734 Q133 778 156 818 L164 873 Q270 895 365 873 L356 824 Q388 780 376 727 Q367 687 353 674 Q305 663 280 635 Q263 603 258 550Z"/>
<path d="M254 650 Q224 670 211 703 L209 735 Q235 749 271 748 L284 705 Q280 674 254 650Z"/>
<path d="M151 803 Q252 835 367 809 M153 811 Q252 843 365 817" fill="none" stroke="#626962" stroke-width="5"/>
<path d="M180 837 L176 866 M340 838 L347 866" fill="none" stroke="#a7afa6" stroke-width="4"/>'''
arm='M211 739 Q242 752 284 740 L278 772 C293 782 293 804 278 817 C264 831 242 824 231 812 C217 799 220 783 228 773 Q213 761 211 739Z'
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+arm+'"/></svg>'
(HERE/'near-arm-ownership.svg').write_bytes(svg.encode());(HERE/'near-arm-ownership.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'near-arm-ownership.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20);sheet=Image.new('RGBA',(1536,1088));isolated=Image.new('RGBA',sheet.size)
for i,(facing,shape) in enumerate([('south',front),('east',side),('north',back)]):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g fill="#c8cdc2" stroke="#343c35" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'+shape+'</g></svg>'
    (HERE/f'constructed-{facing}.svg').write_bytes(svg.encode());(HERE/f'constructed-{facing}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{facing}.svg'),skip_system_fonts=True))
    cloth=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA');isolated.alpha_composite(cloth,(i*512,0))
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA');head=Image.open(BODY/f'head-{facing}.png').convert('RGBA');body=Image.alpha_composite(body,head)
    detail=BODY/f'head-detail-{facing}.png'
    if detail.exists():body=Image.alpha_composite(body,Image.open(detail).convert('RGBA'))
    if facing=='east':
        cut=ImageChops.multiply(Image.open(HERE/'near-arm-ownership.png').getchannel('A'),body.getchannel('A'));cloth.putalpha(ImageChops.subtract(cloth.getchannel('A'),cut))
    fit=Image.alpha_composite(body,cloth);fit.save(HERE/f'constructed-fit-{facing}.png');sheet.alpha_composite(fit,(i*512,0))
    for p in [sheet,isolated]:ImageDraw.Draw(p).text((i*512+100,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
sheet.save(HERE/'constructed-fit-comparison.png');isolated.save(HERE/'constructed-intact-comparison.png')
packet=json.loads((HERE.parent/'v1/source-packet.json').read_text(encoding='utf-8'))
hp=ROOT/'art/conversion/fit-human-child-woven-tunic/v2/source-packet.json'
packet['donor_reference']=json.loads(hp.read_text(encoding='utf-8'))['donor_reference']
packet['garment_style_reference']={'path':'art/conversion/fit-human-child-woven-tunic/v2/registered-isolated-comparison.png','sha256':hashlib.sha256((ROOT/'art/conversion/fit-human-child-woven-tunic/v2/registered-isolated-comparison.png').read_bytes()).hexdigest()}
packet['correction']='Explicit long-neck collar and hump pattern, not blanket head-alpha subtraction. Separate intact garment and local body-owned arm overlap. No anatomy or frame changes.'
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
