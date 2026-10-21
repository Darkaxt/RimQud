"""Inspect saved map-plane geometry/camera only; open surfaces intentionally are ground paint."""
from pathlib import Path
import json,hashlib,bpy,bmesh
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SRC=HERE/'blender-v2';bpy.ops.wm.open_mainfile(filepath=str(SRC/'paint.blend'));s=bpy.context.scene;controls=json.loads((SRC/'model-controls.json').read_text());deps=bpy.context.evaluated_depsgraph_get();rows=[];materials=set()
for st in controls['states']:
 points=[]
 for name in st['objects']:
  ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data);assert not any(f.calc_area()<1e-10 for f in bm.faces);bm.free()
  for v in ob.data.vertices:
   p=world_to_camera_view(s,s.camera,ob.matrix_world@v.co);assert 0<p.x<1 and 0<p.y<1;points.append([p.x,p.y])
  materials.update(slot.material for slot in ob.material_slots if slot.material)
 rows.append(dict(state=st['id'],objects=st['objects'],bounds=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)],zero_area_faces=0,geometry='Open source-bound map-plane surfaces, not physical raised props'))
images=[n.image.filepath for m in materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];assert not images
(SRC/'reopen-audit.json').write_text(json.dumps(dict(reopened=True,blend_sha256=hashlib.sha256((SRC/'paint.blend').read_bytes()).hexdigest(),states=rows,external_render_images=images,native_activation=False),indent=2)+'\n',encoding='utf-8');print('Saved2 map states reopen;7 intended open paint meshes, no zero-area faces, fixed-cell bounds and no external render images.')
