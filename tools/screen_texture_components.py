"""Nonvisual file/neutral-plane diagnostics for the retrospective art review."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'evidence/texture-review-20261021'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
inventory=read(HERE/'inventory.json');ledger=read(ROOT/'evidence/conversion-ledger.json');byid={e['id']:e for e in ledger['entries']}
rows={};hash_mismatches=[]
for item in inventory['sets']:
 for ref in item['component_textures']:
  path=ref['path']
  if path in rows:continue
  p=ROOT/path;raw=p.read_bytes();digest=hashlib.sha256(raw).hexdigest()
  if digest!=ref['sha256']:hash_mismatches.append(path)
  im=Image.open(p);a=np.array(im.convert('RGBA'));visible=a[:,:,3]>0
  rgb=a[:,:,:3];chromatic=np.ptp(rgb.astype(int),axis=2)>0
  neutral_named='neutral' in p.name.lower()
  rows[path]=dict(sha256=digest,mode=im.mode,size=list(im.size),visible_pixels=int(visible.sum()),chromatic_visible_pixels=int((chromatic&visible).sum()),nonzero_hidden_rgb_pixels=int(((rgb.max(2)>0)&~visible).sum()),neutral_named=neutral_named)
models=[];aggregate_links=[]
for item in inventory['sets']:
 e=byid[item['entry']];model=read(ROOT/item['model']['path']);decl=(e.get('current_registration') or {}).get('model')
 if decl and decl.get('sha256')!=item['model']['sha256']:hash_mismatches.append(item['model']['path'])
 mismatches=[]
 def walk(v):
  if isinstance(v,dict):
   if isinstance(v.get('path'),str) and v['path'] in rows and v.get('sha256') and rows[v['path']]['sha256']!=v['sha256']:mismatches.append(v['path'])
   if v.get('public_file') in rows and v.get('sha256') and rows[v['public_file']]['sha256']!=v['sha256']:mismatches.append(v['public_file'])
   for x in v.values():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(model)
 models.append(dict(entry=e['id'],stored_texture_hash_mismatches=sorted(set(mismatches))))
 if e['id'].startswith('ITEM-'):
  for fitting in model.get('fittings',[]):
   ident=fitting.get('entry');expected=(byid.get(ident,{}).get('current_registration') or {}).get('model');actual=(fitting.get('registration') or {}).get('model') or fitting.get('model')
   aggregate_links.append(dict(item=e['id'],fitting=ident,selected_model=actual,current_fit_model=expected,matches_current=(expected==actual) if expected and actual else None))
out=dict(recorded_at=datetime.now(timezone.utc).isoformat(),scope='File and pixel diagnostics only; NOT a visual structural review or native validation.',file_count=len(rows),inventory_hash_mismatches=hash_mismatches,models=models,aggregate_links=aggregate_links,neutral_named_chromatic_files=[p for p,x in rows.items() if x['neutral_named'] and x['chromatic_visible_pixels']],files=rows)
(HERE/'component-diagnostics.json').write_bytes((json.dumps(out,indent=2,ensure_ascii=False)+'\n').encode())
print(json.dumps(dict(files=len(rows),hash_mismatches=hash_mismatches,models_with_stale_texture_refs=[x for x in models if x['stored_texture_hash_mismatches']],neutral_named_chromatic_files=out['neutral_named_chromatic_files'],aggregate_model_mismatches=[x for x in aggregate_links if x['matches_current'] is False]),indent=2))
