"""Place inspected child views on one frame without independent view fitting."""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE=Path(__file__).resolve().parent
source=Image.open(HERE/'secondary-views.png').convert('RGBA')
views=[('south',(90,0,550,1024),(320,990)),('east',(590,0,940,1024),(744,989)),('north',(990,0,1440,1024),(1216,990))]
scale=.79
sheet=Image.new('RGBA',(1536,1088));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
decisions=dict(common_scale=scale,contact=[256,950],views={})
for index,(facing,region,contact) in enumerate(views):
    image=source.crop(region);alpha=image.getchannel('A').point(lambda v:0 if v<16 else (255 if v>=240 else v));gray=ImageOps.grayscale(image)
    image=Image.merge('RGBA',(gray,gray,gray,alpha)).resize((round(image.width*scale),round(image.height*scale)),Image.Resampling.LANCZOS)
    image.paste((0,0,0,0),mask=image.getchannel('A').point(lambda v:255 if v==0 else 0))
    delta=(256-round((contact[0]-region[0])*scale),950-round(contact[1]*scale))
    canvas=Image.new('RGBA',(512,1024));canvas.paste(image,delta);canvas.save(HERE/f'patched-{facing}.png');sheet.alpha_composite(canvas,(index*512,0))
    draw.text((index*512+130,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
    decisions['views'][facing]=dict(region=region,source_contact=contact,translation=delta,bounds=canvas.getchannel('A').getbbox())
sheet.save(HERE/'patched-views.png');(HERE/'patch-decisions.json').write_bytes((json.dumps(decisions,indent=2)+'\n').encode())
