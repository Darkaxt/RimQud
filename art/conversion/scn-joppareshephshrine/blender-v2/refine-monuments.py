"""Resume complete source-guided monuments; add edges, source-role inlays and carved marks."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'monuments.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'monuments.blend'));s=bpy.context.scene;controls=json.loads((OLD/'model-controls.json').read_text());physical=bpy.data.collections.new('Physical monument outlines');s.collection.children.link(physical)
for ob in list(s.objects):
 if ob.type=='MESH' and ob.get('physical'):
  mod=ob.modifiers.new('Small carved stone edge','BEVEL');mod.width=.10;mod.segments=3;mod.limit_method='ANGLE';physical.objects.link(ob)
def flat(name,value,role):
 m=bpy.data.materials.new(name);m['native_role']=role;m.use_nodes=True;n=m.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(value,)*3+(1,);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],o.inputs[0]);return m
dark=flat('Source negative incisions - primary',.045,'primary');accent=flat('Source secondary face regions - detail',.52,'detail');primary_material=bpy.data.materials['Neutral carved monument - native primary'];detail_material=bpy.data.materials['Neutral secondary stone/slip region - native detail']
def clip(poly,axis,bound,greater):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=a[axis]>=bound-1e-9 if greater else a[axis]<=bound+1e-9;ib=b[axis]>=bound-1e-9 if greater else b[axis]<=bound+1e-9
  if ia:out.append(a)
  if ia!=ib:
   t=(bound-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(2)))
 return out
def area(poly):return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))/2
def make_marks(st,cells,name,material):
 verts=[];faces=[];points=[Vector((x,y,0)) for x,y in st['profile_x_y_down']];triangles=tessellate_polygon([points])
 for x,y in cells:
  for tri in triangles:
   poly=[(points[k].x,points[k].y) for k in tri]
   for axis,bound,greater in [(0,x,True),(0,x+1,False),(1,y,True),(1,y+1,False)]:
    if poly:poly=clip(poly,axis,bound,greater)
   if len(poly)<3 or area(poly)<1e-6:continue
   start=len(verts);verts.extend((a,-st['depth']/2-.012,24-b) for a,b in poly);faces.append(tuple(range(start,start+len(poly))))
 if not faces:return
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);bpy.data.collections[st['collection']].objects.link(ob);mesh.materials.append(material);ob['physical']=False;ob['native_role']=material['native_role'];ob.parent=bpy.data.objects[st['root']];ob.matrix_parent_inverse=ob.parent.matrix_world.inverted()
# Source pixels are read locally by Blender's image reader; no source image becomes a render dependency.
for st in controls['states']:
 image=bpy.data.images.load(st['source_mask']['path'],check_existing=False);width,height=image.size;pixels=list(image.pixels);opaque=set();details=[]
 for y in range(height):
  for x in range(width):
   k=((height-1-y)*width+x)*4
   if pixels[k+3]>.5:
    opaque.add((x,y))
    if pixels[k]>.5:details.append((x,y))
 # Exterior flood identifies enclosed negative glyph strokes, not open silhouette gaps.
 exterior=set();queue=[(-1,-1)]
 while queue:
  p=queue.pop()
  if p in exterior or p in opaque or not(-1<=p[0]<=width and -1<=p[1]<=height):continue
  exterior.add(p);queue.extend([(p[0]-1,p[1]),(p[0]+1,p[1]),(p[0],p[1]-1),(p[0],p[1]+1)])
 holes=[(x,y) for y in range(height) for x in range(width) if (x,y) not in opaque and (x,y) not in exterior]
 make_marks(st,holes,st['id']+' front source incisions',dark);make_marks(st,details,st['id']+' front source secondary regions',accent);st['source_decoration']=dict(enclosed_negative_cells=len(holes),secondary_cells=len(details),negative_translation='Enclosed source negative strokes become shallow-looking dark front incisions on complete solid stone. Open exterior gaps are not filled with paint.',rear='No cloned front inscription; structural reverse inferred from the same closed model.')
 bpy.data.images.remove(image)
 if st['id']=='catalogue':
  bpy.ops.mesh.primitive_cube_add(size=2,location=(8,0,6.5));ob=bpy.context.object;ob.name='catalogue complete base band';ob.scale=(3.95,1.015,.50);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for col in list(ob.users_collection):col.objects.unlink(ob)
  bpy.data.collections[st['collection']].objects.link(ob);physical.objects.link(ob);ob.data.materials.append(detail_material);ob['physical']=True;ob['native_role']='detail';ob.parent=bpy.data.objects[st['root']];ob.matrix_parent_inverse=ob.parent.matrix_world.inverted();bevel=ob.modifiers.new('Band edge','BEVEL');bevel.width=.035;bevel.segments=2
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Complete carved monument contours');ls.select_by_collection=True;ls.collection=physical;ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.018,)*3;ls.linestyle.thickness=1.7;ls.linestyle.caps='ROUND'
hold=bpy.data.materials.new('Primary ownership holdout');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);primary_slots=[(ob,i,slot.material) for ob in s.objects if ob.type=='MESH' for i,slot in enumerate(ob.material_slots) if slot.material and slot.material.get('native_role')=='primary']
for st in controls['states']:
 for other in controls['states']:bpy.data.collections[other['collection']].hide_render=other!=st
 root=bpy.data.objects[st['root']];s.camera=bpy.data.objects['Monument diagnostic'];s.render.filepath=str(HERE/f'{st["id"]}-refined-3d.png');bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['Shared cardinal map camera']
 for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:
  root.rotation_euler.z=angle;s.render.filepath=str(HERE/f'{st["id"]}-{facing}-neutral.png');bpy.ops.render.render(write_still=True)
  for ob,i,material in primary_slots:ob.data.materials[i]=hold
  s.render.use_freestyle=False;s.render.filepath=str(HERE/f'{st["id"]}-{facing}-detail.png');bpy.ops.render.render(write_still=True)
  for ob,i,material in primary_slots:ob.data.materials[i]=material
  s.render.use_freestyle=True
 root.rotation_euler.z=0
for st in controls['states']:bpy.data.collections[st['collection']].hide_render=st['id']!='resheph'
controls.update(resumed_from=ref(OLD/'monuments.blend'),refinement='Direct Blender bevels, contours and source-positioned surface regions/incisions; no ImageGen call.',actual_facings=dict(south=0,east=-90,north=180),native_activation=False);write('model-controls.json',controls);s.camera=bpy.data.objects['Shared cardinal map camera'];bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'monuments.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'monuments.blend'),controls=ref(HERE/'model-controls.json'),actual_refined_renders=42,new_imagegen_call=False,native_activation=False))
