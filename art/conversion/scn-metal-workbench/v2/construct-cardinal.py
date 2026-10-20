"""Reconstruct the source bench in a cardinal, parallel-edged sprite camera."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
assert not (HERE/'source-packet.json').exists(),'Preserve logged authoring outputs'
packet=json.loads((OLD/'source-packet.json').read_text(encoding='utf-8'))
packet.update(supersedes=asset(OLD/'source-packet.json'),camera=dict(facing='south/front',projection='Fixed shallow orthographic-style cardinal presentation; parallel tabletop boundaries and vertical supports. No yaw, diagonal footprint, converging edges or per-state camera changes.',reference='The actual named VTE TableMachining_south graphic provides a cardinal rectangular work-surface convention. Qud trapezoid source contour is reprojected, not copied as a camera.',identity_boundary='Retain chrome-steel material, shallow apron, broad perforated supports and source-shaped occupied markers. Camera reconstruction does not change native states or add four-way rotation.'),construction='Source parts reconstructed in the locked south camera: rectangular top with parallel edges, straight apron and broad slotted supports joined underneath. Upright slotted stock component stays straight front, with no angled side panel. Exact fine joinery and stock identity remain authored/unknown.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
for state in ['empty','occupied','stock']:
 svg=(OLD/f'constructed-{state}.svg').read_text()
 if state!='stock':
  assert 'M3.95 6.05H12.05L14.85 9.45H1.15Z' in svg
  svg=svg.replace('M3.95 6.05H12.05L14.85 9.45H1.15Z','M1.15 6.05H14.85V9.45H1.15Z')
 # Eliminate the marker's thin oblique side-panel cue; retain one shallow highlight.
 svg=svg.replace('<path d="M9.05 3.1L9.4 2.9H12.1L11.85 3.1V8.95L12.1 8.7V2.9" fill="#b5a64e" stroke-width=".1"/>','')
 (HERE/f'constructed-{state}.svg').write_bytes(svg.encode());(HERE/f'constructed-{state}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{state}.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,810),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'METAL WORKBENCH / camera correction / parallel rectangular top + source supports + native stock marker',font=font,fill='#e3cf43')
for x,p,label in [(35,OLD/'constructed-empty.png','Rejected taper / prior camera'),(510,HERE/'constructed-empty.png','Corrected south / parallel edges'),(985,HERE/'constructed-occupied.png','Occupied construction / same camera')]:
 im=Image.open(p).convert('RGBA').resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,70),im);d.text((x,535),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Object identity is retained while the source trapezoid is reconstructed in the target cardinal camera.',
 'Both states share one full-cell frame, steel supports and apron. Gold identifies stock ownership only.',
 'No new game state, craft interaction, camera-dependent stretch or independent component centering.',
 'Older image/prompt/construction remains preserved as rejected camera evidence.']):d.text((20,615+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'camera-construction-comparison.png')
