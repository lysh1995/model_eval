"""Does the grade book actually GRADE? Ground-truth validation.

Every prior test checked "does it run". This checks "is the score correct" -- the only
question that matters for an eval platform, and the one I had not answered.

Method: construct synthetic variants with a KNOWN injected defect, run them through the real
scoring code, and assert the score CATCHES the defect and RANKS variants in the known order.
A grade book that cannot distinguish a looping model from a clean one is a random number
generator with good documentation.

Run: PYTHONPATH=. python3 tests/test_gradebook.py
"""
import sys, statistics as st
sys.path.insert(0, ".")

from ceval.metrics.builtin import Repetition, LengthCapAdherence, Discriminability, Homogenization
from ceval.metrics.craft import Initiative
from ceval.stats import variance_components, shrink, compare, pool_across_languages, \
    PooledCrossLanguageRefused
from ceval.online.events import GenerationEvent, FinishReason, score_or_missing
from ceval.online.session import SessionAssembler

PASS, FAIL = [], []
def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"  — {detail}" if detail else ""))

def ai(text, rnd): return {"role": "ai", "round": rnd, "text": text}
def user(text, rnd): return {"role": "user", "round": rnd, "text": text}

def dialogue(ai_texts):
    turns = []
    for i, t in enumerate(ai_texts):
        turns.append(ai(t, i*2))
        turns.append(user("and then?", i*2+1))
    return turns


# ============================================================ REPETITION grades looping
print("\n=== REPETITION: must rank a looping variant WORSE than a clean one ===")
rep = Repetition("en")
clean = dialogue([f"The {w} moved through the {p} at dawn." for w, p in
                  [("fox","forest"),("ship","harbor"),("clock","tower"),("river","valley"),
                   ("crow","field"),("lantern","alley"),("horse","meadow"),("bell","chapel")]])
looper = dialogue(["I understand how you feel, I really do, tell me more about that."] * 8)
r_clean = rep.compute({"c": clean})["c"]
r_loop = rep.compute({"l": looper})["l"]
check("clean variant scores low repetition", r_clean < 0.10, f"{r_clean:.3f}")
check("looping variant scores high repetition", r_loop > 0.40, f"{r_loop:.3f}")
check("looper ranked WORSE than clean", r_loop > r_clean, f"{r_loop:.3f} > {r_clean:.3f}")


# ============================================================ LENGTH CAP grades its own spec
print("\n=== LENGTH CAP: must catch a variant ignoring its own 150-word instruction ===")
cap = LengthCapAdherence(150)
obedient = dialogue(["A short reply."] * 6)
windbag = dialogue([" ".join(["word"] * 300)] * 6)
c_ob = cap.compute({"o": obedient})["o"]
c_wb = cap.compute({"w": windbag})["w"]
check("obedient variant: 0 violations", c_ob == 0.0, f"{c_ob:.3f}")
check("windbag variant: violates on every turn", c_wb == 1.0, f"{c_wb:.3f}")


# ============================================================ DISCRIMINABILITY grades the asset
print("\n=== DISCRIMINABILITY: distinct characters must beat a one-voice model ===")
dis = Discriminability("en", budget=60)
# a model that gives each character a distinct vocabulary
distinct = {
    "pirate": ["Arr, the briny deep calls, ye scurvy landlubber, hoist the mainsail now!"] * 40,
    "wizard": ["By the arcane sigils of eld, the ley-lines thrum with eldritch power tonight."] * 40,
    "doctor": ["The patient presents acute symptoms; administer the antibiotic and monitor vitals."] * 40,
}
# a model that renders every character in the SAME voice (the catalogue-collapse failure)
collapsed = {
    "pirate": ["I understand how you feel and I am here for you always my friend."] * 40,
    "wizard": ["I understand how you feel and I am here for you always my friend."] * 40,
    "doctor": ["I understand how you feel and I am here for you always my friend."] * 40,
}
d_distinct = dis.compute({k: v for k, v in distinct.items()}).get("accuracy", float("nan"))
d_collapsed = dis.compute({k: v for k, v in collapsed.items()}).get("accuracy", float("nan"))
check("distinct characters are identifiable (> chance)", d_distinct > 0.5,
      f"{d_distinct:.2f} vs chance 0.33")
check("collapsed voices are NOT identifiable (~chance)", d_collapsed <= 0.5,
      f"{d_collapsed:.2f}")
check("distinct ranked BETTER than collapsed", d_distinct > d_collapsed,
      f"{d_distinct:.2f} > {d_collapsed:.2f}")


