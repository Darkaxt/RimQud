"""Confirm the selected reused model and calibrated proxy are editable after reopen."""
from pathlib import Path
from datetime import datetime,timezone
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
bpy.ops.wm.open_mainfile(filepath=str(HERE/'horns-fit.blend'))
receipt=json.loads((HERE/'blender-receipt.json').read_text());horns=[bpy.data.objects[n] for n in ['Left horn','Right horn']]
hashes={o.name:hashlib.sha256(b''.join(float(c).hex().encode()+b';' for v in o.data.vertices for c in v.co)).hexdigest() for o in horns}
assert hashes==receipt['horn_mesh_coordinate_hashes'];proxy=next(o for o in bpy.data.objects if o.name.startswith('Calibrated head-only fit proxy'));assert len(proxy.data.vertices)>0
out=dict(recorded_at=datetime.now(timezone.utc).isoformat(),blend=ref(HERE/'horns-fit.blend'),reopened=True,blender_version=bpy.app.version_string,horn_mesh_coordinate_hashes=hashes,head_proxy=dict(object_name=proxy.name,vertices=len(proxy.data.vertices),faces=len(proxy.data.polygons),controls=ref(HERE/'head-proxy-controls.json'),body=receipt['body_model']),cameras=[dict(name=o.name,type=o.data.type,ortho_scale=o.data.ortho_scale) for o in bpy.data.objects if o.type=='CAMERA'],external_libraries=[dict(name=l.name,file_name=Path(l.filepath).name) for l in bpy.data.libraries],scope='Editable-file verification only; generation fit review is separate and native acceptance pending.')
(ROOT/'evidence/blender-shape-reopen-audit-v2.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Selected model reopens; unchanged horn coordinates and calibrated head proxy verified.',flush=True)
