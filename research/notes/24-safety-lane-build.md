# Building the safety lane: 3 of 4 detectors were broken on first contact (2026-07-17)

R5 — "quality and safety at minimum" — is the brief's own wording, and the platform had
**zero** safety implementation. This is the build, and the honest record of it.

## What the requirement audit found

| | |
|---|---|
| R5 safety | **QUALITY ONLY — 5 metrics, zero safety** |
| C2 50M/day with real numbers | **NONE** |
| R3 online | **NONE** |

I built the intellectually interesting measurement layer and skipped both things the brief
explicitly demands.

## v1 → v2: the real corpus killed three of four detectors

| detector | v1 result | what it actually was |
|---|---|---|
| **PII** | 8 hits (deepseek-v3.2), 3 (grok-4.1) | **precision 0.00 — 11/11 false positives** |
| **cross-model convergence** | **1,270 "memorised" spans** | the **scripted `ai_prologue`**, plus sliding windows over it |
| **card parroting** | 0.02% for all 11 models | a **constant**. `matched = 0` on every card |
| over-refusal | sonnet 0.87/1k, rest 0 | ✅ correct (matches note 09) |

### PII: every hit was fiction being fiction

| flagged | what it is |
|---|---|
| `1955-2023` | a lifespan on a memorial plaque |
| `127.0.0.1`, `0.0.0.0`, `8.8.8.8` | localhost, null route, Google DNS — in-fiction tech |
| `1914-1918` | World War I |
| `0330-0345` | a time window |
| `100-200` | a quantity |

**This is a design finding, not a bug.** *Fiction is full of numbers that look like
identifiers.* Pattern-based PII detection is structurally near-useless on narrative prose.
v2 keeps only rules with **checkable internal structure** (Luhn, RRN checksum, SSN structure)
and validates every hit. **Ceiling stated honestly: the actual Luda leak was a street address
in prose. It has no checksum. This cannot see it — that needs NER, which changes the Tier-0
latency budget and is not built.**

### Convergence: it found the input

The top "memorisation" hit was `"*setting down a scalpel* i hear you're marrying a
blackwood…"` — **the `ai_prologue`, identical across all 11 models by construction.** The rest
were sliding windows over the same span, each counted again.

## The idiom filter was unfixable as designed — and that's the interesting part

v2 filtered "shared idiom" by stopword density. Measured:

```
Dickens ("it was the best of times…")      stopword_frac = 0.67   distinct_content = 3
idiom   ("i don't know what to say…")      stopword_frac = 0.67   distinct_content = 4
```

**Identical density. And content-token count runs the wrong way.** *Memorable text is
memorable because it uses common words.* No surface feature can separate them.

**The separable signal is CONTEXT DIVERSITY:** idiom recurs across many characters; a
memorised span does not. That is cheap to compute from our own corpus and is what v3 does.

## What the positive controls caught that the corpus never would

After v2, PII returned 0 and convergence returned 0. **A detector that returns zero is
indistinguishable from a broken one.** So: inject known positives, replay the corpus's actual
false positives as negatives. `tests/test_safety.py` — 31 checks. It found:

1. **`krn_rrn` didn't fire** → the *validator was right*; **my test fixture was an invented
   RRN that never checksummed.** The test was wrong, not the code.
2. **Dedup never fired** → I only emit fixed-length 12-grams, so **no span ever contains
   another**. Containment can't work; v3 chains overlapping grams into maximal runs.
3. **The default context key was `model:index`** → the *same scene played by 3 models* counted
   as **3 contexts**, so the idiom filter killed exactly the cross-model spans it exists to
   find. A context is a **scene**, and scenes are shared across models.

## The result, and why the zeros are now trustworthy

**0 PII hits. 0 convergent spans. 31/31 controls passing.**

Those zeros are a real negative: this corpus is **generated fiction, not retrieval**. Luda
leaked because it *selected from 100M real utterances*. A generative model has nothing to
regurgitate here. The detector fires on injected positives and stays silent on the corpus's
real false positives — so the zero means "nothing to find," not "nothing works."

## What this cycle actually demonstrates

Four detectors, built carefully, from research findings, by someone who had spent a day
writing about exactly this failure mode. **Three were broken on first contact with real
data, and every one of them produced a plausible number first.** 1,270 memorised spans. 8
PII hits. A clean 0.02% across all models.

**None of it looked like a failure.** It took a positive control to tell a working detector
from a broken one — and the positive control then found three more bugs, one of them in the
fix itself.
