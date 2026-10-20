"""Register four fixed-frame dried-stalk bridge variants with native constant tint mix."""
from pathlib import Path
from collections import deque
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
packet=json.loads((HERE/'source-packet-v2.json').read_text());source=Image.open(HERE/'refined-proposal.png').convert('RGBA');a=source.getchannel('A');w,h=source.size
selection=Image.new('L',source.size);seen=set()
for yy in [.25,.52,.79]:
 seed=(w//2,round(h*yy));assert a.getpixel(seed)>=32
 if seed in seen:continue
 q=deque([seed]);seen.add(seed)
 while q:
  x,y=q.popleft();selection.putpixel((x,y),255)
  for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=nx<w and 0<=ny<h and (nx,ny) not in seen and a.getpixel((nx,ny))>=16:seen.add((nx,ny));q.append((nx,ny))
selection.save(OUT/'source-selection-slats.png');bounds=selection.getbbox();g=ImageOps.grayscale(source)
clean=Image.merge('RGBA',(g,g,g,ImageChops.multiply(a,selection)));px=clean.load()
for y in range(h):
 for x in range(w):
  rr,gg,bb,aa=px[x,y];px[x,y]=(0,0,0,0) if aa<16 else (rr,gg,bb,255 if aa>=240 else aa)
clean.save(OUT/'cleaned-proposal.png');master=clean.crop(bounds);master.save(OUT/'mat-master-neutral.png')
# Shared material element fitted once to the constructed 8x6 panel, then reused unchanged.
mat=master.resize((256,192),Image.Resampling.LANCZOS);base=Image.new('RGBA',(512,768))
for y in [0,192,384,576]:
 for x in [0,256]:base.alpha_composite(mat,(x,y))
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];ratio=65/255
fg,detail=bytes.fromhex(palette['w']),bytes.fromhex(palette['W']);color=tuple(round(f*(1-ratio)+d*ratio) for f,d in zip(fg,detail))
def tint(im):
 v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in color],im.getchannel('A')))
rows=[];previews={};variants={}
for n in range(1,5):
 marks=Image.new('L',base.size);dr=ImageDraw.Draw(marks)
 for x,y in packet['native_accent_positions'][str(n)]:
  dr.line([(x*32,(y+4)*32),(x*32,y*32),((x+6)*32,y*32)],fill=100,width=3,joint='curve')
 marks=marks.filter(ImageFilter.GaussianBlur(.6));marks=ImageChops.multiply(marks,base.getchannel('A'))
 lum=base.getchannel('R');bright=lum.point(lambda v:min(255,v+55));lum=Image.composite(bright,lum,marks)
 im=Image.merge('RGBA',(lum,lum,lum,base.getchannel('A'))).resize((256,256),Image.Resampling.LANCZOS)
 im.save(OUT/f'variant-{n}-neutral.png');im.getchannel('A').save(OUT/f'variant-{n}-coverage.png')
 preview=tint(im);preview.save(OUT/f'variant-{n}-native-preview.png');previews[n]=preview;variants[n]=im
 rows.append(dict(variant=n,source_tile=f'Assets_Content_Textures_Tiles_sw_floor_brickb{n}.bmp',
  aliases=[f'Tiles/sw_floor_brickb{n}.bmp',f'Assets_Content_Textures_Tiles_sw_floor_brickb{n}.bmp'],
  neutral=asset(OUT/f'variant-{n}-neutral.png'),coverage=asset(OUT/f'variant-{n}-coverage.png'),native_accent_positions=packet['native_accent_positions'][str(n)]))
