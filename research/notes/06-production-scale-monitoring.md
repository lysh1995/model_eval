# 06 — Production Scale: Online Eval & Monitoring at 50M generations/day

**Topic owner note.** Synthesis of ~25 `scale-*` sources in `../sources/`. All
arithmetic below is reproducible; the scratch scripts are inline in this note. Pricing
is Anthropic list price as of 2026-06-24 (see `scale-anthropic-pricing-batch-caching.md`
— that file is authoritative, do not re-derive prices from memory).

---

## 0. The headline in one table

Judging all 50M/day with an LLM judge is infeasible **on two independent axes**, and
latency is the binding one:

| | Inline LLM judge | Reality |
|---|---|---|
| **Latency** | 1,000–3,200 ms per judge call | Guardrail budget is **~200 ms p50** |
| **Cost** | $26.9M–$269M/yr | Tiered design: **$283k/yr** |

**Cost is the second reason judging can't be inline. Latency is the first.** Even a free
judge would blow the budget by 5–16x. This matters for how we frame the design: we are
not building a "cheap judge" — we are building a **two-lane architecture** where the
lanes answer different questions on different clocks.

---

## 1. The cross-platform consensus (LangSmith, Braintrust, Weave, Langfuse, Arize, Galileo)

Every major platform converged on the same split, independently. This is the strongest
signal in the whole research pass — it is not one vendor's opinion:

| | **Guardrail** | **Evaluator / Monitor** |
|---|---|---|
| Coverage | **100% — never sampled** | Sampled (1–10% typical) |
| Path | Inline, blocking | Async, off request path |
| Latency | ms; ~200ms ceiling | Seconds–hours; irrelevant |
| Mechanism | regex / small classifier | LLM-as-judge |
| Question | "block this one?" | "is the fleet regressing?" |

W&B Weave states the rule most crisply (`scale-wandb-weave-guardrails.md`):

> **Guardrails have no sampling rate.** Sampling is a monitor-only concept.

This is logically forced: *a guardrail sampled at 10% blocks only 10% of bad content,
which defeats its purpose.* **Guardrails run at 100% or not at all; sampling belongs to
the async tier.** Braintrust is equally explicit that online scoring "does not add
application latency because scoring runs asynchronously after traces are logged."

**Published sampling guidance** — no platform ships a nonzero eval sampling *default*; all
require explicit configuration. But the published *guidance* converges tightly:

| Source | High volume | Critical / low volume |
|---|---|---|
| **Braintrust** | 1–10% | 50–100% |
| **Arize AX** | 1–5% (very high), 10–50% (high) | 100% |
| **Langfuse** (LLM judge) | 5–10% initially | — |

> **Arize's rollout rule is the most actionable thing found in the whole sweep:**
> *"Start at 10–20% and increase once you have validated your evaluator is working
> correctly."* — i.e. **the sampling rate is a function of evaluator maturity, not just
> volume.** Start high while calibrating, ratchet down once trusted.

Langfuse is the sole platform with a documented default, and it's a different layer:
`LANGFUSE_SAMPLE_RATE` defaults to `1` and governs **ingestion**, not evaluation —
unsampled traces don't exist for debugging either.

### ⚠️ The finding that reframes everything: judges have double-digit false-positive rates

- **Arize Phoenix**: at a **12% false-positive rate**, guidance is to *"run them on a
  fraction of production traffic and use **aggregate trends, not individual scores**."*
- **Arize's embeddings guard**: **13.95% FP** on 2,000 regular prompts (86.43% TP on 656
  jailbreaks).

**Individual judge scores are not trustworthy; aggregates are.** This has three
consequences that run through this whole note:

1. **It independently justifies sampling.** Full coverage doesn't fix a noisy evaluator —
   it just buys more wrong verdicts. Sampling costs us little *because the marginal
   information in the 100th sample of a cell is low anyway.*
2. **Never alert on a single bad score.** Alert on distributions (§5). A single Tier-2
   verdict is ~12% likely to be wrong; a shift in a 500-sample cell is not.
3. **It sharpens Tier 3's job.** The gold tier isn't just for hard cases — it is the
   instrument that *measures* Tier 2's FP rate.

### Humanloop's inversion — worth genuinely considering

Humanloop flips the framing: run the **automated evaluator on 100%**, and sample only the
**human** tier, comparing continuously to calibrate the autorater. The scarce resource is
**human attention**, not compute; the sample is an **instrument, not a cost dial.**

This is not what we should do at Tier 2 (a 100% LLM judge is $26.9M/yr — §4), but it is
**exactly the right frame for Tier 1 ↔ Tier 2 ↔ Tier 3.** Our Tier 1 cheap signals *are* a
100%-coverage evaluator; Tier 2 samples to calibrate them; Tier 3 samples to calibrate
Tier 2. Each tier is the measuring instrument for the one below it. That reframing — tiers
as a **calibration chain**, not merely a cost ladder — is the strongest argument for the
architecture and the answer to "how do you know the cheap tier isn't lying to you?"

### Three design details worth stealing verbatim

