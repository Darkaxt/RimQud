"""Register256native wall variants plus16recipient cardinal states in fixed frames."""
from pathlib import Path
import io,json,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageChops,ImageFilter
import resvg_py
from importlib.util import spec_from_file_location,module_from_spec
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True);STATES=OUT/'states';STATES.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite recorded registration'
spec=spec_from_file_location('rusted_geometry',HERE/'construct-geometry.py');mod=module_from_spec(spec);spec.loader.exec_module(mod)
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
index=json.loads((HERE/'native-state-index.json').read_text());palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
g=ImageOps.grayscale(Image.open(HERE/'refined-proposal.png')).resize((512,512),Image.Resampling.LANCZOS)
# Match opposite borders without inventing new material or re-generating.
for axis in ['x','y']:
 old=g.copy()
 for i in range(12):
  t=(1-i/11)**2
  for n in range(512):
   a=(i,n) if axis=='x' else (n,i);b=(511-i,n) if axis=='x' else (n,511-i);x,y=old.getpixel(a),old.getpixel(b);m=(x+y)/2
   g.putpixel(a,round(x*(1-t)+m*t));g.putpixel(b,round(y*(1-t)+m*t))
g.save(OUT/'patched-seamless-material.png');material=g.resize((512,768),Image.Resampling.LANCZOS)
base=material.point(lambda v:max(145,min(235,round(195+(v-145)*.4))))
detail_lum=material.point(lambda v:max(200,min(245,round(230+(v-145)*.2))))
rows=[];previews={};primary_atlas=Image.new('RGBA',(1024,1024));detail_atlas=Image.new('RGBA',(1024,1024))
cardinal={''.join(('1' if mask&bit else '0') if bit else '0' for bit in [1,0,2,0,4,0,8,0]):mask for mask in range(16)}
for row in index['all_native_states']:
 suffix=row['native_suffix'];raw=Image.open(row['private_mask']['path']).convert('RGBA');p,d,node_count=mod.geometry(raw,suffix)
 masks=[Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA').getchannel('A') for s in [p,d]]
 pm,dm=masks;coverage=ImageChops.lighter(pm,dm);outline=ImageChops.subtract(coverage,coverage.filter(ImageFilter.MinFilter(5)))
 lum=base.copy();lum.paste(Image.new('L',lum.size,65),(0,0),outline)
 # Primary owns complete physical coverage; cyan detail replaces it on the
 # source-defined frame regions using its own neutral layer and alpha.
 primary=Image.merge('RGBA',(lum,lum,lum,coverage))
 dl=detail_lum.copy();dl.paste(Image.new('L',dl.size,120),(0,0),outline)
 detail=Image.merge('RGBA',(dl,dl,dl,dm))
 primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS);alpha=coverage.resize((256,256),Image.Resampling.LANCZOS)
 for name,im in [('primary',primary),('detail',detail),('coverage',alpha)]:im.save(STATES/f'{suffix}-{name}.png')
 c=bytes.fromhex(palette['r']);v=primary.getchannel('R');colored=Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],primary.getchannel('A')))
 c=bytes.fromhex(palette['C']);v=detail.getchannel('R');tinted=Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],detail.getchannel('A')));colored.alpha_composite(tinted);previews[suffix]=colored
 rec=dict(native_suffix=suffix,native_tile=row['tile'],welded_mesh_nodes=node_count,primary=asset(STATES/f'{suffix}-primary.png'),detail=asset(STATES/f'{suffix}-detail.png'),coverage=asset(STATES/f'{suffix}-coverage.png'))
 if suffix in cardinal:
  mask=cardinal[suffix];xy=(mask%4*256,(3-mask//4)*256);primary_atlas.paste(primary,xy);detail_atlas.paste(detail,xy);rec.update(cardinal_mask=mask,atlas_rect=[*xy,256,256])
 rows.append(rec)
primary_atlas.save(OUT/'primary-cardinal-atlas.png');detail_atlas.save(OUT/'detail-cardinal-atlas.png')
model=dict(entry='SCN-RUSTEDMETALWALL',kind='native_eight_neighbor_wall_variants',blueprint='RustedMetalWall',
 source=asset(HERE/'source-packet-v2.json'),native_state_evidence=asset(HERE/'native-state-index.json'),
 states=rows,cardinal_atlas=dict(primary=asset(OUT/'primary-cardinal-atlas.png'),detail=asset(OUT/'detail-cardinal-atlas.png'),size=[1024,1024],tile=[256,256],bits=dict(N=1,E=2,S=4,W=8),row='3-floor(mask/4)',sampling='Clamp state UVs to texel centers or point-sample; never blend unrelated packed states.'),
 native_state_order=['N','NE','E','SE','S','SW','W','NW'],native_join_group='MetalWalls, as selected by native PaintWall; do not infer unrelated joins',
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],source_anchor=[8,16],rule='Every source shape uses one full-cell coordinate transform. No per-facing/state bounding-box normalization, added border cap or invented wall extrusion.'),
 palette=dict(primary='actual source foreground r',detail='actual source detail C',preview_primary=palette['r'],preview_detail=palette['C']),
 material=asset(OUT/'patched-seamless-material.png'),
 interpretation='Source frame/base contours and checker node positions remain fixed. Fine welded diagonal mesh between checker nodes is authored geometry; it is not claimed to be literal native alpha or independent proof of physical holes.',
 native_behavior='Visibility, occluding/solid, damage, graffiti, animated exceptions and actual state selection remain native. Source-known state art is prepared; native replacement dispatch still awaits the final integrated acceptance gate.',
 native_acceptance='Pending every-conversion-generated gate')
