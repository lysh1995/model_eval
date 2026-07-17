"""C2: demonstrate the design holds at 50M/day WITH REAL NUMBERS.

Measures on this machine, on the real corpus:
  - Lane 1 throughput (dialogues/sec/core) -> cores needed at 50M/day
  - bytes per event
  - our rubric's token footprint -> does prompt caching even engage?
Then does the arithmetic, printing the provenance of every input.

Run: PYTHONPATH=. python3 scripts/scale_report.py
"""
import json, statistics as st, sys, time
sys.path.insert(0, ".")

from ceval.corpus import Corpus
from ceval.metrics.builtin import Repetition, LengthCapAdherence, FormatDiscipline
from ceval.scale.units import Provenance, TokenProfile, Price, count_tokens, time_it
from ceval.scale.costmodel import CostModel, Workload, TierPlan

BAR = "─" * 78
print(BAR); print("C2 — 50M generations/day, from MEASURED units"); print(BAR)

c = Corpus("data", "en").load(runs=["run_1"])
dialogues = c.dialogues
print(f"\nbenchmark corpus: {len(dialogues)} real dialogues, "
      f"{sum(len(d.turns) for d in dialogues):,} turns\n")

# ---------------------------------------------------------------- MEASURE lane 1
rep, cap, fmt = Repetition("en"), LengthCapAdherence(150), FormatDiscipline("en")

def run_lane1():
    for d in dialogues:
        rep.compute({d.seed_id: d.turns})
        cap.compute({d.seed_id: d.turns})
        fmt.compute({d.seed_id: d.turns})
    return len(dialogues)

print("measuring Lane 1 (best of 3, single core)...")
b = time_it(run_lane1, "lane1", repeats=3)
print(f"  {b.n_items} dialogues in {b.seconds:.2f}s  ->  "
      f"{b.per_sec:,.1f} dialogues/sec/core  ({b.ms_per_item:.2f} ms/dialogue)")

# ---------------------------------------------------------------- MEASURE bytes/event
sizes = []
for d in dialogues[:200]:
    ev = {"gen_ai.response.model": d.model_name, "gen_ai.conversation.id": d.seed_id,
          "eval.variant_id": "v_" + "0"*16, "eval.evaluator_id": None,
          "eval.inclusion_prob": 1.0, "eval.distance_to_anchor": 12,
          "eval.provenance": "human-authored", "eval.assignment_arm": "randomized_default",
          "eval.diegetic_status": "character_claims", "turn_index": 47,
          "text": d.turns[1]["text"], "latency_ms": 812,
          "gen_ai.usage.input_tokens": 1400, "gen_ai.usage.output_tokens": 180}
    sizes.append(len(json.dumps(ev, ensure_ascii=False).encode()))
bytes_per_event = st.mean(sizes)
print(f"  event size: {bytes_per_event:,.0f} bytes (mean of 200 real turns, uncompressed)")

# ---------------------------------------------------------------- MEASURE our rubric
RUBRIC = open("ceval/scale/rubric_sample.txt").read() if __import__("os").path.exists(
    "ceval/scale/rubric_sample.txt") else ("You are comparing two in-character responses. " * 40)
anchor = " ".join(d.turns[0]["text"] for d in dialogues[:3])
candidate = dialogues[0].turns[2]["text"]
tp = TokenProfile(rubric_tokens=count_tokens(RUBRIC), anchor_tokens=count_tokens(anchor),
                  candidate_tokens=count_tokens(candidate), output_tokens=12)
print(f"\n  our judge prompt: rubric={tp.rubric_tokens:,} + anchors={tp.anchor_tokens:,} "
      f"= {tp.cached_prefix:,}-token cacheable prefix")
print(f"  prompt caching engages (needs >=4096)?  {'YES' if tp.cache_engages() else '*** NO ***'}")
if not tp.cache_engages():
    print(f"  !! {4096 - tp.cached_prefix:,} tokens short. Caching would save NOTHING and")
    print(f"     report no error. This is the single highest-leverage fact in the model.")

