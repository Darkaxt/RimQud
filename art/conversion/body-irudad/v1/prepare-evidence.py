"""Show source, actual human reference and separate construction while refinement runs."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
packet=json.loads((HERE/'source-packet.json').read_text());font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
a=np.array(Image.open(packet['original']['private_mask']['path']).convert('RGBA'));weight=a[:,:,:1].astype(float)/255
color=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
original=Image.fromarray(np.dstack([np.uint8(np.round((1-weight)*color('r')+weight*color('w'))),a[:,:,3]]))
out=Image.new('RGB',(1380,900),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'IRUDAD > human / older base > separate mutation anatomy',font=font,fill='#e3cf43')
original=original.resize((160,240),Image.Resampling.NEAREST);out.paste(original,(45,100),original)
for i,name in enumerate(['human-body-south.png','human-body-east.png']):
    p=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/name
    im=Image.open(p).convert('RGBA').resize((160,160),Image.Resampling.NEAREST);out.paste(im,(270,80+i*200),im)
for p,x in [('baseline-south.png',550),('patched-construction-south.png',920)]:
    im=Image.open(HERE/p).convert('RGBA').resize((240,593),Image.Resampling.LANCZOS);out.paste(im,(x,55),im)
for x,label in [(25,'ORIGINAL QUD r/w'),(250,'ACTUAL CORE S / E'),(515,'REUSED OLDER BASE'),(890,'MANUAL SEPARATE ADDITIONS')]:d.text((x,675),label,font=font,fill='#e3cf43')
lines=['Native: old face, hunched back, second raised arm pair, interlaced mouthless hands-face, short barb-crowned tail.',
       'No close whole-body RimWorld equivalent. Core reference supplies ordinary human outline/shading convention only.',
       'Body and head pixels are unchanged. Add240 transparent pixels above; original world scale/contact remain fixed.',
       'No extra Head node, no tail in the reusable race body, no clothes or personal cosmetics. Native binding untested.',
       'Hand201/6 holds the captured stick; neutral raised-pair/Hands-Face pose does not establish the equipped pose.']
for i,line in enumerate(lines):d.text((18,725+i*30),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-reference-construction.png')
now=datetime.now(timezone.utc).isoformat();ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='BODY-IRUDAD'
e=next(e for e in ledger['entries'] if e['id']=='BODY-IRUDAD');assert not e['process_log']
def event(step,action,ins,outs,review,result='PASS',**extra):e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result,**extra))
event(e['required_steps'][0],'Resolve ElderBob507 race, source description, exact captured mutation topology and shared older-human baseline.',[],['source-packet.json','source-reference-construction.png'],'Native HumanoidWithHandsFace, four Arm/Hand pairs, Hands-Face211 under Hands210 and Tail214/Stinger preserved. Source description and original r/w glyph retained. Extra arms/tail stay separate from reusable human age template; actual equipped Hand201/6 pose unresolved.')
event(e['required_steps'][1],'Inspect actual Core directional human body/head references; reuse their established presentation through the selected older-human baseline.',['source-packet.json'],['source-reference-construction.png'],'Exact private reference hashes retained. No close whole mutant equivalent claimed; Core is only an ordinary human rendering reference, not anatomy authority.')
event(e['required_steps'][2],'Construct independent raised arms, joined-hands face and barbed tail over unchanged older-human body/head pixels.',['source-packet.json'],['construct-irudad.py','constructed-south.png','constructed-turnaround.png','manual-anatomy-review.json'],'All three editable cardinal constructions preserve the base, two ordinary arms and paired feet. Top padding preserves physical scale/contact. Manual first inspection found side tail root gap and north tail incorrectly hidden by legs; these are corrected in the next recorded action.')
event(e['required_steps'][2],'Correct the side tail attachment and north tail depth before contextual refinement.',['constructed-turnaround.png'],['patch-construction.py','patched-tail-east.svg','patched-construction-turnaround.png','construction-corrections.json'],'Viewed corrected sheet: side tail root now meets posterior hip; north tail visible above back-facing body, front/side behind. Front anchor, base pixels and four-arm count retained. Finger interlacing remains a refinement target.')
event(e['required_steps'][3],'Request actual ImageGen front-guided side/back and restrained contextual refinement with native anatomy and fixed baseline constraints.',['secondary-views-prompt.txt','patched-construction-turnaround.png'],['prepare-evidence.py'],'Actual built-in request is running; no generated result or PASS credited yet. Requested transparent grayscale sheet with strict S/E/N, four arms total, interlaced mouthless hands-face and posterior barbed tail. No isolation request.',result='IN PROGRESS',tool='image_gen.imagegen',prompt_file=ref(HERE/'secondary-views-prompt.txt'),referenced_image_paths=[str(HERE/'patched-construction-turnaround.png'),'E:/Temp/qud-transplant-probe-pawns-20261019/donor/human-body-south.png'],transparent_background=True)
e['current_step']=e['required_steps'][3];e['known_issues']=['Mutation art refinement pending. Exact raised-pair/Hands-Face versus captured equipped Hand201/6 pose remains unresolved on NPC-ELDERBOB; no slot renamed or native anatomy acceptance claimed.'];ledger['updated_at']=now
write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Recorded source, donor decision, original and corrected manual views, and actual pending generation request.')
