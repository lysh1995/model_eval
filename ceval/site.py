"""The local platform site — 4 pages, served by `ceval serve`, rendered fresh from the DB.

  /          ① Data     — every test input: models, prompts, offline dialogues, online sessions
  /run       ② Run      — the CLI + a live form: pick model + prompt → trigger eval → see output
  /compare   ③ Compare  — the cross-compare grade book (headline = storytelling craft)
  /variant   ④ Detail   — drill into one variant (from ③): score, prompt, evidence, drill-down

Reuses the dashboard's styling and matrix/detail renderers so the look is one system.
"""
from __future__ import annotations
import html as _html
from typing import Optional

from .store import Store
from .dashboard.interactive import _CSS, _matrix, _detail, _e, _fmt
from .report import _prep

NAV = [("/", "① Data"), ("/run", "② Run eval"), ("/compare", "③ Compare"), ("/variant", "④ Detail")]

_SITE_CSS = """
.nav{display:flex;gap:4px;background:var(--line);padding:4px;border-radius:11px;width:fit-content;
max-width:100%;margin:2px 0 18px;flex-wrap:wrap}
.nav a{font-size:13px;font-weight:600;color:var(--muted);padding:7px 15px;border-radius:8px;
text-decoration:none;white-space:nowrap}
.nav a:hover{color:var(--ink)}
.nav a.on{background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
.sec{margin:24px 0}
.sec-h{font-size:12px;font-weight:700;color:var(--ink);letter-spacing:.02em;margin:0 0 4px}
.sec-d{font-size:11.5px;color:var(--muted);margin:0 0 10px}
.tag{display:inline-block;font-size:10px;font-family:ui-monospace,Menlo,monospace;color:var(--signal);
background:var(--signal-soft);padding:1px 7px;border-radius:5px}
.mono{font-family:ui-monospace,Menlo,monospace;font-size:12px}
.cli{background:#161b22;color:#e6e9ee;border-radius:10px;padding:14px 16px;font-family:ui-monospace,Menlo,monospace;
font-size:12px;line-height:2;white-space:pre;overflow-x:auto;display:block}
.cli b{color:#5cc295;font-weight:600}
.cli .c{color:#8a94a3}
.chips{display:flex;flex-wrap:wrap;gap:7px;margin:6px 0 16px}
.chip{font-size:12.5px;font-weight:600;color:var(--ink);background:var(--panel);border:1px solid var(--line);
border-radius:9px;padding:8px 13px;text-decoration:none;box-shadow:var(--shadow)}
.chip:hover{border-color:var(--signal);color:var(--signal)}
.chip.on{background:var(--pass-soft);border-color:var(--pass);color:var(--ink)}
form.run{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;
box-shadow:var(--shadow);margin:4px 0 18px;display:flex;gap:14px;flex-wrap:wrap;align-items:flex-end}
form.run label{display:flex;flex-direction:column;gap:5px;font-size:11px;font-weight:700;color:var(--faint);
text-transform:uppercase;letter-spacing:.05em}
form.run select,form.run input{font-size:13px;padding:8px 11px;border:1px solid var(--line);border-radius:8px;
background:var(--paper);color:var(--ink);min-width:180px}
form.run button{font-size:13px;font-weight:700;color:#fff;background:var(--signal);border:0;border-radius:8px;
padding:10px 20px;cursor:pointer}
form.run button:hover{filter:brightness(1.08)}
.out{background:var(--panel);border:1px solid var(--pass);border-radius:12px;padding:16px 18px;margin:4px 0}
a.back{font-size:12px;color:var(--signal);text-decoration:none}
"""


def shell(active: str, h1: str, sub: str, body: str) -> str:
    nav = "".join(
        f'<a href="{p}" class="{"on" if p == active else ""}">{_e(t)}</a>' for p, t in NAV)
    return (f"<style>{_CSS}{_SITE_CSS}</style>"
            f'<div id="app"><div class="wrap">'
            f'<div class="eyebrow">COMPANION VARIANT EVALUATION · ONE PLATFORM</div>'
            f'<nav class="nav">{nav}</nav>'
            f"<h1>{_e(h1)}</h1><div class=\"sub\">{_e(sub)}</div>{body}</div></div>")


