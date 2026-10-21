"""Bounded Blender authoring trial: actual model, fixed orthographic views.

Run with Blender --background --factory-startup --python this_file.
No skill deployment, production registration or game integration.
"""
import bpy
import math
import json
import hashlib
from pathlib import Path
from mathutils import Vector
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
VOLUME=HERE/'volume.json'
data=json.loads(VOLUME.read_text())
SCALE=.01
def xyz(p):return Vector((p[0]*SCALE,-p[2]*SCALE,-p[1]*SCALE))
def save_json(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def ref(path):return dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene
scene.render.engine='CYCLES'
scene.cycles.device='CPU'
scene.cycles.samples=16
scene.cycles.use_denoising=True
scene.render.threads_mode='FIXED'
scene.render.threads=4
scene.render.resolution_x=768
scene.render.resolution_y=1152
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.image_settings.color_mode='RGBA'
scene.render.image_settings.color_depth='8'
scene.render.film_transparent=True
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.world.color=(.32,.32,.32)
scene.render.use_file_extension=True
bpy.context.preferences.filepaths.save_version=0

def material(name,color):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1)
    m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=.88
    return m
bone=material('Neutral bone - toon render trial',(.72,.72,.72))
nodes=bone.node_tree.nodes;links=bone.node_tree.links
attr=nodes.new('ShaderNodeAttribute');attr.attribute_name='arc_fraction'
mult=nodes.new('ShaderNodeMath');mult.operation='MULTIPLY';mult.inputs[1].default_value=2*math.pi*17
cos=nodes.new('ShaderNodeMath');cos.operation='COSINE'
ramp=nodes.new('ShaderNodeValToRGB')
ramp.color_ramp.elements[0].position=.86;ramp.color_ramp.elements[0].color=(.62,.62,.62,1)
ramp.color_ramp.elements[1].position=1;ramp.color_ramp.elements[1].color=(.40,.40,.40,1)
links.new(attr.outputs['Fac'],mult.inputs[0]);links.new(mult.outputs[0],cos.inputs[0]);links.new(cos.outputs[0],ramp.inputs[0])
# Blender-native stepped shading from actual surface normals: neutral,
# stable and simple, without image quantization or generative redraw.
geometry=nodes.new('ShaderNodeNewGeometry')
dot=nodes.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.4,-.5,.76)
shade=nodes.new('ShaderNodeValToRGB');shade.color_ramp.interpolation='CONSTANT'
shade.color_ramp.elements[0].position=.10;shade.color_ramp.elements[0].color=(.24,.24,.24,1)
shade.color_ramp.elements[1].position=.70;shade.color_ramp.elements[1].color=(.78,.78,.78,1)
shade.color_ramp.elements.new(.40).color=(.50,.50,.50,1)
links.new(geometry.outputs['Normal'],dot.inputs[0]);links.new(dot.outputs['Value'],shade.inputs[0])
mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.34
links.new(shade.outputs[0],mix.inputs[1]);links.new(ramp.outputs[0],mix.inputs[2])
emit=nodes.new('ShaderNodeEmission');links.new(mix.outputs[0],emit.inputs['Color']);links.new(emit.outputs[0],nodes.get('Material Output').inputs['Surface'])
# Freestyle supplies actual render-time contours, excluding the skull proxy.
horn_lines=bpy.data.collections.new('Horn contour selection');scene.collection.children.link(horn_lines)
scene.render.use_freestyle=True
fs=scene.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Visible horn silhouettes');ls.select_by_collection=True;ls.collection=horn_lines;ls.collection_negation='INCLUSIVE'
ls.select_crease=False;ls.select_border=True;ls.select_silhouette=True;ls.select_contour=True;ls.select_external_contour=True
ls.linestyle.color=(.012,.012,.012);ls.linestyle.thickness=2.6;ls.linestyle.caps='ROUND'

skullmat=material('Red skull proxy - NOT original body',(.60,.025,.025))
holdout=bpy.data.materials.new('Head occlusion only - full item retained separately');holdout.use_nodes=True
hn=holdout.node_tree.nodes;hn.clear();h=hn.new('ShaderNodeHoldout');out=hn.new('ShaderNodeOutputMaterial');holdout.node_tree.links.new(h.outputs[0],out.inputs['Surface'])

