"""Inspect saved woven elements and the corrected no-tunneling fit."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];bpy.ops.wm.open_mainfile(filepath=str(HERE/'basket.blend'));s=bpy.context.scene;deps=bpy.context.evaluated_depsgraph_get();elements=[];materials=set()
for ob in s.objects:
 if ob.type not in ['MESH','CURVE']:continue
 mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh)
 if ob.type=='CURVE':bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
 result=dict(object=ob.name,type=ob.type,nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces));bm.free();assert result['nonmanifold_edges']==0 and result['zero_area_faces']==0,result;elements.append(result)
 materials.update(slot.material for slot in ob.material_slots if slot.material)
fits=[]
for row in range(6):
 ob=bpy.data.objects[f'Complete weft course {row}'];radial=[(v.co.x-8)*math.cos((k//2)*2*math.pi/128)+v.co.y*math.sin((k//2)*2*math.pi/128) for k,v in enumerate(ob.data.vertices)];fits.append(dict(course=row,minimum_outward_projection=min(radial)));assert min(radial)>0
images=[n.image.filepath for m in materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image];assert not images
assert abs(bpy.data.objects['Basket shared facing pivot'].rotation_euler.z)<1e-8
out=dict(reopened=True,blend=dict(path=(HERE/'basket.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'basket.blend').read_bytes()).hexdigest()),elements=elements,geometric_curve_closure='Curve-generated coincident cap boundaries welded only in the diagnostic mesh; saved source remains editable curves.',weft_outer_fit=fits,external_render_images=images,source_frame=[512,768],active_camera=s.camera.name,production_facing='south',native_activation=False,scope='Saved actual assembled woven components and absence of opposite-wall strand samples; no game/runtime validation.')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(dict(elements=len(elements),nonmanifold_edges=0,zero_area_faces=0,all_weft_samples_outward=True,external_images=images)))
