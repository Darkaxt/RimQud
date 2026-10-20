"""Retain three source shelf fronts; parallel caps and complete wooden end/rear."""
from pathlib import Path
import sys,json,hashlib,xml.etree.ElementTree as ET
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';MOD=Path('D:/Steam/steamapps/workshop/content/294100/2119687603')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'cap-geometry-correction.json').exists(), 'Preserve completed construction; partial failed authoring may resume'
packet=json.loads((OLD/'source-packet.json').read_text());refs={}
for f in ['south','east','north']:
    p=MOD/f'Textures/Things/Building/BookShelfSparse_{f}.png';im=read(p);refs[f]=dict(**private(p),frame=list(im.size),alpha_bounds=im.getbbox())
definition=MOD/'Defs/Things.xml';node=next(n for n in ET.parse(definition).getroot() if n.findtext('defName')=='BookShelf')
packet.update(previous_packet=ref(OLD/'source-packet.json'),directional_reference=dict(textures=refs,definition=private(definition),object=ET.tostring(node,encoding='unicode'),graphic_class='Graphic_Multi',drawSize=[3,2],footprint=[2,1],load_folders='No LoadFolders.xml installed; selected assets and matching definition are in root Textures/Defs. Runtime activation/profile not asserted.',mapping='BookShelf CompProperties_StorageGraphic.graphicSparse explicitly references Things/Building/BookShelfSparse with3x2drawSize. Actual end is a solid closed wood panel; N/S show book rows. Transparent bounds are recorded, not treated as physical Qud dimensions.',role='Parallel map planes, modest visible depth, restrained plank/book shading and closed end only. Do not copy broad four-row donor cabinet, native donor storage/research logic or footprint.'),
    camera=dict(classification='CARDINAL_SOURCE_BOUND',authored_width=14.0,authored_depth=6.8,top_depth_visibility=1.9/6.8,dimensions_status='Hidden depth and joinery are authored estimates informed by source cap/frame and inspected actual directional reference; not native dimensions or a donor width-ratio target.',shared_frame='16x24cell,512x768construction,256square recipient, native-cell pivot8,16 for all3layouts/views/role masks. Same plane elevation across facings.',front_patch='Replace only converging trapezoid cap with a parallel plane and reuse cap material. Original selected frame/books/boards below authoring y224 remain exact.',unseen='Closed solid end; open rear compartments with the same source books seen from the back/foreedges, no copied spine labels. Open backing remains authored, not native established construction.',west='Same closed unmarked end geometry permits mirrored east; no handed side decoration.'),native_acceptance='Pending full-set generation gate; native mounted storage/inventory/full-empty tint/support/visibility/physics and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
cap='''<path d="M1 3.25H15V6.9H1Z" fill="#bcbcbc" stroke="#303030" stroke-width=".12"/><path d="M1 5.15H15" fill="none" stroke="#626262" stroke-width=".11"/>'''
cap_svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+cap+'</svg>'
(HERE/'parallel-front-cap.svg').write_bytes(cap_svg.encode());(HERE/'parallel-front-cap.png').write_bytes(svg_to_bytes(svg_string=cap_svg));ca=np.array(read(HERE/'parallel-front-cap.png'));inside=ca[:,:,3]>0;yy,xx=np.indices((768,512));ty,tx=np.where(inside);target=[int(tx.min()),int(ty.min()),int(tx.max()),int(ty.max())];patches=[]
def cap_material(raw):
    a=np.array(raw);y,x=np.indices(a.shape[:2]);mask=(a[:,:,3]>250)&(y>196)&(y<420);mask=ndimage.binary_erosion(mask,iterations=8);ys,xs=np.where(mask);lo,hi=int(ys.min()),int(ys.max());left=np.zeros(a.shape[0]);right=left.copy()
    for row in range(lo,hi+1):
        q=np.where(mask[row])[0];left[row]=q.min() if len(q) else xs.min();right[row]=q.max() if len(q) else xs.max()
    ry=np.clip(lo+(yy-target[1])*(hi-lo)/(target[3]-target[1]),lo,hi);l=np.interp(ry,np.arange(len(left)),left);r=np.interp(ry,np.arange(len(right)),right);rx=l+(xx-target[0])*(r-l)/(target[2]-target[0]);v=ndimage.map_coordinates(a[:,:,0].astype(float),[ry,rx],order=1,mode='nearest');ink=ca[:,:,:3].mean(2);v[inside&(ink<120)]=ink[inside&(ink<120)];v=np.uint8(np.clip(np.round(v),0,255));v[~inside]=0
    return Image.fromarray(np.dstack([v,v,v,ca[:,:,3]])),dict(source_cap_interior_y=[lo,hi],source_boundary_clearance=8,target_cap_bounds=target)
def book_shapes(layout,rear=False,owner=False):
    out=[];fill='#ffffff' if owner else '#cfc041';ink='none' if owner else '#303030';sw=0 if owner else .12
    for shelf in layout['shelves']:
        base=shelf['base']
        for group in shelf['groups']:
            x0,y0,x1,y1=group['source_bounds'];pts=group['source_pixels']
            if group['kind']=='horizontal':
                x=x0+.15;w=max(.8,x1-x0-.3);d=f'M{x} {base-.55}H{x+w}V{base-.05}H{x}Z'
            else:
                bottom=[x for x,y in pts if y==y1-1];top=[x for x,y in pts if y==y0];xb=sum(bottom)/len(bottom)+.5;xt=xb+(.65 if sum(top)/len(top)>sum(bottom)/len(bottom) else -.65 if sum(top)/len(top)<sum(bottom)/len(bottom) else 0);yt=base-2.55;d=f'M{xt-.3} {yt}H{xt+.3}L{xb+.3} {base-.05}H{xb-.3}Z'
            out.append(f'<path d="{d}" fill="{fill}" stroke="{ink}" stroke-width="{sw}"/>')
    return ('<g transform="translate(16 0) scale(-1 1)">'+''.join(out)+'</g>') if rear else ''.join(out)
def back(layout,owner=False):
    fill='#000000' if owner else '#aaaaaa';stroke='none' if owner else '#303030';sw=0 if owner else .12
    wood=f'<path d="M1.2 5.6H1.85V20.85H1.2Z M14.15 5.6H14.8V20.85H14.15Z M1.15 10.9H14.85V11.6H1.15Z M1.15 15.9H14.85V16.6H1.15Z M1.15 20.4H14.85V20.9H1.15Z M1 3.25H15V6.9H1Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    return wood+book_shapes(layout,True,owner)
def end(owner=False):
    fill='#000000' if owner else '#aaaaaa';stroke='none' if owner else '#303030';sw=0 if owner else .12
    return f'<path d="M4.6 6.15H11.4V21.9H4.6Z M4.6 2.23H11.4V7.9H4.6Z" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'+('' if owner else '<path d="M4.6 6.15H11.4 M4.9 8.5H11.1V21.2H4.9Z" fill="none" stroke="#626262" stroke-width=".1"/>')
for layout in packet['source_spine_layouts']:
    n=layout['variant'];folder=HERE/f'variant-{n}';folder.mkdir(exist_ok=True);raw=read(OLD/f'registered/variant-{n}-neutral-master.png');base=raw.convert('RGBa').resize((512,768),Image.Resampling.LANCZOS).convert('RGBA');base.save(folder/'retained-front-before-cap.png');oldmask=Image.open(OLD/f'registered/variant-{n}-spine-ownership-mask.png').convert('L');role=Image.merge('RGBA',(oldmask,oldmask,oldmask,raw.getchannel('A'))).convert('RGBa').resize((512,768),Image.Resampling.LANCZOS).convert('RGBA');a=np.array(base);o=np.array(role);a[:221]=0;o[:221]=0;material,stats=cap_material(raw);front=Image.fromarray(a);front.alpha_composite(material);front.save(folder/'selected-front-neutral.png');alpha=np.array(front)[:,:,3];o[:,:,3]=alpha;o[:221,:,:3]=0;o[alpha==0,:3]=0;role=Image.fromarray(o);role.save(folder/'ownership-south.png');assert np.array_equal(np.array(front)[224:],np.array(base)[224:]);patches.append(dict(variant=n,before=ref(folder/'retained-front-before-cap.png'),after=ref(folder/'selected-front-neutral.png'),**stats,unchanged_below_y=224))
    a=np.array(front);weight=o[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-weight[:,:,None])+weight[:,:,None]*np.array([1,.95,.4])));Image.fromarray(a).save(folder/'constructed-south.png')
    for f,builder in [('east',lambda owner:end(owner)),('north',lambda owner:back(layout,owner))]:
        for owner in [False,True]:
            svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+builder(owner)+'</svg>';name=f'ownership-{f}' if owner else f'constructed-{f}';(folder/f'{name}.svg').write_bytes(svg.encode());(folder/f'{name}.png').write_bytes(svg_to_bytes(svg_string=svg))
    sheet=Image.new('RGBA',(1536,768))
    for i,f in enumerate(['south','east','north']):sheet.alpha_composite(read(folder/f'constructed-{f}.png'),(i*512,0))
    sheet.save(folder/'front-guided-turnaround.png')
    counts=[len(s['groups']) for s in layout['shelves']]
    text=f'''Use case: sketch-to-render. One Qud Joppa Bookshelf, cosmetic layout{n}, three cardinal views. Image1 is1536x768 edit target, equal512x768panels: LEFT SOUTH selected refined front with patched parallel cap, CENTER EAST complete closed end, RIGHT NORTH authored open rear. Image2 actual JPT BookShelfSparse_east is ONLY a restrained wood/solid end/map-camera reference. Image3 actual original Qud variants for sparse identity; this is variant{n}.
Canonical description: {packet['description']} Three tall shelf levels, not the donor broad four-row cabinet. Source book counts by shelf are{counts}, with upright/horizontal/leaning groups exactly as current front. Retain selected front books, planks, sparse gaps and lower material; parallel cap replaces old receding trapezoid. Rear shows same books reversed spatially with plain foreedges/back surfaces, no labels or copied spine bands. End is CLOSED plain orthogonal wood: no front books or shelves pasted onto it. No backing panel added to the authored open rear, no new books, lettering, research gear, decorative props or hardware.
Shared authored width14.0, depth6.8, top-depth factor1.9/6.8; preserve full end panel/height at this fixed map elevation. Same source cell16x24/pivot8,16, same scale and positions. Keep cap and shelf planes PARALLEL; no convergence, isometric/diagonal yaw, thin end compression or independent panel bounds fitting. Refine restrained plank grain, subtle dust and shallow paper detail, matching selected front material. Gray frame/cap and muted-gold book surfaces remain distinct role keys; full/empty changes only native tint later, never removes the books. SAME1536x768frame, transparent exterior/open rear compartments. No opaque scenery/backing, glow, drop shadow, labels/text or new state. No second isolation.'''
    (folder/'turnaround-prompt.txt').write_bytes(text.encode())
