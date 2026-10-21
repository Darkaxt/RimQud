"""Transfer bounded material grain while retaining physical geometry and native colour roles."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math
import numpy as np
from scipy.ndimage import gaussian_filter, binary_erosion
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CON=HERE/'construction-v2';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def save(p,a):Image.fromarray(a).save(p)
assert not (OUT/'model.json').exists()
controls=read(CON/'construction-controls.json'); packet=read(HERE/'source-packet.json');native=read(HERE/'native-state-index.json');raw=Image.open(HERE/'refined-raw.png').convert('RGBA')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
boxes={'linen':[945,180,1100,250],'wood':[110,346,165,353]}; materials={}; selection={}
for name,box in boxes.items():
    a=np.array(raw.crop(box));assert a[:,:,3].min()>=250
    patch=HERE/f'selected-{name}.png';save(patch,a);lum=a[:,:,:3].astype(float).mean(2)
    # Remove generated shading: only quiet high-frequency surface residual is used.
    residual=lum-gaussian_filter(lum,2.0);limit=2.0 if name=='wood' else 3.0;residual=np.clip(residual*.18,-limit,limit)
    materials[name]=residual;selection[name]=dict(box=box,specimen=ref(patch),alpha_min=int(a[:,:,3].min()),amplitude_limit=limit,selection='Unmarked interior; no generated alpha, edge, bolt, lettering, broad illumination or geometry transferred.')
write(HERE/'material-selection.json',dict(actual_source=ref(HERE/'refined-raw.png'),materials=selection,method='Neutral luminance high-pass residual with fixed amplitude limit, through canonical material ownership. No second ImageGen isolation. Fixed physical shape and P/D paint motif remain authoritative.'))
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette']
def col(k):return np.frombuffer(bytes.fromhex(palette[k]),dtype=np.uint8).astype(float)
def tinted(master,weight,fg='w',de='R'):
    lum=master[:,:,:3].astype(float).mean(2)/255; w=weight.astype(float)/255
    rgb=np.uint8(np.clip(np.rint(lum[:,:,None]*((1-w[:,:,None])*col(fg)+w[:,:,None]*col(de))),0,255))
    rgb[master[:,:,3]==0]=0
    return np.dstack([rgb,master[:,:,3]])
def resized(a,size):return np.array(Image.fromarray(a).resize(size,Image.Resampling.LANCZOS))
model=dict(entry='SCN-PAINTING',blueprint='Painting',kind='source-bound two-design furniture turnaround with native palette roles',source=ref(HERE/'source-packet.json'),native_states=ref(HERE/'native-state-index.json'),construction=ref(CON/'construction-controls.json'),
    refinement=ref(HERE/'generation-receipt.json'),first_structural_review=ref(HERE/'first-structural-review.json'),material_selection=ref(HERE/'material-selection.json'),
    registration=dict(native=[16,24],master=[512,768],recipient=[256,256],common_pivot=[256,712],policy='Shared full source-cell frame for both designs/all views; no individual alpha-bounds fitting. Projected support contact varies naturally with shared depth/camera, not independent recentering.'),
    camera=dict(elevation_degrees=14,physical_dimensions=controls['dimensions'],provenance=controls['provenance'],contract=controls['depth_contract']),
    palette=packet['palette'],state_owner='Native RandomTile selects one of two designs. RandomColors sets glyph ColorString independently; tile primary remains declared w, detail one of m/W/r/R/b/B/g/G. Preserve captured/runtime values; no authored animation/palette timer.',
    reverse='Unpainted linen/stretcher/rear brace, authored unseen structure; source front motif never mirrored onto reverse.',
    non_applicable='Equipment/clothing assembly is not applicable to Painting; no inventory outfit or fabricated body fit.',
    native_activation=False,native_acceptance='Pending integrated Stage3 after every pending entry is generated: exact tile choice, runtime palette, visibility and cell mapping. Only current bound fixed map view is a binding candidate; other furniture views are unbound authoring.',states=[])
neutral_plate=Image.new('RGB',(1536,1640),'#142823');mask_plate=Image.new('RGB',(1536,1640),'#142823');dn=ImageDraw.Draw(neutral_plate);dm=ImageDraw.Draw(mask_plate)
dn.text((20,10),'PAINTING / refined material + fixed geometry / SOUTH - EAST - NORTH',font=font,fill='#e3cf43');dm.text((20,10),'PAINTING / white=detail region; gray=primary coverage / fixed canvas',font=font,fill='#e3cf43')
scale_plate=Image.new('RGB',(1400,750),'#142823');ds=ImageDraw.Draw(scale_plate);ds.text((20,15),'PAINTING / actual source and registered art / eight native detail choices',font=font,fill='#e3cf43')
for i,state in enumerate(controls['states']):
    result=dict(id=state['id'],native_tile=state['native_tile'],role='Native RandomTile choice',views={})
    for j,facing in enumerate(['south','east','north']):
        view=state['views'][facing];a=np.array(Image.open(ROOT/view['constructed']['path']).convert('RGBA'));lum=a[:,:,:3].astype(float).mean(2)
        stand=np.array(Image.open(ROOT/view['ownership']['stand']['path']).convert('RGBA'))[:,:,3]>127
        # Derive fixed material ownership from authored geometry. Refinement cannot alter alpha.
        fabric=np.array(Image.open(ROOT/view['ownership']['linen']['path']).convert('RGBA'))[:,:,3]>127
        quiet=(a[:,:,3]==255)&(lum>90)&(lum<243)
        for name,mask in [('wood',stand&~fabric),('linen',fabric)]:
            residual=materials[name]; tiled=np.tile(residual,(math.ceil(768/residual.shape[0]),math.ceil(512/residual.shape[1])))[:768,:512]
            own=binary_erosion(mask&quiet,iterations=2);lum[own]+=tiled[own]
        gray=np.uint8(np.clip(np.rint(lum),0,255));master=np.dstack([gray,gray,gray,a[:,:,3]]);master[a[:,:,3]==0,:3]=0
        detail=np.array(Image.open(ROOT/view['ownership']['detail_paint']['path']).convert('RGBA'))[:,:,3]
        detail=np.minimum(detail,master[:,:,3]); master_weight=np.divide(detail.astype(float)*255,master[:,:,3],out=np.zeros(detail.shape,float),where=master[:,:,3]>0);master_weight=np.uint8(np.rint(master_weight))
        target=OUT/state['id']/facing;target.mkdir(parents=True,exist_ok=True)
        save(target/'master-neutral.png',master);save(target/'master-detail-weight.png',master_weight)
        small=resized(master,(256,256)); small[:,:,:3]=np.uint8(np.rint(small[:,:,:3].astype(float).mean(2)))[:,:,None];small[small[:,:,3]==0,:3]=0
        detail_cov=resized(detail,(256,256));detail_cov=np.minimum(detail_cov,small[:,:,3]);weight=np.uint8(np.rint(np.divide(detail_cov.astype(float)*255,small[:,:,3],out=np.zeros(detail_cov.shape,float),where=small[:,:,3]>0)))
        # Both neutral colour textures share full alpha. Weights select one colour in the shader;
        # they must NOT be alpha-over composited as two independent complete objects.
        for name,data in [('primary-neutral.png',small),('detail-neutral.png',small),('coverage.png',small[:,:,3]),('detail-weight.png',weight),('detail-coverage.png',detail_cov),('native-w-R.png',tinted(small,weight))]:save(target/name,data)
        dual=np.dstack([weight,weight,weight,small[:,:,3]]);save(target/'authored-dualcolor-mask.png',dual)
        refs={name:ref(target/file) for name,file in [('master','master-neutral.png'),('master_detail_weight','master-detail-weight.png'),('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png'),('native_preview','native-w-R.png')]}
        result['views'][facing]=refs
        display=Image.fromarray(master);neutral_plate.paste(display,(j*512,i*768+45),display)
        shown=np.dstack([np.uint8(80+(master_weight.astype(float)/255)*175)]*3+[master[:,:,3]]);shown=Image.fromarray(shown);mask_plate.paste(shown,(j*512,i*768+45),shown)
        for drawer in [dn,dm]:drawer.text((j*512+20,i*768+775),f'{state["id"]} / {facing.upper()}',font=font,fill='#e3cf43')
    # West mirrors the physical east frame; no motif is moved onto a back surface.
    target=OUT/state['id']/'west';target.mkdir(exist_ok=True)
    result['views']['west']={}
    for key,r in result['views']['east'].items():
        pp=ROOT/r['path'];new=target/pp.name;Image.open(pp).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(new);result['views']['west'][key]=ref(new)
    result['west_policy']='Mirror east in common frame, source geometry is bilaterally symmetric; no front motif visible in profile.'
    model['states'].append(result)
    source_a=np.array(Image.open(native['states'][i]['private_mask']['path']).convert('RGBA'))
    front=result['views']['south'];m=np.array(Image.open(ROOT/front['master']['path']).convert('RGBA'));w=np.array(Image.open(ROOT/front['master_detail_weight']['path']).convert('L'))
    for j,key in enumerate(packet['palette']['random_detail']):
        src=tinted(np.dstack([np.ones((24,16,3),np.uint8)*255,source_a[:,:,3]]),source_a[:,:,0],de=key)
        out=tinted(m,w,de=key);xx=25+j*170;yy=75+i*310
        src=Image.fromarray(src).resize((64,96),Image.Resampling.NEAREST);out=Image.fromarray(out).resize((80,120),Image.Resampling.LANCZOS)
        scale_plate.paste(src,(xx,yy),src);scale_plate.paste(out,(xx+70,yy-12),out)
        for k,sz in enumerate([(24,36),(32,48),(48,72)]):
            im=Image.fromarray(tinted(m,w,de=key)).resize(sz,Image.Resampling.LANCZOS);scale_plate.paste(im,(xx+k*48,yy+130),im)
        ds.text((xx,yy+220),f'Design{i+1} / w,{key}',font=font,fill='#e3cf43')
    ds.text((20,690),'Primary tile w fixed; source D colour native-selected. Three smaller previews share source-cell frame.',font=font,fill='#e5e8d8')
neutral_plate.save(OUT/'neutral-turnarounds.png');mask_plate.save(OUT/'ownership-turnarounds.png');scale_plate.save(OUT/'source-and-native-palettes.png')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(timestamp=datetime.now(timezone.utc).isoformat(),actual_material_source=ref(HERE/'refined-raw.png'),construction=ref(CON/'construction-controls.json'),
    alpha='Exact constructed master coverage retained; generated border/alpha/bolts are never imported.',
    colour='Neutral equal-RGB in every texture. Single coverage plus independent detail weight; two neutral textures are shader colour inputs, not independent alpha-over layers. Eight native detail examples, declared primary w from verified TileColor precedence.',
    source_interpretation='Abstract source P/D/negative patterns on continuous linen. Source transparent interior interpreted as dark painted image space rather than physical holes; outside silhouette/gaps remain transparent.',
    patch='Flat strips were corrected to square-section solid beams before ImageGen. Final refinement patch transfers bounded material grain into fixed geometry and excludes generated metal fittings/heavy shading.',
    views='Two actual designs each S/E/N and mirrored W. Common frame and projected depth/contact. Furniture extras unbound until later integration decision; no native rotation or placement logic.'))
print('Registered both native designs with four cardinal authoring views, independent colour weight/coverage, and eight native detail examples.')
