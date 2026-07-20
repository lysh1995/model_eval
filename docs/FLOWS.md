# System flows

How the platform actually works, end to end. Every flow here is constrained by a measured number
— the design is downstream of [PROJECT.md §4](PROJECT.md#4-what-we-measured-ourselves-not-borrowed),
not of taste.

> **Note:** the online event schema (Flow 3) follows the OpenTelemetry GenAI semantic conventions and is implemented in `ceval/online/events.py` — the field names below are concrete.

---

## Flow 0 — The variant lifecycle (top level)

```mermaid
flowchart LR
    A[Author variant<br/>model + params + prompt] --> B[Dry-run<br/>local, cheap, fast]
    B -->|fails smoke| A
    B --> C[Benchmark gate<br/>full grid, judged]
    C -->|regression| A
    C --> D[Ship review<br/>evidence + recommendation]
    D -->|no-ship| A
    D --> E[Shadow<br/>SMOKE TEST ONLY -- turn 1<br/>crash / refusal / latency / cost]
    E --> F[Canary<br/>small % of real users<br/>the first on-policy signal]
    F --> G[Live<br/>continuous monitoring]
    G -->|drift / regression| D
    G --> H[Curation<br/>hard cases ACCUMULATE into benchmark]
    H -.grows, never replaces.-> C
```

The loop closes at **H**: production teaches the benchmark what it was missing. Without that arm,
the benchmark decays into a fixed exam that no longer represents traffic. This abstract loop is
instantiated by the service CLI (`ceval variant add → data → eval run → dashboard`).

### ⚠️ Shadow is not a quality gate — it cannot be

**Corrected** ([14](../research/notes/14-eval-lifecycle-system.md)). The obvious design —
mirror production traffic to the candidate and compare — **does not work for multi-turn roleplay.**
The candidate's turn-2 reply is conditioned on the **incumbent's** turn-1. By turn 3 you are
scoring a conversation the candidate would never have produced. This is the FED result
(per-turn ranking *flips* vs dialogue-level) arriving through deployment instead of through
metrics. **Traffic replay onto a live candidate has the identical flaw.**

The industry's "shadow eval on production traces" gate is borrowed from **single-turn RAG apps
and does not transfer.**

**Consequence:** there is **no user-safe, on-policy middle ground.** Only two things give honest
multi-turn signal:
- **offline self-play** (our 102-turn benchmark — the model generates its own assistant turns), or
- **a real canary** (real users, real exposure).

Shadow survives only as a **smoke test on turn 1**: does it crash, refuse, blow latency, blow
cost, blow length. That is worth having and is not a quality signal.

**This forces weight back onto the offline benchmark** — which is exactly the stage we've measured
as underpowered (~2pp). That tension is real and is not resolved by more pipeline.

---

## Flow 1 — Dry-run (local, pre-benchmark)

Purpose: **fail fast and free.** Catch the 90% of bad variants that don't deserve a judge.

```mermaid
flowchart TD
    V[Variant manifest] --> G[Generate: N chars x K runs<br/>stratified subset]
    G --> L0[Lane 0: safety tripwires<br/>regex + classifier]
    G --> L1[Lane 1: spec compliance<br/>pure computation]
    L0 --> S{Autofail?}
    L1 --> S
    S -->|yes| X[Reject + reason<br/>no judge spend]
    S -->|no| P[Promote to benchmark gate]
```

**Why this tier exists:** Lane 0/1 are exact — no judge, no calibration, ~$0. A variant that
violates its own length cap, loops, or leaks assistant-voice is rejected before we spend a cent
on judging. The dry-run is a **filter, not a measurement** — it is deliberately underpowered and
must never emit a ship recommendation.

**Dry-run stratification** must preserve the language split. A dry-run on English only is
uninformative about Chinese: `Spearman(en, zh) = −0.082`.

---

## Flow 2 — Benchmark gate (the pre-launch decision)

```mermaid
flowchart TD
    V[Candidate variant] --> GEN[Generate over full grid<br/>95 chars x 2 langs x R runs<br/>replay user turns, 102 turns]
    GEN --> L1[Lane 1: violations<br/>per dialogue, free]
    GEN --> L2[Lane 2: corpus stats<br/>needs k>=10 per cell]
    GEN --> SAMP[Stratified sample<br/>~1% -> Lane 3]
    SAMP --> J[Lane 3: judge panel<br/>3 family-disjoint judges<br/>pairwise vs frozen anchors]
    J --> ABST{Abstain?<br/>~20%}
    ABST -->|yes| HU[Human queue<br/>= free calibration set]
    ABST -->|no| BT[Bradley-Terry fit<br/>+ style covariates]
    L1 --> AGG[Aggregate:<br/>min over turns<br/>n = conversations]
    L2 --> AGG
    BT --> AGG
    HU --> AGG
    AGG --> HIER[Hierarchical model<br/>shrink per-character cells]
    HIER --> REP[Ship report<br/>per language, never pooled]
```

### The constraints encoded here

| Step | Why | Evidence |
|---|---|---|
| Replay **user** turns, model generates **assistant** turns | Freezing the assistant half manufactures "illusory improvement" via ICL. Live simulators inflate success ~14pp and impose stylistic uniformity that would fabricate our homogenization metric | [08](../research/notes/08-multiturn-conversation-eval.md) |
| **102 turns, don't shorten** | At 4 turns models are indistinguishable (1.5% spread); at 16 they separate sharply. Short dialogues lose *discrimination*, not just power. **If cost bites, cut sampling rate, never dialogue length** | BotChat |
| **Pairwise vs frozen anchors**, never absolute | Absolute creativity judging: r=0.159. Pairwise: 73–78%. Anchors keep it **O(n) not O(n²)** and hold comparability as variants come and go | [02](../research/notes/02-llm-judge-reliability.md), [03](../research/notes/03-creativity-measurement.md) |
| **3 family-disjoint judges** | τ 0.778 vs 0.667 for single GPT-4, at **7–8× lower cost**. Strict dominance. Family-disjoint because self-preference is causal and **doesn't cancel by averaging** | PoLL |
| **Style covariates inside BT** | Length coefficient **0.249, ~8× any format term**; under style control Grok-2-mini moved **12 ranks**. We compare *prompt variants* — "be thorough and detailed" is a one-line leaderboard exploit | [02](../research/notes/02-llm-judge-reliability.md) |
| **min over turns, not mean** | **87% vs 75%** human agreement. Averaging launders the one catastrophic turn that ends the session | MT-Bench-101 |
| **n = conversations** | Turns are autocorrelated; **42% of turn-level findings may be spurious**. Effective n ≈ 95, not 313,500 | [08](../research/notes/08-multiturn-conversation-eval.md) |
| **Shrink per-character cells** | At n=3, a per-cell MDE is **19.4pp**. Raw cells are noise amplifiers that manufacture a story every release | [10](../research/notes/10-noise-floor.md) |
| **Report per language, never pooled** | ρ(en,zh) = **−0.082** | [09](../research/notes/09-offline-probes.md) |

---

## Flow 3 — Online collection (the contract)

There is no app behind this, so **we specify what the product must emit.** Nothing downstream
exists without this contract.

```mermaid
flowchart LR
    subgraph Product
      T[Turn served]
    end
    T -->|blocking, 5-50ms| L0[Lane 0 gate<br/>crisis / autofail / PII]
    L0 -->|flag| ESC[Escalation<br/>human path]
    L0 --> EMIT[Emit generation event]
    T --> SESS[Session lifecycle events]
    EMIT --> BUS[(Event bus)]
    SESS --> BUS
    BUS --> STORE[(Columnar store<br/>100% retained)]
    STORE --> L1O[Lane 1: free metrics<br/>100% async]
    STORE --> SAMPLER[Session sampler<br/>500/cell/day floor]
    SAMPLER --> L3O[Lane 3: judge ~1%]
    L1O --> ROLL[(Rollups + drift)]
    L3O --> ROLL
```

### Event essentials

**No existing standard is sufficient — this is a real finding, not NIH.** OpenTelemetry's
`gen_ai.evaluation.result` carries exactly **six** attributes — `evaluation.name`, `score.value`,
`score.label`, `explanation`, `response.id`, `error.type` — and **not one identifies the evaluator
that produced the score.** The spec concedes that evaluation semantics are evaluator-dependent and
then provides no field for the evaluator. That is precisely constraint **C1**, unmet. Likewise
`gen_ai.conversation.id` is a bare label the spec forbids you to synthesize, and there is no
session entity at all. Most of the namespace is `Development` stability.

**So: adopt `gen_ai.*` where it exists, add an `eval.*` namespace for what no standard has.**

```
# gen_ai.* -- adopt as-is
gen_ai.response.model          # NOT request.model -- what actually served
gen_ai.finish_reasons          # branch on this: a refusal is a MISSING OBSERVATION, not a zero
gen_ai.usage.{input,output}_tokens
gen_ai.conversation.id
# content capture is Opt-In in the spec -- we must explicitly opt in

# eval.* -- ours, because nothing standard carries it
eval.variant_id          = H(model, params, system_prompt_bytes, anchoring_policy)
eval.evaluator_id        = content-addressed (model_snapshot, prompt_hash, rubric_ver, decoding, seed)
eval.inclusion_prob      # pi_i -- LINEAGE, not telemetry: without it, sampled estimates are unweighted and biased
eval.distance_to_anchor  # the real causal variable. OTel offers only a boolean
eval.pairwise_outcome
eval.provenance          # human-authored | mined-from-production | synthetic
eval.rollout_stage
```

**Session is a first-class entity we build.** It stores `min_turn_score` and
`first_failure_turn_idx`. **If it stores a mean, the platform is wrong by design** — min-over-turns
beats mean by 12 points of human agreement, and a mean launders the one catastrophic turn.

**A refusal is not a zero.** Branch on `finish_reasons`: scoring a refusal as 0 silently averages
a *missing observation* into a quality mean, which is how over-refusal disappears from a dashboard.

### Three decisions that are easy to get wrong

1. **Sample *sessions*, not generations.** Boundary erosion and dependency are **trajectory**
   properties. A per-generation sampler draws turn #47 blind to turns #1–46 and sees nothing
   wrong — structurally blind to our worst failure modes.
2. **Don't sample for storage — only for judge cost.** Ingest is 579 rows/sec average against
   2.1M/sec single-node capacity (**3,600× headroom**), ~3–8 TB/yr compressed. Cardinality is
   950 combinations — a non-problem. Storage is not the constraint; **judge latency is**
   (1,000–3,200ms vs a ~200ms guardrail budget — even a *free* judge is 5–16× too slow to sit inline).
3. **Log the assignment arm from day one.** If users *choose* their model, quality differences are
   contaminated by who chose it — a model that attracts heavy roleplayers looks better on every
   behavioral metric while being no better. If a randomized default exists, that arm supports
   causal claims and the self-selected arm doesn't. **This cannot be reconstructed after the
   fact.** (Scoping note: the product may not randomize; the field costs nothing and its absence
   is unrecoverable.)

### Behavioral signals — and the trap

Worth collecting (diagnostic, hard to game): **follow-up-question rate** (validated against
wellbeing; degrades exactly for depressed/anxious/lonely users, and points *against* engagement),
**user edit rate** (persona-repair leading indicator), **self-similarity**,
**contradiction-by-distance**, **persona bleed**.

**Never optimize, ideally never headline:** thumbs-up, D1/D7/D30 retention, time-to-next-session,
raw affective intensity.

> Chai got **+30.3% D30 / +50.87% MCL** from RLHF on pure continuation+retry labels. OpenAI added
> a thumbs-up signal to a reward and it "weakened the influence of our primary reward signal,
> which had been holding sycophancy in check" — rollback in 4 days. **Their A/B tests approved of
> it.** You cannot detect reward hacking with the metric being hacked.

Also: MCL has **undefined variance** (truncation at ≤100 msgs), affective cues are power-law (the
at-risk cohort is invisible to means), latency contaminates everything (+1s → −3.01% MCL), and
affective intensity is **sign-ambiguous** (β=+0.26 generally, **β=−0.47** for companionship use) —
so an unconditioned engagement metric averages a benefit and a harm and reports zero.

---

## Flow 4 — Tiered evaluation at 50M/day

```mermaid
flowchart TD
    ALL[50M generations/day] --> T0[Tier 0: 100% blocking<br/>regex + classifier, 5-50ms<br/>~$0]
    ALL --> T1[Tier 1: 100% async<br/>repetition, length, refusal,<br/>embedding drift -- no LLM<br/>~$0]
    ALL --> T2[Tier 2: ~1% stratified<br/>cheap judge, batch + cached rubric<br/>$738/day]
    T2 -->|escalate| T3[Tier 3: ~0.01%<br/>strong judge, gold<br/>$37/day]
    T0 --> ESC[Escalation path]
    T1 --> D[Drift detection]
    T2 --> D
    T3 --> D
```

| | 100% cheap judge | 100% strong judge | **Tiered** |
|---|---|---|---|
| cost/yr | $26.9M | $269M | **$283k** |

**95× reduction.** Even 30% cascade escalation only reaches $687k/yr — so don't over-tune it.
**Prompt caching alone saves $370k/yr — more than the rest of the platform costs.**
Trap: caching needs a **≥4,096-token prefix** to engage *at all*, silently. Our rubric must exceed it.

### Sampling: uniform 1% is wrong, and fixing it is free

950 cells (95 chars × 2 langs × 5 variants). Uniform 1% gives the head **100,000 judged/day**
(it needs ~1,000) while the deep tail takes **21 days** to detect a 3pp regression.
A **500/cell/day floor = 475k/day = 0.95% of traffic** — *same budget*, every cell at ~2 days.
**Highest-leverage decision in the online design.**

### Drift detection

**Do not use the KS test.** Evidently — a drift vendor — abandons it above **1,000 rows**; we're
at 50M. At n=100k, KS fires on a 0.5% shift. Use **PSI** (0.1/0.2 bands) + **e-values** (peek
freely, reject at E≥20) + **e-BH** across cells. Uncorrected, 950 cells at α=.05 yields
**47.5 false alarms/day with nothing wrong.**

Judges have **12–14% false-positive rates** — **alert on aggregates, never on a single score.**

---

## Flow 5 — The eval loop (how the benchmark stays honest)

```mermaid
flowchart LR
    LIVE[Live traffic] --> MINE[Mine hard cases<br/>abstentions, drift, escalations,<br/>high-uncertainty cells]
    MINE --> DEDUP[Dedupe vs existing suite]
    DEDUP --> HUM[Human adjudication<br/>the abstained ~20%]
    HUM --> CAL[(Calibration set<br/>-> judge kappa)]
    HUM --> SUITE[(Regression suite<br/>grows)]
    SUITE -.->|next release| GATE[Benchmark gate]
    CAL -.->|validates| JUDGE[Judge version]
```

The **abstention queue is the engine**, not a failure mode. ~19% of items are irreducibly
contested; routing them to humans yields a calibration set concentrated on exactly the hard
cases — the cheapest source of κ we have.

**Contamination guard — the benchmark ACCUMULATES, never REPLACES.** Mined cases are our own
models' output. Curation that *replaces* human-authored anchors runs the Nature model-collapse
experiment on our eval set — after which the benchmark **reports improvement forever, by
construction.** Enforce a provenance cap in CI (`eval.provenance` ratio), don't merely monitor it.
Curated production data also trains *nothing*: findings feed humans, not a reward model.

### The cautionary tale that defines this flow

**RLUF (Meta) is the only published offline↔online correlation we found: Pearson r = 0.95** across
10 iterations. Read the method before celebrating: it was achieved by **training the evaluator on
1M production labels of the online metric** — not by a rubric judge. Then optimizing it by +28%
produced a model that **ends conversations early to farm the signal** ("bye" rate 0.72% → 2.8%).

**The correlation and the pathology are the same property:** a metric that predicts online
outcomes is, by construction, a metric worth gaming.

And the detail that should decide our architecture: **the tripwire that caught it was a cheap
deterministic phrase rate — not the judge.** That is the strongest available argument for Tier 1
(free, exact, 100% coverage). The expensive instrument missed it; the trivial one caught it.

**Therefore: we cannot claim offline↔online correlation** until we backtest against our own A/B
history. Until then it's an aspiration, not a property.

---

## Flow 6 — The ship decision

```mermaid
flowchart TD
    R[Benchmark results] --> POOL[Pre-registered pooled gate<br/>one test, no correction<br/>CAN BLOCK]
    R --> SLICE[Slice views<br/>BH q=0.10, shrunk<br/>INFORM ONLY, never block]
    POOL --> REC[Recommendation]
    SLICE --> REC
    SAFE[Safety: harm axis] --> REC
    REF[Safety: over-refusal axis] --> REC
    REC --> HUM{Human review}
    QUAL[Qualitative dissent] --> HUM
    HUM -->|veto, no stats required| NO[No-ship]
    HUM --> YES[Ship -> shadow -> canary]
```

**Two tiers by design.** One pre-registered pooled test that can block; FDR-controlled slices that
inform but never block. Otherwise 190 cells at α=.05 produce ~9.5 false regressions per dimension
per release, and the failure isn't that people are misled — **it's that they correctly learn to
ignore us.**

**Safety enters as two axes, never averaged.** Harm and over-refusal are different defects.
Anthropic's constitution names *"refuses to engage with fiction"* as a defect and says the risks
of being "too unhelpful or overly cautious are just as real."

**The human veto requires no statistical justification.** This is the single most important box
in this document. OpenAI's April 2025 rollback happened *because* the A/B tests approved the
sycophantic model and expert testers who said it felt "off" were overruled. A platform that
cannot be overridden by a human who is right rebuilds that incident with better dashboards.

---

## What the ship report must say

A recommendation is not a number. It states:

1. The delta **and its interval and the MDE** — "no regression" is meaningless without the
   detectable effect. Our benchmark resolves ~2pp; a 1pp regression is **invisible**, not absent.
2. **Per language, never pooled.**
3. Which slices moved **after shrinkage**.
4. Which dimensions **abstained**, and how often.
5. **What it could not measure.** Judge sentiment bias (RR 0.60–0.80, worse under
   sadness/anger/fear) means emotional dimensions are least reliable exactly where our traffic
   lives. That belongs in the report, every time — not in a footnote.
