"""Bind path facts and native variants to the requested stone-over-grass direction."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2608762624')
REF=MOD/'Textures/Terrains/Cobblestone.png'
DEFS=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml')
COLORS=DEFS.parents[1]/'Colors.xml'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='DirtPath')
resolved=next(x for x in json.loads((ROOT/'art/village/sources.json').read_text())['scenery'] if x['blueprint']=='DirtPath')
text=DEFS.read_text(encoding='utf-8-sig')
declarations={name:re.search('<object Name="'+name+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['DirtPath','DirtFloor','Floor']}
brown=next(x.attrib for x in ET.parse(COLORS).getroot().find('solidcolors') if x.get('Name')=='brown')
assert sha(DONOR/original['reference_file'])==original['reference_sha256']
packet=dict(entry='SCN-DIRTPATH',recorded_at=datetime.now(timezone.utc).isoformat(),
 source=resolved,original=original,native_declarations=declarations,
 source_files=dict(zone_terrain_sha256=sha(DEFS),colors_sha256=sha(COLORS)),
 palette_evidence=dict(foreground='&w',detail='w',native_color_name=brown,
                       interpretation='Native path color is brown; maintain muted brown stone tonal family over green grass rather than sandy-beige opaque ground.'),
 description_evidence='No Description.Short on resolved DirtPath. It inherits DirtFloor; do not invent a native cobblestone description.',
 native_variants=['Terrain/sw_ground_dots1.png','Terrain/sw_ground_dots2.png','Terrain/sw_ground_dots3.png','Terrain/sw_ground_dots4.png'],
 variant_owner='RandomTileOnMove inherited from DirtFloor. Keep native state ownership and tile provenance; renderer must not reroll simulation.',
 donor_reference=dict(file=str(REF),sha256=sha(REF),mod='Vanilla Furniture Expanded - Architect',package_id='VanillaExpanded.VFEArchitect',workshop_id='2608762624',about_sha256=sha(MOD/'About/About.xml'),role='Cobblestone scale, irregular joins and subdued material shading. Exact installed texture is a reference only; no donor ground color or cell-bounded tile is automatically accepted.'),
 user_visual_contract='Cobblestone-like paving integrated over green grass, close to original Qud palette/forms; no sand-road substitution. This is an explicitly requested interpretation, distinct from native DirtPath name and sparse ground-dot glyph.',
 authoring_requirements=['Editable stone/coverage suggestion based on source glyph and selected reference before material refinement.',
   'One top-down surface needs no invented front/side/back object views. Required states are continuous fill and path/grass connectivity: end, straight, bend, junction, isolated and diagonal-neighbor cases.',
   'Use world-continuous material coordinates and neighbor-aware coverage, not independently framed floor tiles. Transparent gaps permit grass to show through.',
   'Keep stone tint/detail coverage separate from green grass. Preserve native visibility and path ownership; do not alter passability or simulation.',
   'Record refined/patch inputs and outputs, selected masks, repeated-surface/connection previews and intended village-scale authoring review. Native validation waits until all conversions.'],
 remaining='Construct and refine the source-bound connected stone/grass surface, register material/coverage/state variants and inspect assembly; no conversion completion credit yet.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
plate=Image.new('RGB',(1400,700),'#142823');d=ImageDraw.Draw(plate)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',19)
d.text((24,18),'DIRTPATH / native facts + requested connected-stone interpretation',font=font,fill='#e3cf43')
im=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST)
plate.paste(im,(70,130),im)
ref=Image.open(REF).convert('RGB').resize((420,420),Image.Resampling.LANCZOS);plate.paste(ref,(395,105))
for xy,text in [((25,430),'Qud 16 x 24 ground-dot glyph'),((25,470),'Native foreground/detail: w'),((25,500),'w is named brown in Colors.xml'),((395,555),'Installed Architect Cobblestone'),((395,590),'Reference only; not selected output'),((865,150),'Requested visual direction:'),((865,195),'brown stone over green grass'),((865,235),'soft, connected coverage'),((865,275),'world-continuous material'),((865,315),'native visibility/state ownership'),((865,405),'No directional creature views'),((865,445),'Connection/state variants required')]:d.text(xy,text,font=font,fill='#e5e8d8')
plate.save(HERE/'source-comparison.png')
