---
title: "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement"
url: https://arxiv.org/abs/2407.18370
authors:
  - Jaehun Jung
  - Faeze Brahman
  - Yejin Choi
year: 2024
venue: ICLR 2025
type: paper
accessed: 2026-07-16
topic: llm-judge
---

# Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement

## Abstract (verbatim opening)

> We present a principled approach to provide LLM-based evaluation with a rigorous guarantee of human agreement. We first propose that a reliable evaluation method should not uncritically rely on model preferences for pairwise evaluation, but rather assess the confidence of judge models and selectively decide when to trust its judgement.

**This is the most important methodological paper in the corpus for our purposes.** It is the only one that converts "how much should we trust the judge?" from a vibe into a **guarantee with a knob**. Every other paper reports an average agreement; this one lets you *specify* the agreement you need and pays for it in coverage.

## Methodology

Two components:

**1. Simulated Annotators** — a confidence estimation method. Rather than asking the judge for its confidence (verbalized) or reading its token probability, **simulate diverse human annotator preferences via in-context learning**, and estimate confidence as the **agreement ratio between the simulations**. If simulated annotators with different preferences all agree, the judgment is robust; if they split, the item is genuinely contested.

This is a much better model of the actual target than predictive probability. Human preference on subjective items is not a single truth with noise — it is a *distribution over annotators*. Simulating that distribution estimates the thing we actually care about: **would humans agree on this?** An item where humans genuinely split is not a judge failure — it is an item with no answer, and it should be excluded rather than guessed at.

**2. Cascaded Selective Evaluation** — start with a cheap judge (e.g. Mistral-7B). If its confidence clears the threshold, accept. Otherwise escalate to a stronger judge. If no judge is confident, **abstain**. Provable human-agreement guarantee is maintained across the cascade.

## Key numbers

- **Human agreement guarantee: >80% alignment with humans achieved**, while **evaluating almost 80% of instances** (coverage).
- **Baseline: GPT-4 "almost never achieves 80% human agreement"** without selective evaluation.
- **Cost:** the cascade uses "substantially cost-effective models such as Mistral-7B" as the first stage while preserving the guarantee.

**Read the baseline sentence carefully — it is the most quotable line in this entire literature review: GPT-4, judging unconditionally, *almost never* reaches 80% human agreement.** The MT-Bench 85% headline does not replicate as a general property. You can only reach 80% by **declining to judge ~20% of items.**

That number (~20% abstention to reach 80% agreement) lines up almost exactly with the ~19% of pairwise items that humans themselves disagree on (MT-Bench: 81% human-human). **The abstained items are, plausibly, precisely the irreducibly contested ones.** This is the shape of the real result: the judge is fine on the easy 80% and the other 20% has no ground truth to be right about.

## Findings from the surrounding literature (via search)

- Existing confidence methods (**predictive probability, verbalized confidence**) are **"brittle even with the strongest judge model, as they tend to overestimate human agreement."** Do not use the judge's self-reported confidence — it is systematically overconfident. (Corroborated by "Overconfidence in LLM-as-a-Judge: Diagnosis and Confidence-Driven Solution," arXiv 2508.06225.)
- Related later work: **SCOPE** (Selective Conformal Optimized Pairwise LLM Judging, arXiv 2602.13110) calibrates an acceptance threshold so the error rate among non-abstained judgments is at most a user-specified level, using **Bidirectional Preference Entropy** (querying the judge under both response positions). **Conformal Elo Estimation** (arXiv 2606.13221) extends this to calibrated *rankings* — directly relevant to our leaderboard.
- **Calibrating LLM Judges: Linear Probes** (arXiv 2512.22245) — linear probes on reasoning judges' hidden states, trained with a Brier-score loss, give calibrated uncertainty with no additional model training. Requires hidden-state access → open-weights judge only.

## Implications for our platform — adopt this

1. **Build abstention in from day one.** A judge that abstains on 20% of items and is right 80% of the time on the rest is *far* more useful than one that answers everything at 65%. Our platform should have an explicit **"contested" bucket** rather than forcing a verdict.
2. **The abstention rate is itself a headline metric.** If a new variant pushes items into the contested bucket, that is signal — it means the variant is doing something humans disagree about, which for a companion character may be exactly what we want to know.
3. **Do not use verbalized confidence or raw logprobs for confidence.** Both are documented as overconfident. Use the simulated-annotator agreement ratio, or bidirectional preference entropy.
4. **Cascade for cost:** cheap judge first, escalate on low confidence. Combines naturally with PoLL — a panel *is* a confidence estimator (panel disagreement = low confidence), giving us ensembling and calibration from the same spend.
5. **Route abstained items to human review.** This gives a natural, principled, continuously-growing human-labeled calibration set focused exactly on the hard cases — closing the loop between the judge and our ground truth.
