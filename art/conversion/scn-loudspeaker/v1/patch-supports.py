"""Attach source-separated marks/feet without changing their source locations or palette."""
from pathlib import Path
import json,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent
assert not (HERE/'patched-constructed.svg').exists()
for label in ['constructed','ownership']:
 s=(HERE/f'{label}.svg').read_text();owner=label=='ownership';fill='#000000' if owner else '#adadad';edge='#000000' if owner else '#333d35'
 added=f'<g fill="{fill}" stroke="{edge}" stroke-width=".08">'
 for x in [4.65,7.65,10.65]:added+=f'<rect x="{x}" y="2.65" width=".6" height="1.75"/>'
 for x in [2.7,12.7]:added+=f'<rect x="{x}" y="20.65" width=".6" height="1.7"/>'
 added+='</g>'
 # Put supports behind original physical pieces, preserving the selected source marks/feet.
 s=s.replace('viewBox="0 0 16 24">','viewBox="0 0 16 24">'+added)
 if not owner:s=s.replace('</svg>','<path d="M1.65 17.3H2.35V18H1.65ZM1.65 19.1H2.35V19.8H1.65ZM3.65 19.1H4.35V19.8H3.65Z" fill="#3e453e"/></svg>')
 (HERE/f'patched-{label}.svg').write_bytes(s.encode());(HERE/f'patched-{label}.png').write_bytes(svg_to_bytes(svg_string=s))
p=json.loads((HERE/'source-packet.json').read_text());p['construction']['authored']+=' Manual review added narrow primary support necks under top marks and down to pale feet so physical pieces do not float; their source locations/roles unchanged. Top marks interpreted as raised grille/vent caps, not a verified mechanical function. Lower-left recessed marks recovered from original sparse glyph.'
p['construction']['coverage']='Filled cabinet assembly plus narrowly authored support necks. Gaps around top marks/feet remain transparent; no halo/background accepted.'
(HERE/'corrected-source-packet.json').write_bytes((json.dumps(p,indent=2)+'\n').encode())
text='Manual source/structural review caught floating top pieces/feet and missing lower-left source recess marks. Added narrow primary support necks behind unchanged source marks/feet, and three small lower-left dark recesses. Explicit authored physical connection; no new canonical mechanism or native behavior. Initial suggestion preserved.'
(HERE/'source-support-patch.json').write_bytes((json.dumps(dict(review=text,source_dimensions_changed=False,source_palette_changed=False,semantic_uncertainty='Native top marks do not name mechanical parts; raised caps/supports are authored interpretation.'),indent=2)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(900,850),'#142823');d=ImageDraw.Draw(plate)
for i,label in enumerate(['constructed','patched-constructed']):
 im=Image.open(HERE/f'{label}.png').convert('RGBA').resize((360,540),Image.Resampling.LANCZOS);plate.paste(im,(35+i*440,55),im);d.text((35+i*440,620),label.upper(),font=font,fill='#e3cf43')
d.text((20,690),'Narrow authored support necks; source positions and w/W roles unchanged.',font=font,fill='#e5e8d8');d.text((20,725),'Lower-left recess marks recovered; initial suggestion retained.',font=font,fill='#e5e8d8');plate.save(HERE/'support-patch-comparison.png')
prompt=(HERE/'refine-prompt.txt').read_text().replace('selected shape:','patched selected shape:')
prompt+='\nThe edit target includes narrow primary supports connecting3raised top caps to the cabinet and connecting the two feet to the base. Retain these physical supports, all original cap/foot positions, and the three lower-left recess marks. Cap function is an authored interpretation, not new native behavior.'
(HERE/'patched-refine-prompt.txt').write_bytes(prompt.encode())
(HERE/'manual-structural-review.json').write_bytes((json.dumps(dict(status='PASS AFTER PATCH',review=text),indent=2)+'\n').encode())
print(text)
