# Companion Variant Evaluation Platform

**Status:** Research complete (11 streams), design in review, implementation not started.
**Last updated:** 2026-07-16

---

## 1. Mission

Make ship/no-ship decisions about AI companion variants **trustworthy** — before launch and in
production.

Users chat with characters. Every conversation runs on a **variant**: model + params + system
prompt wrapped around a character description. One variant serves all characters. This platform
owns the variant lifecycle end to end: create → evaluate → ship/no-ship with evidence → monitor.

### The reframe that drives every design decision

This is **not a deployment problem. It is a measurement problem.**

The hard question is not "how do we run evals at scale" — that's plumbing, and the numbers say
it's easy (3,600× ingest headroom, §6). The hard question is: **how do you put a number on
"creativity" or "character fitting" such that the number means the same thing for model A as for
model B, is stable enough to detect a regression, and survives someone asking "why is this a 3.2
and not a 4?"**

If the instrument is bad, the platform is an expensive random number generator that produces
confident, well-formatted, wrong answers. We have already demonstrated in-house how easy that is
to do by accident — twice, in one afternoon, on a metric the literature recommends
([09](research/notes/09-offline-probes.md)).

### What we can and cannot promise

Measured, from the literature:

| | |
|---|---|
| Human–human agreement on roleplay quality | **Krippendorff α = 0.25–0.34** |
| LLM judge scoring creativity *absolutely* vs humans | **r = 0.159**, 40% run-to-run consistency |
| Best judge, chance-corrected, every mitigation stacked | **Cohen's κ ≈ 0.53** |
| Same judges on *pairwise* comparison | **73–78%** human agreement |

> **We cannot sell stable aesthetic scores. Nobody can — humans can't either.**
> **We can sell stable violation rates against a fixed spec.**

This matches MiniMax's own pivot: *"misalignment is surprisingly objective."* The method is to
decompose every soft dimension until the objective part falls out, and send only the irreducible
residue to a judge. "Creativity" = novelty (computable) + non-slop (computable) + constraint
satisfaction (computable) + charm (judge). Three of four need no model call.

---

## 2. Requirements

### From the brief

| ID | Requirement |
|---|---|
| **R1** | Own the variant lifecycle: create → evaluate/compare → ship/no-ship with evidence → monitor |
| **R2** | Evaluate a candidate against what's live: how does it compare, does it regress, is it safe to ship — with a recommendation backed by evidence |
| **R3** | Monitor live variants over time on production-like traffic |
| **R4** | Support drill-down: a variant can pass overall but fail one language or a set of characters — that must be visible |
| **R5** | Dimensions are our call; quality and safety at minimum |
| **C1** | **Traceability** — every score or verdict traceable to the variant, the evaluator version, and the data it ran on |
| **C2** | **Scale** — assume 50M generations/day; demonstrate the design holds with real numbers |

### Added in scoping

| ID | Requirement |
|---|---|
| **R6** | Two-phase: (a) pre-launch benchmark gate; (b) post-launch evaluation on real user dialogue lifecycles, behavior, inputs & outputs |
| **R7** | Define the **collection contract** — what the product must emit for any of this to be evaluable. There is no app behind this; we specify the instrumentation |
| **R8** | Roleplay-specific dimensions, not generic helpfulness: creativity, storytelling, character fitting, and others we identify |
| **R9** | **Same baseline for every model** — scores must be comparable across models |
| **R10** | Dimensions for **storytelling and role-game simulation** specifically |
| **R11** | The system: local model dry-run → online conversation collection → evaluation loops |

### Non-goals

- Not a serving/routing system. We measure variants; we don't run production inference.
- Not a training pipeline. Findings feed humans, not a reward model — see §6, feedback contamination.
- Not a general LLM eval harness. Companion roleplay only; the specificity is the point.

---

## 3. Constraints and context

- **Dataset stands in for production.** `MiniMaxAI/role-play-bench`: 95 characters (45 en / 50 zh),
  11 models × 3 runs × 102 turns = 3,135 dialogues, ~320k turns. Balanced factorial, no missing
  cells. The dataset's published scores (`evaluations.jsonl`) are **quarantined** — the brief
  forbids using them.
