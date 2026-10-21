"""Source-bound slate door: fixed arch, connected hinge and one rotating leaf."""
import bpy, math, json, hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=False
s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0

def mat(name,value,texture=None):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();o=n.new('ShaderNodeOutputMaterial');e=n.new('ShaderNodeEmission')
    # Values are linear; convert desired display neutral to linear.
    v=((value/255+.055)/1.055)**2.4 if value>10 else value/255/12.92
    e.inputs['Color'].default_value=(v,v,v,1);m.node_tree.links.new(e.outputs[0],o.inputs['Surface'])
    if texture:
        t=n.new('ShaderNodeTexImage');t.image=bpy.data.images.load(str(texture));t.image.pack();m.node_tree.links.new(t.outputs['Color'],e.inputs['Color'])
        tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');m.node_tree.links.new(t.outputs['Alpha'],mix.inputs[0]);m.node_tree.links.new(tr.outputs[0],mix.inputs[1]);m.node_tree.links.new(e.outputs[0],mix.inputs[2]);m.node_tree.links.new(mix.outputs[0],o.inputs['Surface'])
    return m
stone=mat('Neutral slate thickness',145);metal=mat('Hinge metal - native foreground y',100);dark=mat('Dark hinge border',37);light=mat('Hinge ridge',175)
archmat=mat('Retained source refined arch surface',180,OLD/'registered/cleaned-frame.png')
leafmat=mat('Retained source slate hand wear - no new AI',180,HERE/'slate-surface-without-old-hardware.png')

def prism(name,points,depth,frontmat,side=stone,front=-.15):
    verts=[(x,front,24-y) for x,y in points]+[(x,front+depth,24-y) for x,y in points];n=len(points)
    faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob)
    mesh.materials.append(frontmat);mesh.materials.append(side)
    for p in mesh.polygons:p.material_index=0 if p.index==0 else 1
    uv=mesh.uv_layers.new()
    for p in mesh.polygons:
        for li in p.loop_indices:
            co=mesh.vertices[mesh.loops[li].vertex_index].co;uv.data[li].uv=(co.x/16,co.z/24)
    return ob
arch=prism('Fixed arched slate surround',[(1.05,22.9),(1.05,5.05),(4.1,1.05),(11.9,1.05),(14.95,5.05),(14.95,22.9),(14.05,22.9),(14.05,5.45),(11.5,2.5),(4.5,2.5),(1.95,5.45),(1.95,22.9)],.35,archmat,front=-.1)
leaf=prism('Complete slate leaf',[(3.1,21.95),(3.1,7.2),(5.15,5.1),(10.85,5.1),(12.9,7.2),(12.9,21.95)],.58,leafmat)
pivot=bpy.data.objects.new('Hinge pivot - closed 0 open 90 degrees',None);s.collection.objects.link(pivot);pivot.location=(2.9,-.27,0)
bpy.context.view_layer.update() # Resolve the parent transform before preserving child world placement.
def parent(ob):
    world=ob.matrix_world.copy();ob.parent=pivot;ob.matrix_world=world
parent(leaf)
fixed=[];moving=[leaf]
def box(name,center,size,material):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center);ob=bpy.context.object;ob.name=name;ob.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(material);return ob
def cylinder(name,x,y,z,r,h,material):
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=r,depth=h,location=(x,y,z));ob=bpy.context.object;ob.name=name;ob.data.materials.append(material);return ob
for j,y in enumerate([10.65,17.85]):
    z=24-y
    # Fixed strap overlaps the actual jamb and barrel; moving strap overlaps slate.
    fixed.append(box(f'Jamb hinge strap {j}',(2.18,-.34,z),(1.68,.16,.44),dark))
    fixed.append(box(f'Jamb hinge face {j}',(2.18,-.44,z),(1.56,.08,.30),metal))
    fixed.append(cylinder(f'Continuous hinge barrel {j}',2.9,-.27,z,.26,.9,dark))
    fixed.append(cylinder(f'Barrel metal ridge {j}',2.9,-.30,z,.20,.78,metal))
    for dz in [-.26,0,.26]:fixed.append(cylinder(f'Knuckle ring {j} {dz}',2.9,-.30,z+dz,.21,.045,light))
    for material,depth,height in [(dark,.16,.44),(metal,.07,.30)]:
        ob=box(f'Leaf hinge strap {j} {material.name}',(3.55,-.43-depth/2,z),(1.52,depth,height),material);parent(ob);moving.append(ob)
    # Gray rust flakes are a value detail, not an invented orange tint role.
    for dx,dz in [(-.11,.43),(.06,.47),(.17,.39)]:
        ob=box(f'Top hinge rust flake {j} {dx}',(2.9+dx,-.52,z+dz),(.09,.04,.06),metal);fixed.append(ob)

def camera(name,location,target,scale):
    data=bpy.data.cameras.new(name);data.type='ORTHO';data.ortho_scale=scale;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=location;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Fixed native cardinal camera',(8,-45,12),(8,0,12),24)
diagnostic=camera('Three dimensional diagnostic only',(34,-38,27),(7,0,12),30)
s.camera=front
# Source textures have baked planar shading. Direct neutral materials preserve
# shape and wear without a second image isolation or ImageGen redraw.
write('model-controls.json',dict(entry='SCN-DOOR',source=ref(OLD/'source-packet.json'),previous_registration=ref(OLD/'registered/model.json'),
    authored_geometry=dict(leaf_thickness=.58,frame_depth=.35,pivot=[2.9,-.27,0],hinge_y_down=[10.65,17.85],barrel_radius=.26,
        fixed_strap_x=[1.34,3.02],moving_strap_x=[2.79,4.31],rotation_closed=0,rotation_open_degrees=90),
    physical_units='Source native-coordinate authoring units, common 16 by 24 projection. Depth and hinges are authored estimates.',
    camera=dict(type='ORTHO',location=list(front.location),target=[8,0,12],ortho_scale=24,resolution=[512,768]),
    retained_material_inputs=[ref(OLD/'registered/cleaned-frame.png'),ref(HERE/'slate-surface-without-old-hardware.png')],
    new_imagegen_call=False,selection='Direct Blender geometry with retained usable source surface; no need to redraw texture.',native_acceptance='Pending full generation gate'))
s.camera=diagnostic;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front
for state,angle in [('closed',0),('open',90)]:
    pivot.rotation_euler.z=math.radians(angle);bpy.context.view_layer.update()
    for ob in [arch]+fixed+moving:ob.hide_render=False
    s.render.filepath=str(HERE/f'raw-{state}-full.png');bpy.ops.render.render(write_still=True)
    arch.hide_render=True
    s.render.filepath=str(HERE/f'raw-{state}-leaf.png');bpy.ops.render.render(write_still=True)
    arch.hide_render=False
    for ob in fixed+moving:ob.hide_render=True
    s.render.filepath=str(HERE/f'raw-{state}-frame.png');bpy.ops.render.render(write_still=True)
    for ob in fixed+moving:ob.hide_render=False
pivot.rotation_euler.z=0;s.camera=front
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'door.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'door.blend'),controls=ref(HERE/'model-controls.json'),
    textures_packed=True,states=['closed','open'],native_activation=False,complete_leaf_retained=True,shared_physical_hinge_axis=True))
print('Saved editable connected hinge/slab door and both direct state passes.')
