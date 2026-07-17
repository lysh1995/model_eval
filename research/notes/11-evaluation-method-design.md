# How we evaluate: which fields, how to grade, how to normalize

Status: **proposal for review, with corrections.** Grounded in notes 00–22.

⚠️ **Superseded in part.** [ABILITY-MODEL.md](../../docs/ABILITY-MODEL.md) now carries the positive
construct (L1→L2→L3) this note lacked; [BENCHMARKS §0.5](../../docs/BENCHMARKS.md) records that a
defect-only catalogue *no-ships the most interesting model* (RPGBench). Item 9 below (position bias)
is **withdrawn**. The organizing principle survives; the claim that it is *sufficient* does not.

---

## The organizing principle

> Human raters agree on roleplay *quality* at Krippendorff α = 0.25–0.34
> ([01](01-roleplay-benchmarks.md)). LLM judges scoring creativity *absolutely* hit r = 0.159 vs
> humans, 40% run-to-run consistency ([03](03-creativity-measurement.md)).

Those two numbers are the whole design constraint. **"Is this good?" has no stable answer — not
from our judge, and not from humans either.** So we don't ask it. MiniMax reached the same
conclusion and pivoted: *misalignment is surprisingly objective*.

The method is therefore: **decompose every soft dimension until the objective part falls out, and
only send the irreducible residue to a judge.** "Creativity" isn't one thing — it's novelty
(population-relative, computable), non-slop (computable), constraint satisfaction (computable),
and charm (irreducible → judge, pairwise only). Three of four need no model call.

Each lane is chosen by one question: **can the failure be defined as a deviation from a fixed
spec?** If yes → deterministic. If it needs a preference → judge, and pay the reliability tax.

---

## The four lanes

| | lane | mechanism | coverage | latency | cost @50M/day | reliability |
|---|---|---|---|---|---|---|
| **0** | Safety gate | regex + classifier | **100%, blocking** | 5–50ms | ~$0 | high (bounded task) |
| **1** | Spec compliance | pure computation | **100%, async** | ~1ms | ~$0 | **exact** (σ from generation only) |
| **2** | Corpus statistics | computation over k samples | 100%, batch | n/a | ~$0 | exact, but needs k≥10/cell |
| **3** | Judge | pairwise LLM panel | **~1% stratified** | 1–3s | ~$738/day | **κ≈0.53 ceiling** |

Lane 0 is 100%-or-nothing: guardrails have no sampling rate. Lanes 1–2 are free, so **sample only
for judge cost, never for storage** ([06](06-production-scale-monitoring.md): 579 rows/sec vs
2.1M/sec single-node capacity = 3,600× headroom).

---

## Lane 1 — Spec compliance (deterministic, free, 100%)

These are **violation rates**: countable events with a real denominator. Bounded [0,1], no
calibration needed, comparable across models *by construction*. This is where the platform's
credibility lives.

| field | definition | status |
|---|---|---|
| **Repetition / looping** | fraction of n-grams recurring from earlier ai turns in the same dialogue | ✅ **validated** — separates models at 10–13× MDE ([10](10-noise-floor.md)) |
| **Length-cap adherence** | violations of the variant's own instruction ("under 150 words") | ✅ trivial, and it's *the variant's own spec* |
| **Format discipline** | meta-commentary, stage-direction malformation, prologue break | ✅ regex |
| **Assistant-voice leak** | "as an AI", "language model" | ⚠️ **tripwire only** — base rate ≤3.2/1000 turns, too rare to score ([09](09-offline-probes.md)) |
| **Constraint satisfaction** | explicit constraints in the character card, honored? report as a **slope across tightness tiers** | 🔨 to build — CS4-style; bounded, judge-free, "the most defensible single number" ([03](03-creativity-measurement.md)) |

**Why the slope, not the level:** a derivative is far more robust than an absolute. It measures
headroom, not charm — necessary, not sufficient.

