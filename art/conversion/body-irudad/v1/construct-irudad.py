"""Construct separate Irudad mutation proposals on the unchanged older-human body."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, re, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
SIZE=(512,1264); PAD=240; CONTACT=[256,1190]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='BODY-IRUDAD'
base_entry=next(e for e in ledger['entries'] if e['id']=='BODY-HUMAN-MALE-OLDER');assert base_entry['generation_ready']
base_ref=base_entry['current_registration']['model'];base=json.loads((ROOT/base_ref['path']).read_text());assert ref(ROOT/base_ref['path'])==base_ref
sources=json.loads((ROOT/'art/village/sources.json').read_text());source=next(r for r in sources['actors'] if r['creature']=='ElderBob');actor=source['native_instances'][0];assert actor['instance']==507
original=next(r for r in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if r['blueprint']=='ElderBob')
donor=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');mask=donor/original['reference_file'].replace('-reference','-mask');assert private(mask)['sha256']==original['native_mask_sha256']
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base')
creatures=definitions/'ObjectBlueprints/Creatures.xml';bodies=definitions/'Bodies.xml'
native=re.search(r'<object\s+Name="ElderBob"[^>]*>.*?</object>',creatures.read_text(encoding='utf-8-sig'),re.S).group()
anatomy=re.search(r'<anatomy\s+Name="HumanoidWithHandsFace"[^>]*>.*?</anatomy>',bodies.read_text(encoding='utf-8-sig'),re.S).group()
donors=[]
for name in ['human-body-south.png','human-body-east.png','human-body-north.png','human-head-south.png']:
    p=donor/name;donors.append(dict(**private(p),role='Actual Core humanlike silhouette/outline and limb shading convention only; no equivalent hands-face or barbed mutant tail claimed.'))
packet=dict(entry='BODY-IRUDAD',recorded_at=datetime.now(timezone.utc).isoformat(),identity_chain=source['lineage'],captured_actor={k:v for k,v in actor.items() if k!='parts'},
    source=ref(ROOT/'art/village/sources.json'),source_snapshot=sources['runtime_catalogue_sha256'],native_parts=actor['parts'],original=dict(**original,private_mask=private(mask)),
    definitions=[dict(**private(creatures),fragment=native),dict(**private(bodies),fragment=anatomy)],baseline=base_ref,baseline_history=ref(ROOT/'art/conversion/body-human-male-older/v1/source-packet.json'),
    donor_references=donors,donor_limits='Core human presentation retained. No close installed whole-body equivalent for a four-armed elder whose joined hands form a second face; use exact Qud anatomy and authored separate additions.',
    anatomy=dict(baseline='Unchanged selected unmutated older-human body/head; its two arms/hands and paired feet remain intact.',additions='Exactly one extra pair of arms, joined/interlaced hands forming a mouthless face with desert-white eyes; one short barb-crowned tail. No extra legs or head graft.',
    native_semantics='Hands-Face211 is a Face variant under Hands210, not an additional Head node. Preserve all exact part IDs/parents/managers/lateralities. Raised-pair geometry is a description-based neutral visual pose, not proof of a bone/part-to-limb mapping.',
    attachment_uncertainty='Captured Walking Stick541 occupies changed Hand201/6. This unarmed anatomy proposal does not establish how that equipped hand and the hands-face pose coexist. Resolve exact attachment/pose in NPC-ELDERBOB authoring; do not silently rename it to another hand.'),
    frame=dict(canvas=list(SIZE),padding_top=PAD,contact=CONTACT,baseline_canvas=[512,1024],baseline_contact=[256,950],method='Integer transparent top padding only. Original body/head pixels remain unchanged at y+240. Preserve world position/scale by extending render height and center consistently; equipment inherits the same pad.',
    width=base['views']['south'][0]['width'],height=base['views']['south'][0]['height']*1264/1024,center_x=0,center_z=base['views']['south'][0]['center_z']+120*base['views']['south'][0]['height']/1024),
    authored_interpretation='Raised-arm curves, exact interlacing pattern, barb count and unseen tail curvature are authored. Keep intrinsic anatomy and count source-bound. Tail is posterior; back of hands has no second set of eyes.',
    workflow='Source-bound separate mutation art over existing unmutated body. No race-body replacement, renderer/framework, profession pose, personal cosmetics or game launch.',native_activation=False,native_acceptance='Pending full-set generation and integrated anatomy/equipment/visibility/hurt/look/save review.')
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def path(d,fill='#dddddd',stroke='#292e2b',width=8):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
def svg(parts):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1264" viewBox="0 0 512 1264">'+''.join(parts)+'</svg>'
def save_svg(name,parts):
    source=svg(parts);(HERE/(name+'.svg')).write_bytes(source.encode());(HERE/(name+'.png')).write_bytes(svg_to_bytes(svg_string=source))
front_arms=[path('M155 490 Q81 450 57 345 Q42 270 85 222 L180 122 L208 151 L119 254 Q102 279 121 333 Q140 387 184 435 Z'),
            path('M357 490 Q431 450 455 345 Q470 270 427 222 L332 122 L304 151 L393 254 Q410 279 391 333 Q372 387 328 435 Z')]
front_face=[path('M176 133 Q190 93 221 101 L248 84 Q267 78 286 96 Q320 91 337 128 L326 177 Q290 213 255 204 Q217 207 181 179 Z'),
            path('M182 130 Q218 124 249 151 M183 147 Q220 141 252 168 M326 124 Q294 132 264 151 M329 143 Q297 147 266 168 M216 104 L255 127 L289 103',fill='none',stroke='#737873',width=5),
            '<ellipse cx="222" cy="170" rx="14" ry="11" fill="#ffffff" stroke="#292e2b" stroke-width="5"/><ellipse cx="289" cy="170" rx="14" ry="11" fill="#ffffff" stroke="#292e2b" stroke-width="5"/>']
front_tail=[path('M329 867 Q431 922 424 1035 Q415 1122 456 1152 L480 1130 L475 1172 L452 1163 L442 1187 L427 1165 Q378 1115 381 1040 Q379 952 314 915 Z')]
back_arms=front_arms
back_face=[path('M176 133 Q190 93 221 101 L248 84 Q267 78 286 96 Q320 91 337 128 L326 177 Q290 213 255 204 Q217 207 181 179 Z'),
           path('M183 132 Q219 143 255 172 M187 152 Q223 161 249 187 M326 130 Q292 142 260 167 M324 151 Q290 164 267 188 M211 107 L252 138 L293 107',fill='none',stroke='#737873',width=5)]
back_tail=[path('M247 879 Q322 908 362 1009 Q399 1096 355 1150 L372 1167 L339 1166 L323 1185 L323 1158 L302 1145 Q353 1087 321 1026 Q294 955 235 925 Z')]
side_arms=[path('M219 491 Q174 409 159 336 Q139 273 180 220 L263 127 L287 152 L219 246 Q196 281 210 321 L253 452 Z',fill='#c8cac7'),
           path('M173 490 Q113 416 101 344 Q86 272 132 219 L224 117 L251 143 L174 245 Q148 276 164 326 L211 449 Z')]
side_face=[path('M224 117 Q243 91 279 102 L321 118 L344 153 L332 180 L278 199 L240 175 Z'),
           path('M238 124 L286 138 M239 141 L289 154 M255 105 L291 122',fill='none',stroke='#737873',width=5),
           '<ellipse cx="317" cy="159" rx="10" ry="11" fill="#ffffff" stroke="#292e2b" stroke-width="5"/>']
side_tail=[path('M169 868 Q78 918 71 1023 Q66 1100 103 1145 L126 1134 L117 1165 L127 1185 L100 1171 L80 1180 L84 1152 Q29 1089 36 1017 Q45 909 154 848 Z')]
for f,arms,face,tail in [('south',front_arms,front_face,front_tail),('east',side_arms,side_face,side_tail),('north',back_arms,back_face,back_tail)]:
    base_image=Image.new('RGBA',SIZE)
    for row in base['views'][f]:
        p=ROOT/row['public_file'];assert ref(p)['sha256']==row['sha256'];base_image.alpha_composite(Image.open(p).convert('RGBA'),(0,PAD))
    base_image.save(HERE/f'baseline-{f}.png')
    for label,parts in [('raised-arms',arms),('hands-face',face),('tail',tail)]:save_svg(label+'-'+f,parts)
    out=Image.new('RGBA',SIZE)
    for label in ['tail','raised-arms']:out.alpha_composite(Image.open(HERE/f'{label}-{f}.png').convert('RGBA'))
    out.alpha_composite(base_image);out.alpha_composite(Image.open(HERE/f'hands-face-{f}.png').convert('RGBA'));out.save(HERE/f'constructed-{f}.png')
out=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'IRUDAD / separate source-bound additions; fixed older-human baseline',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((240,593),Image.Resampling.LANCZOS);out.paste(im,(40+i*330,55),im);d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Manual proposal. Body/head pixels unchanged; actual Hand201/6 pose binding unresolved.',font=font,fill='#e5e8d8');out.save(HERE/'constructed-turnaround.png')
write(HERE/'manual-anatomy-review.json',dict(status='PROPOSAL REQUIRES VISUAL REVIEW',source_supported='Four arms total, joined-hand face with no mouth/desert-white eyes, short barb-crowned posterior tail, older/hunched appearance.',reused='Current unmutated older-human body/head; exact existing age silhouette and all source pixels preserved.',unresolved='Raised-pair mapping versus actual equipped Hand201/6 must be resolved in individual assembly. This is no native bone map.',scope='Neutral separate mutation add-ons only; no new framework or equipment.'))
print('Constructed source packet, padded unchanged baseline and separate south/east/north anatomy proposals.')
