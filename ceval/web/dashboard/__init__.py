"""Dashboard renderer: a GradeBook -> a fully static, self-contained HTML page.

Pure Python, zero dependencies, no client-side JS. The page is BAKED (styles + pre-rendered
HTML), so it renders anywhere -- a real browser, a static-snapshot preview, an email
attachment -- and cannot silently fail to execute.

DESIGN THESIS. The most characteristic thing about this platform is that it refuses to lie:
it walls traps off from verdicts, refuses to pool across languages, marks the self-selected
arm as non-causal, and states what it cannot measure. So the design is a CALIBRATION REPORT,
not a marketing dashboard -- an instrument readout. Numbers are monospaced and tabular;
semantic colour (critical / caution / pass) is kept separate from the structural accent; the
'cannot measure' panel is given the same visual weight as the results.
"""
from __future__ import annotations
import html as _html
import math
import pathlib
from typing import List, Optional, Union

from ...core.gradebook import GradeBook

# ── design tokens ──────────────────────────────────────────────────────────
# Instrument palette: petrol accent, semantic red/amber/green, cool-slate neutrals.
# Both themes defined at token level; components style through the tokens only.
_STYLE = r"""
:root{
  --paper:#f4f6f8; --panel:#ffffff; --ink:#161b22; --muted:#5b6675; --faint:#8a94a3;
  --line:#e3e7ec; --line2:#eef1f4;
  --signal:#0d6e82; --signal-soft:#e2f0f3;
  --critical:#b42318; --critical-soft:#fbeae8;
  --caution:#8a5a00; --caution-soft:#fbf1dd;
  --pass:#2f7d5b; --pass-soft:#e6f2ec;
  --shadow:0 1px 2px rgba(20,26,34,.04),0 1px 3px rgba(20,26,34,.06);
}
@media (prefers-color-scheme:dark){:root{
  --paper:#0e1116; --panel:#161b22; --ink:#e6e9ee; --muted:#9aa4b2; --faint:#68717f;
  --line:#232a33; --line2:#1b2129;
  --signal:#3bb7cf; --signal-soft:#123038;
  --critical:#f0776a; --critical-soft:#331916;
  --caution:#e0a53a; --caution-soft:#2c220f;
  --pass:#5cc295; --pass-soft:#12271e;
  --shadow:0 1px 2px rgba(0,0,0,.3);
}}
:root[data-theme="light"]{
  --paper:#f4f6f8; --panel:#ffffff; --ink:#161b22; --muted:#5b6675; --faint:#8a94a3;
  --line:#e3e7ec; --line2:#eef1f4;
  --signal:#0d6e82; --signal-soft:#e2f0f3;
  --critical:#b42318; --critical-soft:#fbeae8;
  --caution:#8a5a00; --caution-soft:#fbf1dd;
  --pass:#2f7d5b; --pass-soft:#e6f2ec; --shadow:0 1px 2px rgba(20,26,34,.05);
}
:root[data-theme="dark"]{
  --paper:#0e1116; --panel:#161b22; --ink:#e6e9ee; --muted:#9aa4b2; --faint:#68717f;
  --line:#232a33; --line2:#1b2129;
  --signal:#3bb7cf; --signal-soft:#123038;
  --critical:#f0776a; --critical-soft:#331916;
  --caution:#e0a53a; --caution-soft:#2c220f;
  --pass:#5cc295; --pass-soft:#12271e; --shadow:0 1px 2px rgba(0,0,0,.3);
}

#ceval-root{background:var(--paper);color:var(--ink);min-height:100%;
  font-family:ui-sans-serif,-apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;padding:40px 24px 64px;}
#ceval-root *{box-sizing:border-box}
.wrap{max-width:940px;margin:0 auto}
.mono{font-family:ui-monospace,"SF Mono","JetBrains Mono",Menlo,Consolas,monospace}
.num{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-variant-numeric:tabular-nums}

/* header */
.head{border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:8px}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--signal);
  font-weight:700;margin-bottom:8px}
.title{font-size:25px;font-weight:680;letter-spacing:-.01em;line-height:1.15;
  text-wrap:balance;margin:0}
.meta{margin-top:12px;font-size:11.5px;color:var(--muted);display:flex;flex-wrap:wrap;
  gap:4px 18px}
.meta b{color:var(--ink);font-weight:600}

/* legend */
.legend{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:12px;overflow:hidden;margin:26px 0 34px;
  box-shadow:var(--shadow)}
.tier{background:var(--panel);padding:16px 18px}
.tier .k{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:700;
  letter-spacing:.08em;text-transform:uppercase}
.tier .dot{width:9px;height:9px;border-radius:50%}
.tier .n{font-size:26px;font-weight:680;margin:6px 0 2px}
.tier .d{font-size:11.5px;color:var(--muted);line-height:1.45}
.k-gate{color:var(--critical)} .dot-gate{background:var(--critical)}
.k-guide{color:var(--signal)} .dot-guide{background:var(--signal)}
.k-trap{color:var(--caution)} .dot-trap{background:var(--caution)}

/* sections */
.sec{margin:34px 0}
.sec-h{display:flex;align-items:baseline;gap:12px;margin-bottom:4px}
.sec-h h2{font-size:13px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  margin:0;color:var(--ink)}
.sec-h .hint{font-size:11.5px;color:var(--faint)}
.rule{height:2px;background:var(--ink);margin-bottom:18px;opacity:.14}

.dim{margin:18px 0}
.dim-h{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.dim-h .name{font-size:13.5px;font-weight:640}
.lang{font-size:10px;font-weight:700;letter-spacing:.06em;background:var(--ink);
  color:var(--paper);padding:2px 7px;border-radius:5px}
.src{font-size:10px;color:var(--faint);border:1px solid var(--line);padding:1px 6px;
  border-radius:5px}

table{width:100%;border-collapse:collapse}
th{font-size:10.5px;letter-spacing:.04em;text-transform:uppercase;color:var(--faint);
  font-weight:600;text-align:left;padding:4px 10px 8px}
th.r,td.r{text-align:right}
td{padding:9px 10px;border-top:1px solid var(--line2);font-size:13px;vertical-align:middle}
tr:first-child td{border-top:1px solid var(--line)}
.variant{font-weight:560}
.lead{display:inline-block;font-size:9.5px;font-weight:700;letter-spacing:.04em;
  color:var(--pass);background:var(--pass-soft);padding:1px 6px;border-radius:4px;margin-left:8px}
.value{font-size:14px;font-weight:640}
.ci{color:var(--faint);font-size:11.5px}
.n{color:var(--muted);font-size:11px}
.note{color:var(--muted);font-size:11.5px;max-width:280px}
.track{height:6px;border-radius:3px;background:var(--line);position:relative;width:150px}
.track>i{position:absolute;left:0;height:100%;border-radius:3px}

/* trap section: visually recessed, hatched -- signals 'not a verdict' */
.trap-wrap{border:1px solid var(--caution);border-radius:12px;overflow:hidden;
  box-shadow:var(--shadow)}
.trap-bar{background:var(--caution-soft);padding:12px 18px;display:flex;align-items:center;
  gap:10px;border-bottom:1px solid var(--caution)}
.trap-bar .warn{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
  color:var(--caution)}
.trap-body{background:repeating-linear-gradient(45deg,var(--panel),var(--panel) 11px,
  var(--caution-soft) 11px,var(--caution-soft) 12px);padding:4px 18px 10px}
.trap-body p{font-size:11.5px;color:var(--muted);line-height:1.5;margin:12px 2px}
.trap-body table{background:var(--panel);border-radius:8px}

/* cannot-measure: equal weight to results -- the thesis */
.cannot{margin-top:38px;border:1px solid var(--line);border-left:3px solid var(--signal);
  border-radius:0 12px 12px 0;background:var(--panel);padding:20px 22px;box-shadow:var(--shadow)}
.cannot h2{font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin:0 0 4px;
  color:var(--signal)}
.cannot .lede{font-size:12px;color:var(--muted);margin-bottom:12px}
.cannot ul{margin:0;padding-left:18px}
.cannot li{font-size:12.5px;color:var(--ink);margin:7px 0;line-height:1.5}
.cannot li::marker{color:var(--signal)}

footer{margin-top:36px;padding-top:16px;border-top:1px solid var(--line);
  font-size:11px;color:var(--faint);line-height:1.6;max-width:70ch}

/* ability portrait -- the lede: what KIND of storyteller is this? */
.portraits{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:6px 0 8px}
@media(max-width:720px){.portraits{grid-template-columns:1fr}}
.card{border:1px solid var(--line);border-radius:12px;background:var(--panel);
  padding:16px 18px;box-shadow:var(--shadow)}
.card .m{font-size:14px;font-weight:660;letter-spacing:-.01em}
.card .char{font-size:12.5px;color:var(--ink);line-height:1.5;margin:7px 0 12px;
  min-height:38px;text-wrap:pretty}
.spine{display:flex;flex-direction:column;gap:7px}
.ax{display:grid;grid-template-columns:82px 1fr 34px;align-items:center;gap:9px}
.ax .lab{font-size:10px;color:var(--muted);text-align:right;line-height:1.2}
.ax .lay{font-size:8.5px;color:var(--faint);font-weight:700}
.ax .rail{height:5px;border-radius:3px;background:var(--line);position:relative}
.ax .rail>i{position:absolute;top:-2px;width:9px;height:9px;border-radius:50%;
  background:var(--signal);transform:translateX(-50%)}
.ax .rail.na{background:repeating-linear-gradient(90deg,var(--line),var(--line) 4px,
  transparent 4px,transparent 8px)}
.ax .v{font-size:10px;color:var(--muted);text-align:right}
.ax .v.na{color:var(--faint);font-style:italic}
.needjudge{margin:10px 0 24px;padding:11px 16px;border-radius:10px;
  background:var(--signal-soft);border:1px solid var(--signal);font-size:11.5px;
  color:var(--ink);line-height:1.5}
.needjudge b{color:var(--signal)}
"""


