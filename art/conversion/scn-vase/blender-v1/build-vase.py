"""Complete editable hollow pottery with two actual neck-to-shoulder handles."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'vase.blend').exists()
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def material(name,values):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.75,.35);r=n.new('ShaderNodeValToRGB');r.color_ramp.interpolation='CONSTANT'
 for e,value,pos in [(r.color_ramp.elements[0],values[0],0),(r.color_ramp.elements[1],values[2],.72)]:e.position=pos;e.color=(value,)*3+(1,)
 e=r.color_ramp.elements.new(.25);e.color=(values[1],)*3+(1,);em=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],r.inputs[0]);l.new(r.outputs[0],em.inputs[0]);l.new(em.outputs[0],o.inputs[0]);return m
clay=material('Neutral canyon pottery',(.28,.58,.86));slip=clay.copy();slip.name='Decorative slip - source detail ownership'
outer=[(0,20),(3.1,20),(4.2,19.5),(4.8,18.5),(4.9,17.1),(4.9,16.9),(4.9,16.1),(4.9,15.9),(4.9,15.1),(4.9,14.9),(4.9,14.1),(4.9,13.9),(4.5,13),(3.6,12),(2.4,11.2),(1.8,10.5),(1.8,6.2),(2.7,5.9),(2.7,5.3),(2.4,5.1)]
inner=[(2.15,5.3),(2.35,5.65),(1.54,6.25),(1.55,10.4),(2.15,11.05),(3.35,11.85),(4.25,12.9),(4.6,14),(4.6,17),(4.5,18.3),(3.9,19.2),(3,19.7),(0,19.7)]
profile=outer+inner;sides=96;verts=[];faces=[]
for r,y in profile:
 for k in range(sides):t=k*2*math.pi/sides;verts.append((8+r*math.cos(t),r*math.sin(t),24-y))
for j in range(len(profile)-1):
 for k in range(sides):faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
mesh=bpy.data.meshes.new('Full hollow canyon pottery wall');mesh.from_pydata(verts,[],faces);mesh.update();mesh.materials.append(clay);mesh.materials.append(slip)
for p in mesh.polygons:
 p.use_smooth=True;j=p.index//sides;y=(profile[j][1]+profile[j+1][1])/2;p.material_index=1 if j<len(outer)-1 and (14.1<=y<=14.9 or 16.1<=y<=16.9) else 0
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
body=bpy.data.objects.new('Complete hollow vase',mesh);s.collection.objects.link(body);sub=body.modifiers.new('Round kiln-fired pottery profile','SUBSURF');sub.levels=2;sub.render_levels=2
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();surface=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);bvh=BVHTree.FromPolygons([v.co for v in surface.vertices],[tuple(p.vertices) for p in surface.polygons])
handle_defs=[]
for sign,label in [(1,'right'),(-1,'left')]:
 points=[(1.8,6.9),(3.9,7.05),(5.6,8.5),(5.6,10.0),(4.8,11.6),(3.9,12.6)];world=[Vector((8+sign*x,0,24-y)) for x,y in points];seats=[]
 for k in [0,len(world)-1]:
  direction=Vector((sign,0,0));inside=bvh.ray_cast(Vector((8,0,world[k].z)),direction)[0];outside=bvh.ray_cast(inside+direction*.0001,direction)[0];assert inside is not None and outside is not None;world[k]=(inside+outside)/2;seats.append(dict(endpoint=k,inner_wall=list(inside),outer_wall=list(outside),center=list(world[k])))
 data=bpy.data.curves.new(f'Editable {label} pottery handle','CURVE');data.dimensions='3D';data.resolution_u=20;data.bevel_depth=.30;data.bevel_resolution=4;data.use_fill_caps=True;sp=data.splines.new('BEZIER');sp.bezier_points.add(len(world)-1)
 for k,(p,co) in enumerate(zip(sp.bezier_points,world)):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO';p.radius=1.25 if k in [0,len(world)-1] else 1
 source=bpy.data.objects.new(data.name,data);s.collection.objects.link(source);data.materials.append(clay);source.hide_render=True;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();hm=bpy.data.meshes.new_from_object(source.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(hm);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(hm);bm.free();operand=bpy.data.objects.new(f'{label} joined handle operand',hm);s.collection.objects.link(operand);operand.hide_render=True
 union=body.modifiers.new(f'Actual {label} handle to pottery union','BOOLEAN');union.operation='UNION';union.solver='EXACT';union.object=operand;union.material_mode='INDEX';handle_defs.append(dict(side=label,points=[list(p) for p in world],radius=.30,wall_seating=seats))
bevel=body.modifiers.new('Small fused pottery root edge','BEVEL');bevel.width=.055;bevel.segments=3;bevel.limit_method='ANGLE';bevel.angle_limit=.6
def camera(name,loc,target,scale):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Fixed source map camera',(8,-42,18),(8,0,12),24);diag=camera('Hollow pottery construction diagnostic',(29,-34,29),(8,0,12),25)
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'manual-neutral-master.png');bpy.ops.render.render(write_still=True)
write('model-controls.json',dict(source=ref(HERE/'source-packet.json'),outer_profile_radius_y=outer,inner_profile_radius_y=inner,handles=handle_defs,slip_bands_y=[[14.1,14.9],[16.1,16.9]],camera=dict(type='ORTHO',location=[8,-42,18],target=[8,0,12],ortho_scale=24,canvas=[512,768]),authored_depth='Radially lathed hidden bowl/neck depth and wall thickness are authored; source controls silhouette and decorative rows.',new_imagegen_call=False,native_activation=False))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'vase.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'vase.blend'),controls=ref(HERE/'model-controls.json'),scope='Complete manual shape before separate slip/material finishing',native_activation=False))
