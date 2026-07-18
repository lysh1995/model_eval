"""Run the offline scheme with BOTH providers and compare: does the REAL Claude judge agree
with the simulated expectations?

This is the validation the simulated demo could not give. If the real judge lands near the
simulated direction (assistant worst on fidelity, highest on wimp), the pipeline's design
expectations held. If it diverges, that is itself the finding.

Run: python3 scripts/compare_providers.py   ->   out/offline_dashboard.html (real)
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from datetime import datetime, timezone

from ceval.offline import load_run, run, make_provider, SCHEME
from ceval.ability import build_profiles, measure_field
from ceval.dashboard import render

NOW = datetime.now(timezone.utc).isoformat()
BAR = "─" * 74

offline = load_run("out/gen", "out/gen/tasks.json", "en")
sim = make_provider("simulated")
real = make_provider("recorded", judge_dir="out/judge")

# which variants have real recordings?
have_real = [v for v in offline.variant_ids if real.has(v)]
print(f"variants with REAL judge recordings: {have_real or '(none yet — subagents still running)'}")

gb_sim = run(offline, sim, NOW)
gb_real = run(offline, real, NOW) if have_real else None

# side-by-side on the judge/psychometric dimensions
JUDGE_DIMS = ["character_alpha", "voice_fidelity", "wimp_rate"]
print(f"\n{BAR}\nSIMULATED  vs  REAL CLAUDE JUDGE\n{BAR}")
print(f"{'dimension':20s} {'variant':14s} {'simulated':>10s} {'real':>8s} {'Δ':>7s}")
def val(gb, dim, v):
    for g in gb.grades:
        if g.dimension == dim and g.variant_id == v: return g.value
    return None
for dim in JUDGE_DIMS:
    for v in sorted(offline.variant_ids):
        s = val(gb_sim, dim, v)
        r = val(gb_real, dim, v) if gb_real else None
        sd = f"{s:.3f}" if s is not None else "—"
        rd = f"{r:.3f}" if r is not None else "—"
        dd = f"{r-s:+.3f}" if (s is not None and r is not None) else ""
        print(f"{dim:20s} {v:14s} {sd:>10s} {rd:>8s} {dd:>7s}")

# render the REAL dashboard if we have it, else simulated
gb = gb_real or gb_sim
field = {}
for vid, chars in offline.dialogues.items():
    class _Shim:
        def __init__(s, vid, chars): s._vid, s._chars = vid, chars
        def models(s): return [s._vid]
        @property
        def dialogues(s):
            class D:
                def __init__(d, cid, turns): d.model_name=s._vid; d.seed_id=cid; d.turns=turns
                def ai_texts(d): return [t["text"] for t in d.turns if t["role"]=="ai"]
            return [D(c, t) for c, t in s._chars.items()]
        def character_texts(s, m):
            return {c: [t["text"] for t in t2 if t["role"]=="ai"] for c, t2 in s._chars.items()}
    field.update(measure_field(_Shim(vid, chars), "en", budget=200))
profiles = build_profiles(field, "en")

pathlib.Path("out").mkdir(exist_ok=True)
tag = "real" if gb_real else "simulated"
gb.title = f"Offline test — Claude Sonnet variants ({tag} judge)"
pathlib.Path("out/offline_gradebook.json").write_text(gb.to_json())
path = render(gb, "out/offline_dashboard.html", ability_profiles=profiles, scheme=SCHEME)
p = pathlib.Path(path)
if "<title>" not in p.read_text():
    p.write_text(f"<title>Offline Test — Sonnet Variants ({tag})</title>\n" + p.read_text())
print(f"\n{BAR}\n  rendered {path}  ({tag} judge)\n{BAR}")
