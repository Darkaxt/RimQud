"""Measure raw and evaluated source-cleft topology before approving its bevels."""
from pathlib import Path
import bpy,bmesh,json,hashlib,sys
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];folder=HERE/(sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'blender-v2');bpy.ops.wm.open_mainfile(filepath=str(folder/'cleft.blend'));s=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();rows=[];materials=set()
for ob in s.objects:
 if ob.type!='MESH':continue
 row=dict(object=ob.name);points=[]
 for kind,me in [('base',ob.data),('evaluated',bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps))]:
  bm=bmesh.new();bm.from_mesh(me);row[kind]=dict(zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges));bm.free()
  if kind=='evaluated':
   for v in me.vertices:
    p=world_to_camera_view(s,s.camera,ob.matrix_world@v.co);points.append([p.x,p.y])
   bpy.data.meshes.remove(me)
 row['bounds']=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)];rows.append(row);materials.update(slot.material for slot in ob.material_slots if slot.material)
images=[n.image.filepath for m in materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];out=dict(reopened=True,blend_sha256=hashlib.sha256((folder/'cleft.blend').read_bytes()).hexdigest(),elements=rows,external_render_images=images,native_activation=False);(folder/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(rows,indent=2))
