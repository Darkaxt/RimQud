"""Append this actual Door authoring run once; preserve native acceptance gate."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];ledger=ROOT/'evidence/conversion-ledger.json'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def files(*names):return [asset(HERE/n) for n in names]
j=json.loads(ledger.read_text(encoding='utf-8'));e=next(x for x in j['entries'] if x['id']=='SCN-DOOR');assert not e['process_log'] and j['active_entry']==e['id']
def event(step,phase,action,inputs,outputs,review,result='PASS',**extra):
 e['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,phase=phase,action=action,inputs=files(*inputs),outputs=files(*outputs),review=review,result=result,**extra))
event(e['required_steps'][0],'Actual source identity, slate description and runtime states',
 'Read the exact Door blueprint and installed Door class defaults/ObjectCreated/open/close behavior. Extracted the static thumbnail and both actual runtime tiles privately.',
 ['source-packet.json'],['source-packet.json','extract-native-states.py','native-state-index.json','native-states-comparison.png'],
 'Viewed all three decoded source glyphs. Static sw_doorclosed is not the normal synchronized runtime tile. Closed is basic; open is basic_open. Runtime arch uses detail and slab uses foreground; both are y. Native source, selectors and state ownership are explicit.')
event(e['required_steps'][1],'Actual RimWorld rendering reference with a limited role',
 'Selected extracted Core DoorSimple_Mover source id2541 as a planar shading/handle-readability reference; documented that it is not an arched slate equivalent.',
 ['source-packet.json'],['source-construction-comparison.png'],
 'Viewed actual private Core door.png and its recorded manifest/hash. Did not adopt wooden material, rectangular outline, sliding animation or donor mechanics.')
event(e['required_steps'][2],'Editable slate leaf, surround and open-edge construction',
 'Constructed the native arched surround and slate slab, left hinge wear and right L-shaped recessed handle as explicit editable geometry.',
 ['source-packet.json','native-state-index.json'],['prepare-and-construct.py','constructed-closed.svg','constructed-closed.png','constructed-open.svg','constructed-open.png','constructed-leaf.svg','constructed-leaf.png','constructed-frame.svg','constructed-frame.png','source-construction-comparison.png'],
 'Viewed manual comparison and full closed image. Shape, relative placement, native cell proportions and slate identity follow source; hand wear is restrained. Later unrelated invalid XML character references were avoided by parsing the exact valid Door object block.')
event(e['required_steps'][3],'Open and closed views from one unchanged frame',
 'Derived the open edge at the actual source left strip from the selected slate material and manual source-coordinate coverage. Kept the arch byte-identical between states.',
 ['constructed-open.png','refined-proposal.png'],['registered/states-comparison.png'],
 'Viewed selected states at enlarged and16x24/24x36/32x48sizes. The surround and anchor stay fixed. The open strip has no squeezed front handle. No creature turnarounds or clothing apply to this fixed source door; actual native selector/occlusion remains native.')
event(e['required_steps'][4],'One controlled closed-door material refinement',
 'Used built-in ImageGen once with the manual closed door and actual Core panel; retained its slate, hinge wear and handle while supplying finer material/edge rendering.',
 ['refine-closed-prompt.txt','constructed-closed.png','source-packet.json'],['refine-closed-prompt.txt','refined-proposal.png'],
 'Viewed generated output and inspected actual alpha. Apparent exterior glow in the tool preview is primarily invisible RGB, not opaque surroundings. The arch and leaf remain separate connected alpha components. Final extraction clears invisible RGB and enforces neutral equal RGB.',
 tool='image_gen.imagegen',settings=dict(transparent_background=True,referenced_image_paths=[str(HERE/'constructed-closed.png'),'E:/Temp/qud-transplant-probe-pawns-20261019/donor/door.png']),
 generation_file='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-20dd7e5d-cd2e-4931-be9b-0f98bde31cab.png')
event(e['required_steps'][5],'Actual refined component extraction and state registration',
 'Selected the arch and slab by connected alpha, removed unowned pixels, normalized interiors and grayscale, then saved neutral foreground/detail components and coverage per state in one frame.',
 ['refined-proposal.png','constructed-open.png'],['register-door.py','registered/model.json','registered/registration-decisions.json','registered/source-selection-frame.png','registered/source-selection-leaf.png','registered/cleaned-frame.png','registered/cleaned-leaf.png','registered/open-edge-neutral-master.png']+[f'registered/{s}-{c}-{kind}.png' for s in ['closed','open'] for c in ['leaf','frame'] for kind in ['neutral','coverage']],
 'Actual saved state arch bytes match exactly, full-canvas mapping/anchor is shared and open leaf remains in the native left strip. Leaf/arch preserve independent native color roles; no baked rust hue, background fill or isolated per-state bounding-box fit.')
event(e['required_steps'][6],'Slate identity, palette, cut edges and intended-size review',
 'Inspected the assembled neutral and actual native-y states and their intended-cell previews.',
 ['registered/model.json'],['registered/states-comparison.png','registered/closed-neutral-composition.png','registered/open-neutral-composition.png','registered/closed-native-preview.png','registered/open-native-preview.png'],
 'Closed is a weathered arched slate panel, open exposes the background around its left edge-on leaf. Shared surround does not move; gaps remain transparent. This is authoring review, not a game-state or native movement test.')
event(e['required_steps'][7],'Native Door acceptance deferred',
 'Recorded exact selector, native visibility/solid/occlusion and replacement dispatch as pending the final all-conversions-generated gate.',
 ['registered/model.json'],[],
 'No game launch, renderer/harness modification or native acceptance. Overall entry remains UNFINISHED.',result='DEFERRED UNTIL ALL GENERATED')
e.update(status='UNFINISHED',current_step=None,generation_ready=True,native_acceptance='Pending final all-conversions validation gate',
 current_registration=dict(model=asset(HERE/'registered/model.json'),plate=asset(HERE/'registered/states-comparison.png')),
 registration_summary='Selected source-faithful slate Door states: one byte-identical arched surround, a closed worn slab and a source-positioned left edge when open. Runtime Door tiles supersede the old blueprint thumbnail. Neutral leaf/arch preserve foreground/detail ownership and native y colors; state/solid/occlusion acceptance remains pending.')
next_entry=next(x for x in j['entries'] if x['id']=='SCN-RUSTEDMETALWALL');assert next_entry['status']=='UNFINISHED' and not next_entry.get('generation_ready')
next_entry.update(status='IN PROGRESS',current_step=next_entry['required_steps'][0]);j['active_entry']=next_entry['id']
ledger.write_bytes((json.dumps(j,indent=2,ensure_ascii=False)+'\n').encode())
print('Door authoring ready; total',sum(bool(x.get('generation_ready')) for x in j['entries']),'next',j['active_entry'])