decisions=dict(source=asset(HERE/'refined-proposal.png'),source_size=list(source.size),selected_bounds=list(bounds),
 cleanup='Complete connected source slat components selected by actual alpha, grayscale RGB, alpha<16 discarded and >=240 made opaque. Clear RGB in invisible pixels; no generated backdrop/cast shadow retained.',
 element_registration=dict(panel=[8,6],master_pixels=[256,192],frame=[16,24],construction_pixels=[512,768],recipient_pixels=[256,256],
  rule='One shared refined surface mat fitted once to the constructed panel, then reused at all eight fixed positions and all four variants. No per-variant alpha-bound fitting.'),
 physical_coverage='Identical deck coverage across all four variants; narrow slat joints only. Native L-mark differences are cosmetic accents, not missing support/collision panels.',
 palette='All actual native opaque source pixels have R65/255. Resolve that constant mix of actual foreground/detail at draw time, then multiply by neutral albedo. No literal green or fixed brown/ochre in production PNGs.',
 accent_patch='Map original source L positions into restrained neutral wear highlights clipped to the existing deck; accents cannot add coverage outside the bridge or introduce colored foreign outlines.')
model=dict(kind='bridge_object_variants',blueprint='BrineBridge',source=asset(HERE/'source-packet-v2.json'),
 variants=rows,native_variant_index=asset(HERE/'native-variant-index.json'),
 registration=dict(native_frame=[16,24],recipient_frame=[256,256],physical_cell=[1,1],rule='All four variants use identical frame/placement/coverage; keep native cosmetic selector ownership.'),
 native_tint=dict(foreground='actual native foreground',detail='actual native detail',mix=ratio,source_red=65,
  formula='nativeTint=(1-65/255)*foreground+(65/255)*detail; output=alpha*neutralAlbedo*nativeTint+(1-alpha)*underlay',
  implementation_note='Constant source mix can use the existing texture-times-tint material path once actual native colors are combined. No new generic multi-color shader is required for this object.'),
 layer_contract='Native liquid/ground underlay, then bridge at its native object layer, then independent visible foreground. Transparent joints reveal the actual underlay; no opaque black boxes.',
 native_behavior='Keep Bridge=1, SuspendedPlatform, non-solid/non-occluding, native crossing and random cosmetic selection. This art does not create support rules, rails or bridge simulation.',
 state='Generation-ready four source-bound cosmetic variants; actual native tint/selector/visibility/underlay/foreground binding and acceptance pending all-conversions-generated gate')
for name,obj in [('registration-decisions.json',decisions),('model.json',model)]:
 (OUT/name).write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,640),'#142823');dr=ImageDraw.Draw(plate)
dr.text((20,16),'BRINEBRIDGE / four native cosmetic accent layouts / same dried-stalk deck / native w-W mix65/255',font=font,fill='#e3cf43')
for n,im in previews.items():
 x=24+(n-1)*360;plate.paste(im.resize((288,384),Image.Resampling.LANCZOS),(x,70),im.resize((288,384),Image.Resampling.LANCZOS));dr.text((x,480),f'brickb{n}',font=font,fill='#e5e8d8')
 for j,(ww,hh) in enumerate([(16,24),(24,36),(32,48)]):
  sm=im.resize((ww,hh),Image.Resampling.LANCZOS);plate.paste(sm,(x+j*90,535),sm)
plate.save(OUT/'variants-comparison.png')
ground=Image.open(ROOT/'art/conversion/tile-grassy-ground/v1/registered/native-k-preview.png').convert('RGBA')
water=Image.open(ROOT/'art/conversion/tile-water-shallow/v1/registered/native-color-preview.png').convert('RGBA')
context=Image.new('RGBA',(7*256,3*256))
for y in range(0,context.height,1024):
 for x in range(0,context.width,1024):context.paste(ground,(x,y))
for x in [2,3,4]:
 for y in range(3):context.alpha_composite(water.crop((x*128,y*128,x*128+256,y*128+256)),(x*256,y*256))
for x in range(1,6):context.alpha_composite(previews[1+(x-1)%4],(x*256,256))
context=context.resize((1120,480),Image.Resampling.LANCZOS);out=Image.new('RGB',(1120,565),'#142823');out.paste(context.convert('RGB'),(0,60));ImageDraw.Draw(out).text((16,14),'BRIDGE AUTHORING / selected liquid under deck / four cosmetic accents / no native crossing test',font=font,fill='#e3cf43');out.save(OUT/'water-underlay-comparison.png')
