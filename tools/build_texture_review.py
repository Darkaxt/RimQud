"""Render the requested current-texture critique and main-author dispositions."""
from pathlib import Path
from datetime import datetime,timezone
from html import escape
import hashlib,json
ROOT=Path(__file__).resolve().parents[1];HERE=ROOT/'evidence/texture-review-20261021'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
inventory=read(HERE/'inventory.json');decisions=read(HERE/'main-decisions.json') if (HERE/'main-decisions.json').exists() else {'decisions':[]}
ledger=read(ROOT/'evidence/conversion-ledger.json');current={x['id']:x for x in ledger['entries']}
decisionmap={x['finding']:x for x in decisions['decisions']}
reports={};coverage={};findings=[]
bindingpath=HERE/'review-image-bindings.json'
bindings=read(bindingpath) if bindingpath.exists() else {}
for p in sorted(HERE.glob('review-[0-9]*.json')):
 report=read(p);reports[p.name]=ref(p)
 reportkey=reports[p.name]['sha256']
 for e in report['entries']:
  assert e['entry'] not in coverage,('duplicate visual review',e['entry'])
  assert e['inspected_images'],('no actual viewed image',e['entry'])
  images=[]
  for path in e['inspected_images']:
   image=ROOT/path;assert image.is_file(),path
   key=reportkey+'#'+image.relative_to(ROOT).as_posix()
   actual=ref(image)
   if key in bindings:assert bindings[key]==actual,('Reviewed image changed; fresh review required',path)
   else:bindings[key]=actual
   images.append(bindings[key])
  row=dict(e,report=ref(p),reviewed_images=images)
  for i,f in enumerate(e['findings']):
   key=f'{p.name}#{e["entry"]}:{i}';item=dict(f,entry=e['entry'],finding=key,decision=decisionmap.get(key));findings.append(item)
  coverage[e['entry']]=row
bindingpath.write_bytes((json.dumps(bindings,indent=2,ensure_ascii=False)+'\n').encode())
unreviewed=[x['entry'] for x in inventory['sets'] if x['entry'] not in coverage]
undecided=[x['finding'] for x in findings if not x['decision']]
summary=dict(recorded_at=datetime.now(timezone.utc).isoformat(),scope=inventory['scope'],current_sets=inventory['total_sets'],reviewed_sets=len(coverage),unreviewed_sets=unreviewed,not_created=inventory['not_created'],reports=reports,findings=findings,undecided_findings=undecided,coverage=coverage,main_decisions=ref(HERE/'main-decisions.json') if (HERE/'main-decisions.json').exists() else None,complete=not unreviewed and not undecided,limitations=['Static generation-time screening, not native/game validation or a guarantee.','Component files were inventoried and checked for exact hashes; visual review is at rendered-set and targeted-component level, not a claim that all3253 component PNGs were individually inspected.','Superseded/rejected provenance is separately indexed rather than silently approved.'])
summary['existing_critical_issues']=decisions.get('existing_critical_issues',[])
summary['generation_ready_entries']=sum(bool(x.get('generation_ready')) for x in ledger['entries'])
(HERE/'summary.json').write_bytes((json.dumps(summary,indent=2,ensure_ascii=False)+'\n').encode())
lines=['# Texture structural review — 2026-10-21','',f'{len(coverage)} of {inventory["total_sets"]} current sets screened; {len(findings)} findings; {len(undecided)} awaiting main-author disposition.','',*summary['limitations'],'','| Entry | Review | Main decision |','| --- | --- | --- |']
html=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Texture structural review</title><style>body{background:#142823;color:#e5e8d8;font:17px/1.55 Georgia,serif;max-width:1200px;margin:30px auto;padding:0 20px}a{color:#e3cf43}table{border-collapse:collapse;width:100%}td,th{padding:10px;text-align:left;border-bottom:1px solid #526b5c}details{margin:10px 0}img{max-width:100%;height:auto}code{overflow-wrap:anywhere}.issue{color:#ffcc83}</style><a href="conversion-report.html">Conversion evidence</a><h1>Current texture structural review</h1>',f'<p>{len(coverage)} of {inventory["total_sets"]} current sets screened. {len(findings)} findings; {len(undecided)} awaiting main-author disposition.</p>','<p>'+escape(' '.join(summary['limitations']))+'</p><p><a href="../evidence/texture-review-20261021/inventory.json">Exact inventory</a> · <a href="../evidence/texture-review-20261021/summary.json">Reports, findings and hashes</a> · <a href="../evidence/texture-review-20261021/component-diagnostics.json">Nonvisual file diagnostics</a></p><table><thead><tr><th>Entry</th><th>Review</th><th>Main-author disposition</th></tr></thead><tbody>']
queue=[]
for issue in summary['existing_critical_issues']:queue.append((issue['entry'],issue['disposition'],issue['reason']))
for issue in findings:
 d=issue['decision']
 if d and (d['disposition']=='FIX NOW' or d.get('blocks_generation_readiness')):queue.append((issue['entry'],d['disposition'],d['reason']))
queuehtml='<h2>Current correction targets</h2><ul>'+''.join('<li><a href="conversion-report.html#'+escape(ident)+'">'+escape(ident)+'</a> — '+escape(disposition)+': '+escape(reason)+'</li>' for ident,disposition,reason in queue)+'</ul><p>Correction work remains unfinished. Broad screening does not override the closer rejected horn evidence.</p>'
html.insert(2,queuehtml)
lines[2:2]=['','Current correction targets: '+', '.join(ident+' ('+disposition+')' for ident,disposition,_ in queue)+'.','']
for item in inventory['sets']:
 ident=item['entry'];v=coverage.get(ident);issues=[x for x in findings if x['entry']==ident]
 verdict=v['verdict'] if v else 'PENDING';ds=', '.join(x['decision']['disposition'] if x['decision'] else 'AWAITING TRIAGE' for x in issues) or ('No observed finding' if v else 'Pending')
 lines.append(f'| [{ident}](conversion-report.html#{ident}) | {verdict} | {ds} |')
 detail=''
 for x in issues:
  d=x['decision'];detail+='<details><summary>'+escape(x['observation'])+'</summary><p>'+escape(str(x.get('view',''))+' / '+str(x.get('region',''))+' / '+str(x.get('confidence','')))+'<br>'+escape(d['reason'] if d else 'Main-author inspection pending')+'</p></details>'
 if v:detail+='<a href="../'+escape(v['report']['path'])+'">Independent report</a>'
 state=current[ident]
 if not state.get('generation_ready'):
  detail+='<p class="issue">Generation readiness withheld. '+escape(' '.join(state.get('known_issues',[])))+'</p>'
 html.append('<tr><td><a href="conversion-report.html#'+escape(ident)+'">'+escape(ident)+'</a></td><td>'+escape(verdict)+'</td><td>'+escape(ds)+detail+'</td></tr>')
html.append('</tbody></table><h2>Entries with no current created texture set</h2><p>'+escape(', '.join(x['entry'] for x in inventory['not_created']))+'</p><p>These19 entries receive no visual approval from this sweep.</p></html>')
(ROOT/'docs/texture-review-20261021.md').write_bytes(('\n'.join(lines)+'\n').encode());(ROOT/'docs/texture-review-20261021.html').write_bytes(('\n'.join(html)+'\n').encode())
print(json.dumps(dict(reviewed=len(coverage),total=inventory['total_sets'],findings=len(findings),undecided=len(undecided),complete=summary['complete'])))
