"""Editable complete hollow reed bowl, bound mouth and tall carrying loop."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'basket.blend').exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def material(name,values):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.75,.35);r=n.new('ShaderNodeValToRGB');r.color_ramp.interpolation='LINEAR'
 for e,value,pos in [(r.color_ramp.elements[0],values[0],0),(r.color_ramp.elements[1],values[2],.72)]:e.position=pos;e.color=(value,)*3+(1,)
 e=r.color_ramp.elements.new(.25);e.color=(values[1],)*3+(1,);em=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],r.inputs[0]);l.new(r.outputs[0],em.inputs[0]);l.new(em.outputs[0],o.inputs[0]);return m
reed=material('Neutral reed foundation',(.18,.42,.68));inside=material('Dark reed bowl interior',(.035,.09,.18));binding=material('Bound reed rim and carrying loop',(.23,.53,.78))
outer=[(0,19.0),(.72,19.0),(.84,18.5),(.95,17.5),(1.0,15.1),(1.0,13.8)];inner=[(.93,13.8),(.93,15.1),(.88,17.2),(.77,18.1),(.65,18.6),(0,18.6)];profile=outer+inner;sides=96;verts=[];faces=[]
for q,y in profile:
 for k in range(sides):t=k*2*math.pi/sides;verts.append((8+5.4*q*math.cos(t),4.1*q*math.sin(t),24-y))
for j in range(len(profile)-1):
 for k in range(sides):faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
mesh=bpy.data.meshes.new('Complete hollow closed-weave bowl');mesh.from_pydata(verts,[],faces);mesh.update();mesh.materials.append(reed);mesh.materials.append(inside)
for p in mesh.polygons:p.use_smooth=True;p.material_index=1 if p.index//sides>=len(outer) else 0
bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();body=bpy.data.objects.new('Complete woven bowl foundation',mesh);s.collection.objects.link(body);sub=body.modifiers.new('Round vessel floor and walls','SUBSURF');sub.levels=2;sub.render_levels=2
contours=bpy.data.collections.new('Basket outline');s.collection.children.link(contours);contours.objects.link(body)
def curve(name,points,radius,cyclic=False,bezier=True):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=24;d.bevel_depth=radius;d.bevel_resolution=4;d.use_fill_caps=True;sp=d.splines.new('BEZIER' if bezier else 'POLY')
 if bezier:
  sp.bezier_points.add(len(points)-1)
  for p,co in zip(sp.bezier_points,points):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
 else:
  sp.points.add(len(points)-1)
  for p,co in zip(sp.points,points):p.co=(*co,1)
 sp.use_cyclic_u=cyclic;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);d.materials.append(binding);contours.objects.link(ob);return ob
rim=curve('Continuous bound reed mouth',[(8+5.35*math.cos(k*2*math.pi/96),4.06*math.sin(k*2*math.pi/96),10.2) for k in range(96)],.24,True,False)
handle_points=[(-5.15,14.5),(-5.5,11.5),(-4.9,8.2),(-3,6.2),(0,5.65),(3,6.2),(4.9,8.2),(5.5,11.5),(5.15,14.5)]
handle=curve('Tall continuous carrying loop',[(8+x,0,24-y) for x,y in handle_points],.24)
for sign in [-1,1]:
 for y in [13.9,14.25]:curve(f'Handle foot binding {sign} {y}',[(8+sign*5.26+.29*math.cos(k*2*math.pi/32),.29*math.sin(k*2*math.pi/32),24-y) for k in range(32)],.07,True,False)
def camera(name,loc,target,scale):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Fixed source map camera',(8,-42,18),(8,0,12),24);diag=camera('Reed vessel construction diagnostic',(29,-34,29),(8,0,12),25)
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'manual-neutral-master.png');bpy.ops.render.render(write_still=True)
write('model-controls.json',dict(source=ref(HERE/'source-packet.json'),body_radii=[5.4,4.1],outer_profile_scale_y=outer,inner_profile_scale_y=inner,handle_points_x_y_down=handle_points,handle_radius=.24,body_wall='Complete closed-weave hollow wall with separate inner shading, no lid or baked inventory.',handle_join='Loop ends continue into sidewall; two bound reed loops at each foot visibly tie them to the rim/wall.',camera=dict(type='ORTHO',location=[8,-42,18],target=[8,0,12],ortho_scale=24,canvas=[512,768]),authored_dimensions='Hidden depth/wall thickness/strand count are authored; common frame and source low-bowl/tall-loop proportions retained.',new_imagegen_call=False,native_activation=False))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'basket.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'basket.blend'),controls=ref(HERE/'model-controls.json'),scope='Complete manual bowl, bound rim and carry loop before warp/weft finishing',native_activation=False))
