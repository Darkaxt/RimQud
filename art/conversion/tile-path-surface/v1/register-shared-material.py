"""Bind the legacy path-surface ledger row to its source-bound conversion."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
PRODUCER=ROOT/'art/conversion/scn-dirtpath/v1'
SELECTED=PRODUCER/'registered'
OLD=ROOT/'art/village/scenery/surface-sand.png'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=json.loads((PRODUCER/'source-packet.json').read_text())
producer=json.loads((SELECTED/'model.json').read_text())
workflow={name:asset(PRODUCER/path) for name,path in [
 ('original_metadata','source-packet.json'),('source_and_donor_plate','source-comparison.png'),
 ('editable_manual','constructed-stones.svg'),('manual_composition','constructed-connections-comparison.png'),
 ('initial_refinement','refined-material-proposal.png'),('patch','patched-neutral-material.png'),
 ('patched_composition','patched-connections-comparison.png'),('composed_refinement','refined-patched-material.png'),
 ('selected_registration','registered/model.json'),('selected_native_scale','registered/joppa-comparison.png')]}
packet=dict(entry='TILE-SAND',recorded_at=datetime.now(timezone.utc).isoformat(),
 actual_subject='DirtPath path-surface material; historical sand filename only',
 source_blueprint='DirtPath',source_metadata=source,
 historical_draft=asset(OLD),producer_entry='SCN-DIRTPATH',workflow_reuse=workflow,
 reuse_policy='This row and SCN-DIRTPATH own the same path material at different catalogue levels. Adopt the already-performed source-bound conversion and inspect its material binding/scale here; do not spend another ImageGen call or generate a divergent duplicate texture.',
 scope='Native DirtPath and its recorded ground-dot selectors only. Do not globally replace Qud natural sand or the installed donor Sand asset.',
 required_states='One top-down seamless material with the producer eight-neighbor coverage. No liquid depth, creature perspectives or clothing fit applies.',
 remaining_native='Resolve the legacy donor-slot alias in the final integrated set, then verify native visibility/tint/connection behavior after every entry is generation-ready.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
model=dict(kind='terrain_material_binding',subject='Qud DirtPath connected stone surface',
 producer_entry='SCN-DIRTPATH',producer_model=asset(SELECTED/'model.json'),
 neutral_material=producer['neutral_material'],stone_coverage=producer['stone_coverage'],
 world_period_cells=producer['world_period_cells'],logical_cell_pixels=64,
 palette=producer['source_palette'],native_tile_selectors=producer['native_tile_selectors'],
 connectivity=producer['coverage'],legacy_slot='sand.png (historical path-slot label; do not treat it as a native Sand blueprint)',
 binding_scope='Only the source-bound DirtPath presentation in the bounded village conversion. Natural sand and unrelated donor resources are outside this binding.',
 state='Generation-ready material authoring; runtime slot binding and native acceptance deferred until the all-conversions gate')
(HERE/'model.json').write_bytes((json.dumps(model,indent=2)+'\n').encode())
material=Image.open(SELECTED/'qud-material-preview.png').convert('RGBA')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1300,690),'#142823');d=ImageDraw.Draw(plate)
d.text((18,14),'PATH MATERIAL / historical sand draft > source-bound stone with independent grass',font=font,fill='#e3cf43')
old=Image.open(OLD).convert('RGB').resize((384,384),Image.Resampling.LANCZOS);plate.paste(old,(24,70))
new=material.crop((0,0,256,256));bg=Image.new('RGBA',new.size,'#004808');bg.alpha_composite(new)
plate.paste(bg.resize((384,384),Image.Resampling.LANCZOS).convert('RGB'),(450,70))
d.text((24,475),'Historical sand draft / rejected direction',font=font,fill='#e5e8d8')
d.text((450,475),'Selected / four-cell material window',font=font,fill='#e5e8d8')
for i,(cw,ch) in enumerate([(16,24),(24,36)]):
    native=bg.resize((cw*4,ch*4),Image.Resampling.LANCZOS).convert('RGB')
    x=890+i*180;plate.paste(native,(x,70));d.text((x,245),f'{cw} x {ch} cell',font=font,fill='#e3cf43')
    inspect=native.resize((native.width*2,native.height*2),Image.Resampling.NEAREST)
    plate.paste(inspect,(x-10,300))
for i,text in enumerate(['Production RGB stays neutral; this preview applies exact native brown w.',
                         'Transparent gaps retain independent green ground. Context grass is not converted here.',
                         'One world material and separate neighbor coverage; no opaque sand fill or cell UV reset.',
                         'Same original/refinement/patch evidence is linked; no duplicate artwork or native test.']):
    d.text((24,550+i*28),text,font=font,fill='#e5e8d8')
plate.save(HERE/'material-binding-comparison.png')
