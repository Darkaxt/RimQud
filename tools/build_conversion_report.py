"""Render the actual per-entry ledger events as a static HTML evidence report."""
from collections import Counter
from html import escape as h
import json
from pathlib import Path
from enumerate_conversion_ledger import ROOT, enumerate_entries, validate

OUT=ROOT/'docs/conversion-report.html'

def artifact(item,url_prefix='../'):
    path=item['path'];url=url_prefix+path;p=ROOT/path
    label=h(Path(path).name)
    content=f'<a href="{h(url)}">{label}</a>'
    if p.suffix.lower() in ['.png','.jpg','.svg']:
        content=f'<a href="{h(url)}"><img loading="lazy" src="{h(url)}" alt="{h(item.get("role",Path(path).stem))}"></a><figcaption>{content}</figcaption>'
    if p.suffix=='.json':
        parsed=json.loads(p.read_text(encoding='utf-8'))
        content+=f'<details><summary>Read metadata / recorded decisions</summary><pre>{h(json.dumps(parsed,indent=2,ensure_ascii=False))}</pre></details>'
    return f'<figure>{content}<details class="hash"><summary>Exact evidence hash</summary><code>{h(item["sha256"])}</code></details></figure>'

BODY_GROUPS={
    'BODY-HUMAN-MALE':[('Human','Male Adult')],
    'BODY-HUMAN-FEMALE':[('Human','Female Adult')],
    'BODY-HUMAN-MALE-OLDER':[('Human','Male Older Adult')],
    'BODY-HUMAN-FEMALE-OLDER':[('Human','Female Older Adult')],
    'BODY-HUMAN-CHILD':[('Human','Male Child'),('Human','Female Child')],
    'BODY-DROMAD':[('Dromad','Adult')],
    'BODY-DROMAD-CHILD':[('Dromad','Male Child'),('Dromad','Female Child')],
    'BODY-RAY-CAT':[('Ray Cat','Standard')],
    'BODY-GLOWFISH':[('Glowfish','Standard')],
    'BODY-IRUDAD':[('Human','Irudad')],
    'BODY-NIMA':[('Human','Nima')],
    'BODY-YRAME':[('Human','Yrame')],
}

def entry_paths(entry,index):
    """Navigation membership follows existing body links; it does not duplicate records."""
    ident=entry['id'];category=entry['category']
    groups=BODY_GROUPS.get(ident,[])
    if not groups:
        groups=[group for related in entry['related_entries'] for group in BODY_GROUPS.get(related,[])]
    if groups:
        kind='Body' if ident.startswith('BODY-') else ('Equipment' if ident.startswith('FIT-') else 'NPCs')
        return [list(group)+( [kind]) for group in sorted(set(groups))]
    if category=='Equipment inventory':
        groups=[group for related in entry['related_entries'] if related in index
                for body in index[related]['related_entries'] for group in BODY_GROUPS.get(body,[])]
        return [list(group)+['Equipment'] for group in sorted(set(groups))] or [['Items','Equipment','Inventory']]
    environment={
        'Furniture':('Furniture','Objects'),'Vegetation':('Vegetation','Plants'),
        'Machinery/appliances':('Machinery','Objects'),'Containers':('Containers','Objects'),
        'Surface/grass tiles':('Surfaces','Tiles'),'Terrain/structures':('Structures','Tiles'),
        'Signs/shrine':('Signs and Shrines','Objects'),'Other props/debris/light':('Props and Lights','Objects'),
        'Baseline exclusion review':('Exclusion Review','Metadata'),
    }
    if category in environment:return [['Environment',*environment[category]]]
    return [['Other',category,'Entries']]

