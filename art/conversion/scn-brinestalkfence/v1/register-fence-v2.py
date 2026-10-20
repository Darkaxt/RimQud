"""Register one shared picket and all sixteen source-coordinate fence layouts."""
from pathlib import Path
import json,hashlib
from collections import deque
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered-v2';OUT.mkdir(exist_ok=True);STATES=OUT/'states';STATES.mkdir(exist_ok=True)
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');alpha=source.getchannel('A');w,h=source.size
# Select the complete connected middle picket, not the RGB-only transparent halo.
seed=(510,770);assert alpha.getpixel(seed)>=32
seen={seed};q=deque([seed]);selection=Image.new('L',source.size)
while q:
 x,y=q.popleft();selection.putpixel((x,y),255)
 for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen and alpha.getpixel((nx,ny))>=16:seen.add((nx,ny));q.append((nx,ny))
bounds=selection.getbbox();selection.save(OUT/'source-selection-middle.png')
g=ImageOps.grayscale(source);clean=Image.merge('RGBA',(g,g,g,ImageChops.multiply(alpha,selection)))
# Clear RGB outside alpha so tool previews do not imply an actual glow/opaque background.
pixels=clean.load()
for y in range(h):
 for x in range(w):
  rr,gg,bb,aa=pixels[x,y]
  pixels[x,y]=(0,0,0,0) if aa<16 else (rr,gg,bb,255 if aa>=240 else aa)
clean.save(OUT/'cleaned-proposal.png');master=clean.crop(bounds);master.save(OUT/'picket-master-neutral.png')
S=256;sx=S/16;sy=S/24
# ImageGen placement is not registration: the master is placed in this fixed native-derived rectangle.
size=(round(2.6*sx),round(10*sy));master_scaled=master.resize(size,Image.Resampling.LANCZOS)
def place(im,tile,x):im.alpha_composite(tile,(round((x-.6)*sx),round(7*sy)))
index=json.loads((HERE/'native-state-index.json').read_text());palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
primary_atlas=Image.new('RGBA',(1024,1024));detail_atlas=Image.new('RGBA',(1024,1024));rows=[];colored={}
def tint(im,key):
 v=im.getchannel('R');c=bytes.fromhex(palette[key]);return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
