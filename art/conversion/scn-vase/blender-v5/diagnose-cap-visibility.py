"""Identify actual curve caps under the same selected local smoothing, without changing the asset."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];bpy.ops.wm.open_mainfile(filepath=str(HERE/'vase.blend'));s=bpy.context.scene;selected=bpy.data.objects['Complete hollow vase'];original=bpy.data.objects['Editable original hollow vase and two unions'];controls=json.loads((HERE/'model-controls.json').read_text());roots=[Vector(r) for r in controls['root_surface_finish']['root_centers']]
magenta=bpy.data.materials.new('Diagnostic actual terminal caps only');magenta.use_nodes=True;n=magenta.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(1,0,1,1);o=n.new('ShaderNodeOutputMaterial');magenta.node_tree.links.new(e.outputs[0],o.inputs[0]);original.data.materials.append(magenta);cap_faces=0
for label in ['right','left']:
 source=bpy.data.objects[f'Editable {label} pottery handle'];operand=bpy.data.objects[f'{label} joined handle operand']
 operand.data.materials.clear()
 for m in original.data.materials:operand.data.materials.append(m)
 points=source.data.splines[0].bezier_points
 for index in [0,len(points)-1]:
  point=points[index];axis=(point.co-(point.handle_right if index==0 else point.handle_left)).normalized()
  for face in operand.data.polygons:
   if all(abs((operand.data.vertices[k].co-point.co).dot(axis))<1e-5 for k in face.vertices):face.material_index=3;cap_faces+=1
assert cap_faces>0
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(original.evaluated_get(deps),depsgraph=deps);probe=bpy.data.objects.new('Selected root surface diagnostic',mesh);s.collection.objects.link(probe);s.view_layers[0].freestyle_settings.linesets[0].collection.objects.link(probe);group=probe.vertex_groups.new(name='Same local root smoothing')
for v in mesh.vertices:
 distance=min((v.co-r).length for r in roots)
 if distance<1.1:group.add([v.index],(1-distance/1.1)**1.5,'REPLACE')
smooth=probe.modifiers.new('Same selected local relaxation','SMOOTH');smooth.factor=.65;smooth.iterations=8;smooth.vertex_group=group.name;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();evaluated=bpy.data.meshes.new_from_object(probe.evaluated_get(deps),depsgraph=deps)
assert len(evaluated.vertices)==len(selected.data.vertices)
maximum=max((a.co-b.co).length for a,b in zip(evaluated.vertices,selected.data.vertices));assert maximum<1e-5,maximum
selected.hide_render=True;original.hide_render=True;s.camera=bpy.data.objects['Hollow pottery construction diagnostic'];s.render.filepath=str(HERE/'cap-visibility-diagnostic.png');bpy.ops.render.render(write_still=True)
image=bpy.data.images.load(str(HERE/'cap-visibility-diagnostic.png'));pixels=list(image.pixels);visible=sum(pixels[k]>.65 and pixels[k+1]<.15 and pixels[k+2]>.65 and pixels[k+3]>.1 for k in range(0,len(pixels),4))
out=dict(actual_terminal_cap_faces_marked=cap_faces,selected_geometry_maximum_vertex_delta=maximum,visible_magenta_pixels=visible,diagnostic='Only actual curve terminal faces are magenta. The same Boolean surface and local smoothing reproduce selected geometry; production asset was not changed.',render=dict(path=(HERE/'cap-visibility-diagnostic.png').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'cap-visibility-diagnostic.png').read_bytes()).hexdigest()),native_activation=False)
(HERE/'cap-visibility-result.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
