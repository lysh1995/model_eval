"""Interactive dashboard — CSS-only tabs, no JavaScript.

The previous JS version did not interact in the published artifact (strict CSP / no-JS
render). This uses the hidden-radio + label + `:checked ~ .panel` pattern: pure CSS, so tab
switching works in ANY environment — the artifact, a static-snapshot preview, an email.

Structure (addresses 'Overview should be in details'):
  Tab  ALL          the comparison matrix — every variant × dimension side by side, both
                    phases, leader highlighted. Overview and cross-compare in one.
  Tab  <variant>    one per variant: its actual SYSTEM PROMPT, storyteller profile, and every
                    dimension with the variant's value and where it ranks in the field.

All panels are pre-rendered server-side; CSS only shows the selected one. No script.
"""
from __future__ import annotations
import html as _html
import math
import pathlib
from typing import List, Optional, Union

from ...core.gradebook import GradeBook

_LOWER_BETTER = {"repetition", "wimp_rate", "over_refusal", "homogenization",
                 "abandonment", "regenerate_rate", "mean_latency_ms", "regurgitation"}
_OFFLINE = {"offline_content", "offline_judge"}
_ONLINE = {"live_behavior"}

# The HEADLINE quality score — storytelling craft is the product's core value, so it leads the
# dashboard and each variant's profile. It stays a GUIDE (perspectival; informs, never auto-gates).
_HEADLINE = "narrative_craft"
# Display priority: headline first, then the other quality signals, then the rest.
_DIM_ORDER = [_HEADLINE, "voice_fidelity", "character_alpha", "narrative_engagement",
              "scene_drive_treadmill", "discriminability", "repetition", "over_refusal", "wimp_rate",
              # user-behaviour safety dimensions (measured PER LANGUAGE, en + zh)
              "crisis_frame_hold", "help_seeking_support", "regurgitation",
              # online: lead with the craft proxy (the online read of the headline), then opinion
              "story_cocreation", "satisfaction_inferred", "follow_up_question_rate"]


def _dim_rank(dim: str) -> int:
    return _DIM_ORDER.index(dim) if dim in _DIM_ORDER else len(_DIM_ORDER)


def _e(s):
    return _html.escape(str(s))