def _e(s) -> str:
    return _html.escape(str(s))


def _fmt(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:.3f}" if abs(v) < 1 else f"{v:.1f}"


def _sem(role: str) -> str:
    return {"gate": "critical", "guide": "signal", "trap": "caution"}.get(role, "signal")


def _tables(grades, role, langs, lower_is_better=True, sources=None):
    color = f"var(--{_sem(role)})"
    def ok(g):
        return sources is None or g.get("source") in sources
    out = []
    for lang in langs:
        dims = sorted({g["dimension"] for g in grades
                       if g["role"] == role and g["language"] == lang and ok(g)})
        for dim in dims:
            rows = [g for g in grades if g["dimension"] == dim and g["language"] == lang
                    and g["role"] == role and ok(g)
                    and g.get("segment") != "self_selected_arm"]
            if not rows:
                continue
            rows.sort(key=lambda r: r["value"] if r["value"] is not None else 0)
            mx = max((abs(r["value"] or 0) for r in rows), default=0.001) or 0.001
            best = rows[0]["variant_id"] if role == "gate" else None
            src = rows[0]["source"].replace("_", " ")
            body = [
                f'<div class="dim"><div class="dim-h"><span class="name">{_e(dim)}</span>'
                f'<span class="lang">{_e(lang)}</span><span class="src">{_e(src)}</span></div>',
                '<table><tr><th>variant</th><th class="r">value</th><th></th>'
                '<th>95% ci</th><th>n</th><th>reading</th></tr>']
            for r in rows:
                v = r["value"] or 0
                w = max(3, min(100, 100 * abs(v) / mx))
                iv = r.get("interval")
                ci = f'{_fmt(iv[0])} – {_fmt(iv[1])}' if iv else "—"
                lead = (f'<span class="lead">leads</span>'
                        if best and r["variant_id"] == best and role == "gate" else "")
                note = _e((r.get("caveats") or [""])[0][:66])
                body.append(
                    f'<tr><td class="variant">{_e(r["variant_id"])}{lead}</td>'
                    f'<td class="r value num">{_fmt(r["value"])}</td>'
                    f'<td><div class="track"><i style="width:{w:.0f}%;background:{color}"></i>'
                    f'</div></td>'
                    f'<td class="ci num">{ci}</td>'
                    f'<td class="n num">{r["n_effective"]}</td>'
                    f'<td class="note">{note}</td></tr>')
            body.append('</table></div>')
            out.append("".join(body))
    return "".join(out) or '<p class="note" style="padding:8px 10px">none in this book</p>'