def _table(headers, rows) -> str:
    h = "".join(f"<th>{_e(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<table><tr>{h}</tr>{body}</table>'


# ── ① DATA ───────────────────────────────────────────────────────────────────
def page_data(store: Store) -> str:
    models = store.list_models()
    prompts = store.list_prompts()
    variants = store.list_variants()
    chars = store.characters()
    sessions = store.all_sessions()
    body = []

    body.append('<div class="sec"><div class="sec-h">Models under test</div>'
                '<div class="sec-d">the base models a variant can run on — content-addressed by name+params</div>'
                + _table(["id", "name", "provider"],
                         [(f'<span class="tag">{_e(m["id"])}</span>', _e(m["name"]), _e(m["provider"]))
                          for m in models]) + "</div>")

    body.append('<div class="sec"><div class="sec-h">System prompts</div>'
                '<div class="sec-d">the prompt half of a variant — content-addressed by its text, so one prompt is shared across models</div>'
                + _table(["id", "name", "intent", "prompt (start)"],
                         [(f'<span class="tag">{_e(p["id"])}</span>', _e(p["name"]),
                           _e((p.get("intent") or "")[:40]),
                           f'<span class="mono">{_e((p["system_prompt"] or "")[:70])}…</span>')
                          for p in prompts]) + "</div>")

    dcounts = {}
    for v in variants:
        dcounts[v["id"]] = len(store.dialogues_for(v["id"]))
    body.append('<div class="sec"><div class="sec-h">Offline test data — dialogues</div>'
                f'<div class="sec-d">{sum(dcounts.values())} dialogues (a variant playing a character, turn by turn) over '
                f'{len(chars)} characters — the pre-launch benchmark content</div>'
                + _table(["variant", "model × prompt", "dialogues"],
                         [(_e(v.get("label") or v["id"]),
                           f'{_e(v.get("model_name",""))} × {_e(v.get("prompt_name",""))}',
                           f'{dcounts[v["id"]]} / {len(chars)} chars')
                          for v in variants])
                + '<div class="sec-d" style="margin-top:8px">characters: '
                + " · ".join(f'{_e(c["name"])} <span class="tag">{_e(cid)}</span>'
                             for cid, c in chars.items()) + "</div></div>")

    # online sessions — the user-behaviour data points we generated
    from collections import Counter
    byv = Counter(r["variant_id"] for r in sessions)
    byarm = Counter(r["arm"] for r in sessions)
    sample = sessions[:6]
    def sig(r, k, f="{}"):
        return f.format(r["signals"].get(k, "—"))
    srows = [(_e(r["variant_id"]), _e(r["character_id"]), _e(r["arm"]),
              sig(r, "n_turns"), sig(r, "follow_up_rate", "{:.2f}") if isinstance(r["signals"].get("follow_up_rate"), (int, float)) else "—",
              sig(r, "votes_favor"), f'{r["signals"].get("user_cocreation", 0):.2f}',
              "yes" if r["signals"].get("abandoned") else "no")
             for r in sample]
    body.append('<div class="sec"><div class="sec-h">Online dataset — user-behaviour data points</div>'
                f'<div class="sec-d">{len(sessions)} simulated production sessions '
                f'({byarm.get("randomized_default",0)} randomised · {byarm.get("self_selected",0)} self-selected). '
                'Each is one faked user interaction: response times, votes, follow-ups, regenerates, '
                'abandonment, co-creation — the retrievable data the online half grades.</div>'
                + '<div class="sec-d">sessions per variant — ' + " · ".join(
                    f'{_e(v)}: <b>{n}</b>' for v, n in byv.most_common()) + "</div>"
                + _table(["variant", "character", "arm", "turns", "follow_up", "votes", "co-create", "abandoned"], srows)
                + '<div class="note" style="margin-top:6px">showing 6 of '
                f'{len(sessions)} — full stream at <span class="mono">/api/grades.json</span> and the DB '
                '<span class="mono">sessions</span> table</div></div>')

    return shell("/", "① Test data — the inputs",
                 "every input the platform evaluates: models, prompts, offline dialogues, and the online behaviour dataset",
                 "".join(body))


# ── ② RUN ────────────────────────────────────────────────────────────────────
def page_run(store: Store, output: Optional[str] = None) -> str:
    models = store.list_models()
    prompts = store.list_prompts()
    mopt = "".join(f'<option value="{_e(m["id"])}">{_e(m["name"])}</option>' for m in models)
    popt = "".join(f'<option value="{_e(p["id"])}">{_e(p["name"])}</option>' for p in prompts)
    cli = ('<div class="cli">'
           '<b>ceval</b> init  <span class="c"># create the local DB (SQLite, 9 tables)</span>\n'
           '<b>ceval</b> seed  <span class="c"># load the demo → DB</span>\n'
           '<b>ceval</b> model add   --name gpt-5.1 --provider openrouter\n'
           '<b>ceval</b> prompt add  --name Playful --prompt "..."\n'
           '<b>ceval</b> variant add --model-id m_... --prompt-id p_...\n'
           '<b>ceval</b> eval run  <span class="c"># offline judge + online sessions → grade book</span>\n'
           '<b>ceval</b> serve     <span class="c"># this 4-page site</span>'
           '</div><div class="note" style="margin-top:6px">'
           '<span class="mono">ceval</span> = <span class="mono">python3 -m ceval</span></div>')
    form = (f'<form class="run" method="post" action="/api/eval">'
            f'<label>Model<select name="model_id">{mopt}</select></label>'
            f'<label>System prompt<select name="prompt_id">{popt}</select></label>'
            f'<label>Label (optional)<input name="label" placeholder="My variant"></label>'
            f'<button type="submit">▶ Run evaluation</button></form>')
    out = f'<div class="out">{output}</div>' if output else (
        '<div class="note">Pick a model + prompt and hit <b>Run evaluation</b>. '
        'The server evaluates it (offline judge where data exists + online behaviour) and shows the '
        'result here, with a link to its detail page. Re-running is idempotent.</div>')
    body = ('<div class="sec"><div class="sec-h">The CLI — the same surface, headless</div>'
            '<div class="sec-d">everything the buttons do is one command; the whole loop runs from the terminal</div>'
            + cli + "</div>"
            '<div class="sec"><div class="sec-h">Live: select → trigger → review</div>'
            + form + out + "</div>")
    return shell("/run", "② Run an evaluation",
                 "select a model and a system prompt, trigger the eval, and review the grade book output",
                 body)


def eval_output(store: Store, vid: str, log: str) -> str:
    """The result panel shown on ② Run after an eval is triggered."""
    v = store.variant(vid) or {}
    grades = [g for g in store.grades() if g["variant_id"] == vid]
    off = [g for g in grades if g["phase"] == "offline"]
    on = [g for g in grades if g["phase"] == "online" and g.get("segment") == "randomised_arm"]

    def rows(gs):
        if not gs:
            return '<tr><td class="note">— none —</td></tr>'
        return "".join(
            f'<tr><td class="dimname">{_e(g["dimension"])}</td>'
            f'<td><span class="role role-{g["role"]}">{g["role"]}</span></td>'
            f'<td class="r val num">{_fmt(g["value"])}</td></tr>' for g in gs)

    craft = next((g["value"] for g in grades if g["dimension"] == "narrative_craft"), None)
    head = (f'<div class="hq"><span class="hq-label">Storytelling quality</span>'
            f'<span class="hq-val">{_fmt(craft)}</span>'
            f'<span class="hq-rank">headline score</span></div>' if craft is not None else
            '<div class="note" style="margin:8px 0">No offline judge score yet — a new model×prompt '
            'has no generated dialogues, so only the online behaviour grades below appear. '
            'Generate data with <span class="mono">ceval data gen</span> to get the craft score.</div>')
    return (f'<b>✓ Evaluated {_e(v.get("label") or vid)}</b> <span class="tag">{_e(vid)}</span> — '
            f'{_e(v.get("model_name",""))} × {_e(v.get("prompt_name",""))}{head}'
            f'<div class="sec-d" style="margin-top:10px">OFFLINE (pre-launch judge)</div>'
            f'<table>{rows(off)}</table>'
            f'<div class="sec-d" style="margin-top:12px">ONLINE (behaviour · randomised arm)</div>'
            f'<table>{rows(on)}</table>'
            f'<a class="chip" style="display:inline-block;margin-top:14px" '
            f'href="/variant?id={_e(vid)}">Open full detail ④ →</a>'
            f'<details style="margin-top:10px"><summary class="note">run log</summary>'
            f'<pre class="cli">{_e(log.strip())}</pre></details>')


# ── ③ COMPARE ────────────────────────────────────────────────────────────────
def _prep_grades(store):
    gb, variants, profiles, evidence, sessions = _prep(store)
    gd = gb.to_dict()
    grades = [g for g in gd["grades"] if g.get("segment") != "self_selected_arm"]
    profiles = [p.to_row() if hasattr(p, "to_row") else p for p in profiles]
    return grades, variants, profiles, evidence, sessions


def page_compare(store: Store) -> str:
    grades, variants, profiles, evidence, sessions = _prep_grades(store)
    vids = list(variants)
    if not grades:
        return shell("/compare", "③ Cross-compare", "no grades yet",
                     '<div class="note">Run an evaluation first — <a href="/run">② Run eval</a>.</div>')
    chips = "".join(f'<a class="chip" href="/variant?id={_e(v)}">{_e(variants[v]["label"])} →</a>' for v in vids)
    body = ('<div class="hint">Click a variant to drill into its full profile ④ ▸</div>'
            f'<div class="chips">{chips}</div>' + _matrix(grades, variants, vids))
    return shell("/compare", "③ Cross-compare — the grade book",
                 "offline (pre-launch) + online (production-like) for every variant, in one artifact", body)


# ── ④ DETAIL ─────────────────────────────────────────────────────────────────
def page_variant(store: Store, vid: str) -> str:
    grades, variants, profiles, evidence, sessions = _prep_grades(store)
    if vid not in variants:
        return shell("/variant", "④ Detail", "unknown variant",
                     '<a class="back" href="/compare">← back to compare</a>')
    picker = "".join(
        f'<a class="chip {"on" if v == vid else ""}" href="/variant?id={_e(v)}">{_e(variants[v]["label"])}</a>'
        for v in variants)
    body = ('<a class="back" href="/compare">← back to ③ Compare</a>'
            f'<div class="chips" style="margin-top:10px">{picker}</div>'
            + _detail(grades, variants, vid, profiles, evidence, sessions))
    return shell("/variant", f"④ {variants[vid]['label']} — detail",
                 "the headline storytelling score, the system prompt, good/bad examples, and the online drill-down", body)