def render_entry_body(e,url_prefix):
    logs=e['process_log'];latest={l['step']:l for l in logs};passed={s for s,l in latest.items() if l.get('result')=='PASS'}
    parts=['<div class="entry-body">']
    if e.get('furniture_views'):
        views=e['furniture_views'];done=views.get('completed_views',[])
        parts.append('<p class="issues"><strong>Required furniture views: front / south, side / east, back / north.</strong> '+h('Complete set pending.' if not done else 'Recorded views: '+', '.join(done)+'.')+' Extra views are unbound authoring assets; wall/table-facing selection is undecided. West mirrors only where the design permits it.</p>')
    if e.get('apparel_occlusion'):
        parts.append('<p class="issues"><strong>Mask-first apparel.</strong> Retain intact clothing and a separate per-facing body-over-clothing mask. Show original-body overlay, mask-off/on assemblies and independent body/equipment tint. Baked limb cutouts are superseded; native binding remains pending.</p>')
    parts.append(f'<p class="eyebrow">{h(e["id"])} / '+('GENERATION READY · NATIVE ACCEPTANCE PENDING' if e.get('generation_ready') else 'GENERATION UNFINISHED')+'</p><p class="issues">Reset findings / historical defects: '+h(' '.join(e['known_issues']))+'</p>')
    if e.get('current_experiment'):
        trial=e['current_experiment']
        if trial.get('pipeline'):
            parts.append('<p><a href="'+url_prefix+h(trial['pipeline']['path'])+'">Whole clothing pipeline: actual images, limitations and proposed three-band fitting</a></p>')
        parts.append('<h3>Current experiment — unfinished</h3><p>'+h(trial['summary'])+'</p><div class="gallery">'+artifact(trial['plate'],url_prefix)+artifact(trial['before_after'],url_prefix)+'</div>')
        if trial.get('scale_preview'):
            parts.append('<p>Authored sprite-size comparison; this is not a native game capture.</p><div class="gallery">'+artifact(trial['scale_preview'],url_prefix)+'</div>')
        parts.append('<p>Body masks by clothing type: '+', '.join('<a href="'+url_prefix+h(m['path'])+'">'+h(Path(m['path']).name.split('-mask-')[0])+'</a>' for m in trial['masks'])+'. <a href="'+url_prefix+h(trial['review']['path'])+'">Authoring review and limitations</a>.</p>')
    if e.get('current_registration'):
        current=e['current_registration']
        note=e.get('registration_summary','Use this registered version for layer alignment. Gold marks the shared pivot; the ground guide marks contact. Body, head, masks and fitted clothing share that frame. Asymmetric features may extend beyond the pivot.')
        review=e.get('art_review') or e.get('camera_review',{})
        if review.get('status') in ['REQUIRES REWORK','REQUIRES REVIEW']:
            label='Garment fit' if e.get('art_review') else 'Camera'
            parts.append('<p class="issues"><strong>'+label+': '+h(review['status'])+'.</strong> '+h(review['reason'])+'</p>')
            title='Registered candidate — '+('garment' if e.get('art_review') else 'camera')+' correction/review pending'
        else:title='Current registered artwork'
        parts.append('<h3>'+title+'</h3><p>'+h(note)+'</p><div class="gallery">'+artifact(current['plate'],url_prefix)+'</div><p><a href="'+url_prefix+h(current['model']['path'])+'">Current asset registration</a></p>')
    parts.append('<ol class="workflow">'+''.join(f'<li class="{"pass" if s in passed else "pending"}">{h(s.replace("_"," "))} — {"recorded PASS" if s in passed else "pending"}</li>' for s in e['required_steps'])+'</ol>')
    if e.get('current_registration'):
        parts.append('<h3>Process history, including superseded sheets</h3><p class="pending">Raw generations and superseded registrations remain preserved. Use the registered artwork or flagged candidate above for current authoring status. Native acceptance remains pending.</p>')
    elif logs:parts.append('<p class="pending">No registered output is selected. Images below are authoring evidence, not proof of stable runtime alignment.</p>')
    parts.append('<div class="timeline">')
    for i,event in enumerate(logs,1):
        parts.append(f'<section class="event"><small>{i:02} / {h(event["timestamp"])} / {h(event.get("result","PENDING"))}</small><h3>{h(event.get("phase",event["step"].replace("_"," ")))}</h3><p>{h(event["action"])}</p><p><strong>Review:</strong> {h(event.get("review","Not yet reviewed"))}</p>')
        parts.append('<div class="gallery">'+''.join(artifact(x,url_prefix) for x in event.get('outputs',[]))+'</div>')
        parts.append('<details class="method"><summary>Inputs, exact prompt, settings and decisions</summary><pre>'+h(json.dumps({k:v for k,v in event.items() if k!='outputs'},indent=2,ensure_ascii=False))+'</pre></details></section>')
    if not logs:parts.append('<p class="pending">No conversion steps have been performed under the reset.</p>')
    parts.append('</div></div>')
    return '\n'.join(parts)

