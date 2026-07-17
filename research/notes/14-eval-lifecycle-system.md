# 14 — The evaluation lifecycle: how the loop closes

Status: **proposal for review.** Synthesis of the 15 `pipeline-*` sources. Assumes
[06](06-production-scale-monitoring.md) (tiering, sampling, drift, lineage) and
[11](11-evaluation-method-design.md) (what we measure and how we grade) are settled. This
note is about the **system around** them: how a variant gets from a laptop to 50M/day and
how production comes back.

---

## 0. The three findings that shape everything below

**1. Shadow deployment does not work for multi-turn companion traffic.** Not "is
expensive" — *does not work*. The candidate's turn-2 reply is conditioned on the
**incumbent's** turn-1 reply. By turn 3 you are scoring a conversation the candidate would
never have produced. This is note 11 §7's FED result (turn-level ranking **flips** vs
dialogue-level) and note 08's exposure-bias/covariate-shift sources, arriving via
deployment. Traffic replay has the identical flaw. **Shadow is a smoke test, not a quality
gate**, and the industry's "shadow eval on production traces" gate
(`pipeline-shadow-canary-rollout.md`, `pipeline-evals-as-ci-landscape.md`) is borrowed from
single-turn RAG apps where it is sound. It doesn't transfer. This forces weight onto the
**offline self-play benchmark**, which is on-policy, and onto the **canary**, which is
on-policy. There is no user-safe on-policy middle.

**2. The one published offline↔online correlation is r=0.95 — and the same experiment
reward-hacked.** RLUF (Meta, `pipeline-rluf-offline-online-correlation.md`): Pearson
**0.95** between offline reward and online outcome across 10 iterations; optimizing it
**+28%** on the target metric produced a model that **ends conversations early to farm the
signal** ("bye" rate 0.72% → 2.8%). The correlation and the pathology are **the same
property**. A metric that predicts online outcomes well is, by construction, a metric worth
gaming. **High offline↔online correlation is not evidence a metric is safe to gate on.**
And the thing that caught it was a **cheap deterministic phrase rate** — not the judge.

**3. No standard carries evaluator identity, and none models a session.**
`gen_ai.evaluation.result` has exactly six attributes and **not one of them says which
judge produced the score** (`pipeline-otel-genai-semconv.md`). `gen_ai.conversation.id` is
an opaque label the spec forbids you to synthesize. Every vendor stores `(name, value)` and
punts versioning to `metadata`. **The parts of the schema that make our design work are the
parts we have to write ourselves.**

---

## 1. The lifecycle

Six stages. Each has an **entry artifact**, a **question**, a **statistic**, and an **exit
rule**. A stage that can't state its exit rule as a number isn't a stage, it's a vibe.

```
  ┌────────────────────────────────────────────────────────────────────────────┐
  │  0. DRY RUN            laptop / branch      minutes    n=1–3 chars         │
  │     "does it run and is it obviously broken?"                              │
  ├────────────────────────────────────────────────────────────────────────────┤
  │  1. BENCHMARK GATE     CI on PR             ~1–3 h     95 chars × 2 lang   │
  │     "is it worse than the incumbent, beyond MDE?"      × 102 turns × n runs│
  │     ── BLOCKING. This is the real gate. ──                                 │
  ├────────────────────────────────────────────────────────────────────────────┤
  │  2. SHADOW             prod traffic, 0.1%   hours      TURN 1 ONLY         │
  │     "does it crash / refuse / blow up cost or length?"  (see §0.1)         │
  │     ── smoke test. NOT a quality gate. ──                                  │
  ├────────────────────────────────────────────────────────────────────────────┤
  │  3. CANARY             1% → 5% → 20% → 50%  hours–days sticky by session   │
  │     "is it SAFE?"  cheap signals, auto-rollback                            │
  ├────────────────────────────────────────────────────────────────────────────┤
  │  4. A/B + LIVE MON.    50/50 → 100%         days–weeks e-values, e-BH      │
  │     "is it BETTER?"  human ship call                                       │
  ├────────────────────────────────────────────────────────────────────────────┤
  │  5. CURATION           continuous           weekly     back to stage 1     │
  │     "does the benchmark still resemble production?"                        │
  └────────────────────────────────────────────────────────────────────────────┘
```

**Canary ≠ A/B, and the distinction is load-bearing** (`pipeline-shadow-canary-rollout.md`):

> *"Canary deployment tells you whether the new model is **safe** to deploy. A/B testing
> tells you whether it's **better**."*

