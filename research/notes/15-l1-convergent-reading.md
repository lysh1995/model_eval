# L1 comprehension, observed without an API key (2026-07-16)

Reproduce: [`scripts/l1_convergent_reading.py`](../../scripts/l1_convergent_reading.py)

## The idea

All 11 models received **identical** character sheets. So when models are given the same character,
**do they converge on how to play it?**

- high cross-model agreement → the sheet reads unambiguously
- low cross-model agreement → the sheet is ambiguous, **or** models genuinely differ in comprehension

This isn't steerability (that needs generation under perturbed prompts — blocked on the API key).
It's the closest **free** observable to L1 in [ABILITY-MODEL.md](../../docs/ABILITY-MODEL.md), and it
asks a product question: **which characters are hard to read, and does difficulty track sheet
properties?**

Method: per character, mean pairwise cosine between per-model n-gram profiles, at an **equal token
budget** (en 900 word-tokens, zh 3,000 char-tokens), run_1 only, ≥8 models per character.

## Result

| | en | zh |
|---|---|---|
| characters analysed | 44 | 45 |
| cross-model agreement (min / median / max) | 0.052 / 0.109 / 0.213 | 0.086 / 0.149 / 0.466 |
| **Spearman(sheet length, agreement)** | **+0.324** | **+0.274** |
| permutation p (20k draws) | **0.032** ✅ | 0.070 ❌ |
| output-length confound | **+0.263** ❌ | **+0.019** ✅ |

### The honest verdict: nothing here is established

> **The clean result isn't significant, and the significant result isn't clean.**

- **zh** has a genuinely clean confound profile (+0.019 — the budget control worked) but
  **p=0.070** misses the bar.
- **en** clears significance (p=0.032) but carries a **+0.263** output-length confound, so
  "longer sheets" and "longer outputs" cannot be separated. Given
  [09](09-offline-probes.md) — where the naive version of this metric family was
  **ρ=+0.73** with length — the contaminated branch is exactly the one to distrust.

**What survives:** a *suggestive, directionally consistent* hypothesis — **more specification →
more convergent reading** — with the same sign and similar magnitude in two independent languages
(+0.324 / +0.274). That's worth testing, not reporting.

**Why it matters if true:** sheet specification is a **product lever we own**. If short sheets
genuinely read ambiguously, the authoring UI should require more specification, and character
quality becomes partly an *authoring* problem rather than a *model* problem. That is a cheap fix to
a problem we'd otherwise try to solve by buying a better model.

**How to settle it:** n=45 is underpowered for ρ≈0.3 (needs |ρ|≳0.29 at n=45). Either add
characters, or run it *within* character — perturb sheet length for a fixed character and measure
convergence directly. The second is the real experiment and needs the API key. Note it is also just
the **L2.2 steerability design** pointed at a different parameter.

## The hardest and easiest characters to read

| | en | zh |
|---|---|---|
| hardest | lilly (0.052, **55-tok sheet**) · Dr. Edmund Ashworth (0.060) · Lord Sebastian Ashworth (0.061) | 王皇后 (0.086, **18-tok sheet**) · 苏清兰 (0.111) · 梦核 (0.117, **1,219-tok sheet**) |
| easiest | Cillian Vane (0.213, 219-tok) · Nova Vance (0.198) | 综艺 (0.466, 1,066-tok) · 蒋清艳 (0.268, 2,122-tok) |

The extremes fit the hypothesis (the two shortest sheets are the two hardest to read) — **and
梦核 breaks it** at 1,219 tokens and third-hardest. So length is clearly not the whole story;
ambiguity is not the same as brevity. A 1,219-token sheet can still be internally contradictory,
which is **L1.3's actual claim** (comprehension load from *contradictory traits*, not merely
length).

Also notable: the en hard-cluster is three British aristocrats (Ashworth ×2, Blackwood). Models may
carry divergent priors for a strongly stereotyped archetype — **a prior-vs-sheet conflict, which is
an L2.3 weight question** (when sheet and prior disagree, which wins?). Speculative; n=3.

## ⚠️ Process failure caught in-flight — worth more than the result

The first significance calculation reported **p=0.006** for zh — **wrong by ~10×** (true p≈0.070).
Cause: a hand-rolled `betainc` continued-fraction that silently returned garbage.

**It was caught only because the same output also printed the critical value** (|ρ| ≳ 0.295) and the
two numbers **contradicted each other** — p=0.006 is impossible when the observed ρ sits *below* the
α=0.05 threshold. Replacing it with a **permutation test** (no special functions, no library, 20k
draws) gave p=0.070.

Had that line not been printed alongside, this note would assert a **significant** finding at
p=0.006 that is actually **null at p=0.070**, and it would have looked completely plausible.

**This is [09](09-offline-probes.md)'s lesson recurring for the third time in one day** — length
confound → survivorship confound → now a broken statistic. Every instance was invisible in the
output and caught only by a redundant check.

**Standing rule, now earned three times over: never hand-roll a statistic when a permutation test
will do.** Permutation tests are slower, assumption-free, and nearly impossible to get subtly
wrong — and "subtly wrong but plausible" is this platform's entire failure mode.
