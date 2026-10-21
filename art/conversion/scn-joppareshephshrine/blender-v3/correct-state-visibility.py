"""Resume saved refinement; diagnose geometry and isolate each native alternative by object identity."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'monuments.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'monuments.blend'));s=bpy.context.scene;controls=json.loads((OLD/'model-controls.json').read_text());deps=bpy.context.evaluated_depsgraph_get();diagnostic=[]
for ob in s.objects:
 if ob.type!='MESH':continue
 mesh=bpy.data.meshes.new_from_object(ob.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh);mesh.calc_loop_triangles();row=dict(object=ob.name,physical=bool(ob.get('physical')),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),degenerate_loop_triangles=sum((mesh.vertices[t.vertices[1]].co-mesh.vertices[t.vertices[0]].co).cross(mesh.vertices[t.vertices[2]].co-mesh.vertices[t.vertices[0]].co).length<1e-10 for t in mesh.loop_triangles));bm.free();diagnostic.append(row)
write('input-geometry-diagnostic.json',dict(source=ref(OLD/'monuments.blend'),elements=diagnostic,visibility_cause='Physical meshes also belonged to the shared outline collection, so hiding only their state collection left other alternatives render-visible. Per-object hide_render is required.'))
# Clean redundant clipping-boundary vertices in open surface-decoration meshes only.
for ob in s.objects:
 if ob.type=='MESH' and not ob.get('physical'):
  bm=bmesh.new();bm.from_mesh(ob.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7);bm.to_mesh(ob.data);bm.free();ob.data.update()
physical_rows=[r for r in diagnostic if r['physical'] and (r['zero_area_faces'] or r['nonmanifold_edges'])]
assert not physical_rows,physical_rows
def select(st):
 selected=set(bpy.data.collections[st['collection']].objects)
 for other in controls['states']:bpy.data.collections[other['collection']].hide_render=False
 for ob in s.objects:
  if ob.type=='MESH':ob.hide_render=ob not in selected
 assert {ob.name for ob in s.objects if ob.type=='MESH' and not ob.hide_render}=={ob.name for ob in selected if ob.type=='MESH'}
 return sorted(ob.name for ob in selected)
hold=bpy.data.materials.new('Primary ownership holdout');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);primary_slots=[(ob,i,slot.material) for ob in s.objects if ob.type=='MESH' for i,slot in enumerate(ob.material_slots) if slot.material and slot.material.get('native_role')=='primary'];visibility=[]
for st in controls['states']:
 visible=select(st);visibility.append(dict(state=st['id'],visible_objects=visible));root=bpy.data.objects[st['root']];root.rotation_euler.z=0;s.camera=bpy.data.objects['Monument diagnostic'];s.render.filepath=str(HERE/f'{st["id"]}-refined-3d.png');bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['Shared cardinal map camera']
 for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:
  root.rotation_euler.z=angle;s.render.filepath=str(HERE/f'{st["id"]}-{facing}-neutral.png');bpy.ops.render.render(write_still=True)
  for ob,i,material in primary_slots:ob.data.materials[i]=hold
  s.render.use_freestyle=False;s.render.filepath=str(HERE/f'{st["id"]}-{facing}-detail.png');bpy.ops.render.render(write_still=True)
  for ob,i,material in primary_slots:ob.data.materials[i]=material
  s.render.use_freestyle=True
 root.rotation_euler.z=0
select(controls['states'][-1]);s.camera=bpy.data.objects['Shared cardinal map camera'];controls.update(resumed_from=ref(OLD/'monuments.blend'),visibility='Per-object render visibility isolates exactly one state, including members of the shared physical-outline collection.',decoration_cleanup='Redundant clipping vertices welded and degenerate decoration edges dissolved; physical model geometry unchanged.');write('model-controls.json',controls);write('state-visibility.json',dict(states=visibility,one_state_only=True));bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'monuments.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'monuments.blend'),controls=ref(HERE/'model-controls.json'),actual_refined_renders=42,new_imagegen_call=False,native_activation=False))
