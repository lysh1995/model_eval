"""Interactive dashboard: select a variant to review its detail, or cross-compare variants.

Unlike the static renderer, this embeds the grade book as JSON and renders three views in the
browser with vanilla JS (CSP-safe, inline, no framework, no external asset):

  OVERVIEW  a variant × dimension matrix, both phases. Click a variant to drill in.
  DETAIL    one variant: its actual system PROMPT, ability characterization, and every
            dimension score with where it ranks in the field.
  COMPARE   pick variants, side-by-side per dimension with the leader marked.

Published as an artifact, this runs JS on claude.ai. (The local preview pane shows static
snapshots only — view the artifact URL for the interactive version.)
"""
from __future__ import annotations
import html as _html
import json
import pathlib
from typing import List, Optional, Union

from ..gradebook import GradeBook

_CSS = r"""
:root{--paper:#f4f6f8;--panel:#fff;--ink:#161b22;--muted:#5b6675;--faint:#8a94a3;
--line:#e3e7ec;--line2:#eef1f4;--signal:#0d6e82;--signal-soft:#e2f0f3;--critical:#b42318;
--caution:#8a5a00;--caution-soft:#fbf1dd;--pass:#2f7d5b;--pass-soft:#e6f2ec;
--shadow:0 1px 3px rgba(20,26,34,.07)}
@media(prefers-color-scheme:dark){:root{--paper:#0e1116;--panel:#161b22;--ink:#e6e9ee;
--muted:#9aa4b2;--faint:#68717f;--line:#232a33;--line2:#1b2129;--signal:#3bb7cf;
--signal-soft:#123038;--critical:#f0776a;--caution:#e0a53a;--caution-soft:#2c220f;
--pass:#5cc295;--pass-soft:#12271e;--shadow:0 1px 3px rgba(0,0,0,.35)}}
:root[data-theme=light]{--paper:#f4f6f8;--panel:#fff;--ink:#161b22;--muted:#5b6675;
--faint:#8a94a3;--line:#e3e7ec;--line2:#eef1f4;--signal:#0d6e82;--signal-soft:#e2f0f3;
--critical:#b42318;--caution:#8a5a00;--caution-soft:#fbf1dd;--pass:#2f7d5b;--pass-soft:#e6f2ec}
:root[data-theme=dark]{--paper:#0e1116;--panel:#161b22;--ink:#e6e9ee;--muted:#9aa4b2;
--faint:#68717f;--line:#232a33;--line2:#1b2129;--signal:#3bb7cf;--signal-soft:#123038;
--critical:#f0776a;--caution:#e0a53a;--caution-soft:#2c220f;--pass:#5cc295;--pass-soft:#12271e}
#app{background:var(--paper);color:var(--ink);min-height:100vh;padding:32px 24px 64px;
font-family:ui-sans-serif,-apple-system,"Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
#app *{box-sizing:border-box}
.wrap{max-width:1000px;margin:0 auto}
.num{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-variant-numeric:tabular-nums}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--signal);font-weight:700}
h1{font-size:23px;font-weight:680;letter-spacing:-.01em;margin:6px 0 2px}
.sub{color:var(--muted);font-size:12px;margin-bottom:20px}
.nav{display:flex;gap:4px;background:var(--line);padding:4px;border-radius:11px;
width:fit-content;margin-bottom:8px}
.nav button{border:0;background:transparent;color:var(--muted);font-size:13px;font-weight:600;
padding:7px 16px;border-radius:8px;cursor:pointer;font-family:inherit}
.nav button.on{background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
.bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:14px 0}
select,.chk{font-family:inherit;font-size:13px}
select{padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--panel);color:var(--ink)}
.chk{display:inline-flex;align-items:center;gap:6px;padding:6px 11px;border:1px solid var(--line);
border-radius:8px;cursor:pointer;background:var(--panel);user-select:none}
.chk.on{border-color:var(--signal);background:var(--signal-soft);color:var(--signal);font-weight:600}
.phase{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);
font-weight:700;margin:24px 0 6px;border-bottom:2px solid var(--line);padding-bottom:5px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;color:var(--faint);font-size:10.5px;text-transform:uppercase;letter-spacing:.04em;
font-weight:600;padding:6px 10px}
th.r,td.r{text-align:right}
td{padding:8px 10px;border-top:1px solid var(--line2)}
.dimname{font-weight:560}
.lay{font-size:8.5px;color:var(--faint);font-weight:700;margin-right:5px}
.val{font-weight:640}
.track{height:6px;border-radius:3px;background:var(--line);position:relative;min-width:90px;display:inline-block;width:100%;max-width:140px;vertical-align:middle}
.track>i{position:absolute;left:0;top:0;height:100%;border-radius:3px}
.lead{font-size:9px;font-weight:700;color:var(--pass);background:var(--pass-soft);
padding:1px 6px;border-radius:4px;margin-left:6px}
.role{font-size:9px;padding:1px 6px;border-radius:4px;font-weight:700}
.role-gate{background:var(--critical);color:#fff}.role-guide{background:var(--signal-soft);color:var(--signal)}
.role-trap{background:var(--caution-soft);color:var(--caution)}
.card{border:1px solid var(--line);border-radius:12px;background:var(--panel);padding:18px 20px;
box-shadow:var(--shadow);margin:14px 0}
.prompt{font-family:ui-monospace,Menlo,monospace;font-size:12px;line-height:1.55;color:var(--ink);
background:var(--line2);border-radius:8px;padding:12px 14px;white-space:pre-wrap;margin-top:8px}
.char{font-size:13px;color:var(--ink);line-height:1.55;margin:6px 0 4px}
.note{color:var(--muted);font-size:11px}
.meta{font-size:11px;color:var(--muted)}
.warn{background:var(--caution-soft);border:1px solid var(--caution);border-radius:10px;
padding:11px 15px;font-size:11.5px;color:var(--ink);margin:10px 0}
.warn b{color:var(--caution)}
.cannot{background:var(--panel);border-left:3px solid var(--signal);border-radius:0 10px 10px 0;
padding:16px 18px;margin-top:26px}
.cannot li{font-size:12px;margin:5px 0;color:var(--ink)}
.matrix td.hl{background:var(--pass-soft)}
"""


