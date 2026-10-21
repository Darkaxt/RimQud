"""Freeze installed canvas identity, native connection rules and actual donor references."""
from pathlib import Path
from datetime import datetime,timezone
import re,json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');DEFS=NATIVE/'StreamingAssets/Base/ObjectBlueprints'
PRIVATE=Path('E:/Temp/rimqud-native-canvaswall-20261021');MODS=Path('D:/Steam/steamapps/workshop/content/294100')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-CANVASWALL'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert not entry['process_log']
ancestry={}
for name,f in [('CanvasWall','Walls.xml'),('Wall','Walls.xml'),('InorganicObject','PhysicalPhenomena.xml'),('PhysicalObject','PhysicalPhenomena.xml'),('Brinestalk Gate','Furniture.xml'),('Gate','Furniture.xml'),('Door','Furniture.xml'),('MountedFurniture','Furniture.xml'),('Furniture','Furniture.xml')]:
 p=DEFS/f;m=re.search(r'<object\s+Name="'+re.escape(name)+r'"[^>]*>.*?</object>',p.read_text(encoding='utf-8-sig'),re.S);assert m,name
 ob=ET.fromstring(m.group());ancestry[name]=dict(file=ref(p),selected=m.group(),inherits=ob.get('Inherits'))
zone=(PRIVATE/'ZoneManager.cs').read_text(encoding='utf-8-sig');door=(PRIVATE/'Door.cs').read_text(encoding='utf-8-sig')
assert 'if (obj.Blueprint == gameObject.Blueprint)' in zone and 'tagOrStringProperty == "*"' in zone
assert not any(t in door for t in ['PaintWith','Painted','HangingSupport'])
donors=[]
for mod,pkg,name,assets,definition,role in [
 ('2407128339','Aoba.Tent','Camping Tent',['Textures/Things/Building/Tent/Tent_south.png'],None,'Cloth tension, simple folded surface and pole outline only. No roof, triangular tent silhouette or new tent mechanics.'),
 ('2493234474','VanillaExpanded.VTEXVariations','Vanilla Textures Expanded - Variations',['Textures/Things/Building/Furniture/Drapes/VFE_DrapeSparse_south.png','Textures/Things/Building/Furniture/Drapes/VFE_DrapeSparse_east.png'],'1.6/Mods/Royalty/Patches/RoyaltyPatch.xml','Hanging fabric and narrow edge-on pole convention. Do not copy ornamental swags, tassels or crossrod.'),
 ('2608762624','VanillaExpanded.VFEArchitect','Vanilla Furniture Expanded - Architect',['Textures/Fences/PicketFence/PicketFence_MenuIcon.png','Textures/Fences/PicketFence/PicketFence_Atlas.png'],'1.6/Defs/ThingDefs_Buildings/Buildings_Structure.xml','Actual linked fence atlas/cap convention and readable borders only; native Qud connection rules and cloth identity remain authoritative.')]:
 p=MODS/mod;about=p/'About/About.xml';assert pkg.lower() in about.read_text(encoding='utf-8-sig').lower()
 donors.append(dict(name=name,package_id=pkg,workshop_id=mod,about=ref(about),assets=[ref(p/a) for a in assets],definition=ref(p/definition) if definition else None,role=role))
