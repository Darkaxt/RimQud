"""Narrow only original-side wrist ownership; complete wool and body stay unchanged."""
from pathlib import Path
import json,hashlib,sys,io
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2';BODY=ROOT/'art/conversion/body-human-male-older/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
 a=np.array(im).copy();a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
assert not (HERE/'model.json').exists();m=json.loads((OLD/'model.json').read_text())
s='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g fill="white"><path d="M224 519 Q245 527 266 517 L267 535 L224 535Z"/><circle cx="247" cy="553" r="37"/></g></svg>'
(HERE/'body-visibility-east.svg').write_bytes(s.encode());mask=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).getchannel('A');mask.save(HERE/'body-visibility-east.png');body=read(BODY/'selected-east.png');overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(mask)/255))));overlay.save(HERE/'body-overlay-east.png')
for row in m['views']['east']:
 if row['component']=='body-overlay':row.update(file='irudad-black-robes-v3-body-overlay-east.png',public_file=ref(HERE/'body-overlay-east.png')['path'],sha256=ref(HERE/'body-overlay-east.png')['sha256'])
m['occlusion_sources']['east'].update(body_visibility=ref(HERE/'body-visibility-east.png'),curved_wrist_svg=ref(HERE/'body-visibility-east.svg'),original_body_overlay=ref(HERE/'body-overlay-east.png'));m['correction']='v2 side wrist paint included adjacent arm/body outline above the cuff. v3 retains the original complete hand and a narrower smooth exposed-wrist region. Full wool, front/back ownership and original body unchanged.'
for n,d in [('model.json',m),('correction-decisions.json',dict(previous=ref(OLD/'model.json'),cause=m['correction'],full_cloth_unchanged=True,source_body_unchanged=True,new_imagegen_call=False,source=ref(OLD/'source-packet.json'),material_fit=ref(OLD/'registration-decisions.json'),side_mask=ref(HERE/'body-visibility-east.svg')))]: (HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
groups={k:{} for k in ['assembly','palette','overlay']}
for f in ['south','east','north']:
 b=read(BODY/f'selected-{f}.png');cloth=read(ROOT/m['occlusion_sources'][f]['full_cloth']['path']);o=read(ROOT/m['occlusion_sources'][f]['original_body_overlay']['path']);assembly=Image.alpha_composite(Image.alpha_composite(b,cloth),o);color=Image.alpha_composite(Image.alpha_composite(tint(b,(152,135,95)),tint(cloth,(21,83,82))),tint(o,(152,135,95)))
 for k,x in [('assembly',assembly),('palette',color),('overlay',o)]:groups[k][f]=x;x.save(HERE/f'{k}-{f}.png')
for rows in groups.values():rows['west (mirror)']=ImageOps.mirror(rows['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for k,n,title in [('assembly','assembly-comparison.png','BLACK ROBES / original hands with corrected narrow side wrist'),('palette','independent-palette-comparison.png','NATIVE COLORS / original K/K wool, independent body w'),('overlay','body-overlay-comparison.png','OWNERSHIP / original hands, no extra side body-outline paint')]:
 out=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(groups[k].items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284;out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0');d.text((x,584),f.upper(),font=font,fill='#e3cf43')
 d.text((18,620),'Same wool source, full garment, body/frame/contact. Only side wrist ownership corrected; native pending.',font=font,fill='#e5e8d8');out.save(HERE/n)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');print('Side wrist ownership corrected; original full cloth/body preserved. Review pending.')