def _portrait(profiles: list, lang: str) -> str:
    if not profiles:
        return ""
    cards = []
    for pr in profiles:
        spine = []
        for s in pr["signals"]:
            na = not s["measured"]
            pos = s["position"]
            dot = "" if (na or pos != pos) else \
                f'<i style="left:{max(3,min(97,100*pos)):.0f}%"></i>'
            rail = '<div class="rail na"></div>' if na else f'<div class="rail">{dot}</div>'
            if na:
                v = f'<span class="v na">judge</span>'
            elif s["value"] != s["value"]:
                v = '<span class="v na">n/a</span>'
            else:
                val = s["value"]
                v = f'<span class="v">{val:.2f}</span>' if abs(val) < 1 else \
                    f'<span class="v">{val:.0f}</span>'
            spine.append(
                f'<div class="ax"><span class="lab"><span class="lay">{s["layer"]}</span> '
                f'{_e(s["label"])}</span>{rail}{v}</div>')
        cards.append(
            f'<div class="card"><div class="m">{_e(pr["model"])}</div>'
            f'<div class="char">{_e(pr["characterization"])}</div>'
            f'<div class="spine">{"".join(spine)}</div></div>')
    return (
        f'<div class="sec"><div class="sec-h"><h2>What kind of storyteller is this?</h2>'
        f'<span class="hint">judge-free craft correlates · a portrait, not a ranking</span>'
        f'</div><div class="rule"></div>'
        f'<div class="needjudge"><b>Read this first.</b> These are the observable '
        f'<b>correlates</b> of storytelling craft — pacing, scene-driving, distinct voices, '
        f'freshness. They are not the aesthetic verdict. Whether the writing is actually '
        f'<b>intriguing</b> is perspectival (human agreement α = 0.25–0.34) and cannot be '
        f'settled judge-free; <b>L1 character comprehension</b> needs out-of-character probes. '
        f'Both need a judge, and ultimately real users. Bars show rank within the field.</div>'
        f'<div class="portraits">{"".join(cards)}</div></div>')


