# The noise floor — measured, not assumed (2026-07-16)

Computed by [scripts/noise_floor.py](../../scripts/noise_floor.py) over all 3,135 dialogues.
The dataset's 3 independent runs per (model, character) cell let us decompose variance directly.
Most eval harnesses have to guess this. We don't.

Worked example: the repetition metric (judge-free, no API).

## Variance decomposition

| quantity | en | zh |
|---|---|---|
| σ_within — run-to-run, **same model, same character** | **0.0847** | **0.0639** |
| σ across characters, within a model | 0.0352 (0.4× run noise) | 0.0413 (0.6× run noise) |
| σ across models (of model means) | 0.0600 (0.7× run noise) | 0.0870 (1.4× run noise) |

## Finding 1: run-to-run noise exceeds the between-model signal

In English, **σ_within (0.0847) > σ_between-models (0.0600)** — ratio 1.41. Re-running the *same
model* on the *same character* moves the metric more than switching to a different model does.

**A single conversation carries less signal than noise.** Any product surface that shows a score
for one dialogue — "this response scored 3.2" — is showing a coin flip with a decimal point.
This is not a rubric problem; it's the generative process. Temperature is doing this.

Consequences:
- The unit of *evaluation* is never the conversation. It is a cell mean over many rollouts.
- "Look at this bad example" is a **debugging** affordance, not a **measurement** one. The UI
  must not let the two be confused — showing a transcript next to a score invites exactly that.
- zh is better behaved (ratio 0.73) — another instance of the two languages not being one system.

## Finding 2: model-level comparison is well-powered — for large effects only

At 45–50 characters × 3 runs:

| | en | zh |
|---|---|---|
| SE of a model mean | 0.0052 | 0.0058 |
| min detectable model-vs-model delta (80% power, α=.05) | **2.08 pp** | **2.31 pp** |
| observed max model gap | 19.9 pp (10× MDE) | 29.1 pp (13× MDE) |

The big gaps (grok-4.1 zh at 29.6% repetition) are 10–13× the noise — unambiguously real. Good.
But the interesting question is never "is grok obviously broken." It's "did this config change
cost us half a point," and there:

| regression to detect | characters needed (en) | (zh) |
|---|---|---|
| 1.0 pp | 194 | 267 |
| 0.5 pp | 775 | 1,070 |
| 0.2 pp | 4,847 | 6,685 |

**We have 45 en / 50 zh. The benchmark resolves ~2pp. It cannot see a 1pp regression.** A
prompt tweak or a thinking-budget change — precisely the ship decisions this platform exists to
serve — plausibly lives under 1pp. **The current benchmark is underpowered for its actual job**,
and no amount of judge quality fixes it: this is σ_within, and it is upstream of the rubric.

Levers, in order of cost-effectiveness: more **runs per cell** (cheap — generation is ~100× cheaper
than judging), more **characters** (needs authoring), variance reduction via **pairing on
identical seeds** (free, costs only harness discipline).

## Finding 3: per-character drill-down is statistically hollow at n=3

This is the uncomfortable one, because the brief asks for it explicitly.

| | en | zh |
|---|---|---|
| SE of a single (model, character) cell, 3 runs | 0.0489 | 0.0369 |
| MDE between two models **on one character** | **19.4 pp** | **14.6 pp** |
| runs/cell needed to resolve a 2pp per-character difference | **281** | **160** |

To claim "variant B regressed **on Sherlock specifically**" at a 2pp effect requires ~281 runs of
that cell. We have 3. **At n=3, a per-character verdict can only detect a ~19pp difference** —
i.e. only catastrophic, already-obvious breakage.

This does **not** mean drop the drill-down. It means the naive version — compute the metric per
cell, rank, show the worst — is a **noise amplifier**, and it will reliably manufacture a
plausible story about a specific character every single release. Someone will then spend a day
investigating it. That is the mechanism by which teams learn to ignore the platform.

**The fix is the one the psychometrics stream already recommended, arrived at from the opposite
direction:** a hierarchical / partial-pooling model. Per-character estimates get shrunk toward
the model mean by their own noise, so low-evidence cells stop screaming. Cells with genuine
signal survive shrinkage; the other 189 go quiet. Note this is the *same* mixed-effects
machinery that yields the G-study variance components and the clustering correction — one model,
three problems.

**Design rule: the platform must never display a raw per-cell score.** It displays a shrunk
estimate with its interval, or it displays nothing. A number without its uncertainty is a lie in
this system, and per-cell is exactly where the lie is largest.

## Finding 4: characters vary less than runs do

σ across characters within a model (0.0352 en) is **0.4× the run-to-run noise** (0.0847). The
character axis carries real but modest signal for *this* metric — much less than the language
axis, which is enormous (see [09-offline-probes.md](09-offline-probes.md), en/zh rank
correlation −0.082).

Tentative ordering of axis importance, on current evidence: **language ≫ model > character**.
This is one metric only; it must be re-checked per dimension before it informs the aggregation
hierarchy. If it holds, it argues for language above the aggregation line, model next, and
character as a shrunk diagnostic rather than a headline slice.

## Caveats

- One metric (repetition). Other dimensions — especially judge-scored ones — will have their own,
  probably worse, σ_within, since judge stochasticity adds on top of generation stochasticity.
  **Every dimension needs its own noise floor measured before it ships.** That should be a gate.
- Power calc uses a two-sample normal approximation (z≈2.8 for 80%/α=.05 two-sided); repetition
  rates are bounded and skewed, so treat these as the right order of magnitude, not exact.
- σ_within here bundles generation temperature *and* user-simulator stochasticity, which the
  dataset confounds (see [00-dataset-ground-truth.md](00-dataset-ground-truth.md)). Separating
  them requires holding the user turns fixed — impossible in this corpus, possible in ours.