## Lane 2 — Corpus statistics (deterministic, needs k samples per cell)

Measurable **only across responses**, never within one. Skipping this tier is the most common
mistake and it hides the failure users complain about most.

| field | definition | status |
|---|---|---|
| **Voice homogenization** | mean cross-character n-gram profile similarity, within model | ⚠️ **length-controlled version only** — naive version was ρ=+0.73 with length ([09](09-offline-probes.md)) |
| **Slop rate** | frequency of overused tropes vs a frozen reference list | 🔨 to build — **judge-independent cross-check**; EQ-Bench's authors built one because they didn't trust their own judge |
| **Lexical diversity** | distinct-n / entropy, **at equal token budget** | 🔨 length control mandatory |

**The slop metric is structural, not decorative.** Judges favor fluent-but-generic text, and that
bias is *correlated with the construct* — so more judging buys a more precise wrong answer.
Decision rule: **if judge-creativity ↑ while slop ↑, trust the slop metric.**

## Lane 3 — Judge (pairwise only, ~1%, expensive)

Only what genuinely cannot be specced. Every one of these is **pairwise against a frozen anchor
set** — never an absolute score.

| field | why it's irreducible |
|---|---|
| **Character fidelity: voice/style** | the most-reproduced 3-way split in the literature ([01](01-roleplay-benchmarks.md)) — do **not** collapse it |
| **Character fidelity: knowledge** | ground on the *provided description*, **not world knowledge** — our characters are user-authored, so the anonymized setting **is** production |
| **Character fidelity: boundary discipline** | would the character refuse/deflect *in fiction*? |
| **Creativity (residual "charm")** | after novelty/slop/constraint are subtracted |
| **Narrative engagement** | does the scene advance? |
| **Emotional attunement** | ⚠️ **highest-risk field** — see sentiment bias below |

---

## How to grade — the judge protocol

Non-negotiables, each traceable to a measured number:

1. **Pairwise, never absolute.** Absolute creativity judging: r=0.159, 40% consistency. Pairwise:
   73–78% human agreement. **The format is the variable, not the model.** Amabile's CAT confirms
   from human psychometrics: experts only achieve reliability rating *relatively within a set*.
   If experts can't score creativity absolutely, our judge can't.
2. **Format: score-based comparison, not Likert.** 92.75% vs 61.50% — a **31pp** swing on format
   alone ([02](02-llm-judge-reliability.md)). Never pick "rate 1–10" by taste.
3. **Frozen anchor set.** Each candidate is compared against fixed reference responses, not against
   every other variant → **O(n) not O(n²)**, and comparability holds as variants come and go.
4. **Reference-anchor every judgment** (character card + human-authored exemplar). Most
   consistently validated mitigation in the corpus: MT-Bench math failure 70%→15%.
5. **Family-disjoint panel of 3.** Kendall τ 0.778 vs 0.667 for single GPT-4, at **7–8× lower
   cost**, 2.8× more stable. Strict dominance — there is no tradeoff to weigh. Family-disjoint
   because self-preference is causal and **does not cancel by averaging**.
6. **Abstention from day one.** ~19% of items are irreducibly contested; the >80% guarantee in the
   literature is *achieved by* abstaining on ~20%. Abstentions route to humans → a free
   calibration set on exactly the hard cases.
7. **Report Cohen's κ, never percent agreement.** The famous "80% agreement" is raw, ties-excluded,
   base-rate-inflated. Chance-corrected ceiling is **κ≈0.53**.
8. **Judge version = `(model_snapshot, prompt_hash, rubric_ver, decoding, seed)`** — never a
   floating alias. GPT-4 went 84%→51.4% on one task in three months. A judge bump is a **breaking
   change** requiring re-baseline. This is the brief's traceability requirement, made concrete.
