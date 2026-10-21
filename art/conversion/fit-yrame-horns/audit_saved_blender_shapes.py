"""Reopen retained .blend files with Blender; verify actual editable contents."""
from pathlib import Path
import bpy,json,hashlib
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
records=[]
for version in ['blender-trial-v1','blender-trial-v2','blender-trial-v3']:
    p=HERE/version/'horns-trial.blend'
    bpy.ops.wm.open_mainfile(filepath=str(p))
    horns=[o for o in bpy.data.objects if o.type=='MESH' and o.name in ['Left horn','Right horn']]
    cams=[o for o in bpy.data.objects if o.type=='CAMERA']
    assert len(horns)==2 and len(cams)==5,(version,len(horns),len(cams))
    assert all(len(o.data.vertices)>0 and len(o.data.polygons)>0 for o in horns)
    deps=[dict(name=l.name,exists=Path(bpy.path.abspath(l.filepath)).exists(),file_name=Path(l.filepath).name) for l in bpy.data.libraries]
    records.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),reopened=True,editable_horns=[dict(name=o.name,vertices=len(o.data.vertices),faces=len(o.data.polygons),materials=[m.name for m in o.data.materials]) for o in horns],cameras=[dict(name=o.name,type=o.data.type,ortho_scale=o.data.ortho_scale) for o in cams],proxy=[o.name for o in bpy.data.objects if 'proxy' in o.name.lower()],external_libraries=deps))
out=dict(recorded_at=datetime.now(timezone.utc).isoformat(),blender_version=bpy.app.version_string,scope='File reopen/editability verification only. Not art or native acceptance.',versions=records)
(ROOT/'evidence/blender-shape-reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n')
print('THREE_BLEND_FILES_REOPENED_WITH_EDITABLE_HORNS_CAMERAS_AND_MATERIALS',flush=True)
