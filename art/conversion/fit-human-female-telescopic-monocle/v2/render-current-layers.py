"""Show the actual current item/detail/body-ownership layers after neutral-source repair."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];m=json.loads((HERE/'model.json').read_text());BODY=ROOT/f'art/conversion/body-{m["family"]}/v2'
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
groups={k:{} for k in ['assembly','palette','off']}
for f,rows in m['views'].items():
 body=read(BODY/f'selected-{"east" if f=="west" else f}.png')
 if f=='west':body=ImageOps.mirror(body)
 components={row['component']:read(ROOT/row['public_file']) for row in rows}
 off=Image.alpha_composite(Image.alpha_composite(body,components['item']),components['item-detail']);im=Image.alpha_composite(off,components['body-overlay']);color=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(152,135,95)),tint(components['item'],(119,191,207))),tint(components['item-detail'],(255,255,255))),tint(components['body-overlay'],(152,135,95)))
 for k,x in [('assembly',im),('off',off),('palette',color)]:groups[k][f]=x;x.save(HERE/f'{k}-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for k,n,title in [('assembly','headwear-comparison.png','CURRENT LAYERS / neutral full item + neutral detail + original head depth'),('palette','independent-palette-comparison.png','NATIVE COLORS / cyan C primary, white Y detail; body w independent'),('off','mask-off-comparison.png','MASK OFF / full optical source before original-head occlusion')]:
 out=Image.new('RGB',(1152,460),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(groups[k].items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284;out.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');d.text((x,360),f.upper(),font=font,fill='#e3cf43')
 d.text((18,422),'Only detail ink neutrality corrected. Body/item geometry and alpha unchanged; native binding pending.',font=font,fill='#e5e8d8');out.save(HERE/n)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');print('Rendered current corrected model layers, palette and intended-size facings.')
