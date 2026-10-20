"""Construct the requested older adult human front from the shared human family."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import resvg_py

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--gender',choices=['male','female'],required=True);ap.add_argument('--reference-root',type=Path,required=True);a=ap.parse_args()
    base=ROOT/f'art/conversion/body-human-{a.gender}/v1';out=ROOT/f'art/conversion/body-human-{a.gender}-older/v1';out.mkdir(parents=True,exist_ok=True)
    assert not (out/'constructed-front.svg').exists(),'Preserve the previous revision'
    svg=(base/'constructed-front.svg').read_text()
    # Keep the existing head, hands, limbs and bare-foot construction. Changes
    # are limited to a softened torso/shoulder line, not a new anatomy or rig.
    if a.gender=='male':
        before='M214 368 Q256 354 298 368 Q327 386 333 431 L315 570 Q331 652 320 727 L315 878 Q299 889 278 879 L272 754 L256 715 L240 754 L234 879 Q213 889 197 878 L192 727 Q181 652 197 570 L179 431 Q185 386 214 368Z'
        after='M216 380 Q256 372 296 380 Q326 402 331 439 L319 565 Q345 642 323 727 L315 878 Q299 889 278 879 L272 754 L256 715 L240 754 L234 879 Q213 889 197 878 L189 727 Q167 642 193 565 L181 439 Q186 402 216 380Z'
    else:
        before='M221 368 Q256 360 291 368 Q319 386 323 431 L304 553 Q337 627 329 705 L315 878 Q299 889 278 879 L274 755 L256 715 L238 755 L234 879 Q213 889 197 878 L183 705 Q175 627 208 553 L189 431 Q193 386 221 368Z'
        after='M221 380 Q256 374 291 380 Q319 402 324 439 L310 554 Q345 634 330 715 L315 878 Q299 889 278 879 L274 755 L256 715 L238 755 L234 879 Q213 889 197 878 L182 715 Q167 634 202 554 L188 439 Q193 402 221 380Z'
    assert before in svg;svg=svg.replace(before,after)
    (out/'constructed-front.svg').write_bytes(svg.encode());(out/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(out/'constructed-front.svg'),skip_system_fonts=True))
    sources=json.loads((ROOT/'art/village/sources.json').read_text());elder=next(x for x in sources['actors'] if x['creature']=='ElderBob')
    refs=json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'];ref=next(x for x in refs if x['blueprint']=='ElderBob');assert sha(a.reference_root/ref['reference_file'])==ref['reference_sha256']
    adult=json.loads((base/'source-packet.json').read_text());donors=adult['donor_references']
    packet=dict(entry='BODY-HUMAN-'+a.gender.upper()+'-OLDER',recorded_at=datetime.now(timezone.utc).isoformat(),
        identity='Older adult '+a.gender+' human authoring template; no NPC age reassignment',
        race=elder['race_input'],body_plan=adult.get('anatomy_interpretation'),original_age_reference=ref,
        source_age_description=elder['native_instances'][0]['description'],
        source_limits='Irudad explicitly supplies an old face and hunched back. His hands-face, extra arms and stinger are individual mutation features, not baseline human aging; they remain required in BODY-IRUDAD, not here.',
        shared_human_reference=dict(model=(base/'model.json').relative_to(ROOT).as_posix(),sha256=sha(base/'model.json')),
        donor_references=donors,donor_limit='No separate old-age torso is established from these donor references; reuse the same adult presentation convention, with authored age variation.',
        construction=dict(source_svg=(base/'constructed-front.svg').relative_to(ROOT).as_posix(),source_sha256=sha(base/'constructed-front.svg'),
            retained='Same head/limb counts, bare feet, camera and family proportions',changes='Slightly lowered/softened shoulders and torso; side should have a restrained age-related stoop, not a profession pose or extreme caricature'),
        uncertainty='Age variant requested by user. No native numerical-age/life-stage selection is established; no canonical older-female resident is inferred.',
        palette='Neutral grayscale and separate clothing; no baked gray hair or personal cosmetics')
    (out/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
    plate=Image.open(base/'source-comparison.png').convert('RGB');extra=Image.new('RGB',(1240,250),'#142823');draw=ImageDraw.Draw(extra);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
    glyph=Image.open(a.reference_root/ref['reference_file']).convert('RGBA').resize((96,144),Image.Resampling.NEAREST);extra.paste(glyph,(36,35),glyph)
    for y,text in [(25,'Age reference: Elder Irudad (human, individual mutations retained in his own entry).'),(75,'Native description: old face, hunched back; generic older template uses age cues only.'),(125,'Shared adult human body/head remains the construction and rendering reference.'),(175,'No age is assigned to villagers. All actual clothing remains separate.')]:draw.text((170,y),text,font=font,fill='#dce4d7')
    combined=Image.new('RGB',(1240,820));combined.paste(plate,(0,0));combined.paste(extra,(0,570));combined.save(out/'source-comparison.png')
    print('Constructed older '+a.gender+' shared-family front and exact source/age/reference packet.')

if __name__=='__main__':main()
