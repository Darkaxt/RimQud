"""Resume proven shared physical sign geometry; record exact manual-image reuse."""
from pathlib import Path
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=ROOT/'art/conversion/scn-argyvesign/blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'sign.blend').exists();source=json.loads((HERE/'source-packet.json').read_text());assert source['physical_shape_reuse']['source_model']==ref(OLD/'sign.blend')
bpy.ops.wm.open_mainfile(filepath=str(OLD/'sign.blend'));bpy.context.preferences.filepaths.save_version=0
controls=json.loads((OLD/'model-controls.json').read_text());controls['source']=ref(HERE/'source-packet.json');controls['resumed_shared_geometry']=source['physical_shape_reuse'];write('model-controls.json',controls)
for n in ['stage-02-model-3d.png','manual-neutral-master.png']:(HERE/n).write_bytes((OLD/n).read_bytes())
write('reuse-receipt.json',dict(source_model=ref(OLD/'sign.blend'),manual_images=[dict(original=ref(OLD/n),reused=ref(HERE/n)) for n in ['stage-02-model-3d.png','manual-neutral-master.png']],new_render=False,reason=source['physical_shape_reuse']['reason']))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'sign.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'sign.blend'),controls=ref(HERE/'model-controls.json'),scope='Shared unchanged physical plaque/support model saved for mill-sign glyph refinement; manual images explicitly reused by hash.',new_render=False,native_activation=False))
