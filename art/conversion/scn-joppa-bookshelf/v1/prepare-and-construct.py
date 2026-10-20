"""Three source bookshelf layouts with inventory-owned bright/dark spine color."""
from pathlib import Path
from collections import deque
import hashlib,json,re,subprocess
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=digest(p))
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Joppa Bookshelf','Bookshelf','BaseBookshelf','MountedFurniture','Furniture']};obj=ET.fromstring(objects['BaseBookshelf']);description=obj.find("part[@Name='Description']").get('Short')
states=json.loads((HERE/'native-state-index.json').read_text())['states'];assert len(states)==3
for state in states:assert digest(Path(state['private_mask']['path']))==state['private_mask']['sha256']
donor=Path('D:/Steam/steamapps/workshop/content/294100/2119687603/Textures/Things/Building/BookShelfSparse_south.png');about=Path('D:/Steam/steamapps/workshop/content/294100/2119687603/About/About.xml')
assembly=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed/Assembly-CSharp.dll');code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.Inventory',str(assembly)],capture_output=True,check=True).stdout
layouts=[]
for n,state in enumerate(states,1):
 im=Image.open(state['private_mask']['path']).convert('RGBA');shelves=[]
 for lo,hi,base in [(8,10,10.9),(13,15,15.9),(18,20,20.4)]:
  pts={(x,y) for y in range(lo,hi) for x in range(16) if im.getpixel((x,y))[3] and im.getpixel((x,y))[0]>128};groups=[]
  while pts:
   first=pts.pop();q=deque([first]);group=[first]
   while q:
    x,y=q.popleft()
    for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
     p=(x+dx,y+dy)
     if p in pts:pts.remove(p);q.append(p);group.append(p)
   group.sort(key=lambda p:(p[1],p[0]));xs=[p[0] for p in group];ys=[p[1] for p in group]
   groups.append(dict(source_pixels=group,source_bounds=[min(xs),min(ys),max(xs)+1,max(ys)+1],kind='horizontal' if len(set(ys))==1 and len(set(xs))>1 else 'leaning' if len(set(xs))>1 else 'upright'))
  groups.sort(key=lambda g:g['source_bounds'][0]);shelves.append(dict(base=base,groups=groups))
 layouts.append(dict(variant=n,shelves=shelves))
