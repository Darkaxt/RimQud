"""Open the retained preferred .blend; replace only the inaccurate head proxy."""
from pathlib import Path
from datetime import datetime,timezone
import bpy,json,hashlib,math
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-trial-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
controls=json.loads((HERE/'head-proxy-controls.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(OLD/'horns-trial.blend'))
scene=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0
skull=next(o for o in bpy.data.objects if 'Authored skull proxy' in o.name)
old_material=skull.data.materials[0];holdout=bpy.data.materials.get('Head occlusion only - full item retained separately')
if holdout is None:
    holdout=bpy.data.materials.new('Head occlusion only - full item retained separately');holdout.use_nodes=True
    ns=holdout.node_tree.nodes;ns.clear();h=ns.new('ShaderNodeHoldout');out=ns.new('ShaderNodeOutputMaterial');holdout.node_tree.links.new(h.outputs[0],out.inputs[0])
verts=[];faces=[];sides=48
for y,cx,rx,cz,rz in controls['cross_sections']:
    for k in range(sides):
        a=k*2*math.pi/sides;verts.append(((cx+rx*math.cos(a))/100,-(cz+rz*math.sin(a))/100,-y/100))
for j in range(len(controls['cross_sections'])-1):
    for k in range(sides):
        i=j*sides+k;n=j*sides+(k+1)%sides;faces.append((i,n,n+sides,i+sides))
faces.extend([tuple(reversed(range(sides))),tuple((len(controls['cross_sections'])-1)*sides+k for k in range(sides))])
mesh=bpy.data.meshes.new('Head visual hull from accepted cardinal silhouettes');mesh.from_pydata(verts,[],faces);mesh.update()
skull.data=mesh;skull.location=(0,0,0);skull.scale=(1,1,1);skull.name='Calibrated head-only fit proxy - body pixels unchanged';mesh.materials.append(old_material)
for p in mesh.polygons:p.use_smooth=True
skull['source_body']=controls['body_model']['sha256'];skull['limitations']=controls['limits']
horns=[o for o in bpy.data.objects if o.name in ['Left horn','Right horn']]
before={o.name:hashlib.sha256(b''.join(float(c).hex().encode()+b';' for v in o.data.vertices for c in v.co)).hexdigest() for o in horns}
scene.render.resolution_x=900;scene.render.resolution_y=900;scene.camera=bpy.data.objects['DIAGNOSTIC three-quarter - not production'];skull.hide_render=False
scene.render.filepath=str(HERE/'stage-02-calibrated-model.png');bpy.ops.render.render(write_still=True)
scene.render.resolution_x=768;scene.render.resolution_y=1152
outputs=[]
for face in ['south','east','north','west']:
    scene.camera=bpy.data.objects[face.upper()+' - fixed768x1152']
    # Full item contains no proxy and is byte-reused, not redrawn or rescaled.
    p=HERE/f'whole-item-{face}.png';p.write_bytes((OLD/f'whole-item-{face}.png').read_bytes());outputs.append(ref(p))
    for mode in ['with-skull','visible-item']:
        skull.hide_render=False;skull.data.materials[0]=holdout if mode=='visible-item' else old_material
        p=HERE/f'{mode}-{face}.png';scene.render.filepath=str(p);bpy.ops.render.render(write_still=True);outputs.append(ref(p))
    # Actual proxy coverage, without horn shading or linework, for comparison.
    for o in horns:o.hide_render=True
    skull.data.materials[0]=old_material;scene.render.use_freestyle=False
    p=HERE/f'proxy-silhouette-{face}.png';scene.render.filepath=str(p);bpy.ops.render.render(write_still=True);outputs.append(ref(p))
    for o in horns:o.hide_render=False
    scene.render.use_freestyle=True
after={o.name:hashlib.sha256(b''.join(float(c).hex().encode()+b';' for v in o.data.vertices for c in v.co)).hexdigest() for o in horns};assert before==after
skull.data.materials[0]=old_material;scene.camera=bpy.data.objects['DIAGNOSTIC three-quarter - not production'];scene.render.resolution_x=900;scene.render.resolution_y=900
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'horns-fit.blend'))
receipt=dict(recorded_at=datetime.now(timezone.utc).isoformat(),blender_version=bpy.app.version_string,resumed_blend=ref(OLD/'horns-trial.blend'),body_model=controls['body_model'],controls=ref(HERE/'head-proxy-controls.json'),script=ref(Path(__file__)),blend=ref(HERE/'horns-fit.blend'),horn_mesh_coordinate_hashes=after,horn_meshes_unchanged=True,full_item_images_byte_reused=True,outputs=outputs,frame=[768,1152],body_repainted=False,production_approved=False)
(HERE/'blender-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print('CALIBRATED_PROXY_RENDER_COMPLETE_WITH_UNCHANGED_REUSED_HORNS',flush=True)
