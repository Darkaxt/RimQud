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
