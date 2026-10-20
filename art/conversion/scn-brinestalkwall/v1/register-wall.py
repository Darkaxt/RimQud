"""Construct all connected wall faces/caps with one source-bound material/frame."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
STATES=OUT/'states';STATES.mkdir(exist_ok=True)
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
g=ImageOps.grayscale(Image.open(HERE/'refined-proposal.png')).resize((256,256),Image.Resampling.LANCZOS)
# Blend paired border bands only, retaining all four generated stalks/material detail.
band=8
for axis in ['x','y']:
 old=g.copy()
 for i in range(band):
  t=(1-i/(band-1))**2
  for j in range(256):
   p=(i,j) if axis=='x' else (j,i);q=(255-i,j) if axis=='x' else (j,255-i)
   a,b=old.getpixel(p),old.getpixel(q);m=(a+b)/2
   g.putpixel(p,round(a*(1-t)+m*t));g.putpixel(q,round(b*(1-t)+m*t))
g.save(OUT/'face-material.png')
# Editable deterministic top-cap pattern, not another generated object sheet.
caps=['<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256"><rect width="256" height="256" fill="#8f8f8f"/>']
for y in [32,96,160,224]:
 for x in [32,96,160,224]:
  caps.append(f'<ellipse cx="{x}" cy="{y}" rx="27" ry="25" fill="#cccccc" stroke="#666666" stroke-width="2"/><ellipse cx="{x-1}" cy="{y}" rx="18" ry="17" fill="none" stroke="#a6a6a6" stroke-width="1.5"/><path d="M{x-17} {y-13}q17 -8 34 0" fill="none" stroke="#e4e4e4" stroke-width="2"/>')
caps.append('</svg>');(OUT/'constructed-caps.svg').write_bytes(''.join(caps).encode())
import resvg_py
(OUT/'constructed-caps.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(OUT/'constructed-caps.svg'),skip_system_fonts=True))
top=ImageOps.grayscale(Image.open(OUT/'constructed-caps.png'))
S=256;lo,hi=48,208;lift=48
DIRS=[(0,-1),(1,0),(0,1),(-1,0)]
def shape(canvas,x,y,mask):
 d=ImageDraw.Draw(canvas);ox,oy=x*S,y*S;d.rectangle((ox+lo,oy+lo,ox+hi-1,oy+hi-1),fill=255)
 if mask&1:d.rectangle((ox+lo,oy,ox+hi-1,oy+128),fill=255)
 if mask&2:d.rectangle((ox+128,oy+lo,ox+255,oy+hi-1),fill=255)
 if mask&4:d.rectangle((ox+lo,oy+128,ox+hi-1,oy+255),fill=255)
 if mask&8:d.rectangle((ox,oy+lo,ox+128,oy+hi-1),fill=255)
def shifted(im,dy):
 out=Image.new('L',im.size);out.paste(im,(0,dy));return out
def geometry(mask):
 foot=Image.new('L',(768,768));shape(foot,1,1,mask)
 for bit,(dx,dy) in enumerate(DIRS):
  if mask&(1<<bit):shape(foot,1+dx,1+dy,1<<((bit+2)%4))
 raised=shifted(foot,-lift);solid=Image.new('L',foot.size)
 for off in range(lift+1):solid=ImageChops.lighter(solid,shifted(foot,-off))
 face=ImageChops.subtract(solid,raised)
 edge=ImageChops.subtract(solid,solid.filter(ImageFilter.MinFilter(5)))
 topedge=ImageChops.subtract(raised,raised.filter(ImageFilter.MinFilter(3)))
 return [im.crop((256,256,512,512)) for im in [foot,raised,solid,face,edge,topedge]]
def tinted(primary,detail):
 out=Image.new('RGBA',primary.size);a=primary.getchannel('A');v=primary.getchannel('R');c=bytes.fromhex(palette['w'])
 out=Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],a))
 v=detail.getchannel('R');c=bytes.fromhex(palette['y']);layer=Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],detail.getchannel('A')))
 out.alpha_composite(layer);return out
primary_atlas=Image.new('RGBA',(1024,1024));detail_atlas=Image.new('RGBA',(1024,1024));index=[];colored_states={}
for mask in range(16):
 foot,raised,solid,face,edge,topedge=geometry(mask)
 lum=g.point(lambda n:round(n*.83));lum.paste(top,(0,0),raised)
 # Clip outline shading from the complete neighborhood, never from a per-cell rectangle.
 lum.paste(Image.new('L',lum.size,42),(0,0),edge);lum.paste(Image.new('L',lum.size,62),(0,0),topedge)
 primary=Image.merge('RGBA',(lum,lum,lum,solid))
 detail_alpha=lum.point(lambda n:min(112,max(0,round((n-150)*1.1))))
 detail_alpha=ImageChops.multiply(detail_alpha,solid)
 detail=Image.new('RGBA',(256,256),'white');detail.putalpha(detail_alpha)
 primary.save(STATES/f'{mask:02d}-primary.png');detail.save(STATES/f'{mask:02d}-detail.png');solid.save(STATES/f'{mask:02d}-coverage.png')
 xy=(mask%4*256,(3-mask//4)*256);primary_atlas.paste(primary,xy);detail_atlas.paste(detail,xy)
 colored_states[mask]=tinted(primary,detail)
 index.append(dict(mask=mask,neighbors=[n for bit,n in enumerate(['N','E','S','W']) if mask&(1<<bit)],
  atlas_rect=[*xy,256,256],primary=asset(STATES/f'{mask:02d}-primary.png'),detail=asset(STATES/f'{mask:02d}-detail.png'),coverage=asset(STATES/f'{mask:02d}-coverage.png')))
primary_atlas.save(OUT/'primary-atlas.png');detail_atlas.save(OUT/'detail-atlas.png')
model=dict(kind='connected_wall_atlas',blueprint='BrinestalkWall',source=asset(HERE/'source-packet.json'),
 primary=asset(OUT/'primary-atlas.png'),detail=asset(OUT/'detail-atlas.png'),
 atlas_size=[1024,1024],tile_size=[256,256],grid=[4,4],row_policy='Recipient bottom-origin mask layout:col=mask%4,row=3-floor(mask/4). Do not assume donor CornerFiller ordering.',
 bits=dict(N=1,E=2,S=4,W=8),states=index,
 registration=dict(canvas=[256,256],ground_center=[128,128],footprint_width=160,authored_lift=48,physical_cell=[1,1],
  rule='All states share one cell frame, scale and extrusion. Build neighbor context before lifting/cropping; no independently fitted state bounds or per-cell connected outlines.'),
 palette=dict(primary='actual native foreground/TileColor, preview w #'+palette['w'],detail='actual native detail, preview y #'+palette['y']),
 material=asset(OUT/'face-material.png'),caps_geometry=asset(OUT/'constructed-caps.svg'),
 appearance='Stripped upright brinestalk trunks bonded by mud; raised cut-end/mud cap is an authored 2.5D interpretation. No stone courses or horizontal donor logs.',
 connection_scope='Recipient16cardinal masks only, respecting actual visible compatible brinestalk wall types. Do not link every unrelated wall/fence/material or claim all native eight-neighbor variants exported.',
 native_behavior='Preserve source solid/organic/occlusion, hidden/exploration states and native foreground priority. Damage/graffiti/rare animation and unsupported states retain native fallback.',
 native_state='Generation-ready art only; native atlas selection, tint, visibility/contact/occlusion and state acceptance pending every-conversion-generated gate')
decisions=dict(source=asset(HERE/'refined-proposal.png'),face=[256,256],seam_patch='Eight-texel opposing edge bands blend to their shared midpoint at the border. All four source trunks retained; exact x/y border pixels match.',
 topology='One160px-wide connected footprint in256px square cell; top is lifted48px. Three-by-three context includes connected-neighbor return arms before extrusion, outline and crop.',
 cap_interpretation='Explicit editable repeated cut-end circles in mud. Top construction has no original exact cross-section; it follows the stripped-trunk description and donor cap presentation.',
 color_extraction='Neutral source shading in primary w. Independent neutral detail-alpha from bright ridges/caps receives native y; no color baked into atlas.',
 coverage='Primary owns solid body alpha; detail stays within it. Connected boundaries are evaluated before cropping, preventing new endpoint caps/outline seams at every cell border.')
for name,obj in [('model.json',model),('registration-decisions.json',decisions)]:
 (OUT/name).write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1280,1210),'#142823');d=ImageDraw.Draw(plate)
d.text((18,14),'BRINESTALK / all16recipient N/E/S/W states / native w + y / common frame',font=font,fill='#e3cf43')
for m,im in colored_states.items():
 x=m%4*320;y=m//4*282+55
 plate.paste(im,(x+32,y),im);d.text((x+24,y+244),f'{m:02d} '+('-'.join(index[m]['neighbors']) or 'ISOLATED'),font=font,fill='#e5e8d8')
plate.save(OUT/'states-comparison.png')
ground=Image.open(ROOT/'art/conversion/tile-grassy-ground/v1/registered/native-k-preview.png').convert('RGBA')
def field(size):
 out=Image.new('RGBA',size)
 for y in range(0,size[1],1024):
  for x in range(0,size[0],1024):out.paste(ground,(x,y))
 return out
def assembly(cells,w,h,name,title,small=False):
 im=field((w*256,h*256))
 for x,y in cells:
  mask=sum(1<<b for b,(dx,dy) in enumerate(DIRS) if (x+dx,y+dy) in cells)
  tile=colored_states[mask];im.alpha_composite(tile,(x*256,y*256))
 if small:im=im.resize((w*16,h*24),Image.Resampling.LANCZOS)
 else:im=im.resize((w*96,h*96),Image.Resampling.LANCZOS)
 out=Image.new('RGB',(max(im.width,1152),im.height+90),'#142823');out.paste(im.convert('RGB'),((out.width-im.width)//2,60));ImageDraw.Draw(out).text((16,14),title,font=font,fill='#e3cf43');out.save(OUT/name)
cells={(x,1) for x in range(1,12)}|{(x,8) for x in range(1,12) if x not in [5,6]}|{(1,y) for y in range(1,9)}|{(11,y) for y in range(1,9)}|{(6,y) for y in range(1,6)}|{(x,5) for x in range(3,10)}
assembly(cells,13,10,'connections-comparison.png','BRINESTALK AUTHORING / straight, corner, T and open doorway / no cell-edge caps')
assembly(cells,13,10,'native-scale-comparison.png','BRINESTALK AUTHORING /16x24per cell / same assembled art, no native game capture',True)
tree=ET.parse('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/Joppa.rpm').getroot();walls=set()
for c in tree.findall('cell'):
 if any(o.get('Name') in ['BrinestalkWall','BrinestalkWallWithGearbox'] for o in c.findall('object')):walls.add((int(c.get('X')),int(c.get('Y'))))
# Gearbox wall is only a compatible join here; its separate overlay entry remains unfinished.
assembly(walls,80,25,'static-joppa-authoring-comparison.png','STATIC JOPPA AUTHORING / selected brinestalk walls / gearbox details and other objects unfinished',True)
