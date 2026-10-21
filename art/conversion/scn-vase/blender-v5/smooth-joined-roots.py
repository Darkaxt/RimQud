"""Retain editable construction; smooth actual surface transitions at four roots."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v3'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'vase.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'vase.blend'));s=bpy.context.scene;original=bpy.data.objects['Complete hollow vase'];controls=json.loads((OLD/'model-controls.json').read_text())
roots=[Vector(root['center']) for h in controls['handles'] for root in h['wall_seating']]
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(original.evaluated_get(deps),depsgraph=deps)
original.name='Editable original hollow vase and two unions';original.hide_render=True
body=bpy.data.objects.new('Complete hollow vase',mesh);s.collection.objects.link(body);s.view_layers[0].freestyle_settings.linesets[0].collection.objects.link(body)
group=body.vertex_groups.new(name='Four local pottery root transitions');affected=0
for v in mesh.vertices:
 distance=min((v.co-r).length for r in roots)
 if distance<1.1:group.add([v.index],(1-distance/1.1)**1.5,'REPLACE');affected+=1
smooth=body.modifiers.new('Local joined root relaxation','SMOOTH');smooth.factor=.65;smooth.iterations=8;smooth.vertex_group=group.name
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();finished=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);body.modifiers.clear();body.data=finished
clay=bpy.data.materials['Neutral canyon pottery'];slip=bpy.data.materials['Decorative slip - source detail ownership'];cavity=bpy.data.materials['Recessed pottery cavity - source primary'];finished.materials.clear()
for m in [clay,slip,cavity]:finished.materials.append(m)
# Semantic bands remain source-bound coordinates after local root smoothing.
for face in finished.polygons:
 radial=Vector((face.center.x-8,face.center.y,0));y=24-face.center.z;face.use_smooth=True
 face.material_index=2 if radial.dot(face.normal)<-.1 else 1 if (14.1<=y<=14.9 or 16.1<=y<=16.9) else 0
for mat in [clay,slip]:next(n for n in mat.node_tree.nodes if n.type=='VALTORGB').color_ramp.interpolation='LINEAR'
bm=bmesh.new();bm.from_mesh(finished);seen=set();components=[]
for v in bm.verts:
 if v in seen:continue
 component=[];todo=[v];seen.add(v)
 while todo:
  current=todo.pop();component.append(current)
  for edge in current.link_edges:
   other=edge.other_vert(current)
   if other not in seen:seen.add(other);todo.append(other)
 components.append(component)
components.sort(key=len,reverse=True);print('REMESH COMPONENTS',[(len(c),[round(max(v.co[k] for v in c)-min(v.co[k] for v in c),4) for k in range(3)]) for c in components])
audit=dict(nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces),euler_characteristic=len(bm.verts)-len(bm.edges)+len(bm.faces));bm.free();write('surface-refinement-audit.json',audit);assert audit==dict(nonmanifold_edges=0,zero_area_faces=0,euler_characteristic=-2),audit
s.camera=bpy.data.objects['Hollow pottery construction diagnostic'];s.render.filepath=str(HERE/'stage-03-refined-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera'];s.render.filepath=str(HERE/'raw-neutral-master.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Primary holdout for slip ownership');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);finished.materials[0]=hold;finished.materials[2]=hold;s.render.use_freestyle=False;s.render.filepath=str(HERE/'raw-slip-pass.png');bpy.ops.render.render(write_still=True);finished.materials[0]=clay;finished.materials[2]=cavity;s.render.use_freestyle=True
controls.update(resumed_from=ref(OLD/'vase.blend'),review_trigger=ref(OLD/'independent-structural-review.json'),root_surface_finish=dict(geometry_resolution='Original evaluated Boolean surface retained, no voxel reconstruction',local_radius=1.1,smooth_factor=.65,smooth_iterations=8,affected_vertices=affected,root_centers=[list(r) for r in roots],geometry='Complete joined hollow volume; original construction and editable handles retained.',material='Continuous neutral ramp matches restrained VTE pottery shading; eliminates hard toon patches at joins.',source_bands='Two unchanged world-coordinate slip bands, primary cavity material separate.'),selected_object='Complete hollow vase',native_activation=False,new_imagegen_call=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'vase.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'vase.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,new_imagegen_call=False,native_activation=False))
