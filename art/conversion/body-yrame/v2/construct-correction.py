"""Rebuild the additional pair from lower pelvic roots, preserving the human base."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, io, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'v1'
SIZE = (512, 1024)
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p, d): p.write_bytes((json.dumps(d, indent=2, ensure_ascii=False)+'\n').encode())
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())

assert not (HERE/'construction.json').exists(), 'Retain original correction evidence'
baseline = read(ROOT/'art/conversion/body-human-female/v2/model.json')
old = read(OLD/'registered/model.json')
ledger = read(ROOT/'evidence/conversion-ledger.json')
entries = {e['id']: e for e in ledger['entries']}
assert ledger['active_entry'] == 'BODY-RAY-CAT'
entries['BODY-RAY-CAT']['status'] = 'UNFINISHED'
ledger['active_entry'] = 'BODY-YRAME'
reason = ('User-identified structural defect confirmed in both the first generated sheet and selected v1: '
          'added thighs emerge too high on the posterior contour, and the added pair is behind the base in all facings. '
          'V1 is superseded; four-foot count alone did not establish coherent pelvic attachment or depth.')
for ident in ['BODY-YRAME', 'NPC-WARDEN-YRAME']:
    e = entries[ident]
    e['generation_ready'] = False
    e['status'] = 'IN PROGRESS' if ident == 'BODY-YRAME' else 'UNFINISHED'
    e['current_step'] = e['required_steps'][4 if ident == 'BODY-YRAME' else 1]
    e['known_issues'] = [reason if ident == 'BODY-YRAME' else 'Dependent BODY-YRAME anatomy superseded; regenerate assembly after body correction. Existing item fits are unchanged.']
    e['art_review'] = dict(status='REQUIRES REWORK', reason=e['known_issues'][0])
    e['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(), step=e['current_step'],
        action='Withdraw generation-ready credit after confirmed attachment and facing-depth defect.',
        inputs=[e['current_registration']['model'], ref(OLD/'leg-construction.json')], outputs=[], review=e['known_issues'][0], result='REQUIRES REWORK'))

# Feet297 is the native fore group; Feet298 the hind group. No source joint
# coordinates exist. These roots/stance are explicitly authored, not recovered.
# Roots overlap the *lower* pelvis/upper thigh, never its high rear outline.
front = ('M172 602 Q158 628 145 675 Q123 724 113 764 Q108 790 117 817 '
         'L103 898 Q78 913 73 932 Q74 946 96 950 L135 950 Q153 945 150 932 '
         'Q146 919 132 911 L139 815 Q155 795 155 774 Q166 721 197 682 L217 625 Z')
back = ('M161 603 Q174 594 192 612 Q212 637 202 675 Q173 720 157 770 '
        'Q155 795 143 817 L136 910 Q158 927 153 940 Q149 951 130 950 '
        'L93 950 Q72 948 72 934 Q75 920 103 903 L115 815 '
        'Q109 784 117 758 Q132 702 151 655 Z')
profile = ('M217 607 Q242 600 253 623 Q256 645 235 673 '
           'Q198 710 177 751 Q165 779 173 806 L168 898 '
           'Q174 915 199 924 Q213 931 207 941 Q202 949 181 950 '
           'L119 950 Q98 948 101 933 Q108 914 136 897 L138 807 '
           'Q122 779 134 747 Q154 694 191 650 Q204 635 217 607 Z')
geometry = dict(source_packet=ref(OLD/'source-packet.json'), previous=ref(OLD/'registered/model.json'),
    baseline_model=ref(ROOT/'art/conversion/body-human-female/v2/model.json'),
    source_facts={'fore':{'part':297,'parent':287,'laterality':16,'boots':580},
                  'hind':{'part':298,'parent':287,'laterality':64,'boots':None},
                  'description':'shifts her weight between hind and forelegs', 'joint_coordinates':'not provided'},
    authored_roots={'south_hind_left':[190,625], 'north_hind_left':[182,625], 'east_hind':[225,625],
                    'meaning':'Lower pelvic/upper-thigh attachment. Knee bends/stance are authored estimates.'},
    paths={'south_left':front,'north_left':back,'east_near':profile},
    facing_depth={'south':'hind pair behind ordinary fore pair',
                  'east':'far hind behind near hind, both behind ordinary near fore leg',
                  'north':'hind pair in front of ordinary fore pair; roots overlap lower pelvis',
                  'west':'horizontal mirror of east; semantic fore/hind identities unchanged'},
    invariants=['Shared512x1024 frame and contact256,950','Ordinary female body/head files remain byte-identical',
                'No root along high buttock outline','No six legs or new torso/animal body',
                'Do not force all feet visible in exact profile','No native activation or mutation framework'],
    interpretation='Four human legs: fore and hind pairs share the lower pelvic region. Art interpretation, not a source-specified skeleton.')
write(HERE/'construction.json', geometry)
def svg_for(f):
    p = {'south':front,'north':back,'east':profile}[f]
    def shape(): return '<path d="'+p+'" fill="url(#skin)" stroke="#171b19" stroke-width="7" stroke-linejoin="round"/>'
    if f == 'east':
        parts = '<g transform="translate(20 0)">'+shape()+'</g>'+shape()
    else:
        parts = shape()+'<g transform="translate(512 0) scale(-1 1)">'+shape()+'</g>'
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024">'
            '<defs><linearGradient id="skin"><stop stop-color="#c9c9c9"/>'
            '<stop offset=".58" stop-color="#eeeeee"/><stop offset="1" stop-color="#dedede"/>'
            '</linearGradient></defs>'+parts+'</svg>')
for f in ['south','east','north']:
    svg=svg_for(f); (HERE/f'extra-legs-{f}.svg').write_text(svg,encoding='utf-8')
    extra=Image.open(io.BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA');extra.save(HERE/f'extra-legs-{f}.png')
    body=Image.new('RGBA',SIZE)
    for row in sorted(baseline['views'][f],key=lambda r:r['layer']):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        body.alpha_composite(Image.open(ROOT/row['public_file']).convert('RGBA'))
    out=Image.new('RGBA',SIZE)
    if f!='north': out.alpha_composite(extra)
    out.alpha_composite(body)
    if f=='north':out.alpha_composite(extra)
    out.save(HERE/f'constructed-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
plate=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(plate)
d.text((18,16),'YRAME / lower pelvic roots; fore/hind overlap reverses in BACK view',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').resize((256,512),Image.Resampling.LANCZOS)
    x=56+i*374;plate.paste(im,(x,54),im)
    d.text((x,580),{'south':'FRONT / SOUTH','east':'RIGHT PROFILE / EAST','north':'BACK / NORTH'}[f],font=font,fill='#e3cf43')
d.text((18,620),'Corrected editable proposal. No gear. Joint placement is an authored interpretation.',font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png')
entries['BODY-YRAME']['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),
    step=entries['BODY-YRAME']['required_steps'][4],action='Reconstruct lower pelvic attachments and facing-dependent overlap before another refinement.',
    inputs=[ref(OLD/'source-packet.json'),ref(OLD/'registered/model.json')],
    outputs=[ref(HERE/'construction.json'),ref(HERE/'construct-correction.py'),ref(HERE/'constructed-turnaround.png')],
    review='Manual candidate awaiting visual inspection. Native source supplies fore/hind slots, not socket coordinates.',result='REQUIRES REVIEW'))
ledger['updated_at']=datetime.now(timezone.utc).isoformat();write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Reopened body and dependent assembly. Built lower-root construction; visual review pending.')