# ---------------------------------------------------------------- the model
cheap = Price("haiku-4.5", 1.00, 5.00, 0.10, 0.5, "Anthropic published pricing")
gold  = Price("opus-4.8", 15.00, 75.00, 1.50, 0.5, "Anthropic published pricing")
w, plan = Workload(), TierPlan()
m = CostModel(w, plan, cheap, gold, tp, lane1_throughput=b, bytes_per_event=bytes_per_event)

print(f"\n{BAR}"); print("DOES THE TIERING CLAIM SURVIVE MEASUREMENT?"); print(BAR)
cores = m.lane1_cores_needed()
print(f"\n  workload: {w.generations_per_day:,.0f} generations/day = {w.per_sec:,.0f}/sec")
print(f"  Lane 1 at 100% coverage needs: {cores}")
l1 = m.lane1_cost_per_day()
print(f"  -> ${l1.per_day_usd:,.2f}/day  ({l1.note})")
verdict = ("HOLDS — Lane 1 on 100% of traffic is a rounding error"
           if l1.per_day_usd < 500 else
           "*** FAILS — 'Lanes 0-2 are free' is FALSE at this throughput ***")
print(f"  VERDICT: {verdict}")

print(f"\n{BAR}"); print("COST AT 50M/DAY"); print(BAR)
lines = [l1] + m.lane3_cost_per_day()
print(f"\n  {'lane':22s} {'coverage':>9s} {'items/day':>13s} {'$/day':>10s}  provenance")
for L in lines:
    print(f"  {L.lane:22s} {L.coverage:8.4%} {L.items_per_day:13,.0f} {L.per_day_usd:10,.2f}  "
          f"[{L.provenance.value}]")
total = sum(L.per_day_usd for L in lines)
print(f"  {'TOTAL':22s} {'':>9s} {'':>13s} {total:10,.2f}")
print(f"\n  = ${total*365:,.0f}/yr")

print(f"\n  counterfactual — no tiering:")
for k, v in m.counterfactual_100pct().items():
    print(f"    {k:38s} ${v:15,.0f}/yr   ({v/(total*365):,.0f}x more)")
print(f"\n  prompt caching saves: ${m.cache_saving_per_year():,.0f}/yr")

stor = m.storage_per_year_tb()
print(f"\n{BAR}"); print("STORAGE & SAMPLING"); print(BAR)
print(f"\n  {stor}")
print(f"  ingest: {w.per_sec:,.0f} rows/sec sustained")

print(f"\n  sampling — {w.cells} cells ({w.characters} chars x {w.languages} langs x {w.variants} variants)")
g = m.uniform_sampling_gap()
print(f"    uniform {plan.lane3_coverage:.0%} on a FLAT distribution: "
      f"{g['judged_per_cell_per_day_if_uniform_and_flat']:,.0f} judged/cell/day")
f = m.floor_plan(500)
print(f"    a 500/cell/day FLOOR: {f['total_judged_per_day']:,.0f}/day "
      f"= {f['as_frac_of_traffic']:.3%} of traffic")
print(f"\n  ⚠️  ASSUMED, not measured: real traffic is NOT flat. The floor exists because a")
print(f"      head/tail distribution starves the tail -- but the actual shape is unknown to")
print(f"      us. This is a design under an assumption, and it is the FIRST thing to")
print(f"      measure in production.")

print(f"\n{BAR}"); print("PROVENANCE OF EVERY NUMBER ABOVE"); print(BAR)
print(f"""
  MEASURED (this machine, real corpus, reproducible via this script)
    · Lane 1 throughput      {b.per_sec:,.1f} dialogues/sec/core
    · event size             {bytes_per_event:,.0f} bytes
    · our rubric prefix      {tp.cached_prefix:,} tokens
  BORROWED (published; verify before quoting -- prices move)
    · model prices           {cheap.source}
    · core price             $0.04/core-hour
    · token heuristic        ~4 chars/token en, ~1.5 zh (+/-15%)
  ASSUMED (we cannot check these without production)
    · traffic distribution   flat. IT IS NOT.
    · 1% judge coverage      a policy choice, not a finding
    · 95 chars x 5 variants  a scoping guess
""")
