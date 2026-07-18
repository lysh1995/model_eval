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
from typing import List, Union

from ..gradebook import GradeBook

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
"""


def _e(s) -> str:
    return _html.escape(str(s))


def _fmt(v) -> str:
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:.3f}" if abs(v) < 1 else f"{v:.1f}"


def _sem(role: str) -> str:
    return {"gate": "critical", "guide": "signal", "trap": "caution"}.get(role, "signal")


def _tables(grades, role, langs, lower_is_better=True):
    color = f"var(--{_sem(role)})"
    out = []
    for lang in langs:
        dims = sorted({g["dimension"] for g in grades
                       if g["role"] == role and g["language"] == lang})
        for dim in dims:
            rows = [g for g in grades if g["dimension"] == dim and g["language"] == lang
                    and g["role"] == role and g.get("segment") != "self_selected_arm"]
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


def render(gradebook: Union[GradeBook, dict], out_path: str) -> str:
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

    # legend — the tiers explain themselves; this is the honesty made structural
    P.append('<div class="legend">')
    for role, cls, n, desc in [
        ("gate", "gate", c["gate"], "May block a ship. The only tier with a measured noise floor."),
        ("guide", "guide", c["guide"], "Informs a human what to change. Never blocks."),
        ("trap", "trap", c["trap"], "Collected, never headlined. Optimising it is the disaster.")]:
        P.append(f'<div class="tier"><div class="k k-{cls}"><span class="dot dot-{cls}"></span>'
                 f'{role}</div><div class="n num">{n}</div><div class="d">{desc}</div></div>')
    P.append('</div>')

    # gates
    P.append('<div class="sec"><div class="sec-h"><h2>Gates</h2>'
             '<span class="hint">lower is better · a detectable regression here blocks the ship</span>'
             '</div><div class="rule"></div>'
             + _tables(grades, "gate", langs) + '</div>')

    # guides
    P.append('<div class="sec"><div class="sec-h"><h2>Guides</h2>'
             '<span class="hint">what to change, and why · reported per language, shrunk, with intervals</span>'
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

    P.append('<footer>Every value carries its role, interval, effective-n (conversations, not '
             'turns), and reading — in the data, not in a footnote. The instrument refuses to pool '
             'across languages (ρ(en,zh) = −0.082), refuses to headline a trap, and refuses '
             'to treat the self-selected arm as causal.</footer>')
    P.append('</div></div>')

    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(P))
    return str(p)
