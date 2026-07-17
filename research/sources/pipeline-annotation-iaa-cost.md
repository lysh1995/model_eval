---
title: "Human annotation infrastructure — IAA, calibration sets, queues, cost"
url: https://futureagi.com/blog/llm-as-judge-best-practices-2026
org: Future AGI / Label Studio / composite
year: 2026
type: engineering-blog-composite
accessed: 2026-07-16
topic: eval-lifecycle
---

# Human-in-the-loop annotation infrastructure

Composite of:
- https://futureagi.com/blog/llm-as-judge-best-practices-2026
- https://futureagi.com/blog/human-vs-llm-annotation-2025/
- https://labelstud.io/videos/in-the-loop-what-is-agreement/
- https://atlan.com/know/data-labeling-best-practices-llms/
- https://risedatalabs.com/blog/inter-annotator-agreement

⚠️ **Source quality caveat: this is vendor-blog consensus, not peer-reviewed.** The numbers
below are industry rules-of-thumb. Where they conflict with our own measurements
(notes 01/02/10), **our measurements win** — see the sharp conflict flagged below.

## Calibration set sizing (industry rule of thumb)

- **200–500 hand-labeled traces per workload per rubric**
- Each trace labeled by **2–3 humans** against the rubric
- **Inter-annotator agreement (Cohen's κ) tracked** as a first-class number
- The gold set is "the calibration anchor"

## The κ thresholds everyone quotes

| κ | Interpretation |
|---|---|
| **> 0.80** | strong agreement |
| **0.60 – 0.80** | substantial |
| **< 0.60** | "needs rubric work" |

> ### ⚠️ These thresholds are unreachable for our task, and that is the most important thing
> ### on this page.
>
> Note 01: human raters agree on roleplay **quality** at Krippendorff α = **0.25–0.34**.
> Note 11: the chance-corrected judge ceiling is **κ ≈ 0.53**.
>
> **Both are "below 0.60 → needs rubric work" by the industry rule.** But no amount of
> rubric work will fix them, because the disagreement is **in the construct, not the
> instrument** — Amabile's CAT establishes that experts only achieve reliability rating
> creativity *relatively within a set*, and note 11 §6 notes ~19% of items are *irreducibly*
> contested.
>
> **Consequence: we must publish our own agreement bar and defend it, because the industry
> default would tell us to keep polishing a rubric forever.** A team that adopts κ>0.8 as a
> gate for a companion-quality rubric will burn a year and never ship. The correct response
> to α=0.25–0.34 is **not** a better rubric — it's to *stop asking the question that way*
> (note 11's whole thesis: decompose until the objective part falls out, go pairwise for the
> residue, and abstain on the contested ~19%).
>
> Where κ>0.8 *is* achievable and *should* be demanded: our **Lane 0/Lane 1** bounded tasks
> — safety autofails, format violations, assistant-voice leak. Those are the "bounded task,
> high reliability" cells in note 11's lane table. **Apply the industry bar to bounded
> tasks; refuse it for creative-quality tasks.** Same platform, two different bars, stated
> explicitly.

## Agreement metrics — which to use

- **Cohen's κ** — two annotators
- **Krippendorff's α** — more than two annotators (and handles missing data / any
  measurement level) ← what note 01 uses
- Always chance-corrected; never raw percent agreement (note 11 §7)

## Queue design (industry consensus)

- **Active learning** — "prioritize examples where the LLM judge is uncertain"
- **Reviewer roles** — junior labeler → senior reviewer
- **Disagreement resolution** step
- κ and per-rubric agreement **exposed in the labeling queue** itself
- "compare a new judge prompt to the labeled set in one call"

## Cost/efficiency practice

> "you might assign **at least two annotators to 20% of the tasks** to balance quality and
> efficiency — especially on straightforward tasks"

I.e. **double-label a 20% subsample to estimate κ; single-label the rest.** κ is estimated
from the overlap, not from the whole set.

> **This is the realistic answer to "how much human labeling is affordable."** Double-labeling
> everything doubles cost for a number you only need a *confidence interval* on. Our
> Tier 3 (note 06) is 5k/day — double-labeling 20% of a much smaller human tier is
> tractable.

## Judge calibration as table stakes

> "Calibration has moved from 'nice to have' to **table stakes**, with production teams now
> **computing Cohen's κ between judge and a labeled human sample before shipping any new
> rubric**, and **re-sampling monthly to catch judge drift**."

> Confirms note 11 §8 (judge version is a breaking change) and note 06 §7 (frozen golden set
> re-scored on every evaluator bump), from the practitioner side. **"Re-sample monthly" is
> the cadence claim; we can do better** — note 06 §7's golden-set re-score runs on *every*
> evaluator bump, which is event-driven rather than calendar-driven, and strictly better.

## LLM vs human annotator agreement

> "Inter-annotator agreement among LLMs, as well as their alignment with expert annotations,
> are **significantly higher than that of crowd workers**, with GPT-4 and PaLM2 achieving
> **κ scores above 0.70**, approaching expert-level agreement after reconciliation."

> ⚠️ **Do not port this number.** It is from *classification-style* annotation tasks
> (hostility, topic, sentiment) — bounded, objective-ish. Note 02/03 measure the same class
> of models at **r=0.159 / 40% consistency** on *absolute creativity* and κ≈0.53 chance-
> corrected on preference. **The κ>0.70 figure is a fact about easy tasks, not about GPT-4.**
> The relevant lesson is the *comparative* one — **LLM judges beat crowd workers** — which
> matters for us: it means "just hire crowd annotators" is not a way out of the reliability
> problem. Our human tier must be **expert/trained annotators on a small calibration set**,
> not crowd volume. That is a hiring and rubric-training cost, not a marketplace spend.
