"""Bind the completed starapple artwork to its source-identical ripe blueprint."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,copy,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRODUCER=ROOT/'art/conversion/scn-starapple-tree/v1';SOURCE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml')
assert not (HERE/'model.json').exists(),'Never overwrite logged binding'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
tree=ET.parse(SOURCE).getroot();base=tree.find(".//object[@Name='Starapple Tree']");ripe=tree.find(".//object[@Name='Starapple Tree Ripe']")
for name in ['Render','Description']:assert base.find(f"part[@Name='{name}']").attrib==ripe.find(f"part[@Name='{name}']").attrib,name
bh=dict(base.find("part[@Name='Harvestable']").attrib);rh=dict(ripe.find("part[@Name='Harvestable']").attrib);base_chance=bh.pop('StartRipeChance');ripe_chance=rh.pop('StartRipeChance');assert bh==rh and base_chance=='1:5' and ripe_chance=='1:1';assert base.get('Inherits')==ripe.get('Inherits')=='Tree'
j=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'));producer=next(x for x in j['entries'] if x['id']=='SCN-STARAPPLE-TREE');consumer=next(x for x in j['entries'] if x['id']=='SCN-STARAPPLE-TREE-RIPE');assert producer['generation_ready'] and j['active_entry']==consumer['id']
assert producer['metadata']['original_reference']['native_mask_sha256']==consumer['metadata']['original_reference']['native_mask_sha256']
packet=dict(entry=consumer['id'],recorded_at=datetime.now(timezone.utc).isoformat(),identity='Starapple Tree Ripe -> Tree -> Plant -> PhysicalObject',reuse_of_entry=producer['id'],
 source_definition=dict(path=str(SOURCE),sha256=sha(SOURCE),selected=ET.tostring(ripe,encoding='unicode')),
 source_comparison=dict(render='Exact attribute equality',description='Exact attribute equality',parent='Both inherit Tree',harvest='Same harvest appearance and yield fields; only StartRipeChance differs1:5versus1:1',mask_sha256=consumer['metadata']['original_reference']['native_mask_sha256']),
 producer_packet=asset(PRODUCER/'source-packet.json'),producer_model=asset(PRODUCER/'registered/model.json'),
 producer_workflow='Adopt the actually performed source/installed-reference/editable-construction/ImageGen-refinement/halo-correction/neutral-fruit-mask workflow. No new ImageGen call is claimed and no duplicate tree design is created.',
 appearance='Same fixed tree and fruit mask; native g primary with R ripe detail and K unripe detail.1:1initial ripeness does not mean permanently ripe or an independent frozen-red texture.',
 native_behavior='Keep actual native Harvestable state/yield/regeneration, visibility and physics. Do not use a permanently ripe art binding or new schedule to override it.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
model=copy.deepcopy(json.loads((PRODUCER/'registered/model.json').read_text()));model.update(entry=consumer['id'],blueprint='Starapple Tree Ripe',source_binding=asset(HERE/'source-packet.json'),reuse_of_entry=producer['id'],source_model=asset(PRODUCER/'registered/model.json'));(HERE/'model.json').write_bytes((json.dumps(model,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,780),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'STARAPPLE RIPE BINDING / identical artwork and state tints / only starting ripeness differs',font=font,fill='#e3cf43')
for x,file,label in [(50,'ripe-native-preview.png','Normal / possible ripe appearance'),(520,'ripe-native-preview.png','Ripe sibling / same appearance'),(990,'unripe-native-preview.png','Either / native unripe appearance')]:
 im=Image.open(PRODUCER/'registered'/file).convert('RGBA').resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,65),im);draw.text((x,525),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['Installed Render, Description, ancestry and Harvestable appearance fields match exactly; native masks are identical.',
 'Only initial ripe chance differs: Starapple Tree1:5, Starapple Tree Ripe1:1. Both later retain native harvest/unripe state.',
 'One actual conversion workflow is reused with producer hashes and evidence; no duplicate generation call is invented.',
 'Same neutral layers, fruit ownership and anchor. Native interaction/state/visibility acceptance remains pending.']):draw.text((20,585+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'binding-comparison.png');print('Bound exact shared starapple art to ripe sibling; source appearance equality confirmed.')
