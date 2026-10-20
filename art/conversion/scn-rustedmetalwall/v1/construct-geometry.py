"""Rebuild native industrial contours; interpret checker marks as welded diamonds."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def geometry(raw,suffix):
 def at(x,y):return raw.getpixel((x,y)) if 0<=x<16 and 0<=y<24 else (0,0,0,0)
 def black(x,y):r,_,_,a=at(x,y);return bool(a and r==0)
 mesh=set()
 for y in range(24):
  for x in range(16):
   if black(x,y) and not any(black(x+dx,y+dy) for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]) and sum(black(x+dx,y+dy) for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)])>=2:
    mesh.add((x,y))
 # Retain terminal mesh joints with only one diagonal neighbor (the tiny
 # source's lower/right checker endpoint otherwise becomes an orphan square).
 while True:
  endpoints={(x,y) for y in range(24) for x in range(16) if black(x,y) and (x,y) not in mesh
   and not any(black(x+dx,y+dy) for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)])
   and any((x+dx,y+dy) in mesh for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)])}
  if not endpoints:break
  mesh|=endpoints
 primary=[];detail=[]
 for y in range(24):
  for x in range(16):
   r,_,_,a=at(x,y)
   if not a or (x,y) in mesh:continue
   (detail if r else primary).append(f'<rect x="{x}" y="{y}" width="1" height="1" fill="white"/>')
 for x,y in sorted(mesh):
  primary.append(f'<path d="M{x+.5} {y+.19}L{x+.81} {y+.5} {x+.5} {y+.81} {x+.19} {y+.5}Z" fill="white"/>')
  for dx,dy in [(1,1),(-1,1)]:
   if (x+dx,y+dy) in mesh:primary.append(f'<path d="M{x+.5} {y+.5}l{dx} {dy}" stroke="white" stroke-width=".25"/>')
  # Continue half-struts over genuinely connected tile edges. Source suffix
  # owns connectivity; local alpha bounds never decide a join.
  for dx,dy,allowed in [(-1,-1,x==0 and suffix[6]=='1'),(-1,1,x==0 and suffix[6]=='1'),(1,-1,x==15 and suffix[2]=='1'),(1,1,x==15 and suffix[2]=='1'),(-1,-1,y==0 and suffix[0]=='1'),(1,-1,y==0 and suffix[0]=='1'),(-1,1,y==23 and suffix[4]=='1'),(1,1,y==23 and suffix[4]=='1')]:
   if allowed:primary.append(f'<path d="M{x+.5} {y+.5}l{dx} {dy}" stroke="white" stroke-width=".25"/>')
 def svg(parts):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+''.join(parts)+'</svg>'
 return svg(primary),svg(detail),len(mesh)

if __name__=='__main__':
 index=json.loads((HERE/'native-state-index.json').read_text());raw=Image.open(Path(index['originals'][0]['private_mask']['path'])).convert('RGBA')
 p,d,count=geometry(raw,'00000000')
 for name,svg in [('primary',p),('detail',d)]:
  (HERE/f'constructed-isolated-v2-{name}.svg').write_bytes(svg.encode());(HERE/f'constructed-isolated-v2-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-isolated-v2-{name}.svg'),skip_system_fonts=True))
 layers=[]
 for name,color in [('primary',(145,145,145,255)),('detail',(218,218,218,255))]:
  mask=Image.open(HERE/f'constructed-isolated-v2-{name}.png').convert('RGBA').getchannel('A');im=Image.new('RGBA',mask.size,color);im.putalpha(mask);layers.append(im)
 assembly=Image.alpha_composite(*layers);assembly.save(HERE/'constructed-isolated-v2.png')
 plate=Image.new('RGB',(1152,650),'#142823');draw=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
 draw.text((20,15),'RUSTED METAL / pixel trace correction / welded diamond interpretation',font=font,fill='#e3cf43')
 for x,filename,label in [(70,'constructed-isolated.png','Rejected: disjoint checker marks'),(655,'constructed-isolated-v2.png','Selected: connected welded mesh')]:
  im=Image.open(HERE/filename).convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(x,65),im);draw.text((x,485),label,font=font,fill='#e5e8d8')
 draw.text((20,550),'Native node positions, frame, base braces, color roles and state connections remain the design constraints.',font=font,fill='#e5e8d8')
 draw.text((20,582),'Unseen fine metal construction is authored: checker marks become diamond joints and narrow diagonal welds.',font=font,fill='#e5e8d8');plate.save(HERE/'construction-correction-comparison.png')
 packet=json.loads((HERE/'source-packet.json').read_text());packet['supersedes_authoring_interpretation']=dict(path=(HERE/'source-packet.json').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'source-packet.json').read_bytes()).hexdigest(),reason='Literal checker enlargement produced disconnected squares. Preserve source nodes/frame/braces but reconstruct a coherent welded diamond mesh between those nodes; this is an authored interpretation, not exact native alpha preservation.')
 packet['construction']='Native source contour and color-role cells own frame/base/bracing. Checker-region nodes retain their source positions, reconstructed as diamond joints linked by thin welded diagonal struts. Geometry is source-constrained and deterministic; ImageGen supplies only neutral material.'
 (HERE/'source-packet-v2.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode());print('Rebuilt',count,'checker nodes as source-positioned welded mesh joints.')