- **The brief's replay premise was wrong and we corrected it.** User turns are *not* shared
  traffic: across the 11 models on the same seed, they diverge at the **second user turn, in 100%
  of cases** ([00](research/notes/00-dataset-ground-truth.md)). Replaying the **user** half is
  still defensible; freezing the **assistant** half is not.
- **Legal is not optional and has a calendar** (desk research — needs counsel review):
  NY GBL Art. 47 (in force 2025-11-05) and CA SB 243 (in force 2026-01-01) require a
  suicidal-ideation detection-and-referral protocol, published, for **all users**; AI-status
  disclosure at session start and every 3 hours; **crisis-referral counting** for reporting from
  2027-07-01, making 2026 the first reporting year. SB 243 §22605 carries a **private right of
  action at $1,000/violation**. §22603(d) mandates *"evidence-based methods for measuring
  suicidal ideation"* — a statutory mandate for validated measurement. **EU AI Act Art. 50: 2026-08-02.**

---

## 4. What we measured ourselves (not borrowed)

These are the load-bearing local findings. All judge-free, all reproducible from
[`scripts/`](scripts/).

| Finding | Number | Consequence |
|---|---|---|
| **Run-to-run noise exceeds between-model signal** | σ_within 0.0847 > σ_between 0.0600 (en) | **A single conversation is not evaluable.** Any per-dialogue score is a coin flip with a decimal point |
| **Model rankings do not survive a language change** | Spearman(en, zh) = **−0.082** | **Refuse to emit a pooled cross-language number.** Language is a measurement context, not a slice |
| **Per-character drill-down is hollow at n=3** | MDE per cell = **19.4pp**; 2pp needs **281 runs** | Drill-down must use shrinkage; **never display a raw per-cell score** |
| **Benchmark is underpowered for real decisions** | resolves ~2pp; 1pp needs **194 characters** (have 45) | Add runs (cheap) — generation is ~100× cheaper than judging |
| **Length spans 95×** | 40 → 3,783 chars/turn | Every unnormalized metric is a verbosity ranking |
| **The obvious metric is dead** | "as an AI" ≤ 3.2/1000 turns, zero for most models | Tripwire, not a dimension |
| **Repetition works and is free** | separates models at **10–13× MDE** | Ship it. grok-4.1: 1.4% en → **29.6% zh** (21× swing) |

---

## 5. Plan

### Phase 0 — Research ✅ complete
11 streams, 210 raw sources, 12 synthesis notes. See [RESEARCH-PLAN.md](docs/RESEARCH-PLAN.md)
for status, gaps, and what still needs investigation.

### Phase 1 — Design (in review)
- [11 — evaluation method](research/notes/11-evaluation-method-design.md): which fields, how to
  grade, how to normalize. **Awaiting review.**
- [FLOWS.md](docs/FLOWS.md): system flows end to end.
- Open decisions in §7 must be closed before build.

### Phase 2 — Offline engine
Lane 0–2 (judge-free) first, because they're validated and free. Then Lane 3 (judge) — **blocked
on API key**. Every dimension gated on declaring its own noise floor.

### Phase 3 — Online half
Collection contract, sampling, drift detection, cost model at 50M/day, load test.

### Phase 4 — Drill-down + decision surface
Hierarchical model, shrunk slices, ship-gate report.

---

## 6. Acceptance criteria

Testable. A criterion that can't fail isn't one.

### Traceability (C1)
- **AC1** — Every score row carries `(variant_id, evaluator_version, dataset_version,
  judge_snapshot, prompt_hash, decoding_params, seed)`. Test: pick any number in any view, get
  full lineage in one click.
- **AC2** — Re-running an eval from its manifest reproduces the number, or reports the variance
  and why. Test: automated replay of a stored manifest in CI.
- **AC3** — A judge version bump is a **breaking change**: old scores are never silently
  rescaled onto a new judge. Test: attempt it; the system must refuse.

### Measurement validity (R9)
- **AC4** — **No dimension ships without a declared noise floor**: σ_within, MDE at planned
  sample size, registered confound tests (length at minimum) with measured residuals. Test: CI
  gate rejects a dimension lacking any of these.
- **AC5** — Judge dimensions additionally declare **κ vs a human calibration set** and their
  **abstention rate**. Percent agreement is never reported.
