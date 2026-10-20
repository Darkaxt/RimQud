"""Keep the editable whole robe; transfer contextual cloth and restore fixed arms."""
from pathlib import Path
import hashlib, json, io, sys
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-male/v2'
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists(), 'Keep registered versions immutable'

def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,data): (HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
def read(p): return Image.open(p).convert('RGBA')
def tint(im,color):
 a=np.array(im).copy();v=a[:,:,:3].mean(axis=2)
 a[:,:,:3]=np.uint8(np.round(v[:,:,None]*np.array(color)/255));return Image.fromarray(a)

def complete(gray,known,envelope):
 """Same contextual fabric, harmonic continuation only where hidden/invalid."""
 unknown=envelope & ~known; yy,xx=np.where(unknown);n=len(yy)
 ids=np.full(gray.shape,-1,np.int32);ids[yy,xx]=np.arange(n)
 deg=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
 for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
  ny,nx=yy+dy,xx+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512))
  q=q[envelope[ny[q],nx[q]]];deg[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0
  rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
 if n:
  matrix=sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(deg)
  gray[yy,xx]=spsolve(matrix,rhs)
 return gray,unknown

def plate(name,rows,title):
 out=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(out)
 d.text((18,14),title,font=FONT,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284
  out.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#e3cf43');d.line((x,529,x+255,529),fill='#70b8b0')
  d.text((x,584),f.upper(),font=FONT,fill='#e3cf43')
 d.text((18,620),'Fixed original body; intact cloth and curved visibility separate. Native acceptance awaits the full set.',font=FONT,fill='#e5e8d8')
 out.save(HERE/name)

OLD=HERE.parent/'v1'
model=json.loads((OLD/'model.json').read_text())
record={'workflow':'regional-curved-v1','previous_source':ref(OLD/'registration-decisions.json'),'correction':'Replace broad lower arm paint with original-hand circular ownership. Cloth and body unchanged; no new generation or fitting.', 'views':{}}
groups={k:{} for k in ['assembly','cloth','mask','overlay','off','palette']}
for f in ['south','east','north']:
 if f=='east':
  svg=(OLD/f'body-visibility-{f}.svg').read_text()
  mask=Image.open(OLD/f'body-visibility-{f}.png').convert('L')
 else:
  # Cuff curve above, explicit forearm, then exact circle for the hand.
  # This excludes the adjacent torso contour previously inside a broad hull.
  cx=124 if f=='south' else 123
  left='M91 422 Q128 448 174 430 L161 488 L148 528 L102 528 L91 480Z'
  svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g fill="white"><path d="'+left+'"/><circle cx="'+str(cx)+'" cy="557" r="35"/><g transform="translate(512 0) scale(-1 1)"><path d="'+left+'"/><circle cx="'+str(cx)+'" cy="557" r="35"/></g></g></svg>'
  mask=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg,skip_system_fonts=True))).getchannel('A')
 (HERE/f'body-visibility-{f}.svg').write_bytes(svg.encode());mask.save(HERE/f'body-visibility-{f}.png')
 body=read(BODY/f'selected-{f}.png');cloth=read(OLD/f'intact-robe-{f}.png')
 (HERE/f'intact-robe-{f}.png').write_bytes((OLD/f'intact-robe-{f}.png').read_bytes())
 overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(mask)/255))))
 overlay.save(HERE/f'body-overlay-{f}.png');off=Image.alpha_composite(body,cloth);assembly=Image.alpha_composite(off,overlay)
 assembly.save(HERE/f'assembled-{f}.png');off.save(HERE/f'mask-off-{f}.png')
 colored=Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(cloth,(177,201,195))),tint(overlay,(119,191,207)));colored.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('cloth',cloth),('mask',mask.convert('RGBA')),('overlay',overlay),('off',off),('palette',colored)]:groups[k][f]=im
 for row in model['views'][f]:
  name=f'intact-robe-{f}.png' if row['component']=='item' else f'body-overlay-{f}.png'
  row.update(public_file=ref(HERE/name)['path'],sha256=ref(HERE/name)['sha256'],file=row['file'].replace('-v1-','-v2-'))
 model['occlusion_sources'][f]=dict(cloth=ref(HERE/f'intact-robe-{f}.png'),mask=ref(HERE/f'body-visibility-{f}.png'),editable_mask=ref(HERE/f'body-visibility-{f}.svg'))
 record['views'][f]=dict(cloth_unchanged=ref(OLD/f'intact-robe-{f}.png'),**model['occlusion_sources'][f])
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
for k,name,title in [('assembly','assembly-comparison.png','ADULT MALE / same intact robe; corrected original-hand ownership'),('cloth','intact-garment-comparison.png','FULL CLOTH / unchanged contextual material and editable pattern'),('mask','body-mask-comparison.png','CURVED VISIBILITY / cuff cross-section and original forearm/round hand'),('overlay','body-overlay-comparison.png','ORIGINAL ARMS / no adjacent torso-outline selection'),('off','mask-off-comparison.png','MASK OFF / unchanged continuous cloth under the arm'),('palette','independent-palette-comparison.png','PALETTE OWNERSHIP / illustrative body C; actual Cloth Robe y/y')]:plate(name,groups[k],title)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
write('model.json',model);write('registration-decisions.json',record)
print('Male hand ownership corrected; full cloth unchanged.')
