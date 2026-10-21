"""Preserve actual refinement, independent review and main-author selection."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
now=datetime.now(timezone.utc).isoformat()
review=read(HERE/'independent-style-review.json')
for r in review['images_inspected']:assert ref(HERE/r['path'])['sha256']==r['sha256'],r
decision=dict(recorded_at=now,status='REQUIRES ROOT CORRECTION',review=ref(HERE/'independent-style-review.json'),
 findings=[dict(id='root-contact',disposition='FIX NOW',reason='The visible anterior bone ends are dark-bounded rounded lobes against the forehead. This reading is already present in the model and repeated by AI. Move the emergence to the upper forehead/crown with a continuous outward stem; inspect actual original-head compositions, not only the red ellipsoid or buried-cap metric.'),
 dict(id='detail-loss',disposition='MINOR POLISH / STYLE GUIDANCE ONLY',reason='Simple graphic banding is compatible with user-selected shape-first art. It is not preservation of exact modeled grooves. The candidate remains style guidance while root geometry is corrected.'),
 dict(id='body-repaint',disposition='FIX NOW IF SELECTED',reason='Candidate context differs in framing and body pixels; never use it to replace original head/ears/body. Direct Blender layers and original body stay authoritative.')],
 selected_production_source=None,trial_result='Blender-first is selected by the user as the default for remaining/revised objects. This does not approve the current horn root fit.',
 reviewer=dict(agent='/root/blender_horn_style_review',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override',completed=True),
 next='Correct Blender root emergence before production registration. No new blanket review or generation reset.')
write(HERE/'main-review-decision.json',decision)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
candidate=Image.open(HERE/'context-refinement-raw.png').convert('RGBA');candidate.thumbnail((1600,700))
out=Image.new('RGB',(1600,candidate.height+90),'#142b24');bg=Image.new('RGBA',candidate.size,'#20382d');bg.alpha_composite(candidate);out.paste(bg.convert('RGB'),(0,45));d=ImageDraw.Draw(out);d.text((15,12),'06 / ACTUAL IMAGEGEN STYLE COMPARISON / not selected for registration',font=font,fill='#e3ce43');d.text((15,out.height-28),'Useful flattening; original body stays fixed; root transition still requires model correction.',font=font,fill='#ebeadd');out.save(HERE/'stage-06-imagegen-comparison.png')
page=ROOT/'docs/yrame-horns-blender-trial.html';text=page.read_text(encoding='utf-8');start=text.index('<section id="stage-6">');end=text.index('</section>',start)+len('</section>');r=ref(HERE/'stage-06-imagegen-comparison.png')
replacement=f'<section id="stage-6"><h2>6. Actual ImageGen style comparison</h2><p>One actual call. The user selected Blender-first for remaining/revised objects. This candidate is retained as style guidance; the root transition still blocks horn fitting. The original body is authoritative.</p><a href="../{r["path"]}"><img loading="lazy" src="../{r["path"]}" alt="Actual optional 2D refinement"></a><p><a href="../{ref(HERE/"generation-receipt.json")["path"]}">Exact prompt/call receipt</a> · <a href="../{ref(HERE/"independent-style-review.json")["path"]}">Fresh independent review</a> · <a href="../{ref(HERE/"main-review-decision.json")["path"]}">Main dispositions</a></p></section>'
text=text[:start]+replacement+text[end:];text=text.replace('Not performed for this trial yet.','Performed once.');page.write_text(text,encoding='utf-8',newline='\n')
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='FIT-YRAME-HORNS-HEAD-0';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
entry['process_log'].append(dict(timestamp=now,step='imagegen_refine_in_context_on_unchanged_body',action='Compare actual optional ImageGen style refinement against Blender exports; run a fresh Low-effort independent review, inspect and disposition all findings.',inputs=[ref(HERE/'refinement-input.png'),ref(HERE.parent/'v4/source-reference-construction.png')],outputs=[ref(HERE/p) for p in ['context-refinement-prompt.txt','context-refinement-raw.png','generation-receipt.json','independent-style-review.json','main-review-decision.json','stage-06-imagegen-comparison.png']],review='Principal modeled curl/ear ownership retained; front/rear roots actually occlude differently. Anterior root still reads as a cap, so no production selection or readiness. Style guidance only; original body pixels cannot be replaced.',result='REQUIRES CORRECTION'))
ledger['authoring_policy']=dict(version='blender-first-v1',record=ref(ROOT/'evidence/blender-first-policy-20261021.json'),scope='Remaining and revised non-body assets; body-fit proxies for complements; bodies remain ImageGen-led',transition='Finish existing generation and confirmed defects; keep usable existing art provisional; test the complete set after full generation, then prioritize visible replacements. No blanket invalidation.',readiness_reset=False)
entry['art_review']=dict(status='REQUIRES CORRECTION',reason='Current Blender trial improves shape and physically distinct views; visible anterior root still reads as a blunt cap. Correct actual model emergence before registration.',record=ref(HERE/'main-review-decision.json'));entry['generation_ready']=False;entry['current_step']='construct_and_overlay_one_item';entry['advancement_blocker']['reason']=entry['art_review']['reason'];ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Actual six-stage trial, fresh review and policy recorded. Horn fitting still withheld; no blanket reset.')
