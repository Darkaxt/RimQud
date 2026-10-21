"""Source-bound map-plane Blender art for two uncovered dynamic cell-paint aliases."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'blender-v1';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
def mat(name,value):
 m=bpy.data.materials.new(name);m['native_role']='primary';m.use_nodes=True;n=m.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(value,)*3+(1,);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],o.inputs[0]);return m
def mesh(name,verts,faces,col,material):
 me=bpy.data.meshes.new(name);me.from_pydata([(x,24-y,z) for x,y,z in verts],[],faces);me.update();ob=bpy.data.objects.new(name,me);col.objects.link(ob);me.materials.append(material);ob['map_plane']=True;return ob
assert not (OUT/'paint.blend').exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard';s.view_settings.look='None';primary=mat('Neutral paint primary',.67);shade=mat('Neutral primary edge',.30);light=mat('Neutral primary vein',.80)
camdata=bpy.data.cameras.new('Fixed ground camera');camdata.type='ORTHO';camdata.ortho_scale=24;cam=bpy.data.objects.new('Fixed ground camera',camdata);s.collection.objects.link(cam);cam.location=(8,12,30);cam.rotation_euler=(0,0,0);s.camera=cam
cols={}
for name in ['dirt1','legacy-grass1']:c=bpy.data.collections.new(name);s.collection.children.link(c);cols[name]=c
# The single dirt point remains one small irregular earth fleck, never a filled soil tile.
outline=[(7.5+(.49+.025*math.sin(i*2.4))*math.cos(i*math.tau/18),11.5+(.47+.023*math.sin(i*1.7))*math.sin(i*math.tau/18),0) for i in range(18)]
mesh('Single source dirt fleck',[(7.5,11.5,0)]+outline,[(0,i+1,(i+1)%18+1) for i in range(18)],cols['dirt1'],primary)
paths=[[(7.5,14.9),(7.5,12.9),(5.7,10.3),(4.5,9.5)],[(4.5,15.9),(4.6,14.3),(3.1,12.9),(2.5,12.5)],[(9.5,15.8),(9.4,14.1),(11.4,11.4),(12.5,10.5)]]
def curve(p,t):return tuple((1-t)**3*p[0][k]+3*(1-t)**2*t*p[1][k]+3*(1-t)*t*t*p[2][k]+t**3*p[3][k] for k in range(2))
for j,p in enumerate(paths):
 verts=[]
 for i in range(33):
  t=i/32;x,y=curve(p,t);a=curve(p,max(0,t-.001));b=curve(p,min(1,t+.001));dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);width=.77*math.sqrt(max(.0001,1-t))
  verts.extend([(x-dy/length*width/2,y+dx/length*width/2,0),(x+dy/length*width/2,y-dx/length*width/2,0)])
 mesh(f'Legacy sparse blade{j+1}',verts,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(32)],cols['legacy-grass1'],primary)
manual=[]
for name,c in cols.items():
 for ob in s.objects:
  if ob.type=='MESH':ob.hide_render=ob.name not in c.objects
 s.render.filepath=str(OUT/f'{name}-manual.png');bpy.ops.render.render(write_still=True);manual.append(ref(Path(s.render.filepath)))
controls=dict(entry='SCOPE-DIRTY',source=ref(HERE/'painted-tile-index.json'),states=[dict(id=name,objects=[o.name for o in c.objects]) for name,c in cols.items()],native_aliases={'dirt1':'Tiles/tile-dirt1.png','legacy-grass1':'assets_content_textures_tiles_tile-grass1.png'},grass_paths_source_xy=paths,dirt_fleck_center_source_xy=[7.5,11.5],camera=dict(location=[8,12,30],rotation=[0,0,0],type='ORTHO',scale=24,canvas=[512,768]),registration=dict(native_cell=[16,24],canvas=[512,768],nominal_anchor=[8,16],policy='Full original source-cell frame, one fixed map-plane camera; no bounds normalization.'),authored='Dirt pixel becomes one irregular fine-earth fleck. Legacy source three sparse strokes become three tapered blades, keeping source roots/tips and sparse layout. No species, wind, volume slab or growth state.',native_activation=False)
write(OUT/'model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'paint.blend'));write(OUT/'blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'paint.blend'),manual_renders=manual,native_activation=False))
# Actual restrained refinement, saved separately after the manual checkpoint.
REF=HERE/'blender-v2';REF.mkdir(exist_ok=True)
for ob in list(s.objects):
 if ob.type!='MESH':continue
 if 'blade' in ob.name:
  ob.data.materials.append(shade);ob.data.materials.append(light)
  for face in ob.data.polygons:face.material_index=0
  # Explicit center vein follows source-guided blade centerline; no unrelated strokes.
  j=int(ob.name[-1])-1;p=paths[j];vs=[]
  for i in range(1,31):
   t=i/32;x,y=curve(p,t);a=curve(p,t-.001);b=curve(p,t+.001);dx,dy=b[0]-a[0],b[1]-a[1];norm=math.hypot(dx,dy);w=.055*math.sqrt(1-t);vs.extend([(x-dy/norm*w,y+dx/norm*w,.002),(x+dy/norm*w,y-dx/norm*w,.002)])
  mesh(ob.name+' subtle center shading',vs,[(2*i,2*i+1,2*i+3,2*i+2) for i in range(29)],cols['legacy-grass1'],light)
 else:
  m=primary.copy();m.name='Neutral fine-earth grain';n=m.node_tree.nodes;l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=16;noise.inputs['Detail'].default_value=1;l.new(g.outputs['Position'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.44,)*3+(1,);r.color_ramp.elements[1].color=(.72,)*3+(1,);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],next(v for v in n if v.bl_idname=='ShaderNodeEmission').inputs[0]);ob.data.materials[0]=m
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for old in list(fs.linesets):fs.linesets.remove(old)
ls=fs.linesets.new('Ground paint fine contours');ls.select_crease=False;ls.linestyle.color=(.055,)*3;ls.linestyle.thickness=.8
refined=[]
for name,c in cols.items():
 for ob in s.objects:
  if ob.type=='MESH':ob.hide_render=ob.name not in c.objects
 s.render.filepath=str(REF/f'{name}-refined.png');bpy.ops.render.render(write_still=True);refined.append(ref(Path(s.render.filepath)))
controls.update(resumed_manual_model=ref(OUT/'paint.blend'),states=[dict(id=name,objects=[o.name for o in c.objects]) for name,c in cols.items()],refinement='Subtle native-primary blade center shading and narrow rendered borders; one fleck gains restrained fine-earth procedural grain.',new_imagegen_call=False,selection_reason='Sparse map-plane sources need exact fixed cell placement and primary-only tint. Direct Blender geometry/materials suffice; optional ImageGen is not used.')
write(REF/'model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(REF/'paint.blend'));write(REF/'blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(REF/'paint.blend'),refined_renders=refined,native_activation=False))