Different questions, statistics, clocks, and exit criteria. Conflating them is how the
OpenAI April 2025 sycophancy rollback happened (note 11 open question #4): **the A/B test
approved the model.** A/B answers "better on the metric" — not "safe", and not "good".

### Stage table

| # | Stage | Question | Statistic | Exit rule | Blocking? |
|---|---|---|---|---|---|
| 0 | Dry run | does it run? | none | no crash, no empty output, format parses | dev-local |
| 1 | **Benchmark gate** | worse than incumbent? | **shrunk BT delta + CI vs declared MDE** | CI excludes −MDE on every gating dim | **YES** |
| 2 | Shadow | operationally sane? | Tier-1 cheap signals, turn-1 only | length/refusal/latency/cost within band | YES (cheap) |
| 3 | Canary | safe? | Tier-1 + Tier-0 rates, per cohort | auto-rollback thresholds hold | **YES, automated** |
| 4 | A/B | better? | e-values, e-BH across cells | human decision + qual sign-off | human |
| 5 | Curation | benchmark still valid? | **PSI(benchmark ‖ production)** | PSI < 0.2 on all keyed features | advisory |

### Why stage 1 carries the weight

Given §0.1, our **102-turn self-play benchmark is the only on-policy multi-turn evidence we
can get without exposing users.** Note 11 §8 (BotChat: at N=4 turns models are
indistinguishable at 1.5% spread; at N=16 they separate sharply) says that benchmark must
stay long. So: **cut the sampling rate, never the dialogue length** — and never substitute
shadow for it.

---

## 2. The event schema

Five event types. **Three are 100%-coverage, two are sampled.** Storage is not the
constraint (note 06 §6: 3–8 TB/yr full fidelity, 3,600× ingest headroom) — **sample only
for judge cost, never for storage.**

### 2.0 The identity keys — compute these first, everything hangs off them

```python
# ── VARIANT: the thing under test. (model + params + system prompt) as ONE id.
variant_id = H(
    model_snapshot,            # "claude-haiku-4-5-20260101" — NEVER a floating alias
    decoding_params,           # temp, top_p, top_k, max_tokens, stop, seed
    system_prompt_bytes,       # THE BYTES. not a label. not a version string.
    anchoring_policy,          # re-anchor every N turns / window size  (note 11 §9)
    scaffold_git_sha,          # our prompt-assembly code
)

# ── EVALUATOR: content-addressed. (note 06 §7, extended with env)
evaluator_id = H(
    rubric_prompt_bytes,       # the BYTES
    judge_model_snapshot,      # exact id
    judge_params,              # effort, thinking, output schema
    scoring_code_git_sha,      # parse + aggregate logic
    package_lock_hash,         # ← ADDED: Inspect logs `packages`; note 06 omitted it.
                               #   our tokenizer/regex deps drift under us.
)

# ── BENCHMARK RUN: the dvc.lock idea — pin RESOLVED inputs, not a label.
run_manifest_id = H(
    variant_id,
    character_card_hashes,     # all 95, individually
    anchor_set_hash,           # the frozen human-authored anchors (note 11 §3)
    evaluator_id,
    n_runs, seed_base,
    iceberg_snapshot_id,       # dataset commit (we already have Iceberg — see below)
)

# ── SCORE: idempotent by construction.
score_id = H(variant_id, generation_id, evaluator_id, stratum_id, inclusion_prob)
```

**Rules, each earned from a source:**

1. **Hash bytes, never labels.** Four independent tools converged on content-addressing the
   eval's resolved inputs (promptfoo `hashFiles()`, Vercel agent-eval "result reuse for
   matching fingerprints", DVC `dvc.lock`, lakeFS commit-as-source-of-truth). Note 06 §7
   wanted it for lineage; they want it for cache hits. **Same key. Lineage and speed are
   not in tension — build it once.**
2. **The fingerprint makes a score idempotent.** If `run_manifest_id` is unchanged, **do
   not re-run and do not re-score.** Otherwise the same variant gets two different numbers
   from judge stochasticity, someone notices, and the platform loses its credibility in one
   meeting.
3. **Do NOT adopt DVC or lakeFS** (`pipeline-lineage-dvc-lakefs.md`). They version *bytes on
   a filesystem*; we need a hash spanning a file, an API model string, and a JSON blob —
   ten lines of application code. We already have Iceberg (note 06 §6), which has snapshots
   and time-travel natively. **Use Iceberg snapshot IDs as the dataset commit; compute the
   rest ourselves.** Adding a data-versioning product buys a second storage system to
   operate and a hash we can already compute.

### 2.1 `generation` — 100%, one row per AI turn

The OTel-native fields, **using the real attribute names** so we stay on-standard where the
standard exists (`pipeline-otel-genai-semconv.md`):

| our column | OTel attribute | req. level | note |
|---|---|---|---|
| `operation` | `gen_ai.operation.name` | Required | `chat` |
| `provider` | `gen_ai.provider.name` | Required | `anthropic` |
| `conversation_id` | `gen_ai.conversation.id` | Cond. Required | **our session key** |
| `request_model` | `gen_ai.request.model` | Cond. Required | what we asked for |
| `response_model` | `gen_ai.response.model` | Recommended | ⚠️ **what actually served** |
| `response_id` | `gen_ai.response.id` | Recommended | join key to provider |
| `finish_reasons` | `gen_ai.response.finish_reasons` | Recommended | ⚠️ branch on this |
| `temperature`,`top_p`,`top_k`,`max_tokens`,`seed`,`stop_sequences` | `gen_ai.request.*` | Rec./Cond. | the params axis |
| `input_tokens`,`output_tokens` | `gen_ai.usage.*_tokens` | Recommended | |
| `cache_read_tokens`,`cache_creation_tokens` | `gen_ai.usage.cache_{read,creation}.input_tokens` | Recommended | **verify >0 — note 06's 4,096 cache trap** |
| `ttfc` | `gen_ai.response.time_to_first_chunk` | Rec. if streaming | |
| `error_type` | `error.type` | Cond. Required | **Stable** tier |
| `prompt_name` / `prompt_version` | `gen_ai.prompt.{name,version}` | Cond. Required | **set version = our content hash** |
| `compacted` | `gen_ai.conversation.compacted` | Recommended | boolean only — insufficient, see below |
| `input_messages`,`output_messages`,`system_instructions` | `gen_ai.{input,output}.messages`, `gen_ai.system_instructions` | **Opt-In** | **off by default. we must opt in.** |

**Our extensions — the `eval.*` namespace. None of this exists in any standard:**

```
eval.variant_id            # H(...) above — the unit of the whole platform
eval.character_id          # LowCardinality — 95 values
eval.language              # LowCardinality — note 11 §3: ABOVE the aggregation line
eval.turn_index            # int
eval.distance_to_anchor    # ⚠️ int, tokens since character card. THE variable (note 11 §9)
eval.anchor_reanchored     # bool — did this turn re-inject the card?
eval.rollout_stage         # ENUM: dryrun|benchmark|shadow|canary|live
eval.rollout_cohort        # canary bucket
eval.session_hash_bucket   # ⚠️ ONE hash, THREE consumers (§2.6)
eval.provenance            # ENUM: production|synthetic|benchmark  ← model-collapse guard
```

> **`eval.distance_to_anchor` is the highest-value non-standard field we log.** Note 11 §9:
> MT-Eval shows six distractor turns at the *front* of a conversation cost nothing; the
> *same six* between the relevant content and the query cost **−1.13**. So "quality degrades
> with turn depth" is confounded shorthand — **the causal variable is distance from the
> character card to the current turn.** The standard offers only
> `gen_ai.conversation.compacted`, a boolean. A boolean cannot express a dose-response
> curve. Log the integer.

⚠️ **Two traps the standard hands us, both already flagged in note 06 §7 and both confirmed
by the spec text:**
- **`response.model` ≠ `request.model`.** The spec's own note says the provider attribute
  "may differ from the actual upstream provider... a client SDK may be configured against a
  proxy or hosting platform that transparently relays requests to a different provider."
  **A lineage record that logs the requested model is wrong.**
- **`finish_reasons` must be branched on before parsing a score.** A refused or truncated
  judge call is a **missing observation, not a zero**. Conflating them poisons the metric
  and silently guts the per-cell sample sizes in note 06 §3.

### 2.2 `session` — 100%, one row per conversation, mutable-then-closed

**We have to invent this. No standard has it.** OTel's `gen_ai.conversation.id` is a bare
label — no lifecycle, no attributes, no start, no end, and the spec **explicitly forbids
synthesizing one** ("a new UUID, a trace identifier, or a hash of request content SHOULD
NOT be used as a fallback value"). OpenInference's `session.id` is the same. Only Langfuse
(session) and LangSmith (thread) model it at all, and they're products, not standards.

Note 06 §2 already concluded **the session is the sampling unit** and note 11 §7 that **the
conversation is the sampling unit; the turn is a repeated measure** (effective n ≈ **95
characters**, not 313,500 turns; ignoring autocorrelation makes **42% of turn-level
findings spurious**). A schema with no session entity cannot express our sampling design.

```
session_id            # = gen_ai.conversation.id
user_id_hashed
character_id, language, variant_id       # ⚠️ variant is a SESSION property (sticky, §2.6)
started_at, last_turn_at, closed_at, close_reason
turn_count
eval.min_turn_score         # ⚠️ MIN, not mean — note 11 §6: 87% vs 75% human agreement
eval.first_failure_turn_idx # turns a score into a debuggable LOCATION
eval.reanchor_count
eval.session_hash_bucket
eval.inclusion_prob         # π_i — LINEAGE, NOT TELEMETRY (note 06 §3)
eval.stratum_id
```

> **`min_turn_score` + `first_failure_turn_idx` is the whole of note 11 §6 in two columns.**
> MT-Bench-101: min-over-turns beats mean-over-turns by **12 points of human agreement (87%
> vs 75%)**, and min-aggregation of a GPT-4 judge *exceeds human experts' own internal
> agreement*. **Averaging launders the one catastrophic turn that actually ends the
> session.** If the session table stores a mean, the platform is wrong by design and no
> downstream query can fix it.
>
> ⚠️ **This is why the framework choice matters more than it looks.** Reducing N runs and
> M turns to one number with a **pluggable reducer** is a first-class feature in exactly one
> surveyed framework (Inspect's `reductions` / multi-epoch). Everything else assumes
> one-run-per-item and mean-aggregation. **A tool that can't express "min, not mean" can't
> host our design.**

### 2.3 `evaluation` — sampled; extends `gen_ai.evaluation.result`

Start from the standard (all six attributes), then add what it's missing:

```
# ── the standard's six
gen_ai.evaluation.name                # Required.  "repetition" | "voice_fidelity" | ...
gen_ai.evaluation.score.value         # double
gen_ai.evaluation.score.label         # low-cardinality: pass|fail|abstain|a_wins|b_wins|tie
gen_ai.evaluation.explanation         # judge rationale
gen_ai.response.id                    # correlation when span id unavailable
error.type

# ── OUR EXTENSIONS. the standard has NONE of this.
eval.evaluator_id          # ⚠️ content hash. WITHOUT THIS THE EVENT IS MEANINGLESS.
eval.evaluator_kind        # ENUM: regex|classifier|corpus_stat|llm_judge|human
eval.lane                  # 0|1|2|3   (note 11's four lanes)
eval.target_kind           # ENUM: generation|session   ← OTel cannot express `session`
eval.target_id
eval.inclusion_prob        # π_i
eval.stratum_id
eval.anchor_id             # which frozen anchor was this compared against
eval.comparison_result     # ⚠️ pairwise outcome — score.value is a scalar; ours isn't
eval.judge_panel_member    # family-disjoint panel of 3 (note 11 §5)
eval.abstained             # bool — a FIRST-CLASS monitored metric (note 06 §4)
eval.judge_input_tokens    # the judge has a cost and we must monitor it
eval.judge_latency_ms
```

> ### ⚠️ Why `evaluator_id` is non-negotiable
>
> The spec's own note concedes: *"a score value of 1 could mean 'relevant' in one evaluation
> system and 'not relevant' in another, depending on the scoring range and evaluator"* — and
> **then provides no field to record which evaluator it was.** Two `gen_ai.evaluation.result`
> events reading `name=Relevance, value=4.0` from **different judge versions are
> indistinguishable on the wire.**
>
> Note 11 §8: GPT-4 went **84% → 51.4%** on one task in three months. Note 06 §7: a
> "regression" has three causes — the variant got worse, the traffic mix shifted, or **the
> evaluator changed**. A schema that cannot record the evaluator **cannot distinguish cause 3
> from cause 1, ever, even retroactively.** This is the difference between a reproducible
> score and a number.
>
> **`gen_ai.evaluation.result` as shipped is not self-describing.** Emit it for
> interoperability; never rely on it alone.

> ⚠️ **`score.value` is a `double`, and note 11 §1 mandates pairwise-only.** Pairwise
> outcomes don't fit a scalar without a private encoding. We keep `eval.comparison_result`
> + `eval.anchor_id` as the real payload and emit `score.value` as a lossy courtesy for
> OTel consumers. **Anyone reading only the standard fields is reading a degraded view of
> our data** — document this loudly or someone will build a dashboard on it.

> **Also missing from OTel: the judge's own cost and latency.** An evaluation *event* has no
> duration and no token usage, so **you cannot monitor your judge in the OTel model.**
> OpenInference is better here — it has `EVALUATOR` and `GUARDRAIL` **span kinds**, so the
> judge is a span with latency, cost, and errors. **Steal the idea, keep the `gen_ai.*`
> names.** We need judge cost/latency/abstention monitored (note 06 §4: abstention spike
> *is* a regression signal, arguably earlier than the score).

### 2.4 `label` — human, tiny, append-only

```
label_id, target_kind, target_id
annotator_id, annotator_tier        # expert|trained|reviewer
queue_id                            # ⚠️ WHICH QUEUE — see §5. four queues, four π.
inclusion_prob                      # π_i differs PER QUEUE
rubric_id                           # content hash
value, label, rationale
labeled_at
prior_label_id                      # append-only; corrections don't mutate
```

> **`prior_label_id` + append-only** is Inspect's `log_updates` — *"post-eval edits to tags
> and metadata **(with provenance tracking)"*. Inspect assumes the log gets annotated later
> and makes that an **attributed, append-only** operation instead of a mutation. That is
> exactly what our humans do to a production trace, and it is the difference between an
> auditable label history and a spreadsheet.

### 2.5 `curation` — the flywheel's audit trail

```
curation_id
source_trace_id, source_session_id   # ⚠️ THE back-pointer
decision                             # promote|reject|retire
target_set                           # anchor_frozen | rolling_representative
failure_mode                         # our OWN enum — see §5.2
provenance                           # human_authored | mined_from_prod
decided_by, decided_at, rationale
iceberg_snapshot_id                  # which dataset commit this landed in
```

> **`source_trace_id` is settled practice** — Langfuse ships `sourceTraceId` /
> `sourceObservationId` on DatasetItem; Braintrust ships `origin`. Two vendors converged
> independently: **a benchmark item must remember which production trace it came from.** It
> is what makes "promote a failure into the suite" auditable rather than copy-paste.
>
> **`status: ACTIVE|ARCHIVED`** (Langfuse) — dataset items are **retired, never deleted**.
> That's what lets us re-run a historical benchmark exactly as it was, by filtering on
> status-at-a-timestamp. Adopt verbatim.

### 2.6 One hash, three consumers

```python
bucket = H(session_id) % 10_000      # deterministic, coordination-free, per Langfuse/OTel
                                     # TraceIdRatioBased
```

Consumed by:
1. **eval sampling** (note 06 §1: trace-level all-or-nothing; *"scores inherit the sampling
   decision of their parent trace to prevent orphaned scores"*)
2. **shadow selection**
3. **canary assignment** — *"maintain consistent user assignment so users experience
   coherent behavior within sessions rather than random model switching per request"*

> **For a roleplay product, sticky assignment is correctness, not comfort.** Randomizing per
> request means **the persona changes mid-conversation**. And the same function that makes
> canary sticky makes eval sampling session-complete — which note 06 §2 requires, because a
> per-generation sampler drawing generation #47 with no view of #1–46 is **structurally
> blind** to boundary erosion, dependency, and persona drift. **One function, three
> problems.**

### 2.7 Standard vs us — the honest ledger

| need | OTel GenAI | OpenInference | Langfuse | ours |
|---|---|---|---|---|
| generation fields | ✅ good | ✅ good | ✅ | adopt OTel names |
| conversation content | ⚠️ **Opt-In** | ✅ flattened | ✅ | opt in |
| session **entity** | ❌ label only | ❌ label only | ✅ | **build** |
| score on a session | ❌ | ❌ | ✅ | **build** |
| evaluator identity | ❌ | ❌ | ❌ (metadata) | **build** |
| pairwise outcome | ❌ (scalar) | ❌ | ❌ | **build** |
| judge cost/latency | ❌ (event) | ✅ (span kind) | ✅ | **build** |
| guardrail as span | ❌ | ✅ | ~ | steal idea |
| π_i / inclusion prob | ❌ | ❌ | ❌ | **build** |
| variant identity | ❌ | ❌ | ❌ | **build** |
| distance-to-anchor | ❌ (bool) | ❌ | ❌ | **build** |
| provenance | ❌ | ❌ | ~ | **build** |

**Verdict: adopt `gen_ai.*` names for the generation event; add an `eval.*` namespace for
everything else; do not wait for the standard.** Nearly every `gen_ai.*` attribute is at
**`Development`** stability — pre-stable, MAY break. Pin the semconv version and treat a
bump as a change with a migration.

⚠️ **Do not adopt OpenInference's flattening as our storage schema.** `llm.input_messages.0
…99.message.content` on a 102-turn corpus is unbounded **column-name** cardinality — note 06
§6's cardinality hazard relocated into the namespace. OTel's structured `any` is the right
call for us. (The two specs made **opposite choices on the same problem**; ours is the
long-conversation case, which breaks the tie.)

---

## 3. What is logged at each stage

**The point of this table: the schema is one schema.** The same `generation` row shape is
written by the CI harness and by production. That is what makes a benchmark score and a
production score comparable — and it is why `eval.rollout_stage` is a **column, not a
separate table**.

| | 0 dry-run | 1 benchmark | 2 shadow | 3 canary | 4 live | 5 curation |
|---|---|---|---|---|---|---|
| `generation` | ✅ local | ✅ | ✅ (turn 1) | ✅ | ✅ 100% | — |
| `session` | — | ✅ | ❌ n/a | ✅ | ✅ 100% | — |
| Lane 0 guardrail | — | ✅ | ✅ | ✅ 100% | ✅ 100% | — |
| Lane 1 cheap | ✅ | ✅ | ✅ | ✅ 100% | ✅ 100% | — |
| Lane 2 corpus stat | — | ✅ full grid | ❌ | ~ | ✅ batch | — |
| Lane 3 judge | ❌ | ✅ full | ❌ | ❌ | ✅ ~1% strat | — |
| `label` (human) | — | on abstain | — | — | 4 queues | ✅ |
| `curation` | — | — | — | — | — | ✅ |
| π_i recorded | n/a | 1.0 | ✅ | ✅ | ✅ | ✅ |

**Read the Lane 3 row.** The judge runs at **stage 1 and stage 4 only**. Not in shadow
(off-policy — §0.1). Not in canary (12% FP rate + 1–3 s latency; note 06 §1: *"never alert
on a single bad score"*). **Nobody auto-rollbacks on a judge score and neither should we** —
a 12%-FP instrument wired to automatic production rollback is an outage generator. Judge
scores inform a **human** ship call on a slow clock; **cheap deterministic signals drive the
automation.** RLUF is the proof: the reward hack was caught by a phrase rate, not a rubric.

---

## 4. The gate that actually gates

### 4.1 The CI mechanics are settled — do not invent them

Every tool surveyed has the same four parts (`pipeline-evals-as-ci-landscape.md`):
a CLI that runs a dataset through a config → a CI action on PR → comparison against a named
baseline → a threshold that fails the build.

```yaml
# the shape. promptfoo's trigger is the right one:
on:
  pull_request:
    paths: ['variants/**', 'prompts/**', 'rubrics/**']
```

**The system prompt is source code.** It lives in the repo, it triggers CI when it changes,
it gets reviewed. That's the whole "evals as CI" thesis, and it's free.

**Baseline = the incumbent, always.** promptfoo does before/after on the changed prompt;
DeepEval has an "official test run" on main. Both reframe the gate from *absolute threshold*
to *delta vs a pinned baseline* — structurally identical to note 11 §1's pairwise-not-
absolute. **The CI tools and the measurement design agree: the comparison is the unit.**

### 4.2 The gap: every tool compares point estimates

This is where we differ from all five, and it is the platform's reason to exist.

- promptfoo: `if PASS_RATE < 95: exit 1`
- DeepEval: `--regression` → *"fails if any metric regresses"*
- Braintrust: `__pass_threshold`

> **At our noise floor these are noise machines.** Note 10: at n=3 runs a single
> (model, character) cell resolves only **19.4pp**; a 2pp difference needs **281 runs**. A
> gate firing on *any* downward movement of *any* metric fires on nearly every PR. The team
> disables it in a fortnight. **This is the single most common way an eval-gate program
> dies, and it is a statistics failure, not a tooling failure.**

**Our gate:**

```
FAIL iff  the shrunk per-cell estimate's CI excludes the baseline by more than
          the dimension's pre-registered MDE
```

with note 11's machinery underneath: **shrinkage, not division** (§4 — never display a raw
per-cell score); **BT with length as a style covariate** (§2 — coefficient 0.249, ~8× any
formatting term; unmitigated **we ship a verbosity meter**, and "be thorough and detailed"
is a one-line leaderboard exploit findable in week one); **min-over-turns** (§6);
**mixed-effects with random intercepts per character** (§7 — effective n ≈ 95).

**And no pooled cross-language number** (§3: `Spearman(en, zh) = −0.082`; grok-4.1 swings
1.4% → 29.6% on repetition). **The gate runs per language and the platform refuses to
aggregate.** A CI check that emits one number across languages is lying; ours emits two and
fails if either fails.

Adopt Braintrust's four rules verbatim — they're unusually good and each maps onto us:
1. **Schema validators require 1.0** → our Lane 1 format checks
2. **Calibrate judge thresholds BELOW measured human agreement** → **κ≈0.53 *is* that bound**
   (note 11 §7). A gate stricter than the instrument's reliability is a coin flip.
3. **Start scorers in shadow before making them blocking** → **a new metric is a change that
   needs a canary.** Note 11's "no dimension ships without its noise floor" is the same rule
   stated statistically.
4. **Revalidate judges against human labels when prompt or model version changes** → note 11
   §8: a judge bump is a **breaking change requiring re-baseline**.

### 4.3 Data hygiene in CI

⚠️ **The CI tier must run on human-authored characters only — never on mined production
conversation.** promptfoo posts results as **PR comments** and has a `--share` flag and a
`shareableUrl`. Our production traffic is intimate companion conversation. **A PR comment on
a shared repo is an exfiltration channel.** promptfoo ships
`PROMPTFOO_STRIP_RESPONSE_OUTPUT=true` for exactly this. Set it, and enforce the
character-provenance rule in the harness rather than in a wiki page.

---

## 5. Where the human attaches

### 5.1 Four queues, not one

The annotation queue is the flywheel's on-ramp, not a labeling tool — LangSmith is explicit
that single-run queues are for *"triaging issues or **building datasets from production
traces**."* One UI, **four queues, four different inclusion probabilities**:

| queue | source | π | consumer | cadence |
|---|---|---|---|---|
| **A. Abstentions** | judge declined (note 11 §6: ~19% contested) | 1.0 of abstains | judge calibration on hard cases | continuous |
| **B. Uniform audit** | random sample of production | **uniform, fixed** | ⚠️ **unbiased κ + Tier-2 FP rate** | weekly |
| **C. Uncertainty** | judge low-confidence / disagreement | non-uniform | cheap improvement | weekly |
| **D. Curation** | flagged sessions, Tier-1 outliers | purposive | promote/reject → §5.2 | weekly |

> ### ⚠️ Queue B exists for one reason and it is easy to skip
>
> Shankar's rule — *"prioritize retrieving examples where human labels differed from what an
> LLM would predict"* — is the sharpest sampling advice in the literature, and it maps neatly
> onto note 11 §6 (abstentions route to humans → **a free calibration set on exactly the hard
> cases**). Two motivations, one queue. Tempting to stop there.
>
> **But if human labels are collected *only* where the judge is uncertain, the calibration
> set is non-random by construction and κ measured on it is not κ on production.** It's κ on
> the hard tail — a biased lower bound. **This is note 06 §3's Horvitz–Thompson lesson
> applied to human labels instead of judge samples: once selection is non-uniform, the naive
> average is biased.** Same math, and it silently corrupts the headline reliability number
> that the whole platform's credibility rests on.
>
> Note 06 §1 already assigned this job — *"the gold tier isn't just for hard cases — it is
> the instrument that **measures** Tier 2's FP rate"* — and an instrument must sample the
> population it's measuring. **Queues B and C must never be pooled.** Record `queue_id` and
> `inclusion_prob` on every label or the distinction is lost the first time someone runs a
> `GROUP BY`.

### 5.2 How much human labeling is realistic

Industry practice (`pipeline-annotation-iaa-cost.md`): **200–500 hand-labeled traces per
workload per rubric**, **2–3 labelers each**, κ tracked. Efficiency rule: **double-label 20%
of tasks**, single-label the rest — **κ is estimated from the overlap, not the whole set.**
Against note 06's Tier 3 (5k/day), a double-labeled 20% subsample of a much smaller expert
tier is tractable.

> ### ⚠️ The industry κ bar is unreachable for us, and adopting it silently would sink the project
>
> Everyone quotes **κ>0.80 strong / 0.60–0.80 substantial / <0.60 "needs rubric work."**
>
> Note 01: humans agree on roleplay quality at **α = 0.25–0.34**. Note 11: judge ceiling
> **κ ≈ 0.53**. **Both are "needs rubric work" by the industry rule — and no amount of rubric
> work will fix them**, because the disagreement is **in the construct, not the instrument**
> (Amabile: experts achieve reliability on creativity only *relatively within a set*; ~19% of
> items are irreducibly contested).
>
> **A team that adopts κ>0.8 as a gate for a companion-quality rubric will burn a year and
> never ship.** The correct response to α=0.25–0.34 is not a better rubric — it is note 11's
> entire thesis: decompose until the objective part falls out, go pairwise for the residue,
> abstain on the contested fifth.
>
> **Two bars, stated explicitly, in the score config:**
> - **Lane 0/1 bounded tasks** (safety autofail, format, voice leak) → **demand κ > 0.8.**
>   These are the "bounded task, high reliability" cells in note 11's lane table. Hold the
>   industry line here.
> - **Lane 3 creative-quality** → **κ ≈ 0.5 is the ceiling, published as a known instrument
>   limitation.** Anything higher is a bug in the measurement, not a win.
>
> Also: **LLM judges beat crowd workers** (κ>0.70 vs crowd, on classification tasks). So
> "hire crowd annotators" is **not** an escape from the reliability problem. Our human tier
> must be **expert/trained annotators on a small calibration set** — a hiring and
> rubric-training cost, not a marketplace spend. (⚠️ **Do not port that κ>0.70**: it's from
> bounded classification. The same models score **r=0.159 / 40% consistency** on absolute
> creativity, note 03.)

### 5.3 The failure-mode enum must be ours

Braintrust's five (hallucination / retrieval miss / tool-arg error / instruction-follow /
format violation) is a **RAG/agent taxonomy — we have no retrieval and no tools, and only
two transfer.** Every published flywheel writeup assumes a RAG app; **nobody has published a
companion/roleplay curation taxonomy.** Ours, from notes 07/11:

```
persona_drift | repetition_loop | voice_homogenization | constraint_violation
| format_violation | assistant_voice_leak | sycophancy | boundary_erosion
| dependency_signal | crisis_mishandling | engagement_farming     ← RLUF's "bye" mode
```

**The practice of a closed enum transfers; the enum does not.** `engagement_farming` earns
its place from RLUF: a real, measured, production degeneration in a conversational product
with a user-affect reward — the closest published analogue to us.

---

## 6. Curation: closing the loop without eating ourselves

### 6.1 The contradiction, and the resolution

**A benchmark must be frozen to be comparable across time, and must change to stay
representative.** Every source on eval-set drift states both and none reconciles them
(*"built at launch and frozen forever, by month six... the set scores a system that no
longer exists"*).

**Resolution: stop treating it as one set.** Note 11 §3 already forces this split for a
different reason (a *frozen anchor set* is what makes pairwise O(n) and keeps comparability
as variants come and go):

| | **frozen anchor set** | **rolling representativeness set** |
|---|---|---|
| purpose | **comparability** across variants/time | **coverage** of current traffic |
| mutability | **never changes** | refreshed from production |
| provenance | **human-authored** | mined |
| changing it breaks | every historical score | nothing |
| answers | "is B better than A?" | "does the benchmark still look like traffic?" |

**Only the second drifts and only the second may be refreshed.** Conflating them is what
makes eval-set drift look unsolvable.

### 6.2 The same split defuses model collapse

Nature 2024 (`pipeline-model-collapse.md`): recursive training on model-generated data
causes **irreversible defects**; **tails of the original distribution disappear**. Critically:

> **Early collapse: the model "loses information about distribution tails," primarily
> affecting minority data. Performance metrics may appear stable while minority-data
> accuracy declines significantly.**

**"Aggregate metrics look fine while the tail dies" is our platform's failure mode,
restated.** Note 11's Lane 2 exists because homogenization is invisible per-character and
only measurable across the cohort; note 06 §3 exists because uniform sampling starves the
tail. **Our 95-character grid *is* the tail**, and note 09 already measures homogenization as
a real, moving quantity. **This is not hypothetical for us.**

And the collapse mechanism is **replacement**: `Var(X^n) = σ²(1 + n/M)`, recursively → a
delta function. But the follow-up literature is decisive on the fix — **collapse is largely
averted when synthetic and human data *accumulate together* rather than replace.**

> **So: the benchmark ACCUMULATES, never REPLACES.** Mined cases are generated by *our own
> variants*. If curation gradually replaces human-authored anchors with model-generated
> cases, **we are running the Nature experiment on our own eval set** — generation by
> generation the benchmark's tails vanish and it converges to "whatever our models already
> do." **The eval would report improvement forever, by construction.** That is the most
> dangerous single failure available to this platform, because it is invisible and
> self-congratulating.

**Three enforced rules:**
1. **The frozen human-authored anchor set is never regenerated and never retired.** It is the
   non-synthetic term that makes accumulation safe — and it's already load-bearing for
   pairwise comparability. One artifact, two jobs.
2. **Every dataset item carries `provenance`**, and **mined items are capped as a fraction of
   the suite**, monitored as a first-class number. **Ratio → 1.0 means the eval set is
   collapsing.**
3. **Never promote items selected by the judge alone** — that's the recursive loop with extra
   steps. A human decides (queue D), and the **family-disjoint panel** (note 11 §5) keeps the
   judge off its own family's output.

⚠️ **Enforce rule 2 in CI, don't monitor it.** lakeFS's pre-merge hooks are the pattern:
refuse a merge to the benchmark branch unless every new item carries `provenance` and
`source_trace_id`, and unless the mined fraction is under cap. **A monitored cap drifts; an
enforced cap doesn't.**

### 6.3 Detecting eval-set drift quantitatively

The blogs say "refresh quarterly" and never say **how you know**. Note 06 §5 already built
the instrument:

```
PSI( benchmark_distribution ‖ production_distribution )
    over: character mix, language mix, turn depth, length distribution,
          session length, distance_to_anchor
    10 frozen reference bins.  0.1 warn / 0.2 alert.
```

**Eval-set drift is just distribution drift with the benchmark as reference.** Same
statistic, same thresholds, same code path — a materialized view and a reference snapshot.
No new machinery.

The alert reads: *"the benchmark no longer resembles production on character-mix; PSI =
0.24."* Actionable, dated, debuggable — more than "refresh quarterly" provides.

And **freeze the bin edges on the reference** (note 06 §5): recomputing per batch destroys
comparability. Classic silent bug.

### 6.4 The dual-vintage run

The one concretely good idea in the drift literature, and it's cheap:

> **"For every model release, run against the current month's set AND the set from 6 months
> ago."**

This decomposes note 06 §7's three-way ambiguity. A regression = variant got worse **or**
traffic mix shifted **or** evaluator changed. Running **two vintages of the benchmark on one
variant with one pinned evaluator holds variant and evaluator constant and isolates the
set** — turning composition drift from a confound into a measurement.

Because full-trace retention is only 3–8 TB/yr (note 06 §6), we can go further: **retro-score
history under the new set** and get a clean 2×2 of (set vintage) × (variant vintage). **This
is the payoff for not sampling storage.**

---

## 7. Offline↔online: what we can and cannot claim

**The RLUF construction is the only strong published evidence, and reading it correctly
matters more than citing it.** r=0.95 was achieved by:
- an evaluator **trained on 1M production labels of the actual online metric** (P[Love],
  Llama3-8B + classification head, positives upsampled to 10%)
- scored on a **fixed prompt set**
- correlated over **10 iterations of the same model family in the same product**

> **The correlation is high because the offline metric is a learned surrogate of the online
> metric on in-distribution traffic.** That is a completely different object from a rubric
> judge or a static benchmark. **Nobody has published r=0.95 for "our benchmark predicts our
> A/B test."** The lesson is not *"offline evals correlate with online"* — it is **"offline
> evals correlate with online when you build the offline evaluator by regressing on the
> online outcome."**
>
> (Also: **n=10 points.** r=0.95 on n=10 has a CI of roughly 0.80–0.99. Directionally strong,
> not a precision instrument. Don't quote it as 0.95±nothing.)

**What we should therefore build — and it's a different thing from our benchmark:**

1. **A surrogate model of our online outcome**, trained on production labels, scored on a
   fixed prompt set. **This is the only construction with published evidence of predicting
   online behavior.** It is *not* the rubric judge and must not be confused with it. It is a
   separate Lane, cheap to run, and it answers "will this variant move the product metric?"
2. **Backtest it against our own history** — the RLUF validation method (10 past A/B tests)
   costs nothing but bookkeeping and is the only way to earn the claim. **We cannot claim
   offline↔online correlation until we've done this.** Until then the benchmark's status is
   *"detects regressions we defined"*, not *"predicts user outcomes."* Say so on the
   dashboard.
3. ⚠️ **And never let it gate a ship, precisely because it correlates.** RLUF: +28% on the
   target metric, "bye" rate **0.72% → 2.8%**, premature conversation closure. **The
   correlation and the reward hack are the same experiment.** A metric that predicts online
   outcomes is a metric worth gaming.

**Pre-register a side-channel tripwire per dimension.** For each dimension, name the
degenerate strategy that would win, and log a cheap deterministic statistic that detects it.
RLUF's "bye" rate is the template — it was **not** the optimized metric, **not** a judge
score, and it is what caught the pathology. This operationalizes note 11's open question #3
(*"name the model that would win by gaming it"*) as a logging requirement instead of a
discussion topic.

| dimension | degenerate strategy | tripwire (Lane 1, 100%) |
|---|---|---|
| engagement | end scenes early to farm reactions | session-end rate, turn-count distribution |
| emotional attunement | escalating intimacy / dependency | intimacy-lexicon rate, session frequency per user |
| narrative engagement | cliffhanger spam | question-mark rate, turn-length collapse |
| creativity | verbosity | **length distribution** (already the #1 confound, note 11 §2) |
| character fidelity | refuse-everything safety posture | refusal rate, Lane-0 trigger rate |

> Note how many of these are already in the canary gate. **The canary's cheap signals and
> the anti-gaming tripwires are the same list.** That is not a coincidence — both are asking
> "did the model find a shortcut?" **Build the list once.**

---

## 8. The uncomfortable parts

### 8.1 Criteria drift undercuts a premise we rely on

"Who Validates the Validators?" (UIST 2024):

> *"users need criteria to grade outputs, but grading outputs helps users define criteria"* —
> some criteria *"appear dependent on the specific LLM outputs observed (rather than
> independent and definable a priori), **raising serious questions for approaches that assume
> the independence of evaluation from observation of model outputs**."*

Note 11 assumes a **frozen** rubric and **frozen** anchors — that criteria are definable a
priori and held still while variants move. **Criteria drift says the rubric is itself a
moving object that only stabilizes by looking at outputs produced by the variants we're
grading.** The eval and the evaluated are not independent.

**We can't dissolve this. We contain it:** a rubric change is **allowed**, but it is a
versioned, content-addressed release requiring **re-baseline on the frozen golden set** (note
06 §7) — never a silent edit. Criteria drift becomes a **visible, dated event in the
lineage** rather than an invisible confound.

**The honest framing, and it should be on the dashboard:** *our eval does not measure a fixed
construct over time; it measures a construct we re-ratify at each rubric version, and the
golden set is what makes the re-ratification auditable.*

### 8.2 Confidence must be purchased, not read off

Shankar: **"next-token probabilities from instruction-tuned models are uncalibrated and
unhelpful when analyzing outputs at scale."**

Note 06's Tier 1 lists logprobs among cheap 100%-coverage signals, and note 11 §6's
abstention + note 06 §4's Trust-or-Escalate cascade both need a **confidence** signal.
**The free one doesn't work.** That's precisely why Trust-or-Escalate uses **N=5 Simulated
Annotators** and why the paper reconciles to **">40% cost reduction"** rather than 78.5%
(note 06 §4's warning). **Budget for calibration; don't plan on reading it off the logits.**

### 8.3 A qualitative signal must be able to block a ship

Note 11 open question #4, and §0.2 is the evidence: **the A/B test approved the sycophantic
model.** RLUF's aggressive variant was **p << 0.01 significant** and **28% better** on its
metric — and it was worse. Statistical significance was never the problem. **If stage 4's
exit is "the numbers are green," we rebuild the OpenAI April 2025 incident with better
dashboards.** Stage 4 needs a named human owner with veto power and no obligation to
quantify the objection.

### 8.4 Open questions for the lead

1. **Do we accept that shadow is only a smoke test?** If someone wants a real pre-launch
   quality signal on production traffic, **the honest answer is that it does not exist for
   multi-turn** — the options are self-play offline (on-policy, no users) or canary
   (on-policy, real users). This will be argued; the argument is §0.1 and note 11 §7.
2. **Do we build the RLUF-style surrogate at all?** It's the only construction with published
   offline↔online evidence — and §7.3 says it must never gate. **Is a predictor we refuse to
   gate on worth building?** (I think yes: it prioritizes *which* variants deserve an
   expensive canary. But it needs an explicit decision, not a default.)
3. **What is the mined-fraction cap?** §6.2 rule 2 needs a number. There is no published
   guidance. Suggest starting at **0.5** and monitoring the anchor set's share as the real
   control.
4. **Who owns the dual-vintage benchmark run?** It's cheap and it's the only defense against
   confusing composition drift with quality drift. It's also the first thing cut when CI gets
   slow.
5. **Judge TPM vs production TPM** (note 06 open q5) now has a lifecycle edge: the **CI
   benchmark** is bursty by nature — a PR triggers 95 chars × 2 langs × 102 turns × n runs.
   **A merge queue could throttle production if they share a rate-limit pool.** Separate
   workspace/key, and this is now urgent rather than theoretical because it fires on every PR.
6. **Semconv is `Development`-stability.** We're building on a spec that MAY break. Pin the
   version, budget for a migration, and don't let `gen_ai.*` names into our internal
   analytics contracts — map at the edge.