centers=[xyz(p) for p in data['centerline']]
radius=data['radius'];sides=24
for sign in [-1,1]:
    cs=[Vector((p.x*sign,p.y,p.z)) for p in centers]
    verts=[];faces=[]
    for j,p in enumerate(cs):
        t=(cs[min(j+1,len(cs)-1)]-cs[max(j-1,0)]).normalized()
        a=t.cross(Vector((1,0,0))).normalized();b=t.cross(a).normalized()
        for k in range(sides):
            theta=k*2*math.pi/sides
            verts.append(p+(a*math.cos(theta)+b*math.sin(theta))*radius[j]*SCALE)
    for j in range(len(cs)-1):
        for k in range(sides):
            i=j*sides+k;n=j*sides+(k+1)%sides
            faces.append((i,n,n+sides,i+sides))
    faces.extend([tuple(reversed(range(sides))),tuple((len(cs)-1)*sides+k for k in range(sides))])
    mesh=bpy.data.meshes.new('Continuous tapered horn mesh');mesh.from_pydata(verts,[],faces);mesh.update()
    obj=bpy.data.objects.new('Left horn' if sign<0 else 'Right horn',mesh);scene.collection.objects.link(obj)
    obj.data.materials.append(bone);horn_lines.objects.link(obj)
    for poly in mesh.polygons:poly.use_smooth=True
    attribute=mesh.attributes.new('arc_fraction','FLOAT','POINT')
    for i,v in enumerate(attribute.data):v.value=(i//sides)/(len(cs)-1)
    obj['geometry_role']='Complete physical item including buried root; never cut against head'
    obj['native_item']='Horns575 / Head288 / laterality0'

bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,location=xyz([0,185,25]))
skull=bpy.context.object;skull.name='Authored skull proxy - excluded from final body art'
skull.scale=(.90,.70,.90);skull.data.materials.append(skullmat)
for p in skull.data.polygons:p.use_smooth=True
skull['limitation']='Ellipsoid fit aid; original body/head PNG pixels remain authoritative'

def camera(name,target,offset,ortho):
    c=bpy.data.cameras.new(name);c.type='ORTHO';c.ortho_scale=ortho
    o=bpy.data.objects.new(name,c);scene.collection.objects.link(o);o.location=Vector(target)+Vector(offset)
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
    return o
cameras={
 'south':camera('SOUTH - fixed768x1152', (0,0,-5.76),(0,-20,0),11.52),
 'east':camera('EAST - fixed768x1152', (0,.86,-5.58),(-20,0,0),11.52),
 'north':camera('NORTH - fixed768x1152', (0,0,-5.60),(0,20,0),11.52),
 'west':camera('WEST - fixed768x1152', (0,.86,-5.58),(20,0,0),11.52),
}
probe=camera('DIAGNOSTIC three-quarter - not production', (0,-.1,-1.5),(-6,-8,4),4.4)
for name,loc,power,size in [('Soft key',(-4,-6,6),600,5),('Soft fill',(4,2,3),300,5)]:
    ld=bpy.data.lights.new(name,'AREA');ld.energy=power;ld.shape='DISK';ld.size=size
    ob=bpy.data.objects.new(name,ld);scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector((0,0,-1.5))-ob.location).to_track_quat('-Z','Y').to_euler()

scene['source_contract']='One editable volume, orthographic cardinal views at100px/Blender unit. No independent bounds fitting.'
scene['trial_scope']='Third manual trial: continuous upper-forehead emergence, same main curl, simple rendered tone regions. Skill is updated; current horn fit remains unapproved.'
scene.camera=probe
scene.render.resolution_x=900;scene.render.resolution_y=900
scene.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
scene.render.resolution_x=768;scene.render.resolution_y=1152
renders=[]
for face,cam in cameras.items():
    if face=='west':continue  # Symmetric geometry; inspect direct S/E/N first.
    scene.camera=cam
    for mode in ['whole-item','with-skull','visible-item']:
        skull.hide_render=mode=='whole-item'
        skull.data.materials[0]=holdout if mode=='visible-item' else skullmat
        p=HERE/f'{mode}-{face}.png';scene.render.filepath=str(p);bpy.ops.render.render(write_still=True)
        renders.append(ref(p))
skull.hide_render=False;skull.data.materials[0]=skullmat
# Remove unused startup brushes/materials instead of saving external brush links.
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
scene.camera=probe
scene.render.resolution_x=900;scene.render.resolution_y=900
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'horns-trial.blend'))
save_json(HERE/'blender-receipt.json',dict(recorded_at=datetime.now(timezone.utc).isoformat(),blender_version=bpy.app.version_string,blender_build_hash=bpy.app.build_hash.decode(),source_volume=ref(VOLUME),script=ref(Path(__file__)),blend=ref(HERE/'horns-trial.blend'),render_engine=scene.render.engine,outline='Blender Freestyle visible horn collection,2.6px',shading='Blender normal-based three neutral tone regions, groove modulation and emission',samples=16,threads=4,cameras={f:dict(type=c.data.type,ortho_scale=c.data.ortho_scale,location=list(c.location),rotation_euler=list(c.rotation_euler)) for f,c in cameras.items()},renders=renders,body_changed=False,production_registration=False,skill_applied=False))
print('BLENDER_TRIAL_RENDER_COMPLETE',flush=True)
