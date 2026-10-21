"""Saved geometry/frame/attachment diagnostic, without native activation."""
from pathlib import Path
import json,hashlib,bpy,bmesh,sys
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(sys.argv[sys.argv.index('--')+1]).resolve() if '--' in sys.argv else Path(__file__).resolve().parent;ROOT=HERE.parents[3];bpy.ops.wm.open_mainfile(filepath=str(HERE/'canvas.blend'));s=bpy.context.scene;c=json.loads((HERE/'model-controls.json').read_text());deps=bpy.context.evaluated_depsgraph_get();rows=[];materials=set();frames=[];anchors=[]
for ob in s.objects:
 if ob.type!='MESH':continue
 me=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(me);row=dict(object=ob.name,physical=bool(ob.get('physical')),zero_area_faces=sum(f.calc_area()<1e-12 for f in bm.faces),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges));assert row['zero_area_faces']==0,row
 if row['physical']:assert row['nonmanifold_edges']==0,row
 bm.free();bpy.data.meshes.remove(me);rows.append(row);materials.update(slot.material for slot in ob.material_slots if slot.material)
images=[n.image.filepath for m in materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];assert not images
for st in c['states']:
 points=[]
 for name in st['objects']:
  ob=bpy.data.objects[name];me=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps)
  for v in me.vertices:points.append(list(world_to_camera_view(s,s.camera,ob.matrix_world@v.co))[:2])
  bpy.data.meshes.remove(me)
 bounds=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)]
 for exceeded,bit,side in [(bounds[0]<0,8,'W'),(bounds[2]>1,2,'E'),(bounds[1]<0,4,'S'),(bounds[3]>1,1,'N')]:assert not exceeded or st['mask']&bit,(st['mask'],side,bounds)
 frames.append(dict(mask=st['mask'],bounds=bounds,crop_allowed_only_on_declared_connections=True))
 for direction,p in c['attachment_anchors'].items():
  ob=bpy.data.objects[f'{st["mask"]:02d} attachment {direction}'];assert (ob.location-Vector(p)).length<1e-7;anchors.append(dict(mask=st['mask'],direction=direction,point=p))
out=dict(reopened=True,blend=dict(path=(HERE/'canvas.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'canvas.blend').read_bytes()).hexdigest()),elements=rows,frame_checks=frames,attachment_anchors=anchors,external_render_images=images,limits='Authored geometry and render-frame diagnostic only. Half-arm continuations beyond declared connected crops avoid exposed endcaps; native gate and other item groups unchanged.',native_activation=False)
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(physical=sum(r['physical'] for r in rows),decorations=sum(not r['physical'] for r in rows),frame_checks=len(frames),anchors=len(anchors),external_images=images)))
