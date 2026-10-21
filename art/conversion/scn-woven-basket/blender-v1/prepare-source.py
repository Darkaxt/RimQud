"""Bind reed basket glyph, dry-container metadata and actual woven RimWorld reference."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');MASK=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/woven-basket-mask.png');MOD=Path('D:/Steam/steamapps/workshop/content/294100/2249071438');DONOR=MOD/'Common/Textures/Things/HMC_Woven_Basket/HMC_Woven_Basket.png'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'source-packet.json').exists();ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='SCN-WOVEN-BASKET';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert private(MASK)['sha256']==entry['metadata']['original_reference']['native_mask_sha256']
ancestry={}
for name,f in [('Woven Basket','Furniture.xml'),('Furniture','Furniture.xml'),('InorganicObject','PhysicalPhenomena.xml'),('PhysicalObject','PhysicalPhenomena.xml')]:
 p=NATIVE/f;s=p.read_text(encoding='utf-8-sig');m=re.search(r'<object\s+Name="'+name+r'"[^>]*>.*?</object>',s,re.S);assert m,name;ET.fromstring(m.group());ancestry[name]=dict(file=private(p),selected=m.group())
a=np.array(Image.open(MASK).convert('RGBA'));assert np.all(a[:,:,0][a[:,:,3]>0]==255)
packet=dict(entry=entry['id'],identity='Woven Basket -> Furniture -> InorganicObject -> PhysicalObject -> Object',description=entry['metadata']['description']['Short'],ancestry=ancestry,original_mask=private(MASK),original_tile=entry['metadata']['original_reference'],
 source_features='Low rounded woven vessel beneath a tall arching carry loop. Bottom warp/weft marks establish woven reed material. Small internal glyph marks do not identify actual inventory contents.',
 source_behavior=dict(container=True,inventory=True,empty_tile='Items/sw_basket.bmp',full_tile='Items/sw_basket.bmp',dont_warn_on_open=True,weight=3,organic=True,takeable=False,scope='Native dry-goods inventory/open behavior, furniture tags and organic damage remain native. Empty/full tile is identical; no new lid or contents state.'),
 palette=dict(primary='w metadata foreground, unused by visible source ink',detail='w all visible reed ink',original_ink_all_detail=True,rule='Keep neutral reed shading and one coverage; all visible shape uses detail ownership, as in the original mask.'),
 donor_reference=dict(mod='Primitive Storage',package_id='PrimitiveStorage.velcroboy333',workshop_id='2249071438',**private(DONOR),about=private(MOD/'About/About.xml'),role='Actual installed woven storage basket supplies reed-crossing/shadow/edge convention. Keep the source rounded bowl and tall single arch; do not import rectangular donor footprint, capacity, stored goods or game behavior.'),
 authored_interpretation='A complete hollow close-woven bowl with bound rim, one tall carry loop and visible warp/weft courses. Hidden depth, thickness, strand count and weave geometry are authored; no contents inferred.',
 view_contract=dict(south='Source map-facing tall arch left/right over open low bowl; two loop ends continue into bound rim/wall.',east='Actual same object profile, adequate bowl depth, physically edge-on loop; no independent panel compression.',north='Actual same object back, same complete arch/rim and continuous weave.',production='One original fixed map tile only. East/north are retained authoring views, not new native direction states.',scale='16x24 native source ->512x768 manual ->256square recipient, anchor8,16; one physical frame for all exports.'),native_activation=False,native_acceptance='Pending full generation gate')
write(HERE/'source-packet.json',packet)
pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];color=np.array(list(bytes.fromhex(pal['w'])));native=Image.fromarray(np.dstack([np.tile(color,(24,16,1)).astype(np.uint8),a[:,:,3]]));font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1160,700),'#142823');d=ImageDraw.Draw(plate);d.text((20,18),'WOVEN BASKET / actual Qud w/w > complete reed vessel + carry loop > actual Primitive Storage weave',font=font,fill='#e3cf43')
for x,im,box in [(35,native,(256,384)),(780,Image.open(DONOR).convert('RGBA'),(330,330))]:
 bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(ImageOps.contain(bg.convert('RGB'),box,Image.Resampling.NEAREST),(x,80))
for i,line in enumerate(['Marsh reed, handcrossed warp and weft; source low bowl and tall arch preserved, no goods invented.',
 'Primitive Storage actual woven basket is a material/edge reference; source supplies the rounded shape and carry loop.',
 'All visible original ink is detail w. Container/Inventory and identical EmptyTile/FullTile remain native.',
 'Retain common-frame S/E/N authoring renders. One native map tile; no new direction, lid or content states.']):d.text((20,525+i*34),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference-comparison.png');now=datetime.now(timezone.utc).isoformat()
for step,action,inputs in [('resolve_object_description_original_tile_palette_state','Bind exact reed-basket ancestry, original detail-only mask and identical empty/full native tile.',[private(MASK)]),('select_render_reference_or_document_no_equivalent','Inspect installed Primitive Storage woven basket for material convention only.',[private(DONOR),private(MOD/'About/About.xml')])]:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=[ref(HERE/'source-packet.json'),ref(HERE/'source-reference-comparison.png')],review='Actual source identity, ambiguous glyph marks and authored hidden geometry remain distinct.',result='PASS'))
entry['current_step']='construct_faithful_shape';ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger);print('Basket source, native contracts and actual woven reference recorded.')
