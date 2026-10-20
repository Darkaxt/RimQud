"""Select end steel material without changing shared geometry; stage occupied refinement."""
from pathlib import Path
import json,hashlib,importlib.util,shutil
from datetime import datetime,timezone
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'empty-first-structural-review.json').exists()
rawpath=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-4daf37e5-ef15-4544-b98f-ecdb129454d9.png')
shutil.copyfile(rawpath,HERE/'refined-empty-raw.png');raw=read(HERE/'refined-empty-raw.png')
write(HERE/'empty-first-structural-review.json',dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',generated_file=str(rawpath),raw=ref(HERE/'refined-empty-raw.png'),prompt_file=ref(HERE/'empty-turnaround-prompt.txt'),review='Inspected actual three-view empty refinement before extraction: parallel tabletop/apron, open south/north support holes, full solid end support and restrained steel shading, no stock or donor tools. Generated placement/edge fringe is not geometry. Retain selected S and mirrored N; sample only E material into fixed manual outline, internal divisions and coverage.',frame=list(raw.size),native_validation=False))
helper=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('fixed_material',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
part=raw.crop((round(raw.width/3),0,round(2*raw.width/3),raw.height));part.save(HERE/'empty-generated-east-material-panel.png')
pattern=np.array(read(HERE/'constructed-east-base.png'));own=pattern.copy();own[:,:,:3]=0
selected,stats=m.select(part,own,pattern);selected.save(HERE/'selected-east-base-neutral.png');ImageOps.mirror(selected).save(HERE/'selected-west-base-neutral.png')
write(HERE/'empty-material-selection.json',dict(helper=ref(helper),material_mapping='Equal generated center panel resized to fixed512x768material frame only. Production alpha and dark boundary/division ink taken from constructed end, not generated alpha/bounds.',stats=stats,helper_role_mapping=dict(wood='neutral chrome steel',top='unused'),south='Retained selected v2 material at common0.95registration',north='Mirrored unmarked selected south base',west='Mirrored selected symmetric empty east end',second_isolation_call=False))
sheet=Image.new('RGBA',(1536,1536))
for i,f in enumerate(['south','east','north','west']):
    base=read(HERE/f'selected-{f}-base-neutral.png');base.save(HERE/f'shared-{f}-base-neutral.png');base.alpha_composite(read(HERE/f'constructed-{f}-stock.png'));base.save(HERE/f'occupied-context-{f}.png');sheet.alpha_composite(base,((i%2)*768+128,(i//2)*768))
sheet.save(HERE/'occupied-front-guided-turnaround.png')
(HERE/'occupied-turnaround-prompt.txt').write_bytes('''Use case: sketch-to-render. ONE Qud occupied metal workbench in four cardinal map views. Image1 is the1536x1536 edit target, four768square panels: SOUTH top-left, EAST top-right, NORTH bottom-left, WEST bottom-right. Each panel contains one512x768 registered source cell centered horizontally, transparent margin. Image2 actual VTE TableMachining_east supplies cold-steel contour/shading convention only. Image3 actual Qud source empty/full plate establishes the two source stock marks; do not invent tool identities or machinery.
Description: Steel was anointed with liquid chrome, cooled, and beaten into a flat and workable surface. Preserve the SAME gray empty bench in all panels. Only refine the muted GOLD-key source occupied marks in place: one upright slotted rectangular stock plate and one small round mark. Gold is ownership key, not final native color. Do not repaint/move the bench or add stock. The native tile conveys stock presence, not exact inventory items.
Shared authored bench width13.7,depth7.6,topheight9.15,apron1.4; projection u8+rotated_x,v16.9+(3.4/7.6)*rotated_y-z; one uniform0.95registration around8,16 already applied. Same physical scale and map-camera elevation all directions; parallel planes, no yaw/convergence, no compressed end. Stock plate authored X1.05..3.85,Y1.88..2.68,Z9.15..15; slot through front/back atX1.7..3.15,Z13.049..14.299. Small mark center[-.45,2.148,9.41],radius.26. These are unseen construction estimates, not source item identities.
SOUTH stock stays right, NORTH stock left; slot remains a real transparent opening in S/N. EAST and WEST show solid thin edge of the same plate, no pasted front slot. EAST plate is nearer and fully hides the little round mark; WEST round mark visible in front. The bench end itself is broad, solid and complete, not compressed with the thin stock. S/N source support holes open; E/W support outside face solid. Preserve all overlaps and current geometry.
Refine source marks with subtle beaten metal volume and clean contours to match selected steel base. No extra tool, flask, machine, occupant, cabinet, handle, new hole, background, text or label. Transparent exterior and openings. Same complete1536square sheet, no independent panel fitting, no isolation request.'''.encode())
print('Empty first refinement inspected and retained; fixed E/W steel selected. Occupied same-base target and exact prompt saved.')
