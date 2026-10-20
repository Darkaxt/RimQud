"""Construct an authored juvenile camelfolk mannequin without demographic changes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/conversion/body-dromad-child/v1'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def record(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'constructed-front.svg').exists()
groups=[]
for component in ['body','head']:
    tree=ET.fromstring((ROOT/f'art/dromad/nude/{component}-south.svg').read_text(encoding='utf-8'))
    elements=[]
    for child in tree:
        # Remove construction toe bars and personal facial marks; retain muzzle,
        # ears, long neck and dulla as the race's structural shape.
        if child.tag.endswith('ellipse'):continue
        if child.attrib.get('d','').startswith(('M93 290','M112 99')):continue
        elements.append(ET.tostring(child,encoding='unicode'))
    factor=.85 if component=='body' else .9
    anchor=(128,298) if component=='body' else (128,200)
    groups.append(f'<g transform="translate({anchor[0]},{anchor[1]}) scale({factor}) translate({-anchor[0]},{-anchor[1]})">'+''.join(elements)+'</g>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g transform="translate(-140.8,26.2) scale(3.1)">'+''.join(groups)+'</g></svg>'
(OUT/'constructed-front.svg').write_bytes(svg.encode());(OUT/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(OUT/'constructed-front.svg'),skip_system_fonts=True))
adult=json.loads((ROOT/'art/conversion/body-dromad/v1/source-packet.json').read_text(encoding='utf-8'))
child_refs=json.loads((ROOT/'evidence/joppa-creature-catalogue.json').read_text(encoding='utf-8'))['reference_families']['child']
for item in child_refs['images']:assert hashlib.sha256((DONOR/item['file']).read_bytes()).hexdigest()==item['sha256']
packet=dict(entry='BODY-DROMAD-CHILD',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Authored featureless child dromad template; male/female labels share geometry',
 race=adult['identity'],native_race_description=adult['description'],body_metadata=adult['body'],mutation_metadata=adult['mutations'],metadata_gaps=adult['metadata_gaps'],
 original=adult['original'],donor_dromedary_references=adult['donor_references'],child_presentation_reference=child_refs,
 baseline_source=record(ROOT/'art/conversion/body-dromad/v1/source-packet.json'),selected_adult=record(ROOT/'art/conversion/body-dromad/v1/model.json'),
 authored_changes='Compact torso and shorter overall body with relatively larger head, smooth featureless mannequin surfaces, no eyes/personal facial markings. Retain species muzzle/ears, long neck, dulla and integrated hump.',
 juvenile_uncertainty='No child dromad resident, canonical juvenile description, hump/dulla development, age selector or required sex-specific geometry is established. This is an authored family template, not a claim about native age biology.',
 donor_role='Dromedary supplies species art conventions only. Biotech child torso supplies a compact life-stage presentation example, not juvenile dromad anatomy or a quadruped substitution.',
 anatomy=dict(heads=1,arms=2,hands=2,legs=2,feet=2,mutations='Not baked into reusable body'),
 variants={'male':'shared geometry','female':'shared geometry'},physical_height=.98,physical_height_kind='Authoring choice, not native age/height evidence',
 registration=dict(canvas=[512,1024],contact=[256,950],rule='Translate whole figure and body/head/masks together; no independent facing fit'),
 clothing='FIT-DROMAD-CHILD-TEMPLATE-TUNIC owns separate garment generation and fit. No clothing baked into base.',
 native_policy='Do not assign an age or child outfit to Tam. Native acceptance waits for all conversions.')
(OUT/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
plate=Image.new('RGB',(1240,940),'#142823');plate.paste(Image.open(ROOT/'art/conversion/body-dromad/v1/source-comparison.png'),(0,0))
draw=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
draw.text((24,715),'Child template: authored compact proportions; no canonical juvenile dromad is established.',font=font,fill='#e3cf43')
for i,item in enumerate(child_refs['images']):
    im=Image.open(DONOR/item['file']).convert('RGBA').resize((160,160),Image.Resampling.NEAREST);x=24+i*390;plate.paste(im,(x,755),im);draw.text((x+165,800),item['name'],font=font,fill='#dce4d7')
plate.save(OUT/'source-comparison.png')
