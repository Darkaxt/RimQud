"""Resume joined vessel, seat roots in its wall and separate glass/liquid optics."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v3'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
assert not (HERE/'bottle.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'bottle.blend'));s=bpy.context.scene;s.cycles.transparent_max_bounces=16
body=bpy.data.objects['Hollow freeblown glass body'];handle=bpy.data.objects['Connected lunar-arc glass handle'];operand=bpy.data.objects['Fused handle solid operand - editable source curve retained']
union=body.modifiers['Actual joined glass handle roots'];fillet=body.modifiers['Small fused glass root fillets'];union.show_viewport=False;fillet.show_viewport=False;bpy.context.view_layer.update()
deps=bpy.context.evaluated_depsgraph_get();pure=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps)
bvh=BVHTree.FromPolygons([v.co for v in pure.vertices],[tuple(p.vertices) for p in pure.polygons]);seating=[];ps=handle.data.splines[0].bezier_points
for k in [0,len(ps)-1]:
    point=ps[k];direction=Vector((1,0,0));origin=Vector((8,0,point.co.z));inside=bvh.ray_cast(origin,direction)[0];assert inside is not None
    outside=bvh.ray_cast(inside+direction*.0001,direction)[0];assert outside is not None and outside.x>inside.x
    point.co.x=(inside.x+outside.x)/2;point.radius=.8;point.handle_left_type='AUTO';point.handle_right_type='AUTO'
    seating.append(dict(endpoint=k,inner_wall=list(inside),outer_wall=list(outside),seated_center=list(point.co),radius_scale=.8))
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();operand.data=bpy.data.meshes.new_from_object(handle.evaluated_get(deps),depsgraph=deps)
union.show_viewport=True;fillet.show_viewport=True;bpy.context.view_layer.update()

def surface(name,values,base_opacity,fresnel=False):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
    g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.75,.35)
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
    for el,v,pos in [(ramp.color_ramp.elements[0],values[0],0),(ramp.color_ramp.elements[1],values[2],.72)]:el.position=pos;el.color=(v,v,v,1)
    el=ramp.color_ramp.elements.new(.25);el.color=(values[1],)*3+(1,)
    e=n.new('ShaderNodeEmission');e.name='Neutral surface contribution';t=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');out=n.new('ShaderNodeOutputMaterial')
    l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],ramp.inputs[0]);l.new(ramp.outputs[0],e.inputs[0]);l.new(t.outputs[0],mix.inputs[1]);l.new(e.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    if fresnel:
        f=n.new('ShaderNodeFresnel');f.inputs['IOR'].default_value=1.45;mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=.72;add=n.new('ShaderNodeMath');add.operation='ADD';add.inputs[1].default_value=base_opacity;add.use_clamp=True
        l.new(f.outputs[0],mul.inputs[0]);l.new(mul.outputs[0],add.inputs[0]);l.new(add.outputs[0],mix.inputs[0])
    else:mix.inputs[0].default_value=base_opacity
    return m
glass=surface('Translucent neutral glass shell - native primary',(.42,.75,.98),.055,True)
liquidmat=surface('Separate neutral liquid - native detail',(.22,.5,.75),.88)
for slot in body.material_slots:slot.material=glass
for slot in operand.material_slots:slot.material=glass
for slot in handle.material_slots:slot.material=glass
# Source lower band supplies one illustrative fill extent, not a measurement
# from RandomLiquid volume or a new state family. The empty shell remains saved.
profile=[(0,19.62),(1.85,19.62),(2.85,19.05),(3.55,17.10),(0,17.10)];sides=96;verts=[];faces=[]
for r,y in profile:
    for k in range(sides):
        angle=k*2*math.pi/sides;verts.append((8+r*math.cos(angle),r*math.sin(angle),24-y))
for j in range(len(profile)-1):
    for k in range(sides):faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
mesh=bpy.data.meshes.new('Independent source-band liquid volume');mesh.from_pydata(verts,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
liquid=bpy.data.objects.new('Liquid contents - independent native detail tint',mesh);s.collection.objects.link(liquid);mesh.materials.append(liquidmat)
for p in mesh.polygons:p.use_smooth=p.center.z<6.89
front=bpy.data.objects['Fixed source map camera'];diag=bpy.data.objects['3D hollow-wall diagnostic']
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'raw-filled-neutral.png');bpy.ops.render.render(write_still=True)
liquid.hide_render=True;s.render.filepath=str(HERE/'raw-empty-glass.png');bpy.ops.render.render(write_still=True);liquid.hide_render=False
# A semantic contribution pass keeps the same transparency and liquid shade,
# but makes glass emission black. Linearize saved RGB to recover conditional
# liquid light contribution, then apply the native 2D tint formula separately.
e=glass.node_tree.nodes['Neutral surface contribution'];link=next(l for l in glass.node_tree.links if l.to_socket==e.inputs[0]);from_socket=link.from_socket;glass.node_tree.links.remove(link);e.inputs[0].default_value=(0,0,0,1)
s.render.filepath=str(HERE/'raw-liquid-contribution.png');bpy.ops.render.render(write_still=True);glass.node_tree.links.new(from_socket,e.inputs[0])
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'bottle.blend'),handle_wall_seating=seating,
    glass_method='Translucent neutral glass shell: opacity .055+.72*Fresnel(IOR1.45), same actual hollow model/handle. Native color applied independently.',
    independent_liquid=dict(profile_radius_y=profile,opacity=.88,fill_extent='Authored from native lower detail band, not a runtime volume measurement.',native_role='DetailColorByLiquid; no liquid identity is guessed.'),
    semantic_pass='Glass emission black with identical transparency; liquid contribution linearized for conditional native detail ownership.',
    empty_shell='Authoring layer retained; actual native empty/filled dispatch remains behind the full generation gate.',
    user_direction='User identified transparent glass with liquid inside; opaque geometry drafts superseded as material selection.',new_imagegen_call=False,native_activation=False)
write('model-controls.json',controls)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,glass_and_liquid_separate=True,new_imagegen_call=False,native_activation=False))
print('Saved translucent glass vessel, seated fused handle and separate liquid geometry.')
