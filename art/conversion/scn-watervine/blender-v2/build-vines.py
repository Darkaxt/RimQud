"""Source-layout watervines with continuous basal tendrils and attached wafers."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
assert not (HERE/'vines.blend').exists()
packet=json.loads((OLD/'source-packet.json').read_text())
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4
s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG'
s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def toon(name,values):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();links=m.node_tree.links
    geom=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.4,-.8,.5)
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
    a=ramp.color_ramp.elements[0];a.position=0;a.color=(values[0],)*3+(1,)
    b=ramp.color_ramp.elements[1];b.position=.75;b.color=(values[2],)*3+(1,)
    c=ramp.color_ramp.elements.new(.2);c.color=(values[1],)*3+(1,)
    emission=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial')
    links.new(geom.outputs['Normal'],dot.inputs[0]);links.new(dot.outputs['Value'],ramp.inputs[0]);links.new(ramp.outputs[0],emission.inputs[0]);links.new(emission.outputs[0],out.inputs[0]);return m
stemmat=toon('Neutral furrowed vine - primary w',(.14,.42,.66));wafermat=toon('Neutral swollen wafer - detail g or K',(.20,.55,.83))
hold=bpy.data.materials.new('Stem holdout for wafer ownership');hold.use_nodes=True;nodes=hold.node_tree.nodes;nodes.clear();h=nodes.new('ShaderNodeHoldout');o=nodes.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0])
linecol=bpy.data.collections.new('Whole plant contour collection');s.collection.children.link(linecol)
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Plant silhouettes');ls.select_by_collection=True;ls.collection=linecol;ls.collection_negation='INCLUSIVE';ls.select_crease=False
ls.linestyle.color=(.012,.012,.012);ls.linestyle.thickness=1.8;ls.linestyle.caps='ROUND'
def curve(name,points,radius,collection,material=stemmat):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=16;data.bevel_depth=radius;data.bevel_resolution=4;data.resolution_u=12
    spline=data.splines.new('BEZIER');spline.bezier_points.add(len(points)-1)
    for b,p in zip(spline.bezier_points,points):b.co=p;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
    ob=bpy.data.objects.new(name,data);collection.objects.link(ob);data.materials.append(material);linecol.objects.link(ob);return ob
def world(p,depth=0):return (p[0],depth,24-p[1])
def closest(p,segments):
    best=None;distance=1e9
    for a,b in segments:
        d=Vector(b)-Vector(a);t=max(0,min(1,(Vector(p)-Vector(a)).dot(d)/d.length_squared));q=Vector(a)+d*t;dist=(q-Vector(p)).length_squared
        if dist<distance:best=tuple(q);distance=dist
    return best
groups={};basal=[]
for layout in packet['layouts']:
    n=layout['variant'];collection=bpy.data.collections.new(f'Source variant {n}');s.collection.children.link(collection);objects=[];stems=[];wafers=[];segments=[]
    for k,path in enumerate(layout['vine_paths']):
        ob=curve(f'Variant{n} continuous vine{k}',[world(p) for p in path],.16,collection);objects.append(ob);stems.append(ob);segments+=list(zip(path[:-1],path[1:]))
        x,y=path[0]
        # Each creeping tendril starts inside its own stem, not at a copied
        # global y row that might float below that variant's actual endpoint.
        for sign in [-1,1]:
            pts=[(x,y-.12),(x+sign*.4,y+.10),(x+sign*.9,y+.35),(x+sign*1.35,y+.25)]
            ob=curve(f'Variant{n} attached basal tendril{k} {sign}',[world(p,.02) for p in pts],.055,collection);objects.append(ob);stems.append(ob)
            basal.append(dict(variant=n,stem=k,points=pts,stem_start=path[0],authored=True))
        # Restrained highlight follows the same editable centerline as salt in
        # its furrows; it cannot detach from a separately guessed stroke.
        ob=curve(f'Variant{n} salt furrow{k}',[world((x-.025,y),-.157) for x,y in path],.018,collection,wafermat);objects.append(ob);stems.append(ob)
    for k,pad in enumerate(layout['wafer_marks']):
        x,y=pad['center'];r=pad['radius'];q=closest((x,y),segments)
        ob=curve(f'Variant{n} wafer tether{k}',[world(q),world(((q[0]+x)/2,(q[1]+y)/2+.12),-.04),world((x,y),-.08)],.045,collection);objects.append(ob);stems.append(ob)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=world((x,y),-.12));ob=bpy.context.object;ob.name=f'Variant{n} moisture swollen wafer{k}';ob.scale=(r,.13,r*.67)
        for c in list(ob.users_collection):c.objects.unlink(ob)
        collection.objects.link(ob);linecol.objects.link(ob);ob.data.materials.append(wafermat)
        for p in ob.data.polygons:p.use_smooth=True
        objects.append(ob);wafers.append(ob)
    groups[n]=(objects,stems,wafers)
def camera(name,loc,target,scale):
    data=bpy.data.cameras.new(name);data.type='ORTHO';data.ortho_scale=scale;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Source fixed map camera',(8,-40,12),(8,0,12),24);diagnostic=camera('3D diagnostic only',(23,-35,19),(8,0,12),26)
for n,(objects,stems,wafers) in groups.items():
    for key,group in groups.items():
        for ob in group[0]:ob.hide_render=key!=n
    s.camera=diagnostic;s.render.filepath=str(HERE/f'stage-02-model-variant-{n}.png');bpy.ops.render.render(write_still=True)
    s.camera=front;s.render.filepath=str(HERE/f'variant-{n}-neutral-master.png');bpy.ops.render.render(write_still=True)
    original={ob:ob.data.materials[0] for ob in stems}
    for ob in stems:ob.data.materials[0]=hold
    s.render.use_freestyle=False;s.render.filepath=str(HERE/f'variant-{n}-wafer-master.png');bpy.ops.render.render(write_still=True);s.render.use_freestyle=True
    for ob,material in original.items():ob.data.materials[0]=material
for n,(objects,_,_) in groups.items():
    for ob in objects:ob.hide_render=n!=1
s.camera=front
write('model-controls.json',dict(source=ref(OLD/'source-packet.json'),source_layouts=packet['layouts'],basal_tendrils=basal,
    camera=dict(type='ORTHO',location=[8,-40,12],target=[8,0,12],ortho_scale=24,canvas=[512,768]),
    authored_depth='Low relief vines and wafer thickness; source sprite gives no measured depth.',
    frame=[16,24],anchor=[8,16],material='Three neutral normal-based tones, source-bound salt furrow and black contour. No complex painted texture.',
    new_imagegen_call=False,native_acceptance='Pending full generation gate'))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'vines.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'vines.blend'),controls=ref(HERE/'model-controls.json'),variants=[1,2,3],
    complete_geometry=True,wafer_counts={n:len(g[2]) for n,g in groups.items()},new_imagegen_call=False,native_activation=False))
print('Saved three source-bound vine layouts with attached basal curves and separate wafer ownership.')
