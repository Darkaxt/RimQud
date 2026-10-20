"""Bind Tam's equipped robe to the fixed adult body and actual donor references."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
BODY=ROOT/'art/conversion/body-dromad/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
body=json.loads((BODY/'source-packet.json').read_text())
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Cloth Robe')
binding=next(x for x in body['body']['attached_parts'] if x.get('equipped') and x['equipped']['blueprint']=='Cloth Robe')
refs=[x for x in json.loads((DONOR/'apparel-textures.json').read_text()) if x['file'].startswith('worn-robe-')]
for ref in refs:assert sha(DONOR/ref['file'])==ref['png_sha256']
assert sha(DONOR/original['reference_file'])==original['reference_sha256']
packet=dict(entry='FIT-DROMAD-CLOTH-ROBE-BODY-0',recorded_at=datetime.now(timezone.utc).isoformat(),
            creature='Tam',race='Dromad',original=original,observed_binding=binding,
            body=asset(BODY/'model.json'),race_metadata=asset(BODY/'source-packet.json'),
            donor_references=refs,
            reference_decision='Actual RimWorld Duster_Male supplies long-garment outline, view and shading conventions only. It is an open coat, not an exact Qud robe equivalent. The closed goat-wool Qud robe remains authoritative; no coat lapels or fasteners are copied.',
            design_constraints=['One actual Body item, laterality 0; do not add the separately held Shillelagh.',
               'Closed plain goat-wool robe with long hem, short broad sleeves, transparent long-neck and arm openings, organic hump allowance.',
               'Description gives shale particles as red freckles. Neutral production artwork uses tonal speckle coverage; native foreground &y/detail y remain separate equipment tint ownership.',
               'Do not bake jewelry, ink, mutation features, head, hands or feet into the garment. Do not modify the selected adult body.',
               'Directional cloth follows the full body. Contact (256,950), 512 x 1024 frame, physical scale inherited from the fixed body.'],
            source_limits='Tiny native tile does not establish every seam or sleeve length; these are authored interpretations. No exact donor robe fit is assumed.',
            native_acceptance='Pending all-conversions generation gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
plate=Image.new('RGB',(1536,760),'#142823');d=ImageDraw.Draw(plate)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
def place(im,xy,size,nearest=False):
    im=im.convert('RGBA');factor=min(size[0]/im.width,size[1]/im.height)
    im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS)
    plate.paste(im,xy,im)
d.text((24,18),'TAM > DROMAD > CLOTH ROBE / source identity before fitting',font=font,fill='#e3cf43')
place(Image.open(DONOR/original['reference_file']),(45,155),(160,240),True)
d.text((24,430),'Qud: 16 x 24 tile',font=font,fill='#e5e8d8')
place(Image.open(BODY/'selected-south.png'),(290,65),(300,600))
place(Image.open(BODY/'selected-east.png'),(595,65),(300,600))
d.text((300,680),'Fixed adult dromad / front and profile',font=font,fill='#e5e8d8')
for i,f in enumerate(['south','east','north']):
    im=Image.open(DONOR/f'worn-robe-{f}.png').convert('RGBA');im=im.crop(im.getbbox())
    place(im,(1010+i*165,180),(150,280),True)
    d.text((1010+i*165,490),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['RimWorld Duster_Male: convention only','Qud garment stays CLOSED goat wool','Sparse shale freckles; neutral tint source','No open coat, belt, jewelry or staff']):
    d.text((975,550+i*30),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-comparison.png')
