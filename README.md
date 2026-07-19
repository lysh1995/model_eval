# Companion Variant Evaluation Platform

A local, end-to-end **service** for making ship/no-ship decisions about AI companion variants
(model + params + system prompt) — pre-launch and in production. One CLI owns the whole loop:
inject a variant → evaluate offline + online → see it on a dashboard → decide, with evidence.

> **This is a measurement problem, not a deployment problem.** Running evals at scale is plumbing
> — the numbers say it's easy (3,600× ingest headroom). Putting a *trustworthy* number on
> "creativity" or "character fitting" is the hard part, and if the instrument is bad the platform
> is an expensive random number generator that produces confident, well-formatted, wrong answers.

**Status:** research complete (16 streams · 475 sources · 26 notes). Design decided. **Platform
built and running as a service** — ~6,800 LOC, **zero dependencies**, end-to-end on real data with
**no API key**. DB-backed (SQLite runnable, MySQL designed), live dashboard. **10 of 13
requirements fully met**; the 3 partial ones are blocked on an API key or on authoring, not on
design. See [docs/HONEST-REVIEW.md](docs/HONEST-REVIEW.md) for what doesn't work.

## Run it — one entrance

Zero dependencies, Python 3.9+, no API key. The whole service is `python3 -m ceval`:

```bash
python3 -m ceval init                 # create the SQLite DB (9 content-addressed tables)
python3 -m ceval seed                 # load the bundled demo variants + dialogues (demo/) → DB
python3 -m ceval eval run --sim       # score offline + online, persist grades + evidence
python3 -m ceval serve                # live dashboard → http://127.0.0.1:8787  (renders from the DB)
```

Inject your own variant and re-evaluate — everything gets an id and persists:

```bash
M=$(python3 -m ceval model  add --name gpt-5.1 --provider openrouter)
P=$(python3 -m ceval prompt add --name Playful --prompt "Tease, riff, never break character." --intent "playful")
python3 -m ceval variant add --model-id $M --prompt-id $P --id v_playful --label Playful
python3 -m ceval data add   --variant v_playful --character en_dialogue_011 --turns-file conv.json
python3 -m ceval eval run --sim && python3 -m ceval dashboard        # re-score, re-render
```

And the measurement science that justifies the design — judge-free, on the raw MiniMax corpus:

```bash
python3 -m ceval probe run  --lang en          # judge-free scores across all 11 dataset models
python3 -m ceval probe pool                     # watch the platform REFUSE to pool across languages
python3 -m ceval probe compare deepseek-v3.2 deepseek-v3.1 --lang en   # a ship report: Δ, CI, MDE
```

Full command reference in [QUICKSTART.md](QUICKSTART.md).

## What this platform promises — and refuses to

Humans agree with each other on roleplay quality at **Krippendorff α = 0.25–0.34**. LLM judges
scoring creativity absolutely hit **r = 0.159** vs humans. The same judges hit **73–78%** on
pairwise comparison.

> **We cannot sell stable aesthetic scores — nobody can, humans included.**
> **We can sell stable violation rates against a fixed spec.**

So: decompose every soft dimension until the objective part falls out, and send only the residue
to a judge. Creativity = novelty (computable) + non-slop (computable) + constraint satisfaction
(computable) + charm (judge). Three of four need no model call.

This is a **category correction**, not a workaround. NarraBench's taxonomy sorts narrative aspects
into three classes, each with a different right instrument:

| class | example | right instrument |
|---|---|---|
| **deterministic** | did it exceed the length cap? did it contradict the card? | computation |
| **consensus** | is this a plot hole? did the scene advance? | judge/NLI — agreement *is* meaningful, report κ |
| **perspectival** | is this beautiful? is this character *compelling*? | report the **distribution**, not a mean |

α=0.25–0.34 is not a failure of the raters. It is what you get when you score a *perspectival*
aspect with a *consensus* instrument. The platform's job is to **match instrument class to aspect
class** — and refuse to average across them.

## Four lanes

| Lane | Mechanism | Coverage | Cost @50M/day | Reliability |
|---|---|---|---|---|
| **0 Safety gate** | regex + classifier | 100% blocking, 5–50ms | ~$0 | high (bounded task) |
| **1 Spec compliance** | pure computation | 100% async | ~$0 | **exact** |
| **2 Corpus statistics** | computation over k samples | 100% batch | ~$0 | exact, needs k≥10/cell |
| **3 Judge** | pairwise panel vs frozen anchors | ~1% stratified | ~$738/day | **κ≈0.53 ceiling** |

Tiered: **$283k/yr** vs **$26.9M/yr** to judge everything with even the cheapest judge — a **95×**
reduction. Latency, not cost, forces the tiering: a judge takes 1,000–3,200ms against a ~200ms
guardrail budget, so even a *free* judge is 5–16× too slow to sit inline.

> **Lane ≠ Level.** The judge (Lane 3) is a *mechanism*. It is used sparingly across every ability
> level — L1 comprehension, L2 steerability, L3 craft, and safety — never a synonym for "the L3
> lane." See [docs/ABILITY-MODEL.md](docs/ABILITY-MODEL.md).

## The five findings that drive the design

All measured by us on the real corpus ([09](research/notes/09-offline-probes.md),
[10](research/notes/10-noise-floor.md)), not borrowed:

1. **A single conversation is not evaluable.** Run-to-run noise exceeds the between-model signal
   (σ_within 0.0847 > σ_between 0.0600). Any per-dialogue score is a coin flip with a decimal point.
2. **Model rankings don't survive a language change.** `Spearman(en, zh) = −0.082`. A pooled
   cross-language number averages two unrelated quantities and is wrong about both — the platform
   *refuses* to emit one.
