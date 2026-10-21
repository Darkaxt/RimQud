"""Construct a source-bound fractured microchip; preserve native open pockets and cell scale."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'construction-controls.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-SCRAP-ELECTRONICS';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
packet=read(HERE/'source-packet.json');packet['identity']=' -> '.join(n['name'] for n in packet['ancestry']);packet['metadata_correction']='Initial identity summary omitted InorganicObject; original ancestry data already contained all six nodes. This corrected packet uses the complete resolved chain.'
write(HERE/'source-packet-corrected.json',packet)
base='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{}</svg>'
primary='''<g id="primary-frame" stroke-linejoin="round" stroke-linecap="round">
<path d="M4.15 11.78 L7.72 8.12 Q7.92 7.98 8.13 8.16 L8.05 10.12 L7.83 10.46 L8.02 10.91 L7.69 11.15 L7.91 11.76 Z" fill="#d6d6d6" stroke="#353a3a" stroke-width=".12"/>
<path d="M8.17 8.22 L11.73 11.76 M4.23 11.96 L7.92 15.70" fill="none" stroke="#969d9d" stroke-width=".23"/>
<path d="M8.17 8.22 L11.73 11.76 M4.23 11.96 L7.92 15.70" fill="none" stroke="#d7d7d7" stroke-width=".10"/>
<path d="M4.30 11.68 L7.72 8.24" fill="none" stroke="#f2f2f2" stroke-width=".10"/>
<path d="M5.10 11.21 L6.53 9.78 L7.23 9.78 M5.92 11.21 L6.62 10.51 L7.25 10.51" fill="none" stroke="#969b9b" stroke-width=".085"/>
<path d="M6.64 11.22 L7.25 11.22" fill="none" stroke="#818888" stroke-width=".075"/>
<circle cx="7.29" cy="9.78" r=".12" fill="#b4baba"/><circle cx="7.30" cy="10.51" r=".12" fill="#b4baba"/>
</g>'''
detail='''<g id="detail-fragment" stroke-linejoin="round" stroke-linecap="round">
<path d="M8.12 11.98 L8.48 12.12 L8.70 11.91 L9.00 12.10 L9.43 11.95 L11.78 11.94 L8.14 15.77 Z" fill="#b9b9b9" stroke="#353a3a" stroke-width=".12"/>
<path d="M8.29 15.52 L11.57 12.20" fill="none" stroke="#e7e7e7" stroke-width=".095"/>
<path d="M8.64 12.58 L10.39 12.58 L9.45 13.52 L8.67 13.52 M8.65 14.35 L9.08 14.35" fill="none" stroke="#899191" stroke-width=".085"/>
<circle cx="8.62" cy="12.58" r=".11" fill="#d9d9d9"/><circle cx="8.62" cy="13.52" r=".11" fill="#d9d9d9"/>
</g>'''
svg=HERE/'constructed-chip.svg';svg.write_text(base.format(primary+detail),encoding='utf-8');(HERE/'constructed-chip.png').write_bytes(svg_to_bytes(svg_string=svg.read_text()))
import re
def mask(s):return re.sub(r'(fill|stroke)="(?!none)[^"]+"',lambda m:m.group(1)+'="white"',s)
(HERE/'detail-ownership.png').write_bytes(svg_to_bytes(svg_string=base.format(mask(detail))))
(HERE/'primary-ownership.png').write_bytes(svg_to_bytes(svg_string=base.format(mask(primary))))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1280,850),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'FRACTURED MICROCHIP / actual source -> editable manual suggestion',font=font,fill='#e3cf43')
source=np.array(Image.open(packet['original']['private_mask']['path']).convert('RGBA'));g=np.uint8(225-source[:,:,0].astype(float)/255*75);im=Image.fromarray(np.dstack([g,g,g,source[:,:,3]])).resize((384,576),Image.Resampling.NEAREST);plate.paste(im,(30,65),im)
manual=Image.open(HERE/'constructed-chip.png').convert('RGBA');plate.paste(manual,(500,0),manual)
for x,label in [(25,'ACTUAL16x24 / P-D NEUTRAL'),(535,'MANUAL512x768 / ONE CELL')]:d.text((x,660),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Keep two opposing triangular fragments, diamond perimeter and source open fracture pockets.',
 'Light circuit/contact marks and .12unit edge are authored, not canonical machine internals.',
 'Single fixed map view; diagonal shape is intrinsic. No display turntable or independent bounds fit.',
 'Separate primary/detail ownership remains even with equal native C/C tint. No baked cyan.']):d.text((20,710+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'manual-suggestion.png')
controls=dict(source=ref(HERE/'source-packet-corrected.json'),svg=ref(svg),constructed=ref(HERE/'constructed-chip.png'),ownership=dict(primary=ref(HERE/'primary-ownership.png'),detail=ref(HERE/'detail-ownership.png')),
    frame=dict(native=[16,24],master=[512,768],recipient=[256,256],center=[8,12],policy='Full-cell mapping; approximate8x8source-visible extent preserved. No independent crop/bounds fitting.'),
    geometry=dict(outer_extent=[4.09,8.02,11.84,15.83],source='Native P/D diamond layout',authored='Small fracture chips, material thickness/shading and etched traces. Not extra circuits/electrical state.'),
    views='One fixed source-bound map resource view. Other facings/furniture turnaround and clothing assembly are inapplicable.',camera='Cardinal map resource art; intrinsic diamond orientation retained. No new isometric slab or strong perspective.',native_activation=False)
write(HERE/'construction-controls.json',controls)
prompt='''Use case: restrained game sprite refinement, preserving source design.
Input1 is the authoritative manual construction of Qud Scrap Electronics, named fractured microchip, drawn in a single512x768full-cell frame with open pockets and two opposing triangular fragments on a diamond-like fractured perimeter. Input2 is the exact source mask and actual installed RimWorld mod SignalChip reference. Qud description: A piece of scrap was shed or peeled off a machine fossil. It is NOT the RimWorld SignalChip and not an intact modern green circuit board.
Refine input1 as a single flat, thin, fractured electronic fragment in quiet RimWorld resource-art rendering. Keep both opposing triangular surfaces, upper-right/lower-left transparent pockets and the existing broken diamond border. Retain each small circuit/contact mark and fracture edge. Subtle etched surface and shallow edge shading, broad readable values, clean simple outline. Actual RimWorld reference supplies quiet contrast/shallow material shading only; do not copy its rounded white housing, blue rectangles, micro-organ identity or mechtech semantics.
View: one fixed cardinal map resource view. The diamond is the actual object shape, not an invitation to rotate to an isometric presentation or make a three-quarter circuit slab. Preserve the native small source-cell occupancy, center(256,384)in512x768, object visible extent about8x8nativepixels inside16x24cell. Keep the entire object and transparent outer margins.
Neutral grayscale only; source primary and detail both later tint C(cyan)and will stay independent masks. Do not bake cyan/green/gold, draw extra pins, wires, components, glowing LED, letters or a floor/shadow. Maintain truly transparent open pockets and background. No scenery or body. Refine material/outline delicately, not photoreal corrosion or dense hard-to-read grain. Output the single complete sprite in the same frame; no extra angles, board, labels or decorative borders. Canonical constructed geometry and coverage will remain authoritative for registration.'''
(HERE/'refinement-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
def event(step,action,ins,outs,review):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result='PASS'))
event(entry['required_steps'][0],'Correct identity summary to include InorganicObject; preserve original complete ancestry data.',['source-packet.json'],['source-packet-corrected.json'],'The original six-node ancestry was complete; only shorthand identity omitted InorganicObject. Corrected current packet derives identity from actual chain, without changing source behavior.')
event(entry['required_steps'][1],'Inspect actual VTE SignalChip and Biotech Graphic_Single definition as compact material/shading reference.',['source-packet-corrected.json','source-reference.png'],['construction-controls.json'],'Actual reference is resource art, not a creature or furniture. Native fractured diamond/open-pockets shape and C/C palette win; no imported rounded housing, blue rectangles, donor scale or mechanics.')
event(entry['required_steps'][2],'Construct editable fractured diamond with two opposing source P/D regions, border bridges and shallow etched traces.',['source-packet-corrected.json'],['construct-chip.py','constructed-chip.svg','constructed-chip.png','manual-suggestion.png','primary-ownership.png','detail-ownership.png','refinement-prompt.txt'],'Source-centered small8x8extent retained in full16x24cell. Open pockets remain transparent rather than being filled with a generic PCB. Etched traces and fracture edge are explicit authored interpretation. Inspect full shape before refinement.')
event(entry['required_steps'][3],'Resolve required native states and views from complete inherited declaration.',['source-packet-corrected.json'],['construction-controls.json'],'One actual fixed tile, no RandomTile builder or source-supported repaired/burning/stack picture. Non-furniture item: no S/E/N turnaround or clothing assembly is needed. Shared bit11 does not grant other scrap identities readiness.')
entry.update(current_step=entry['required_steps'][4],known_issues=['Inspect manual source-bound fracture/open pockets and exact prompt before actual refinement; no generation-ready credit.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Built source-bound fractured microchip with separate ownership and exact prompt.')
