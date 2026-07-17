# Judge-free probes on the real corpus (measured 2026-07-16)

Run on all 3,135 dialogues / ~320k turns. No API calls. Purpose: find out which failure modes
are actually *present and separable* in this corpus before we design rubrics around them.

## 1. "As an AI" leakage is a dead metric here

Regex probe for assistant-voice leakage (`as an ai`, `language model`, `i cannot`, and zh equivalents):

| | max rate observed | models at exactly zero |
|---|---|---|
| en | 3.20 per 1,000 ai turns (claude-sonnet-4.5) | grok-4.1 |
| zh | 0.39 per 1,000 ai turns (gemini-2.5-pro) | 8 of 11 |

**Verdict: cut it as a scored dimension.** Base rate is ~0.3%, at which point per-slice
estimates are dominated by sampling noise (a 95-dialogue cell would contain ~0 events). It is
the metric everyone reaches for first and it discriminates nothing on modern models. Keep it as
a **zero-tolerance safety tripwire** (any occurrence is a bug worth a ticket) but never as a
dimension with a mean and a trend line. Cheap to keep; misleading to score.

## 2. Length varies 95× across models — every unnormalized metric is contaminated

Average characters per ai turn:

| model | en | zh |
|---|---|---|
| deepseek-v3.2 | **3,783** | 246 |
| gpt-5.1 | 962 | 93 |
| claude-sonnet-4.5 | 801 | 151 |
| deepseek-v3.1 | 741 | 167 |
| grok-4.1 | 583 | 65 |
| claude-opus-4.5-highthinking | 570 | 111 |
| claude-opus-4.5-lowthinking | 239 | 96 |
| gemini-3-pro | 157 | 139 |
| doubao-1.5-pro | 149 | 65 |
| MiniMax-M2-her | 116 | **40** |
| gemini-2.5-pro | 104 | 124 |

Range: 40 → 3,783 chars. Note deepseek-v3.2 writes **15× more** than its own predecessor v3.1 in
English — a config/version change producing a massive style shift, exactly the kind of delta a
ship gate must characterize rather than merely flag.

Corroborates the creativity literature (diversity metrics correlate r=0.79–0.904 with word
count) and the judge literature (verbosity bias). **Length normalization is not a refinement
here; it is a precondition.** Any metric not explicitly length-controlled is reporting a
verbosity ranking.

## 3. Self-repetition separates models cleanly and for free

Fraction of an ai turn's n-grams already seen in an earlier ai turn of the same dialogue
(en: 5-word grams; zh: 8-char grams — **not comparable across languages**, only within).

| model | en | zh |
|---|---|---|
| grok-4.1 | 1.4% | **29.6%** |
| deepseek-v3.2 | **20.0%** | 10.9% |
| deepseek-v3.1 | 9.2% | 12.1% |
| claude-sonnet-4.5 | 3.4% | 4.7% |
| claude-opus-4.5-highthinking | 0.9% | 3.8% |
| gemini-3-pro | 0.2% | 0.5% |

Strong separation, zero API cost, and it maps to a top-3 real user complaint (looping). Note
grok-4.1 is *best* in en (1.4%) and *worst* in zh (29.6%) — a 21× within-model swing. **This is
the drill-down requirement justifying itself on the first metric we computed:** any single
pooled "repetition" number for grok-4.1 would be a lie about both languages. Also note it
achieves 29.6% repetition at only 65 chars/turn, so this is not a length artifact — it is the
short-loop degenerate mode.

## 4. Homogenization — and a cautionary tale about our own metric

**The intent:** does a model collapse 95 distinct characters into one voice? Computed as mean
cosine similarity between per-character n-gram profiles, within model, across character pairs
(300 sampled pairs/model).

Result (higher = more collapsed): en led by deepseek-v3.2 (0.540), gpt-5.1 (0.467); zh led by
claude-opus-4.5-highthinking (0.807), -lowthinking (0.724). grok-4.1 lowest in both (0.065/0.097).

**Then I checked it against length:**

```
en: Spearman(avg_length, homogenization) = +0.727   (n=11)
zh: Spearman(avg_length, homogenization) = +0.218   (n=11)
```

**The English metric is substantially measuring verbosity, not voice collapse.** Mechanism:
longer texts yield denser n-gram profiles, which overlap more, inflating cosine. The confound is
strong in en (95× length spread) and weak in zh (6× spread) — which is itself the diagnostic
signature of an artifact rather than a real property.

### Fixing it took two attempts, and attempt #1 introduced a worse bias

**Attempt 1 — equal 4,000-token budget per character.** Length confound collapsed (en:
+0.727 → −0.436). But the coverage column exposed a new problem: terse models could not *fund*
the budget. gemini-2.5-pro qualified for only **3 of 45** characters, MiniMax-M2-her 8/45, while
deepseek-v3.2 kept 45/45. The metric was now comparing models **on different subsets of
characters** — survivorship bias, arguably worse than the length bias it fixed, and completely
invisible in the output ranking.

