"""One-coverage detail-only native basket, plus retained common-frame authoring views."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'model.json').exists();source=json.loads((HERE.parent/'blender-v1/source-packet.json').read_text());pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];color=np.array(list(bytes.fromhex(pal['w'])));views={};large={}
for facing in ['south','east','north']:
 a=np.array(Image.open(HERE/f'{facing}-neutral-master.png').convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;p=np.array(Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS));p[p[:,:,3]<4]=0;weight=np.where(p[:,:,3]>0,255,0).astype(np.uint8);row={}
 for key,im in dict(primary=Image.fromarray(p),detail=Image.fromarray(p),coverage=Image.fromarray(p[:,:,3]),detail_weight=Image.fromarray(weight),detail_coverage=Image.fromarray(p[:,:,3]),authored_dualcolor_mask=Image.fromarray(np.dstack([weight,weight,weight,p[:,:,3]]))).items():
  path=OUT/f'{facing}-{key}.png';im.save(path);row[key]=ref(path)
 native=p.copy();native[:,:,:3]=np.uint8(np.round(p[:,:,:3].astype(float)*color/255));native[native[:,:,3]==0,:3]=0;Image.fromarray(native).save(OUT/f'{facing}-native-w.png');big=a.copy();big[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float)*color/255));big[big[:,:,3]==0,:3]=0;large[facing]=Image.fromarray(big);views[facing]=row
frame=dict(native_tile='Items/sw_basket.bmp',**views['south'])
model=dict(entry='SCN-WOVEN-BASKET',kind='source_detail_only_woven_container',blueprint='Woven Basket',workflow='blender-first-v1',source=ref(HERE.parent/'blender-v1/source-packet.json'),blender_source=ref(HERE/'basket.blend'),blender_controls=ref(HERE/'model-controls.json'),registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full cell/pivot for all exports; no bounds-based resizing.'),palette=source['palette'],native_behavior=source['source_behavior'],native_state_owner='EmptyTile and FullTile are both Items/sw_basket.bmp. Retain native Container/Inventory and organic/furniture behavior; no new lid, contents or facing dispatch.',view_policy=source['view_contract'],frames=[frame],retained_authoring_views=views,formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',native_activation=False,native_acceptance='Pending full generation gate')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(visible_source_ink_all_detail=True,coverage_applied_once=True,identical_full_cell_mapping=True,production_facing='south',retained_auxiliary_facings=['east','north'],new_native_direction_states=False,new_imagegen_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1540,810),'#142823');d=ImageDraw.Draw(plate);mask=np.array(Image.open(source['original_mask']['path']).convert('RGBA'));original=Image.fromarray(np.dstack([np.tile(color,(24,16,1)).astype(np.uint8),mask[:,:,3]]))
items=[('ORIGINAL / detail w',original),('MANUAL / complete shape',Image.open(HERE.parent/'blender-v1/manual-neutral-master.png')),('SOUTH / native detail w',large['south']),('EAST / authoring export',large['east']),('NORTH / authoring export',large['north'])]
for i,(label,im) in enumerate(items):
 im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((280,420),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS),(15+305*i,55));d.text((15+305*i,18),label,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  sm=im.resize(size,Image.Resampling.LANCZOS);plate.paste(sm,(60+305*i+j*70,515),sm)
for i,line in enumerate(['Complete woven reed bowl, bound rim, continuous carrying arch and fitted over/under warp/weft; empty cavity retained.',
 'All visible original ink uses native detail w. Gray reed shading remains neutral; one coverage controls the whole sprite.',
 'Actual shared-model S/E/N rotations. South alone maps the original tile; auxiliary views create no native direction states.',
 'Identical native EmptyTile/FullTile, Container/Inventory and organic behavior remain native. No in-game acceptance yet.']):d.text((15,635+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Basket source tile and retained S/E/N exports registered with original detail-only tint ownership.')
