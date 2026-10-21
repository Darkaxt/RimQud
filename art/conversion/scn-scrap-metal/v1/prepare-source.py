"""Capture Scrap Metal's own bent-sheet identity and B/C source roles."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-SCRAP-METAL';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert not entry['process_log']
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');texts={p:p.read_text() for p in [base/'Items.xml',base/'PhysicalPhenomena.xml',base/'RootObjects.xml']};ancestry=[];nodes=[];name='Scrap Metal'
while name:
    found=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',t,re.S)) for p,t in texts.items()];found=[(p,m) for p,m in found if m];assert len(found)==1,name;p,m=found[0];node=ET.fromstring(m.group());nodes.append(node);ancestry.append(dict(name=name,definition=ref(p),object=m.group()));name=node.get('Inherits')
parts={}
for node in reversed(nodes):
    for n in node.findall('part'):parts.setdefault(n.get('Name'),{}).update(n.attrib)
assert parts['Render']['DisplayName']=='bent metal sheet' and parts['Render']['ColorString']=='&B' and parts['Render']['DetailColor']=='C' and not parts['Render'].get('TileColor');assert parts['TinkerItem']['Bits']=='B'
assert not any(n.findall('builder[@Name="RandomTile"]') for n in nodes)
native=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/scrap-metal-mask.png');assert ref(native)['sha256']==entry['metadata']['original_reference']['native_mask_sha256'];a=np.array(Image.open(native).convert('RGBA'));assert set(np.unique(a[:,:,0][a[:,:,3]>0]))=={0,255}
donor=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');texture=donor/'Textures/Things/Item/Resource/Steel/Steel_a.png';definition=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Items/Items_Resource_Stuff.xml');steel=next(n for n in ET.parse(definition).getroot() if n.findtext('defName')=='Steel')
packet=dict(entry=entry['id'],timestamp=datetime.now(timezone.utc).isoformat(),identity=' -> '.join(n['name'] for n in ancestry),display_name=parts['Render']['DisplayName'],description=parts['Description']['Short'],ancestry=ancestry,resolved_parts=parts,
    original=dict(**entry['metadata']['original_reference'],private_mask=ref(native),size=[16,24],visible_bbox=list(Image.open(native).getbbox()),roles='Source alpha=coverage; opaque R0=primary B; opaque R255=detail C. No baked background.'),
    palette=dict(primary='B',detail='C',primary_rgb='0096ff',detail_rgb='77bfcf',TileColor='Absent throughout resolved inheritance, so native tile uses ColorString &B.',policy='Neutral gray planes plus independent P/D weight and one coverage plane. Apply native blue/cyan later; do not import dull brown/steel donor palette or global tint bit11.'),
    variants=dict(native_tiles=['items/bit11.bmp'],random_builder=False,views=['one fixed source-bound map resource view'],binding='Exact Scrap Metal only. Scrap Electronics, Crystal and Energy share bit11 but have separate identity and palette.',not_applicable=['Furniture S/E/N turnaround','Clothing/body integration','Invented pile-by-stack count','Unsupported polished/repaired/burning appearance']),
    donor_reference=dict(name='Actual installed Vanilla Textures Expanded Steel_a resource art; Core Steel definition',asset=ref(texture),definition=dict(**ref(definition),object=ET.tostring(steel,encoding='unicode')),about=ref(donor/'About/About.xml'),load_folders=ref(donor/'LoadFolders.xml'),graphic_class=steel.findtext('graphicData/graphicClass'),tex_path=steel.findtext('graphicData/texPath'),
        role='Quiet broad metallic facets, edge contrast and compact resource-art shading only. The actual donor is a rounded steel lump, not a bent sheet; no close complete equivalent selected. Do not copy nugget outline, brown palette, stack variants or steel-smelting mechanics. Source Qud silhouette and bent-sheet identity govern.'),
    interpretation=dict(source_supported='Bent metal sheet from machine-fossil scrap, two opposing P/D triangular areas within diamond-like border, native B/C contrast, takeable non-solid stackable/disassemblable scrap.',authored='Shallow curled fold along each occupied sheet edge, broad dent, fine crease and a thin surviving rim. Native empty quadrants stay open rather than becoming solid gray sheet.',prohibited='No electronic traces/pads, chip housing, pins, wires, gears, riveted plate stack or intact rectangular sheet replacing source form.'),
    registration=dict(native=[16,24],master=[512,768],recipient=[256,256],source_center=[8,12],policy='Preserve source8x8visible extent in common full-cell frame; do not fill image bounds or normalize each source scrap independently.'),native_activation=False)
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1250,720),'#142823');d=ImageDraw.Draw(plate);d.text((20,18),'SCRAP METAL / bent sheet / exact source, B-C roles and actual reference',font=font,fill='#e3cf43')
gray=np.uint8(225-a[:,:,0].astype(float)/255*75);ni=Image.fromarray(np.dstack([gray,gray,gray,a[:,:,3]])).resize((256,384),Image.Resampling.NEAREST);plate.paste(ni,(35,65),ni)
w=a[:,:,0].astype(float)/255;rgb=np.uint8(np.rint((1-w[:,:,None])*np.array([0,150,255])+w[:,:,None]*np.array([119,191,207])));co=Image.fromarray(np.dstack([rgb,a[:,:,3]])).resize((256,384),Image.Resampling.NEAREST);plate.paste(co,(360,65),co)
di=Image.open(texture).convert('RGBA').resize((300,300),Image.Resampling.NEAREST);plate.paste(di,(810,100),di)
for x,s in [(25,'SOURCE P / D ROLES'),(345,'ACTUAL B / C PALETTE'),(770,'ACTUAL VTE STEEL_a')]:d.text((x,455),s,font=font,fill='#e3cf43')
for i,s in enumerate(['Same bit11 shape as other scrap; this blueprint is bent metal sheet, not a microchip.',
 'Primary B=0096ff, detail C=77bfcf. Keep both tint roles and alpha separate.',
 'Actual donor guides broad metallic shading only: do not turn Qud sheet into a nugget.',
 'One native fixed view, no source RandomTile or extra stack/direction states.',
 'Native pickup/stack/disassembly and visibility acceptance stay behind full generation.']):d.text((20,520+i*35),s,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference.png')
now=datetime.now(timezone.utc).isoformat();entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][0],action='Resolve exact Scrap Metal and complete inherited parts; verify native mask and B/C palette independently of electronics.',inputs=[ref(p) for p in texts]+[ref(native)],outputs=[ref(HERE/n) for n in ['prepare-source.py','source-packet.json','source-reference.png']],review='Six-node ancestry, bent metal sheet display name, TinkerItem Bits=B, non-solid Takeable/Stacker and no RandomTile established. Same bit11 mask does not justify copying electronics traces or its equal C/C palette. One fixed resource view; native mechanics unchanged.',result='PASS'))
entry.update(current_step=entry['required_steps'][1],known_issues=['Exact source and reference captured. Inspect actual metal shading reference, construct bent source-bound sheet and refine before registration.']);ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Resolved exact bent metal sheet, six ancestors, fixed native B/C source roles.')