assert [[len(s['groups']) for s in v['shelves']] for v in layouts]==[[4,4,4],[4,3,3],[2,3,2]]
packet=dict(entry='SCN-JOPPA-BOOKSHELF',identity='Joppa Bookshelf -> Bookshelf -> BaseBookshelf -> MountedFurniture -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),source_spine_layouts=layouts,
 palette=dict(primary='w',full_detail='W',empty_detail='k',native_primary_rgb='98875f',native_full_detail_rgb='cfc041',native_empty_detail_rgb='0f3b3a',rule='Orthogonal wooden frame stays w. Source book-spine groups use native detail W when stocked and k when empty. Empty state changes tint, not tile/geometry; no invented removal/repopulation of pictured books. Gold is an extraction aid; production layers are neutral.'),
 donor_reference=dict(mod='[JPT] Human Resources',package_id='JPT.HumanResources',workshop_id='2119687603',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed BookShelfSparse_south supplies restrained wooden shelf contours, sparse spine readability and low-relief shading. Its broad four-row footprint, exact books, inventory/research mechanics and facing model are not copied.'),
 construction='Three editable tall orthogonal-plank frames retain native sparse spine groups and upright/horizontal/leaning arrangement. A shallow bottom support board within the native frame extent and book bases seated on boards are explicit physical-construction interpretation. Open-backed compartments preserve source negative space; actual backing construction is not established by the tiny icon. Exact spine thickness/heights, seams and dust remain authored.',
 native_state=dict(owner='RandomTile builder and XRL.World.Parts.Inventory',assembly_sha256=digest(assembly),inventory_stdout_sha256=hashlib.sha256(code).hexdigest(),rule='Inherited RandomTile remains three bookshelf layouts despite child default tile1. Inventory.CheckEmptyState reads EmptyDetailColor k; CheckNonEmptyState reads FullDetailColor W. No EmptyTile/FullTile tags are declared for this chain. Joppa child changes inventory population to JoppaBookshelf; pictured spines are cosmetic source marks, not actual item identities.'),
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One whole-cell transform for each frame and every spine mask. No per-book, shelf or random-layout bbox centering.'),native_behavior='Preserve mounted organic50-weight storage, non-takeability, native hanging-support tag, inventory/population/container-on interaction and sounds. No donor research/knowledge system.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
wood='''<path d="M1.2 5.6H1.85V20.85H1.2Z M14.15 5.6H14.8V20.85H14.15Z" fill="#aaa"/>
<path d="M1.15 10.9H14.85V11.6H1.15Z M1.15 15.9H14.85V16.6H1.15Z M1.15 20.4H14.85V20.9H1.15Z" fill="#aaa"/>
<path d="M1.1 5.15L3.2 3.25H12.8L14.9 5.15V6.6H1.1Z" fill="#bcbcbc"/>
<path d="M1.4 5.45H14.6 M1.4 11.15H14.6 M1.4 16.15H14.6" fill="none" stroke="#ddd" stroke-width=".1"/>'''
for layout in layouts:
 books=''
 for shelf in layout['shelves']:
  base=shelf['base']
  for group in shelf['groups']:
   x0,y0,x1,y1=group['source_bounds'];pts=group['source_pixels']
   if group['kind']=='horizontal':
    x=x0+.15;w=max(.8,x1-x0-.3);h=.55
    books+=f'<path d="M{x} {base-h}H{x+w}V{base-.05}H{x}Z" fill="#cfc041"/><path d="M{x+.15} {base-.23}H{x+w-.15}" stroke="#ece29b" stroke-width=".09"/>'
   else:
    bottom=[x for x,y in pts if y==y1-1];top=[x for x,y in pts if y==y0];xb=sum(bottom)/len(bottom)+.5;xt=xb+(.65 if sum(top)/len(top)>sum(bottom)/len(bottom) else -.65 if sum(top)/len(top)<sum(bottom)/len(bottom) else 0);yt=base-2.55
    books+=f'<path d="M{xt-.3} {yt}H{xt+.3}L{xb+.3} {base-.05}H{xb-.3}Z" fill="#cfc041"/><path d="M{xt-.15} {yt+.2}L{xb-.15} {base-.25}" stroke="#ece29b" stroke-width=".08"/>'
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><g stroke="#303030" stroke-width=".12" stroke-linejoin="round">'+wood+books+'</g></svg>'
 n=layout['variant'];(HERE/f'constructed-variant-{n}.svg').write_bytes(svg.encode());(HERE/f'constructed-variant-{n}.png').write_bytes(svg_to_bytes(svg_string=svg))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1040),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'JOPPA BOOKSHELF / three native sparse layouts > editable orthogonal wood + spines > actual JPT reference',font=font,fill='#e3cf43')
for n in range(1,4):
 x=40+(n-1)*355;im=Image.open(HERE/f'constructed-variant-{n}.png').convert('RGBA').resize((240,360),Image.Resampling.LANCZOS);plate.paste(im,(x,80),im);draw.text((x,470),f'Layout{n} / source counts '+str([len(s['groups']) for s in layouts[n-1]['shelves']]),font=font,fill='#e3cf43')
im=Image.open(donor).convert('RGBA');im.thumbnail((280,360));plate.paste(im,(1100,130),im);draw.text((1070,470),'Actual JPT sparse shelf',font=font,fill='#e3cf43')
for i,line in enumerate(['Exact native layouts are shown in native-states-comparison.png; all three inherited RandomTile choices are retained.',
 'Upright, flat and leaning spine arrangements follow source groups; books rest on boards as authored construction.',
 'Open-backed compartments and a low bottom board are physical interpretations within the source frame, not native inventory.',
 'Native stock state changes only spine detail tint: full W, empty k. Frame remains w; no book identities are invented.',
 'One full-cell mapping for every layout/mask. Native inventory, source hanging-support tag and visibility remain pending.']):draw.text((20,660+i*44),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared three source spine layouts4/4/4,4/3/3,2/3/2and exact native full/empty detail-tint contract.')
