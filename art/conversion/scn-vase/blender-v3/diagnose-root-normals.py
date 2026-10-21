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

print('Flat faces:',sum(not p.use_smooth for p in mesh.polygons),'of',len(mesh.polygons))
print('Flat face centers:',[(tuple(round(c,3) for c in p.center),round(p.area,6)) for p in mesh.polygons if not p.use_smooth][:15])
