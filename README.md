# model_eval — Companion Variant Evaluation Platform

Ship/no-ship decisions for AI companion variants (model + params + system prompt), pre-launch and
in production. Built around one claim:

> **This is a measurement problem, not a deployment problem.** Running evals at scale is plumbing
> — the numbers say it's easy (3,600× ingest headroom). Putting a *trustworthy* number on
> "creativity" or "character fitting" is the hard part, and if the instrument is bad the platform
> is an expensive random number generator that produces confident, well-formatted, wrong answers.

**Status:** research complete (16 streams, 475 sources, 26 notes). Design decided. **Platform built and running** — 3,303 LOC, zero dependencies, end-to-end on real data with no API key. **10 of 13 requirements fully met**; the 3 partial ones are blocked on an API key, not on design. See [HONEST-REVIEW.md](docs/HONEST-REVIEW.md) for what doesn't work.

## Start here

| | |
|---|---|
| **[docs/HONEST-REVIEW.md](docs/HONEST-REVIEW.md)** | **What works, what doesn't, and the six times a plausible number was wrong** |
| **[QUICKSTART.md](QUICKSTART.md)** | Run it — zero deps, no API key |
| **[PROJECT.md](PROJECT.md)** | Mission, requirements, acceptance criteria, open decisions, risks |
| **[docs/ABILITY-MODEL.md](docs/ABILITY-MODEL.md)** | **What makes a roleplay model good**: comprehension -> application & steerability -> creativity |
| **[docs/BENCHMARKS.md](docs/BENCHMARKS.md)** | The benchmark catalogue, and an honest account of what it does not measure |
| **[docs/FLOWS.md](docs/FLOWS.md)** | System flows: dry-run → benchmark gate → online collection → eval loop → ship decision |
| **[docs/RESEARCH-PLAN.md](docs/RESEARCH-PLAN.md)** | What we researched, what's missing, what needs investigation |
| **[research/notes/11-evaluation-method-design.md](research/notes/11-evaluation-method-design.md)** | **The core design**: which fields, how to grade, how to normalize |
| **[research/](research/)** | The knowledge base — 271 raw sources + 15 synthesis notes |

## The five findings that drive the design

All measured by us on the real corpus ([09](research/notes/09-offline-probes.md),
[10](research/notes/10-noise-floor.md)), not borrowed:

1. **A single conversation is not evaluable.** Run-to-run noise exceeds the between-model signal
   (σ_within 0.0847 > σ_between 0.0600). Any per-dialogue score is a coin flip with a decimal point.
2. **Model rankings don't survive a language change.** `Spearman(en, zh) = −0.082`. A pooled
   cross-language number averages two unrelated quantities and is wrong about both — the platform
   should *refuse* to emit one.
3. **Per-character drill-down is hollow at n=3.** Per-cell MDE is 19.4pp; resolving 2pp needs 281
   runs. Raw per-cell scores are noise amplifiers. Shrinkage is mandatory.
4. **The benchmark is underpowered for real ship decisions.** It resolves ~2pp; a 1pp regression
   needs ~194 characters and we have 45. No judge quality fixes this — it's upstream of the rubric.
5. **We broke our own metric, twice, in one afternoon.** A literature-recommended metric,
   implemented the obvious way, gave a plausible ranking that was really measuring verbosity
   (ρ=+0.73 with length). The fix introduced a survivorship confound. Neither was visible in the
   output. **Hence: a metric's confound tests are part of its definition, not a review step.**

## What this platform promises — and refuses to

Humans agree with each other on roleplay quality at **Krippendorff α = 0.25–0.34**. LLM judges
scoring creativity absolutely hit **r = 0.159** vs humans. The same judges hit **73–78%** on
pairwise comparison.

> **We cannot sell stable aesthetic scores — nobody can, humans included.**
> **We can sell stable violation rates against a fixed spec.**

So: decompose every soft dimension until the objective part falls out, and send only the residue
to a judge. Creativity = novelty (computable) + non-slop (computable) + constraint satisfaction
(computable) + charm (judge). Three of four need no model call.

## Four lanes

| Lane | Mechanism | Coverage | Cost @50M/day | Reliability |
|---|---|---|---|---|
| **0 Safety gate** | regex + classifier | 100% blocking, 5–50ms | ~$0 | high (bounded task) |
| **1 Spec compliance** | pure computation | 100% async | ~$0 | **exact** |
| **2 Corpus statistics** | computation over k samples | 100% batch | ~$0 | exact, needs k≥10/cell |
| **3 Judge** | pairwise panel vs frozen anchors | ~1% stratified | ~$738/day | **κ≈0.53 ceiling** |

Tiered: **$283k/yr** vs **$26.9M/yr** to judge everything with even the cheapest judge — a **95×**
reduction. Latency, not cost, is what forces the tiering: a judge takes 1,000–3,200ms against a
~200ms guardrail budget, so even a *free* judge is 5–16× too slow to sit inline.

## Data

`MiniMaxAI/role-play-bench` — 95 characters (45 en / 50 zh), 11 models × 3 runs × 102 turns =
3,135 dialogues, ~320k turns. Balanced factorial, no missing cells.

Not committed (171 MB, redownloadable). Fetch:

```bash
mkdir -p data/{en,zh} data/_quarantine
B=https://huggingface.co/datasets/MiniMaxAI/role-play-bench/resolve/main/data
for L in en zh; do
  curl -sL "$B/$L/seeds.jsonl"       -o data/$L/seeds.jsonl
  curl -sL "$B/$L/dialogues.jsonl"   -o data/$L/dialogues.jsonl
  curl -sL "$B/$L/evaluations.jsonl" -o data/_quarantine/evaluations.$L.jsonl
done
```

`evaluations.jsonl` holds the dataset's **published scores** — quarantined, the brief forbids
using them. Kept out of the pipeline; legitimate only as an external convergent-validity check
*after* our instrument is frozen.

```bash
python3 scripts/noise_floor.py   # reproduces the variance decomposition
```

## Open decisions

1. Keep or cut **`emotional attunement`**? Judge sentiment bias (RR 0.60–0.80, → 0.24–0.66 under
   sadness/anger/fear) has no published mitigation and sits on our core traffic.
2. Fix the underpowered benchmark with **more runs** (cheap) or **more characters** (authoring cost)?
3. **Governance:** can a qualitative signal block a ship when everything quantitative is green?
   OpenAI's April 2025 sycophancy rollback happened *because* A/B tests approved the model and
   expert dissent was overruled.
4. **Legal review** of CA SB 243 / NY GBL Art. 47 — and EU AI Act Art. 50 lands **2026-08-02**.
5. **API key** — gates every judge-lane experiment. Everything to date is judge-free.