decisions=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(HERE/'construct-geometry.py'),asset(Path(__file__).resolve())],
 source_shapes='All256installed painted keys extracted privately. Public geometry reconstructs source frame/base and mesh nodes, then adds explicit welded mesh struts; no generic donor wall silhouette replaces them.',
 correction='Rejected literal checker enlargement retained. Mesh terminal nodes with one diagonal neighbor are included; no orphan square is accepted as a separate object.',
 material_patch='One grayscale512square material, twelve-texel opposite-edge bands matched, then common512x768sampling. Grain is restrained to preserve palette readability; geometry never comes from material alpha.',
 layers='Source cyan frame/edge cells remain separately detail-owned. Red rust-metal primary underlies complete constructed coverage. Edge bevel derives from constructed union, not cell boundary, so no extra seam/cap is introduced per tile.',
 source_limit='Fine mesh is an authored interpretation of tiny checker marks. Native alpha cannot establish seeing through an occluding wall; mechanics stay native.',
 views='All256native shapes and16cardinal atlas layouts. No creature turnarounds or clothing are applicable.')
for name,value in [('model.json',model),('registration-decisions.json',decisions)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
plate=Image.new('RGB',(1280,1020),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,12),'RUSTED METAL /16cardinal layouts from256native variants / source r + C',font=font,fill='#e3cf43')
for suffix,mask in cardinal.items():
 x=mask%4*320+90;y=mask//4*235+50;im=previews[suffix].resize((128,192),Image.Resampling.LANCZOS);plate.paste(im,(x,y),im);draw.text((mask%4*320+20,y+194),f'{mask:02} / {suffix}',font=font,fill='#e5e8d8')
plate.save(OUT/'states-comparison.png')
all_plate=Image.new('RGB',(1024,1600),'#142823');draw=ImageDraw.Draw(all_plate);draw.text((16,12),'ALL256NATIVE STATES / N NE E SE S SW W NW',font=font,fill='#e3cf43')
for n,(suffix,im) in enumerate(sorted(previews.items())):
 thumb=im.resize((64,96),Image.Resampling.LANCZOS);all_plate.paste(thumb,(n%16*64,40+n//16*96),thumb)
all_plate.save(OUT/'all-native-states-comparison.png')
cells={(x,1) for x in range(1,12)}|{(x,8) for x in range(1,12) if x not in [5,6]}|{(1,y) for y in range(1,9)}|{(11,y) for y in range(1,9)}|{(6,y) for y in range(1,6)}|{(x,5) for x in range(3,10)}
dirs=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
for tile_size,name in [((64,96),'connections-comparison.png'),((16,24),'native-scale-comparison.png')]:
 w,h=tile_size;field=Image.new('RGBA',(13*w,10*h),'#'+palette['k'])
 for x,y in cells:
  suffix=''.join('1' if (x+dx,y+dy) in cells else '0' for dx,dy in dirs);im=previews[suffix].resize(tile_size,Image.Resampling.LANCZOS);field.alpha_composite(im,(x*w,y*h))
 plate=Image.new('RGB',(max(1152,field.width),field.height+100),'#142823');draw=ImageDraw.Draw(plate);draw.text((16,16),'RUSTED METAL AUTHORING / actual8neighbor states / same grid, material and anchors',font=font,fill='#e3cf43');plate.paste(field.convert('RGB'),((plate.width-field.width)//2,65));plate.save(OUT/name)
print('Saved256source-constrained painted variants,16cardinal atlas states and connected authoring plates. No native tests.')
