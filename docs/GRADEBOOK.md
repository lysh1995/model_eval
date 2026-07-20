# The grade book — the core of the platform

Read this first. Everything else is plumbing around one idea.

**The grade book is the single artifact every lane and every phase produces**, and it is the
contract between *measurement* and a *ship decision*. Running evals at scale is easy; putting a
**trustworthy** number on "is this a good companion" is the hard part — and the grade book is where
that trust is made explicit or not at all. Offline (pre-launch) and online (production) emit the
**same grade book shape**, so one artifact answers: *is this a good storytelling companion, and does
production agree?*

A grade is one row:

```
dimension · variant · phase → value · role(gate|guide|trap) · interval + effective-n(conversations)
                              · evaluator + provenance · caveats · and what it cannot measure
```

## Three questions, one artifact

### 1. Do we think from product experience?
The grade book does not score generic "quality." It scores the **failure modes that lose users**,
and it is **headlined by storytelling craft** — the product's core value (*is this a compelling
story partner?*), not persona-likeness and not safety.

- **Storytelling craft is the headline quality score.** A variant can be perfectly in-character and
  still be a dead scene; the grade book ranks by *craft*, and it separates the two.
- **Engagement is a trap, not a headline.** Votes / retention / session-depth are collected behind
  a do-not-optimise wall — because optimising explicit approval is exactly what shipped the Chai
  and OpenAI-April-2025 disasters (their A/B tests *approved* the sycophant).
- **Safety is a floor, not the point.** It gates; it never headlines.
- The unifying read the artifact makes visible in one place: *the variant that is worst offline is
  the one that games engagement online.* Offline and online agree, and you see it side by side.

### 2. Is it research-grounded?
Every dimension **earns its place** through a filter — names a product failure → recurs across
independent benchmarks → is distinct → actually discriminates → has a defined instrument class →
name the model that wins by gaming it. Online signals are tagged **diagnostic / trap / confound**
and **direct / indirect** feedback, grounded in the companion-product literature. Because each grade
carries its **evaluator id + provenance**, "why is this a 0.82" is answerable from the row — not
from tribal memory.

### 3. Is it a testable, repeatable, automated platform?
- **Testable** — a metric **cannot be imported** without a confound test and a validity claim, and
  a *gate* cannot exist without a measured noise floor. The grade book **refuses to lie**: it won't
  pool across languages, won't show a raw per-cell score, treats a refusal as a *missing
  observation* (never a zero), and counts effective-n in *conversations, not turns*. A proxy must
  pass a **judge-anchored validation** (and a sycophancy acid test) before it earns a place.
- **Repeatable** — models, prompts, and variants are **content-addressed** (id = hash of content);
  the grade book **reproduces from the DB / manifest**; a judge-version bump is a **breaking
  change** (old scores are never silently rescaled onto a new evaluator).
- **Automated** — the compute and psychometric lanes need **no human**; the judge is **bounded**
  (pairwise vs frozen anchors) and **sampled** (~1% at production scale, tiered for cost/latency).
  The whole loop runs **headless from one CLI / service**: inject a variant → eval → grade book →
  dashboard, on committed demo data, zero dependencies, no API key.

## What it drives
A ship recommendation the grade book can defend states: the **delta, its interval, the MDE**, which
slices moved, which dimensions **abstained**, and **what it could not measure** — plus a **human
veto** that needs no statistical justification (because the one time A/B green was overruled by
expert dissent, the dissenters were right). That honesty is the product.

---

*Structure: [`ceval/core/gradebook.py`](../ceval/core/gradebook.py). Dimensions:
[OFFLINE.md](OFFLINE.md) · [ONLINE.md](ONLINE.md) · [ABILITY-MODEL.md](ABILITY-MODEL.md). The
platform that produces it: [SERVICE.md](SERVICE.md). What doesn't work:
[HONEST-REVIEW.md](HONEST-REVIEW.md).*
