"""Bind the two-handled canyon pottery source before modeling."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');MASK=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/vase-mask.png');DONOR=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Building/Misc/Urn.png')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'source-packet.json').exists()
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='SCN-VASE';entry=next(e for e in ledger['entries'] if e['id']=='SCN-VASE')
ancestry={}
for name,f in [('Vase','Furniture.xml'),('Vessel','Furniture.xml'),('WaterContainer','Items.xml'),('Item','Items.xml')]:
 p=NATIVE/f;s=p.read_text(encoding='utf-8-sig');m=re.search(r'<object\s+Name="'+re.escape(name)+r'"[^>]*>.*?</object>',s,re.S);assert m,name;ET.fromstring(m.group());ancestry[name]=dict(file=private(p),selected=m.group())
assert private(MASK)['sha256']==entry['metadata']['original_reference']['native_mask_sha256']
packet=dict(entry='SCN-VASE',identity='Vase -> Vessel -> WaterContainer -> Item',description=entry['metadata']['description']['Short'],ancestry=ancestry,original_mask=private(MASK),original_tile=entry['metadata']['original_reference'],
 source_features='Large rounded pottery bowl, long narrow neck, flared open mouth and two side loop handles. Source detail rows14 and16 define two decorative slip bands.',
 native_behavior=dict(capacity=64,initial_volume=0,population_filler='VesselLiquid_Standard 1d6',random_colors=dict(main='w',detail='all'),weight=15,takeable=False,leak_when_broken=True,mods='PotteryMods',scope='Native liquid storage, randomized slip color and pottery behavior remain native. No new state or fill simulation.'),
 palette=dict(primary='w pottery',detail='g default decorative slip; RandomColors detail all remains native',rule='Neutral material and independent slip ownership; do not bake donor white or the default detail green.'),
 donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',**private(DONOR),role='Actual Urn.png supplies restrained pottery shading and open-rim/edge convention only. Keep the Qud long neck, pair of handles and two slip bands.'),
 authored_interpretation='A complete hollow lathed pottery wall, joined two handles and two circumferential slip bands. Hidden depth, wall thickness, smoothed contours and shallow camera elevation are authored.',
 per_view_contract=dict(production='One original fixed map view: both symmetric handles connect neck to shoulder; two slip bands remain on bowl; visible open rim.',diagnostic='Angled actual model shows hollow mouth, handle depth and continuation of both decorative rings.',scale='One16x24 source cell ->512x768 manual ->256square recipient. Anchor8,16; no alpha-bound sizing.'),
 states='One fixed native tile. RandomColors changes palette and liquid filling changes contents, not evidence of extra exterior geometry or a directional family.',native_activation=False,native_acceptance='Pending full generation gate')
write(HERE/'source-packet.json',packet)
pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];a=np.array(Image.open(MASK).convert('RGBA'));w=a[:,:,0]/255;fg=np.array(list(bytes.fromhex(pal['w'])));dc=np.array(list(bytes.fromhex(pal['g'])));native=np.dstack([np.uint8(np.round((1-w[:,:,None])*fg+w[:,:,None]*dc)),a[:,:,3]]);im=Image.fromarray(native)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1160,700),'#142823');d=ImageDraw.Draw(plate)
d.text((20,18),'VASE / actual Qud source w/g > hollow two-handled pottery > actual VTE urn style',font=font,fill='#e3cf43')
for x,asset,size in [(35,im,(256,384)),(790,Image.open(DONOR).convert('RGBA'),(320,320))]:
 bg=Image.new('RGBA',asset.size,'#20382d');bg.alpha_composite(asset);plate.paste(bg.convert('RGB').resize(size,Image.Resampling.NEAREST),(x,75))
for i,line in enumerate(['Source: large storage vase, decorative slip, canyon-dweller home kiln; two handles and two native detail bands.',
 'VTE urn: actual installed material/rim reference. Its short neck, pedestal and handle-free shape are not copied.',
 'Native default w/g with RandomColors detail all; capacity64 and standard filler1d6 remain native.',
 'Opaque pottery hides contents. One fixed native map view; full editable hollow object, no invented extra tile states.']):d.text((20,525+i*34),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference-comparison.png')
now=datetime.now(timezone.utc).isoformat()
for step,action,inputs in [('resolve_object_description_original_tile_palette_state','Bind installed ancestry, original mask, slip palette and native content behavior.',[private(MASK)]),('select_render_reference_or_document_no_equivalent','Inspect actual VTE urn as pottery/rim convention; source supplies two handles, neck and slip bands.',[private(DONOR)])]:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=[ref(HERE/'source-packet.json'),ref(HERE/'source-reference-comparison.png')],review='Source facts and authored depth remain distinct; native acceptance gated.',result='PASS'))
entry['current_step']='construct_faithful_shape';ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Vase source, native palette/state and actual urn reference recorded.')
