"""Resolve source colour ownership and record inspected native/donor reference roles."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'palette-resolution.json').exists();data=read(HERE/'native-state-index.json');samples=[]
for s in data['states']:
    a=np.array(Image.open(s['private_mask']['path']).convert('RGBA'));red=sorted(set(a[a[:,:,3]>0,0].tolist()));assert red==[0]
    samples.append(dict(native_tile=s['native_tile'],visible_red_values=red,covered_pixels=int((a[:,:,3]>0).sum()),private_mask=s['private_mask']))
resolution=dict(shader_contract='Verified installed Kobold dual-color contract: alpha is coverage; visible R0 selects foreground. Background is outside coverage, not an object detail region.',samples=samples,
    primary='K',background='k',detail='No visible source detail pixels in any of the five masks. Inherited/default DetailColor therefore has no visible effect on this source family.',
    authoring='Use grayscale material shading and primary K tint only. Preserve alpha gaps between fragments. Do not invent a bright lens/ink/wire secondary palette or fill transparency with ^k background.',
    source_packet_note='Initial source packet recorded inherited detail as unresolved. Actual mask analysis resolves its visual relevance without guessing a default or changing the original record.',native_activation=False)
write(HERE/'palette-resolution.json',resolution)
im=Image.open(HERE/'source-reference-variants.png').convert('RGB');d=ImageDraw.Draw(im);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.rectangle((1120,350,1399,385),fill='#142823');d.text((1125,355),'Tile-7-3.png',font=font,fill='#e5e8d8')
d.rectangle((10,802,1399,899),fill='#142823')
d.text((18,809),'All5visible masks have R=0: primary K only. ^k is background, not a detail-colour layer.',font=font,fill='#e5e8d8')
d.text((18,841),'Four native builder choices + declared fallback. Fixed source view; next is faithful manual construction.',font=font,fill='#e5e8d8')
im.save(HERE/'source-reference-variants-reviewed.png')
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-GARBAGE';entry=next(e for e in ledger['entries'] if e['id']=='SCN-GARBAGE');now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][0],action='Inspect actual five masks to resolve visible palette ownership before constructing replacement art.',inputs=[ref(HERE/'native-state-index.json'),ref(HERE/'source-packet.json')],outputs=[ref(HERE/'review-source.py'),ref(HERE/'palette-resolution.json'),ref(HERE/'source-reference-variants-reviewed.png')],review='All visible source pixels are R0, so no default DetailColor guess is needed. Native K is primary and ^k is outside-coverage background. Preserve all fragment gaps, no invented bright secondary material palette. Initial source packet remains unchanged as historical evidence.',result='PASS'))
entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][1],action='Inspect actual Core TrashA/B/C and Filth_Trash Graphic_Cluster as map-scatter rendering references.',inputs=[ref(HERE/'source-packet.json')],outputs=[ref(HERE/'source-reference-variants-reviewed.png')],review='Viewed native four choices/fallback and actual Core textures. Core provides simple fragment overlap/edge shading and scatter readability only. Its sparse bar-shaped scraps, contents, colours, procedural cluster placement, cleaning/disappearance and filth behavior are not imported. Qud source layouts and lens/ink/lug/wire prose govern authored design; unseen fragment identities remain estimates.',result='PASS'))
entry.update(current_step=entry['required_steps'][2],known_issues=['All four actual random trash tiles plus declared fallback and Core references are resolved/inspected. Visible palette uses only primary K; ^k is background. Faithful editable construction for each source layout, actual refinement, extraction/registration and final art review remain unfinished.'],source_state_inventory=dict(random_tile_choices=[r['native_tile'] for r in data['states'] if r['role']=='RandomTile choice'],declared_fallback=next(r['native_tile'] for r in data['states'] if r['role']!='RandomTile choice'),palette_resolution=ref(HERE/'palette-resolution.json')))
ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Resolved primary-only source palette and actual Core reference roles; Garbage is active at manual construction, without readiness credit.')