1. **Filter → sample → evaluate**, universally. Sampling is applied *after* the filter.
   This lets us eval 100% of a flagged cohort and 0.1% of the bulk without separate
   instrumentation. Our stratification (§3) is exactly this pattern generalized.
   ⚠️ **LangSmith rule ordering is *not* guaranteed** — a cascade cannot be expressed as
   rule sequencing; it must be expressed as **feedback-predicate filters** (rule B filters
   on the feedback key rule A wrote). Worth knowing if we build on their primitives.
2. **Trace-level, all-or-nothing sampling via deterministic trace-ID hash** (Langfuse /
   OTel `TraceIdRatioBased`). `hash(trace_id) < rate`. Pure function of trace ID → every
   service reaches the same decision **without coordination**, so traces are never
   partial. Their stated rationale: *"Scores inherit the sampling decision of their
   parent trace to prevent 'orphaned' scores."* Adopt this.
3. **One primitive, two call sites** (Weave). The same Scorer is a guardrail when called
   inline and a monitor when called async — and *"every scorer result from guardrails is
   automatically stored... so your guardrails also function as monitors without any extra
   configuration."* **Our Tier 0 guardrail output is free 100%-coverage monitoring data.**
   This is a significant and easy win: it gives us a full-population signal to cross-check
   the sampled tiers against.

---

## 2. Reference tiered architecture

```
                       50M generations/day  (579/sec avg, ~2,300/sec peak @4x diurnal)
                                 │
   ┌─────────────────────────────┼──────────────────────────────┐
   │                             │                              │
┌──▼───────────────┐   ┌─────────▼──────────┐   ┌───────────────▼────────┐
│ TIER 0  100%     │   │ TIER 1  100%       │   │ TIER 2  ~1% stratified │
│ 50M/day          │   │ 50M/day            │   │ 500k/day               │
│ INLINE GUARDRAIL │   │ CHEAP SIGNALS      │   │ ASYNC LLM JUDGE        │
│ blocking         │   │ async, no LLM      │   │ Haiku 4.5, batch+cache │
├──────────────────┤   ├────────────────────┤   ├────────────────────────┤
│ regex / classifier│  │ logprobs, length   │   │ rubric score, sycophancy│
│ crisis, autofail │   │ refusal rate, dedup│   │ persona adherence      │
│ PII, jailbreak   │   │ embedding centroid │   │ dependency signals     │
│ 5–50ms; ≤200ms   │   │ ~0 marginal cost   │   │ seconds; $738/day      │
└──────────────────┘   └────────────────────┘   └──────────┬─────────────┘
                                                            │ escalate
                                                            │ low-confidence
                                                 ┌──────────▼─────────────┐
                                                 │ TIER 3  ~0.01%         │
                                                 │ 5k/day  GOLD JUDGE     │
                                                 │ Opus 4.8, batch        │
                                                 │ $37/day                │
                                                 │ + human review queue   │
                                                 └────────────────────────┘
```

### What runs where, and why

**Tier 0 — inline guardrail, 100%, blocking.** Only **autofail conditions** from the
InvisibleBench taxonomy (`scale-invisiblebench-companion-gate.md`): crisis/self-harm
disclosure, abuse-enabling, PII, jailbreak. These are catastrophic, classifier-detectable,
and unacceptable to catch 6 hours later.

> **Critical asymmetry:** the standard "run the guardrail in parallel with the LLM call so
> it's free" trick (`scale-guardrail-latency-budgets.md`) **only works on the input side** —
> you can fire both at t=0. An **output** guardrail cannot run in parallel with the
> generation that produces its input. It is strictly serial and its latency adds to the
> user-visible total. Output-side checks must therefore be much cheaper than input-side
> ones, or must operate on streaming chunks.

Galileo's Luna-2 gives the only hard published guardrail numbers — and its latency
*shape* is the important part (`scale-galileo-luna2-benchmarks.md`):

| Input size | Latency |
|---|---|
| 500 tokens | **15 ms** |
| 2K tokens | **15 ms** |
| 15K tokens | 141 ms |
| 100K tokens | **2.8 s** |

**Latency is flat to ~2K tokens, then scales with context — it is prefill-dominated.**
So *guardrail latency is a function of how much context you feed it, not of verdict
complexity.* Trimming judge input is the highest-leverage latency optimization. And at
100K tokens even a fast small model is 2.8s — **long-context checks cannot be inline at
any price.** For a roleplay product with long sessions, this is decisive: Tier 0 must
score the **current turn**, not the accumulated session.

**Tier 1 — cheap signals, 100%, async, no LLM.** Nearly free and enormously useful:
refusal rate, output length distribution, n-gram repetition/slop, embedding centroid
drift, latency, error/`stop_reason` rates. This tier is what makes 100% coverage
statistically meaningful. **Most regressions will be caught here first** — a variant that
breaks usually shows up as a shift in length or refusal rate long before a rubric score
moves. Cheap proxies are not a consolation prize for the unsampled traffic; they are the
first line of detection.

