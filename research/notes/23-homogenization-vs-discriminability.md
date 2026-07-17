# Two catalogue metrics that don't measure the same thing (2026-07-17)

Produced by the platform itself: `python3 -m ceval.cli run --lang en`.

## The result

| model | homogenization | discriminability | (chance 2.2%) |
|---|---|---|---|
| gemini-2.5-pro | 0.089 | **93.3%** | |
| doubao-1.5-pro | 0.089 | **93.2%** | |
| deepseek-v3.1 | 0.067 | 86.7% | |
| gemini-3-pro | 0.065 | 84.1% | |
| claude-sonnet-4.5 | 0.045 | 80.0% | |
| grok-4.1 | **0.026** | 75.6% | |
| claude-opus-4.5-lowthinking | 0.046 | 73.3% | |
| deepseek-v3.2 | **0.103** | 73.3% | |
| MiniMax-M2-her | 0.045 | 72.1% | |
| claude-opus-4.5-highthinking | 0.057 | 71.1% | |
| gpt-5.1 | 0.063 | **64.4%** | |

```
Spearman(homogenization, discriminability) = +0.473   (permutation p = 0.146, n=11)
```

## What survives

**The two metrics are not redundant, and the sign is the interesting part.** If they measured one
construct we would expect a strong **negative** correlation — more homogenized ⇒ less
distinguishable. We get **+0.473**, which is *not significant at n=11* but is pointing the wrong way
for redundancy.

**Why that's coherent rather than broken:** they measure genuinely different quantities.

- **Homogenization** = *mean pairwise similarity* — how alike characters are on average.
- **Discriminability** = *separability* — whether a decision boundary exists.

These come apart exactly as within-class and between-class variance come apart. **A model can render
every character in a similar register (high homogenization) while giving each one a reliable tic
(high discriminability).** Mean similarity does not imply inseparability.

**Consequence: keep both.** [BENCHMARKS](../../docs/BENCHMARKS.md) already listed the pairing as a
gaming cross-check for K2 (*"a model could inject verbal tics to score well — cross-check against
K1"*). This is that cross-check earning its place on the first real run: **either metric alone would
give a different, confident answer.**

## ⚠️ What does NOT survive — and I nearly published it

My first pass tagged gemini-2.5-pro and doubao-1.5-pro **"similar voices, reliable TICS ← gaming
signature."**

**That is post-hoc storytelling.** It is **n=2 of 11**, at **p=0.146**, from a pattern I went looking
for after seeing the numbers. It is precisely the failure this project has documented four times
already — a plausible label attached to noise, and it *reads* like a finding.

**The honest claim is narrow:** the two metrics are not redundant. **Whether the positive direction
reflects tic-gaming is a hypothesis, and n=11 models cannot test it.**

To actually test it you would need the tic itself: extract each model's top discriminative features
per character and ask whether they are **stylistic markers** (a catchphrase, a punctuation habit — the
gaming signature) or **semantic content** (this character talks about surgery because they are a
surgeon — legitimate). That is a real experiment, it is cheap, and it is **not run**.

## Also worth noting

- **gpt-5.1 is the least distinguishable model at 64.4%** while sitting mid-pack on homogenization
  (0.063). On the catalogue metric that prices the business asset, it is last — and a homogenization-
  only view would not have shown it.
- **deepseek-v3.2 is the most homogenized (0.103) and mid-pack on discriminability (73.3%).** It is
  also the model that writes **15× longer than its own predecessor** (3,783 vs 741 chars/turn). The
  equal-token-budget control means that length is *not* what's producing the homogenization number —
  which is the whole reason the control exists.
- All values are far above chance (2.2%), so **every model does render characters distinguishably**.
  The question is never "can it?" but "how much did it lose?" — which is why this ships as a **GUIDE**
  (a trend to watch) and not a **GATE** (a bar to clear).

## Provenance

Both metrics are `role=GUIDE` — neither has a measured noise floor, so **neither may block a ship**.
Homogenization ships with its unresolved zh length residual (ρ=+0.264) printed on the number.
Discriminability is length-controlled by construction (equal token budget, train/test split within
character) and has prior art: Miyazaki & Sato (2019), 29 characters, LIBLINEAR.
