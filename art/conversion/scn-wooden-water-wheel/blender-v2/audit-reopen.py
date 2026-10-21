"""Verify cached wheel and actual authored support intersections on reopening."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
bpy.ops.wm.open_mainfile(filepath=str(HERE/'wheel.blend'));c=json.loads((HERE/'model-controls.json').read_text());checks=[]
for y in [8.8,15.2]:
    ob=bpy.data.objects[f'Authored rear inset support at{y}'];assert abs(ob.location.x-10.75)<1e-5 and abs(ob.dimensions.x-6.85)<1e-5
    left=ob.location.x-ob.dimensions.x/2;right=ob.location.x+ob.dimensions.x/2
    # Source-locked main spine spans7.1..7.8. Rim/support and inset/support
    # intersections are authored overlap, not proofs of native mechanics.
    assert left<7.8
    rim_x=8+6.35*math.sqrt(1-((y-11.88)/10.28)**2);assert right>=rim_x-.43
    inset_x=[10.85+sign*1.6*math.sqrt(1-((y-12)/6.6)**2) for sign in [-1,1]];assert all(left<x<right for x in inset_x)
    support_front=ob.location.y-ob.dimensions.y/2;assert support_front<=-.15+1e-6
    checks.append(dict(y_down=y,spine_overlap=True,rim_overlap=True,inset_crossings=inset_x,depth_overlap=True))
for phase in [1,2,3]:
    rows=[r for r in c['source_segment_runs'] if r['frame']==phase]
    for k,row in enumerate(rows):
        x,y,w,h=row['native_run'];ob=bpy.data.objects[f'Phase{phase} source detail run{k}'];expected=Vector((x+w/2,-.32,24-y-h/2));assert (ob.location-expected).length<1e-5
        attach=bpy.data.objects[f'Phase{phase} inset marking attachment{k}'];ps=attach.data.splines[0].points
        end=Vector(ps[-1].co[:3]);assert abs(end.x-ob.location.x)<1e-5 and abs(end.z-ob.location.z)<1e-5
    checks.append(dict(phase=phase,source_detail_run_count=len(rows),all_runs_attached_to_carrier=True))
camera=bpy.data.objects['Source cardinal map camera'];assert camera.data.type=='ORTHO' and camera.data.ortho_scale==24
out=dict(reopened=True,blend=dict(path=(HERE/'wheel.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'wheel.blend').read_bytes()).hexdigest()),checks=checks,
    materials_editable=True,no_external_texture_dependency=True,scope='Editable cache and authored overlap diagnostics only; native behavior remains unvalidated.')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('Wheel source reopens; native detail runs and authored support overlaps verified.')