**Tier 2 — async LLM judge, ~1% stratified (see §3 — *stratified*, not uniform).**
Haiku 4.5, Batch API, prompt-cached rubric. Rubric-scored dimensions: persona adherence,
sycophancy, dependency, quality.

**Tier 3 — gold judge, ~0.01% + escalations.** Opus 4.8. Two jobs: (a) score
low-confidence Tier-2 items via cascade, (b) serve as a **fixed audit sample** that
validates Tier 2. Job (b) is not optional — it's how we know the cheap judge hasn't
drifted.

### Sampling unit: the SESSION, not the generation

**This is the most important architectural consequence in this note and the easiest to get
wrong.** From `scale-invisiblebench-companion-gate.md`: boundary erosion, dependency, and
persona drift are **properties of a conversation trajectory, not of a single generation.**

A per-generation sampler at 1% will draw generation #47 of a session with no visibility
into #1–46 — and will see nothing wrong. **A per-generation sampling design is structurally
blind to the failure modes that matter most for companion AI.**

→ **Tier 2 must sample whole sessions (or session suffixes), keyed by deterministic hash
of `session_id`.** This aligns with Langfuse's trace-level all-or-nothing rule and avoids
orphaned scores.

Arize has already formalized the semantics and they're worth copying verbatim:

> *"Sampling is applied at the highest evaluator scope: **session > trace > span**, and
> lower-level evaluators run on all matching data within that sampled set."*

> ⚠️ **Sampling unit ≠ billing unit.** 10% *session* sampling on a 50-turn companion
> session is far more eval calls than naive math suggests. **Budget in judge calls, not
> generations** — §4's model is per judge call. Given the 2K-token latency cliff above,
> a **session suffix (last N turns)** is the pragmatic unit: it preserves trajectory
> context while bounding judge input.

---

## 3. Sampling math — why uniform 1% fails, and the fix that costs the same

### The slicing space

95 characters × 2 languages × 5 variants = **950 cells**.

### Sample size to detect a regression

Two-proportion test, 80% power, α=0.05, two-sided, baseline failure rate p₀=5%:

| Effect | Judged samples needed **per arm** | Raw gens needed @ 1% sample |
|---|---|---|
| 5% → 10% (+5pp) | **434** | 43,443 |
| 5% → 8% (+3pp) | **1,059** | 105,886 |
| 5% → 7% (+2pp) | **2,212** | 221,220 |
| 5% → 6% (+1pp) | **8,158** | 815,773 |

**Detecting a 1pp shift needs ~8,200 judged items per arm.** That is the number to quote
when someone asks "why can't we just sample less?"

### Uniform 1% sampling: the head is drowning, the tail is starving

Traffic across 95 characters will be Zipfian, not uniform. Under a flat 1%:

| Cell | Raw/day | Judged/day | Days to detect 5%→8% |
|---|---|---|---|
| Head char (20% of traffic) | 10,000,000 | **100,000** | < 0.1 |
| Mid (1%) | 500,000 | 5,000 | 0.2 |
| Tail (0.1%) | 50,000 | 500 | 2.1 |
| **Deep tail (0.01%)** | 5,000 | **50** | **21.2** |

Two failures at once: the head cell gets **100,000 judged/day when it needs ~1,000** —
100x waste — while the deep tail takes **three weeks** to detect a 3pp regression. A
regression in a niche character ships and sits undetected for most of a month.

### The fix: stratified allocation with a per-cell floor — for the same budget

| Floor per cell/day | Total judged/day | % of traffic | Days to n=1,059 |
|---|---|---|---|
| 200 | 190,000 | 0.38% | 5.3 |
| **500** | **475,000** | **0.95%** | **2.1** |
| 1,000 | 950,000 | 1.90% | 1.1 |

> **A 500/cell/day floor across all 950 cells costs 475,000 judged/day = 0.95% of
> traffic — essentially identical to the uniform 1% budget (500,000/day).**

Same spend. But every cell now detects a 3pp regression in **~2 days** instead of ranging
from 0.1 days to 3 weeks. We are not asking for more budget; we are asking to stop
spending 100x too much on the head. **This is the single highest-leverage design decision
in the note.**

Practical shape: `π_cell = clamp(min_floor / cell_traffic, π_min, π_max)` — cap head
cells, floor tail cells, recompute weekly from traffic.

### The correction that makes it honest

Once sampling is non-uniform, **the judged set is no longer representative of production**
and a naive average over it is a **biased** estimate of true quality
(`scale-horvitz-thompson-reweighting.md`). Horvitz–Thompson inverse-probability weighting
(`T̂ = Σ y_i/π_i`) is the standard fix — **but HT is unbiased with high variance when π is
tiny**, and a tail cell at π=0.0001 carries weight 10,000, which will make the top-line
metric jitter.

**Recommendation — sidestep the variance entirely by running two samples with two jobs:**

| Sample | Job | Reweighting |
|---|---|---|
| **Uniform ~0.1%** (50k/day) | Global top-line metric | None needed — weights constant |
| **Stratified floor** (475k/day) | Per-slice metrics | **None needed** — reported *within* slice |

