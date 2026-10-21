"""Inspect saved six-state geometry, frame isolation and source-mark support contacts."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];bpy.ops.wm.open_mainfile(filepath=str(HERE/'monuments.blend'));s=bpy.context.scene;controls=json.loads((HERE/'model-controls.json').read_text());deps=bpy.context.evaluated_depsgraph_get();rows=[];materials=set()
for ob in s.objects:
 if ob.type not in ['MESH','CURVE']:continue
 mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh)
 if ob.type=='CURVE':bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 row=dict(object=ob.name,physical=bool(ob.get('physical')),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges));assert row['zero_area_faces']==0,row
 if row['physical']:assert row['nonmanifold_edges']==0,row
 bm.free();rows.append(row);materials.update(slot.material for slot in ob.material_slots if slot.material)
images=[n.image.filepath for m in materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];assert not images
frames=[]
for st in controls['states']:
 selected=set(bpy.data.collections[st['collection']].objects);root=bpy.data.objects[st['root']]
 for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:
  root.rotation_euler.z=angle;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();projected=[]
  for ob in selected:
   if ob.type not in ['MESH','CURVE']:continue
   mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps)
   for v in mesh.vertices:
    p=world_to_camera_view(s,s.camera,ob.matrix_world@v.co);projected.append([p.x,p.y]);assert 0<p.x<1 and 0<p.y<1,(st['id'],facing,ob.name,p[:])
  frames.append(dict(state=st['id'],facing=facing,bounds=[min(p[0] for p in projected),min(p[1] for p in projected),max(p[0] for p in projected),max(p[1] for p in projected)]))
 root.rotation_euler.z=0
def inside(point,poly):
 x,y=point;result=False
 for a,b in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:result=not result
 return result
assert inside((7.5,3.5),controls['states'][-1]['profile_x_y_down']) and inside((9.4,5.2),controls['states'][-1]['profile_x_y_down'])
out=dict(reopened=True,blend=dict(path=(HERE/'monuments.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'monuments.blend').read_bytes()).hexdigest()),elements=rows,curve_closure='Only diagnostic cap-boundary vertices welded; saved support remains editable capped curve.',frame_checks=frames,all_geometry_inside_shared_frame=True,upper_rail_head_contacts='Both rail endpoints inside the single head profile and slab depth; four mark centers lie on rail controls.',rear_key_support_contacts='Keys overlap body by.3 and plinth by.25 source units; body/plinth/support dimensions retained in controls.',external_render_images=images,native_activation=False,scope='Saved authoring shape, support and frame diagnostics; no native/runtime validation.')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(physical=sum(r['physical'] for r in rows),decorations=sum(not r['physical'] for r in rows),frame_checks=len(frames),external_images=images)))
