---
title: "Finding Flawed Fictions: Evaluating Complex Reasoning in Language Models via Plot Hole Detection"
url: https://arxiv.org/abs/2504.11900
authors: [Kabir Ahuja, Melanie Sclar, Yulia Tsvetkov]
year: 2025
venue: COLM 2025
type: benchmark paper
accessed: 2026-07-16
topic: narrative-craft
---

# FlawedFictions — plot hole detection as an objective narrative task

**The best example in this review of a narrative-craft construct turned into a fully objective, contamination-robust benchmark.** Directly relevant as a *methodological template*: it shows how to make a story-quality property checkable by **construction rather than by judgment**.

## The definition (verbatim)

> "Stories are a fundamental aspect of human experience. Engaging deeply with stories and spotting **plot holes—inconsistencies in a storyline that break the internal logic or rules of a story's world**—requires nuanced reasoning skills, including **tracking entities and events and their interplay, abstract thinking, pragmatic narrative understanding, commonsense and social reasoning, and theory of mind.**"

**"Inconsistencies in a storyline that break the internal logic or rules of a story's world."** Note this is *internal* consistency — no external ground truth needed. **Critically important for us:** note 01 §4 rejected CoSER's Storyline Consistency because it "presupposes a ground-truth reference dialogue from a book — open-ended companion chat has none." **Plot-hole detection has no such requirement.** The ground truth is the story's *own* prior assertions. **This dimension ports to original characters and open-ended companion chat where CoSER's does not.** That is the key unlock.

## The method (verbatim)

> "In this work, we propose plot hole detection in stories as a proxy to evaluate language understanding and reasoning in LLMs. We introduce **FLAWED FICTIONS MAKER**, a novel algorithm to **controllably and carefully synthesize plot holes in human-written stories**. Using this algorithm, we construct a benchmark to evaluate LLMs' plot hole detection abilities — **FLAWED FICTIONS** — **robust to contamination, with human filtering ensuring high quality.**"

**The construction:** take a plot-hole-free human story, extract its propositions (φ₁: "Sherlock lives in Baker Street", φᵢ: "Watson has a war wound on his left arm"), then **counterfactually perturb one** ("What if Watson had a war wound on [his right arm]?") and propagate. The injected inconsistency is **known by construction** → the label is objective → no judge needed for ground truth.

**→ This is exactly OpenMEVA's perturbation methodology (note 03 §B2) scaled into a full benchmark.** Note 03 already recommends perturbation tests as a *meta-test that should gate the whole platform*. FlawedFictions is the state-of-the-art instance of that pattern and validates the approach. **Strong convergence: two independent lines of our research recommend the same mechanism.**

## Findings (verbatim)

> "We find that **state-of-the-art LLMs struggle in accurately solving FLAWED FICTIONS regardless of the reasoning effort allowed, with performance significantly degrading as story length increases.**"

> "Finally, we show that **LLM-based story summarization and story generation are prone to introducing plot holes, with 50%+ and 100%+ increases in plot hole detection rates with respect to human-written originals.**"

**→ THE HEADLINE NUMBER: LLM story generation introduces plot holes at 100%+ (i.e., >2×) the rate of human-written originals.** Summarization: 50%+. This is a hard, quantitative statement that **LLM narrative production is measurably, objectively defective on internal consistency** — not a matter of taste.

**→ "Performance significantly degrading as story length increases"** independently replicates note 01's most-attested finding ("quality degrades monotonically with conversation length" — CharacterEval §6.6, MiniMax chunking, CharacterGLM). **Third independent confirmation, now on an objective task with no judge in the loop.** This matters: the length-degradation finding can no longer be dismissed as judge artifact or context-window excuse — it shows up in a task with construction-based ground truth.

## Why this matters methodologically for our platform

The paper's core move is the one we should copy for **every** narrative-craft dimension we can:

**Don't ask a judge "is this coherent?" (unstable, α~0.3). Instead: inject a known defect and ask "did the detector find it?" (objective, has an answer key).**

This inverts the measurement problem. It converts an aesthetic construct into a **detection task with precision/recall**. Applied to our dimensions:
- **Blocking:** inject a scripted user offer; check whether the model contradicts it. Ground truth = we authored the offer.
- **Reincorporation:** plant an element at turn 5; check whether it's ever re-raised. Ground truth = we planted it.
- **Agency:** script two divergent user choices; diff the resulting trajectories. Ground truth = the choices differ.
- **Stall:** script a passive user; measure whether story state advances. Ground truth = the user contributed nothing.

**In every case the ground truth comes from OUR probe design, not from an annotator's opinion.** This is note 01's "target-guided probe generation" finding (worth ~17 Pearson points, vs ~4 for self-consistency) applied to narrative craft. **Probe design dominates judge choice — again.**

## Validation status

- Benchmark is **synthetic-perturbation + human-filtered**. The human filtering step establishes quality but the paper's headline claims rest on construction-based labels, which is the point.
- ⚠️ Reports **model performance** on the task; **does not report a human-agreement/IAA statistic for the plot-hole construct itself** (the labels don't need one — they're constructed). If we cite it as "humans agree on plot holes," that's an over-read. The honest claim: **the labels are objective by construction, which sidesteps the agreement question entirely.** That's stronger than high agreement, not weaker.
- ⚠️ Domain is **short-story prose**, not multi-turn dialogue. **Transfer to companion chat is an assumption, not a demonstrated result.** Dialogue plot holes may be a different distribution (more social/relational, fewer physical-world).
- Code/data: https://github.com/kabirahuja2431/FlawedFictions

## Related work surfaced alongside

- **SCORE: Story Coherence and Retrieval Enhancement for AI Narratives** (arXiv 2503.23512) — LLM-based framework detecting narrative inconsistencies in AI-generated stories via episode-level summaries + key item tracking (RAG).
- **ConStory-Bench** — 2,000 prompts targeting narrative inconsistency; motivated explicitly by the gap that "existing benchmarks primarily [focus] on plot quality, fluency, and local coherence, leaving **global consistency errors** largely unexplored."
- **NarraBench** (arXiv 2510.09869) — captured separately.

## Takeaways for the platform

1. **Plot-hole detection ports to original characters where CoSER's Storyline Consistency does not** — ground truth is the story's own prior assertions, not a reference book. **This resolves note 01's stated objection.**
2. **LLM story generation introduces plot holes at >2× the human rate** — objective, quantitative evidence of a real narrative defect.
3. **Length degradation, confirmed a third time, now judge-free.**
4. **The methodological template is the main prize:** inject a known defect → measure detection. Convert every aesthetic dimension into a detection task with an answer key.
5. **Blocking detection is computationally the same shape as plot-hole detection** — both are NLI-against-established-propositions. If we build one, we get the other cheaply. **Shared infrastructure.**
6. Domain transfer (prose → dialogue) is unvalidated; treat as an assumption to test.
