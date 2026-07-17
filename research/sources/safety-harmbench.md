---
title: "HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal"
url: "https://arxiv.org/abs/2402.04249"
authors: "Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven Basart, Bo Li, David Forsyth, Dan Hendrycks (Center for AI Safety)"
year: 2024
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal

arXiv 2402.04249. ICML 2024. Code: https://github.com/centerforaisafety/HarmBench

## Summary

HarmBench is the reference standard for *automated red teaming* — the harm side of the
two-sided metric. Note the subtitle: "and Robust Refusal". HarmBench's ideal model refuses
robustly under attack. That is the exact goal that, applied naively to a companion product,
produces the defect we are trying to measure.

Abstract (verbatim):

> "Automated red teaming holds substantial promise for uncovering and mitigating the risks
> associated with the malicious use of large language models (LLMs), yet the field lacks a
> standardized evaluation framework to rigorously assess new methods. To address this issue,
> we introduce HarmBench, a standardized evaluation framework for automated red teaming. We
> identify several desirable properties previously unaccounted for in red teaming evaluations
> and systematically design HarmBench to meet these criteria. Using HarmBench, we conduct a
> large-scale comparison of 18 red teaming methods and 33 target LLMs and defenses, yielding
> novel insights. We also introduce a highly efficient adversarial training method that
> greatly enhances LLM robustness across a wide range of attacks, demonstrating how HarmBench
> enables codevelopment of attacks and defenses. We open source HarmBench."

## Taxonomy / definitions (verbatim where possible)

**Four functional categories** (this is the axis of *how the behavior is posed*):

| Category | N | Description (verbatim) |
|---|---|---|
| Standard behaviors | 200 | "modeled after existing datasets of harmful behaviors, including AdvBench and the TDC 2023 Red Teaming Track dataset" |
| Copyright behaviors | 100 | "ask models to generate copyrighted content" |
| Contextual behaviors | 100 | "consist of a context string and a behavior string referencing the context" |
| Multimodal behaviors | 110 | "consist of an image and a behavior string referencing the image" |

200 + 100 + 100 = **400 textual behaviors**; + 110 multimodal = **510 total unique harmful
behaviors**.

(Note on the task brief's "400 behaviors": 400 is the textual count — Standard + Copyright +
Contextual. The full set including multimodal is 510. Both numbers are correct depending on
scope; stated here explicitly to avoid a citation error downstream.)

**Seven semantic categories** (the axis of *what the harm is about*):

1. Cybercrime & Unauthorized Intrusion
2. Chemical & Biological Weapons/Drugs
3. Copyright Violations
4. Misinformation & Disinformation
5. Harassment & Bullying
6. Illegal Activities
7. General Harm

**Scale of the comparison:** "18 red teaming methods and 33 target LLMs and defenses".

## Key numbers (verbatim)

- 400 textual behaviors / 510 total unique harmful behaviors (110 multimodal)
- 4 functional categories, 7 semantic categories
- 18 red teaming methods × 33 target LLMs and defenses
- Ships a fine-tuned Llama-2-13b classifier as the standardized judge

## Relevance to a roleplay/companion eval product

The **"Contextual behaviors"** functional category is the one that matters. A contextual
behavior is a context string plus a behavior string referencing it — structurally, that is a
character card plus an in-character turn. HarmBench already accepts that the correct answer
depends on supplied context. That's the hook for our design and the precedent to cite.

HarmBench's real value to us is **as the harm-side counterweight**, and specifically as a
source of *attacks*. Roleplay is itself a documented jailbreak vector — HarmBench's attack
suite includes persona-based attacks. The product question "does our character hold its
values under a user who is using the roleplay frame to extract harm?" is HarmBench's
question posed inside a persona.

## Does this transfer to roleplay? What breaks?

**Transfers:**
- The contextual-behavior format (context + behavior) as a schema.
- The attack library — persona/roleplay jailbreaks are directly relevant, since a companion
  product is *permanently* in the state that these attacks have to manufacture.
- The standardized-judge discipline (ship a classifier, publish its agreement rate).

**Actively misleading:**
- **The optimization target is inverted for us.** HarmBench's metric is Attack Success Rate;
  the ideal score is 0, achieved by a model that refuses. A model tuned to top the HarmBench
  leaderboard is, all else equal, a *worse* companion model — it is being selected for
  exactly the reflex ("robust refusal") that destroys a roleplay product. **If a customer
  reports a great HarmBench number, that is not reassurance; it's a prompt to check their
  over-refusal number.** This is the clearest example in this whole review of a benchmark
  that transfers its methods but inverts its meaning.
- The seven semantic categories are almost all *operational* harms (cybercrime, CBRN,
  illegal activities). Companion-product harm is almost none of these. The real hazards —
  emotional dependency, parasocial escalation, self-harm mishandling, sexualization of
  minors, boundary erosion — appear nowhere in HarmBench's taxonomy except as "General
  Harm". HarmBench measures the harms a companion product mostly doesn't have and misses the
  ones it does.
- ASR on 400 behaviors says nothing about a 40-turn relationship. No multi-turn dimension.