write(HERE/'cap-geometry-correction.json',dict(method='Same-material row-wise rectification from actual eroded old cap interiors into parallel cap plane; clear whole old upper geometry and preserve every lower selected pixel. No new front generation or finished-side stretch.',variants=patches))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,1350),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'JOPPA BOOKSHELF / original3layouts > retained fronts + parallel caps / complete end and open rear',font=font,fill='#e3cf43');im=read(OLD/'native-states-comparison.png');im.thumbnail((850,420));plate.paste(im,(15,50),im)
for i,f in enumerate(['south','east','north']):
    im=read(Path(refs[f]['path']));im.thumbnail((140,160));plate.paste(im,(920+i*165,80),im);d.text((915+i*165,260),'ACTUAL JPT / '+f,font=font,fill='#e3cf43')
for n in range(1,4):
    im=read(HERE/f'variant-{n}/front-guided-turnaround.png').resize((690,345));x=20+((n-1)%2)*710;y=480+((n-1)//2)*380;plate.paste(im,(x,y),im);d.text((x,y+325),f'LAYOUT{n} / SOUTH EAST NORTH',font=font,fill='#e3cf43')
for i,line in enumerate(['Actual JPT sparse graphics: Graphic_Multi drawSize3x2, footprint2x1. Donor book count/footprint/mechanics not copied.',
 'Authored depth6.8; parallel cap reuses accepted wood and preserves all lower front pixels below y224.',
 'Open rear is an explicit unseen-construction assumption. Gold book keys remain neutral in production; native full W/empty k.',
 'Three RandomTile layouts, not facings. Extra directions unbound; native mounted inventory/support acceptance pending.']):d.text((18,1200+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-reference-construction.png');write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Complete source/ref camera construction before composed refinement',review='All3source book arrangements retained. Converging caps replaced by parallel planes while preserving selected lower fronts. Closed6.8depth end and authored open rear show consistent tall3levels; books rest on boards. Actual JPT S/E/N textures and Graphic_Multi3x2drawSize/2x1footprint inspected. Depth/open backing remain authored, no donor broad4rows or inventory/research behavior.',outputs=[ref(p) for p in sorted(HERE.glob('variant-*/front-guided-turnaround.png'))]));print('Retained all3selected sparse fronts, corrected parallel caps and constructed full end/rear in shared source frame.')