# ============================================================ INITIATIVE grades the treadmill
print("\n=== INITIATIVE: a scene-driver must beat a treadmill talker ===")
ini = Initiative("en")
# introduces new named entities -> drives the scene
driver = dialogue(["Captain Reyes burst in. The Meridian was sinking off Cape Thorne.",
                   "Sergeant Vale drew her blade as the Kesh raiders breached the Gate.",
                   "Doctor Finch produced the Aurelian serum from the Blackwood vault.",
                   "The Chancellor's envoy arrived bearing news from the Iron Court."])
# asks questions, introduces nothing -> the treadmill
treadmill = dialogue(["How does that make you feel? Tell me more?",
                      "And what happened next? Why do you think that?",
                      "Really? How interesting, and then? Go on?",
                      "What else? How so? Can you say more about that?"])
t_driver = ini.compute({"d": driver})["d::treadmill"]
t_tread = ini.compute({"t": treadmill})["t::treadmill"]
check("scene-driver has task initiative", ini.compute({"d": driver})["d"] > 0.3)
check("treadmill talker scores treadmill-positive (talks, moves nothing)", t_tread > t_driver,
      f"tread={t_tread:+.2f} vs driver={t_driver:+.2f}")


# ============================================================ STATS: variance -> the noise verdict
print("\n=== VARIANCE: must SAY a single conversation isn't evaluable when noise dominates ===")
# high within-cell noise, low between-model signal
cells = {}
import random
rng = random.Random(0)
for m in ("A", "B"):
    for ch in range(20):
        base = 0.10 + (0.02 if m == "B" else 0)
        cells[(m, f"c{ch}")] = [max(0, base + rng.gauss(0, 0.15)) for _ in range(3)]
vc = variance_components(cells)
check("variance decomposition returns 4 components summing to ~100%",
      abs(sum(vc.pct().values()) - 100) < 0.01, f"{sum(vc.pct().values()):.1f}%")
check("noise-dominated design triggers the 'not evaluable' verdict",
      "not evaluable" in vc.verdict(), vc.verdict()[:50])


# ============================================================ STATS: gate compares intervals
print("\n=== GATE: a sub-MDE change must be reported as UNDETECTABLE, not 'no regression' ===")
tiny = {}
for m in ("A", "B"):
    for ch in range(45):
        base = 0.10 + (0.001 if m == "B" else 0)   # a 0.1pp difference, far below MDE
        tiny[(m, f"c{ch}")] = [base, base, base]
cmp_tiny = compare(tiny, "B", "A", mde=0.0208)
check("a 0.1pp delta is called UNDETECTABLE (not 'no change')",
      not cmp_tiny.detectable, cmp_tiny.verdict()[:60])

big = {}
for m in ("A", "B"):
    for ch in range(45):
        base = 0.10 + (0.05 if m == "B" else 0)   # a 5pp difference, well above MDE
        big[(m, f"c{ch}")] = [base, base, base]
cmp_big = compare(big, "B", "A", mde=0.0208)
check("a 5pp delta is called REAL", cmp_big.detectable and cmp_big.delta > 0,
      cmp_big.verdict()[:50])


# ============================================================ STATS: shrinkage tames n=3
print("\n=== SHRINKAGE: a noisy 3-run cell must be pulled toward the model mean ===")
noisy_cells = {}
for ch in range(20):
    noisy_cells[("M", f"c{ch}")] = [0.10, 0.10, 0.10]          # quiet cells
noisy_cells[("M", "outlier")] = [0.40, 0.05, 0.35]            # one loud, noisy cell
shrunk = shrink(noisy_cells)
out = shrunk[("M", "outlier")]
check("the noisy outlier cell is pulled toward the mean",
      out.shrunk < out.raw and out.weight < 1.0,
      f"raw={out.raw:.3f} -> shrunk={out.shrunk:.3f}, pulled {100*(1-out.weight):.0f}%")


# ============================================================ REFUSAL != ZERO
print("\n=== SCORE-OR-MISSING: a content-filter refusal is MISSING, not 0.0 ===")
ev_ok = GenerationEvent("m", "c", FinishReason.STOP, 0, 0, "v", "ch", "en", 0, 0, 0.0)
ev_ref = GenerationEvent("m", "c", FinishReason.CONTENT_FILTER, 0, 0, "v", "ch", "en", 0, 0, 0.0)
check("an answered turn keeps its score", score_or_missing(ev_ok, 0.9) == 0.9)
check("a refused turn returns None, NOT 0.0", score_or_missing(ev_ref, 0.9) is None,
      "averaging it as 0 is how over-refusal vanishes from a dashboard")


# ============================================================ THE REFUSAL TO POOL
print("\n=== CROSS-LANGUAGE: the platform must REFUSE to pool ===")
try:
    pool_across_languages(); check("pooling refused", False)
except PooledCrossLanguageRefused:
    check("pooling across languages raises (rho(en,zh) = -0.082)", True)


print(f"\n{'='*72}\n{len(PASS)} passed, {len(FAIL)} failed")
if FAIL:
    print("FAILURES:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
