"""Bind Random Bottle ancestry, actual native mask and installed style reference."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');DONOR=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Item/Drug/Beer/Beer_a.png')
MASK=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/random-bottle-mask.png')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'source-packet.json').exists()
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='SCN-RANDOM-BOTTLE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
objects={}
for name,filename in [('Random Bottle','Furniture.xml'),('Bottle','Furniture.xml'),('Vessel','Furniture.xml'),('WaterContainer','Items.xml'),('Item','Items.xml')]:
    p=NATIVE/filename;s=p.read_text(encoding='utf-8-sig');m=re.search(r'<object\s+Name="'+re.escape(name)+r'"[^>]*>.*?</object>',s,re.S);assert m,name;fragment=m.group();ET.fromstring(fragment);objects[name]=dict(file=private(p),selected=fragment)
assert private(MASK)['sha256']==entry['metadata']['original_reference']['native_mask_sha256']
packet=dict(entry=entry['id'],recorded_at=datetime.now(timezone.utc).isoformat(),identity='Random Bottle -> Bottle -> Vessel -> WaterContainer -> Item',description=entry['metadata']['description']['Short'],ancestry=objects,
    original_mask=private(MASK),original_tile=entry['metadata']['original_reference'],
    source_features='Long neck, flared mouth, round lower vessel and right loop handle. Lower source detail region is independently liquid-colored; the separate top pixel marker does not establish a floating physical cap.',
    source_behavior=dict(capacity=16,initial_volume=0,population_filler='RandomLiquid 1d8',manual_seal=True,liquid_visible_when_sealed=True,detail_color_by_liquid='c',transparent_tag=True,shatters_on_hit=True,
        scope='Native part/tag contracts retained, not evidence of measured glass opacity or a new tile/state family.'),
    palette=dict(primary='c',detail='c or native liquid-driven detail',rule='Neutral independent body/detail roles. Actual native palette, contents and seal behavior remain native.'),
    donor_reference=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',**private(DONOR),role='Actual beer-bottle asset supplies restrained bottle highlights and edge weight only. No beer label, amber color, cap, straight silhouette or content is copied.'),
    authored_interpretation='Hollow freeblown glass body and connected C-shaped handle, rolled mouth and low-complexity glass shading. Source top marker becomes a joined mouth glint, not a detached stopper. Depth, wall thickness and smoothing are authored.',
    states='One fixed source map tile for Random Bottle. Random liquid is content/palette, not evidence of random bottle shapes. No new seal animation, fill-level geometry, rotated furniture view or liquid simulation.',
    frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],anchor=[8,16],rule='One full-cell mapping; no alpha-bound fitting.'),native_acceptance='Pending every-conversion-generated gate')
write(HERE/'source-packet.json',packet)
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];a=np.array(Image.open(MASK).convert('RGBA'));fg=np.array(list(bytes.fromhex(palette['c'])));native=np.dstack([np.tile(fg,(24,16,1)).astype(np.uint8),a[:,:,3]]);image=Image.fromarray(native)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);out=Image.new('RGB',(1160,700),'#142823');d=ImageDraw.Draw(out);d.text((20,15),'RANDOM BOTTLE / actual Qud mask + c/c palette > source-bound glass construction > actual VTE bottle style',font=font,fill='#e3cf43')
bg=Image.new('RGBA',image.size,'#20382d');bg.alpha_composite(image);out.paste(bg.convert('RGB').resize((240,360),Image.Resampling.NEAREST),(35,70));donor=Image.open(DONOR).convert('RGBA');bg=Image.new('RGBA',donor.size,'#20382d');bg.alpha_composite(donor);out.paste(bg.convert('RGB').resize((320,320),Image.Resampling.NEAREST),(790,90))
d.text((20,460),'SOURCE / long neck + right handle',font=font,fill='#e3cf43');d.text((775,460),'VTE Beer_a / style only',font=font,fill='#e3cf43')
for i,line in enumerate(['Freeblown glass from the Fuming God Sea tradition; no modern beer label, amber glass or generic can copied.',
    'Bottle capacity16, native random liquid filler1d8, manual seal and liquid-dependent detail remain native.',
    'A joined hollow rim avoids treating the isolated source top glint as a floating stopper.',
    'One fixed source tile and common frame. Contents, seal interaction, breakage and transparency acceptance pending.']):d.text((20,530+32*i),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-reference-comparison.png')
now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step='resolve_object_description_original_tile_palette_state',action='Resolve exact bottle ancestry, native content/color/seal contracts and original mask before construction.',inputs=[private(MASK)],outputs=[ref(HERE/'source-packet.json'),ref(HERE/'source-reference-comparison.png')],review='No new random shape/state inferred; glass opacity/depth are authored.',result='PASS'))
entry['process_log'].append(dict(timestamp=now,step='select_render_reference_or_document_no_equivalent',action='Inspect actual installed VTE bottle for rendering conventions only.',inputs=[private(DONOR)],outputs=[ref(HERE/'source-reference-comparison.png')],review=packet['donor_reference']['role'],result='PASS'))
entry['current_step']='construct_faithful_shape';ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Random Bottle source and actual style reference bound before Blender modeling.')