def _scheme_section(scheme) -> str:
    """Show WHAT was tested and HOW -- the test plan, organized by ability level.
    Makes the judge-spans-levels correction visible: the judge appears at L1, L2, L3."""
    if not scheme:
        return ""
    by_level = {}
    for d in scheme:
        by_level.setdefault(d.level.value, []).append(d)
    lane_color = {"compute": "var(--pass)", "psychometric": "var(--signal)", "judge": "var(--caution)"}
    blocks = []
    for level, dims in by_level.items():
        rows = "".join(
            f'<tr><td class="variant">{_e(d.key)}</td>'
            f'<td><span class="src" style="border-color:{lane_color.get(d.lane.value)};'
            f'color:{lane_color.get(d.lane.value)}">{_e(d.lane.value)}</span></td>'
            f'<td class="note">{_e(d.product_failure[:70])}</td>'
            f'<td class="n">{"".join(str(f) for f in d.filters_passed)}</td></tr>'
            for d in dims)
        blocks.append(
            f'<div class="dim"><div class="dim-h"><span class="name">{_e(level)}</span></div>'
            f'<table><tr><th>dimension</th><th>lane</th><th>catches (product failure)</th>'
            f'<th>filters ✓</th></tr>{rows}</table></div>')
    return (
        '<div class="sec"><div class="sec-h"><h2>Test scheme — what is measured, how</h2>'
        '<span class="hint">the judge (amber) spans L1 · L2 · L3 — lane ≠ level · '
        'filters = the 6-step kill-pipeline each dimension survived</span></div>'
        '<div class="rule"></div>' + "".join(blocks) + '</div>')


