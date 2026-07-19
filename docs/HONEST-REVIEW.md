# Honest review

2026-07-18. What was built, what works, what doesn't, and what I got wrong. The platform is now a
**DB-backed local service** (`python3 -m ceval`) — the measurement findings and honest limits below
are unchanged by that; the plumbing moved from files to a database, the science did not.

---

## 1. Requirement coverage

| | requirement | status | evidence |
|---|---|---|---|
| **R1** | lifecycle: create → evaluate → ship → monitor | ✅ | `lifecycle.py`; `promote()` refuses LIVE without CANARY |
| **R2** | candidate vs live + evidence | ✅ | `ShipDecision`: delta + CI + **MDE** + shrunk slices + **what it cannot measure** + human veto |
| **R3** | monitor live on production-like traffic | ✅ | `online/collector.py` — 4 injection points, Tier 0 inline |
| **R4** | drill-down: language / character | ✅ | shrunk cells + intervals; **pooling raises** |
| **R5** | quality **and safety** at minimum | ✅ | `safety/` — regurgitation, crisis+escalation, refusal frontier; **31 controls** |
| **R6** | two-phase | ✅ | one instrument, two data sources |
| **R7** | the collection contract | ✅ | `online/events.py` — `gen_ai.*` + `eval.*`; refusal ≠ zero |
| **R8** | roleplay dimensions | 🟡 | 5 judge-free + 2 craft. Fidelity needs the judge lane |
| **R9** | same baseline | 🟡 | paired compare + pooling refusal. **BT/anchors need the key** |
| **R10** | storytelling / game dimensions | 🟡 | **2 of 4 ship**; 2 degenerate and say so in-code |
| **R11** | dry-run → online → loop | ✅ | `scripts/e2e.py` — six stages, real data, no key |
| **C1** | traceability | ✅ | content-addressed; `RebaselineRequired` |
| **C2** | 50M/day with **real numbers** | ✅ | **measured**: 386 dlg/sec/core → 1.5 cores → **$1.44/day** |

**10 of 13 fully met. 3 partial. 0 unmet.** Everything partial is blocked on the API key or on
authoring, not on design.

Verified this run: **31/31 safety controls · 4/4 core refusals · e2e all six stages · the service
reproduces from a fresh DB (init → seed → eval run → dashboard/serve) · 6,812 LOC · zero
dependencies.**

## 2. What actually works

- **The end-to-end flow runs on real data with no key.** Dry-run **rejects deepseek-v3.2 before
  spending a cent on judging** (>40% looping, >50% length-cap violations); the benchmark
  independently returns **NO-SHIP** (Δ=+0.1083, CI excludes zero, effective n = **45 conversations**).
- **The refusals are real, not documentation.** A metric with no confound test **does not import**.
  `role=GATE` without a noise floor **does not import**. Pooling across languages **raises**. A
  card-aware simulator **cannot be constructed**. A `CrisisPipeline` without an escalation sink
  **cannot be constructed**. `Session.mean_turn_score()` **raises**.
- **C2 is a demonstration, not a citation.** Lane 1 measured at 386 dialogues/sec/core → **1.5 cores
  at 50M/day = $1.44/day**. The "Lanes 0–2 are free" claim, on which the whole tiering rests, is now
  tested rather than asserted.
- **The platform is a service, reproducible from a clean clone.** `python3 -m ceval init && seed &&
  eval run --sim && dashboard` runs end to end on committed demo data with zero dependencies and no
  key; `serve` re-renders live from the DB on every request. Models, prompts, variants, grades, and
  evidence are content-addressed and persisted — SQLite runnable, MySQL designed (one schema, two
  drivers). Injecting a variant while `serve` is running shows it on the next request, no restart.

## 3. What doesn't work, stated plainly

| | |
|---|---|
| **wimp rate** | spread **0.12**, no noise floor. Flagged degenerate **in its own caveats** |
| **slop rate** | **0.000–0.014**. A 12-pattern hand list is far too small. Construct sound, build isn't |
| **homogenization (zh)** | unresolved length residual **ρ=+0.264** |
| **Lane 3 entirely** | **0 validated.** Our κ, position-bias, sentiment-bias, abstention: all unknown |
| **Q-series** | **0 built, 0 possible offline.** The corpus has no users |
| **N3 / N7 / C5 world-state** | designed, not built — need a judge or NLI |
| **noise floors** | **1 of ~50 dimensions** has one |

## 4. What I got wrong — the pattern, five times

Every single one produced a **plausible number first**, and none looked like a failure.

| # | it reported | it was | caught by |
|---|---|---|---|
| 1 | a clean homogenization ranking | **verbosity** (ρ=+0.73 with length) | a confound check nobody required |
| 2 | a cleaner ranking after the fix | **survivorship** — 3 of 45 characters funded the budget | reading the coverage column |
| 3 | **p = 0.006**, significant | **p = 0.070**, null — a hand-rolled `betainc` | the same output printed a contradicting critical value |
| 4 | "~8M MAU", cited 5 times | **no source exists** — SEO aggregators citing each other | a research agent tracing it |
| 5 | 1,270 memorised spans · 8 PII hits · 0.02% parroting | **the scripted prologue · 11/11 false positives · a constant** | positive controls |

**And the sixth, today:** three craft metrics degenerate because I used *"has an `*action*`"* as the
test for "moved the scene" — when **my own note 09 recorded that 89.7% of en turns contain one.** I
used a predicate that is *always true in this corpus* as a discriminator. Fixing it to *"introduces a
new entity"* moved the spread from 0.86–1.00 (saturated) to 0.31–0.78 (2.5×, discriminating).

**The lesson is not "be careful."** I was careful. It's that **plausibility is worthless as a signal**
and the only thing that ever caught these was a *redundant check nobody was required to run*: a
confound test, a coverage column, a second statistic, a positive control.

That is why those checks are **import-time errors** in this codebase and not review items.

## 5. What I'd do next, in order

1. **B5 steerability — the first use of the key.** A variant *is* a prompt. If prompts don't move the
   model, the variant lifecycle is a ritual and this platform's premise fails. **The DEAD hypothesis
   is the prior**, not the tail risk. Find out in week one.
2. **Our own judge κ.** Every Lane 3 number is borrowed. The literature ceiling is κ≈0.53; ours is
   unknown, and a counterexample in our exact condition shows ICC collapsing **.88 → .05** depending
   on what is asked.
3. **The proper-noun card-awareness test.** Cheap, offline, and it settles whether every drift number
   from this corpus is a lower bound.
4. **Legal review.** EU Art 50 landed **2026-08-02** — 16 days. The Chinese statute is corroborated by
   two independent streams and still needs counsel on the gazette.
5. **Production traffic shape.** The 500/cell/day floor rests on an **assumed** flat distribution. It
   is not flat. First thing to measure.

## 6. The honest summary

**This is a working measurement instrument with most of its dimensions unvalidated, and it says so
everywhere — in the output, in the caveats, and in the type system.**

What it can do today: score 11 variants on real data, refuse to lie about languages it can't compare,
shrink a drill-down that would otherwise manufacture a story every release, block a ship on a
measured regression, reject a bad variant before spending money, collect production data with
escalation wired in, and cost out 50M/day from numbers it measured itself.

What it cannot do: tell you whether users will like a variant. That needs users, and no offline
benchmark — ours or anyone's — has any.
