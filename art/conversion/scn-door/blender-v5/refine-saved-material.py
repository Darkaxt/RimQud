"""Resume the saved v4 geometry; replace only its prepared slate surface."""
import bpy,math,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v4'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
bpy.ops.wm.open_mainfile(filepath=str(OLD/'door.blend'))
s=bpy.context.scene;pivot=bpy.data.objects['Hinge pivot - closed 0 open 90 degrees'];arch=bpy.data.objects['Fixed arched slate surround']
image=bpy.data.images.load(str(HERE/'slate-surface-without-old-hardware.png'));image.pack()
material=bpy.data.materials['Retained source slate hand wear - no new AI']
for n in material.node_tree.nodes:
    if n.type=='TEX_IMAGE':n.image=image
front=bpy.data.objects['Fixed native cardinal camera'];diagnostic=bpy.data.objects['Three dimensional diagnostic only']
parts=[o for o in s.objects if o.type=='MESH' and o!=arch]
before={o.name:hashlib.sha256(str([tuple(v.co) for v in o.data.vertices]).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
s.camera=diagnostic;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True);s.camera=front
for state,angle in [('closed',0),('open',90)]:
    pivot.rotation_euler.z=math.radians(angle);bpy.context.view_layer.update()
    for o in [arch]+parts:o.hide_render=False
    s.render.filepath=str(HERE/f'raw-{state}-full.png');bpy.ops.render.render(write_still=True)
    arch.hide_render=True;s.render.filepath=str(HERE/f'raw-{state}-leaf.png');bpy.ops.render.render(write_still=True)
    arch.hide_render=False
    for o in parts:o.hide_render=True
    s.render.filepath=str(HERE/f'raw-{state}-frame.png');bpy.ops.render.render(write_still=True)
    for o in parts:o.hide_render=False
pivot.rotation_euler.z=0;s.camera=front
after={o.name:hashlib.sha256(str([tuple(v.co) for v in o.data.vertices]).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
assert before==after
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'door.blend'),geometry_unchanged=True,material_preparation=ref(HERE/'surface-preparation.json'),material=ref(HERE/'slate-surface-without-old-hardware.png'))
write('model-controls.json',controls)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'door.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'door.blend'),geometry_unchanged=before==after,controls=ref(HERE/'model-controls.json'),textures_packed=True,states=['closed','open'],native_activation=False))
