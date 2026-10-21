"""Inspect the saved selected hollow-pottery model and its real dependencies."""
from pathlib import Path
import bpy,bmesh,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];bpy.ops.wm.open_mainfile(filepath=str(HERE/'vase.blend'));body=bpy.data.objects['Complete hollow vase'];deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh);seen=set();components=0
for v in bm.verts:
 if v in seen:continue
 components+=1;todo=[v];seen.add(v)
 while todo:
  v=todo.pop()
  for edge in v.link_edges:
   other=edge.other_vert(v)
   if other not in seen:seen.add(other);todo.append(other)
surface=dict(connected_components=components,nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces),euler_characteristic=len(bm.verts)-len(bm.edges)+len(bm.faces));bm.free()
materials={slot.material for ob in [body,bpy.data.objects['right joined handle operand'],bpy.data.objects['left joined handle operand']] for slot in ob.material_slots if slot.material};images=[n.image.filepath for m in materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image]
out=dict(reopened=True,blend=dict(path=(HERE/'vase.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'vase.blend').read_bytes()).hexdigest()),evaluated_surface=surface,render_material_external_images=images,active_camera=bpy.context.scene.camera.name,source_frame=[512,768],root_bevel_rendered=body.modifiers['Small fused pottery root edge'].show_render,scope='Saved complete hollow pottery and two actual handle unions; no game/runtime validation.')
assert surface['connected_components']==1 and surface['nonmanifold_edges']==0 and surface['zero_area_faces']==0 and not images and not out['root_bevel_rendered'],out
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