def render(data):
    rows=data['entries'];counts=Counter(e['status'] for e in rows)
    parts=['''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>RimQud · conversion evidence</title><style>
:root{color-scheme:dark;--bg:#142823;--panel:#20382d;--ink:#e5e8d8;--muted:#b6c8ba;--line:#526b5c;--gold:#e3cf43}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:18px/1.55 Georgia,serif}main{max-width:1440px;padding:36px 32px 80px;margin:auto}a{color:var(--gold)}h1{font-size:clamp(2.2rem,5vw,4.1rem);line-height:1.05;max-width:950px;margin:16px 0 22px}h2,h3{line-height:1.2}p{max-width:85ch}.eyebrow,.status,small,figcaption,label,summary{font-family:Consolas,monospace}.eyebrow{color:var(--gold);letter-spacing:.13em;font-size:13px}.intro{color:var(--muted)}.counts{display:flex;flex-wrap:wrap;gap:14px;border-block:1px solid var(--line);padding:16px 0;margin:25px 0}.counts strong{font:25px Consolas,monospace;color:var(--gold)}.filters{display:flex;gap:20px;align-items:center;flex-wrap:wrap;margin-bottom:30px}input{background:var(--panel);color:var(--ink);border:1px solid var(--line);padding:10px;font:16px Consolas,monospace;width:min(100%,470px)}.entry{margin:10px 0;border:1px solid var(--line);scroll-margin-top:20px}.entry>.entry-toggle{display:flex;gap:15px;align-items:center;justify-content:space-between;padding:16px;cursor:pointer;background:var(--panel);font-size:15px}.entry[data-open="true"]>.entry-toggle{border-bottom:1px solid var(--gold)}.status{color:var(--gold);font-size:12px;white-space:nowrap}.entry-body{padding:20px}.issues{color:var(--muted);font-size:16px}.workflow{display:flex;gap:8px;flex-wrap:wrap;list-style:none;padding:0;margin:20px 0}.workflow li{font:12px/1.4 Consolas,monospace;border:1px solid var(--line);padding:8px;max-width:240px}.workflow .pass{border-color:var(--gold)}.timeline{border-left:2px solid var(--line);padding-left:22px}.event{padding:8px 0 28px;border-bottom:1px solid var(--line);margin-bottom:20px}.event h3{font-size:25px;margin:8px 0}.event small{color:var(--muted);font-size:12px}.gallery{display:flex;align-items:flex-start;flex-wrap:wrap;gap:16px}figure{margin:0;min-width:0;max-width:100%;padding:12px;border:1px solid var(--line);background:#1b3028;flex:1 1 260px}figure img{display:block;width:100%;height:340px;object-fit:contain;background:repeating-conic-gradient(#20382d 0% 25%,#294135 0% 50%) 50%/20px 20px}figure:has(img[src*="comparison"]) {flex-basis:100%}figure:has(img[src*="comparison"]) img{height:auto;max-height:570px}figcaption{font-size:13px;margin-top:10px;overflow-wrap:anywhere}pre,code{font:12px/1.5 Consolas,monospace;white-space:pre-wrap;overflow-wrap:anywhere}details.hash{font-size:12px;color:var(--muted);margin-top:8px}.method{margin-top:16px}summary:focus-visible,a:focus-visible,input:focus-visible{outline:2px solid var(--gold);outline-offset:4px}.pending{color:var(--muted);font-style:italic}nav{display:flex;gap:18px;flex-wrap:wrap}footer{border-top:1px solid var(--line);margin-top:40px;padding-top:20px;color:var(--muted);font-size:15px}@media(max-width:650px){main{padding:24px 12px 45px}.entry-body{padding:12px}.entry>.entry-toggle{align-items:flex-start;flex-direction:column;gap:5px}.timeline{padding-left:12px}figure img{height:300px}.filters{display:block}.filters label{display:block;margin:12px 0}}
.taxonomy{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;width:100%}.taxonomy label{display:block;min-width:0}.taxonomy select{display:block;width:100%;margin-top:6px;background:var(--panel);color:var(--ink);border:1px solid var(--line);padding:10px;font:16px Consolas,monospace}.taxonomy select:disabled{opacity:.55}button{background:var(--panel);color:var(--gold);border:1px solid var(--line);padding:10px 14px;font:15px Consolas,monospace;cursor:pointer}select:focus-visible,button:focus-visible{outline:2px solid var(--gold);outline-offset:4px}.filter-note{margin:0;font:14px/1.5 Consolas,monospace;color:var(--muted);width:100%}.entry>.entry-toggle{width:100%;text-align:left;color:var(--ink)}.entry-host:empty{display:none}@media(max-width:650px){.taxonomy{grid-template-columns:1fr;gap:8px}.taxonomy label{margin:0}.filters input[type=search]{width:100%}}
</style><main><div class="eyebrow">RIMQUD / ORIGINAL → CONSTRUCTION → REFINEMENT → INTEGRATION</div>
<h1>Every shape, with its evidence.</h1><p class="intro">This report shows the conversion as it happens. Source facts, authored interpretations, generated proposals, corrections and actual native results remain distinguishable. A missing step stays visible. Historical drafts receive no completion credit.</p>
<nav><a href="conversion-ledger.md">Readable ledger</a><a href="../evidence/conversion-ledger.json">Structured record</a><a href="../art/village/preview.html">Historical village draft</a></nav>''']
    ready=sum(bool(e.get('generation_ready')) for e in rows)
    parts.append('<div class="counts">'+f'<span><strong>{ready}</strong> generation-ready</span>'+''.join(f'<span><strong>{n}</strong> {h(s.lower())}</span>' for s,n in counts.items())+'</div>')
    parts.append(f'<p>Active entry: <strong>{h(data["active_entry"] or "none")}</strong>. Stage 3 remains ACTIVE. Overall conversion is unfinished.</p>')
    parts.append('<p class="intro"><strong>Generation first.</strong> Native and formal integration validation waits until every pending conversion is generation-ready. Generation-ready is an authoring milestone; overall ledger status stays unfinished until applicable final acceptance. Image inspection, patches and recomposition remain generation work.</p>')
    if data.get('camera_policy'):
        parts.append('<p class="intro"><strong>Cardinal camera correction.</strong> '+h(data['camera_policy']['summary'])+' <a href="../evidence/camera-facing-audit.json">Camera audit and affected entries</a>.</p>')
    parts.append('<p class="intro">Environment contract: preserve the original Qud palette and forms. Paths should read as stone/cobblestone-like paving integrated over grass, rather than the historical sandy-road interpretation. Extra views may be omitted only when the object and its states do not require them, with the reason logged.</p>')
    parts.append('<section class="filters" aria-label="Filter conversions"><div class="taxonomy"><label>Category<select id="category"><option value="">All categories</option></select></label><label>Subcategory<select id="subcategory" disabled><option value="">All subcategories</option></select></label><label>Asset type<select id="asset-type" disabled><option value="">All asset types</option></select></label></div><label>Find a subject <input id="search" type="search" placeholder="Name, category or ledger entry"></label><label><input id="worked" type="checkbox" style="width:auto" checked> Entries with process evidence only</label><button id="reset-filters" type="button">Clear filters</button><span id="shown" role="status" aria-live="polite"></span><p class="filter-note">Evidence loads when you expand a subject and is removed when you collapse it. Shared child templates appear under both Male Child and Female Child; ledger entries are not duplicated.</p></section>')
    index={e['id']:e for e in rows}
    for e in sorted(rows,key=lambda x:(x['id']!=data['active_entry'],x['category'],x['name'])):
        paths=entry_paths(e,index)
        search_text=' '.join([e['id'],e['name'],e['category'],*(word for path in paths for word in path)])
        parts.append(f'<article class="entry" id="{h(e["id"])}" data-search="{h(search_text.lower())}" data-paths="{h(json.dumps(paths))}" data-worked="{int(bool(e["process_log"]))}" data-url="conversion-entries/{h(e["id"])}.html"><button class="entry-toggle" type="button" aria-expanded="false" aria-controls="evidence-{h(e["id"])}"><span>{h(e["name"])} <small> / {h(e["category"])}</small></span><span class="status">'+('GENERATION READY' if e.get('generation_ready') else h(e['status']))+'</span></button><div class="entry-host" id="evidence-'+h(e['id'])+'"></div></article>')
    parts.append('''<footer>Generated directly from the conversion ledger. The evidence hashes identify the actual saved files. A recorded PASS applies only to its stated step; it does not accept the entire entry, clothing or native integration. Source game textures remain private; contextual comparison plates show reference use.</footer></main><script>
const entries=[...document.querySelectorAll('.entry')],search=document.querySelector('#search'),worked=document.querySelector('#worked');
const category=document.querySelector('#category'),subcategory=document.querySelector('#subcategory'),assetType=document.querySelector('#asset-type');
const memberships=new Map(entries.map(e=>[e,JSON.parse(e.dataset.paths)])),requests=new WeakMap();
function options(select,values,label){select.replaceChildren(new Option(label,''),...[...new Set(values)].sort().map(v=>new Option(v,v)));}
options(category,[...memberships.values()].flat().map(p=>p[0]),'All categories');
function children(){
 options(subcategory,[...memberships.values()].flat().filter(p=>p[0]===category.value).map(p=>p[1]),'All subcategories');subcategory.disabled=!category.value;
 types();
}
function types(){
 options(assetType,[...memberships.values()].flat().filter(p=>p[0]===category.value&&p[1]===subcategory.value).map(p=>p[2]),'All asset types');assetType.disabled=!subcategory.value;
}
function unload(e){const state=requests.get(e);if(state){state.controller.abort();requests.delete(e);}e.querySelector('.entry-host').replaceChildren();}
async function loadEntry(e){
 const host=e.querySelector('.entry-host');if(requests.has(e)||host.querySelector('.entry-body'))return;
 const state={controller:new AbortController()};requests.set(e,state);const message=document.createElement('p');message.className='entry-body';message.setAttribute('role','status');message.textContent='Loading this subject’s evidence…';host.replaceChildren(message);
 try{
  const response=await fetch(e.dataset.url,{signal:state.controller.signal});if(!response.ok)throw new Error('Entry could not be loaded ('+response.status+').');
  const page=new DOMParser().parseFromString(await response.text(),'text/html'),body=page.querySelector('.entry-body');if(!body)throw new Error('Entry evidence is missing.');
  if(e.dataset.open!=='true'||requests.get(e)!==state)return;
  for(const node of body.querySelectorAll('[href],[src]'))for(const attr of ['href','src'])if(node.hasAttribute(attr))node.setAttribute(attr,new URL(node.getAttribute(attr),response.url).href);
  host.replaceChildren(document.importNode(body,true));
 }catch(error){
  if(state.controller.signal.aborted||requests.get(e)!==state||e.dataset.open!=='true')return;
  message.replaceChildren(document.createTextNode('This entry could not be loaded. '));const retry=document.createElement('button');retry.type='button';retry.textContent='Retry entry';retry.addEventListener('click',()=>{host.replaceChildren();loadEntry(e);});message.append(retry);
 }finally{if(requests.get(e)===state)requests.delete(e);}
}
function setOpen(e,open){e.dataset.open=String(open);e.querySelector('.entry-toggle').setAttribute('aria-expanded',String(open));if(open)loadEntry(e);else unload(e);}
for(const e of entries)e.querySelector('.entry-toggle').addEventListener('click',()=>setOpen(e,e.dataset.open!=='true'));
function filter(){let count=0;for(const e of entries){const match=memberships.get(e).some(p=>(!category.value||p[0]===category.value)&&(!subcategory.value||p[1]===subcategory.value)&&(!assetType.value||p[2]===assetType.value));const visible=match&&e.dataset.search.includes(search.value.toLowerCase())&&(!worked.checked||e.dataset.worked==='1');e.hidden=!visible;if(!visible&&e.dataset.open==='true')setOpen(e,false);if(visible)count++;}document.querySelector('#shown').textContent=count+' entries shown';}
category.addEventListener('change',()=>{children();filter();});subcategory.addEventListener('change',()=>{types();filter();});assetType.addEventListener('change',filter);search.addEventListener('input',filter);worked.addEventListener('change',filter);
document.querySelector('#reset-filters').addEventListener('click',()=>{category.value='';children();search.value='';worked.checked=false;filter();});
function followHash(){if(!location.hash)return;const e=document.getElementById(decodeURIComponent(location.hash.slice(1)));if(e&&e.classList.contains('entry')){category.value='';children();search.value='';worked.checked=false;filter();setOpen(e,true);e.scrollIntoView();}}
filter();followHash();window.addEventListener('hashchange',followHash);
</script></html>''')
    return '\n'.join(parts)

def main():
    data=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'))
    validate(data,enumerate_entries())
    rendered=render(data)
    entry_dir=ROOT/'docs/conversion-entries';entry_dir.mkdir(exist_ok=True)
    style=rendered.split('<style>',1)[1].split('</style>',1)[0]
    for e in data['entries']:
        page='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+h(e['name'])+' · RimQud evidence</title><style>'+style+'</style><main><nav><a href="../conversion-report.html#'+h(e['id'])+'">Back to conversion index</a></nav><h1>'+h(e['name'])+'</h1>'+render_entry_body(e,'../../')+'</main></html>'
        (entry_dir/(e['id']+'.html')).write_bytes(page.encode())
    OUT.write_bytes(rendered.encode())
    print(f'HTML report rendered: {len(data["entries"])} entries, {sum(len(e["process_log"]) for e in data["entries"])} actual events.')

if __name__=='__main__':main()
