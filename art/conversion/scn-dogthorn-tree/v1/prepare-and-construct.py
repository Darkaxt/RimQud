"""Two source-shaped dogthorn tree proposals with thorny wood and tangled roots."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml');MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');REF=MOD/'Textures/Things/Plant/TreeOak/TreeOakA.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
index=json.loads((HERE/'native-state-index.json').read_text());assert len(index['states'])==2
for r in index['states']:assert sha(Path(r['private_mask']['path']))==r['private_mask']['sha256']
tree=ET.parse(NATIVE).getroot();native=tree.find(".//object[@Name='Dogthorn Tree']");about=ET.parse(MOD/'About/About.xml').getroot()
packet=dict(entry='SCN-DOGTHORN-TREE',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Dogthorn Tree -> Tree -> Plant -> PhysicalObject',
 description=native.find("part[@Name='Description']").get('Short'),native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode'),tree_parent=ET.tostring(tree.find(".//object[@Name='Tree']"),encoding='unicode'),plant_parent=ET.tostring(tree.find(".//object[@Name='Plant']"),encoding='unicode')),
 original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),
 source_shape='Both16x24native variants have broad irregular greasy-leaf crowns, crooked visible brown branches/trunk and a wide exposed root nest. Variant1leans its crown toward the upper right with a low left lobe; variant2has a higher central lobe and a lower right-spreading crown.',
 palette=dict(primary='G',detail='w',native_primary_rgb='00c420',native_detail_rgb='98875f',rule='Foliage is source primary; exposed trunk/branches/roots are source detail. Neutral albedo and independent wood tint mask must be extracted after refinement.'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2016436324',path=str(REF),sha256=sha(REF),role='Actual installed oak replacement supplies readable clustered leaf masses, dark game-art contours and restrained tree shading only. It is not a dogthorn species equivalent. Source root nest, thorns, branch visibility, two crown shapes and native G/w colors stay authoritative.'),
 construction='Editable thorn-splintered crooked wood and tangled exposed roots under irregular clustered pointed leaves. Neutral gray foliage and brown wood during refinement explicitly identify tint ownership; final selected layers are entirely grayscale.',
 states='Two actual RandomTile builder choices: Terrain/sw_fattree1.bmp and Terrain/sw_fattree2.bmp. They are cosmetic fixed-map-view variants, not different ages/facings/races. Native instance selection remains source-owned.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_anchor=[8,16],rule='One full-cell transform across both variants; no independent alpha-bound fit or new per-state root center.'),
 native_behavior='Preserve source occlusion, plant/hanging support, inherited non-solid physics and native tile/random selection. Dense leaf art does not add collision or new growth behavior.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
roots=['M8.4 13.4Q8 16.5 8.7 18.3L10.5 19.5 12 20.2 13.8 21.1M8.7 18.3L7.5 19.2 5 19.8 2.3 21.1M8.7 18.6L9.7 20.5 9.7 22.2 11.5 22.6M7.8 19.1L6.3 20.8 4.8 21.8M8.8 18.9L11 18.8 12.2 20.3M8 19.5L7.1 21 7.7 22.8',
 'M8.7 13.7Q9.5 16.2 8.1 18.6L7.2 19.8 5 20.7 2 21.6M8.1 18.6L10 19.4 12.2 19.6 13.6 21M8.1 19.4L8.7 21.6 10.3 22.6M7.2 19.8L5.5 20.8 4.7 22M9 19.5L10.5 20.7 12 21.4M8.2 20.4L7.1 21.3 7.6 22.2']
branches=['M8.4 18.2Q7 15.7 7.7 13.5L6.3 12 4.9 10.6M7.7 14.5L10 13 11.7 11.3M7.8 16.4L10 15.4 12.2 14.3M7.3 13L7 10.6 8.2 8.8',
 'M8.1 18.5Q9.5 16.8 8.7 14.1L7.1 12.8 5 11M8.8 14L10.5 12.5 11.5 10M9 16.4L11 15 12.1 13.6M7.6 13.2L7.2 10.4 8 8.5']
clusters=[[(4.3,5.2,2.6,1.7),(7.1,6.8,2.6,1.9),(10.6,4.1,2.3,2.1),(12.1,6.9,2.2,1.7),(10.4,9.2,3.5,1.9),(4.7,8,2,1.8),(4.5,12.3,2.2,1.5),(7.6,11.2,2.5,1.2),(10.7,14.6,2.6,1.1),(6.8,15.4,1.8,.9)],
 [(7.8,3.8,2.1,1.9),(10.9,6.1,2.4,1.7),(12.4,8,2,1.5),(7.8,8.8,3.6,1.8),(4.1,7.4,2.3,1.5),(4.2,12.1,1.5,1.7),(7.3,11.5,2.1,1.3),(12.1,13.5,2.1,1.3),(6.4,14.1,1.7,1),(10.4,15.3,1.8,.9)]]
for n in [1,2]:
 wood=''
 for path,width in [(roots[n-1],.7),(branches[n-1],1.15)]:
  wood+=f'<path d="{path}" fill="none" stroke="#4a3826" stroke-width="{width+.2}" stroke-linecap="round" stroke-linejoin="round"/><path d="{path}" fill="none" stroke="#a17a47" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
 # Prominent source-description splinters, on the exposed wood rather than a
 # new set of branches. All are an authored interpretation of unseen detail.
 for x,y,sign in [(7.8,15.4,-1),(9.1,16.7,1),(6.4,12.6,-1),(10.8,12.5,1)]:
  wood+=f'<path d="M{x} {y}l{sign*.8} -.6 {sign*-.3} 1" fill="#a17a47" stroke="#4a3826" stroke-width=".08"/>'
 leaves=''
 for i,(x,y,rx,ry) in enumerate(clusters[n-1]):
  leaves+=f'<path d="M{x-rx} {y}Q{x-rx*.8} {y-ry*.8} {x-rx*.25} {y-ry*.7}L{x} {y-ry} {x+rx*.3} {y-ry*.7}Q{x+rx*.9} {y-ry*.9} {x+rx} {y}L{x+rx*.7} {y+ry*.4}Q{x+rx*.8} {y+ry} {x} {y+ry*.8}L{x-rx*.6} {y+ry}Z" fill="#{["a4a4a4","b9b9b9","c7c7c7"][i%3]}" stroke="#4a4a4a" stroke-width=".12"/>'
  for dx,dy in [(-.5,-.2),(.4,.15),(-.1,.5)]:
   leaves+=f'<path d="M{x+dx-.5} {y+dy}q.35 -.4 .9 -.2q-.2 .45 -.9 .2" fill="none" stroke="#7d7d7d" stroke-width=".065"/>'
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{wood}{leaves}</svg>'
 (HERE/f'constructed-variant-{n}.svg').write_bytes(svg.encode());(HERE/f'constructed-variant-{n}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-variant-{n}.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,780),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,14),'DOGTHORN / two original crown/root layouts > editable thorny rooted trees > installed oak reference',font=font,fill='#e3cf43')
source=Image.open(HERE/'native-states-comparison.png').crop((45,84,301,468));plate.paste(source,(30,80))
for x,n in [(390,1),(740,2)]:
 im=Image.open(HERE/f'constructed-variant-{n}.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(x,80),im)
donor=Image.open(REF).convert('RGBA').resize((288,288),Image.Resampling.NEAREST);plate.paste(donor,(1100,100),donor)
for x,label in [(20,'Native variant1 / G + w'),(370,'Manual1 / right-leaning crown'),(720,'Manual2 / high central crown'),(1070,'VTE oak / rendering reference')]:draw.text((x,510),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['Both native RandomTile choices are retained, with distinct crowns in a shared source-cell coordinate frame.',
 'Wide tangled roots, crooked exposed branches and splintered bark belong to dogthorn; oak supplies leaf rendering only.',
 'Brown identifies wood during refinement. Selected albedo/wood mask will be neutral, with actual native G/w tint roles.',
 'Two fixed-map-view cosmetic variants; no invented ages, secondary facing, new growth simulation or clothing.']):draw.text((20,585+32*i),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
