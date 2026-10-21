"""Verify the retained editable model, pivot and packed used textures."""
from pathlib import Path
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
bpy.ops.wm.open_mainfile(filepath=str(HERE/'door.blend'))
pivot=bpy.data.objects['Hinge pivot - closed 0 open 90 degrees'];leaf=bpy.data.objects['Complete slate leaf']
assert leaf.parent==pivot and len(leaf.data.vertices)>0
images=[]
for ob in bpy.context.scene.objects:
    if ob.type!='MESH':continue
    for slot in ob.material_slots:
        if not slot.material or not slot.material.use_nodes:continue
        for node in slot.material.node_tree.nodes:
            if node.type=='TEX_IMAGE':
                assert node.image.packed_file;images.append(node.image.name)
camera=bpy.data.objects['Fixed native cardinal camera'];assert camera.data.type=='ORTHO' and camera.data.ortho_scale==24
out=dict(reopened=True,editable_leaf_vertices=len(leaf.data.vertices),pivot=list(pivot.location),parent=leaf.parent.name,used_images_packed=sorted(set(images)),
    blend=dict(path=(HERE/'door.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'door.blend').read_bytes()).hexdigest()),
    version=bpy.app.version_string,scope='Editable source verification, not native behavior acceptance')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('Retained door model reopens with editable pivot/leaf and packed used textures.')
