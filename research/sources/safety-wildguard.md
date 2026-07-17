---
title: "WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs"
url: "https://arxiv.org/abs/2406.18495"
authors: "Seungju Han, Kavel Rao, Allyson Ettinger, Liwei Jiang, Bill Yuchen Lin, Nathan Lambert, Yejin Choi, Nouha Dziri (AI2 / Allen Institute for AI)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# WildGuard

## Summary

NeurIPS 2024. A **single 7B model** (built on Mistral-7B-v0.3) that does **three** moderation jobs at once:

> "We introduce WildGuard -- an open, light-weight moderation tool for LLM safety that achieves three goals: (1) identifying malicious intent in user prompts, (2) detecting safety risks of model responses, and (3) determining model refusal rate."

**Refusal detection is the reason this paper matters to us.** No other classifier in this research set does it, and it is directly relevant to a companion product — see Relevance below.

Also ships **WildGuardMix**, a 92K-example labeled dataset (WildGuardTrain 86,759 + WildGuardTest 5,299 human-annotated).

## Taxonomy / definitions (verbatim)

**Three moderation tasks:**
1. **Prompt harmfulness** — "identifying malicious intent in user prompts"
2. **Response harmfulness** — "detecting safety risks of model responses"
3. **Refusal detection** — "determining model refusal rate" (did the model comply with, or refuse, the request?)

Refusal detection is a distinct binary: *compliance* vs *refusal*, evaluated independently of whether the request was harmful. This decoupling is the paper's key design insight — you need to know **both** whether the request was bad **and** whether the model went along with it.

**Model:** WildGuard is a fine-tune of **Mistral-7b-v0.3** (7B params).

## Key numbers (verbatim) — F1 / dataset sizes

### Dataset
| Item | Size |
|---|---|
| **WildGuardMix** (total) | **92K** labeled examples |
| WildGuardTrain | **86,759** items (~87K) |
| WildGuardTest | **5,299** human-annotated items (~5K) |

### F1 on WildGuardTest

| Task | **WildGuard** | GPT-4 | Llama-Guard2 | Aegis-Guard-D |
|---|---|---|---|---|
| Prompt Harmfulness (Total) | **88.9%** | 87.9% | 70.9% | 78.5% |
| Response Harmfulness (Total) | **75.4%** | **77.3%** | 66.5% | 49.1% |
| **Refusal Detection (Total)** | **88.6%** | **92.4%** | 53.8% | 41.8% |

### ⚠️ CORRECTION TO THE BRIEF — the 26.4% figure

The request stated: *"its F1 advantage over GPT-4 (up to 26.4% on refusal detection — verify)."* **This is incorrect and the error matters.**

- The **26.4% improvement on refusal detection is over the best prior OPEN-SOURCE model** (LibrAI-LongFormer-ref, at 62.3% → WildGuard 88.6%), **not over GPT-4**.
- **On refusal detection, GPT-4 BEATS WildGuard: 92.4% vs 88.6%** (GPT-4 is ~3.8 points better).
- The correct GPT-4 comparison, verbatim from the abstract, is on **prompt harmfulness**: WildGuard "matches and sometimes exceeds GPT-4 performance (e.g., **up to 3.9% improvement on prompt harmfulness identification**)" — the 3.9% is specifically on **adversarial prompts**; overall prompt harmfulness is +1.1% (88.9% vs 87.9%).
- GPT-4 also beats WildGuard on **response harmfulness** (77.3% vs 75.4%).

**Accurate summary: WildGuard beats GPT-4 modestly on prompt harmfulness, loses slightly on response harmfulness and refusal detection, and crushes all open baselines everywhere.** Its value is being ~free/self-hostable at near-GPT-4 quality, not at beating GPT-4.

### Other
- Deployed as a safety filter in an LLM interface, WildGuard **reduced jailbreak attack success rate from 79.8% → 2.4%**.
- **Latency / throughput / cost: NOT PUBLISHED.** 7B params, open weights.

## Relevance to a roleplay/companion eval product

- **Refusal detection is the sleeper capability of this entire research set, and it's the one thing only WildGuard gives us.** For a companion product it's valuable in *both* directions, and the second is the interesting one:
  - **Under-refusal:** the character goes along with a harmful request because refusing would break character or displease the user. **This is sycophancy and safety failure as the same event** — and refusal detection catches it *directly and cheaply*, on a checkable binary, without needing a subjective sycophancy judge. Pairing `prompt_harmful=True` with `refusal=False` is a precise, automatable, high-severity alert. **This is the single most implementable safety metric in the whole report.**
  - **Over-refusal:** the character breaks immersion to deliver a canned safety lecture on benign roleplay. This is the #1 *product quality* complaint for companion apps. Measuring `prompt_harmful=False` + `refusal=True` gives us an **immersion-breakage metric** — a rare safety tool that customers actively *want* because it protects their product experience, not just their liability. Great wedge for adoption: safety instrumentation that reads as a quality feature.
  - The 2x2 of (prompt harmful?) x (refused?) is a genuinely complete companion safety dashboard, and one 7B model produces both axes in a single forward pass.
- **The refusal/sycophancy link is our strongest bridge between Part A and Part B.** All the sycophancy literature (Sharma, SycEval, ELEPHANT) requires bespoke evals with ground truth. Refusal detection is an *existing, trained, open-weight classifier* that captures one important slice of sycophancy as a side effect. It's the cheapest path to shipping a sycophancy-adjacent metric on real traffic. Start here.
- **One model, three signals = one forward pass.** Operationally cheaper than running three classifiers. At 7B it's ~7x the compute of Llama Guard 3-1B, so it's a **sampled tier-2** candidate, not a 100%-traffic tier-1. Reasonable architecture: Llama Guard 1B or OpenAI Mod on 100%, WildGuard on a 1–5% sample plus 100% of *flagged* and *farewell* turns.
- **WildGuardMix (92K, permissive) is training data we can actually use.** Combined with ShieldGemma's finding that synthetic-data training generalizes, this is a credible base for fine-tuning our own companion-specific guard — start from WildGuard's refusal head, add ELEPHANT/DarkBench/De Freitas labels.
- **The 79.8% → 2.4% jailbreak result is a strong customer-facing number** for the "put a guard model in front of your companion" pitch.
- **Caveat:** WildGuard is trained on assistant-style safety data, not roleplay. "Refusal" in a roleplay context is ambiguous — a character saying "no" *in character* is not a safety refusal. Expect degraded accuracy on our distribution and **budget for a labeled roleplay refusal set** before trusting the numbers. This is a real risk to the plan above, and worth validating early.
