"""Bind the exact native pepper-sign tile to the existing reviewed geometry and layers."""
from pathlib import Path
import json,hashlib,copy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SHARED=ROOT/'art/conversion/scn-joppamillsign/blender-v2';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'model.json').exists();l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='SCN-PEPPERSIGN2';source=read(HERE.parent/'blender-v1/source-packet.json');original=read(SHARED.parent/'blender-v1/source-packet.json')
assert source['original_mask']['sha256']==original['original_mask']['sha256'];assert source['original_tile']['tile']==original['original_tile']['tile']=='Items/sw_sign_pepper.bmp'
for k in ['TileColor','DetailColor']:assert source['original_tile']['render'][k]==original['original_tile']['render'][k]
assert source['description']==original['description'] and all(source['glyph_translation'][k]==original['glyph_translation'][k] for k in ['cells','method','coverage_change'])
write(HERE/'reuse-controls.json',dict(source=ref(HERE.parent/'blender-v1/source-packet.json'),geometry=ref(SHARED/'sign.blend'),geometry_controls=ref(SHARED/'model-controls.json'),shared_registered_model=ref(SHARED/'registered/model.json'),reused_geometry_review=ref(SHARED/'registered/authoring-review.json'),reopen_evidence=ref(SHARED/'reopen-audit.json'),rule='Open shared source and save a new PepperSign2 version before editing; preserve the selected shared mill-sign source.',same_native_mask_and_tile=True,same_tile_primary_detail=True,different_text_fallback='PepperSign2 inherits ColorString r; nonempty TileColor y still controls actual tile-primary.',native_chat='Herbs and Tonics',new_blender_render=False,new_imagegen_call=False,native_activation=False))
model=copy.deepcopy(read(SHARED/'registered/model.json'));model.update(entry='SCN-PEPPERSIGN2',blueprint='PepperSign2',source=ref(HERE.parent/'blender-v1/source-packet.json'),blender_variant_controls=ref(HERE/'reuse-controls.json'),palette=source['palette'],native_behavior=source['native_behavior'],glyph_translation=source['glyph_translation'],native_state_owner='One native fixed sw_sign_pepper tile; Herbs and Tonics remains native Chat. TileColor y overrides inherited text fallback r. No new native direction/state dispatch.',reuse='Exact source-identical mill-sign geometry, glyph, complete registered layers, physical frame and palette. No new rendering or refinement is claimed.');write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(reused_layers_exact=True,same_source_tile_mask_palette=True,coverage_applied_once=True,new_blender_render=False,new_imagegen_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1540,840),'#142823');d=ImageDraw.Draw(plate)
items=[('ORIGINAL / Herbs and Tonics',Image.open(HERE.parent/'blender-v1/original-native-y-r.png')),('REUSED MANUAL SHAPE',Image.open(SHARED.parent/'blender-v1/manual-neutral-master.png')),('SOUTH / exact shared y+r',Image.open(SHARED/'registered/south-native-y-r.png')),('EAST / exact shared y+r',Image.open(SHARED/'registered/east-native-y-r.png')),('NORTH / exact shared y+r',Image.open(SHARED/'registered/north-native-y-r.png'))]
for i,(label,im) in enumerate(items):
 im=im.convert('RGBA');im=im.resize((512,768),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS);bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((280,420),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS),(15+305*i,55));d.text((15+305*i,18),label,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  sm=im.resize(size,Image.Resampling.LANCZOS);plate.paste(sm,(60+305*i+j*70,515),sm)
for i,line in enumerate(['PepperSign2 and JoppaMillSign share the exact native pepper tile, y/r roles, description and source mask.',
 'Complete saved model, real rendered S/E/N and registered masks are reused by hash; no new drawing/render is claimed.',
 'Herbs and Tonics is native chat. Inherited ColorString r is text fallback; TileColor y still owns the supports.',
 'Front painted glyph and blank supported back retain the disclosed solid-board translation. Native acceptance remains pending.']):d.text((15,645+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
paths=[HERE.parent/'blender-v1/source-packet.json',HERE.parent/'blender-v1/source-reference-comparison.png',SHARED.parent/'blender-v1/manual-neutral-master.png',SHARED/'three-view-authoring-comparison.png',SHARED/'south-neutral-master.png',SHARED/'east-neutral-master.png',SHARED/'north-neutral-master.png',SHARED/'stage-03-refined-model-3d.png',OUT/'registration-comparison.png'];write(HERE/'review-inputs.json',[ref(p) for p in paths]);print('Exact pepper-sign geometry/view/layer reuse bound to its own source and interaction metadata.')