Reweighting is only required when *aggregating across strata*. A dashboard reading
"character X failure rate = 4.2%" uses only character X's own sample and is unbiased with
no weights. **Report per-slice metrics per-slice; keep a separate uniform sample for the
global roll-up.** If we must aggregate across strata, clip/winsorize the weights or use
the Hájek ratio estimator, and always publish a variance estimate.

> **Schema requirement:** every judged record must persist its **inclusion probability
> `π_i`** (or stratum ID + rate) *at sample time*. Sampling rates will change as we re-tune
> strata; once they do, π_i is **not recoverable** from a config file, and every historical
> global estimate becomes uncomputable. **π_i is lineage, not telemetry.**

---

## 4. Cost model — real numbers, plug-and-play

**Prices** (Anthropic list, 2026-06-24): Haiku 4.5 **$1/$5** per MTok · Sonnet 5 **$3/$15**
· Opus 4.8 **$5/$25**. Batch API = **50% off**. Cache read ≈ **0.1×** input; cache write
1.25× (5-min TTL).

**Judge call shape (the parameters to tune):**

| Component | Tokens | Note |
|---|---|---|
| Rubric (cached prefix) | **4,500** | ⚠️ see cache-minimum trap below |
| Transcript (varying suffix) | 1,500 | |
| Output (structured score + rationale) | 200 | |

> ### ⚠️ The cache-minimum trap — a real, silent design constraint
> **Haiku 4.5 and Opus 4.8 require a ≥4,096-token prefix to cache at all.** Below that the
> cache **silently does not engage** — no error, just `cache_creation_input_tokens: 0` and a
> 2.4x cost overrun nobody notices. Sonnet 4.6/Fable 5 need only 2,048.
> **Our rubric must be ≥4,096 tokens on the Haiku tier** — which inverts normal instincts:
> here a *longer* rubric is *cheaper*. Verify with `cache_read_input_tokens > 0` in CI.

### Per-judge-call cost

| Model | Live + cache | **Batch + cache** | Live, no cache |
|---|---|---|---|
| Haiku 4.5 | $0.00295 | **$0.00147** | $0.00700 |
| Sonnet 5 | $0.00885 | $0.00443 | $0.02100 |
| Opus 4.8 | $0.01475 | **$0.00737** | $0.03500 |

### The infeasibility proof (judge 100% of 50M/day)

| Config | Per day | Per year |
|---|---|---|
| 100% Haiku 4.5, live | $147,500 | **$53.8M** |
| 100% Haiku 4.5, batch | $73,750 | **$26.9M** |
| 100% Opus 4.8, live | $737,500 | **$269.2M** |
| 100% Opus 4.8, batch | $368,750 | $134.6M |

**Even the cheapest possible full-coverage judge is $26.9M/yr** — before latency makes it
impossible anyway.

### The tiered design

| Tier | Volume/day | Model | Cost/day |
|---|---|---|---|
| Tier 2 (1%) | 500,000 | Haiku 4.5, batch+cache | **$738** |
| Tier 3 (0.01%) | 5,000 | Opus 4.8, batch | **$37** |
| **Total** | | | **$774/day ≈ $283k/yr** |

**$283k/yr vs $26.9M/yr — a 95x reduction, and ~350x vs live Opus.**

### Sensitivity levers (the numbers to argue about)

**Cascade escalation rate** — Tier 2 → Opus on low confidence:

| Escalation rate | Opus calls/day | Added $/day | Total $/day |
|---|---|---|---|
| 5% | 25,000 | $184 | $959 |
| 10% | 50,000 | $369 | $1,143 |
| **17.5%** (Trust-or-Escalate prior) | 87,500 | $645 | **$1,420** |
| 30% | 150,000 | $1,106 | $1,881 |

Even at 30% escalation we're at **$687k/yr** — still 39x under full-Haiku coverage. **The
cascade is affordable at any plausible escalation rate.** Don't over-optimize this.

**Prompt caching** — Tier 2 alone: **$1,750/day uncached → $738/day cached**, saving
**$1,012/day ($370k/yr)**. *Caching saves more than the entire rest of the platform
costs.* It is the highest-ROI single engineering task in this design.

### Cascade evidence — and one number not to misquote

`scale-trust-or-escalate-cascade.md` (ICLR 2025) is the peer-reviewed basis for tiering,
with a *provable* human-agreement guarantee rather than a hand-tuned heuristic:
`P(agrees with human | LLM evaluates x) ≥ 1−α`.

- Cascade Mistral-7B → GPT-3.5 → GPT-4: **85.8%** human agreement, **63.2%** coverage,
  only **17.5%** of items reached GPT-4, **78.5% cost reduction** vs GPT-4-only.
- On Auto-J the cascade was **more accurate than GPT-4 alone** (80% guaranteed vs
  **63.2%** ungated) — abstention removes the cases where the judge is unreliable.

