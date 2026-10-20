"""Keep the editable whole vest; transfer contextual cloth and restore fixed arms."""
from pathlib import Path
import hashlib, json, io, sys
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import spsolve
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0,"E:/Temp/rimqud-conversion-runtime/python-libs")
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
 d.text((18,620),'Fixed original body; intact cloth and body visibility and detail tint separate. Native acceptance awaits the full set.',font=FONT,fill='#e5e8d8')
 out.save(HERE/name)

OLD=HERE.parent/'v1'
model=json.loads((OLD/'model.json').read_text());record={'workflow':'regional-curved-v1','source':ref(OLD/'registration-decisions.json'),'correction':'Remove the old sleeve-mask torso spur at inner elbows; this sleeveless item keeps only original forearm ownership. Full cloth/detail/body/profile unchanged.','views':{}}
groups={k:{} for k in ['assembly','overlay','mask','palette']}
for f in ['south','east','north']:
 mask=Image.open(OLD/f'body-visibility-{f}.png').convert('L')
 if f!='east':
  clip='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g fill="white"><path d="M0 0 H200 V350 Q180 390 168 420 Q162 460 155 500 L154 525 H0Z"/><g transform="translate(512 0) scale(-1 1)"><path d="M0 0 H200 V350 Q180 390 168 420 Q162 460 155 500 L154 525 H0Z"/></g><rect x="0" y="525" width="512" height="499"/></g></svg>'
  (HERE/f'arm-ownership-limit-{f}.svg').write_bytes(clip.encode());cap=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=clip,skip_system_fonts=True))).getchannel('A');mask=Image.fromarray(np.minimum(np.array(mask),np.array(cap)))
 mask.save(HERE/f'body-visibility-{f}.png');body=read(BODY/f'selected-{f}.png');cloth=read(OLD/f'intact-vest-{f}.png');detail=read(OLD/f'item-detail-{f}.png')
 overlay=body.copy();overlay.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(mask)/255))));overlay.save(HERE/f'body-overlay-{f}.png')
 assembly=Image.alpha_composite(Image.alpha_composite(body,cloth),overlay);assembly.save(HERE/f'assembled-{f}.png')
 colored=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(tint(body,(119,191,207)),tint(cloth,(177,201,195))),tint(detail,(21,83,82))),tint(overlay,(119,191,207)));colored.save(HERE/f'palette-{f}.png')
 for k,im in [('assembly',assembly),('overlay',overlay),('mask',mask.convert('RGBA')),('palette',colored)]:groups[k][f]=im
 over=model['views'][f][-1];over.update(public_file=ref(HERE/f'body-overlay-{f}.png')['path'],sha256=ref(HERE/f'body-overlay-{f}.png')['sha256'],file=over['file'].replace('-v1-','-v2-'))
 model['occlusion_sources'][f]['mask']=ref(HERE/f'body-visibility-{f}.png');record['views'][f]=dict(mask=ref(HERE/f'body-visibility-{f}.png'),body=ref(BODY/f'selected-{f}.png'),cloth_unchanged=ref(OLD/f'intact-vest-{f}.png'),detail_unchanged=ref(OLD/f'item-detail-{f}.png'))
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
for k,name,title in [('assembly','assembly-comparison.png','ADULT MALE / intact Pocketed Vest, corrected inner elbow ownership'),('overlay','body-overlay-comparison.png','ORIGINAL ARMS / old sleeve spur excluded for this sleeveless garment'),('mask','body-mask-comparison.png','BODY OWNERSHIP / smooth forearm limits and unchanged original hands'),('palette','independent-palette-comparison.png','NATIVE PALETTE / primary y, pocket detail K; body C illustrative')]:plate(name,groups[k],title)
small=Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',record)
print('Corrected only the inner elbow ownership; prior source/detail/profile/body unchanged.')
