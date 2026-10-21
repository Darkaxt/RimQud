"""Complete solid terracotta plaque and two actual rear supports."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'sign.blend').exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def material(name,values):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.75,.35);r=n.new('ShaderNodeValToRGB');r.color_ramp.interpolation='LINEAR'
 for e,value,pos in [(r.color_ramp.elements[0],values[0],0),(r.color_ramp.elements[1],values[2],.72)]:e.position=pos;e.color=(value,)*3+(1,)
 e=r.color_ramp.elements.new(.25);e.color=(values[1],)*3+(1,);em=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],r.inputs[0]);l.new(r.outputs[0],em.inputs[0]);l.new(em.outputs[0],o.inputs[0]);return m
clay=material('Neutral terracotta board - detail r',(.28,.56,.84));support=material('Neutral rear supports - tile primary y',(.22,.48,.74));outline=[(1.05,5.1),(14.95,5.1),(14.15,6.05),(14.75,6.9),(14.75,15.1),(14.15,16),(14.95,16.9),(1.05,16.9),(1.85,16),(1.25,15.1),(1.25,6.9),(1.85,6.05)];n=len(outline);vertices=[(x,depth,24-y) for depth in [-.275,.275] for x,y in outline];faces=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)];mesh=bpy.data.meshes.new('One continuous clay plaque');mesh.from_pydata(vertices,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();board=bpy.data.objects.new('Complete terracotta plaque',mesh);s.collection.objects.link(board);mesh.materials.append(clay)
posts=[]
for x in [4,12]:
 bpy.ops.mesh.primitive_cube_add(size=2,location=(x,.48,12.1));ob=bpy.context.object;ob.name=f'Rear upright {x}';ob.scale=(.8,.35,8.9);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(support);posts.append(ob.name)
def camera(name,loc,target,scale):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Fixed source map camera',(8,-42,18),(8,0,12),24);diag=camera('Plaque and rear-support diagnostic',(29,-34,29),(8,0,12),25)
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'manual-neutral-master.png');bpy.ops.render.render(write_still=True)
write('model-controls.json',dict(source=ref(HERE/'source-packet.json'),board_outline_x_y_down=outline,board_depth=[-.275,.275],posts=dict(x_centers=[4,12],y_center=.48,width=1.6,depth=.7,z_range=[3.2,21.0],contact='Uprights overlap rear plaque depth by.145; source above/below positions retained, no artificial gap.'),camera=dict(type='ORTHO',location=[8,-42,18],target=[8,0,12],ortho_scale=24,canvas=[512,768]),authored_depth='Board/support thickness and rear offset are authored; native source only shows above/below post segments.',new_imagegen_call=False,native_activation=False))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'sign.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'sign.blend'),controls=ref(HERE/'model-controls.json'),scope='Manual complete plaque/support geometry before source pictogram/material finish',native_activation=False))
