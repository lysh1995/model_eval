# Did the user simulator see the character card? (2026-07-16)

Reproduce: [`scripts/card_awareness_audit.py`](../../scripts/card_awareness_audit.py) (v1),
[`scripts/card_awareness_audit2.py`](../../scripts/card_awareness_audit2.py) (v2)

## Why this matters

Stream 8 flagged it as **a bigger threat to validity than off-policyness itself**. If the dataset's
user turns were generated *with* card access, the simulator is a **collaborative partner, not a
user**. A collaborator knows who the character is and plays along; **it does not probe the seams.**
That systematically **under-detects drift**, biasing every consistency metric in the catalogue —
C1, C4, S5, and the whole L2 layer of [ABILITY-MODEL.md](../../docs/ABILITY-MODEL.md).

It also bears directly on the brief's premise that these user turns are "replayable user traffic."
Traffic from a collaborator is not traffic.

## v1 — and its two defects

Compared own-card term leakage into user turns against a **random other card**:

| | en | zh |
|---|---|---|
| own-card leak | 0.1098 | 0.0365 |
| random-card control | 0.0595 | 0.0218 |
| lift | **1.84×** | **1.68×** |
| paired permutation p | <0.0001 | <0.0001 |

**Two problems, one a bug and one a confound:**

1. **Bug:** the first user turn is `initial_user_input`, taken **verbatim from the seed**. It is
   card-derived *by construction*. v1 counted it.
2. **Confound — topic.** The card says *scalpel*; the AI says *knife*; the user says *scalpel*
   because they are in a hospital. A **random** other card is a different topic entirely, so v1's
   lift may be measuring topic-relatedness rather than card access.

## v2 — precedence + topic-matched control

Fixes: drop the scripted first turn; control with the **nearest-neighbour card** (highest Jaccard
overlap) instead of a random one; and add the decisive test — **temporal precedence**: count card
terms the user utters at turn *t* that the AI has **not said at any turn < t**. A card-blind
simulator can only learn the character from what the AI has already said.

| | en | zh |
|---|---|---|
| own card | 0.00681 | 0.00174 |
| topic-matched control | 0.00430 | 0.00117 |
| lift | **1.59×** | **1.48×** |
| paired permutation p | <0.0001 | <0.0001 |
| **control quality — Jaccard(own, nearest)** | **0.058** | **0.034** |

## Verdict: suggestive, NOT conclusive — and the reason is in that last row

The effect survives the bug fix, the precedence test, and a nominal topic control, in both
languages, at p<0.0001. **But the topic control is weak.** A Jaccard of **0.058** means the
"topic-matched" card shares ~6% of its terms with the target — that is not a matched control, it is
**the least-different card in a set of very different cards**. The characters are simply too
heterogeneous for nearest-neighbour matching to hold topic fixed.

So the honest statement: **there is a consistent, highly significant own-card advantage that topic
does not obviously explain — but has not been shown *not* to explain either.** The absolute effect
is also small (0.68% vs 0.43% of unrevealed card terms), though it is a rate over a large
denominator and significance is not the issue here; **confounding is.**

## The decisive follow-up (cheap, offline, not yet run)

**Restrict to proper nouns and rare specifics** — the character's sister's name, a specific street,
an invented place. **Topic cannot explain a proper noun.** If the user utters the character's
sister's name before the AI ever mentions it, that is card access, full stop; there is no
"they were both talking about family" explanation.

This is the right experiment and it is a small change to v2 (swap the term extractor for a
capitalized-token/NER filter, en; a name-list filter, zh). **Do this before trusting any drift
metric derived from this corpus.**

## What to do in the meantime

- **Treat the corpus's drift measurements as a lower bound.** If the simulator is collaborative, real
  users — who *don't* know the card and *do* poke at inconsistencies — will surface more drift than
  we measure here.
- **Our own user simulator must be card-blind by construction**, and that should be an explicit
  property of the instrument, versioned with it. The temptation to give the simulator the card
  ("so it stays on topic") is exactly the thing that would quietly destroy the metric.
- This does **not** invalidate the replay design ([00](00-dataset-ground-truth.md)) — replaying the
  user half stays defensible. It bounds what the replayed corpus can tell us about **drift
  specifically**.

## Method note

Both versions use a **paired permutation test** (sign-flip on paired differences, 20k draws),
per the standing rule from [15](15-l1-convergent-reading.md): *never hand-roll a statistic when a
permutation test will do.* No p-value here came from a closed-form approximation.

**And v1→v2 is the pattern repeating for a fourth time today:** a plausible, highly significant
result (1.84×, p<0.0001) that contained a construction bug *and* an uncontrolled confound. v2 is
better and is *still* not clean. **The finding survived every check I ran; it has not survived
every check that matters.**
