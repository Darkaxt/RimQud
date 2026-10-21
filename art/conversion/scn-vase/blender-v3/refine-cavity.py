"""Make the real hollow interior read as a cavity, preserving complete geometry."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'vase.blend').exists()
bpy.ops.wm.open_mainfile(filepath=str(OLD/'vase.blend'));s=bpy.context.scene;body=bpy.data.objects['Complete hollow vase'];clay=bpy.data.materials['Neutral canyon pottery'];cavity=clay.copy();cavity.name='Recessed pottery cavity - source primary';ramp=next(n for n in cavity.node_tree.nodes if n.type=='VALTORGB')
for e,v in zip(sorted(ramp.color_ramp.elements,key=lambda e:e.position),(.035,.075,.14)):e.color=(v,)*3+(1,)
body.data.materials.append(cavity);changed=0
for face in body.data.polygons:
 radial=Vector((face.center.x-8,face.center.y,0))
 if radial.dot(face.normal)<-.1:face.material_index=2;changed+=1
assert changed>100
s.camera=bpy.data.objects['Hollow pottery construction diagnostic'];s.render.filepath=str(HERE/'stage-03-refined-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=bpy.data.objects['Fixed source map camera'];s.render.filepath=str(HERE/'raw-neutral-master.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Primary holdout for independent decorative slip');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);body.data.materials[0]=hold;body.data.materials[2]=hold
for label in ['right','left']:
 for slot in bpy.data.objects[f'{label} joined handle operand'].material_slots:slot.material=hold
s.render.use_freestyle=False;s.render.filepath=str(HERE/'raw-slip-pass.png');bpy.ops.render.render(write_still=True)
body.data.materials[0]=clay;body.data.materials[2]=cavity
for label in ['right','left']:
 for slot in bpy.data.objects[f'{label} joined handle operand'].material_slots:slot.material=clay
s.render.use_freestyle=True
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'vase.blend'),review_trigger=ref(OLD/'independent-structural-review.json'),cavity_finish=dict(inward_wall_faces=changed,neutral_values=[.035,.075,.14],role='Recessed opaque pottery interior remains primary color; no cap, painted hole or new geometry.',geometry_unchanged=True),new_imagegen_call=False,native_activation=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'vase.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'vase.blend'),controls=ref(HERE/'model-controls.json'),resumed_geometry=True,new_imagegen_call=False,native_activation=False))
