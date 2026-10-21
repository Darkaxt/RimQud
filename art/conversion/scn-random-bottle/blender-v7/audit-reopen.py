"""Check the saved evaluated fused glass surface, not just hidden endpoints."""
from pathlib import Path
import bpy,bmesh,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
bpy.ops.wm.open_mainfile(filepath=str(HERE/'bottle.blend'));body=bpy.data.objects['Hollow freeblown glass body'];deps=bpy.context.evaluated_depsgraph_get();evaluated=body.evaluated_get(deps);mesh=bpy.data.meshes.new_from_object(evaluated,depsgraph=deps)
bm=bmesh.new();bm.from_mesh(mesh);nonmanifold=sum(not e.is_manifold for e in bm.edges);zero=sum(f.calc_area()<1e-10 for f in bm.faces)
seen=set();components=0
for vertex in bm.verts:
    if vertex in seen:continue
    components+=1;pending=[vertex];seen.add(vertex)
    while pending:
        current=pending.pop()
        for edge in current.link_edges:
            other=edge.other_vert(current)
            if other not in seen:seen.add(other);pending.append(other)
euler=len(bm.verts)-len(bm.edges)+len(bm.faces)
out=dict(reopened=True,blend=dict(path=(HERE/'bottle.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'bottle.blend').read_bytes()).hexdigest()),evaluated_surface=dict(vertices=len(bm.verts),edges=len(bm.edges),faces=len(bm.faces),connected_components=components,nonmanifold_edges=nonmanifold,zero_area_faces=zero,euler_characteristic=euler),
    modifiers=[dict(name=m.name,type=m.type) for m in body.modifiers],scope='Actual evaluated joined surface diagnostics. Does not by itself establish visually flowing glass roots or native behavior.')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out['evaluated_surface']))
bm.free()
from mathutils.bvhtree import BVHTree
liquid=bpy.data.objects['Liquid contents - independent native detail tint'];lm=liquid.data
body_tree=BVHTree.FromPolygons([v.co for v in mesh.vertices],[tuple(p.vertices) for p in mesh.polygons])
liquid_tree=BVHTree.FromPolygons([v.co for v in lm.vertices],[tuple(p.vertices) for p in lm.polygons])
lb=bmesh.new();lb.from_mesh(lm)
from mathutils import Vector
lm.calc_loop_triangles();samples=[v.co.copy() for v in lm.vertices]+[sum((lm.vertices[k].co for k in t.vertices),Vector())/3 for t in lm.loop_triangles]
clearances=[]
for p in samples:
    axis=Vector((8,0,p.z));radial=p-axis;radius=radial.length;direction=radial.normalized() if radius>1e-8 else Vector((1,0,0));hit=body_tree.ray_cast(axis,direction)[0];assert hit is not None
    clearances.append((hit-axis).length-radius)
floor=body_tree.ray_cast(Vector((8,0,12)),Vector((0,0,-1)))[0]
out['liquid']=dict(separate_object=True,nonmanifold_edges=sum(not e.is_manifold for e in lb.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in lb.faces),sample_count=len(samples),minimum_radial_cavity_clearance=min(clearances),minimum_floor_clearance=min(v.co.z for v in lm.vertices)-floor.z,bvh_candidate_pairs=len(body_tree.overlap(liquid_tree)),candidate_note='BVH overlap returns candidate polygon bounding-box pairs, not proof of triangle intersections. Do not classify these pairs as leaks.',scope='Samples compare liquid vertices/triangle centroids against the evaluated radial cavity and floor; the passed field records the actual outcome. Static authoring diagnostics only.')
lb.free()
out['liquid']['passed']=bool(min(clearances)>0 and out['liquid']['minimum_floor_clearance']>0)
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
assert out['liquid']['nonmanifold_edges']==0 and out['liquid']['zero_area_faces']==0 and min(clearances)>0 and out['liquid']['minimum_floor_clearance']>0,out['liquid']
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out['liquid']))
