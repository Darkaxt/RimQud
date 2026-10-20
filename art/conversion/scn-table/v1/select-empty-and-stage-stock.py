"""Retain exact empty table geometry and prepare each native stock variant in context."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,importlib.util
import numpy as np
from scipy import ndimage
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'empty-first-structural-review.json').exists();rawpath=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-0eaa9841-93f1-4803-a3a4-cbc5eaebed93.png');shutil.copyfile(rawpath,HERE/'refined-empty-raw.png');raw=read(HERE/'refined-empty-raw.png');write(HERE/'empty-first-structural-review.json',dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',generated_file=str(rawpath),raw=ref(HERE/'refined-empty-raw.png'),prompt_file=ref(HERE/'patched-empty-turnaround-prompt.txt'),review='Inspected actual S/E/N empty refinement before extraction: simple wood table with grain/knots, parallel top/apron, connected end supports/low stretcher and corrected near-end occlusion; no inventory, donor drawers or extra mechanics. Keep fixed construction coverage/ink and exclude generated fringes/placement changes.'))
hp=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('material',hp);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);a=np.array(raw);labels,n=ndimage.label(a[:,:,3]>128);parts=[]
for k in range(1,n+1):
 ys,xs=np.where(labels==k)
 if len(xs)>1000:parts.append((len(xs),(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)))
parts=sorted(sorted(parts,reverse=True)[:3],key=lambda x:x[1][0]);assert len(parts)==3;stats={}
for f,(_,box) in zip(['south','east','north'],parts):
 pattern=np.array(read(HERE/f'patched-{f}-base.png'));own=pattern.copy();own[:,:,:3]=0;target=Image.fromarray(pattern).getbbox();sample=Image.new('RGBA',(512,768));sample.alpha_composite(raw.crop(box).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.LANCZOS),(target[0],target[1]));sample.save(HERE/f'empty-{f}-mapped-material.png');master,values=m.select(sample,own,pattern);master.save(HERE/f'selected-{f}-base-neutral.png');stats[f]=dict(source_material_bounds=box,target_material_extent=target,selection=values,geometry='Exact patched base alpha and structural ink; bounds map RGB sampling coordinates only, not production fitting.')
ImageOps.mirror(read(HERE/'selected-east-base-neutral.png')).save(HERE/'selected-west-base-neutral.png');write(HERE/'empty-material-selection.json',dict(helper=ref(hp),views=stats,west='Mirror symmetric unmarked empty E base only.',second_isolation_call=False));packet=json.loads((HERE/'source-packet.json').read_text())
for k in range(1,5):
 state=f'occupied-{k}';sheet=Image.new('RGBA',(1536,1536))
 for i,f in enumerate(['south','east','north','west']):
  im=read(HERE/f'selected-{f}-base-neutral.png');im.alpha_composite(read(HERE/f'{state}-{f}-stock.png'));im.save(HERE/f'{state}-{f}-context.png');sheet.alpha_composite(im,((i%2)*768+128,(i//2)*768))
 sheet.save(HERE/f'{state}-front-guided-turnaround.png')
 extra={1:'Tall narrow-neck stock at left and a smaller upright stock near center; only these2forms.',2:'Broad rectangular stock body and open right handle. S/N opening remains open; E/W show physical thin/occluded edge, never a pasted front handle.',3:'Large rounded-shoulder/narrow-top stock at right, small left upright form and one tiny mark; only these3forms.',4:'Broad left stock with open right frame and2unequal uprights. Keep actual bar/frame lengths and open S/N slot; E/W have edge/occlusion rather than a pasted front frame.'}[k]
 prompt=f'''Use case: sketch-to-render. ONE Qud ordinary TABLE native {state.upper()} appearance, same fixed gray wood table with its source stock in four cardinal map views. Image1 is1536square edit target,768square panels SOUTH top-left,EAST top-right,NORTH bottom-left,WEST bottom-right. Each contains full512x768source cell centered horizontally. Image2 actual native5state plate establishes only the selected {state} shape. Image3 actual VTE EndTable east is style reference only, no donor drawers.
Source shape: {packet['stock_features'][state]} {extra} These are unrecognized native stock marks, not identified inventory items. Do not add labels, tools, specific equipment identity or new parts. Gold is a temporary OWNERSHIP KEY only; retain gold-key stock with gentle form/shading and crisp contour, gray selected wood base unchanged. Do not repaint, replace, shift or scale table, move stock or change their overlap.
Shared authored table width14/depth8/height9.3/slab.7; u8+rotated_x,v18+.45*rotated_y-z. Same physical dimensions/elevation/scale/pivot8,16 for every view. Stock parameter projection is already in target; preserve its actual shape/placement, unseen depths are authored. Same broad source top, simple trestle end boards/splayed feet/low central stretcher. Side end full8depth, no compressed panel or converging tabletop. Keep crossbar behind outside end board.
Refine only stock material/form coherently in context, no extra objects/straps/arms, no random matching of color to item identity, no native state change. Native Inventory separately chooses one of4occupied tiles and independent C,c,y,W detail; this call is ONE shape, not4random variants. Transparent background and genuine stock openings/exterior; no backdrop/glow/cast shadow/text. Same1536square sheet, no independent bounds fitting and no second isolation request.'''
 (HERE/f'{state}-turnaround-prompt.txt').write_bytes(prompt.encode())
print('Selected shared empty table and staged each of four real stock appearances in same bases/frames.')