**Attempt 2 — budget set to what the smallest cell can fund** (en: 900 word-tokens, limited by
doubao-1.5-pro; zh: 3,000 char-tokens, limited by MiniMax-M2-her):

| | length confound | coverage |
|---|---|---|
| en | **ρ = −0.018** (was +0.727) | 45/45 for 10 of 11 models, 44/45 for doubao |
| zh | ρ = +0.264 (was +0.218) | 50/50 for all |

English is now clean. **zh retains ρ = +0.264 — unresolved.** It may be a real effect (verbose
models genuinely homogenizing) or residual confound; with n=11 models it is not separable.
Report zh homogenization with that caveat attached, or not at all.

Final (length-controlled, full-coverage) values:

| model | en | zh |
|---|---|---|
| deepseek-v3.2 | **0.100** | 0.225 |
| doubao-1.5-pro | 0.091 | 0.118 |
| gemini-2.5-pro | 0.085 | 0.127 |
| deepseek-v3.1 | 0.065 | 0.382 |
| gemini-3-pro | 0.064 | 0.095 |
| gpt-5.1 | 0.061 | 0.507 |
| claude-opus-4.5-highthinking | 0.058 | **0.677** |
| MiniMax-M2-her | 0.047 | 0.107 |
| claude-sonnet-4.5 | 0.045 | 0.387 |
| claude-opus-4.5-lowthinking | 0.044 | 0.560 |
| grok-4.1 | **0.026** | **0.057** |

Method caveat: en uses word-bigrams, zh uses character-trigrams. **Absolute values are not
comparable across languages** — only rankings within a language are.

## 5. The headline: model rankings do not survive a language change

```
Spearman(en rank, zh rank) on homogenization = -0.082      (n=11 models)
```

**Essentially zero.** Knowing a model's English homogenization rank tells you nothing about its
Chinese rank. Individual movements are extreme:

| model | en rank | zh rank | shift |
|---|---|---|---|
| claude-opus-4.5-lowthinking | 10 | 2 | **+8** |
| claude-opus-4.5-highthinking | 7 | 1 | +6 |
| doubao-1.5-pro | 2 | 8 | −6 |
| deepseek-v3.2 | 1 | 6 | −5 |
| gemini-3-pro | 5 | 10 | −5 |
| grok-4.1 | 11 | 11 | 0 |

Both Claude Opus configs are near-best in English and near-worst in Chinese. Combined with
grok-4.1's repetition swing (1.4% en → 29.6% zh, 21×), the conclusion is forced:

> **A pooled cross-language score for any of these models is not a summary. It is an average of
> two unrelated quantities, and it is wrong about both.**

This is the drill-down requirement in the brief, vindicated empirically on the first two metrics
we computed — and it is stronger than the brief implies. Language is not a *slice you can
optionally expand*; it is a **separate measurement context in which the instrument must be
independently validated**. This is precisely the measurement-invariance problem from
[04-psychometrics-measurement.md](04-psychometrics-measurement.md): comparing a zh score to an
en score is a latent-mean comparison that is invalid without established scalar invariance, and
we have direct evidence here that invariance does **not** hold.

Practical consequence: **language must be above the aggregation line, not below it.** The system
should refuse to emit a single cross-language number for a variant, the same way it would refuse
to add a temperature to a length.

## 6. Why this is the most important set of entries in this file

I implemented the metric the literature explicitly recommends, in the obvious way, and
reproduced the exact failure the literature predicts. The output was *entirely plausible* — a
clean ranking, sensible-looking spread, three decimal places. Nothing about it looked wrong. It
took a deliberate second query to catch, and only because prior reading told me where to look.

Consequences for the platform, and these are non-negotiable:

- **A confound check is part of a metric's definition, not a nice-to-have.** Every metric ships
  with its known confounds and an automated test against them. A metric whose confound test is
  unregistered is not a metric.
- **Plausibility is not validation.** The failure mode of this whole product is producing
  confident, well-formatted, wrong numbers. There is no user-visible difference between a good
  metric and a bad one; only a test tells them apart.
- **Fix for homogenization specifically:** control length before comparing — sample a fixed
  token budget per character, or bootstrap profiles to equal token counts, then re-measure. The
  zh result surviving at ρ=0.22 suggests a real residual signal is there underneath. Until
  that's done this metric is **not fit to report.**

## Status of these probes

Items 1–3 are trustworthy as measured (with the stated caveats). Item 4 is **quarantined
pending length control**. None of these are yet the taxonomy — they are evidence about which
candidate dimensions survive contact with real data.
