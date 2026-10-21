"""Resolve exact Scrap Electronics identity, ancestry, mask and actual chip reference."""
from pathlib import Path
from datetime import datetime,timezone
import json,re,hashlib,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-SCRAP-ELECTRONICS';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert not entry['process_log']
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');texts={p:p.read_text() for p in [base/'Items.xml',base/'PhysicalPhenomena.xml',base/'RootObjects.xml']}
ancestry=[];name='Scrap Electronics';resolved={};chain=[]
while name:
    found=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',t,re.S)) for p,t in texts.items()];found=[(p,m) for p,m in found if m];assert len(found)==1,name
    p,m=found[0];node=ET.fromstring(m.group());ancestry.append(dict(name=name,definition=ref(p),object=m.group()));chain.append(node);name=node.get('Inherits')
for n in reversed(chain):
    for part in n.findall('part'):resolved.setdefault(part.get('Name'),{}).update(part.attrib)
assert resolved['Render']['Tile']=='items/bit11.bmp';assert resolved['Render']['ColorString']=='&C' and resolved['Render']['DetailColor']=='C';assert not resolved['Render'].get('TileColor')
assert not any(n.findall('builder[@Name="RandomTile"]') for n in chain)
native=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/scrap-electronics-mask.png');a=np.array(Image.open(native).convert('RGBA'));assert hashlib.sha256(native.read_bytes()).hexdigest()==entry['metadata']['original_reference']['native_mask_sha256']
assert a.shape==(24,16,4) and set(np.unique(a[:,:,0][a[:,:,3]>0]))=={0,255}
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');texture=donor/'Textures/Things/Item/Resource/SignalChip.png';definition=Path('D:/Steam/steamapps/common/RimWorld/Data/Biotech/Defs/ThingDefs_Items/Items_Resource_Manufactured.xml');dn=next(n for n in ET.parse(definition).getroot() if n.findtext('defName')=='SignalChip')
packet=dict(entry=entry['id'],timestamp=datetime.now(timezone.utc).isoformat(),identity='Scrap Electronics -> Scrap -> Item -> PhysicalObject -> Object',display_name=resolved['Render']['DisplayName'],description=resolved['Description']['Short'],ancestry=ancestry,resolved_parts=resolved,
    original=dict(**entry['metadata']['original_reference'],private_mask=ref(native),size=[16,24],visible_bbox=list(Image.open(native).getbbox()),source_roles='Opaque R0=primary, opaque R255=detail, A=coverage. Both foreground/detail are C in this blueprint.'),
    variants=dict(native_tile_choices=['items/bit11.bmp'],random_tile_builder=False,authoring_views=['fixed source-bound map view'],reason='A takeable non-furniture scrap item with one declared tile. No invented S/E/N, stack piles, repair/burning variants or procedural animation.',binding='Bind replacement to exact Scrap Electronics identity, not globally to bit11.bmp: Scrap Metal, Scrap Crystal and Scrap Energy reuse this same tile with other identities/colours.'),
    palette=dict(primary='C',detail='C',TileColor='Absent throughout resolved inheritance: native tile rendering uses ColorString &C.',rgb='77bfcf',mask_contract='Retain independent primary/detail roles even though both native tints are currently equal. Neutral artwork plus weight and coverage; do not bake cyan, donor white/blue, green PCB or background.'),
    semantics=dict(native='A fractured microchip shed/peeled from a machine fossil; TinkerItem Bits=C and inherited disassembly remain native.',authored='Diamond-like perimeter with two opposing occupied triangular regions and open fracture pockets. Etched contact traces and shallow planar thickness are authored visual interpretation, not additional source parts.',prohibited='Do not replace with complete modern green PCB, generic circuit box, pile, SignalChip micro-organ or imported mechanoid/research behavior.'),
    donor_reference=dict(name='Actual installed Vanilla Textures Expanded SignalChip texture / Biotech definition',asset=ref(texture),definition=dict(**ref(definition),object=ET.tostring(dn,encoding='unicode')),about=ref(donor/'About/About.xml'),load_folders=ref(donor/'LoadFolders.xml'),role='Quiet chip/surface contrast, compact silhouette, shallow material edge and simple resource-art shading only. Qud source controls fractured shape, scale, two-region layout and cyan palette. Reference is resource art, not pawn/furniture. No donor machinery semantics or white/blue palette.',graphic_class=dn.findtext('graphicData/graphicClass'),tex_path=dn.findtext('graphicData/texPath')),
    registration=dict(source=[16,24],manual=[512,768],source_units_per_pixel=1/32,recipient=[256,256],source_center=[8,12],policy='Full cell mapping, preserving original centered8x8visible extent; do not fill the canvas or fit each alpha bound.'),native_activation=False)
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1150,720),'#142823');d=ImageDraw.Draw(plate);d.text((20,18),'SCRAP ELECTRONICS / fractured microchip / exact source and actual reference',font=font,fill='#e3cf43')
gray=np.uint8(225-(a[:,:,0].astype(float)/255)*75);neutral=Image.fromarray(np.dstack([gray,gray,gray,a[:,:,3]]));neutral=neutral.resize((256,384),Image.Resampling.NEAREST);plate.paste(neutral,(45,65),neutral)
rgb=np.zeros((24,16,3),np.uint8);rgb[:]=[119,191,207];colored=Image.fromarray(np.dstack([rgb,a[:,:,3]])).resize((256,384),Image.Resampling.NEAREST);plate.paste(colored,(355,65),colored)
di=Image.open(texture).convert('RGBA').resize((256,256),Image.Resampling.NEAREST);plate.paste(di,(770,120),di)
for x,label in [(35,'SOURCE P / D ROLES'),(345,'ACTUAL C / C PALETTE'),(755,'ACTUAL VTE SIGNAL CHIP')]:d.text((x,455),label,font=font,fill='#e3cf43')
for i,line in enumerate(['One fixed native tile; retain diamond fracture/open pockets and source cell occupancy.',
 'Same bit11 tile is shared by other identities: this conversion is exact-blueprint scoped.',
 'Primary C and detail C match; preserve masks separately rather than baking cyan.',
 'RimWorld reference: resource shading and compact edge only, no copied shape/mechanics.',
 'No equipment assembly or furniture turnaround applies. Native acceptance stays deferred.']):d.text((20,520+i*35),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference.png')
now=datetime.now(timezone.utc).isoformat();entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][0],action='Resolve complete Scrap Electronics inheritance, exact bit11 mask, C/C palette, single native art state and exact-identity replacement boundary.',inputs=[ref(p) for p in texts]+[ref(native)],outputs=[ref(HERE/n) for n in ['prepare-source.py','source-packet.json','source-reference.png']],review='Name is fractured microchip, not a generic metal scrap heap. No inherited RandomTile or TileColor assignment. Source two-color roles remain distinct although both resolve to C. Single fixed map view; physical diamond orientation is intrinsic shape, not a three-quarter camera.',result='PASS'))
entry.update(current_step=entry['required_steps'][1],known_issues=['Exact identity/source/palette resolved. Inspect actual chip reference, then construct and refine source-bound fractured shape before registration.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Resolved',len(ancestry),'ancestors; exact fractured microchip with fixed C/C source tile.')
