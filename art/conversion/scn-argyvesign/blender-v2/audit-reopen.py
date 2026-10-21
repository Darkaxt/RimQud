"""Inspect saved physical plaque and front paint attachment, not runtime behavior."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
bpy.ops.wm.open_mainfile(filepath=str(HERE/'sign.blend'));s=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();elements=[];materials=set();projected=[]
for ob in s.objects:
 if ob.type!='MESH':continue
 mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh)
 paint=ob.name=='Front-only source pictogram paint';row=dict(object=ob.name,role='Attached front paint surface' if paint else 'Closed physical element',nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces))
 assert row['zero_area_faces']==0,row
 if not paint:assert row['nonmanifold_edges']==0,row
 else:
  assert len(mesh.polygons)==43
  assert all(abs(v.co.y+.279)<1e-6 and 3<=v.co.x<=13 and 9<=v.co.z<=17 for v in mesh.vertices)
 for v in mesh.vertices:
  co=world_to_camera_view(s,s.camera,ob.matrix_world@v.co);assert 0<co.x<1 and 0<co.y<1;projected.append([co.x,co.y])
 bm.free();elements.append(row);materials.update(slot.material for slot in ob.material_slots if slot.material)
assert not any(o.type=='FONT' for o in s.objects)
assert abs(bpy.data.objects['Sign shared physical pivot'].rotation_euler.z)<1e-8
images=[n.image.filepath for m in materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];assert not images
controls=json.loads((HERE/'model-controls.json').read_text());overlap=controls['board_depth'][1]-(controls['posts']['y_center']-controls['posts']['depth']/2);assert overlap>.14
out=dict(reopened=True,blend=dict(path=(HERE/'sign.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'sign.blend').read_bytes()).hexdigest()),elements=elements,paint_contract='43 front-only flat source cells, within plaque field; open surface by design, not a physical solid or cut-through mask.',support_plaque_depth_overlap=overlap,all_geometry_inside_shared_frame=True,external_render_images=images,source_frame=[512,768],active_camera=s.camera.name,production_facing='south',native_activation=False,scope='Saved mesh, paint contact and frame diagnostics only; no game/runtime validation.')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))
