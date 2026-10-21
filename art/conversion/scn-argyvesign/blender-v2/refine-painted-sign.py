"""Resume the physical plaque; add source-positioned dark paint and restrained edges."""
from pathlib import Path
import bpy,json,hashlib,math
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'sign.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'sign.blend'));s=bpy.context.scene;source=json.loads((OLD/'source-packet.json').read_text());board=bpy.data.objects['Complete terracotta plaque'];contours=bpy.data.collections.new('Sign physical outline');s.collection.children.link(contours)
for ob in [board,bpy.data.objects['Rear upright 4'],bpy.data.objects['Rear upright 12']]:
 bevel=ob.modifiers.new('Small hand-finished edge bevel','BEVEL');bevel.width=.075 if ob==board else .06;bevel.segments=3;bevel.limit_method='ANGLE';contours.objects.link(ob)
paint=bpy.data.materials.new('Dark source pictogram paint - detail r');paint.use_nodes=True;n=paint.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(.025,.025,.025,1);o=n.new('ShaderNodeOutputMaterial');paint.node_tree.links.new(em.outputs[0],o.inputs[0]);vertices=[];faces=[]
for cell in source['glyph_translation']['cells']:
 x,y=cell['x'],cell['y'];start=len(vertices);vertices.extend([(x,-.279,24-y),(x+1,-.279,24-y),(x+1,-.279,23-y),(x,-.279,23-y)]);faces.append(tuple(range(start,start+4)))
mesh=bpy.data.meshes.new('Literal source-positioned negative-space pictogram paint');mesh.from_pydata(vertices,[],faces);mesh.update();glyph=bpy.data.objects.new('Front-only source pictogram paint',mesh);s.collection.objects.link(glyph);mesh.materials.append(paint)
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Plaque and two supports');ls.select_by_collection=True;ls.collection=contours;ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.018,.018,.018);ls.linestyle.thickness=1.8;ls.linestyle.caps='ROUND'
root=bpy.data.objects.new('Sign shared physical pivot',None);s.collection.objects.link(root);root.location=(8,0,0);bpy.context.view_layer.update()
for ob in list(s.objects):
 if ob.type=='MESH':ob.parent=root;ob.matrix_parent_inverse=root.matrix_world.inverted()
s.camera=bpy.data.objects['Plaque and rear-support diagnostic'];s.render.filepath=str(HERE/'stage-03-refined-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera'];supports=[bpy.data.objects['Rear upright 4'],bpy.data.objects['Rear upright 12']];support_mat=supports[0].data.materials[0]
hold=bpy.data.materials.new('Primary-support ownership holdout');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0])
for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:
 root.rotation_euler.z=angle;s.render.filepath=str(HERE/f'{facing}-neutral-master.png');bpy.ops.render.render(write_still=True)
 for ob in supports:ob.data.materials[0]=hold
 s.render.use_freestyle=False;s.render.filepath=str(HERE/f'{facing}-detail-pass.png');bpy.ops.render.render(write_still=True)
 for ob in supports:ob.data.materials[0]=support_mat
 s.render.use_freestyle=True
root.rotation_euler.z=0;bpy.context.view_layer.update();controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'sign.blend'),glyph=dict(source_cells=len(source['glyph_translation']['cells']),paint_plane_y=-.279,method=source['glyph_translation'],front_only=True,rear='Blank clay face behind actual rear uprights; no mirrored pictogram.'),edge_bevels=dict(board=.075,posts=.06,segments=3),facings=dict(south=0,east=-90,north=180),source_selection='Direct retained Blender slab/support geometry and literal source-cell matte paint. No ImageGen or isolation call.',production_view='South original map tile; E/N are retained authoring geometry/mask exports only.',new_imagegen_call=False,native_activation=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'sign.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'sign.blend'),controls=ref(HERE/'model-controls.json'),actual_views=['south','east','north'],new_imagegen_call=False,native_activation=False))