def _e(s):
    return _html.escape(str(s))


def render_interactive(gradebook: Union[GradeBook, dict], variants: dict, profiles: list,
                       out_path: str, title: Optional[str] = None) -> str:
    gb = gradebook.to_dict() if isinstance(gradebook, GradeBook) else gradebook
    payload = {
        "title": title or gb.get("title", "Companion variant evaluation"),
        "variants": variants,
        "grades": [g for g in gb["grades"] if g.get("segment") != "self_selected_arm"],
        "profiles": [p.to_row() if hasattr(p, "to_row") else p for p in profiles],
        "cannot_measure": gb.get("cannot_measure", []),
        "created": gb.get("created_iso", "")[:19],
        "evaluators": gb.get("evaluator_ids", []),
    }
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")

    js = r"""
const D = JSON.parse(document.getElementById('data').textContent);
const OFF = new Set(['offline_content','offline_judge']), ON = new Set(['live_behavior']);
const esc = s => String(s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const fmt = v => v==null||isNaN(v)?'—':(Math.abs(v)<1?v.toFixed(3):v.toFixed(1));
const vids = Object.keys(D.variants);
const dimsOf = src => [...new Set(D.grades.filter(g=>src.has(g.source)).map(g=>g.dimension))];
const grade = (dim,vid) => D.grades.find(g=>g.dimension===dim&&g.variant_id===vid);
const lowerBetter = new Set(['repetition','wimp_rate','over_refusal','homogenization','abandonment','regenerate_rate']);
let state = {view:'overview', variant:vids[0], cmp:new Set(vids)};

function roleTag(r){return `<span class="role role-${r}">${r}</span>`}
function bar(v,mx,color){const p=mx?Math.max(3,Math.min(100,100*Math.abs(v)/mx)):3;
  return `<span class="track"><i style="width:${p}%;background:${color}"></i></span>`}
function color(r){return r==='gate'?'var(--critical)':r==='trap'?'var(--caution)':'var(--signal)'}

function overview(){
  let h='';
  for(const [label,src] of [['Pre-launch — offline',OFF],['Live — online',ON]]){
    const dims=dimsOf(src); if(!dims.length) continue;
    h+=`<div class="phase">${label}</div><table class="matrix"><tr><th>dimension</th>`+
       vids.map(v=>`<th class="r">${esc(D.variants[v].label)}</th>`).join('')+`</tr>`;
    for(const dim of dims){
      const gs=vids.map(v=>grade(dim,v)); const g0=gs.find(Boolean); if(!g0) continue;
      const vals=gs.map(g=>g?g.value:null).filter(x=>x!=null);
      const best = lowerBetter.has(dim)?Math.min(...vals):Math.max(...vals);
      h+=`<tr><td class="dimname"><span class="lay">${g0.role[0].toUpperCase()}</span>${esc(dim)}</td>`+
        gs.map(g=>{if(!g)return '<td class="r note">—</td>';
          const hl=g.value===best?' hl':'';
          return `<td class="r${hl}"><span class="val num">${fmt(g.value)}</span></td>`}).join('')+`</tr>`;
    }
    h+=`</table>`;
  }
  h+=`<div class="note" style="margin-top:12px">Green = leads on that dimension `+
     `(direction-aware: lower is better for repetition, wimp, refusal…). `+
     `Click <b>By variant</b> to see one variant's prompt and full profile, or <b>Compare</b> for deltas.</div>`;
  return h;
}

function detail(){
  const v=state.variant, meta=D.variants[v];
  const prof=D.profiles.find(p=>p.model===v);
  let h=`<div class="bar"><span class="meta">variant</span>
    <select id="vsel">${vids.map(x=>`<option value="${x}"${x===v?' selected':''}>${esc(D.variants[x].label)}</option>`).join('')}</select></div>`;
  h+=`<div class="card"><div class="meta">${esc(meta.model)} · ${esc(meta.intent)}</div>
      <div class="eyebrow" style="margin-top:10px">system prompt</div>
      <div class="prompt">${esc(meta.system_prompt)}</div>`;
  if(prof) h+=`<div class="char" style="margin-top:12px"><b>Storyteller profile:</b> ${esc(prof.characterization)}</div>`;
  h+=`</div>`;
  for(const [label,src] of [['Pre-launch — offline',OFF],['Live — online',ON]]){
    const rows=D.grades.filter(g=>g.variant_id===v&&src.has(g.source));
    if(!rows.length) continue;
    h+=`<div class="phase">${label}</div><table><tr><th>dimension</th><th>role</th>
        <th class="r">value</th><th>rank in field</th><th>reading</th></tr>`;
    for(const g of rows){
      const peers=D.grades.filter(x=>x.dimension===g.dimension&&x.value!=null).map(x=>x.value).sort((a,b)=>a-b);
      const rank=peers.indexOf(g.value)+1;
      h+=`<tr><td class="dimname">${esc(g.dimension)}</td><td>${roleTag(g.role)}</td>
        <td class="r val num">${fmt(g.value)}</td>
        <td class="note num">${rank}/${peers.length}</td>
        <td class="note">${esc((g.caveats||[''])[0].slice(0,60))}</td></tr>`;
    }
    h+=`</table>`;
  }
  return h;
}

function compare(){
  let h=`<div class="bar"><span class="meta">compare</span>`+
    vids.map(v=>`<span class="chk${state.cmp.has(v)?' on':''}" data-v="${v}">${esc(D.variants[v].label)}</span>`).join('')+`</div>`;
  const sel=vids.filter(v=>state.cmp.has(v));
  if(sel.length<1){return h+`<div class="note">select at least one variant.</div>`}
  for(const [label,src] of [['Pre-launch — offline',OFF],['Live — online',ON]]){
    const dims=dimsOf(src); if(!dims.length) continue;
    h+=`<div class="phase">${label}</div><table><tr><th>dimension</th><th>role</th>`+
       sel.map(v=>`<th class="r">${esc(D.variants[v].label)}</th>`).join('')+
       (sel.length>1?`<th class="r">Δ max−min</th>`:'')+`</tr>`;
    for(const dim of dims){
      const gs=sel.map(v=>grade(dim,v)); const g0=gs.find(Boolean); if(!g0) continue;
      const vals=gs.map(g=>g?g.value:null).filter(x=>x!=null);
      const best=lowerBetter.has(dim)?Math.min(...vals):Math.max(...vals);
      const mx=Math.max(...vals.map(Math.abs))||.001;
      h+=`<tr><td class="dimname">${esc(dim)}</td><td>${roleTag(g0.role)}</td>`+
        gs.map(g=>{if(!g)return '<td class="r note">—</td>';
          const lead=g.value===best?'<span class="lead">lead</span>':'';
          return `<td class="r"><span class="val num">${fmt(g.value)}</span>${lead}<br>${bar(g.value,mx,color(g0.role))}</td>`}).join('')+
        (sel.length>1?`<td class="r num note">${vals.length>1?fmt(Math.max(...vals)-Math.min(...vals)):'—'}</td>`:'')+`</tr>`;
    }
    h+=`</table>`;
  }
  return h;
}

function render(){
  document.querySelectorAll('.nav button').forEach(b=>b.classList.toggle('on',b.dataset.view===state.view));
  const el=document.getElementById('view');
  el.innerHTML = state.view==='overview'?overview():state.view==='detail'?detail():compare();
  if(state.view==='detail'){document.getElementById('vsel').onchange=e=>{state.variant=e.target.value;render()}}
  if(state.view==='compare'){el.querySelectorAll('.chk').forEach(c=>c.onclick=()=>{
    const v=c.dataset.v; state.cmp.has(v)?state.cmp.delete(v):state.cmp.add(v); render()})}
}
document.querySelectorAll('.nav button').forEach(b=>b.onclick=()=>{state.view=b.dataset.view;render()});
render();
"""

    cannot = "".join(f"<li>{_e(x)}</li>" for x in payload["cannot_measure"])
    body = (
        f'<div id="app"><style>{_CSS}</style><div class="wrap">'
        f'<div class="eyebrow">Companion variant evaluation · one platform</div>'
        f'<h1>{_e(payload["title"])}</h1>'
        f'<div class="sub">variants {_e(", ".join(v["label"] for v in variants.values()))} · '
        f'evaluators {_e(", ".join(payload["evaluators"]))} · {_e(payload["created"])}</div>'
        f'<div class="nav">'
        f'<button data-view="overview" class="on">Overview</button>'
        f'<button data-view="detail">By variant</button>'
        f'<button data-view="compare">Compare</button></div>'
        f'<div id="view"></div>'
        f'<div class="warn"><b>Provenance.</b> Offline compute grades are real measurements on '
        f'real Claude output; offline judge/psychometric grades are real Claude judging. Online '
        f'grades are from <b>faked user traffic</b> — the pipeline is real, the behaviour is '
        f'simulated to exercise the platform.</div>'
        f'<div class="cannot"><div class="eyebrow">What this cannot measure</div>'
        f'<ul>{cannot}</ul></div>'
        f'</div>'
        f'<script type="application/json" id="data">{data}</script>'
        f'<script>{js}</script></div>')

    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return str(p)