3. **Per-character drill-down is hollow at n=3.** Per-cell MDE is 19.4pp; resolving 2pp needs 281
   runs. Raw per-cell scores are noise amplifiers. Shrinkage is mandatory.
4. **The benchmark is underpowered for real ship decisions.** It resolves ~2pp; a 1pp regression
   needs ~194 characters and we have 45. No judge quality fixes this — it's upstream of the rubric.
5. **We broke our own metric, twice, in one afternoon.** A literature-recommended metric,
   implemented the obvious way, gave a plausible ranking that was really measuring verbosity
   (ρ=+0.73 with length). The fix introduced a survivorship confound. Neither was visible in the
   output. **Hence: a metric's confound tests are part of its definition, not a review step** —
   enforced at import time, not in review.

## The platform, end to end

```
INPUT                      DOMAIN (stored, with ids)        OUTPUT
models, prompts,    ──▶    dimensions + scoring lanes  ──▶  dashboard
dialogues, sessions        grades + evidence + lineage      (static · interactive · live serve)
     (CLI)                          (DB)
```

- **Storage is the backbone** — one schema, two drivers. **SQLite** is the zero-dependency runnable
  backend (default); **MySQL** is the designed production database (full DDL in
  [ceval/store/schema.sql](ceval/store/schema.sql)). Models, prompts, and variants are
  **content-addressed** (id = hash of content), so "which prompt produced this score" is answerable
  from the row.
- **Two data sources, one instrument** — offline (benchmark dialogues) and online (production-like
  session signals) flow through the same registry, stats engine, and lineage store.
- **The dashboard reads the DB** — a static view (renders anywhere, even email), an interactive
  view (CSS-only tabs: select a variant, cross-compare, drill into good/bad examples per
  dimension), and `ceval serve`, which re-renders live from the DB on every request.

Architecture in [docs/SERVICE.md](docs/SERVICE.md) · offline design in [docs/OFFLINE.md](docs/OFFLINE.md).

## Data

`MiniMaxAI/role-play-bench` — 95 characters (45 en / 50 zh), 11 models × 3 runs × 102 turns =
3,135 dialogues, ~320k turns. Balanced factorial, no missing cells. It stands in for production.

Not committed (171 MB, redownloadable). The **service demo** in `demo/` runs without it; the
`probe` commands need it. Fetch:

```bash
mkdir -p data/{en,zh} data/_quarantine
B=https://huggingface.co/datasets/MiniMaxAI/role-play-bench/resolve/main/data
for L in en zh; do
  curl -sL "$B/$L/seeds.jsonl"       -o data/$L/seeds.jsonl
  curl -sL "$B/$L/dialogues.jsonl"   -o data/$L/dialogues.jsonl
  curl -sL "$B/$L/evaluations.jsonl" -o data/_quarantine/evaluations.$L.jsonl
done
```

`evaluations.jsonl` holds the dataset's **published scores** — quarantined, the brief forbids using
them. Kept out of the pipeline; legitimate only as an external convergent-validity check *after*
our instrument is frozen.

## Start here

| | |
|---|---|
| **[QUICKSTART.md](QUICKSTART.md)** | Run the service and reproduce the findings — zero deps, no key |
| **[docs/SERVICE.md](docs/SERVICE.md)** | **The service architecture** — DB, CLI, offline + online, dashboard, serve |
| **[docs/HONEST-REVIEW.md](docs/HONEST-REVIEW.md)** | **What works, what doesn't, and the six times a plausible number was wrong** |
| **[docs/OFFLINE.md](docs/OFFLINE.md)** | The offline design: test targets, the dimension scheme, scoring ranked by how little human judgment it needs |
| **[docs/ABILITY-MODEL.md](docs/ABILITY-MODEL.md)** | **What makes a roleplay model good**: comprehension → application & steerability → creativity |
| **[docs/EVAL-DESIGN.md](docs/EVAL-DESIGN.md)** | The decided measurement design: two rules, GATE/GUIDE/DEAD, the judge protocol, normalization |
| **[docs/BENCHMARKS.md](docs/BENCHMARKS.md)** | The ~50-dimension catalogue, and an honest account of what it does not measure |
| **[docs/PLATFORM.md](docs/PLATFORM.md)** | The architecture: offline gate and online monitor as one instrument, and where it's built |
| **[docs/FLOWS.md](docs/FLOWS.md)** | System flows: dry-run → benchmark gate → online collection → eval loop → ship decision |
| **[PROJECT.md](PROJECT.md)** | Mission, requirements, acceptance criteria, open decisions, risks |
| **[docs/RESEARCH-PLAN.md](docs/RESEARCH-PLAN.md)** | What we researched, what's missing, what needs investigation |
| **[research/](research/)** | The knowledge base — 475 raw sources + 26 synthesis notes |

## Open decisions

1. Keep or cut **`emotional attunement`**? Judge sentiment bias (RR 0.60–0.80, → 0.24–0.66 under
   sadness/anger/fear) has no published mitigation and sits on our core traffic.
2. Fix the underpowered benchmark with **more runs** (cheap) or **more characters** (authoring cost)?
3. **Governance:** can a qualitative signal block a ship when everything quantitative is green?
   OpenAI's April 2025 sycophancy rollback happened *because* A/B tests approved the model and
   expert dissent was overruled.
4. **Legal review** of CA SB 243 / NY GBL Art. 47 — and EU AI Act Art. 50 in force **2026-08-02**.
5. **API key** — gates every judge-lane experiment. Everything to date is judge-free.
