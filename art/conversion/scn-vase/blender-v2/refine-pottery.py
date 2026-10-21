"""Resume manual pottery, seat hidden roots and finish slip/contours directly."""
from pathlib import Path
import bpy,bmesh,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'vase.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'vase.blend'));s=bpy.context.scene;body=bpy.data.objects['Complete hollow vase'];updates=[]
bevel=body.modifiers['Small fused pottery root edge'];bevel.show_viewport=False;bevel.show_render=False
for label,sign in [('right',1),('left',-1)]:
 source=bpy.data.objects[f'Editable {label} pottery handle'];operand=bpy.data.objects[f'{label} joined handle operand'];points=source.data.splines[0].bezier_points
 for k in [0,len(points)-1]:points[k].co.x-=sign*.45
 bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(source.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(e.is_manifold for e in bm.edges);bm.to_mesh(mesh);bm.free();operand.data=mesh;updates.append(dict(side=label,root_inward_translation=.45,points=[list(p.co) for p in points]))
clay=bpy.data.materials['Neutral canyon pottery'];slip=bpy.data.materials['Decorative slip - source detail ownership']
for material,values in [(clay,(.24,.58,.86)),(slip,(.18,.40,.68))]:
 ramp=next(n for n in material.node_tree.nodes if n.type=='VALTORGB')
 for e,value in zip(sorted(ramp.color_ramp.elements,key=lambda e:e.position),values):e.color=(value,)*3+(1,)
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for lineset in list(fs.linesets):fs.linesets.remove(lineset)
contours=bpy.data.collections.new('Selected pottery contour');s.collection.children.link(contours);contours.objects.link(body)
ls=fs.linesets.new('Pottery silhouette and open rim');ls.select_by_collection=True;ls.collection=contours;ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.015,.015,.015);ls.linestyle.thickness=2.0;ls.linestyle.caps='ROUND'
bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();mesh=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);bm=bmesh.new();bm.from_mesh(mesh);seen=set();components=0
for v in bm.verts:
 if v in seen:continue
 components+=1;todo=[v];seen.add(v)
 while todo:
  v=todo.pop()
  for edge in v.link_edges:
   other=edge.other_vert(v)
   if other not in seen:seen.add(other);todo.append(other)
audit=dict(connected_components=components,nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),zero_area_faces=sum(f.calc_area()<1e-10 for f in bm.faces));bm.free();write('evaluated-shape-audit.json',audit);assert audit==dict(connected_components=1,nonmanifold_edges=0,zero_area_faces=0),audit
s.camera=bpy.data.objects['Hollow pottery construction diagnostic'];s.render.filepath=str(HERE/'stage-03-refined-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera'];s.render.filepath=str(HERE/'raw-neutral-master.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Primary holdout for independent decorative slip');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);body.data.materials[0]=hold
for label in ['right','left']:
 ob=bpy.data.objects[f'{label} joined handle operand']
 for slot in ob.material_slots:slot.material=hold
s.render.use_freestyle=False;s.render.filepath=str(HERE/'raw-slip-pass.png');bpy.ops.render.render(write_still=True)
body.data.materials[0]=clay
for label in ['right','left']:
 for slot in bpy.data.objects[f'{label} joined handle operand'].material_slots:slot.material=clay
s.render.use_freestyle=True
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'vase.blend'),hidden_root_correction=updates,bevel_disposition='Disabled the optional root-edge bevel after prefix diagnostics isolated99 zero-area faces to that modifier; hollow wall and both handle unions themselves have none.',material_finish='Neutral3tone clay and separate slip material on the two source-supported bands, actual Blender silhouette contour.',source_selection='Direct Blender output preserves handles/rim/slip. No ImageGen is needed for the simple pottery material; no isolation call.',new_imagegen_call=False,native_activation=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'vase.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'vase.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,new_imagegen_call=False,native_activation=False))