> ⚠️ **Do not quote 78.5% in a cost model that also uses Simulated Annotators.** The
> paper's own Table 5 shows the cascade at **2.849× GPT-4 cost** when running N=5 simulated
> annotators for confidence calibration. The 78.5% is the *routing* benefit assuming
> calibration is free. The paper reconciles to **">40% cost reduction"**. **Budget ~40% if
> we adopt Simulated Annotators.**

Three caveats before we lean on the numbers: the paper's task is *pairwise preference*
(ours is likely pointwise rubric scoring — the calibration machinery transfers, the
numbers may not); **coverage is 42–63%**, meaning the cascade *declines to score* a large
share; and their base tier was Mistral-7B, far weaker than Haiku 4.5 — so **17.5% is a
conservative escalation ceiling for us.**

> **Abstention is not free — this is a monitoring system, not a benchmark.** An abstained
> item is a *missing data point*, and 40%+ abstention silently guts the per-cell sample
> sizes computed in §3. Two rules: (1) **treat abstention rate as a first-class monitored
> metric — a spike in abstention IS a regression signal**, arguably an earlier one than the
> score itself; (2) size the stratified floor on *post-abstention* n, i.e. inflate the
> floor by ~1/coverage.

---

## 5. Drift detection — do NOT use the KS test

### The finding

At 50M/day, **statistical significance tests are actively harmful.** They measure "do I
have enough data" rather than "did anything change." With n large enough, *every*
difference is significant.

The decisive citation (`scale-evidently-drift-algorithm-defaults.md`): **Evidently AI —
a mature drift library — abandons the KS test entirely above 1,000 observations.**

| Reference size | Numerical | Categorical | Threshold |
|---|---|---|---|
| **≤ 1000** | KS test | chi-squared | p ≤ 0.05 |
| **> 1000** | **Wasserstein (normalized)** | **Jensen-Shannon** | **≥ 0.1** |

**We operate at 50,000,000/day — five orders of magnitude past where the vendor stops
using p-value tests.**

Their empirical study (`scale-evidently-large-dataset-drift-comparison.md`) shows why —
minimum drift magnitude detected at n=100,000:

| Method | Min. drift detected |
|---|---|
| **KS** | **~0.5–1%** ← fires on operationally meaningless noise |
| Wasserstein | ~5% |
| PSI / KL / JS | ~10% |

**Why effect sizes are scale-stable:** PSI has **no n in it** — bin proportions are
normalized. Its value doesn't inflate with sample size, so a fixed 0.1/0.2 threshold means
the same thing at 10k or 10M. That is exactly the property KS lacks.

### PSI reference (`scale-psi-drift-thresholds.md`)

```
PSI = Σ_b (ActualProp(b) − ExpectedProp(b)) × ln( ActualProp(b) / ExpectedProp(b) )
```

| PSI | Interpretation |
|---|---|
| < 0.1 | Similar — no significant change |
| 0.1 – 0.2 | Moderately different — investigate |
| > 0.2 | Significant shift — act |

- **10 bins (deciles) of the reference** is the industry default.
- **Freeze bin edges on the reference.** Recomputing edges per batch destroys
  comparability — a classic silent bug.
- Zero-bin handling: add 0.01 to each proportion, or a base count of 1 (PSI is unbounded
  at a zero bin).
- PSI = symmetrized KL: `KL(E‖A) + KL(A‖E)`. Bounded alternative: JS distance (0–1).

### The peeking problem — the second statistical trap

A monitoring dashboard **is** a continuously-monitored test. From
`scale-always-valid-inference.md`:

> A/B tests analyzed via frequentist p-values are "**wholly unreliable if users
> endogenously choose sample sizes by continuously monitoring their tests**."

**If we recompute a p-value every 5 minutes against fixed α=0.05, the realized false-alarm
rate approaches 1.0.** We *will* alert eventually, guaranteed, on data with no change in
it. Note this is a *separate* problem from large-n over-triggering — fixing one does not
fix the other.

**Fix: anytime-valid inference via e-values.** An e-value is a nonnegative r.v. with
E[·] ≤ 1 under the null. By Ville's inequality, `P(sup_t E_t ≥ 1/α) ≤ α` — **peek
continuously, reject when the e-process exceeds 1/α (= 20 for α=0.05), no correction
needed.** E-values **multiply** across sequential batches, so a running product is the
entire implementation. Trade-off: wider intervals at fixed n — irrelevant for us, since
**at 50M/day we have power to burn.** Trading power for validity-under-peeking is exactly
the right trade here.

### Alert fatigue — the arithmetic

**950 cells × α=0.05 = 47.5 false alarms/day** with *nothing wrong* (17,338/yr). At 3
metrics/cell: **142.5/day.** The alerting system becomes noise and gets ignored. This is
arithmetic, not bad luck.

Fix: **Benjamini–Hochberg FDR** (`scale-multiple-testing-bh-alert-fatigue.md`) — controls
the expected *proportion* of false positives among alerts. Sort p ascending, compare
p₍ᵢ₎ against (i/m)·Q, reject up to the largest passing index. BH is far less
conservative than Bonferroni (which would demand α = 0.05/950 = **5.3e-5** per test and
kill sensitivity to real regressions).

