"""Present actual Blender outputs alongside unchanged body and derived outlines."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
FACES=['south','east','north','west'];SIZE=(768,1152)
FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
SMALL=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',13)
BG='#142b24';PANEL='#20382d';GOLD='#e3ce43';INK='#ebeadd'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rgba(p):return Image.open(p).convert('RGBA')
def plate(name,title,images,caption):
    out=Image.new('RGB',(1600,490),BG);d=ImageDraw.Draw(out);d.text((16,12),title,font=FONT,fill=GOLD)
    for i,(face,im) in enumerate(images.items()):
        bg=Image.new('RGBA',SIZE,PANEL);bg.alpha_composite(im)
        box=(290,0,690,400) if face=='east' else ((78,0,478,400) if face=='west' else (184,0,584,400))
        out.paste(bg.crop(box).convert('RGB'),(i*400,45));d.text((i*400+16,450),face.upper(),font=FONT,fill=GOLD)
    d.text((16,475),caption,font=SMALL,fill=INK);out.save(HERE/name)
    return HERE/name

assert (HERE/'blender-receipt.json').exists(),'Observe original Blender operation to completion first'
bodymodel=ROOT/'art/conversion/body-yrame/v3/registered-v2/model.json';model=read(bodymodel)
raw={};fitted={};outlined={};diagnostics={}
for face in FACES:
    whole=np.array(rgba(HERE/f'whole-item-{face}.png'))
    vis=np.array(rgba(HERE/f'visible-item-{face}.png'))
    base=Image.new('RGBA',SIZE)
    for row in sorted(model['views'][face],key=lambda x:x['layer']):base.alpha_composite(rgba(ROOT/row['public_file']))
    raw[face]=rgba(HERE/f'with-skull-{face}.png')
    a=whole[:,:,3].astype(float);n=np.minimum(vis[:,:,3],a).astype(float)
    f=np.round(np.divide(255*(a-n),255-n,out=np.zeros_like(a),where=n<255))
    def assemble(pixels):
        far=pixels.copy();far[:,:,3]=np.uint8(f)
        near=pixels.copy();near[:,:,3]=np.uint8(n)
        return Image.alpha_composite(Image.alpha_composite(Image.fromarray(far),base),Image.fromarray(near))
    fitted[face]=assemble(whole);fitted[face].save(HERE/f'raw-assembly-{face}.png')
    pix=whole.copy();lum=np.round(pix[:,:,:3].mean(2))
    # A repeatable pixel-art finishing operation: five neutral tones and a
    # two-pixel inside contour. No mesh, alpha, scale or camera deformation.
    tones=np.round(lum/36)*36
    edge=np.clip((distance_transform_edt(a>127)-.5)/2,0,1)
    tones=24+(tones-24)*edge
    pix[:,:,:3]=np.uint8(np.clip(tones,0,255))[:,:,None];pix[a==0,:3]=0
    Image.fromarray(pix).save(HERE/f'outlined-whole-item-{face}.png')
    outlined[face]=assemble(pix);outlined[face].save(HERE/f'outlined-assembly-{face}.png')
    diagnostics[face]=dict(canvas=list(rgba(HERE/f'whole-item-{face}.png').size),full_alpha_unchanged=bool(np.array_equal(pix[:,:,3],whole[:,:,3])),visible_alpha_clamped_to_full=True,alpha_partition_max_rounding=float(np.max(np.abs(n+f*(1-n/255)-a))),original_body=ref(bodymodel))

plate('stage-03-cardinal-renders.png','03 / ACTUAL BLENDER CARDINAL RENDERS / red proxy is not replacement body art',raw,'One complete horn model; same physical scale; orthographic cameras. No per-view image stretch.')
plate('stage-04-original-body.png','04 / BLENDER HORNS OVER ORIGINAL BODY / raw shaded render',fitted,'Original registered body pixels; depth-derived near/far ownership; this fit is a trial, not approved art.')
plate('stage-05-manual-outlines.png','05 / MANUAL PIXEL FINISH / same render alpha, neutral tones and inside black outline',outlined,'No regenerated geometry. Compare the root, thickness, front/back overlap and intended-size readability.')

source=rgba(HERE.parent/'v4/source-reference-construction.png').convert('RGB')
out=Image.new('RGB',(1600,800),BG);out.paste(source,(0,0));d=ImageDraw.Draw(out)
for j,line in enumerate(['01 / SOURCE + REFERENCES','Qud: Horns575','Natural equipment on Head288','Bone extrusions, grooves','w primary / W detail','Ram-like curl: user interpretation','No native skull coordinates','','Core ram: shape/render cues only','Original human head stays fixed']):d.text((1210,20+j*28),line,font=SMALL,fill=GOLD if j in [0,1] else INK)
out.save(HERE/'stage-01-source.png')
probe=rgba(HERE/'stage-02-model-3d.png');proof=Image.new('RGBA',probe.size,PANEL);proof.alpha_composite(probe)
out=Image.new('RGB',(1000,1000),BG);out.paste(proof.convert('RGB'),(50,50));d=ImageDraw.Draw(out);d.text((20,15),'02 / ACTUAL BLENDER MODEL / diagnostic angle; not a production facing',font=FONT,fill=GOLD);d.text((20,970),'Gray complete horns + red authored skull proxy. Original 2D body is not remodeled.',font=SMALL,fill=INK);out.save(HERE/'stage-02-model-proof.png')

packet=read(HERE.parent/'v9/fit-contract.json');packet.update(method='Blender trial before any skill deployment',blender_receipt=ref(HERE/'blender-receipt.json'),main_review='Pending actual stage-image inspection. Earlier v9 mathematical clearance is not artwork approval.',body=ref(bodymodel),artwork_status='UNAPPROVED TRIAL');write(HERE/'trial-contract.json',packet)
write(HERE/'composition-diagnostics.json',diagnostics)
stages=[('Source, native metadata and actual references','stage-01-source.png'),('Editable Blender model — diagnostic angle','stage-02-model-proof.png'),('Unmodified orthographic cardinal renders','stage-03-cardinal-renders.png'),('Depth-layered render over original body','stage-04-original-body.png'),('Manual neutral tones and black contour','stage-05-manual-outlines.png')]
html=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Yrame horns — Blender trial</title><style>body{background:#142b24;color:#ebeadd;font:17px/1.5 system-ui;margin:24px auto;max-width:1600px;padding:0 20px}a,h1,h2{color:#e3ce43}img{width:100%;height:auto;background:#20382d}section{margin:40px 0}code{overflow-wrap:anywhere}</style><h1>Yrame horns: Blender → 2D trial</h1><p>Test before applying the proposed skill change. All stages below are actual saved output. The three-quarter model view is diagnostic only; production directions are orthographic. This item remains unfinished.</p>']
for number,(title,p) in enumerate(stages,1):
    r=ref(HERE/p);html.append(f'<section id="stage-{number}"><h2>{number}. {title}</h2><a href="../{r["path"]}"><img loading="lazy" src="../{r["path"]}" alt="{title}"></a><details><summary>Exact image hash</summary><code>{r["sha256"]}</code></details></section>')
html.append('<section id="stage-6"><h2>6. ImageGen refinement</h2><p>Not performed for this trial yet. The manual construction must first pass structural inspection; no invented refinement image is shown.</p></section><p><a href="../art/conversion/fit-yrame-horns/blender-trial-v1/horns-trial.blend">Editable .blend model</a> · <a href="../art/conversion/fit-yrame-horns/blender-trial-v1/trial-contract.json">Fit contract and provenance</a> · <a href="conversion-report.html#FIT-YRAME-HORNS-HEAD-0">Entry ledger</a></p></html>')
(ROOT/'docs/yrame-horns-blender-trial.html').write_text('\n'.join(html),encoding='utf-8',newline='\n')
ledger=read(ROOT/'evidence/conversion-ledger.json');entry=next(e for e in ledger['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0');now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',action='Test user-proposed Blender-to-2D workflow before applying skill changes. Render one complete mesh from actual orthographic cameras, preserve full source and original body; derive black contour/neutral tones separately.',inputs=[ref(HERE.parent/'v9/volume.json'),ref(bodymodel)],outputs=[ref(HERE/p) for _,p in stages]+[ref(HERE/'build_blender.py'),ref(HERE/'present.py'),ref(HERE/'horns-trial.blend'),ref(HERE/'blender-receipt.json'),ref(HERE/'trial-contract.json'),ref(HERE/'composition-diagnostics.json')],review='Stage images produced for main/user inspection; no ImageGen call, skill update, registration or readiness credit yet.',result='REQUIRES REVIEW'))
ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Five actual stage plates and bounded trial HTML produced. No skill applied.')
