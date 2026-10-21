"""Inspect retained editable curves and actual body-relative attachment distances."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
from mathutils.geometry import interpolate_bezier
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
bpy.ops.wm.open_mainfile(filepath=str(HERE/'vines.blend'));controls=json.loads((HERE/'model-controls.json').read_text());checks=[]
for layout in controls['source_layouts']:
    n=layout['variant'];samples=[]
    for k,path in enumerate(layout['vine_paths']):
        ob=bpy.data.objects[f'Variant{n} continuous vine{k}'];ps=ob.data.splines[0].bezier_points
        for a,b in zip(ps[:-1],ps[1:]):samples+=list(interpolate_bezier(a.co,a.handle_right,b.handle_left,b.co,257))
        for sign in [-1,1]:
            root=bpy.data.objects[f'Variant{n} attached basal tendril{k} {sign}'];distance=(root.data.splines[0].bezier_points[0].co-ps[0].co).length
            assert distance<=ob.data.bevel_depth+root.data.bevel_depth
            checks.append(dict(variant=n,kind='basal_overlap',stem=k,sign=sign,centerline_distance=distance,combined_radii=ob.data.bevel_depth+root.data.bevel_depth))
    for k,pad in enumerate(layout['wafer_marks']):
        wafer=bpy.data.objects[f'Variant{n} moisture swollen wafer{k}'];x,y=pad['center'];assert (wafer.location-Vector((x,-.12,24-y))).length<1e-5
        tether=bpy.data.objects[f'Variant{n} wafer tether{k}'];q=tether.data.splines[0].bezier_points[0].co;distance=min((q-p).length for p in samples);assert distance<.03
        checks.append(dict(variant=n,kind='tether_stem_overlap',wafer=k,distance_to_dense_stem_samples=distance,stem_radius=.16))
camera=bpy.data.objects['Source fixed map camera'];assert camera.data.type=='ORTHO' and camera.data.ortho_scale==24
out=dict(reopened=True,blend=dict(path=(HERE/'vines.blend').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/'vines.blend').read_bytes()).hexdigest()),checks=checks,
    source_wafer_positions_unchanged=True,source_variant_count=3,native_acceptance='Pending full generation gate; numeric overlap does not replace visual authoring inspection')
(HERE/'reopen-audit.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('Saved model reopens; basal overlaps, curved-stem tether contact and source wafer positions verified.')
