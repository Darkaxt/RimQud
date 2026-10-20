"""Append the actual source-bound rusted-wall conversion once, without native tests."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];ledger=ROOT/'evidence/conversion-ledger.json'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def files(names):return [asset(HERE/n) for n in names]
j=json.loads(ledger.read_text(encoding='utf-8'));e=next(x for x in j['entries'] if x['id']=='SCN-RUSTEDMETALWALL');assert j['active_entry']==e['id'] and not e['process_log']
def event(step,phase,action,inputs,outputs,review,result='PASS',**extra):e['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,phase=phase,action=action,inputs=files(inputs),outputs=files(outputs),review=review,result=result,**extra))
event(e['required_steps'][0],'Actual painted source shapes and native metal palette',
 'Read RustedMetalWall ancestry, description and native eight-neighbor paint selection. Extracted all256installed wall_metal source masks privately, retaining16cardinal source examples.',
 ['source-packet.json'],['source-packet.json','extract-native-states.py','native-state-index.json','native-states-comparison.png'],
 'Viewed actual r/C source shapes. Earlier tile-0-13 was an inherited placeholder. Source has checker/diamond metal, pale-cyan edging and lower industrial bracing. Native N,NE,E,SE,S,SW,W,NW ordering differs from recipient four-bit order.')
event(e['required_steps'][1],'Actual Core smooth-wall reference with constrained use',
 'Selected extracted Core Wall_Atlas_Smooth source id392 as a shallow metal bevel/material and connected-atlas reference.',
 ['source-packet.json'],['source-construction-comparison.png'],
 'Viewed the actual private320x320Core atlas and recorded manifest/hash. No donor atlas ordering, neutral gray palette or generic solid wall silhouette replaces Qud source geometry/colors.')
event(e['required_steps'][2],'Literal source reconstruction retained as rejected design',
 'Created an explicit editable source-coordinate trace and a separate neutral welded-metal material proposal.',
 ['native-state-index.json','source-packet.json'],['prepare-and-construct.py','constructed-isolated.svg','constructed-isolated.png','constructed-material.svg','constructed-material.png','source-construction-comparison.png'],
 'Viewed original and manual comparison. Literal checker enlargement yields disconnected square marks and is retained as a rejected shape interpretation; this record is not the selected final geometry.',result='RECORDED')
event(e['required_steps'][2],'Source-positioned welded diamond correction',
 'Rebuilt checker nodes as diamond joints and connected diagonal welded strips while preserving source frame/base contours and color ownership. Included terminal joints with only one diagonal neighbor.',
 ['native-state-index.json','constructed-isolated.png'],['construct-geometry.py','source-packet-v2.json','constructed-isolated-v2-primary.svg','constructed-isolated-v2-primary.png','constructed-isolated-v2-detail.svg','constructed-isolated-v2-detail.png','constructed-isolated-v2.png','construction-correction-comparison.png'],
 'Viewed correction plate and selected all-state/connection plates. Fine mesh construction is an explicit authored interpretation of tiny source checker marks; it is not presented as exact native alpha. Native physical occlusion remains independent.')
event(e['required_steps'][3],'All256native layouts and sixteen cardinal recipient layouts',
 'Applied the same source-coordinate geometry procedure and fixed material phase to every native painted suffix, then packed the16cardinal states in recipient bottom-origin order.',
 ['source-packet-v2.json','native-state-index.json','construct-geometry.py'],['registered/states-comparison.png','registered/all-native-states-comparison.png','registered/primary-cardinal-atlas.png','registered/detail-cardinal-atlas.png'],
 'Viewed all256contact-sheet states and16cardinal examples. Frame/base shapes and color roles follow their actual state; no independent alpha-bounds centering or added cell-edge caps. No creature turnarounds or clothing apply.')
event(e['required_steps'][4],'One controlled neutral metal material refinement',
 'Used built-in ImageGen once on the editable square welded-metal swatch with actual Core smooth-wall shading reference; geometry and source tint ownership remain deterministic.',
 ['refine-material-prompt.txt','constructed-material.png','source-packet.json'],['refine-material-prompt.txt','refined-proposal.png'],
 'Viewed the generated opaque grayscale metal surface with diamond seams, scratches, scorches and pitting. It supplies material only, not wall topology or unobserved physical behavior. Opposite material edges receive a recorded seam patch before registration.',
 tool='image_gen.imagegen',settings=dict(transparent_background=False,referenced_image_paths=[str(HERE/'constructed-material.png'),'E:/Temp/qud-transplant-probe-pawns-20261019/donor/wall-metal.png']),
 generation_file='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-c8d2778e-b32c-40e6-bff2-c0fee245282e.png')
event(e['required_steps'][5],'Neutral source-role layers and coverage in one fixed frame',
 'Matched opposite material borders, restrained luminance, applied constructed coverage and shallow edge bevel, and saved primary/detail/coverage for all256states with an exact selected model index.',
 ['refined-proposal.png','source-packet-v2.json','construct-geometry.py'],['register-wall.py','registered/registration-decisions.json','registered/patched-seamless-material.png','registered/model.json','registered/primary-cardinal-atlas.png','registered/detail-cardinal-atlas.png'],
 'All state assets are referenced with exact hashes in selected model.json. Primary is rust-metal r; detail is pale-cyan C. Both are neutral grayscale RGBA. Shared16x24source frame maps to256x256recipient textures; native source coordinates control relative placement.')
event(e['required_steps'][6],'Native palette, intended-size and connected-shape authoring review',
 'Composed source-native r/C states in a connected enclosure, corners, T junction and opening, and inspected enlarged and16x24cell previews.',
 ['registered/model.json'],['registered/connections-comparison.png','registered/native-scale-comparison.png','registered/states-comparison.png','registered/all-native-states-comparison.png'],
 'Viewed the actual saved plates. Diamond metal and lower bracing join according to source eight-neighbor state; cyan edging follows source contours. No generic mud cap or sand/masonry texture is substituted. Fine mesh remains authored and native visibility/solid/occlusion acceptance is pending.')
event(e['required_steps'][7],'Native wall acceptance deferred',
 'Kept native256state dispatch, recipient atlas UV/sampling, paint/visibility/solid/occlusion and damage/graffiti exceptions behind the all-conversions-generated gate.',
 ['registered/model.json'],[],
 'No game launch, production renderer edits or native/harness tests occurred. Overall entry remains UNFINISHED.',result='DEFERRED UNTIL ALL GENERATED')
e.update(status='UNFINISHED',current_step=None,generation_ready=True,native_acceptance='Pending final all-conversions validation gate',
 current_registration=dict(model=asset(HERE/'registered/model.json'),plate=asset(HERE/'registered/connections-comparison.png')),
 registration_summary='Selected rusted metal with source r/C colors, source-shaped industrial frame/bracing and authored welded diamond mesh at the native checker nodes. All256native eight-neighbor variants and the16cardinal recipient layouts share one coordinate frame. Rejected square trace, material refinement and mesh correction remain below. Native dispatch/visibility/occlusion acceptance is pending.')
n=next(x for x in j['entries'] if x['id']=='SCN-BRINESTALK');assert n['status']=='UNFINISHED' and not n.get('generation_ready');n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);j['active_entry']=n['id']
ledger.write_bytes((json.dumps(j,indent=2,ensure_ascii=False)+'\n').encode());print('Rusted wall generation-ready; total',sum(bool(x.get('generation_ready')) for x in j['entries']),'next',j['active_entry'])
