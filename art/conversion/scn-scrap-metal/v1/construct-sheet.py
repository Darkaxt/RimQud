"""Construct source-bound bent sheet with curled facets and separate P/D ownership."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'construction-controls.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-SCRAP-METAL';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);source=read(HERE/'source-packet.json')
primary='''<g id="primary-sheet" stroke-linejoin="round" stroke-linecap="round">
<path d="M4.16 11.76 L7.71 8.14 Q7.93 7.98 8.15 8.16 L8.02 11.68 Q6.40 11.25 4.16 11.76Z" fill="#d3d3d3" stroke="#343838" stroke-width=".13"/>
<path d="M4.32 11.62 L7.73 8.29" fill="none" stroke="#ededed" stroke-width=".10"/>
<path d="M5.06 10.94 Q6.31 10.46 7.48 8.74 Q7.03 10.65 5.06 10.94Z" fill="#bdbdbd"/>
<path d="M4.16 11.76 Q6.40 11.25 8.02 11.68 L8.13 12.02 Q6.36 11.62 4.24 11.98Z" fill="#a0a0a0" stroke="#4e5353" stroke-width=".08"/>
<path d="M4.30 11.79 Q6.25 11.40 7.90 11.74" fill="none" stroke="#f0f0f0" stroke-width=".08"/>
<path d="M8.12 8.22 L11.81 11.95 M4.25 11.98 L8.19 15.77" fill="none" stroke="#929797" stroke-width=".22"/>
<path d="M8.12 8.22 L11.81 11.95 M4.25 11.98 L8.19 15.77" fill="none" stroke="#d6d6d6" stroke-width=".09"/>
<path d="M6.14 10.94 L6.76 10.66 M7.19 9.36 L7.48 9.10" fill="none" stroke="#babdbd" stroke-width=".045"/>
</g>'''
detail='''<g id="detail-sheet" stroke-linejoin="round" stroke-linecap="round">
<path d="M8.13 12.06 Q9.91 12.62 11.81 11.95 L8.19 15.77Z" fill="#bdbdbd" stroke="#343838" stroke-width=".13"/>
<path d="M8.13 12.06 Q9.91 12.62 11.81 11.95 L11.53 12.29 Q9.80 12.96 8.15 12.40Z" fill="#e0e0e0"/>
<path d="M8.40 15.42 L11.51 12.30" fill="none" stroke="#e8e8e8" stroke-width=".09"/>
<path d="M8.61 14.68 Q8.79 13.27 10.27 13.12 Q9.15 13.92 8.61 14.68Z" fill="#a2a2a2"/>
<path d="M8.65 13.08 L9.22 13.20 M9.34 13.73 L9.73 13.40" fill="none" stroke="#cfd1d1" stroke-width=".045"/>
</g>'''
base='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{}</svg>'
svg=HERE/'constructed-sheet.svg';svg.write_text(base.format(primary+detail),encoding='utf-8');(HERE/'constructed-sheet.png').write_bytes(svg_to_bytes(svg_string=svg.read_text()))
for name,fragment in [('primary',primary),('detail',detail)]:
    fragment=re.sub(r'(fill|stroke)="(?!none)[^"]+"',lambda m:m.group(1)+'="white"',fragment);(HERE/f'{name}-ownership.png').write_bytes(svg_to_bytes(svg_string=base.format(fragment)))
controls=dict(source=ref(HERE/'source-packet.json'),svg=ref(svg),constructed=ref(HERE/'constructed-sheet.png'),ownership={name:ref(HERE/f'{name}-ownership.png') for name in ['primary','detail']},frame=source['registration'],
    source_bound='Two opposing triangular P/D surfaces, open quadrants and fine diamond perimeter preserved. Curled sheet edge, broad dent/fold and shallow scratches are authored interpretations of bent metal sheet, not Qud dimensions.',
    camera='One fixed source-bound cardinal map-resource view. Intrinsic diamond outline is not an oblique camera; use shallow broad facet shading without tilted display slab.',
    views='One declared native tile; no additional directions, stack-count art, repaired/burning variants or apparel integration required.',native_activation=False)
write(HERE/'construction-controls.json',controls)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1260,850),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'BENT METAL SHEET / actual source -> manual metal folds, no circuitry',font=font,fill='#e3cf43')
a=np.array(Image.open(source['original']['private_mask']['path']).convert('RGBA'));g=np.uint8(225-a[:,:,0].astype(float)/255*75);im=Image.fromarray(np.dstack([g,g,g,a[:,:,3]])).resize((384,576),Image.Resampling.NEAREST);plate.paste(im,(30,65),im);manual=Image.open(HERE/'constructed-sheet.png').convert('RGBA');plate.paste(manual,(500,0),manual)
for x,label in [(25,'ACTUAL16x24 / P-D NEUTRAL'),(535,'EDITABLE512x768 / ONE CELL')]:d.text((x,660),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Source identity is bent metal sheet; no electronic traces, pads or invented chip components.',
 'Curled edges and broad dents interpret the two occupied source surfaces; both open pockets remain.',
 'Primary B and detail C remain independent masks; source size/center and fixed map view retained.',
 'Refinement follows canonical geometry: no repaired panel, lump, stack, extra direction or apparel.']):d.text((20,710+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'manual-suggestion.png')
prompt='''Use case: restrained source-bound game sprite material refinement.
Input1 is the authoritative editable construction for Qud Scrap Metal, display name bent metal sheet. Input2 is the original mask, actual source B/C palette and real installed Vanilla Textures Expanded Steel_a reference. Source description: A piece of scrap was shed or peeled off a machine fossil. Preserve THIS bent sheet, not a rounded steel nugget or a fractured electronic chip.
Refine input1 with simple RimWorld resource-art metallic facets, broad quiet folds/dents and thin curled sheet edges. Keep its two opposing triangular sheet surfaces, diamond perimeter bridges, source size/center and shallow authored creases. No circuit traces, contact pads, pins, wires, electronic components, bolts, armor plate stack or complete square panel. The donor supplies restrained material/shading convention only, not its rounded shape or brown palette.
The upper-right and lower-left internal quadrants are OPEN AIR: preserve real alpha0 transparency in both pockets and in all outer background. Do not fill them with grey glass, a second face, translucent plastic, darkness, haze, glow or cast shadow. No particles. Background must be truly transparent. Existing thin perimeter bridges must touch both sheet fragments without a gap.
One fixed cardinal map-resource view; intrinsic diamond orientation is the source object shape, not a request for isometric/three-quarter camera or a tilted material slab. Neutral grayscale only, no blue/cyan/brown baked in. Actual native primary B and detail C will be applied using independent masks later.
Keep the complete512x768full-cell frame and center(256,384), approximately8x8nativepixel object extent inside16x24cell, transparent margins. No crop-to-bounds, extra angles, labels, scenery or body. Clean smooth simple outline, broad readable shading, no photoreal mirror shine, dense rust, thick pixel-art borders or ambient halo. Canonical manual geometry and coverage remain authoritative for registration.'''
(HERE/'refinement-prompt.txt').write_text(prompt+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat()
def event(step,action,outs,review):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'source-reference.png')],outputs=[ref(HERE/n) for n in outs],review=review,result='PASS'))
event(entry['required_steps'][1],'Inspect actual installed VTE Steel_a and Core Steel resource definition; record material-only reference.',['construction-controls.json'],'Reference rounded lump is not a whole bent-sheet equivalent. Use only broad metal facets/shading; do not import nugget geometry, dull brown palette, stack-count variants, metallurgy or donor physical size.')
event(entry['required_steps'][2],'Construct editable bent sheet with source-opposing regions, open pockets, continuous rim contacts and shallow curled folds.',['construct-sheet.py','constructed-sheet.svg','constructed-sheet.png','manual-suggestion.png','primary-ownership.png','detail-ownership.png','refinement-prompt.txt'],'Native source silhouette/occupancy and B/C ownership govern. Folds/dents are authored; electronics traces/pads are excluded despite same source tile as Scrap Electronics. Inspect before actual refinement.')
event(entry['required_steps'][3],'Resolve complete source-supported state and view requirements.',['construction-controls.json'],'One fixed native bit11 resource view. No inherited RandomTile, furniture directions, clothing fit, stack image or hypothetical repair/burning state. Exact Scrap Metal binding stays separate from other bit11 identities.')
entry.update(current_step=entry['required_steps'][4],known_issues=['Inspect bent source geometry and exact prompt before actual material refinement; no generation-ready credit.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Built editable bent metal sheet, source P/D masks, complete required fixed view and exact refinement prompt.')
