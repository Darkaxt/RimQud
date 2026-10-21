"""Editable, source-layout-bound debris fragments for Garbage's four choices/fallback."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'constructed-family.png').exists();states=read(HERE/'native-state-index.json')['states']
defs='''<defs>
<linearGradient id="metal" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#d8d8d8"/><stop offset=".5" stop-color="#aaaaaa"/><stop offset="1" stop-color="#737373"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f2f2f2"/><stop offset="1" stop-color="#c3c3c3"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2=".5" y2="1"><stop stop-color="#eeeeee"/><stop offset=".4" stop-color="#bdbdbd"/><stop offset=".7" stop-color="#d5d5d5"/><stop offset="1" stop-color="#9b9b9b"/></linearGradient>
</defs>'''
def shape(d,fill='url(#metal)',stroke='#343434',width=.14):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
def stroke(d,c='#444444',w=.12):return shape(d,'none',c,w)
def paper(d,ink):return shape(d,'url(#paper)')+stroke(ink,'#606060',.11)
def lens(x,y,rx,ry,angle=0):
    return f'<g transform="rotate({angle} {x} {y})"><ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#glass)" stroke="#474747" stroke-width=".17"/>'+stroke(f'M{x-rx*.6} {y-ry*.2} Q{x} {y-ry*.9} {x+rx*.65} {y-ry*.3}','#ededed',.12)+stroke(f'M{x-rx*.65} {y+ry*.3} Q{x} {y+ry*.8} {x+rx*.6} {y+ry*.3}','#858585',.1)+'</g>'
def lug(x,y,w,h,angle=0):
    # Irregular acid-nibbled plate and one actual hole; fragments are not modern whole appliances.
    d=f'M{x-w*.5} {y-h*.45} L{x+w*.25} {y-h*.5} L{x+w*.45} {y-h*.3} L{x+w*.37} {y-h*.15} L{x+w*.5} {y+h*.05} L{x+w*.32} {y+h*.48} L{x+w*.1} {y+h*.4} L{x-w*.12} {y+h*.5} L{x-w*.5} {y+h*.28} L{x-w*.39} {y+h*.03} L{x-w*.5} {y-h*.18} Z'
    hole=f'<ellipse cx="{x+w*.08}" cy="{y-h*.09}" rx="{w*.18}" ry="{h*.16}" fill="#696969" stroke="#d4d4d4" stroke-width=".10"/>'
    return f'<g transform="rotate({angle} {x} {y})">'+shape(d)+hole+stroke(f'M{x-w*.27} {y+h*.03} L{x-w*.1} {y+h*.15} M{x+w*.23} {y+h*.15} L{x+w*.30} {y+h*.25}','#777777',.10)+'</g>'
def ribbon(d,w=.85):return stroke(d,'#383838',w+.19)+stroke(d,'#adadad',w)+stroke(d,'#d3d3d3',w*.24)
# Coordinates remain in the source16x24cell. Objects are authored interpretations of ambiguous blobs.
parts=[
 [ribbon('M4.8 2.3 L4.8 4.7 Q3.6 6 3.9 8.3 Q4.1 9.8 6.1 10.5 L11.3 11.1 Q12.7 12 10.4 15.7',1.25),
  paper('M9.7 7.7 L12.9 5.6 L14.6 6.5 L13.2 8.5 L12.9 9.8 L10.7 10.8 L9.9 9.4 Z','M11.1 8.3 L12.7 7.1 M11.8 7.5 L12.5 8.4 M10.7 9.7 L11.8 8.9'),
  lug(11.4,13.7,3.4,5.2,-13),lens(4.2,10.2,2.7,1.35,12),
  lug(2.6,16.5,2.8,1.7,-24),paper('M4.7 18.1 L6.4 17.6 L7.3 19 L8.7 19.6 L8.4 21.2 L6.4 21.0 L5.8 20.2 L3.7 19.5 Z','M5.4 19.0 L6.8 19.3 M6.1 18.9 L5.9 19.9')],
 [paper('M7.4 1.4 L9.0 1.5 L9.4 2.3 L11.4 2.7 L11.2 4.9 L10.2 5.2 L10.0 7.1 L8.6 6.5 L7.3 4.4 Z','M8.0 3.0 L10.3 3.2 M8.6 2.9 L8.7 4.9 L9.4 4.8 M9.8 5.0 L9.6 5.8'),
  lug(3.8,3.9,2.2,3.1,-15),ribbon('M7.6 7.6 Q5.6 8.0 4.0 10.7 Q4.3 12.1 6.1 11.7 L11.2 11.4 Q14.4 11.9 12.5 17.7',1.0),
  lens(5.4,9.8,3.7,1.7,-16),lug(11.8,14.8,4.8,6.5,-8),
  paper('M4.3 17.8 L5.3 17.5 L6.6 18.8 L7.5 19.2 L7.1 20.5 L5.8 20.0 L5.6 19.3 Z','M5.2 18.7 L6.8 19.4')],
 [paper('M4.4 2.4 L5.6 2.4 L6.0 3.2 L8.3 3.7 L8.4 5.6 L7.3 6.4 L6.4 5.4 L5.3 5.1 L5.1 4.2 L4.4 4.2 Z','M5.2 3.8 L7.3 4.2 M6.0 3.9 L5.7 4.9 M6.8 4.3 L7.4 5.1'),
  lug(2.9,6.4,3.0,1.8,27),ribbon('M3.3 17.7 L3.2 14.5 Q4.2 12.6 7.4 13.2 L11.8 12.0 Q14.1 10.8 11.5 7.4',1.2),
  lens(12.0,9.6,2.5,2.6,-14),lug(9.5,13.0,4.9,3.8,-16),
  paper('M11.9 17.9 L12.6 17.8 L13.0 18.7 L14.3 19.4 L14.5 20.7 L13.4 21.0 L12.5 20.0 L12.7 19.1 Z','M12.8 19.6 L13.8 20.1')],
 [paper('M11.6 4.5 L13.1 3.6 L14.4 3.5 L14.5 4.5 L13.0 4.8 L11.9 5.2 Z','M12.4 4.4 L13.8 4.0'),
  lug(5.6,8.0,4.8,2.5,10),ribbon('M3.8 12.2 L3.7 14.8 L2.2 16.3 L2.5 18.5 M4.0 15.0 Q7.1 13.2 10.2 14.7 L13.6 12.6',1.05),
  lens(8.1,14.0,3.7,1.7,-15),lug(8.2,18.7,4.0,6.5,-25),
  paper('M10.9 11.7 L12.3 11.9 L13.3 11.4 L14.5 12.7 L13.8 13.5 L12.3 13.1 L11.6 13.9 L10.7 13.2 Z','M11.6 12.4 L13.3 12.8')],
 [lug(5.7,5.8,2.7,2.4,-12),ribbon('M5.6 7.4 L7.0 8.8 L8.1 8.9 L9.8 10.9 L10.9 12.8',.57),lens(12.4,8.7,1.1,1.5,18),
  paper('M5.3 13.3 L6.6 13.2 L6.4 14.5 L5.0 14.9 L4.9 14.1 Z','M5.4 13.8 L6.2 13.7'),
  shape('M3.8 8.1 L4.4 8.7 L3.9 9.7 L3.3 9.1 Z'),shape('M9.7 11.8 L10.5 12.1 L10.1 13.2 L9.3 12.8 Z'),
  shape('M1.6 7.1 L2.0 7.3 L1.8 7.8 L1.4 7.6 Z'),shape('M11.3 4.4 L11.8 4.4 L11.8 4.9 L11.3 4.9 Z')]
]
controls=[]
for i,(state,objects) in enumerate(zip(states,parts)):
    ident=f'choice-{i+1}' if i<4 else 'fallback';svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+defs+''.join(objects)+'</svg>'
    (HERE/f'{ident}-constructed.svg').write_bytes(svg.encode());(HERE/f'{ident}-constructed.png').write_bytes(svg_to_bytes(svg_string=svg))
    controls.append(dict(id=ident,native_tile=state['native_tile'],source_mask=state['private_mask'],objects=['bent wire/ribbon','torn inked paper fragment','corroded lug/plate','glass lens'],editable=ref(HERE/f'{ident}-constructed.svg'),constructed=ref(HERE/f'{ident}-constructed.png'),
        interpretation='Specific blob-to-material assignments, exact fragment dimensions and hidden surfaces are authored from the source prose; source16x24placement is the anchor, not measured physical junk size.'))
write(HERE/'construction-controls.json',dict(frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],anchor=[8,12],policy='Same full source-cell mapping for all5states. No per-pile bounding-box fitting or imported donor footprint.'),camera='Fixed cardinal map scatter using Core simple shallow map-art shading. No isometric stage, tilted sample slab or perspective camera.',states=controls,
    material_policy='All gray material roles feed the same native K primary tint. Lens highlights/ink/lug/wire are luminance differences, not invented secondary colors. Keep fragment gaps transparent; ^k stays background.',
    state_policy='Four native RandomTile choices plus declared fallback. No adjacency, new rotation, empty/burning/charge state or changed item/scavenge/filth mechanics.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
plate=Image.new('RGB',(1400,1000),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'GARBAGE / original footprint above, editable material interpretation below',font=font,fill='#e3cf43')
for i,state in enumerate(states):
    xx=25+i*275;a=np.array(Image.open(state['private_mask']['path']).convert('RGBA'));a[:,:,:3]=220;source=Image.fromarray(a).resize((224,336),Image.Resampling.NEAREST);plate.paste(source,(xx,55),source)
    im=Image.open(HERE/f'{controls[i]["id"]}-constructed.png').convert('RGBA').resize((224,336),Image.Resampling.LANCZOS);plate.paste(im,(xx,450),im);d.text((xx,810),controls[i]['id'].upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Qud glass lens, ink serif, acid-eaten lug and wire ribbon; exact identities in ambiguous pixels are authored.',
    'Same source-cell placement/scale. No imported cans, bottles, donor palette, generic dense mound or outside shadow.',
    'All material shades are neutral; final native primary K only. Gaps remain transparent; not a background-filled tile.',
    'Fixed-view debris has no furniture turnaround requirement. Native RandomTile selection and behavior remain native.']):d.text((18,870+i*28),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
plate=Image.new('RGB',(1400,520),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'GARBAGE / selected5source-bound piles / fixed native map view',font=font,fill='#e3cf43')
for i,c in enumerate(controls):
    im=Image.open(HERE/f'{c["id"]}-constructed.png').convert('RGBA').resize((224,336),Image.Resampling.LANCZOS);xx=25+i*275;plate.paste(im,(xx,55),im);d.text((xx,420),c['id'].upper(),font=font,fill='#e3cf43')
d.text((18,475),'Quiet gray glass/paper/metal/wire; transparent fragment gaps. No new runtime state or behavior.',font=font,fill='#e5e8d8');plate.save(HERE/'constructed-family.png')
print('Constructed five editable source-layout piles; inspect against original before material refinement.')
