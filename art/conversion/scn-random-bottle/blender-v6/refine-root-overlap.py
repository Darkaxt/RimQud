"""Remove coincident cap/equator edges in the rounded glass root operands."""
from pathlib import Path
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v5'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'bottle.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'bottle.blend'));s=bpy.context.scene
for ob in bpy.data.objects:
 if ob.name.startswith('Rounded fused glass root '):ob.scale=(1.2,1.2,1.2)
bpy.context.view_layer.update()
glass=bpy.data.materials['Translucent neutral glass shell - native primary'];liquid=bpy.data.objects['Liquid contents - independent native detail tint']
s.camera=bpy.data.objects['3D hollow-wall diagnostic'];s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera'];s.render.filepath=str(HERE/'raw-filled-neutral.png');bpy.ops.render.render(write_still=True)
liquid.hide_render=True;s.render.filepath=str(HERE/'raw-empty-glass.png');bpy.ops.render.render(write_still=True);liquid.hide_render=False
e=glass.node_tree.nodes['Neutral surface contribution'];link=next(l for l in glass.node_tree.links if l.to_socket==e.inputs[0]);source=link.from_socket;glass.node_tree.links.remove(link);e.inputs[0].default_value=(0,0,0,1)
s.render.filepath=str(HERE/'raw-liquid-contribution.png');bpy.ops.render.render(write_still=True);glass.node_tree.links.new(source,e.inputs[0])
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'bottle.blend'),root_overlap_correction=dict(scale=1.2,reason='v5 equal-radius sphere equator coincided with curve cap boundary. Slightly larger actual fused glass bead removes this degenerate Boolean intersection.',rejected_audit=ref(OLD/'reopen-audit.json')))
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,glass_and_liquid_separate=True,new_imagegen_call=False,native_activation=False))
