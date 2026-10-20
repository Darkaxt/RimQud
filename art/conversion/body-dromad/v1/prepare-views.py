"""Place inspected complete dromad figures on a common centered frame."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops

HERE=Path(__file__).resolve().parent
source=Image.open(HERE/'secondary-views.png').convert('RGBA')
views=[('south',(285,680),(285,990)),('east',(780,680),(744,994)),('north',(1253,680),(1253,991))]
scale=.84
sheet=Image.new('RGBA',(1536,1088));draw=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',20)
decisions=dict(common_scale=scale,contact=[256,950],anatomy_correction_pending='Rear proposal has an extra rounded lobe beside the neck; composed refinement must resolve one integrated central upper-back hump.',views={})
for index,(facing,seed,contact) in enumerate(views):
    selection=source.getchannel('A').point(lambda v:255 if v>=16 else 0)
    ImageDraw.floodfill(selection,seed,128);selection=selection.point(lambda v:255 if v==128 else 0)
    selection.save(HERE/f'source-selection-{facing}.png');region=selection.getbbox()
    im=source.copy();im.putalpha(ImageChops.multiply(im.getchannel('A'),selection));im=im.crop(region)
    a=im.getchannel('A').point(lambda v:0 if v<16 else (255 if v>=240 else v));g=ImageOps.grayscale(im)
    im=Image.merge('RGBA',(g,g,g,a)).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    im.paste((0,0,0,0),mask=im.getchannel('A').point(lambda v:255 if v==0 else 0))
    delta=(256-round((contact[0]-region[0])*scale),950-round((contact[1]-region[1])*scale))
    canvas=Image.new('RGBA',(512,1024));canvas.paste(im,delta);canvas.save(HERE/f'patched-{facing}.png');sheet.alpha_composite(canvas,(index*512,0))
    draw.text((index*512+125,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[facing],font=font,fill='#b9b9b9')
    decisions['views'][facing]=dict(region=region,component_seed=seed,selection_mask=f'source-selection-{facing}.png',source_contact=contact,translation=delta,bounds=canvas.getchannel('A').getbbox())
sheet.save(HERE/'patched-views.png');(HERE/'patch-decisions.json').write_bytes((json.dumps(decisions,indent=2)+'\n').encode())
