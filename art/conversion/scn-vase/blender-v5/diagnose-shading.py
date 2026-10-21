from pathlib import Path
import bpy
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'vase.blend'));m=bpy.data.objects['Complete hollow vase'].data
print('CUSTOM NORMALS',m.has_custom_normals)
print('ATTRIBUTES',[(a.name,a.domain,a.data_type) for a in m.attributes])
a=m.attributes.get('sharp_edge');print('SHARP EDGES',sum(d.value for d in a.data) if a else 0)
print('NORMAL API',[n for n in dir(m) if 'normal' in n or 'sharp' in n])
