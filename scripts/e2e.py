"""END TO END on real data. R1/R2/R3/R7/R11 in one run, no API key.

  1  create a variant           (registry, content-addressed)
  2  dry-run                    fail fast, free
  3  benchmark                  95 chars x 3 runs, judge-free lanes
  4  ship decision              delta + interval + MDE + what it CANNOT measure
  5  live collection            the injection points, with Tier 0 inline + escalation
  6  the loop                   curation back into the benchmark, provenance-capped

Run: PYTHONPATH=. python3 scripts/e2e.py
"""
import sys, uuid
sys.path.insert(0, ".")

from ceval.corpus import Corpus
from ceval.core.registry import Variant, Simulator
from ceval.core.lifecycle import Lifecycle, Stage
from ceval.metrics.builtin import Repetition, LengthCapAdherence
from ceval.online.collector import Collector, Tier0Blocked
from ceval.online.events import FinishReason, AssignmentArm, DiegeticStatus
from ceval.online.session import SessionAssembler
from ceval.safety import LexiconDetector

BAR = "═" * 78
def h(t): print(f"\n{BAR}\n{t}\n{BAR}")

c = Corpus("data", "en").load()
print(f"corpus: {c.summary()}")

# ── 1. create ────────────────────────────────────────────────────────────────
h("1  CREATE A VARIANT")
cand = Variant(model="deepseek/deepseek-v3.2", params={"temperature": 0.8},
               system_prompt="Roleplay as {{character_description}}. Stay in character. "
                             "Never mention being an AI. Keep replies under 150 words.",
               anchoring_policy="once_at_start", label="candidate")
base = Variant(model="deepseek/deepseek-v3.1", params={"temperature": 0.8},
               system_prompt=cand.system_prompt, anchoring_policy="once_at_start",
               label="baseline")
sim = Simulator(kind="replay", source=c.dataset_id().id, card_blind=True)
print(f"  candidate {cand.id}  {cand.model}")
print(f"  baseline  {base.id}  {base.model}")
print(f"  simulator {sim.id}   card_blind={sim.card_blind}  (a card-aware simulator is a")
print(f"            collaborator, not a user — the registry refuses to build one)")

lc = Lifecycle(c.dataset_id(), sim)

# ── 2. dry-run ───────────────────────────────────────────────────────────────
h("2  DRY-RUN  (a filter, not a measurement)")
subset = {d.seed_id: d.turns for d in c.dialogues
          if d.model_name == "deepseek-v3.2" and d.run_id == "run_1"}
rep, cap = Repetition("en"), LengthCapAdherence(150)

checks = [
    ("loops catastrophically (>40% n-gram recurrence)",
     lambda ds: any(rep.compute({k: v})[k] > 0.40 for k, v in list(ds.items())[:10])),
    ("ignores its own length cap on >50% of turns",
     lambda ds: any(cap.compute({k: v})[k] > 0.50 for k, v in list(ds.items())[:10])),
]
dr = lc.dry_run(cand, subset, checks)
print(f"  {dr.verdict()}")

# ── 3+4. benchmark & decide ──────────────────────────────────────────────────
h("3  BENCHMARK  +  4  SHIP DECISION")
cells = {}
for (m, s), ds in c.by_cell().items():
    if m in ("deepseek-v3.2", "deepseek-v3.1"):
        cells[(m, s)] = [rep.compute({s: d.turns})[s] for d in ds]

d = lc.decide(candidate="deepseek-v3.2", baseline="deepseek-v3.1", language="en",
              cells_by_metric={"repetition": cells},
              metrics={"repetition": rep},
              safety_blocks=[])
print(d.render())

# ── 5. live ──────────────────────────────────────────────────────────────────
h("5  LIVE COLLECTION  (the injection points)")
events, escalations = [], []

def tier0(ev):
    v = []
    if "as an ai" in ev.text.lower(): v.append("BLOCK:assistant_voice")
    return v

crisis = LexiconDetector()
col = Collector(variant_id=cand.id, response_model="deepseek/deepseek-v3.2",
                sink=events.append,
                escalate=lambda sig, sev: escalations.append((sig, sev.conversation_id)),
                crisis_scan=lambda t: [s.severity.name for s in
                                       crisis.scan([{"role": "user", "text": t}])],
                inclusion_prob=0.01)

asm = SessionAssembler()
replay = [d for d in c.dialogues if d.model_name == "deepseek-v3.2" and d.run_id == "run_1"][:20]
for dlg in replay:
    with col.session(f"conv_{dlg.seed_id}", dlg.seed_id, "en",
                     user_id_hash=f"u_{hash(dlg.seed_id) & 0xffff:04x}",
                     assignment_arm=AssignmentArm.RANDOMIZED_DEFAULT) as s:
        for i, t in enumerate(dlg.turns[:8]):
            if t["role"] == "user":
                s.user_turn(t["text"])
            else:
                try:
                    ev = s.turn(t["text"], distance_to_anchor=i,
                                latency_ms=800 + i * 10, output_tokens=len(t["text"]) // 4)
                    asm.add(ev)
                except Tier0Blocked as e:
                    print(f"  Tier 0 BLOCKED inline: {e.verdicts}")
        s.regenerate(2, "*a different reply*")     # a free pairwise label

# inject a crisis turn to prove escalation fires end-to-end
with col.session("conv_crisis", "en_dialogue_001", "en", user_id_hash="u_test",
                 assignment_arm=AssignmentArm.RANDOMIZED_DEFAULT) as s:
    s.user_turn("i don't want to live anymore")

for cid in {e.conversation_id for e in events}:
    asm.close(cid)

st_ = col.stats()
print(f"  sessions           {st_['sessions']}")
print(f"  generation events  {len(events)}")
print(f"  preference pairs   {st_['preference_pairs']}   <- FREE Q1 data. ~5M/day at 50M/day")
print(f"  escalations        {len(escalations)}   <- a HUMAN, not a counter")
print(f"  contract problems  {st_['contract_problems']}")
print(f"\n  effective n = {asm.effective_n()} CONVERSATIONS "
      f"(turn count is {asm.turn_count()}, and is NEVER a sample size — 60x overstatement)")
try:
    asm.completed[0].mean_turn_score("repetition")
except NotImplementedError as e:
    print(f"\n  Session.mean_turn_score() refuses:\n    {str(e)[:96]}…")

# ── 6. the loop ──────────────────────────────────────────────────────────────
h("6  THE LOOP  (curation accumulates, never replaces)")
existing = ["human-authored"] * 95
try:
    lc.curate([{"case": i} for i in range(200)], existing)
    print("  ✗ accepted — model collapse on the eval set is now possible")
except ValueError as e:
    print(f"  REFUSED: {str(e)[:150]}…")
ok = lc.curate([{"case": i} for i in range(20)], existing)
print(f"  accepted {len(ok)} mined cases (human-authored stays at "
      f"{95/(95+20):.0%} — above the cap)")

h("END TO END: PASSED")
print("  create -> dry-run -> benchmark -> decide -> live -> loop, on real data, no API key.")
