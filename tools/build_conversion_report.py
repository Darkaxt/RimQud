"""Render the actual per-entry ledger events as a static HTML evidence report."""
from collections import Counter
from html import escape as h
import json
from pathlib import Path
from enumerate_conversion_ledger import ROOT, enumerate_entries, validate

OUT=ROOT/'docs/conversion-report.html'

def artifact(item):
    path=item['path'];url='../'+path;p=ROOT/path
    label=h(Path(path).name)
    content=f'<a href="{h(url)}">{label}</a>'
    if p.suffix.lower() in ['.png','.jpg','.svg']:
        content=f'<a href="{h(url)}"><img loading="lazy" src="{h(url)}" alt="{h(item.get("role",Path(path).stem))}"></a><figcaption>{content}</figcaption>'
    if p.suffix=='.json':
        parsed=json.loads(p.read_text(encoding='utf-8'))
        content+=f'<details><summary>Read metadata / recorded decisions</summary><pre>{h(json.dumps(parsed,indent=2,ensure_ascii=False))}</pre></details>'
    return f'<figure>{content}<details class="hash"><summary>Exact evidence hash</summary><code>{h(item["sha256"])}</code></details></figure>'

def render(data):
    rows=data['entries'];counts=Counter(e['status'] for e in rows)
    parts=['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RimQud · conversion evidence</title><style>
:root{color-scheme:dark;--bg:#142823;--panel:#20382d;--ink:#e5e8d8;--muted:#b6c8ba;--line:#526b5c;--gold:#e3cf43}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.55 Georgia,serif}main{max-width:1440px;padding:36px 32px 80px;margin:auto}a{color:var(--gold)}h1{font-size:clamp(2.2rem,5vw,4.1rem);line-height:1.05;max-width:950px;margin:16px 0 22px}h2,h3{line-height:1.2}p{max-width:85ch}.eyebrow,.status,small,figcaption,label,summary{font-family:Consolas,monospace}.eyebrow{color:var(--gold);letter-spacing:.13em;font-size:13px}.intro{color:var(--muted)}.counts{display:flex;flex-wrap:wrap;gap:14px;border-block:1px solid var(--line);padding:16px 0;margin:25px 0}.counts strong{font:25px Consolas,monospace;color:var(--gold)}.filters{display:flex;gap:20px;align-items:center;flex-wrap:wrap;margin-bottom:30px}input{background:var(--panel);color:var(--ink);border:1px solid var(--line);padding:10px;font:16px Consolas,monospace;width:min(100%,470px)}.entry{margin:10px 0;border:1px solid var(--line);scroll-margin-top:20px}.entry>summary{display:flex;gap:15px;align-items:center;justify-content:space-between;padding:16px;cursor:pointer;background:var(--panel);font-size:15px}.entry[open]>summary{border-bottom:1px solid var(--gold)}.status{color:var(--gold);font-size:12px;white-space:nowrap}.entry-body{padding:20px}.issues{color:var(--muted);font-size:16px}.workflow{display:flex;gap:8px;flex-wrap:wrap;list-style:none;padding:0;margin:20px 0}.workflow li{font:12px/1.4 Consolas,monospace;border:1px solid var(--line);padding:8px;max-width:240px}.workflow .pass{border-color:var(--gold)}.timeline{border-left:2px solid var(--line);padding-left:22px}.event{padding:8px 0 28px;border-bottom:1px solid var(--line);margin-bottom:20px}.event h3{font-size:25px;margin:8px 0}.event small{color:var(--muted);font-size:12px}.gallery{display:flex;align-items:flex-start;flex-wrap:wrap;gap:16px}figure{margin:0;min-width:0;max-width:100%;padding:12px;border:1px solid var(--line);background:#1b3028;flex:1 1 260px}figure img{display:block;width:100%;height:340px;object-fit:contain;background:repeating-conic-gradient(#20382d 0% 25%,#294135 0% 50%) 50%/20px 20px}figure:has(img[src*="comparison"]) {flex-basis:100%}figure:has(img[src*="comparison"]) img{height:auto;max-height:570px}figcaption{font-size:13px;margin-top:10px;overflow-wrap:anywhere}pre,code{font:12px/1.5 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}details.hash{font-size:12px;color:var(--muted);margin-top:8px}.method{margin-top:16px}summary:focus-visible,a:focus-visible,input:focus-visible{outline:2px solid var(--gold);outline-offset:4px}.pending{color:var(--muted);font-style:italic}nav{display:flex;gap:18px;flex-wrap:wrap}footer{border-top:1px solid var(--line);margin-top:40px;padding-top:20px;color:var(--muted);font-size:15px}@media(max-width:650px){main{padding:24px 12px 45px}.entry-body{padding:12px}.entry>summary{align-items:flex-start;flex-direction:column;gap:5px}.timeline{padding-left:12px}figure img{height:300px}.filters{display:block}.filters label{display:block;margin:12px 0}}
</style><main><div class="eyebrow">RIMQUD / ORIGINAL → CONSTRUCTION → REFINEMENT → INTEGRATION</div>
<h1>Every shape, with its evidence.</h1><p class="intro">This report shows the conversion as it happens. Source facts, authored interpretations, generated proposals, corrections and actual native results remain distinguishable. A missing step stays visible. Historical drafts receive no completion credit.</p>
<nav><a href="conversion-ledger.md">Readable ledger</a><a href="../evidence/conversion-ledger.json">Structured record</a><a href="../art/village/preview.html">Historical village draft</a></nav>''']
    ready=sum(bool(e.get('generation_ready')) for e in rows)
    parts.append('<div class="counts">'+f'<span><strong>{ready}</strong> generation-ready</span>'+''.join(f'<span><strong>{n}</strong> {h(s.lower())}</span>' for s,n in counts.items())+'</div>')
    parts.append(f'<p>Active entry: <strong>{h(data["active_entry"] or "none")}</strong>. Stage 3 remains ACTIVE. Overall conversion is unfinished.</p>')
    parts.append('<p class="intro"><strong>Generation first.</strong> Native and formal integration validation waits until every pending conversion is generation-ready. Generation-ready is an authoring milestone; overall ledger status stays unfinished until applicable final acceptance. Image inspection, patches and recomposition remain generation work.</p>')
    parts.append('<p class="intro">Environment contract: preserve the original Qud palette and forms. Paths should read as stone/cobblestone-like paving integrated over grass, rather than the historical sandy-road interpretation. Extra views may be omitted only when the object and its states do not require them, with the reason logged.</p>')
    parts.append('<div class="filters"><label>Find a subject <input id="search" type="search" placeholder="Name, category or ledger entry"></label><label><input id="worked" type="checkbox" style="width:auto" checked> Entries with process evidence only</label><span id="shown" role="status"></span></div>')
    for e in sorted(rows,key=lambda x:(x['id']!=data['active_entry'],x['category'],x['name'])):
        logs=e['process_log'];passed={l['step'] for l in logs if l.get('result')=='PASS'}
        parts.append(f'<details class="entry" id="{h(e["id"])}" data-search="{h((e["id"]+" "+e["name"]+" "+e["category"]).lower())}" data-worked="{int(bool(logs))}"'+(' open' if logs else '')+f'><summary><span>{h(e["name"])} <small> / {h(e["category"])}</small></span><span class="status">{h(e["status"])}</span></summary><div class="entry-body">')
        parts.append(f'<p class="eyebrow">{h(e["id"])} / '+('GENERATION READY · NATIVE ACCEPTANCE PENDING' if e.get('generation_ready') else 'GENERATION UNFINISHED')+'</p><p class="issues">Reset findings / historical defects: '+h(' '.join(e['known_issues']))+'</p>')
        if e.get('current_registration'):
            current=e['current_registration']
            registration_note=e.get('registration_summary','Use this registered version for layer alignment. The gold guide marks the shared horizontal pivot; the ground guide marks the common contact baseline. Body, head, masks and fitted clothing share that frame. A muzzle, hump or forward-pointing foot can extend beyond the pivot without moving it.')
            parts.append('<h3>Current registered artwork</h3><p>'+h(registration_note)+'</p><div class="gallery">'+artifact(current['plate'])+'</div><p><a href="../'+h(current['model']['path'])+'">Current asset registration</a></p>')
        parts.append('<ol class="workflow">'+''.join(f'<li class="{"pass" if s in passed else "pending"}">{h(s.replace("_"," "))} — {"recorded PASS" if s in passed else "pending"}</li>' for s in e['required_steps'])+'</ol>')
        if e.get('current_registration'):
            parts.append('<h3>Process history, including superseded sheets</h3>')
            parts.append('<p class="pending">These records include raw ImageGen sheets with uneven placement and superseded registrations. Their placement is not the current runtime alignment. Refer to Current registered artwork above for the selected frame. Native movement acceptance remains pending.</p>')
        elif logs:
            parts.append('<p class="pending">No current registered output is selected for this entry. The images below are authoring evidence; their position on a sheet does not establish a stable runtime pivot.</p>')
        parts.append('<div class="timeline">')
        for i,event in enumerate(logs,1):
            parts.append(f'<section class="event"><small>{i:02} / {h(event["timestamp"])} / {h(event.get("result","PENDING"))}</small><h3>{h(event.get("phase",event["step"].replace("_"," ")))}</h3><p>{h(event["action"])}</p><p><strong>Review:</strong> {h(event.get("review","Not yet reviewed"))}</p>')
            parts.append('<div class="gallery">'+''.join(artifact(x) for x in event.get('outputs',[]))+'</div>')
            parts.append('<details class="method"><summary>Inputs, exact prompt, settings and decisions</summary><pre>'+h(json.dumps({k:v for k,v in event.items() if k not in ['outputs']},indent=2,ensure_ascii=False))+'</pre></details></section>')
        if not logs:parts.append('<p class="pending">No conversion steps have been performed under the reset.</p>')
        parts.append('</div></div></details>')
    parts.append('''<footer>Generated directly from the conversion ledger. The evidence hashes identify the actual saved files. A recorded PASS applies only to its stated step; it does not accept the entire entry, clothing or native integration. Source game textures remain private; contextual comparison plates show reference use.</footer></main><script>
const entries=[...document.querySelectorAll('.entry')],search=document.querySelector('#search'),worked=document.querySelector('#worked');
function filter(){let count=0;for(const e of entries){const visible=e.dataset.search.includes(search.value.toLowerCase())&&(!worked.checked||e.dataset.worked==='1');e.hidden=!visible;if(visible)count++;}document.querySelector('#shown').textContent=count+' entries shown';}
search.addEventListener('input',filter);worked.addEventListener('change',filter);filter();
if(location.hash){worked.checked=false;filter();const e=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(e){e.open=true;e.scrollIntoView();}}
</script></html>''')
    return '\n'.join(parts)

def main():
    data=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'))
    validate(data,enumerate_entries())
    OUT.write_bytes(render(data).encode())
    print(f'HTML report rendered: {len(data["entries"])} entries, {sum(len(e["process_log"]) for e in data["entries"])} actual events.')

if __name__=='__main__':main()
