"""Diagnostic only: mark the actual starting end faces to test their visibility."""
from pathlib import Path
import bpy,json
HERE=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(HERE/'horns-fit.blend'))
scene=bpy.context.scene;scene.render.resolution_x=768;scene.render.resolution_y=1152
marker=bpy.data.materials.new('Diagnostic MAGENTA actual root end face');marker.use_nodes=True
n=marker.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=(1,0,1,1);o=n.new('ShaderNodeOutputMaterial');marker.node_tree.links.new(e.outputs[0],o.inputs[0])
for name in ['Left horn','Right horn']:
    ob=bpy.data.objects[name];ob.data.materials.append(marker);ob.data.polygons[-2].material_index=len(ob.data.materials)-1
scene.render.use_freestyle=False
for f in ['south','east','north']:
    scene.camera=bpy.data.objects[f.upper()+' - fixed768x1152'];scene.render.filepath=str(HERE/f'root-end-diagnostic-{f}.png');bpy.ops.render.render(write_still=True)
print('Actual buried root-end diagnostic rendered; canonical .blend unchanged.',flush=True)
