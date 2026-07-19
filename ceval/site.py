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

NAV = [("/", "① Data"), ("/run", "② Run eval"), ("/compare", "③ Compare"),
       ("/variant", "④ Detail"), ("/design", "⑤ Design")]

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
details.dlg{border:1px solid var(--line);border-radius:10px;background:var(--panel);margin:7px 0;padding:0 15px;box-shadow:var(--shadow)}
details.dlg summary{cursor:pointer;font-size:12.5px;font-weight:600;padding:12px 0;color:var(--ink);list-style:none}
details.dlg summary::-webkit-details-marker{display:none}
details.dlg summary::before{content:"▸ ";color:var(--signal)}
details.dlg[open] summary::before{content:"▾ "}
.thread{padding:2px 0 14px}
.turn{font-size:12.5px;line-height:1.5;padding:8px 12px;margin:6px 0;border-radius:10px;max-width:86%}
.turn .who{display:block;font-size:8.5px;font-weight:700;letter-spacing:.07em;color:var(--faint);margin-bottom:3px}
.turn.u{background:var(--line2);margin-left:14%}
.turn.a{background:var(--signal-soft)}
.turn.a .who{color:var(--signal)}
h2{font-size:16px;font-weight:680;margin:32px 0 6px;padding-top:6px;border-bottom:2px solid var(--line);padding-bottom:6px}
.lead{font-size:13px;color:var(--muted);line-height:1.55;margin:6px 0 4px}
.toc{display:flex;flex-wrap:wrap;gap:7px;margin:6px 0 8px}
.toc a{font-size:12px;font-weight:600;color:var(--signal);background:var(--signal-soft);padding:6px 12px;border-radius:8px;text-decoration:none}
.flow{display:flex;flex-wrap:wrap;align-items:stretch;gap:0;margin:12px 0}
.fbox{flex:1;min-width:150px;background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:12px 15px;box-shadow:var(--shadow)}
.fbox .k{font-size:9.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--signal);margin-bottom:5px}
.fbox .d{font-size:12px;color:var(--ink);line-height:1.45}
.farrow{display:flex;align-items:center;padding:0 9px;color:var(--faint);font-size:19px;font-weight:700}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:12px 0}
.cat{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:14px 16px;box-shadow:var(--shadow)}
.cat h4{margin:0;font-size:14px}.cat .lvl{font-size:10px;font-weight:700;color:var(--faint);text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.dim{font-size:12px;padding:6px 0;border-top:1px solid var(--line2);display:flex;justify-content:space-between;align-items:center;gap:8px}
.step{display:flex;gap:13px;padding:13px 0;border-top:1px solid var(--line2)}
.step .n{flex:0 0 27px;height:27px;border-radius:50%;background:var(--signal);color:#fff;font-weight:700;font-size:13px;display:flex;align-items:center;justify-content:center}
.step .b{font-size:12.5px;line-height:1.5;color:var(--muted)}.step .b b{color:var(--ink)}
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


def _thread(turns, cap=360) -> str:
    """Render a dialogue's turns as a chat thread (user right, AI/character left)."""
    out = []
    for t in turns:
        u = t.get("role") == "user"
        txt = t.get("text", "")
        txt = txt if len(txt) <= cap else txt[:cap] + "…"
        out.append(f'<div class="turn {"u" if u else "a"}">'
                   f'<span class="who">{"USER" if u else "CHARACTER"}</span>{_e(txt)}</div>')
    return f'<div class="thread">{"".join(out)}</div>'


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

    # OFFLINE DIALOGUES — the actual transcripts (a variant playing a character, turn by turn)
    dcounts = {v["id"]: len(store.dialogues_for(v["id"])) for v in variants}
    threads = []
    for v in variants:
        dl = store.dialogues_for(v["id"])
        if not dl:
            continue
        d = dl[0]                                  # one sample transcript per variant
        cname = chars.get(d["character_id"], {}).get("name", d["character_id"])
        nturns = len(d["turns"])
        threads.append(
            f'<details class="dlg"><summary>{_e(v.get("label") or v["id"])} playing '
            f'<b>{_e(cname)}</b> · {nturns} turns · <span class="tag">{_e(d["character_id"])}</span>'
            f'</summary>{_thread(d["turns"])}</details>')
    body.append('<div class="sec"><div class="sec-h">Offline dataset — dialogues (transcripts)</div>'
                f'<div class="sec-d">{sum(dcounts.values())} dialogues over {len(chars)} characters — '
                'each is a variant playing a character turn by turn (real Claude output). This is the '
                'pre-launch benchmark content the offline judge grades. '
                f'Characters: {" · ".join(_e(c["name"]) for c in chars.values())}. '
                'Click a row to read the actual conversation:</div>'
                + "".join(threads) + "</div>")

    # ONLINE DATASET — the fake user-behaviour data we injected
    from collections import Counter
    byv = Counter(r["variant_id"] for r in sessions)
    byarm = Counter(r["arm"] for r in sessions)
    def g(sg, k, f=None, d="—"):
        v = sg.get(k)
        if v is None:
            return d
        return (f.format(v) if f else str(v))
    srows = [(f'<span class="tag">{_e(r["variant_id"])}</span>', _e(r["character_id"]),
              _e(r["arm"].replace("_", " ")), g(r["signals"], "n_turns"),
              g(r["signals"], "total_latency_ms", "{:.0f}ms"),
              g(r["signals"], "follow_up_rate", "{:.2f}"),
              g(r["signals"], "regenerates"), g(r["signals"], "votes_favor"),
              g(r["signals"], "user_cocreation", "{:.2f}"),
              "yes" if r["signals"].get("abandoned") else "no")
             for r in sessions[:10]]
    body.append('<div class="sec"><div class="sec-h">Online dataset — injected fake user-behaviour data points</div>'
                f'<div class="sec-d"><b>{len(sessions)} simulated production sessions</b> '
                f'({byarm.get("randomized_default",0)} randomised-default · {byarm.get("self_selected",0)} self-selected arm). '
                'There is no real product behind this, so we <b>inject fake user traffic</b> with a known '
                'structure — response times, up/down votes, model selection (arm), regenerates, abandonment, '
                'follow-ups, and story co-creation — so the retrieve→grade pipeline can be built and tested. '
                'These are the online data points the live half grades.</div>'
                + '<div class="sec-d">sessions per variant — ' + " · ".join(
                    f'{_e(v)}: <b>{n}</b>' for v, n in byv.most_common()) + "</div>"
                + _table(["variant", "character", "arm", "turns", "latency", "follow_up",
                          "regen", "votes↑", "co-create", "abandon"], srows)
                + f'<div class="note" style="margin-top:6px">showing 10 of {len(sessions)} — '
                'all live in the DB <span class="mono">sessions</span> table, retrieved fresh on every page load.</div></div>')

    return shell("/", "① Test data — the inputs",
                 "everything the platform evaluates, live from the local DB: models, prompts, offline "
                 "dialogue transcripts, and the injected online behaviour dataset",
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


# ── ⑤ DESIGN / KNOWLEDGE ─────────────────────────────────────────────────────
_LANE_BADGE = {"compute": "role-guide", "psychometric": "role-headline", "judge": "role-trap"}
_CLASS_BADGE = {"diagnostic": "role-guide", "monitor": "role-headline",
                "trap": "role-trap", "confound": "role-gate"}


def _fbox(k, d):
    return f'<div class="fbox"><div class="k">{_e(k)}</div><div class="d">{d}</div></div>'


def _flow(*boxes):
    inner = '<div class="farrow">→</div>'.join(boxes)
    return f'<div class="flow">{inner}</div>'


def page_design(store: Store) -> str:
    from .offline.scheme import SCHEME, FILTERS
    from .online.signals import SIGNALS
    from collections import OrderedDict

    toc = ('<div class="toc">'
           '<a href="#svc">Service design</a><a href="#flow">Data flows</a>'
           '<a href="#cat">Categories</a><a href="#grade">Grading criteria</a>'
           '<a href="#online">Online data points</a><a href="#prod">→ Production</a></div>')

    # ── service design ──
    svc = ('<h2 id="svc">Service design</h2>'
           '<div class="lead">Scale is plumbing; the hard part is a <b>trustworthy number</b>. So the '
           '<b>grade book</b> is the core artifact — one row per (variant × dimension × phase) carrying '
           'its value, role, interval, evaluator, and what it <i>refuses</i> to claim. Offline (pre-launch) '
           'and online (production-like) emit the <b>same grade book</b>, joined by one registry, one '
           'stats engine, one DB. The whole loop runs headless from one CLI.</div>'
           + _flow(
               _fbox("Input", "model + params + system prompt = a <b>variant</b> "
                              "(content-addressed). Injected by CLI or the ② Run form."),
               _fbox("Domain — the grade book", "the dimension catalogue × the scoring lanes → "
                                                "<b>grades + evidence</b>, persisted in the DB with full lineage."),
               _fbox("Output", "the 4-page site + JSON API — cross-compare, drill-down, ship view.")))

    # ── data flows ──
    flow = ('<h2 id="flow">Data flows</h2>'
            '<div class="lead"><b>Offline</b> — the pre-launch benchmark gate:</div>'
            + _flow(
                _fbox("variant", "model × prompt"),
                _fbox("generate", "play the characters turn-by-turn → dialogues"),
                _fbox("store", "dialogues → DB"),
                _fbox("score", "compute · psychometric · <b>judge</b> lanes"),
                _fbox("grade book", "grades + evidence"))
            + '<div class="lead" style="margin-top:14px"><b>Online</b> — production-like monitoring:</div>'
            + _flow(
                _fbox("variant", "served to traffic"),
                _fbox("collect", "sessions: votes, latency, follow-up, regenerate, co-creation…"),
                _fbox("store", "sessions → DB"),
                _fbox("grade", "diagnostics (act on) · traps (walled off) · per-arm"),
                _fbox("grade book", "same shape as offline")))

    # ── categories (from SCHEME, grouped by ability level) ──
    levels = OrderedDict()
    for d in SCHEME:
        levels.setdefault(d.level.value, []).append(d)
    cards = []
    for lvl, dims in levels.items():
        rows = "".join(
            f'<div class="dim"><span class="dimname">{_e(d.key)}</span>'
            f'<span><span class="role {_LANE_BADGE.get(d.lane.value,"role-guide")}">{_e(d.lane.value)}</span> '
            f'<span class="role {"role-gate" if d.gates else "role-guide"}">{"gate" if d.gates else "guide"}</span></span></div>'
            for d in dims)
        cards.append(f'<div class="cat"><div class="lvl">{_e(lvl)}</div>{rows}</div>')
    cat = ('<h2 id="cat">Categories</h2>'
           '<div class="lead">Every dimension is placed on two axes. <b>Ability level</b> — what it tests: '
           'L1 comprehension → L2 application &amp; steerability → L3 craft (the product core) → safety. '
           '<b>Lane</b> — the mechanism: <span class="role role-guide">compute</span> (deterministic, no '
           'model call) · <span class="role role-headline">psychometric</span> (self-validating, no ground '
           'truth) · <span class="role role-trap">judge</span> (LLM, bounded question). Lane ≠ Level — the '
           'judge spans every level. <b>Role</b> — <span class="role role-gate">gate</span> can block a ship, '
           '<span class="role role-guide">guide</span> informs a human, <span class="role role-trap">trap</span> '
           'is collected but never a grade.</div>'
           f'<div class="grid">{"".join(cards)}</div>')

    # ── grading criteria (the 6-filter kill-pipeline + per-dim validate/score) ──
    filt = "".join(f'<div class="step"><div class="n">{i+1}</div><div class="b">{_e(f)}</div></div>'
                   for i, f in enumerate(FILTERS))
    grows = [(f'<span class="dimname">{_e(d.key)}</span>', _e(d.validate), _e(d.score),
              " ".join(str(x) for x in d.filters_passed)) for d in SCHEME]
    grade = ('<h2 id="grade">Grading criteria</h2>'
             '<div class="lead">A candidate dimension must survive a <b>6-filter kill-pipeline</b> (cheapest '
             'kill first) before any measurement is built — this is a method, not a brainstorm:</div>'
             + filt
             + '<div class="lead" style="margin-top:14px">And each surviving dimension declares exactly how it '
             'is validated and scored (filters it passed shown at right):</div>'
             + _table(["dimension", "how it's validated", "how it's scored", "filters"], grows))

    # ── online user data points (from SIGNALS) ──
    orows = []
    for s in SIGNALS.values():
        orows.append((
            f'<span class="dimname">{_e(s.name)}</span>',
            f'<span class="role {"role-guide" if s.feedback.value=="direct" else "role-headline" if s.feedback.value=="indirect" else "role-trap"}">{_e(s.feedback.value)}</span>',
            f'<span class="role {_CLASS_BADGE.get(s.signal_class.value,"role-guide")}">{_e(s.signal_class.value)}</span>',
            _e(s.proxies_for), _e(s.gameable_by[:70])))
    online = ('<h2 id="online">Online user data points we designed</h2>'
              '<div class="lead">The online half estimates the <b>user\'s opinion</b> of a variant from behaviour. '
              'Each signal is tagged by <b>how the feedback reaches us</b> — '
              '<span class="role role-guide">direct</span> (explicit: votes, regenerate, edit) vs '
              '<span class="role role-headline">indirect</span> (implicit: follow-up, abandonment, co-creation) — '
              'and whether it is safe to act on: <span class="role role-guide">diagnostic</span> · '
              '<span class="role role-headline">monitor</span> · <span class="role role-trap">trap</span> '
              '(collect, never optimise) · <span class="role role-gate">confound</span>. '
              'The load-bearing rule: <b>direct approval (votes) is a trap</b> — optimising thumbs-up is exactly '
              'how sycophancy shipped. We infer opinion from indirect health + direct <i>rejection</i> instead.</div>'
              + _table(["signal", "feedback", "class", "proxies for", "gameable by"], orows))

    # ── wiring into production ──
    steps = [
        ("<b>Collection contract</b> — there is no app behind the demo, so the product must emit it: a "
         "per-turn <span class='mono'>GenerationEvent</span> + per-session <span class='mono'>SessionEvent</span> "
         "(OpenTelemetry <span class='mono'>gen_ai.*</span> + our <span class='mono'>eval.*</span> fields — "
         "variant_id, distance_to_anchor, assignment_arm, finish_reason). A refusal is a <i>missing</i> "
         "observation, not a zero; the assignment arm can't be reconstructed later."),
        ("<b>Tier the lanes for 50M generations/day</b> — Lane 0 safety inline (5–50ms, 100%); Lanes 1–2 "
         "compute at 100% (free, async); the <b>judge (Lane 3) on a ~1% stratified sample</b>. Measured: "
         "$283k/yr tiered vs $26.9M/yr judging everything — a 95× reduction, and latency (not cost) is what "
         "forces it."),
        ("<b>Anchor the online proxies to the judge</b> — behavioural signals (e.g. story-cocreation for craft) "
         "are cheap proxies at 100%; they only <i>earn their place</i> once validated against the judge sample "
         "and past the sycophancy acid test (must rank the vote-gamer low). Re-fit on drift."),
        ("<b>Swap SQLite → MySQL</b> — one schema, two drivers; the DDL is written. Content-addressed ids and a "
         "versioned evaluator make a judge-version bump a breaking change, never a silent rescale."),
        ("<b>Wire safety to escalation, not a counter</b> — crisis detection routes to a human with an audit "
         "trail; over-refusal is a first-class defect measured alongside harm, never averaged into quality."),
        ("<b>Ship on evidence, with a human veto</b> — shadow → canary → live; the gate compares intervals "
         "(not point estimates) against the measured MDE, and a qualitative signal can block a green ship."),
    ]
    prod = ('<h2 id="prod">Wiring this into real production</h2>'
            '<div class="lead">Everything here runs locally on simulated traffic. The path to production is '
            'specified, not hand-wavy — the design already encodes it:</div>'
            + "".join(f'<div class="step"><div class="n">{i+1}</div><div class="b">{b}</div></div>'
                      for i, b in enumerate(steps))
            + '<div class="note" style="margin-top:12px">Deeper: '
            '<span class="mono">docs/GRADEBOOK.md</span> · <span class="mono">docs/SERVICE.md</span> · '
            '<span class="mono">docs/ONLINE.md</span> · <span class="mono">docs/PLATFORM.md</span></div>')

    return shell("/design", "⑤ Design & knowledge",
                 "the service design, data flows, dimension categories, grading criteria, the online "
                 "data points we designed, and how to wire this into real production",
                 toc + svc + flow + cat + grade + online + prod)
