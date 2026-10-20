"""Build this adult human variant from the shared editable human front."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import resvg_py
from construct_human_base import FRONT,ROOT

OUT=ROOT/'art/conversion/body-human-female/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--reference-root',type=Path,required=True);a=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);assert not (OUT/'constructed-front.svg').exists(),'Preserve previous revision'
    sources=json.loads((ROOT/'art/village/sources.json').read_text());cat=json.loads((ROOT/'evidence/joppa-creature-catalogue.json').read_text());refs=json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries']
    actors=[x for x in sources['actors'] if x['creature'] in ['JoppaFarmerConvert','WatervineFarmerJoppa']]
    originals=[x for x in refs if x['blueprint'] in {a['creature'] for a in actors}]
    donors=[x for x in cat['reference_families']['human'] if x['name'] in ['Naked_Female_south','Female_Average_Normal_south']]
    for x in originals:assert sha(a.reference_root/x['reference_file'])==x['reference_sha256']
    for x in donors:assert sha(a.reference_root/x['file'])==x['png_sha256']
    male='M214 368 Q256 354 298 368 Q327 386 333 431 L315 570 Q331 652 320 727 L315 878 Q299 889 278 879 L272 754 L256 715 L240 754 L234 879 Q213 889 197 878 L192 727 Q181 652 197 570 L179 431 Q185 386 214 368Z'
    female='M221 368 Q256 360 291 368 Q319 386 323 431 L304 553 Q337 627 329 705 L315 878 Q299 889 278 879 L274 755 L256 715 L238 755 L234 879 Q213 889 197 878 L183 705 Q175 627 208 553 L189 431 Q193 386 221 368Z'
    assert male in FRONT
    svg=FRONT.replace(male,female)
    (OUT/'constructed-front.svg').write_bytes(svg.encode());(OUT/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(OUT/'constructed-front.svg'),skip_system_fonts=True))
    save(OUT/'source-packet.json',dict(entry='BODY-HUMAN-FEMALE',recorded_at=datetime.now(timezone.utc).isoformat(),
        identity='Reusable adult female human template; not a separate species or a profession costume',
        source_sha256={p:sha(ROOT/p) for p in ['art/village/sources.json','evidence/joppa-creature-catalogue.json','evidence/village-reference-index.json']},
        observed=[dict(blueprint=x['creature'],race=x['race_input'],lineage=x['lineage'],instances=[n for n in x['native_instances'] if n['gender']=='female']) for x in actors],
        original_references=originals,donor_references=donors,
        shared_geometry=dict(source='tools/construct_human_base.py',sha256=sha(ROOT/'tools/construct_human_base.py'),
            retained='Same canvas, head, arms, hands, legs and explicit bare feet; no independent anatomical redesign',
            changes='Modestly narrower upper torso/waist and wider hips in editable front geometry. Donor body-type convention, not a native race-wide morphological fact.'),
        anatomy_interpretation=dict(heads=1,arms=2,hands=2,legs=2,feet=2,source='Observed Humanoid body tree, paired Feet group; no race-wide Description.Short'),
        uncertainties=['Gender is from this captured snapshot only; it does not establish age or a mandatory body shape.',
                       'Clothed Qud glyphs establish identity/palette, not exact nude anatomy. No sexual details or clothing baked into this adult mannequin.',
                       'Personal hair/eyes and mutations remain separate; the ordinary base has no extra limbs.'],
        construction_contract=dict(canvas=[512,1024],front_contact=[256,926],views=['south','east','north','west mirror'],palette='Neutral grayscale under native foreground tint; equipment owns its colors',layers='Body includes painted limbs; head/neck separate. No independent limb rig.')))
    plate=Image.new('RGB',(1240,570),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18);small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
    d.text((24,20),'BODY-HUMAN-FEMALE / SHARED HUMAN GEOMETRY + REFERENCES',font=font,fill='#e4e7d6')
    for i,x in enumerate(originals):
        im=Image.open(a.reference_root/x['reference_file']).convert('RGBA').resize((96,144),Image.Resampling.NEAREST);px=50+i*230;plate.paste(im,(px,110),im);d.text((px,275),x['blueprint'],font=small,fill='#e3cf43')
    d.text((30,330),'Qud clothed originals / captured female humans',font=small,fill='#e4e7d6');d.text((30,365),'Not a nude anatomical diagram.',font=small,fill='#b7cbbb')
    for i,x in enumerate(donors):
        im=Image.open(a.reference_root/x['file']).convert('RGBA').resize((256,256),Image.Resampling.NEAREST);px=645+i*280;plate.paste(im,(px,70),im);d.text((px,345),x['name'],font=small,fill='#e3cf43')
    d.text((640,395),'RimWorld Core body/head convention only.',font=small,fill='#e4e7d6');d.text((30,505),'Contextual reference comparison. Exact source identities, anatomy and hashes: source-packet.json.',font=small,fill='#b7cbbb');plate.save(OUT/'source-comparison.png')
    print('Female front derived from shared human geometry; reference identities and observed anatomy recorded.')

if __name__=='__main__':main()
