"""Source-identical native Wine Vase reuses the retained Vase shape, not a new drawing."""
from pathlib import Path
import json,hashlib,re,copy,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=ROOT/'art/conversion/scn-vase';SHARED=BASE/'blender-v5';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');MASK=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/wine-vase-mask.png')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-WINE-VASE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);vase=next(e for e in ledger['entries'] if e['id']=='SCN-VASE');assert vase['generation_ready']
assert private(MASK)['sha256']==entry['metadata']['original_reference']['native_mask_sha256']==vase['metadata']['original_reference']['native_mask_sha256']
ancestry={}
for name,f in [('Wine Vase','Furniture.xml'),('Vase','Furniture.xml'),('Vessel','Furniture.xml'),('WaterContainer','Items.xml'),('Item','Items.xml')]:
 p=NATIVE/f;s=p.read_text(encoding='utf-8-sig');m=re.search(r'<object\s+Name="'+re.escape(name)+r'"[^>]*>.*?</object>',s,re.S);assert m,name;ET.fromstring(m.group());ancestry[name]=dict(file=private(p),selected=m.group())
base=read(BASE/'blender-v1/source-packet.json');donor=Path(base['donor_reference']['path']);assert private(donor)['sha256']==base['donor_reference']['sha256']
source=dict(entry='SCN-WINE-VASE',identity='Wine Vase -> Vase -> Vessel -> WaterContainer -> Item',description=entry['metadata']['description']['Short'],ancestry=ancestry,original_mask=private(MASK),original_tile=entry['metadata']['original_reference'],
 shape_reuse=dict(source_vase=ref(SHARED/'registered/model.json'),blend=ref(SHARED/'vase.blend'),controls=ref(SHARED/'model-controls.json'),same_native_tile_and_mask=True,reason='Native Wine Vase inherits Vase and uses exactly the same Items/sw_jug.bmp mask; no new silhouette, handle, band or exterior state is declared.'),
 palette=dict(primary='w pottery',detail='m fixed decorative slip',rule='Wine Vase removes RandomColors. Slip remains decorative, not a visible pool of wine or liquid-driven glass band.'),
 native_behavior=dict(capacity=64,initial_volume='1d7-1',initial_liquid='wine-1000',random_colors_removed=True,population_liquid_filler_removed=True,weight=15,takeable=False,leak_when_broken=True,mods='PotteryMods',scope='Inherited opaque pottery/storage behavior stays native; wine content is hidden by the complete wall. No liquid simulation or invented exterior state.'),
 donor_reference=base['donor_reference'],view_contract=base['per_view_contract'],actual_new_generation='None. Reuse unchanged accepted complete Blender surface and material masks, then apply exact native w/m palette.',native_activation=False,native_acceptance='Pending full generation gate')
write(HERE/'source-packet.json',source);write(HERE/'reuse-controls.json',dict(source=ref(HERE/'source-packet.json'),geometry=ref(SHARED/'vase.blend'),geometry_controls=ref(SHARED/'model-controls.json'),raw_neutral=ref(SHARED/'raw-neutral-master.png'),raw_slip=ref(SHARED/'raw-slip-pass.png'),reused_independent_geometry_review=ref(SHARED/'independent-structural-review.json'),reused_main_geometry_disposition=ref(SHARED/'registered/authoring-review.json'),reopen_evidence=ref(SHARED/'reopen-audit.json'),rule='Open retained shared Vase model, save a new Wine Vase version before making geometry changes; never overwrite its accepted shared source.',new_blender_render=False,new_imagegen_call=False,native_activation=False))
model=copy.deepcopy(read(SHARED/'registered/model.json'));model.update(entry='SCN-WINE-VASE',blueprint='Wine Vase',source=ref(HERE/'source-packet.json'),blender_variant_controls=ref(HERE/'reuse-controls.json'),palette=source['palette'],native_behavior=source['native_behavior'],native_state_owner='One Items/sw_jug.bmp tile, fixed w/m. Remove inherited RandomColors/PopulationLiquidFiller; native wine-1000 initial volume1d7-1 remains native.',reuse='Exact source-identical Vase geometry, full registered neutral layers/masks and original frame; only native tint/metadata differ.')
write(OUT/'model.json',model)
pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.array(list(bytes.fromhex(pal['w'])));dc=np.array(list(bytes.fromhex(pal['m'])));row=model['frames'][0];a=np.array(Image.open(ROOT/row['primary']['path']).convert('RGBA'));weight=np.array(Image.open(ROOT/row['detail_weight']['path'])).astype(float)/255
def tint(a,w):
 out=a.copy();out[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float)*((1-w[:,:,None])*fg+w[:,:,None]*dc)/255));out[out[:,:,3]==0,:3]=0;return Image.fromarray(out)
native=tint(a,weight);native.save(OUT/'native-w-m.png');full=np.array(Image.open(SHARED/'raw-neutral-master.png').convert('RGBA'));slip=np.array(Image.open(SHARED/'raw-slip-pass.png').convert('RGBA'));fullw=np.divide(np.minimum(slip[:,:,3],full[:,:,3]).astype(float),full[:,:,3],out=np.zeros(full.shape[:2]),where=full[:,:,3]>0);big=tint(full,fullw)
mask=np.array(Image.open(MASK).convert('RGBA'));mw=mask[:,:,0].astype(float)/255;original=np.dstack([np.uint8(np.round((1-mw[:,:,None])*fg+mw[:,:,None]*dc)),mask[:,:,3]])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1540,810),'#142823');d=ImageDraw.Draw(plate)
items=[('ORIGINAL / w+m',Image.fromarray(original)),('SHARED MANUAL SHAPE',Image.open(BASE/'blender-v1/manual-neutral-master.png')),('SHARED BLENDER REFINEMENT',Image.fromarray(full)),('WINE VASE / native w+m',big),('ACTUAL VTE URN / style',Image.open(donor))]
for i,(title,im) in enumerate(items):
 im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((280,420),Image.Resampling.NEAREST if i in [0,4] else Image.Resampling.LANCZOS),(15+305*i,55));d.text((15+305*i,18),title,font=font,fill='#e3cf43')
 if i==4:
  panel=Image.new('RGB',(280,420),'#20382d');actual=ImageOps.contain(bg.convert('RGB'),(280,420),Image.Resampling.NEAREST);panel.paste(actual,((280-actual.width)//2,(420-actual.height)//2));plate.paste(panel,(15+305*i,55))
 if i<4:
  for j,size in enumerate([(16,24),(24,36),(32,48)]):
   sm=im.resize(size,Image.Resampling.LANCZOS);plate.paste(sm,(60+305*i+j*70,515),sm)
for i,line in enumerate(['Wine Vase inherits the same source shape/mask: complete hollow pottery, two handles and two decorative bands.',
 'Fixed native w/m; RandomColors and PopulationLiquidFiller removed. Native wine-1000 volume1d7-1 is content, not a new exterior.',
 'Exact retained Blender model and neutral mask reuse. No new rendering, ImageGen drawing, or isolation is claimed.',
 'Same source cell/anchor/coverage. Native liquid storage and full-set in-game acceptance remain pending.']):d.text((15,635+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
write(OUT/'registration-decisions.json',dict(reused_layers_exact=True,source_identical_tile_mask=True,frame_anchor_unchanged=True,single_coverage=True,new_blender_render=False,new_imagegen_call=False,native_activation=False))
print('Wine Vase exact shared geometry/masks registered with source-bound fixed magenta slip and native wine metadata.')
