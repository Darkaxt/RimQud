"""Resume transparent glass; replace visible flat handle caps with rounded roots."""
from pathlib import Path
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v4'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'bottle.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'bottle.blend'));s=bpy.context.scene;s.cycles.samples=32
body=bpy.data.objects['Hollow freeblown glass body'];handle=bpy.data.objects['Connected lunar-arc glass handle'];operand=bpy.data.objects['Fused handle solid operand - editable source curve retained'];glass=bpy.data.materials['Translucent neutral glass shell - native primary']
roots=[]
for i in [0,len(handle.data.splines[0].bezier_points)-1]:
 point=handle.data.splines[0].bezier_points[i];radius=handle.data.bevel_depth*point.radius
 bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=radius,location=point.co)
 root=bpy.context.object;root.name=f'Rounded fused glass root {i}';root.data.materials.append(glass)
 for p in root.data.polygons:p.use_smooth=True
 m=operand.modifiers.new(f'Round actual handle terminal {i}','BOOLEAN');m.operation='UNION';m.solver='EXACT';m.object=root
 root.hide_render=True;roots.append(dict(endpoint=i,center=list(point.co),radius=radius,method='Actual sphere unions over flat curve cap; transparent shell and hollow wall retained.'))
body.modifiers['Small fused glass root fillets'].width=.075
bpy.context.view_layer.update()
front=bpy.data.objects['Fixed source map camera'];diag=bpy.data.objects['3D hollow-wall diagnostic'];liquid=bpy.data.objects['Liquid contents - independent native detail tint']
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'raw-filled-neutral.png');bpy.ops.render.render(write_still=True)
liquid.hide_render=True;s.render.filepath=str(HERE/'raw-empty-glass.png');bpy.ops.render.render(write_still=True);liquid.hide_render=False
e=glass.node_tree.nodes['Neutral surface contribution'];link=next(l for l in glass.node_tree.links if l.to_socket==e.inputs[0]);source=link.from_socket;glass.node_tree.links.remove(link);e.inputs[0].default_value=(0,0,0,1)
s.render.filepath=str(HERE/'raw-liquid-contribution.png');bpy.ops.render.render(write_still=True);glass.node_tree.links.new(source,e.inputs[0])
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'bottle.blend'),rounded_root_correction=roots,review_trigger=ref(OLD/'independent-structural-review.json'),detail_region='Separate contained liquid volume; source lower band only guides authored fill extent.',samples=32)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,glass_and_liquid_separate=True,new_imagegen_call=False,native_activation=False))
print('Rounded roots saved in resumed translucent glass model.')