def _fmt(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    return f"{v:.3f}" if abs(v) < 1 else f"{v:.1f}"


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
#app{background:var(--paper);color:var(--ink);min-height:100vh;padding:34px 22px 64px;
font-family:ui-sans-serif,-apple-system,"Segoe UI",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
#app *{box-sizing:border-box}
.wrap{max-width:1000px;margin:0 auto}
.num{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-variant-numeric:tabular-nums}
.eyebrow{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--signal);font-weight:700}
h1{font-size:22px;font-weight:680;letter-spacing:-.01em;margin:6px 0 2px}
.sub{color:var(--muted);font-size:12px;margin-bottom:18px}
/* CSS-only tabs */
.tabin{position:absolute;opacity:0;pointer-events:none}
.tabs{display:flex;flex-wrap:wrap;gap:4px;background:var(--line);padding:4px;border-radius:11px;
width:fit-content;max-width:100%;margin-bottom:18px}
.tabs label{font-size:13px;font-weight:600;color:var(--muted);padding:7px 15px;border-radius:8px;
cursor:pointer;white-space:nowrap}
.tabs label:hover{color:var(--ink)}
.panel{display:none}
#t_all:checked~.tabs label[for=t_all],
#t_0:checked~.tabs label[for=t_0],#t_1:checked~.tabs label[for=t_1],
#t_2:checked~.tabs label[for=t_2],#t_3:checked~.tabs label[for=t_3],
#t_4:checked~.tabs label[for=t_4],#t_5:checked~.tabs label[for=t_5]
{background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
#t_all:checked~#p_all,#t_0:checked~#p_0,#t_1:checked~#p_1,#t_2:checked~#p_2,
#t_3:checked~#p_3,#t_4:checked~#p_4,#t_5:checked~#p_5{display:block}
.phase{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);
font-weight:700;margin:22px 0 6px;border-bottom:2px solid var(--line);padding-bottom:5px}
table{width:100%;border-collapse:collapse;font-size:13px}
th{text-align:left;color:var(--faint);font-size:10.5px;text-transform:uppercase;letter-spacing:.04em;
font-weight:600;padding:6px 9px}
th.r,td.r{text-align:right}
td{padding:8px 9px;border-top:1px solid var(--line2);vertical-align:middle}
.dimname{font-weight:560}.lay{font-size:8.5px;color:var(--faint);font-weight:700;margin-right:5px}
.lang{font-size:9.5px;font-weight:700;color:var(--signal);background:var(--signal-soft);
padding:1px 5px;border-radius:4px;letter-spacing:.04em}
.val{font-weight:640}
.track{height:6px;border-radius:3px;background:var(--line);position:relative;display:inline-block;
width:100%;max-width:130px;vertical-align:middle}
.track>i{position:absolute;left:0;top:0;height:100%;border-radius:3px}
.hl{background:var(--pass-soft)}
.lead{font-size:9px;font-weight:700;color:var(--pass);background:var(--pass-soft);padding:1px 6px;
border-radius:4px;margin-left:6px}
.role{font-size:9px;padding:1px 6px;border-radius:4px;font-weight:700;white-space:nowrap}
.role-gate{background:var(--critical);color:#fff}.role-guide{background:var(--signal-soft);color:var(--signal)}
.role-trap{background:var(--caution-soft);color:var(--caution)}
.role-headline{background:var(--pass);color:#fff}
tr.headline{background:var(--pass-soft)}
tr.headline .dimname{font-weight:700;color:var(--ink)}
.hq{display:flex;align-items:baseline;gap:10px;margin:2px 0 14px;padding:12px 16px;
border:1px solid var(--pass);border-radius:12px;background:var(--pass-soft)}
.hq-label{font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--pass);font-weight:700}
.hq-val{font-size:30px;font-weight:800;color:var(--ink);font-variant-numeric:tabular-nums;line-height:1}
.hq-rank{font-size:12px;color:var(--muted)}
.card{border:1px solid var(--line);border-radius:12px;background:var(--panel);padding:18px 20px;
box-shadow:var(--shadow);margin:0 0 18px}
.meta{font-size:11px;color:var(--muted)}
.prompt{font-family:ui-monospace,Menlo,monospace;font-size:12px;line-height:1.55;color:var(--ink);
background:var(--line2);border-radius:8px;padding:12px 14px;white-space:pre-wrap;margin-top:8px}
.char{font-size:13px;color:var(--ink);line-height:1.55;margin-top:12px}
.note{color:var(--muted);font-size:11px}
.warn{background:var(--caution-soft);border:1px solid var(--caution);border-radius:10px;
padding:11px 15px;font-size:11.5px;color:var(--ink);margin:20px 0}
.warn b{color:var(--caution)}
.cannot{background:var(--panel);border-left:3px solid var(--signal);border-radius:0 10px 10px 0;
padding:16px 18px;margin-top:22px}
.cannot li{font-size:12px;margin:5px 0;color:var(--ink)}
.hint{font-size:11.5px;color:var(--faint);margin-bottom:10px}
/* evidence: good & bad examples per dimension */
details.ev{margin:2px 0 10px}
details.ev summary{font-size:11px;color:var(--signal);cursor:pointer;font-weight:600;
list-style:none;padding:3px 0}
details.ev summary::-webkit-details-marker{display:none}
details.ev summary::before{content:"▸ ";font-size:9px}
details.ev[open] summary::before{content:"▾ "}
.ex{border-radius:8px;padding:9px 12px;margin:6px 0;font-size:12px;line-height:1.5}
.ex.good{background:var(--pass-soft);border:1px solid var(--pass)}
.ex.bad{background:var(--critical-soft,#fbeae8);border:1px solid var(--critical)}
.ex .tag{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}
.ex.good .tag{color:var(--pass)}.ex.bad .tag{color:var(--critical)}
.ex .why{font-size:10.5px;color:var(--muted);margin:3px 0 5px}
.ex .txt{font-family:ui-monospace,Menlo,monospace;font-size:11.5px;white-space:pre-wrap;color:var(--ink)}
.ev-note{font-size:11px;color:var(--faint);font-style:italic;padding:2px 0 8px}
/* CSS-only language switch (EN / 中文) — swaps which language's values show, never both at once */
.langtoggle{display:inline-flex;align-items:center;gap:3px;background:var(--line);padding:4px;
border-radius:10px;margin:2px 0 16px}
.langtoggle .lgl{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;
color:var(--faint);padding:0 8px}
.langtoggle label{font-size:12.5px;font-weight:700;color:var(--muted);padding:5px 15px;
border-radius:7px;cursor:pointer}
.langtoggle label:hover{color:var(--ink)}
#pglang_en:checked ~ .langtoggle label[for=pglang_en],
#pglang_zh:checked ~ .langtoggle label[for=pglang_zh]
{background:var(--panel);color:var(--ink);box-shadow:var(--shadow)}
/* default: show en, hide zh. Cover BOTH top-level-sibling and nested-in-a-sibling cases. */
.lv{display:inline}.lv.zh{display:none}
.lp{display:block}.lp.lp-zh{display:none}
#pglang_zh:checked ~ .lv.en,#pglang_zh:checked ~ * .lv.en{display:none}
#pglang_zh:checked ~ .lv.zh,#pglang_zh:checked ~ * .lv.zh{display:inline}
#pglang_zh:checked ~ .lp.lp-en,#pglang_zh:checked ~ * .lp.lp-en{display:none}
#pglang_zh:checked ~ .lp.lp-zh,#pglang_zh:checked ~ * .lp.lp-zh{display:block}
"""


def langtoggle() -> str:
    """The page-level EN/中文 switch. Its two radios must PRECEDE the content as siblings, so the
    `#pglang_zh:checked ~ * .lv/.lp` rules can reach it. One per rendered document."""
    return ('<input type="radio" name="pglang" id="pglang_en" class="tabin" checked>'
            '<input type="radio" name="pglang" id="pglang_zh" class="tabin">'
            '<div class="langtoggle"><span class="lgl">Language</span>'
            '<label for="pglang_en">EN</label><label for="pglang_zh">中文</label></div>')


def _color(role):
    return {"gate": "var(--critical)", "guide": "var(--signal)", "trap": "var(--caution)"}.get(role, "var(--signal)")


def _matrix(grades, variants, vids):
    """Overview + compare in one: every variant × dimension, leader highlighted.

    A dimension measured in more than one language shows BOTH values in one row (as en/zh spans);
    the page-level EN/中文 switch shows one at a time. The leader ▸ is chosen WITHIN the language,
    so the ranking is never pooled across languages (rho(en,zh) = −0.082)."""
    def one(dim, lang, vid):
        return next((x for x in grades if x["dimension"] == dim
                     and x.get("language", "en") == lang and x["variant_id"] == vid), None)
    def best_of(dim, lang):
        vals = [g["value"] for g in grades if g["dimension"] == dim
                and g.get("language", "en") == lang and g["value"] is not None]
        return (min if dim in _LOWER_BETTER else max)(vals) if vals else None

    out = ['<div class="hint">Every variant, side by side. <b>★ narrative_craft is the headline '
           'quality score</b> — the product core (a guide, not an automatic gate; repetition remains '
           'the one gate). A green ▸ leads on that dimension (direction-aware: lower is better for '
           'repetition, wimp, refusal, and regurgitation). Safety dimensions marked '
           '<span class="lang">by language</span> are measured in two languages — use the '
           '<b>EN / 中文</b> switch above; each language is ranked on its own, <b>never pooled</b> '
           '(ρ(en,zh)=−0.082).</div>']
    for label, srcs in (("Pre-launch — offline", _OFFLINE), ("Live — online", _ONLINE)):
        langs_by_dim = {}
        for g in grades:
            if g["source"] in srcs:
                langs_by_dim.setdefault(g["dimension"], set()).add(g.get("language", "en"))
        if not langs_by_dim:
            continue
        dims = sorted(langs_by_dim, key=_dim_rank)
        out.append(f'<div class="phase">{label}</div><table><tr><th>dimension</th><th></th>'
                   + "".join(f'<th class="r">{_e(variants[v]["label"])}</th>' for v in vids) + '</tr>')
        for dim in dims:
            langs = sorted(langs_by_dim[dim])
            multi = len(langs) > 1
            role = next(g["role"] for g in grades if g["dimension"] == dim)
            head = dim == _HEADLINE
            name = (f'★ {_e(dim)}' if head else _e(dim)) + (
                ' <span class="lang">by language</span>' if multi else '')
            badge = ('<span class="role role-headline">headline quality</span>' if head
                     else f'<span class="role role-{role}">{role}</span>')
            cells = []
            for v in vids:
                if multi:
                    spans = []
                    for lang in langs:
                        g = one(dim, lang, v); best = best_of(dim, lang)
                        if not g or g["value"] is None:
                            spans.append(f'<span class="lv {lang} note">—</span>')
                        else:
                            lead = '<span class="lead">▸</span>' if g["value"] == best else ""
                            spans.append(f'<span class="lv {lang}"><span class="val num">'
                                         f'{_fmt(g["value"])}</span>{lead}</span>')
                    cells.append(f'<td class="r">{"".join(spans)}</td>')
                else:
                    g = one(dim, langs[0], v); best = best_of(dim, langs[0])
                    if not g or g["value"] is None:
                        cells.append('<td class="r note">—</td>')
                    else:
                        hl = " hl" if g["value"] == best else ""
                        lead = '<span class="lead">▸</span>' if g["value"] == best else ""
                        cells.append(f'<td class="r{hl}"><span class="val num">'
                                     f'{_fmt(g["value"])}</span>{lead}</td>')
            out.append(f'<tr{" class=headline" if head else ""}><td class="dimname">{name}</td>'
                       f'<td>{badge}</td>' + "".join(cells) + '</tr>')
        out.append('</table>')
    return "".join(out)


def _example_html(ev_dim: dict) -> str:
    """A <details> disclosure with the good & bad example replies (native HTML, no JS)."""
    if not ev_dim:
        return ""
    if "note" in ev_dim:
        return f'<div class="ev-note">{_e(ev_dim["note"])}</div>'
    def ex(kind):
        e = ev_dim.get(kind)
        if not e:
            return ""
        return (f'<div class="ex {kind}"><span class="tag">{kind} example</span> '
                f'<span class="note">· {_e(e["character"])}</span>'
                f'<div class="why">{_e(e["why"])}</div>'
                f'<div class="txt">{_e(e["text"][:340])}</div></div>')
    return (f'<details class="ev"><summary>why this grade — good &amp; bad examples</summary>'
            f'{ex("good")}{ex("bad")}</details>')


def _sessions_block(sess):
    """Online drill-down from the persisted sessions: arm split (the self-selection confound) and
    the per-character spread. Randomised = clean; self-selected reflects who chose the variant."""
    if not sess:
        return ""
    rnd, slf = sess["randomised"], sess["self_selected"]
    pull = (slf / rnd) if rnd else 0.0
    tag = ("heavy users OVER-picked it — the self-selection confound inflates its self-selected arm"
           if pull > 1.15 else
           "heavy users UNDER-picked it" if pull < 0.85 else "picked ~evenly by both arms")
    chars = " · ".join(f"{_e(c)}: {n}" for c, n in sorted(sess["by_character"].items()))
    return (
        f'<div class="char" style="margin-top:8px">'
        f'<b>Behavioural drill-down</b> — {sess["total"]} sessions · '
        f'randomised {rnd} vs self-selected {slf} '
        f'(pull ×{pull:.2f}: {tag}). '
        f'Grades above use the <b>randomised arm only</b>; the self-selected arm is retrieved but '
        f'walled off as observational.<br><span class="note">by character — {chars}</span></div>')


def _detail(grades, variants, vid, profiles, evidence, sessions=None):
    meta = variants[vid]
    prof = next((p for p in profiles if p["model"] == vid), None)
    ev = (evidence or {}).get(vid, {})
    # headline quality: storytelling craft leads the profile (a guide, not a gate)
    craft = next((g for g in grades if g["variant_id"] == vid and g["dimension"] == _HEADLINE), None)
    hq = ""
    if craft and craft["value"] is not None:
        peers = sorted((g["value"] for g in grades
                        if g["dimension"] == _HEADLINE and g["value"] is not None), reverse=True)
        rank = peers.index(craft["value"]) + 1 if craft["value"] in peers else "—"
        hq = (f'<div class="hq"><span class="hq-label">Storytelling quality</span>'
              f'<span class="hq-val">{_fmt(craft["value"])}</span>'
              f'<span class="hq-rank">headline score · rank {rank} of {len(peers)} · '
              f'the product core — a guide, not an automatic gate</span></div>')
    out = [hq, f'<div class="card"><div class="meta">{_e(meta["model"])} · {_e(meta["intent"])}</div>'
           f'<div class="eyebrow" style="margin-top:10px">system prompt</div>'
           f'<div class="prompt">{_e(meta["system_prompt"])}</div>']
    if prof:
        out.append(f'<div class="char"><b>Storyteller profile:</b> {_e(prof["characterization"])}</div>')
    out.append('</div>')
    for label, srcs in (("Pre-launch — offline", _OFFLINE), ("Live — online", _ONLINE)):
        rows = [g for g in grades if g["variant_id"] == vid and g["source"] in srcs]
        if not rows:
            continue
        langs_by_dim = {}
        for g in rows:
            langs_by_dim.setdefault(g["dimension"], set()).add(g.get("language", "en"))
        rows.sort(key=lambda g: (_dim_rank(g["dimension"]), g.get("language", "en")))
        out.append(f'<div class="phase">{label}</div>')
        for g in rows:
            lang = g.get("language", "en")
            # peers are computed WITHIN the language — the ranking is never pooled (ρ(en,zh)=−0.082)
            peers = sorted(x["value"] for x in grades
                           if x["dimension"] == g["dimension"]
                           and x.get("language", "en") == lang and x["value"] is not None)
            rank = peers.index(g["value"]) + 1 if g["value"] in peers else "—"
            mx = max((abs(p) for p in peers), default=0.001) or 0.001
            v = g["value"] or 0
            w = max(3, min(100, 100 * abs(v) / mx))
            bar = f'<div class="track"><i style="width:{w:.0f}%;background:{_color(g["role"])}"></i></div>'
            multi = len(langs_by_dim.get(g["dimension"], set())) > 1
            dimlabel = _e(g["dimension"]) + (' <span class="lang">by language</span>' if multi else '')
            block = (
                '<table style="margin-bottom:0"><tr>'
                f'<td class="dimname" style="width:190px">{dimlabel}</td>'
                f'<td style="width:64px"><span class="role role-{g["role"]}">{g["role"]}</span></td>'
                f'<td class="r val num" style="width:60px">{_fmt(g["value"])}</td>'
                f'<td class="r note num" style="width:64px">{rank}/{len(peers)}</td>'
                f'<td>{bar}</td></tr></table>')
            cavs = [c for c in (g.get("caveats") or []) if c]
            if cavs:
                block += ('<div style="margin:2px 0 9px;padding-left:2px">'
                          + "".join(f'<div class="note" style="line-height:1.45;margin:1px 0">· {_e(c)}</div>'
                                    for c in cavs) + '</div>')
            block += _example_html(ev.get(g["dimension"], {}))
            # multi-language dims: wrap each language's block so the EN/中文 switch shows one
            out.append(f'<div class="lp lp-{lang}">{block}</div>' if multi else block)
    if sessions and sessions.get(vid):
        out.append(_sessions_block(sessions[vid]))
    return "".join(out)


def render_interactive(gradebook: Union[GradeBook, dict], variants: dict, profiles: list,
                       out_path: str, title: Optional[str] = None, evidence: dict = None,
                       sessions: dict = None) -> str:
    gb = gradebook.to_dict() if isinstance(gradebook, GradeBook) else gradebook
    grades = [g for g in gb["grades"] if g.get("segment") != "self_selected_arm"]
    profiles = [p.to_row() if hasattr(p, "to_row") else p for p in profiles]
    vids = list(variants)
    title = title or gb.get("title", "Companion variant evaluation")

    # radio inputs (must precede the tabs+panels for the ~ sibling selector)
    radios = ['<input type="radio" name="tab" id="t_all" class="tabin" checked>']
    radios += [f'<input type="radio" name="tab" id="t_{i}" class="tabin">' for i in range(len(vids))]

    tabs = ['<label for="t_all">All variants</label>']
    tabs += [f'<label for="t_{i}">{_e(variants[v]["label"])}</label>' for i, v in enumerate(vids)]

    panels = [f'<div class="panel" id="p_all">{_matrix(grades, variants, vids)}</div>']
    panels += [f'<div class="panel" id="p_{i}">{_detail(grades, variants, v, profiles, evidence, sessions)}</div>'
               for i, v in enumerate(vids)]

    cannot = "".join(f"<li>{_e(x)}</li>" for x in gb.get("cannot_measure", []))
    body = (
        f'<div id="app"><style>{_CSS}</style><div class="wrap">'
        f'<div class="eyebrow">Companion variant evaluation · one platform</div>'
        f'<h1>{_e(title)}</h1>'
        f'<div class="sub">variants {_e(", ".join(v["label"] for v in variants.values()))} · '
        f'evaluators {_e(", ".join(gb.get("evaluator_ids", [])))} · {_e(gb.get("created_iso","")[:19])}</div>'
        + langtoggle()
        + "".join(radios)
        + '<div class="tabs">' + "".join(tabs) + '</div>'
        + "".join(panels)
        + '<div class="warn"><b>Provenance.</b> Offline compute grades (incl. <b>regurgitation</b>) '
          'are real measurements on real Claude output; offline judge/psychometric grades are real '
          'Claude judging. The two user-behaviour judge dimensions (<b>crisis_frame_hold</b>, '
          '<b>help_seeking_support</b>) are <b>designed expectations, labelled</b> '
          '(evaluator designed/behavioural-v1) — wired and discriminating, with real judge recordings '
          'the swap-in. Online grades are from <b>faked user traffic</b> — the pipeline is real, the '
          'behaviour is simulated to exercise the platform.</div>'
        + f'<div class="cannot"><div class="eyebrow">What this cannot measure</div><ul>{cannot}</ul></div>'
        + '</div></div>')

    p = pathlib.Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body)
    return str(p)
