"""Keep one source head, preserve separated upper marks, and restore the dark front fork."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v3'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'monuments.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'monuments.blend'));s=bpy.context.scene;controls=json.loads((OLD/'model-controls.json').read_text());st=controls['states'][-1];root=bpy.data.objects[st['root']];collection=bpy.data.collections[st['collection']];outline_collection=bpy.data.collections['Physical monument outlines'];ob=bpy.data.objects['resheph complete relief'];old_outline=st['profile_x_y_down'];outline=[(7.1,3.1),(8.8,3.1),(10,4.3),(10,5.7),(9.1,6.4)]+old_outline[8:35];count=len(outline);vertices=[(x,y,24-z) for y in [-st['depth']/2,st['depth']/2] for x,z in outline];faces=[tuple(range(count-1,-1,-1)),tuple(range(count,2*count))]+[(k,(k+1)%count,(k+1)%count+count,k+count) for k in range(count)];mesh=bpy.data.meshes.new('One source-connected main head and relief body');mesh.from_pydata(vertices,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();mesh.materials.append(ob.data.materials[0]);ob.data=mesh;st['profile_x_y_down']=outline;primary=bpy.data.materials['Neutral carved monument - native primary'];dark=bpy.data.materials['Source negative incisions - primary']
def attach(piece,physical=True,outline=True):
 for c in list(piece.users_collection):c.objects.unlink(piece)
 collection.objects.link(piece)
 if outline:outline_collection.objects.link(piece)
 piece['physical']=physical;piece['native_role']='primary';piece.parent=root;piece.matrix_parent_inverse=root.matrix_world.inverted();piece.hide_render=False
# A narrow continuous rear rail supports four separated source marks without filling their envelope.
marks=[(7.5,1.5),(9.5,1.5),(10.5,2.5),(11.5,4.5)];rail_points=[(7.5,3.5),*marks,(9.4,5.2)];curve=bpy.data.curves.new('Authored narrow rear support for upper source marks','CURVE');curve.dimensions='3D';curve.bevel_depth=.065;curve.bevel_resolution=3;curve.use_fill_caps=True;sp=curve.splines.new('POLY');sp.points.add(len(rail_points)-1)
for point,(x,y) in zip(sp.points,rail_points):point.co=(x,.6,24-y,1)
rail=bpy.data.objects.new('resheph upper-mark support rail',curve);s.collection.objects.link(rail);curve.materials.append(primary);attach(rail,outline=False)
for i,(x,y) in enumerate(marks):
 bpy.ops.mesh.primitive_cube_add(size=2,location=(x,.6,24-y));piece=bpy.context.object;piece.name=f'resheph source upper mark {i}';piece.scale=(.35,.24,.35);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);piece.data.materials.append(primary);attach(piece);mod=piece.modifiers.new('Mark edge','BEVEL');mod.width=.05;mod.segments=3
# Clip the source's open central negative strokes to the front solid profile as dark carving.
image=bpy.data.images.load(st['source_mask']['path'],check_existing=False);width,height=image.size;pixels=list(image.pixels);cells=[(x,y) for y in range(7,14) for x in range(4,11) if pixels[((height-1-y)*width+x)*4+3]<.5];bpy.data.images.remove(image)
def clip(poly,axis,bound,greater):
 out=[]
 for a,b in zip(poly,poly[1:]+poly[:1]):
  ia=a[axis]>=bound-1e-9 if greater else a[axis]<=bound+1e-9;ib=b[axis]>=bound-1e-9 if greater else b[axis]<=bound+1e-9
  if ia:out.append(a)
  if ia!=ib:
   t=(bound-a[axis])/(b[axis]-a[axis]);out.append(tuple(a[k]+t*(b[k]-a[k]) for k in range(2)))
 return out
points=[Vector((x,y,0)) for x,y in outline];triangles=tessellate_polygon([points]);verts=[];polys=[]
for x,y in cells:
 for tri in triangles:
  poly=[(points[k].x,points[k].y) for k in tri]
  for axis,bound,greater in [(0,x,True),(0,x+1,False),(1,y,True),(1,y+1,False)]:
   if poly:poly=clip(poly,axis,bound,greater)
  if len(poly)<3 or abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(poly,poly[1:]+poly[:1])))<2e-6:continue
  start=len(verts);verts.extend((a,-st['depth']/2-.024,24-b) for a,b in poly);polys.append(tuple(range(start,start+len(poly))))
mesh=bpy.data.meshes.new('Source central fork front-carving surface');mesh.from_pydata(verts,[],polys);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(mesh);bm.free();piece=bpy.data.objects.new('resheph source central fork incisions',mesh);s.collection.objects.link(piece);mesh.materials.append(dark);attach(piece,physical=False,outline=False)
selected=set(collection.objects)
for other in controls['states']:bpy.data.collections[other['collection']].hide_render=False
for piece in s.objects:
 if piece.type in ['MESH','CURVE']:piece.hide_render=piece not in selected
hold=bpy.data.materials.new('Primary ownership holdout');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);slots=[(piece,i,slot.material) for piece in selected if piece.type in ['MESH','CURVE'] for i,slot in enumerate(piece.material_slots) if slot.material and slot.material.get('native_role')=='primary'];s.camera=bpy.data.objects['Monument diagnostic'];s.render.filepath=str(HERE/'resheph-refined-3d.png');bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['Shared cardinal map camera']
for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:
 root.rotation_euler.z=angle;s.render.filepath=str(HERE/f'resheph-{facing}-neutral.png');bpy.ops.render.render(write_still=True)
 for piece,i,material in slots:piece.data.materials[i]=hold
 s.render.use_freestyle=False;s.render.filepath=str(HERE/f'resheph-{facing}-detail.png');bpy.ops.render.render(write_still=True)
 for piece,i,material in slots:piece.data.materials[i]=material
 s.render.use_freestyle=True
root.rotation_euler.z=0;reused=[]
for other in controls['states'][:-1]:
 for suffix in ['refined-3d.png']+[f'{f}-{kind}.png' for f in ['south','east','north'] for kind in ['neutral','detail']]:
  name=other['id']+'-'+suffix;(HERE/name).write_bytes((OLD/name).read_bytes());reused.append(dict(original=ref(OLD/name),reused=ref(HERE/name)))
controls.update(resumed_from=ref(OLD/'monuments.blend'),resheph_correction=dict(previous_profile=old_outline,main_head='One source-connected head; isolated upper marks no longer merged into an extra head-like lobe.',upper_marks=marks,upper_mark_support='Authored thin rear rail connects marks to the same head; rail is a structural estimate, not a claim that Qud defines a halo/crown.',central_front_carving_cells=cells,unchanged_alternatives='Other five exact v3 model/renders retained; no new render claimed for them.'));write('model-controls.json',controls);write('unchanged-render-reuse.json',dict(artifacts=reused,new_renders=7));bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'monuments.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'monuments.blend'),controls=ref(HERE/'model-controls.json'),actual_refined_renders=7,reused_unchanged_renders=35,new_imagegen_call=False,native_activation=False))