9. **Position bias: CONTESTED — do not skip the swap on my earlier advice.** I wrote that position
   bias is ~solved on frontier judges (≤0.04 in 2026 data vs 35% in 2023) and that swapping
   *worsens* verbosity bias. **A 541k-judgment study finds >0.10 in production judges**
   ([20](20-recent-developments.md)) — an order of magnitude above the number I relied on, and
   measured at production scale rather than in a benchmark. **The "skip the 2× spend" conclusion is
   withdrawn.** Measure our own judge before choosing; the default should now be *swap* until we
   have our own number.

### The unfixable one

**Sentiment bias: RR 0.60–0.80 across all judges, degrading to 0.24–0.66 under sadness, anger,
fear. No published mitigation.** A companion product is *made of* emotional conversation — our
judge is least reliable exactly where our traffic lives. This is not solvable at our altitude.
Response: measure our own exposure, publish it as a known instrument limitation, weight
`emotional attunement` accordingly, and **never let it gate a ship alone**.

---

## How to normalize

"Normalize" means five different things here. Conflating them is the trap.

### 1. Across models → Bradley-Terry latent scale
Pairwise outcomes vs frozen anchors → BT fit → latent score. **This is the answer to "same
baseline for each model."** Comparability by construction; no absolute calibration to drift.

### 2. Length → style covariates in the BT model
**Not** a post-hoc divide-by-length. Fit length as a covariate: coefficient **0.249, ~8× any
formatting term**; under style control **Grok-2-mini moved 12 ranks**. We compare *system-prompt
variants*, so "be thorough and detailed" is a one-line leaderboard exploit findable in week one.
Corroborated locally: our corpus spans **40 → 3,783 chars/turn (95×)**, and my first
homogenization metric was ρ=+0.73 with length before control. **Unmitigated, we ship a verbosity
meter.**

### 3. Across languages → **do not normalize. Refuse.**
`Spearman(en rank, zh rank) = −0.082` on homogenization ([09](09-offline-probes.md)); grok-4.1
swings 1.4%→29.6% on repetition. Measurement invariance does not hold — a Chinese "4" is not an
English "4", a property of the **scale**, not the content, so better translation cannot fix it.
**Language sits above the aggregation line.** The platform should *refuse* to emit a pooled
cross-language number, as it would refuse to add a temperature to a length. If a single number is
ever forced, it requires a permanent versioned **anchoring-vignette set** rated by every judge in
every language every run — that is the only mechanism that makes "same baseline" true across
languages rather than aspirational.

### 4. Across characters → shrinkage, not division
At n=3 runs, a single (model, character) cell resolves only a **19.4pp** difference; 2pp would
need **281 runs** ([10](10-noise-floor.md)). Raw per-cell scores are **noise amplifiers** that
will manufacture a story about some character every release. Partial pooling shrinks each cell
toward the model mean by its own noise. **Never display a raw per-cell score** — a shrunk
estimate with its interval, or nothing.

### 5. Across judge versions → re-baseline, don't rescale
Pin the version; on a bump, dual-run the frozen calibration set and re-baseline. Never silently
rescale old scores onto a new judge.

---

### 6. Across turns → **min, not mean**

MT-Bench-101 measured this directly: scoring a conversation by **min-over-turns beats
mean-over-turns by 12 points of human agreement (87% vs 75%)**, and min-aggregation of a GPT-4
judge *exceeds human experts' own internal agreement*. Rationale: "a single failed response can
compromise the entire dialogue." Averaging is not a neutral summary here — it **launders the one
catastrophic turn** that actually ends the session. Report min (or a low percentile) plus
**turn-index-of-first-failure**, which turns a score into a debuggable location.

### 7. Effective sample size → characters, not turns

**The conversation is the sampling unit; the turn is a repeated measure.** Turns within a dialogue
are autocorrelated — **42% of turn-level findings may be spurious** from ignoring this. Our
effective n is **~95 characters, not 313,500 turns**. Requires mixed-effects with random
intercepts per character and cluster-robust SEs — the *same* model already required by §4
shrinkage and the G-study.

