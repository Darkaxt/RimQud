"""Construct BODY-HUMAN-MALE's front and contextual source plate, not other entries.

Game references remain private. The report plate embeds small attributed source
comparisons with explanatory labels; it is not a redistributed source texture.
The constructed front is editable original geometry, with explicit bare feet.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import resvg_py

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/conversion/body-human-male/v1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save_json(p,data):p.write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())

FRONT='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024">
<g stroke="#303a34" stroke-width="8" stroke-linejoin="round" stroke-linecap="round">
<!-- Bare feet have heels/ankles and broad rounded forefeet, no shoe seam. -->
<path d="M195 839 L193 885 Q171 899 177 920 Q198 935 229 921 L235 846Z" fill="#cbd0c7"/>
<path d="M277 846 L283 921 Q314 935 335 920 Q341 899 319 885 L317 839Z" fill="#cbd0c7"/>
<!-- Neutral torso and legs, not an occupation-specific costume. -->
<path d="M214 368 Q256 354 298 368 Q327 386 333 431 L315 570 Q331 652 320 727 L315 878 Q299 889 278 879 L272 754 L256 715 L240 754 L234 879 Q213 889 197 878 L192 727 Q181 652 197 570 L179 431 Q185 386 214 368Z" fill="#cbd0c7"/>
<path d="M206 384 Q177 379 164 416 L149 536 L152 608 Q164 620 180 608 L186 541 L205 447 M306 384 Q335 379 348 416 L363 536 L360 608 Q348 620 332 608 L326 541 L307 447" fill="#cbd0c7"/>
<ellipse cx="166" cy="615" rx="19" ry="22" fill="#dce0d6"/>
<ellipse cx="346" cy="615" rx="19" ry="22" fill="#dce0d6"/>
<path d="M236 332 L234 374 Q256 390 278 374 L276 332Z" fill="#cbd0c7"/>
<path d="M196 230 Q177 219 181 247 Q181 267 198 267 M316 230 Q335 219 331 247 Q331 267 314 267" fill="#cbd0c7"/>
<path d="M198 212 Q195 164 230 157 Q256 150 282 157 Q317 164 314 212 L309 287 Q298 336 256 345 Q214 336 203 287Z" fill="#dce0d6"/>
</g>
<!-- Restrained shade planes do not define clothing or personal cosmetics. -->
<path d="M201 577 Q211 667 206 766 L206 867 L226 870 L229 741 L247 707 Q215 683 201 577Z" fill="#b8c0b4"/>
<path d="M311 577 Q301 667 306 766 L306 867 L286 870 L283 741 L265 707 Q297 683 311 577Z" fill="#b8c0b4"/>
</svg>'''

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--reference-root',type=Path,required=True);a=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    assert not (OUT/'constructed-front.svg').exists(),'Preserve prior evidence; use a new revision for a new construction'
    sources=json.loads((ROOT/'art/village/sources.json').read_text(encoding='utf-8'))
    catalogue=json.loads((ROOT/'evidence/joppa-creature-catalogue.json').read_text(encoding='utf-8'))
    refs=json.loads((ROOT/'evidence/village-reference-index.json').read_text(encoding='utf-8'))['entries']
    wanted=['Argyve','Mehmet','WatervineFarmerJoppa']
    actors=[x for x in sources['actors'] if x['creature'] in wanted]
    refs=[x for x in refs if x['blueprint'] in wanted]
    donor=[x for x in catalogue['reference_families']['human'] if x['name'] in ['Naked_Male_south','Male_Average_Normal_south']]
    for ref in refs:assert digest(a.reference_root/ref['reference_file'])==ref['reference_sha256']
    for ref in donor:assert digest(a.reference_root/ref['file'])==ref['png_sha256']
    observed=[dict(blueprint=x['creature'],race=x['race_input'],lineage=x['lineage'],
                   original_tiles=x['original_model_tiles'],instances=[n for n in x['native_instances'] if n['gender']=='male']) for x in actors]
    save_json(OUT/'source-packet.json',dict(entry='BODY-HUMAN-MALE',recorded_at=datetime.now(timezone.utc).isoformat(),
        source_sha256={p:digest(ROOT/p) for p in ['art/village/sources.json','evidence/joppa-creature-catalogue.json','evidence/village-reference-index.json']},
        identity='Reusable adult male human base, not Argyve-specific anatomy or clothing',observed=observed,original_references=refs,
        donor_references=donor,reference_role='RimWorld Core neutral body/head: graphic scale, high-contrast outline and restrained shading. Explicit arms and bare feet are authored for this Qud base; do not claim they are donor limb nodes.',
        anatomy_interpretation=dict(heads=1,arms=2,hands=2,legs=2,feet=2,source='Observed Humanoid body tree; plural Feet is a group, not a count of one. No race-wide native Description.Short is supplied.'),
        uncertainties=['Clothed original sprites do not establish a precise nude silhouette. The unclothed proportions and unseen surfaces are authored interpretations.',
                       'No native age selector is established; adult authoring template does not change demographics.',
                       'Argyve beard/eyebrows and profession tools belong to later personal/equipment layers, not this shared body.'],
        construction_contract=dict(canvas=[512,1024],front_contact=[256,926],head_neck_seam_y=360,
            view_rule='Same body dimensions, foot baseline and head scale across directions; side limbs/feet overlap in profile.',
            palette='Neutral grayscale body with uniform foreground tint; clothing owns its own palette. No baked colored skin or equipment.',
            layers='Body includes painted arms, hands, legs and feet. Head/neck separate. No new arm or leg render nodes.')))
    (OUT/'constructed-front.svg').write_bytes(FRONT.encode())
    (OUT/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(OUT/'constructed-front.svg'),skip_system_fonts=True))
    # A contextual comparison rather than loose original asset files in the repo.
    plate=Image.new('RGB',(1240,570),'#142823');draw=ImageDraw.Draw(plate)
    font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
    small=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
    draw.text((24,20),'BODY-HUMAN-MALE / SOURCE AND RENDERING REFERENCES',font=font,fill='#e4e7d6')
    for i,ref in enumerate(refs):
        im=Image.open(a.reference_root/ref['reference_file']).convert('RGBA');im=im.resize((96,144),Image.Resampling.NEAREST)
        x=36+i*170;plate.paste(im,(x,110),im);draw.text((x-5,275),ref['blueprint'],font=small,fill='#e3cf43')
    draw.text((30,330),'Qud: original clothed glyphs',font=font,fill='#e4e7d6')
    draw.text((30,365),'Identity/palette, not a nude-body diagram.',font=small,fill='#b7cbbb')
    for i,ref in enumerate(donor):
        im=Image.open(a.reference_root/ref['file']).convert('RGBA').resize((256,256),Image.Resampling.NEAREST)
        x=645+i*280;plate.paste(im,(x,70),im);draw.text((x,345),ref['name'],font=small,fill='#e3cf43')
    draw.text((640,390),'RimWorld Core: body + head convention',font=font,fill='#e4e7d6')
    draw.text((640,425),'Proportions / outline / shading only.',font=small,fill='#b7cbbb')
    draw.text((30,505),'Installed game references shown only in this annotated comparison. Exact hashes are in source-packet.json.',font=small,fill='#b7cbbb')
    plate.save(OUT/'source-comparison.png')
    print('Constructed explicit-foot front and source packet; reference hashes matched. No other entry modified.')

if __name__=='__main__':main()
