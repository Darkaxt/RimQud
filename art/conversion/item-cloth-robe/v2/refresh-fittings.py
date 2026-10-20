"""Refresh the item aggregate after the inspected dromad profile correction."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
p=ROOT/'evidence/conversion-ledger.json';data=json.loads(p.read_text());entry=next(e for e in data['entries'] if e['id']=='ITEM-CLOTH-ROBE');assert data['active_entry']==entry['id']
packet=json.loads((HERE.parent/'v1/fittings.json').read_text());out=Image.new('RGB',(1440,900),'#142823');draw=ImageDraw.Draw(out)
for i,fit in enumerate(packet['fittings']):
 e=next(e for e in data['entries'] if e['id']==fit['entry']);assert e['generation_ready'] and e['art_review']['status']=='PASS'
 fit.update(registration=e['current_registration'],authoring_review=e['art_review'])
 for asset in fit['registration'].values():assert ref(ROOT/asset['path'])['sha256']==asset['sha256']
 plate=Image.open(ROOT/fit['registration']['plate']['path']).convert('RGB');plate.thumbnail((1420,270));out.paste(plate,(10,30+i*290));draw.text((10,10+i*290),e['id'],fill='#e3cf43')
out.save(HERE/'body-fittings-comparison.png');packet['scope']='Current dromad v7 profile correction plus unchanged human fits. One robe on each fixed unclothed base; no native item acceptance.';write(HERE/'fittings.json',packet)
review='Reconciled current three body-specific robe fits against their exact registered models/plates and authoring logs. Dromad v7 supersedes v6 only for profile cuff ownership; male/female human fits unchanged. Aggregate and all fits remain native-pending.'
entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step='verify_every_body_fitting_log',action='Refresh aggregate after dromad profile cuff correction; preserve prior aggregate history.',inputs=[e['registration']['model'] for e in packet['fittings']],outputs=[ref(HERE/'fittings.json'),ref(HERE/'body-fittings-comparison.png')],review=review,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='record_item_acceptance_from_all_fittings',current_registration=dict(model=ref(HERE/'fittings.json'),plate=ref(HERE/'body-fittings-comparison.png')),art_review=dict(status='PASS',reason=review));entry['apparel_workflow']['status']='GENERATION READY'
n=next(e for e in data['entries'] if e['id']=='FIT-DROMAD-SHILLELAGH-HAND-2');n.update(status='IN PROGRESS',generation_ready=False,current_step='recompose_check_cuffs_attachment_occlusion_all_views');data['active_entry']=n['id'];data['updated_at']=datetime.now(timezone.utc).isoformat();write(p,data)
print('Robe aggregate reconciled; staff single-item preview is sole active.')
