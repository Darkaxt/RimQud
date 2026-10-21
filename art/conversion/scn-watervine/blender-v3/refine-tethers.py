"""Resume saved plant shapes and attach tethers to evaluated curved stems."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import interpolate_bezier
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
bpy.ops.wm.open_mainfile(filepath=str(OLD/'vines.blend'));s=bpy.context.scene
controls=json.loads((OLD/'model-controls.json').read_text());changes=[];groups={}
def closest(p,segments):
    best=None;distance=1e9
    for a,b in segments:
        d=b-a;t=max(0,min(1,(p-a).dot(d)/d.length_squared));q=a+d*t;dist=(q-p).length_squared
        if dist<distance:best=q;distance=dist
    return best
for layout in controls['source_layouts']:
    n=layout['variant'];objects=[o for o in s.objects if o.name.startswith(f'Variant{n} ')];stems=[o for o in objects if 'moisture swollen wafer' not in o.name];segments=[]
    for ob in objects:
        if 'continuous vine' not in ob.name:continue
        ps=ob.data.splines[0].bezier_points
        for a,b in zip(ps[:-1],ps[1:]):
            points=interpolate_bezier(a.co,a.handle_right,b.handle_left,b.co,65);segments+=list(zip(points[:-1],points[1:]))
    for k,pad in enumerate(layout['wafer_marks']):
        x,y=pad['center'];p=Vector((x,0,24-y));q=closest(p,segments);ob=bpy.data.objects[f'Variant{n} wafer tether{k}'];ps=ob.data.splines[0].bezier_points
        before=list(ps[0].co);ps[0].co=q;ps[1].co=((q.x+x)/2,-.04,(q.z+24-y)/2-.12)
        for b in ps:b.handle_left_type='AUTO';b.handle_right_type='AUTO'
        changes.append(dict(variant=n,wafer=k,previous_anchor=before,curved_stem_anchor=list(q),distance_to_evaluated_stem=0))
    groups[n]=(objects,stems)
front=bpy.data.objects['Source fixed map camera'];diagnostic=bpy.data.objects['3D diagnostic only']
# The transient pass material had no users when v2 was saved. Recreate that
# render-pass material explicitly; all retained object geometry stays loaded.
hold=bpy.data.materials.new('Stem holdout for wafer ownership');hold.use_nodes=True
nodes=hold.node_tree.nodes;nodes.clear();h=nodes.new('ShaderNodeHoldout');o=nodes.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0])
for n,(objects,stems) in groups.items():
    for key,group in groups.items():
        for ob in group[0]:ob.hide_render=key!=n
    s.camera=diagnostic;s.render.filepath=str(HERE/f'stage-02-model-variant-{n}.png');bpy.ops.render.render(write_still=True)
    s.camera=front;s.render.filepath=str(HERE/f'variant-{n}-neutral-master.png');bpy.ops.render.render(write_still=True)
    original={ob:ob.data.materials[0] for ob in stems}
    for ob in stems:ob.data.materials[0]=hold
    s.render.use_freestyle=False;s.render.filepath=str(HERE/f'variant-{n}-wafer-master.png');bpy.ops.render.render(write_still=True);s.render.use_freestyle=True
    for ob,m in original.items():ob.data.materials[0]=m
for n,group in groups.items():
    for ob in group[0]:ob.hide_render=n!=1
s.camera=front
controls.update(resumed_from=ref(OLD/'vines.blend'),tether_anchor_correction='Attach to actual evaluated Bezier stem, not straight control chords.',tether_changes=changes)
write('model-controls.json',controls)
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'vines.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'vines.blend'),controls=ref(HERE/'model-controls.json'),variants=[1,2,3],
    resumed_geometry=True,changed='Tether anchor and middle control point only; main stems, wafers, basal roots and source frame unchanged.',native_activation=False))
