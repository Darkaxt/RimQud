"""Contextual source/reference comparison; raw game textures remain private files."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
packet=json.loads((HERE/'source-packet.json').read_text());font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
out=Image.new('RGB',(1140,850),'#142823');draw=ImageDraw.Draw(out)
draw.text((18,15),'SPECTACLES / source -> actual directional reference -> construction -> registered art',font=font,fill='#e3cf43')
for x,t in [(18,'QUD ORIGINAL GLYPH'),(240,'MOD REFERENCE'),(520,'CONSTRUCTION'),(820,'REGISTERED RESULT')]:draw.text((x,62),t,font=font,fill='#e3cf43')
reference=Path(packet['reference']['path']);assert hashlib.sha256(reference.read_bytes()).hexdigest()==packet['reference']['sha256'];im=Image.open(reference).convert('RGBA').resize((128,192),Image.Resampling.NEAREST);out.paste(im,(45,160),im)
for i,t in enumerate(['Spectacles','16 x 24 source glyph','Normalized reference','Actual palette: y / Y','','Two almonds of glass','in wireframe cups.','','Face / laterality 0','Part 198 / item 540','','Native acceptance pending']):draw.text((18,385+i*24),t,font=font,fill='#e5e8d8')
for i,f in enumerate(['south','east','north']):
 y=110+i*230;draw.text((240,y),f.upper(),font=font,fill='#e3cf43');source=packet['donor']['assets'][i];p=Path(source['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'];im=Image.open(p).convert('RGBA');bounds=im.getchannel('A').point(lambda v:255 if v>128 else 0).getbbox();im=im.crop(bounds);scale=min(210/im.width,120/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);bg=Image.new('RGBA',(220,190),'#20382d');bg.alpha_composite(im,((220-im.width)//2,(190-im.height)//2));out.paste(bg.convert('RGB'),(240,y+25))
 for x,name in [(510,'constructed-assembly'),(810,'assembled')]:
  im=Image.open(HERE/f'{name}-{f}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((200,200)),(x,y+15))
draw.text((18,805),'Vanilla Apparel Expanded supplies directional attachment only; Qud thin wire and almond glass govern design.',font=font,fill='#e5e8d8');out.save(HERE/'reference-comparison.png');print('Contextual original/mod/construction/current art comparison saved; raw source files stay local.')