index=read(HERE/'native-state-index.json');assert len(index['originals'])==16 and not index['missing']
packet=dict(entry=entry['id'],identity='CanvasWall -> Wall -> InorganicObject -> PhysicalObject -> Object',description='The quickened flax of the earth was duck-weaved in a simple square pattern and hung up on pickets.',ancestry=ancestry,
 actual_native_states=ref(HERE/'native-state-index.json'),original_placeholder=entry['metadata']['original_reference'],source_correction='Inherited static tile-0-13 is a catalogue placeholder. PaintedFence tent is assigned after inherited PaintedWall and is the actual connected tile family.',
 source_code=dict(assembly=ref(NATIVE/'Managed/Assembly-CSharp.dll'),zone_manager=ref(PRIVATE/'ZoneManager.cs'),door=ref(PRIVATE/'Door.cs'),resources_sha256=hashlib.sha256((NATIVE/'resources.assets').read_bytes()).hexdigest()),
 connections=dict(recipient_bits=dict(N=1,E=2,S=4,W=8),native_suffix_order=['n','s','e','w'],required_states='isolated; four ends; two straights; four corners; four T junctions; crossing',
  same_blueprint=True,paint_part=None,paint_with=None,single_track_neighbor_wildcard=True,multi_track_wildcard_requires_nonempty_source_paint_with=True,
  named_gate='Brinestalk Gate',gate_paint_with='brinestalkfence',gate_scope='UsesGate is the native placement association, not an automatic shared paint group. Canvas has no PaintWith group. Do not add gate-neighbor flags absent source support. Preserve native gate art and state mechanics; gate is not a new ledger target.',
  attached_items='Expose cardinal midpoint join/attachment anchors. Named-gate contact is a visual authoring proxy; wildcard PaintWith=* has source support in SingleTrack only. Unknown other item groups remain unknown.',
  native_rules='Same exact blueprint joins. Nonempty PaintPart matches parts. Neighbor PaintWith=* joins SingleTrack. Equal PaintWith requires nonempty source group. MultiTrack wildcard check is guarded by nonempty source group. Preserve track-dependent behavior; do not repair it during art generation.'),
 palette=dict(primary='w',detail='r',preview='Native w (#98875f) and r (#a64a2e), separate semantic roles and one coverage'),
 source_shape='One central thin picket with red cap. East/west hanging canvas panels have a red upper hem and lower outer red folded corner. North/south connectors are a narrow red edge-on strip with intermittent primary crossbars. Not a solid masonry checker block or a roof tent.',
 native_behavior=dict(solid=True,occluding=True,organic=True,weight=100,av=1,hitpoints=15,body_type='ClothWall',immutable_when_unexplored=1,graffiti_chance_one_in=300,uses_gate='Brinestalk Gate',render_layer=7,note='Do not import BrinestalkFence Flyover or AllowMissiles declarations; maintain native collision, exploration, damage and gate ownership.'),
 donors=donors,authored_geometry='Thin complete hanging fabric with a squared central picket, upper hem, lower folded color region and subdued square weave. Hidden thickness, cloth tension and camera elevation are authored estimates. One common frame for all16 masks, no independently fitted bounds.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],anchor=[8,16],camera='Fixed cardinal map view. Calibrate world axes/pixel aspect in Blender and retain projection receipt. Source N/S connector spans tile boundaries; only declared connected sides may touch or cross canvas.'),
 evidence_required=['actual all16 states','joined multicell straight/corner/T/cross contexts','explicit attachment anchors and named gate/unknown group limits','saved editable model and controls','fresh independent structural review','neutral/detail/coverage and intended-size plate'],
 native_activation=False,native_acceptance='Pending full generation gate')
write(HERE/'source-packet.json',packet)
plate=Image.new('RGB',(1400,710),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
for i,(a,label) in enumerate([(donors[0]['assets'][0],'Tent: surface/pole only'),(donors[1]['assets'][0],'Drape south: fabric only'),(donors[1]['assets'][1],'Drape east: edge-on'),(donors[2]['assets'][0],'Linked picket outline')]):
 im=Image.open(a['path']).convert('RGBA');im=ImageOps.contain(im,(320,380),Image.Resampling.NEAREST);bg=Image.new('RGBA',(330,400),'#20382d');bg.alpha_composite(im,((330-im.width)//2,(400-im.height)//2));plate.paste(bg.convert('RGB'),(10+i*350,55));d.text((10+i*350,20),label,font=font,fill='#e3cf43')
for j,line in enumerate(['Native source: hanging duck-weave canvas on pickets;16 connected masks.', 'References supply material and border conventions. No tent roof, ornamental drape or sawn fence design.', 'Canvas self-joins; Brinestalk Gate is named for placement but has a different native PaintWith group.', 'Cardinal anchors and multicell/corner proofs are required. Native connection logic is unchanged.', 'This is source/reference evidence; no completed geometry or game acceptance claimed.']):d.text((20,485+j*38),line,font=font,fill='#e5e8d8')
plate.save(HERE/'actual-render-references-comparison.png');now=datetime.now(timezone.utc).isoformat()
for step,action,inputs in [('resolve_object_description_original_tile_palette_state','Resolve actual16 tent tiles, full native ancestry and precise self/wildcard/gate connectivity; distinguish inherited catalogue placeholder.',[ref(HERE/'extract-native-states.py')]),('select_render_reference_or_document_no_equivalent','Inspect actual installed tent, drape S/E and linked fence references for cloth/edge-on/border conventions only.',[r for donor in donors for r in donor['assets']])]:
 entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=[ref(HERE/'source-packet.json'),ref(HERE/'native-states-comparison.png'),ref(HERE/'actual-render-references-comparison.png')],review='All16 native connection shapes are retained. Named gate association does not establish matching paint group or new connection mechanics. Construction still required.',result='PASS'))
entry['current_step']='construct_faithful_shape';entry['known_issues']=['Canvas self-joins and full16 masks source-resolved; actual Blender geometry, joined contexts and attachment proof remain required.'];ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Canvas source, all16 masks, actual donor references and connection/item boundaries recorded.')
