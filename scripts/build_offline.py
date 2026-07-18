"""The three offline components, end to end, into one dashboard. No API key.

  1  TEST TARGETS   3 Claude Sonnet variants (real generation in out/gen/)
  2  TEST SCHEME    scheme.py — dimensions across L1/L2/L3/safety, compute + psychometric + judge
  3  PLATFORM       run the scheme over the variants -> GradeBook -> cross-variant dashboard

Compute grades are REAL measurements on real Claude output. Judge + psychometric grades come
from the SIMULATED provider (token-thrifty demo) and are labelled as such -- the pipeline is
real, those specific numbers are not.

Run: python3 scripts/build_offline.py   ->   out/offline_dashboard.html
"""
import sys, pathlib, statistics as st
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from datetime import datetime, timezone

from ceval.offline import load_run, run, make_provider, summary, SCHEME
from ceval.ability import build_profiles
from ceval.dashboard import render

NOW = datetime.now(timezone.utc).isoformat()
BAR = "─" * 70

# ═══ 1 + 2 + 3: load real generation, run the scheme ═════════════════════════
print(BAR); print("OFFLINE TEST — 3 Claude Sonnet variants, real generation"); print(BAR)
offline = load_run("out/gen", "out/gen/tasks.json", "en")
print(f"  variants:   {', '.join(offline.variant_ids)}")
print(f"  characters: {len(next(iter(offline.dialogues.values())))} per variant")
s = summary()
print(f"  scheme:     {s['dimensions']} dimensions · lanes {s['by_lane']} · "
      f"judge spans {s['judge_spans_levels']}")

provider = make_provider("simulated")   # token-thrifty; swap 'subagent' for real Claude judging
gb = run(offline, provider, NOW)
print(f"\n{BAR}\nGRADE BOOK ({gb.to_dict()['counts']})\n{BAR}")

# print the cross-variant comparison per dimension
dims = {}
for g in gb.grades:
    dims.setdefault(g.dimension, {})[g.variant_id] = g.value
for dim, byv in dims.items():
    row = "  ".join(f"{v}={byv[v]:.3f}" for v in sorted(byv))
    print(f"  {dim:26s} {row}")

# ═══ ability portrait over the 3 variants (from real generated text) ═════════
field = {}
for vid, chars in offline.dialogues.items():
    from ceval.ability import measure_field
    # measure_field wants a corpus-like object; build a tiny shim
    class _Shim:
        def __init__(self, vid, chars):
            self._vid, self._chars = vid, chars
        def models(self): return [self._vid]
        @property
        def dialogues(self):
            class D:
                def __init__(s, cid, turns): s.model_name=vid; s.seed_id=cid; s.turns=turns
                def ai_texts(s): return [t["text"] for t in s.turns if t["role"]=="ai"]
            return [D(cid, turns) for cid, turns in self._chars.items()]
        def character_texts(self, m):
            return {cid: [t["text"] for t in turns if t["role"]=="ai"]
                    for cid, turns in self._chars.items()}
    f1 = measure_field(_Shim(vid, chars), "en", budget=200)
    field.update(f1)
profiles = build_profiles(field, "en")
print(f"\n{BAR}\nABILITY PORTRAIT (real generation)\n{BAR}")
for pr in profiles:
    print(f"  {pr.model:14s} {pr.characterization}")

# ═══ render ══════════════════════════════════════════════════════════════════
pathlib.Path("out").mkdir(exist_ok=True)
pathlib.Path("out/offline_gradebook.json").write_text(gb.to_json())
path = render(gb, "out/offline_dashboard.html", ability_profiles=profiles, scheme=SCHEME)
if "<title>" not in pathlib.Path(path).read_text():
    p = pathlib.Path(path); p.write_text("<title>Offline Test — Sonnet Variants</title>\n" + p.read_text())
print(f"\n{BAR}\n  wrote {path}\n{BAR}")
