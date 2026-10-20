"""Source-bound dromad front and contextual references for the reset ledger."""
from datetime import datetime,timezone
import hashlib,json,textwrap
from pathlib import Path
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'art/conversion/body-dromad/v1'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def record(path):return dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'constructed-front.svg').exists()
metadata=json.loads((ROOT/'evidence/tam-conversion-input.json').read_text(encoding='utf-8'))
catalogue=json.loads((ROOT/'evidence/joppa-creature-catalogue.json').read_text(encoding='utf-8'))
refs=json.loads((ROOT/'evidence/village-reference-index.json').read_text(encoding='utf-8'))['entries'];original=next(x for x in refs if x['blueprint']=='Tam')
assert hashlib.sha256((DONOR/original['reference_file']).read_bytes()).hexdigest()==original['reference_sha256']
donors=catalogue['reference_families']['dromad_camel_features']
for item in donors:assert hashlib.sha256((DONOR/item['file']).read_bytes()).hexdigest()==item['png_sha256']
parts=[]
for component in ['body','head']:
    old=ROOT/f'art/dromad/nude/{component}-south.svg'
    element=ET.fromstring(old.read_text(encoding='utf-8'));parts.extend(ET.tostring(child,encoding='unicode') for child in element)
# One fixed transform of the complete source construction, never per-component fitting.
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g transform="translate(-204.8,-122.8) scale(3.6)">'+''.join(parts)+'</g></svg>'
(OUT/'constructed-front.svg').write_bytes(svg.encode());(OUT/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(OUT/'constructed-front.svg'),skip_system_fonts=True))
packet=dict(entry='BODY-DROMAD',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity=metadata['identity'],description=metadata['description'],source=metadata['source'],body=metadata['body'],
 mutations=metadata['mutations'],appearance=metadata['appearance'],metadata_gaps=metadata['metadata_gaps'],
 original=original,donor_references=donors,
 reference_role='Actual Core dromedary images supply camel muzzle, neck/hump and clean directional shading. Qud Humanoid tree supplies bipedal hands/feet; donor quadruped legs/tail do not replace it.',
 baseline_policy='Reusable unmutated dromad race base. Intrinsic long neck/dulla/hump remain. No mutation appendages, named clothing or staff baked into the body.',
 anatomy_interpretation=dict(heads=1,arms=2,hands=2,legs=2,feet=2,features=['elongated camel muzzle','long neck','dulla','pointed ears','integrated upper-back hump'],
    interpretation='Paired Feet humanoid group supports two feet; fine unseen anatomy and rounded foot forms remain authored. No separate Neck/Hump/Dulla mechanical nodes are required.'),
 authoring=dict(front_sources=[record(ROOT/f'art/dromad/nude/{c}-south.svg') for c in ['body','head']],
    reuse='Existing editable construction is an input only. Fresh review/refinement and the reset log are required; no historical acceptance credit.',
    shared_frame=dict(canvas=[512,1024],contact=[256,950],transform='Uniform scale 3.6 and translation (-204.8,-122.8) for the complete old construction'),
    palette='Neutral base and separate detail coverage. Source tileColor &w and detail W retained. Dulla detail-region placement is authored, not a proven pixel-to-anatomy reading of the tiny original.',
    cosmetics='Native ear rings, eyelashes and ink descriptions retained; personal/cosmetic layers remain separate from the baseline body.',
    demographic_policy='Observed Tam is male. No race-wide visual dimorphism or age selector established; do not invent a native gender/age assignment.'))
(OUT/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
plate=Image.new('RGB',(1240,700),'#142823');draw=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
draw.text((24,20),'DROMAD / QUD IDENTITY + HUMANOID BODY + ACTUAL CAMEL REFERENCES',font=font,fill='#e3cf43')
glyph=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((96,144),Image.Resampling.NEAREST);plate.paste(glyph,(62,90),glyph)
draw.text((24,270),'Tam: original Qud glyph',font=small,fill='#e3cf43')
for i,item in enumerate(donors):
    x=340+i*290;im=Image.open(DONOR/item['file']).convert('RGBA').resize((240,240),Image.Resampling.NEAREST);plate.paste(im,(x,65),im);draw.text((x,325),item['name'],font=small,fill='#e3cf43')
draw.text((24,390),'Native Dromad Description.Short:',font=font,fill='#dce4d7')
for i,line in enumerate(textwrap.wrap(metadata['description']['race_template'],117)):draw.text((24,425+i*25),line,font=small,fill='#dce4d7')
for y,line in [(555,'Qud: long neck, dulla, hump; paired humanoid feet and two hand-bearing arms.'),(590,'Donor camel: muzzle / hump / directional art conventions, not four-legged anatomy.'),(625,'Cloth Robe, Shillelagh, jewelry and ink are separate. No age/dimorphism inferred.')]:draw.text((24,y),line,font=small,fill='#b7cbbb')
plate.save(OUT/'source-comparison.png')