for m in range(16):
 p=Image.new('RGBA',(S,S));d=Image.new('RGBA',(S,S));ns=bool(m&5)
 if m&2 and m&8:positions=[-1,3,7,11,15]
 elif m&2:positions=[7,11,15]
 elif m&8:positions=[-1,3,7]
 elif ns:positions=[7]
 else:positions=[3,7,11]
 for x in positions:
  if x==7 and ns:continue
  place(p,master_scaled,x)
 # Same neutral source master, with pale cap/wave ownership mapped to the independent native detail role.
 lum=p.getchannel('R');a=p.getchannel('A');da=ImageChops.multiply(lum.point(lambda n:min(235,max(0,round((n-200)*6)))),a)
 d=Image.new('RGBA',(S,S),'white');d.putalpha(da)
 if ns:
  y0=0 if m&1 else round(7*sy);y1=S if m&4 else round(17*sy)
  # Native edge-on view is a narrow continuous shaft, not a rotated frontal panel.
  strip=Image.new('RGBA',(round(2*sx),y1-y0));sd=ImageDraw.Draw(strip)
  for x in range(strip.width):
   v=round(118+78*(1-abs((x/(strip.width-1))*2-1)));sd.line((x,0,x,strip.height),fill=(v,v,v,255))
  p.alpha_composite(strip,(round(7*sx),y0))
  native=Image.open(index['originals'][m]['private_mask']['path']).convert('RGBA')
  native_detail=ImageChops.multiply(native.getchannel('R'),native.getchannel('A')).resize((S,S),Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(.65))
  # Restrict native alternating cap ownership to the actual central edge-on shaft.
  central=Image.new('L',(S,S));ImageDraw.Draw(central).rectangle((round(7*sx)+2,y0,round(9*sx)-3,y1-1),fill=235)
  cap=ImageChops.multiply(native_detail,central);layer=Image.new('RGBA',(S,S),'white');layer.putalpha(cap);d.alpha_composite(layer)
 # Every detail pixel must remain inside this state's actual visible picket coverage.
 d.putalpha(ImageChops.multiply(d.getchannel('A'),p.getchannel('A')))
 p.save(STATES/f'{m:02d}-primary.png');d.save(STATES/f'{m:02d}-detail.png');p.getchannel('A').save(STATES/f'{m:02d}-coverage.png')
 xy=(m%4*S,(3-m//4)*S);primary_atlas.paste(p,xy);detail_atlas.paste(d,xy)
 view=tint(p,'w');view.alpha_composite(tint(d,'y'));colored[m]=view
 rows.append(dict(mask=m,native_tile=index['originals'][m]['tile'],front_post_positions=[x for x in positions if not(x==7 and ns)],edge_on=ns,
  atlas_rect=[*xy,S,S],primary=asset(STATES/f'{m:02d}-primary.png'),detail=asset(STATES/f'{m:02d}-detail.png'),coverage=asset(STATES/f'{m:02d}-coverage.png')))
primary_atlas.save(OUT/'primary-atlas.png');detail_atlas.save(OUT/'detail-atlas.png')
decisions=dict(source=asset(HERE/'refined-proposal.png'),source_size=list(source.size),selected_component='Complete middle connected picket',selection_bounds=list(bounds),
 cleanup='Select actual alpha, grayscale RGB, discard alpha<16 and make alpha>=240 opaque. RGB-only exterior glow is cleared rather than baked into a fence.',
 registration=dict(native_frame=[16,24],recipient_frame=[256,256],native_front_picket_rectangle=[6.4,7,9,17],
  rule='Use the same native-derived position/extent for every cloned upright; no per-state independent fit. The generator sheet offsets are not world pivots.'),
 source_topology='Front pickets keep native counts/locations, including clipped neighbor-edge pickets. N/S connections use a separate narrow edge-on strip and actual native pale cap positions. No wall cap, connecting board or opaque gap fill.',
 source_color_ownership='Native w body and independent y pale tips/salt traces. N/S native cap boundaries keep only .65texel smoothing and leave the two-texel shaft edge to primary shading. No fixed color in production sources.',
 interpretation='Refined stump contour/grain and short side spurs are authored. Explicit source-state layouts, not generated connection variants, own the atlas.')
model=dict(kind='connected_fence_atlas',blueprint='BrinestalkFence',source=asset(HERE/'source-packet.json'),
 primary=asset(OUT/'primary-atlas.png'),detail=asset(OUT/'detail-atlas.png'),states=rows,
 atlas_size=[1024,1024],grid=[4,4],tile_size=[256,256],row_policy='Recipient bottom-origin mask order:col=mask%4,row=3-floor(mask/4)',bits=dict(N=1,E=2,S=4,W=8),
 native_states=asset(HERE/'native-state-index.json'),registration=decisions['registration'],
 palette=dict(primary='actual native foreground, preview w #'+palette['w'],detail='actual native detail, preview y #'+palette['y']),
 alpha_contract='Actual open gaps remain transparent. Native solidity, AllowMissiles, Flyover and non-occlusion remain game rules; alpha does not rewrite those mechanics.',
 connection_scope='Native PaintWith brinestalkfence compatibility and supported16cardinal source tile names. Do not adopt donor Asymmetric ordering/mechanics or link unrelated structures.',
 sampling_contract='Sample only the selected atlas state at texel centers or with point filtering; avoid bilinear bleed from unrelated packed states.',
 state='Generation-ready authored states; native atlas/tint, connection/visibility/foreground and supported-state acceptance pending every-conversion-generated gate')
for name,obj in [('registration-decisions.json',decisions),('model.json',model)]:
 (OUT/name).write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1280,1090),'#142823');dr=ImageDraw.Draw(plate)
dr.text((18,14),'BRINESTALK FENCE /16native-derived states / w body + y salt tips / open alpha gaps',font=font,fill='#e3cf43')
for m,im in colored.items():
 x=m%4*320;y=m//4*250+55;plate.paste(im,(x+32,y),im);dr.text((x+20,y+230),f'{m:02d} '+index['originals'][m]['native_suffix'],font=font,fill='#e5e8d8')
plate.save(OUT/'states-comparison.png')
ground=Image.open(ROOT/'art/conversion/tile-grassy-ground/v1/registered/native-k-preview.png').convert('RGBA')
DIRS=[(0,-1),(1,0),(0,1),(-1,0)]
def assembly(cells,w,h,name,small=False):
 im=Image.new('RGBA',(w*S,h*S))
 for y in range(0,im.height,1024):
  for x in range(0,im.width,1024):im.paste(ground,(x,y))
 for x,y in cells:
  mask=sum(1<<b for b,(dx,dy) in enumerate(DIRS) if (x+dx,y+dy) in cells);im.alpha_composite(colored[mask],(x*S,y*S))
 im=im.resize((w*16,h*24) if small else (w*80,h*120),Image.Resampling.LANCZOS)
 out=Image.new('RGB',(max(im.width,1120),im.height+90),'#142823');out.paste(im.convert('RGB'),((out.width-im.width)//2,60));draw=ImageDraw.Draw(out)
 draw.text((16,14),'FENCE AUTHORING / connected rows, corners, T and open gate / '+('16x24 per cell' if small else 'Qud display-cell proportions'),font=font,fill='#e3cf43');out.save(OUT/name)
cells={(x,1) for x in range(1,12)}|{(x,6) for x in range(1,12) if x not in [6,7]}|{(1,y) for y in range(1,7)}|{(11,y) for y in range(1,7)}|{(6,y) for y in range(1,5)}|{(x,4) for x in range(4,9)}
assembly(cells,13,8,'connections-comparison.png');assembly(cells,13,8,'native-scale-comparison.png',True)