**The UI must never display turn-pooled n as sample size.** "n = 313,500" is a 60× overstatement
of the evidence and is the single most likely way this platform lies to someone.

**Per-response scoring isn't just noisy — it is directionally wrong.** FED measured the same
systems at both levels: at turn level **Meena (4.19) beats Human (3.85)**; at dialogue level the
ranking **flips** — **Human (4.60) > Meena (4.11)**. A per-response metric ranked a bot above a
human, and the error was not noise but sign. This retires the "per-response is a cheap
approximation" argument entirely: it is a *different and wrong* measurement, and it fails on
exactly the comparison an eval exists to make.

### 8. Dialogue length → long, or it cannot rank at all

BotChat: at **N=4 turns models are indistinguishable (1.5% spread)**; at **N=16 they separate
sharply**. Short dialogues don't merely lose power — they lose *discrimination*. Our corpus is
**102 turns**, which is an asset, not an inconvenience, and the benchmark must not be trimmed to
short exchanges for cost reasons. If judging cost forces a cut, cut the *sampling rate*, never
the *dialogue length*.

### 9. Depth is a proxy — the real variable is distance to relevant content

MT-Eval isolates the mechanism: six distractor turns at the **front** of a conversation cost
nothing; the **same six** placed between the relevant document and the query cost **−1.13**. So
"quality degrades with turn depth" is a confounded shorthand. **The causal variable is distance
from the character card to the current turn** — which is exactly what Character.AI's 1024-token
sliding window does to a persona definition
([05](05-companion-products-practice.md)), and it mechanically explains the #1 user complaint.

Consequence: don't model drift as `f(turn_index)`. Model it as `f(distance-to-anchor)`, and make
**re-anchoring frequency** a first-class variant parameter — it is likely a bigger quality lever
than model choice, and it is one we control.

---

## The grid is not optional: fidelity and diversity are anti-correlated

**Per-character fidelity and cross-character diversity trade off against each other.** Models at
ρ>0.9 persona fidelity produce Cohen's d up to **15.7** between persona groups (human "very
large" ≈ 0.8–2). **A model can win every per-character evaluation and be the worst model in the
cohort** — perfectly consistent, and consistently the same voice.

This is why Lane 2 exists and why the 95-character grid can't be trimmed to a convenience sample:
the failure is **mathematically undefined for a single character**. It is only visible across the
cohort. Any eval that scores characters one at a time is structurally blind to it.

## The gate: no dimension ships without its noise floor

Every dimension declares, **before** it can gate anything:

- σ_within (run-to-run) — for judge lanes this includes judge stochasticity **on top of**
  generation stochasticity, so expect worse than the 0.0847 we measured for repetition
- its **minimum detectable effect** at the planned sample size
- its **registered confound tests** (length at minimum) with measured residuals
- for judge dimensions: **κ vs a human calibration set**, and its **abstention rate**

Rationale is empirical, not procedural: I implemented a literature-recommended metric in the
obvious way and shipped two invisible confounds in a row (length → then survivorship). The
output looked *entirely plausible* both times. **Plausibility is not validation, and this system's
failure mode is confident, well-formatted, wrong numbers.**

## Open questions for review

1. **Is `emotional attunement` worth having**, given sentiment bias has no mitigation and sits on
   our core traffic? Defensible either way; needs an explicit decision, not a default.
2. **Benchmark is underpowered**: 45–50 characters resolves ~2pp; a 1pp regression needs ~194.
   Add runs (cheap) or characters (authoring cost)?
3. **Who owns consequential validity** — for each dimension, name the model that would win by
   gaming it. For a companion product, **"engagement" gamed = emotional dependency**. We'd be
   building a sycophancy optimizer and calling it quality.
4. **Governance**: the OpenAI April 2025 rollback happened *because* A/B tests approved the
   sycophantic model; only expert testers dissented, and were overruled. **A qualitative signal
   must be able to block a ship when everything quantitative is green** — or we rebuild that
   incident with better dashboards.
