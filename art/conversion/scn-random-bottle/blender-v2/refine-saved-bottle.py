"""Resume the bottle, clean axial vertices and round its actual glass geometry."""
from pathlib import Path
import bpy,bmesh,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
assert not (HERE/'bottle.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'bottle.blend'));s=bpy.context.scene;body=bpy.data.objects['Hollow freeblown glass body'];handle=bpy.data.objects['Connected lunar-arc glass handle'];before=len(body.data.vertices)
bm=bmesh.new();bm.from_mesh(body.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));assert all(f.calc_area()>1e-9 for f in bm.faces);bm.to_mesh(body.data);bm.free()
modifier=body.modifiers.new('Round freeblown bowl and continuous rolled mouth','SUBSURF');modifier.levels=2;modifier.render_levels=2
for ob in bpy.data.objects:
    if ob.name.startswith('Glass glint '):ob.hide_render=True
# Use surface-normal shading on the rounded wall; no separate glint geometry
# needs to be re-fitted when the wall is smoothed.
front=bpy.data.objects['Fixed source map camera'];diag=bpy.data.objects['3D hollow-wall diagnostic']
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'raw-neutral-master.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Transient body ownership holdout');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0])
originals={body:body.data.materials[0],handle:handle.data.materials[0]}
for ob in originals:ob.data.materials[0]=hold
s.render.use_freestyle=False;s.render.filepath=str(HERE/'raw-detail-pass.png');bpy.ops.render.render(write_still=True);s.render.use_freestyle=True
for ob,m in originals.items():ob.data.materials[0]=m
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'bottle.blend'),geometry_refinement=dict(vertices_before=before,vertices_after=len(body.data.vertices),axial_duplicates_welded=True,zero_area_faces=False,subdivision_level=2,
    purpose='Round bowl/shoulder/rolled mouth on the actual hollow model; source neck/handle identity and shared frame retained.'),standalone_glint_curves='Retained but excluded from renders; rounded actual surface normals supply highlights.')
write('model-controls.json',controls)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,new_imagegen_call=False,native_activation=False))