Two refinements that matter for us specifically:

- **Prefer e-BH.** Plain BH assumes independence (or PRDS). **Our slices are correlated by
  construction** — a base-model change moves every character at once. **e-BH requires no
  independence assumption**, and e-values are already our sequential test, so the
  anytime-valid and multiplicity fixes stack in one mechanism.
- **Test hierarchically.** Test the global metric first; descend into per-variant, then
  per-character, **only where the parent moved.** This cuts m by an order of magnitude in
  the common case (nothing wrong → one test, not 950) and matches how an engineer actually
  debugs. It also directly addresses composition drift (§7): if the global moved but no
  slice did, the *mix* changed, not the quality.

### ✅ Recommended stack

| Purpose | Method | Threshold |
|---|---|---|
| **Score distribution drift** per (variant, slice) | **PSI**, 10 frozen reference bins | 0.1 warn / **0.2 alert** |
| **Failure-rate regression** per (variant, slice) | **e-value / confidence sequence** (anytime-valid, two-proportion) | E ≥ 20 (α=0.05) |
| **Multiplicity across 950 cells** | **e-BH (FDR)** | Q = 0.05 |
| **Fast-moving level shift** | **EWMA** λ=0.2, L=3; limits `μ₀ ± Lσ√(λ/(2−λ))` (use L=2.6–2.8 if λ≤0.1). Or **CUSUM** k=0.5, h=5 → in-control ARL≈465, detects 1σ in ~10 obs | Tier-1 cheap signals |
| **Embedding drift** | **domain classifier, ROC AUC > 0.55** (Evidently's recommended default) | Tier-1, 100% coverage |
| **Explicitly rejected** | ~~KS test~~, ~~chi-squared~~, ~~fixed-horizon p-values~~, ~~MMD~~ (O(n²), "hard to set"), ~~cosine centroid~~ (breaks under PCA) | — |

**Run EWMA/CUSUM on hourly aggregates, not raw events.** This decouples sensitivity from
raw volume: you tune ARL in *"hours until false alarm"* — the operationally meaningful
unit — instead of chasing a threshold that shifts with traffic.

**The meta-pattern worth adopting broadly (NannyML): chunk-level 3-sigma calibration.**
Compute any statistic per chunk (say, hourly) over a reference period, take **mean ± 3sd
of the *chunk-level* values**, and alert on excursion. This asks *"is this hour outside the
range this metric normally occupies?"* rather than *"could these samples share a
distribution?"* The former stays meaningful at any n **because reference variability is
measured at the same chunk size as the test.** It generalizes to judge scores, refusal
rates — even to PSI itself, which neatly sidesteps arguing about whether our threshold
should be 0.1 or 0.2 by learning our own normal range.

Rationale for e-values over CUSUM/SPRT: CUSUM and SPRT need a **parametric likelihood and
a pre-specified shift size** — we have neither for a rubric score of unknown distribution.
E-detectors (Shin/Ramdas/Rinaldo) generalize CUSUM to the nonparametric setting and
recover CUSUM as a special case when the likelihood ratio is known. We get the same
"detect a sustained change with controlled false-alarm rate" behavior without committing
to distributional assumptions we can't justify.

---

## 6. Data infrastructure — this is the easy part

### Ingest is a non-issue

| | |
|---|---|
| 50M/day | **579 rows/sec average** |
| Peak @4x diurnal | **~2,300 rows/sec** |
| Single ClickHouse node (measured) | **2.1M rows/sec** (8.8M/s tuned) |
| **Headroom** | **~3,600x** |

`scale-clickhouse-ingest.md` — even at 10 events/generation (5,800/sec) this is a
**single-node-plus-replica workload**, not a cluster. **Storage, query fan-out, and
cardinality are the real constraints; insert throughput is not.** Rule of thumb:
~25,000–50,000 rows/sec/core.

### Storage

Compression: **15–20x** — and the best data point is **Character.AI's own production
number (15–20x)**, an LLM chat product with our exact data shape. LLM traces compress
unusually well (repetitive model names, prompt templates, enum-ish fields). Using 17.5x:

| Event shape | Raw/day | Compressed/day | **Per year** |
|---|---|---|---|
| Metadata-only (200 B) | 10 GB | 0.6 GB | **0.21 TB** |
| Full trace w/ text (3 KB) | 150 GB | 8.6 GB | **3.1 TB** |
| Long roleplay ctx (8 KB) | 400 GB | 22.9 GB | **8.3 TB** |
| Judged scores (500 B × 500k) | 0.25 GB | 0.014 GB | **5.2 GB** |

**Full-fidelity trace retention is ~3–8 TB/yr — trivial.** We do not need to sample for
storage reasons; sample only to control **judge cost**. Worth stating explicitly, because
"sample to save storage" is the wrong instinct here and would destroy our ability to
retro-score.

**Schema codecs** (`scale-clickhouse-compression.md`):
- Timestamps → `CODEC(DoubleDelta, LZ4)`
- Scores/latencies (floats) → `CODEC(Gorilla, LZ4)`
- `character_id`, `language`, `variant_id`, `model` → **`LowCardinality(String)`** → 30x+ tier
- Prompt/completion text → `CODEC(ZSTD(1))` (30% smaller than LZ4; 2–3x slower decompress —
  fine, rarely scanned in aggregates)

### Cardinality is NOT our problem

**The key finding, and it defuses a stated worry in the brief:** 95 × 2 × 5 = **950
combinations**. At hourly grain that's 22,800 rows/day = **8.3M rows/year** — a rounding
error for ClickHouse.

**The character × language × variant cross-product is not a cardinality explosion.** The
danger appears only if unbounded dimensions (`user_id`, `session_id`, `request_id`, raw
text) enter a GROUP BY.

> **Rule: rollup keys must be drawn only from bounded, enumerable dimensions.** Unbounded
> identifiers stay in raw storage (point lookups) or are counted via sketches
> (`uniqState`) — never grouped by.

### Sketches & rollups

- **AggregatingMergeTree** materialized views on (hour, variant, character, language).
  Aggregation ratio ~**2,200:1** — exactly the regime where rollups pay.
- **Distinct counts:** prefer **`uniqCombined`** (sub-1% error) over `uniqHLL12` (2.5 KB,
  ~1.6% at 10K–100M but **~10% below 10K** — ClickHouse explicitly discourages it). Our
  tail cells are small, so the sub-10K regime is exactly where we live.
- **Quantiles — with a real caveat.** Mergeable sketch states are what let per-cell p95s
  compose from hourly to daily without re-scanning raw.
  > ⚠️ **t-digest's relative error exceeds 100% on heavy-tailed simulated latencies**, and
  > **LLM latency *is* heavy-tailed.** **DDSketch** gives a *relative-error guarantee*
  > (γ=(1+α)/(1−α); α=1% → true 100 lands in [99,101]) and is the correct choice on paper.
  > **But ClickHouse ships `quantileTDigest`, not DDSketch.** Options: accept t-digest and
  > validate error against exact quantiles on real latency data before trusting p99s; or
  > keep exact histograms with fixed log-spaced buckets (cheap at 950 cells). **Do not
  > ship a t-digest p99 SLO without validating it first.**

> ⚠️ **Write amplification is the one real infra risk.** One materialized view costs
> **~55% of insert throughput** at 100-row batches; five chained **~80%**; ten **~90%**.
> Mitigate with large batches (`min_insert_block_size_rows=150000`) and **single-digit MV
> counts**; **chain raw→hourly→daily rather than fanning out from raw.** With 3,600x
> ingest headroom (above) we can absorb this — but it's the reason to keep the MV count
> disciplined rather than adding one per dashboard.

**Store:** ClickHouse for the online/serving path. Iceberg/Parquet for cold archive + the
offline retro-scoring path (re-scoring history under a new evaluator version — see §7).
DuckDB for local analysis of extracts. BigQuery only if the org is already there.

---

## 7. Reproducibility & lineage

Brief requirement: **every score traceable to (variant, evaluator version, data).**
Recommendation: make that identity **content-addressed**, not label-based.

```
score_id = H(
    variant_id,
    generation_id,          # content hash of the judged generation
    evaluator_id = H(       # content-addressed "evaluator version"
        rubric_prompt_bytes,    # the BYTES, not a version string
        judge_model_id,         # claude-haiku-4-5
        judge_params,           # effort, thinking, output schema
        scoring_code_git_sha,   # parse/aggregate logic
    ),
    sampling_stratum_id,
    inclusion_prob,         # π_i — see §3
)
```

Two non-obvious rules, both earned from the sources:

1. **Hash the rubric bytes, not a version label.** Human-assigned versions drift from
   reality (someone edits the prompt without bumping the label). Content-addressing makes
   that impossible. From `redharness`: *"content-addressed datasets (hash-pinned) verified
   before use... attempts cached on their fully resolved parameters."*
2. **`inclusion_prob` is lineage, not telemetry** (§3).

**The four-part tuple that recurs across every lineage source is model + prompt + dataset
+ evaluation logic.** Our brief's triple is missing **evaluation logic** as a distinct
axis — worth separating, because the rubric prompt and the scoring/parsing code drift
independently.

### API-side lineage primitives (Anthropic)

- **`response._request_id`** — join key to provider-side traces. Log it.
- **`response.model`** — ⚠️ **the model that *actually* served the request.** With
  server-side fallbacks or sticky routing, a request nominally to model A can be served by
  model B. **A lineage record that logs the *requested* model is wrong.** Log
  `response.model`.
- **`response.usage`** (+ `usage.iterations`) — per-attempt token accounting.
- **`response.stop_reason`** — ⚠️ **a judge harness MUST branch on `refusal` and
  `max_tokens` before parsing a score, or it will silently record garbage.** A refused
  judge call is not a score of zero; it is a missing observation, and conflating the two
  poisons the metric.
- **Structured outputs** (`output_config.format`) guarantee parseable JSON. Note the
  schema is itself a versioned artifact (24-hour compile cache), and its presence
  **disallows** the `max_tokens: 0` cache pre-warm trick.

### The judge-drift problem — the thing most teams miss

`redharness`'s **judge-sensitivity study** is the idea to steal. In continuous monitoring
a "regression" has **three** possible causes:

1. the variant actually got worse;
2. **the traffic mix shifted** (a harder character got popular) — *composition drift*, not
   quality drift;
3. **the evaluator changed** (rubric edit, judge model updated provider-side).

**A monitoring system that cannot distinguish these three will generate confident, wrong
alerts.** Mitigations, each mapping to one cause:

- **(3)** Pin the judge model to an exact ID; content-address the evaluator; treat a judge
  change as a release requiring back-comparison.
- **(3)** Keep a **frozen golden set**, re-scored on every evaluator bump. If golden-set
  scores move, the *evaluator* moved — and any production delta in that window is
  confounded. This is our evaluator-drift alarm.
- **(2)** **Report sliced by default** — this is the same stratification from §3 pulling
  double duty. Composition shift is invisible in an aggregate and obvious per-slice.
- Retro-scoring: because full traces are cheap to retain (§6), we can **re-score history
  under a new evaluator** and get a clean A/B of evaluator versions on identical data.
  This is the payoff for not sampling storage.

---

## 8. Open questions / risks for the lead

1. **Session vs generation sampling unit.** §2 argues sessions. This changes the cost model
   (judge calls ≠ generations) and interacts with the 2K-token latency cliff. **Needs a
   decision before the schema is fixed** — it's expensive to change later.
2. **Abstention rate is unknown for our task.** The 42–63% coverage figure is from pairwise
   preference on 2024-era models. If our Haiku tier abstains at 40%, the §3 floors must
   inflate ~1.7x. **Measure this first** — it's the biggest unknown in the cost model.
3. **Zipf parameter for character traffic is assumed.** The §3 tables use illustrative
   shares (20% head / 0.01% deep tail). **Pull the real distribution before fixing floors** —
   if the tail is thinner than assumed, the floor is cheaper; if fatter, more expensive.
4. **N variants = 5 is assumed.** Cells scale linearly: at 20 variants, 3,800 cells and the
   500/cell floor becomes 1.9M judged/day (~$2,800/day). Still fine, but the "same as
   uniform 1%" symmetry breaks. **Variant count is the main cost driver in this design.**
5. **Judge TPM competes with production traffic.** Judge and prod draw on the same org
   rate-limit pool unless separated. At 500k judge calls/day this is real capacity
   planning — **recommend a separate workspace/key** so a judge backlog cannot throttle
   production.
6. **Batch API's 24h SLA vs regression detection speed.** Batch (50% off) is what makes
   Tier 2 cheap, but "most batches complete within 1 hour; maximum 24 hours." With §3's
   2.1-day detection latency, a 1h batch delay is noise — **but a 24h worst case doubles
   time-to-detect.** Consider live (2x cost, still only $1,475/day) for a small
   fast-feedback slice of the most-trafficked variants, and batch the rest.
7. **The "don't sample at all" thesis deserves a fair hearing — I checked, and it loses.**
   Two vendors market against sampling: **Galileo** ("100% traffic monitoring economically
   feasible"; claims 100M+ sessions, 100B+ tokens/month, $30M+ annual savings, 80x cost /
   20x latency reduction) and **Confident AI** ("Run eval metrics on 100% of traces — no
   sampling", enabled by **$1/GB ingestion pricing** tiering to $0.45/GB — which shifts the
   cost lever from trace *count* to trace *payload*). Their shared thesis: **sampling is a
   tax for using the wrong evaluator.** Run the numbers at our judge shape (6,200 tok/call
   × 50M = **310B tokens/day**):

   | Approach | Cost/yr |
   |---|---|
   | 100% @ Luna-2 list ($0.12/M) | **$13.6M** |
   | 100% @ Luna-2 docs price ($0.02/M) | **$2.3M** |
   | Self-hosted SLM (~35 concurrent H100 streams at 2,315/sec peak) | ~$0.6M + eng |
   | **Our tiered design** | **$0.28M** |

   Even the most favorable framing is **~2–8x our tiered cost**, and self-hosting adds a
   GPU fleet to operate. **Recommendation: keep tiering.** But the thesis is *directionally*
   right about one thing we've already adopted — **Tier 1 cheap signals are exactly the
   "100% coverage with the right evaluator" idea**, just with classifiers instead of an
   SLM. If we later want a 100% *semantic* signal, a self-hosted SLM at Tier 1.5 is the
   credible path, and the sizing above (~35 streams) says it's not absurd.
8. **Tokenizers differ across tiers.** Haiku 4.5 and Opus 4.8 do **not** share a tokenizer;
   Sonnet 5 counts ~30% more tokens than Sonnet 4.6 for the same text. **Cost models must
   count per model** via `count_tokens`. And **never use `tiktoken`** — it undercounts
   Claude tokens by 15–20% on English and worse on non-English, which would corrupt our
   per-language cost slice specifically.
