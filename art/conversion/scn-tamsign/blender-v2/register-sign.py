"""Register the intact painted plaque and actual support ownership under one coverage."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
review=json.loads((HERE/'independent-structural-review.json').read_text());assert review['recommendation']=='pass' and not review['fix_now']
OUT.mkdir(exist_ok=True);assert not (OUT/'model.json').exists()
source=json.loads((HERE.parent/'blender-v1/source-packet.json').read_text());pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.array(list(bytes.fromhex(pal['y'])));dt=np.array(list(bytes.fromhex(pal['r'])));views={};large={}
for facing in ['south','east','north']:
 a=np.array(Image.open(HERE/f'{facing}-neutral-master.png').convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0
 p=np.array(Image.fromarray(a).resize((256,256),Image.Resampling.LANCZOS));p[p[:,:,3]<4]=0
 da=np.array(Image.open(HERE/f'{facing}-detail-pass.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS))[:,:,3];da=np.minimum(da,p[:,:,3]);weight=np.uint8(np.round(np.divide(da.astype(float)*255,p[:,:,3],out=np.zeros_like(da,dtype=float),where=p[:,:,3]>0)))
 row={}
 for key,im in dict(primary=Image.fromarray(p),detail=Image.fromarray(p),coverage=Image.fromarray(p[:,:,3]),detail_weight=Image.fromarray(weight),detail_coverage=Image.fromarray(da),authored_dualcolor_mask=Image.fromarray(np.dstack([weight,weight,weight,p[:,:,3]]))).items():
  path=OUT/f'{facing}-{key}.png';im.save(path);row[key]=ref(path)
 native=p.copy();native[:,:,:3]=np.uint8(np.round(p[:,:,:3].astype(float)*((1-weight[:,:,None]/255)*fg+weight[:,:,None]/255*dt)/255));native[native[:,:,3]==0,:3]=0;Image.fromarray(native).save(OUT/f'{facing}-native-y-r.png');views[facing]=row;large[facing]=Image.fromarray(native).resize((512,768),Image.Resampling.LANCZOS)
frame=dict(native_tile='Items/sw_sign_goods.bmp',**views['south'])
model=dict(entry='SCN-TAMSIGN',kind='painted_terracotta_sign',blueprint='TamSign',workflow='blender-first-v1',source=ref(HERE.parent/'blender-v1/source-packet.json'),blender_source=ref(HERE/'sign.blend'),blender_controls=ref(HERE/'model-controls.json'),registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full cell/pivot for all exports; no bounds-based resizing.'),palette=source['palette'],native_behavior=source['native_behavior'],glyph_translation=source['glyph_translation'],native_state_owner='One native fixed sw_sign_goods tile; Salt Sundries remains native Chat text. No new native direction/state dispatch.',view_policy=source['view_contract'],frames=[frame],retained_authoring_views=views,formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',native_activation=False,native_acceptance='Pending full generation gate')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(primary='TileColor y supports; TileColor y overrides text fallback ColorString r',detail='r plaque and dark pictogram paint',glyph_alpha_translation=source['glyph_translation']['coverage_change'],coverage_applied_once=True,identical_full_cell_mapping=True,production_facing='south',retained_auxiliary_facings=['east','north'],new_native_direction_states=False,new_imagegen_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1540,820),'#142823');d=ImageDraw.Draw(plate)
items=[('ORIGINAL / native y+r',Image.open(HERE.parent/'blender-v1/original-native-y-r.png')),('MANUAL / complete shape',Image.open(HERE.parent/'blender-v1/manual-neutral-master.png')),('SOUTH / painted front',large['south']),('EAST / actual depth',large['east']),('NORTH / blank back',large['north'])]
for i,(label,im) in enumerate(items):
 im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((280,420),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS),(15+305*i,55));d.text((15+305*i,18),label,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  sm=im.resize(size,Image.Resampling.LANCZOS);plate.paste(sm,(60+305*i+j*70,515),sm)
for i,line in enumerate(['Solid painted terracotta board with two rear supports; exact source pictogram positions become dark matte paint.',
 'Explicit physical interpretation: source negative glyph cells gain opaque painted coverage; no literal through-holes claimed.',
 'Native tile-primary y and detail r, neutral shading, one coverage. Salt Sundries is retained as native chat, not new art lettering.',
 'Common model/frame for S/E/N; only south maps the native tile. All native acceptance waits for the complete generation gate.']):d.text((15,640+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Painted sign registered with shared frame and one-coverage native y/r ownership.')
