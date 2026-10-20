"""Construct the featureless child-human family from captured human anatomy."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import resvg_py

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'art/conversion/body-human-child/v1'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def record(path):
    return dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

OUT.mkdir(parents=True,exist_ok=True)
assert not (OUT/'constructed-front.svg').exists()
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024">
<g stroke="#303a34" stroke-width="8" stroke-linejoin="round" stroke-linecap="round" fill="#cbd0c7">
<path d="M204 876 L201 915 Q180 927 186 942 Q207 954 232 940 L235 878Z"/>
<path d="M277 878 L280 940 Q305 954 326 942 Q332 927 311 915 L308 876Z"/>
<path d="M202 404 Q256 387 310 404 Q333 426 326 499 L310 658 Q320 704 313 760 L307 904 Q291 915 274 904 L269 767 L256 739 L243 767 L238 904 Q221 915 205 904 L199 760 Q192 704 202 658 L186 499 Q179 426 202 404Z"/>
<path d="M198 417 Q170 411 158 449 L143 567 L148 628 Q162 641 178 628 L179 573 L197 481 M314 417 Q342 411 354 449 L369 567 L364 628 Q350 641 334 628 L333 573 L315 481"/>
<ellipse cx="162" cy="635" rx="18" ry="20" fill="#dce0d6"/>
<ellipse cx="350" cy="635" rx="18" ry="20" fill="#dce0d6"/>
<path d="M235 351 L233 400 Q256 414 279 400 L277 351Z"/>
<path d="M181 257 Q162 249 165 275 Q168 294 183 291 M331 257 Q350 249 347 275 Q344 294 329 291"/>
<path d="M181 234 Q177 181 215 176 Q256 164 297 176 Q335 181 331 234 L326 302 Q316 355 256 368 Q196 355 186 302Z" fill="#dce0d6"/>
</g>
<path d="M204 660 Q219 711 215 777 L217 897 L230 898 L235 766 L251 735 Q220 716 204 660Z" fill="#b8c0b4"/>
<path d="M308 660 Q293 711 297 777 L295 897 L282 898 L277 766 L261 735 Q292 716 308 660Z" fill="#b8c0b4"/>
</svg>'''
(OUT/'constructed-front.svg').write_bytes(svg.encode())
(OUT/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(OUT/'constructed-front.svg'),skip_system_fonts=True))
catalogue=json.loads((ROOT/'evidence/joppa-creature-catalogue.json').read_text(encoding='utf-8'))
child=catalogue['reference_families']['child']
for item in child['images']:
    assert hashlib.sha256((DONOR/item['file']).read_bytes()).hexdigest()==item['sha256']
packet=dict(entry='BODY-HUMAN-CHILD',recorded_at=datetime.now(timezone.utc).isoformat(),
            identity='Reusable human child authoring mannequin, male/female labels share geometry',
            baseline_metadata=[record(ROOT/f'art/conversion/body-human-{sex}/v1/source-packet.json') for sex in ['male','female']],
            original_appearance='Original clothed Qud human glyphs and full captured body trees are linked in the baseline packets. No child resident or child-specific original sprite is inferred.',
            race_description='Source-derived Humanoid baseline: one head, torso/back, two arms/hands and paired feet. Native race-wide appearance prose is absent.',
            body_plan=dict(heads=1,arms=2,hands=2,legs=2,feet=2,mutations='Excluded from reusable baseline; metadata retained in original packets'),
            donor_reference=child,reference_role='Actual RimWorld Biotech child torso gives compact child body convention. It does not contain an articulated limb model or prove sex-specific child anatomy.',
            authoring='Larger head relative to torso, shorter limbs, simple smooth featureless surfaces. Explicit hands/feet are authored for Qud. No personal cosmetics or baked garment.',
            variants=dict(male='Shared child geometry',female='Shared child geometry; no supported anatomical distinction required'),
            physical_height=0.88,physical_height_kind='Authoring choice, not an exported Qud child height or age',
            registration=dict(canvas=[512,1024],contact=[256,950],layers='Separate head/neck and body with painted limbs. Clothing separately authored.'),
            clothing='FIT-HUMAN-CHILD-TEMPLATE-TUNIC owns the separate removable garment workflow; no body output accepts that fitting.',
            native_policy='No resident reassignment or native age selector established. Native acceptance waits for all conversions.')
(OUT/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
plate=Image.new('RGB',(1240,820),'#142823');plate.paste(Image.open(ROOT/'art/conversion/body-human-male/v1/source-comparison.png'),(0,0))
draw=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
draw.text((25,585),'Child torso references: actual Biotech assets. Shared featureless male/female geometry.',font=font,fill='#e3cf43')
for i,item in enumerate(child['images']):
    image=Image.open(DONOR/item['file']).convert('RGBA').resize((160,160),Image.Resampling.NEAREST)
    x=30+i*390;plate.paste(image,(x,625),image);draw.text((x+165,670),item['name'],font=font,fill='#dce4d7')
plate.save(OUT/'source-comparison.png')
