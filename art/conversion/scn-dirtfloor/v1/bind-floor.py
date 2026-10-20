"""Bind DirtFloor to the performed sparse packed-earth conversion."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOIL=ROOT/'art/conversion/tile-soil/v1'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=json.loads((SOIL/'source-packet.json').read_text())
native=Path(source['native_definition']['path']);assert hashlib.sha256(native.read_bytes()).hexdigest()==source['native_definition']['sha256']
floor=next(x for x in json.loads((ROOT/'art/village/sources.json').read_text())['scenery'] if x['blueprint']=='DirtFloor')
packet=dict(entry='SCN-DIRTFLOOR',recorded_at=datetime.now(timezone.utc).isoformat(),identity='DirtFloor -> Floor -> CosmeticObject',
 object=floor,description='No native Description.Short; Render.DisplayName is packed dirt floor.',
 producer=dict(entry='TILE-SOIL',source=asset(SOIL/'source-packet.json'),model=asset(SOIL/'registered/model.json')),
 original=source['original'],original_coverage=source['native_coverage'],native_definition=source['native_definition'],
 source_roles=source['source_color_roles'],native_selectors=source['native_selectors'],selector_limit=source['selector_limit'],
 reuse='This is the exact native object used to author TILE-SOIL. Adopt its actual source/ref/manual/refinement/coverage work; do not generate another packed-ground texture for a second ledger role.',
 state='One overhead continuous packed-earth material, with source-owned native brown and background roles, source tile aliases and actual visible floor eligibility. No creature views, depth or equipment applies.',
 separation='DirtPath inherits DirtFloor but uses its independently authored cobble interpretation. This binding must not select every subtype or overwrite actual water, furniture, vegetation or other floor/foreground winners.',
 native_acceptance='Actual native visibility/ownership, source tint/UV and RandomTileOnMove appearance binding pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
model=dict(kind='ground_blueprint_art_binding',blueprint='DirtFloor',material_model=asset(SOIL/'registered/model.json'),
 source=asset(HERE/'source-packet.json'),native_tile_aliases=source['native_selectors'],
 layers=['Actual source-owned native background','Sparse neutral packed-earth pigment with native w foreground/detail tint','Independent visible native foreground/paint or separately converted art'],
 eligibility='Only the supported actual visible native packed-floor state; DirtPath and other subtype/material ownership stay separate.',
 state='Generation-ready art binding; native ownership/tint/world-UV and cosmetic-state acceptance pending')
(HERE/'model.json').write_bytes((json.dumps(model,indent=2,ensure_ascii=False)+'\n').encode())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
original=Image.new('RGBA',(16,24),'#'+palette['k'])
for p in source['native_coverage']:original.putpixel((p['x'],p['y']),(*bytes.fromhex(palette['w']),255))
selected=Image.open(SOIL/'registered/native-color-preview.png').convert('RGB')
out=Image.new('RGB',(1280,710),'#142823');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((22,16),'DIRTFLOOR / native object bound to the performed sparse packed-earth conversion',font=font,fill='#e3cf43')
for x,im,size,label in [(55,original,(224,336),'ORIGINAL 16 x 24'),(420,selected,(352,352),'SELECTED MATERIAL PERIOD'),(925,selected.crop((64,64,128,128)),(224,336),'SELECTED ONE CELL')]:
 out.paste(im.resize(size,Image.Resampling.NEAREST if x==55 else Image.Resampling.LANCZOS).convert('RGB'),(x,90));d.text((x,470),label,font=font,fill='#e5e8d8')
for j,text in enumerate(['Native primary/detail both w; dark-teal field remains visible between the fine earth deposits.',
 'Original dots1 is exported; other declared aliases are not claimed independently observed point layouts.',
 'DirtPath is a separate source-owned material. Object/paint visibility and native state binding remain pending.']):d.text((22,540+j*35),text,font=font,fill='#e5e8d8')
out.save(HERE/'binding-comparison.png')