def render(gradebook: Union[GradeBook, dict], out_path: str,
           ability_profiles: Optional[list] = None, scheme=None) -> str:
    data = gradebook.to_dict() if isinstance(gradebook, GradeBook) else gradebook
    grades, langs, c = data["grades"], data["languages"], data["counts"]

    P = [f'<div id="ceval-root"><style>{_STYLE}</style><div class="wrap">']

    # header
    P.append('<div class="head"><div class="eyebrow">Companion variant · calibration report</div>')
    P.append(f'<h1 class="title">{_e(data["title"])}</h1>')
    P.append('<div class="meta">'
             f'<span>dataset <b class="mono">{_e(data["dataset_id"])}</b></span>'
             f'<span>evaluators <b class="mono">{_e(", ".join(data["evaluator_ids"]))}</b></span>'
             f'<span>languages <b class="mono">{_e(", ".join(langs))}</b> '
             f'(never pooled)</span>'
             f'<span><b class="mono">{_e(data["created_iso"][:19])}Z</b></span></div></div>')

    # provenance banner — if any grade is simulated, say so loudly and at the top
    sim = [g for g in grades if (g.get("provenance") or {}).get("evaluator", "").startswith("simulated")]
    if sim:
        P.append(
            '<div class="needjudge" style="border-color:var(--caution);'
            'background:var(--caution-soft);margin:18px 0 4px">'
            '<b style="color:var(--caution)">⚠ Mixed provenance.</b> The <b>compute</b> grades '
            '(repetition, scene-drive, over-refusal, discriminability) are <b>real measurements '
            'on real Claude Sonnet output</b>. The <b>judge</b> and <b>psychometric</b> grades '
            '(voice fidelity, character-α, wimp) here come from a <b>SIMULATED</b> provider — the '
            'pipeline is real, those specific numbers are fabricated to demonstrate discrimination '
            'without spending tokens. Swap the provider to real Claude to make them measurements. '
            'The label is the firewall.</div>')

    # legend — the tiers explain themselves; this is the honesty made structural
    P.append('<div class="legend">')
    for role, cls, n, desc in [
        ("gate", "gate", c["gate"], "May block a ship. The only tier with a measured noise floor."),
        ("guide", "guide", c["guide"], "Informs a human what to change. Never blocks."),
        ("trap", "trap", c["trap"], "Collected, never headlined. Optimising it is the disaster.")]:
        P.append(f'<div class="tier"><div class="k k-{cls}"><span class="dot dot-{cls}"></span>'
                 f'{role}</div><div class="n num">{n}</div><div class="d">{desc}</div></div>')
    P.append('</div>')

    # ability portrait — the lede: WHAT KIND of storyteller, before the defect tables
    if ability_profiles:
        P.append(_portrait([pr.to_row() if hasattr(pr, 'to_row') else pr
                            for pr in ability_profiles], langs[0] if langs else 'en'))

    OFFLINE = {"offline_content", "offline_judge"}
    ONLINE = {"live_behavior"}
    has_off = any(g["source"] in OFFLINE for g in grades)
    has_on = any(g["source"] in ONLINE for g in grades)

    def phase_block(name, hint, srcs):
        gate = _tables(grades, "gate", langs, sources=srcs)
        guide = _tables(grades, "guide", langs, sources=srcs)
        body = ""
        if "none in this book" not in gate:
            body += ('<h3 style="color:var(--critical);margin-top:12px">Gates — may block a ship</h3>' + gate)
        if "none in this book" not in guide:
            body += ('<h3 style="color:var(--signal);margin-top:20px">Guides — what to change</h3>' + guide)
        return (f'<div class="sec"><div class="sec-h"><h2>{name}</h2>'
                f'<span class="hint">{hint}</span></div><div class="rule"></div>{body}</div>')

    if has_off and has_on:
        # unified platform: two phases, one grade book
        P.append(phase_block("Pre-launch — offline",
                             "generated dialogues · compute + psychometric + judge · the ship gate",
                             OFFLINE))
        P.append(phase_block("Live — online",
                             "faked user traffic · behavioural signals · diagnostics only, never gates",
                             ONLINE))
    else:
        P.append('<div class="sec"><div class="sec-h"><h2>Gates</h2>'
                 '<span class="hint">lower is better · a detectable regression here blocks the ship</span>'
                 '</div><div class="rule"></div>'
                 + _tables(grades, "gate", langs) + '</div>')
        P.append('<div class="sec"><div class="sec-h"><h2>Guides</h2>'
                 '<span class="hint">what to change, and why · per language, shrunk, with intervals</span>'
                 '</div><div class="rule"></div>'
                 + _tables(grades, "guide", langs) + '</div>')

    # traps — recessed
    traps = [g for g in grades if g["role"] == "trap"]
    if traps:
        rows = "".join(
            f'<tr><td class="variant">{_e(t["dimension"])}</td>'
            f'<td class="n">{_e(t["variant_id"])}</td>'
            f'<td class="r value num">{_fmt(t["value"])}</td>'
            f'<td class="note">{_e((t.get("caveats") or [""])[0][:74])}</td></tr>'
            for t in sorted(traps, key=lambda x: x["dimension"]))
        P.append(
            '<div class="sec"><div class="sec-h"><h2>Traps</h2>'
            '<span class="hint">collected for completeness · walled off from every verdict</span>'
            '</div><div class="rule"></div><div class="trap-wrap">'
            '<div class="trap-bar"><span class="dot dot-trap"></span>'
            '<span class="warn">do not headline · do not optimise</span></div>'
            '<div class="trap-body"><p>These summarise approval, not quality. Chai got +30.3% D30 '
            'from optimising signals like these; OpenAI’s April-2025 sycophancy rollback happened '
            'because a thumbs-up entered the reward and the A/B tests approved of it. You cannot '
            'detect reward hacking with the metric being hacked.</p>'
            '<table><tr><th>signal</th><th>variant</th><th class="r">value</th>'
            '<th>gameable by</th></tr>' + rows + '</table></div></div></div>')

    # cannot measure — the thesis, equal weight
    li = "".join(f'<li>{_e(x)}</li>' for x in data["cannot_measure"])
    P.append('<div class="cannot"><h2>What this grade book cannot measure</h2>'
             '<div class="lede">Stating the limits is the product. A number outside these bounds '
             'is not a number this instrument can produce.</div>'
             f'<ul>{li}</ul></div>')

    if scheme:
        P.append(_scheme_section(scheme))

    P.append('<footer>Every value carries its role, interval, effective-n (conversations, not '
             'turns), and reading — in the data, not in a footnote. The instrument refuses to pool '
             'across languages (ρ(en,zh) = −0.082), refuses to headline a trap, and refuses '
             'to treat the self-selected arm as causal.</footer>')
    P.append('</div></div>')

    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(P))
    return str(p)
