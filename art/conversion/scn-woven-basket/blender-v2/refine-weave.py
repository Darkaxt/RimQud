"""Resume the complete basket; fit actual interlaced reed ribbons to its wall."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'basket.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'basket.blend'));s=bpy.context.scene;body=bpy.data.objects['Complete woven bowl foundation'];bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();evaluated=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);tree=BVHTree.FromPolygons([v.co for v in evaluated.vertices],[tuple(p.vertices) for p in evaluated.polygons])
reed=bpy.data.materials['Neutral reed foundation'];warp_mat=reed.copy();warp_mat.name='Neutral raised warp reeds';weft_mat=reed.copy();weft_mat.name='Neutral crossing weft reeds'
for mat,values in [(warp_mat,(.23,.49,.77)),(weft_mat,(.18,.41,.68))]:
 ramp=next(n for n in mat.node_tree.nodes if n.type=='VALTORGB')
 for e,v in zip(sorted(ramp.color_ramp.elements,key=lambda e:e.position),values):e.color=(v,)*3+(1,)
def point(phi,y,offset):
 direction=Vector((math.cos(phi),math.sin(phi),0));origin=Vector((8,0,24-y))+direction*15;hit,normal,_,_=tree.ray_cast(origin,-direction);assert hit is not None,(phi,y);return hit+normal*offset
def ribbon(name,vertices,faces,material):
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(vertices,[],faces);mesh.update();mesh.materials.append(material)
 for p in mesh.polygons:p.use_smooth=True
 ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob);solid=ob.modifiers.new('Real reed ribbon thickness','SOLIDIFY');solid.thickness=.06;solid.offset=0;solid.use_even_offset=True;return ob
courses=[]
for row in range(6):
 y=14.4+.8*row;vertices=[];faces=[]
 for k in range(128):
  phi=k*2*math.pi/128;offset=.04+.045*math.cos(8*phi+row*math.pi)
  for edge in [-.25,.25]:vertices.append(point(phi,y+edge,offset))
 for k in range(128):faces.append((2*k,2*((k+1)%128),2*((k+1)%128)+1,2*k+1))
 courses.append(ribbon(f'Complete weft course {row}',vertices,faces,weft_mat).name)
warps=[]
for column in range(16):
 phi=column*2*math.pi/16;vertices=[];faces=[]
 for k in range(65):
  y=13.9+(18.65-13.9)*k/64;offset=.04-.045*math.cos(column*math.pi+(y-14.4)*math.pi/.8)
  for edge in [-.055,.055]:vertices.append(point(phi+edge,y,offset))
 for k in range(64):faces.append((2*k,2*k+2,2*k+3,2*k+1))
 warps.append(ribbon(f'Bound vertical warp {column}',vertices,faces,warp_mat).name)
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Reed vessel silhouette, bound rim and handle');ls.select_by_collection=True;ls.collection=bpy.data.collections['Basket outline'];ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.018,.018,.018);ls.linestyle.thickness=1.8;ls.linestyle.caps='ROUND'
root=bpy.data.objects.new('Basket shared facing pivot',None);s.collection.objects.link(root);root.location=(8,0,0);bpy.context.view_layer.update()
for ob in list(s.objects):
 if ob.type in ['MESH','CURVE']:ob.parent=root;ob.matrix_parent_inverse=root.matrix_world.inverted()
s.camera=bpy.data.objects['Reed vessel construction diagnostic'];s.render.filepath=str(HERE/'stage-03-refined-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera']
for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:
 root.rotation_euler.z=angle;s.render.filepath=str(HERE/f'{facing}-neutral-master.png');bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0;bpy.context.view_layer.update()
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'basket.blend'),weave=dict(warp_count=16,weft_courses=6,actual_wall_fit='Ribbon samples ray-cast onto evaluated outer bowl wall, with alternating small over/under displacement and real thickness.',course_centers_y=[14.4+.8*j for j in range(6)],strand_thickness=.06,openings='Close-woven foundation remains continuous; no inventory contents or unrelated floating marks.'),facings=dict(south=0,east=-90,north=180),source_selection='Direct Blender neutral reeds, bound loop/rim and contours preserve shape and weave. No ImageGen or isolation call.',production_view='south only; east/north retained as actual common-frame authoring views, not added native direction states.',new_imagegen_call=False,native_activation=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'basket.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'basket.blend'),controls=ref(HERE/'model-controls.json'),actual_views=['south','east','north'],new_imagegen_call=False,native_activation=False))