- **AC6** — The platform **refuses** to emit a pooled cross-language score. Test: request one;
  it must decline with the reason.
- **AC7** — **No raw per-cell score is ever displayed** — a shrunk estimate with its interval, or
  nothing.
- **AC8** — Effective n is **conversations, not turns**. Test: no view displays turn-pooled n.

### Decision quality (R2)
- **AC9** — A ship recommendation states: the delta, its interval, the MDE, which slices moved,
  which dimensions abstained, and **what it could not measure**.
- **AC10** — A **qualitative signal can block a ship when every quantitative signal is green.**
  Non-negotiable: OpenAI's April 2025 sycophancy rollback happened *because* A/B tests approved
  the model and expert dissent was overruled. Test: the ship gate has a human veto that requires
  no statistical justification.
- **AC10b** — **The gate compares intervals, never point estimates.** Every CI tool surveyed fails
  a PR "if any metric regresses" — at our measured noise floor that fires on **every** PR and gets
  disabled within a fortnight. A gate that doesn't know its own MDE is theatre. **This is the
  differentiator, not the harness.** Test: submit a variant with a delta below MDE; the gate must
  pass it *and say so*.
- **AC10c** — **The benchmark accumulates, never replaces.** Mined cases are our own models'
  output; curation that replaces human-authored anchors runs the model-collapse experiment on our
  eval set, after which it **reports improvement forever by construction**. Test: CI enforces a
  provenance cap on `eval.provenance`; a PR breaching it fails.

### Safety (R5) — legally load-bearing
- **AC11** — Crisis detection is wired to **escalation**, not just logging. In the Raine case the
  classifier fired **377 times, 23 above 90% confidence, and nothing happened.** **Detection
  without escalation is worse than none — it manufactures the plaintiff's exhibit.** Test: an
  end-to-end drill from detection to a human.
- **AC12** — Crisis referrals are **counted and reportable** (CA SB 243 §22603(a)(1)).
- **AC13** — Over-refusal is measured as a **first-class defect alongside harm**, never averaged
  with it. A refusal that breaks character is a product bug.

### Scale (C2)
- **AC14** — Cost model at 50M/day from **measured** unit costs, with the tiering that makes it
  affordable. Current estimate: **$774/day (~$283k/yr) vs $26.9M/yr** to judge everything with
  the cheapest judge — **95× reduction**.
- **AC15** — Every cell (95 chars × 2 langs × N variants) reaches detection in ~2 days, not 21.
  Uniform 1% sampling fails this; a **500/cell/day floor** fixes it at the same budget.
- **AC16** — Load test the ingest path; demonstrate headroom.

---

## 7. Open decisions (blocking build)

1. **Keep or cut `emotional attunement`?** Judge sentiment bias is **RR 0.60–0.80, degrading to
   0.24–0.66 under sadness/anger/fear, with no published mitigation** — and that is exactly what
   companion traffic is made of. Defensible either way; not defensible by default.
2. **Fix the underpowered benchmark how?** More runs/cell (cheap) or more characters (authoring
   cost)? Currently ~2pp resolvable; a real ship decision needs ~1pp.
3. **Governance:** confirm AC10 — a qualitative signal can block a green ship.
4. **Legal review of SB 243 / NY Art. 47 this week?** It has a calendar; nothing else here does.
5. **API key** — gates every judge-lane experiment (our κ, our position-bias exposure, our
   sentiment-bias exposure, abstention rate). Everything to date is judge-free.

## 8. Known risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| **Judge sentiment bias** | Unfixable at our altitude; sits on our core traffic | Measure our exposure, publish as a limitation, never let it gate alone |
| **Confident wrong numbers** | Demonstrated twice locally in one afternoon | Confound tests are part of a metric's definition, not a review step |
| **Consequential validity** | For each dimension, name the model that wins by gaming it. **"Engagement" gamed = emotional dependency** — we'd build a sycophancy optimizer and call it quality | Named owner per dimension; engagement proxies never headline |
| **Feedback contamination** | Curating production data our own models generated | Findings feed humans, not a reward model |
| **Slice false alarms** | 190 cells at α=.05 → ~9.5 false regressions/dimension/release. Teams correctly learn to ignore us | Pooled pre-registered gate blocks; FDR-controlled slices inform only |
