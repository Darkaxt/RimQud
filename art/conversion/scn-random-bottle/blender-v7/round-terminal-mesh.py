"""Round the existing terminal faces directly; no overlapping sphere operands."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v4'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'bottle.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'bottle.blend'));s=bpy.context.scene;s.cycles.samples=32
body=bpy.data.objects['Hollow freeblown glass body'];operand=bpy.data.objects['Fused handle solid operand - editable source curve retained']
old=operand.data;verts=[v.co.copy() for v in old.vertices];faces=[];caps=[];removed=set();rings=[]
points=bpy.data.objects['Connected lunar-arc glass handle'].data.splines[0].bezier_points
for index in [0,len(points)-1]:
 point=points[index];center=point.co.copy();axis=(center-(point.handle_right if index==0 else point.handle_left)).normalized()
 selected=[p for p in old.polygons if all(abs((verts[k]-center).dot(axis))<1e-5 for k in p.vertices)]
 assert selected,'No planar cap faces at endpoint'
 edges={}
 for p in selected:
  removed.add(p.index)
  for e in p.edge_keys:edges[tuple(sorted(e))]=edges.get(tuple(sorted(e)),0)+1
 boundary=[e for e,n in edges.items() if n==1];neighbors={}
 for a,b in boundary:neighbors.setdefault(a,[]).append(b);neighbors.setdefault(b,[]).append(a)
 start=min(neighbors);ring=[start];previous_vertex=None;current=start
 while True:
  options=[k for k in neighbors[current] if k!=previous_vertex];nxt=next((k for k in options if k not in ring),start)
  if nxt==start:break
  ring.append(nxt);previous_vertex,current=current,nxt
 assert len(ring)==len(neighbors)
 rings.append((ring,center,axis))
faces=[tuple(p.vertices) for p in old.polygons if p.index not in removed]
for ring,center,axis in rings:
 radius=sum((verts[k]-center).length for k in ring)/len(ring);previous=ring
 for j in range(1,5):
  angle=j*math.pi/10;current=[]
  for k in ring:current.append(len(verts));verts.append(center+(verts[k]-center)*math.cos(angle)+axis*radius*math.sin(angle))
  for k in range(len(ring)):faces.append((previous[k],previous[(k+1)%len(ring)],current[(k+1)%len(ring)],current[k]))
  previous=current
 pole=len(verts);verts.append(center+axis*radius)
 for k in range(len(ring)):faces.append((previous[k],previous[(k+1)%len(ring)],pole))
 caps.append(dict(center=list(center),normal=list(axis),radius=radius,original_boundary_vertices=len(ring)))
assert len(caps)==2
mesh=bpy.data.meshes.new('Rounded actual handle terminals');mesh.from_pydata(verts,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.delete(bm,geom=[v for v in bm.verts if not v.link_faces],context='VERTS');bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);assert all(f.calc_area()>1e-10 for f in bm.faces);bm.to_mesh(mesh);bm.free()
for m in old.materials:mesh.materials.append(m)
for p in mesh.polygons:p.use_smooth=True
operand.data=mesh;bpy.context.view_layer.update()
# Inspect the evaluated complete fused vessel before rendering or selecting it.
deps=bpy.context.evaluated_depsgraph_get();evaluated=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(evaluated)
topology=dict(nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces));bm.free();write('pre-render-topology.json',topology);assert topology==dict(nonmanifold_edges=0,zero_area_faces=0),topology
glass=bpy.data.materials['Translucent neutral glass shell - native primary'];liquid=bpy.data.objects['Liquid contents - independent native detail tint']
s.camera=bpy.data.objects['3D hollow-wall diagnostic'];s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera'];s.render.filepath=str(HERE/'raw-filled-neutral.png');bpy.ops.render.render(write_still=True)
liquid.hide_render=True;s.render.filepath=str(HERE/'raw-empty-glass.png');bpy.ops.render.render(write_still=True);liquid.hide_render=False
e=glass.node_tree.nodes['Neutral surface contribution'];link=next(l for l in glass.node_tree.links if l.to_socket==e.inputs[0]);source=link.from_socket;glass.node_tree.links.remove(link);e.inputs[0].default_value=(0,0,0,1)
s.render.filepath=str(HERE/'raw-liquid-contribution.png');bpy.ops.render.render(write_still=True);glass.node_tree.links.new(source,e.inputs[0])
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'bottle.blend'),rounded_terminal_mesh=caps,detail_region='Independent contained liquid geometry; source lower band guides authored fill extent.',samples=32,rejected_trials='v5/v6 sphere unions caused degenerate intersections; direct terminal rings replace the two flat caps.')
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,glass_and_liquid_separate=True,new_imagegen_call=False,native_activation=False))
