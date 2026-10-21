"""Resume manual pottery, seat hidden roots and finish slip/contours directly."""
from pathlib import Path
import bpy,bmesh,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'vase.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'vase.blend'));s=bpy.context.scene;body=bpy.data.objects['Complete hollow vase'];updates=[]
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

for m in body.modifiers:m.show_viewport=False
for m in body.modifiers:
 m.show_viewport=True;bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();probe=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps)
 bm=bmesh.new();bm.from_mesh(probe);areas=sorted(f.calc_area() for f in bm.faces);print(m.name,'nonmanifold',sum(not e.is_manifold for e in bm.edges),'area<1e-10',sum(a<1e-10 for a in areas),'min',areas[:4]);bm.free()
