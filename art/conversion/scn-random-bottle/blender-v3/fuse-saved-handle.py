"""Fuse the handle into the retained hollow wall, preserving editable controls."""
from pathlib import Path
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
assert not (HERE/'bottle.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'bottle.blend'));s=bpy.context.scene;body=bpy.data.objects['Hollow freeblown glass body'];handle=bpy.data.objects['Connected lunar-arc glass handle']
handle.data.use_fill_caps=True
for k,p in enumerate(handle.data.splines[0].bezier_points):p.radius=1.3 if k in [0,len(handle.data.splines[0].bezier_points)-1] else 1
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();evaluated=handle.evaluated_get(deps)
mesh=bpy.data.meshes.new_from_object(evaluated,depsgraph=deps);operand=bpy.data.objects.new('Fused handle solid operand - editable source curve retained',mesh);s.collection.objects.link(operand)
operand.matrix_world=handle.matrix_world.copy();operand.hide_render=True;handle.hide_render=True
modifier=body.modifiers.new('Actual joined glass handle roots','BOOLEAN');modifier.operation='UNION';modifier.solver='EXACT';modifier.object=operand;modifier.material_mode='INDEX'
bevel=body.modifiers.new('Small fused glass root fillets','BEVEL');bevel.width=.055;bevel.segments=3;bevel.limit_method='ANGLE';bevel.angle_limit=.5;bevel.use_clamp_overlap=True
front=bpy.data.objects['Fixed source map camera'];diag=bpy.data.objects['3D hollow-wall diagnostic']
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'raw-neutral-master.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Transient primary ownership holdout');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);original=body.data.materials[0];body.data.materials[0]=hold
s.render.use_freestyle=False;s.render.filepath=str(HERE/'raw-detail-pass.png');bpy.ops.render.render(write_still=True);s.render.use_freestyle=True;body.data.materials[0]=original
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'bottle.blend'),root_correction=dict(source_review=ref(OLD/'independent-structural-review.json'),
    method='Closed handle operand unioned with already rounded hollow glass wall; endpoint radius1.3 and small actual root fillet. Original curve remains editable and saved.',root_fillet_width=.055,
    same_source_handle_points=True,source_frame_unchanged=True,not_a_2d_mask_patch=True))
write('model-controls.json',controls)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,new_imagegen_call=False,native_activation=False))
