"""Correct the first spaced-mat sketch: corner glyphs are accents, not deck holes."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
p=json.loads((HERE/'source-packet.json').read_text());p['supersedes_authoring_frame']=asset(HERE/'source-packet.json')
p['frame']=dict(native=[16,24],manual=[512,768],recipient=[256,256],panel_origins=[[8*c,6*r] for r in range(4) for c in range(2)],panel_extent=[8,6],
 interpretation='Native L marks are inset surface accents, not physical panel origins/holes. Keep eight contiguous three-slat mats, separated only by narrow .2-native-unit joints. All four cosmetic variants share this traversable deck coverage.')
p['construction']='Continuous dried-stalk deck made from eight three-slat mats in the shared native cell frame. Original L locations supply worn edge accents; first widely spaced sketch was rejected as stepping islands.'
(HERE/'source-packet-v2.json').write_bytes((json.dumps(p,indent=2,ensure_ascii=False)+'\n').encode())
defs='<defs><linearGradient id="fiber" x2="0" y2="1"><stop stop-color="#636363"/><stop offset=".25" stop-color="#d0d0d0"/><stop offset=".55" stop-color="#b6b6b6"/><stop offset="1" stop-color="#6b6b6b"/></linearGradient></defs>'
def mat():
 out=[]
 for j in range(3):
  y=j*2+.1
  out.append(f'<path d="M.1 {y+.05}Q2.5 {y-.02} 4 {y+.04}T7.87 {y+.05}L7.91 {y+1.73}Q5.5 {y+1.87} 3.8 {y+1.78}T.08 {y+1.74}Z" fill="url(#fiber)" stroke="#414141" stroke-width=".07"/>')
  out.append(f'<path d="M.3 {y+.46}Q2.5 {y+.31} 4.4 {y+.43}T7.7 {y+.40} M.4 {y+1.04}Q3 {y+.91} 4.3 {y+1.03}T7.5 {y+1.02}" fill="none" stroke="#dedede" stroke-width=".04"/>')
 return ''.join(out)
single='<svg xmlns="http://www.w3.org/2000/svg" width="768" height="576" viewBox="0 0 8 6">'+defs+mat()+'</svg>'
deck='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+defs+''.join(f'<g transform="translate({x} {y})">{mat()}</g>' for x,y in p['frame']['panel_origins'])+'</svg>'
for name,svg in [('constructed-mat-v2',single),('constructed-deck-v2',deck)]:
 (HERE/(name+'.svg')).write_bytes(svg.encode());(HERE/(name+'.png')).write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/(name+'.svg')),skip_system_fonts=True))
plate=Image.new('RGB',(1280,690),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((20,16),'DECK CONSTRUCTION CORRECTION / native corner glyphs are accents, not missing physical panels',font=font,fill='#e3cf43')
for i,(name,label) in enumerate([('constructed-deck.png','REJECTED / stepping islands'),('constructed-deck-v2.png','SELECTED / contiguous dried-stalk deck')]):
 im=Image.open(HERE/name).convert('RGBA').resize((320,480),Image.Resampling.LANCZOS);plate.paste(im,(110+i*640,75),im);d.text((30+i*640,590),label,font=font,fill='#e5e8d8')
plate.save(HERE/'construction-correction-comparison.png')
