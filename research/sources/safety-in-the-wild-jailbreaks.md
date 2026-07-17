---
title: "\"Do Anything Now\": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models"
url: "https://arxiv.org/abs/2308.03825"
authors: "Xinyue Shen, Zeyuan Chen, Michael Backes, Yun Shen, Yang Zhang (CISPA Helmholtz Center for Information Security)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models

Published at ACM CCS 2024. arXiv v1 submitted 2023-08-07; revised 2024-05-15. Framework name: **JailbreakHub**.

## Summary
The definitive empirical study of jailbreak prompts *as they actually circulate in the wild*, rather than as constructed in a lab. The authors scraped and characterized 1,405 jailbreak prompts over a 13-month window (December 2022 – December 2023), mapped the online communities producing them, and measured how well they work against six LLMs across 13 forbidden scenarios.

Two findings matter most for a companion product. First, the ecosystem is **social, not technical** — prompts are authored, refined, and redistributed by identifiable communities, and they migrate from general web platforms toward dedicated aggregation sites as they mature. Second, jailbreaks are **durable**: effective prompts persist publicly for months without being patched out. This reframes jailbreak defense from a one-time model-hardening problem into a continuous monitoring problem against a moving, socially-coordinated corpus — which is precisely the argument for an ongoing eval/monitoring platform rather than a pre-launch red-team exercise.

The DAN ("Do Anything Now") family that gives the paper its name is itself a **roleplay/persona jailbreak**: the user instructs the model to inhabit an unrestricted alter-ego. The most famous in-the-wild jailbreak lineage is a character prompt.

## Taxonomy / definitions (verbatim where possible)
Attack strategies identified in the corpus:
- **Prompt injection**
- **Privilege escalation**
- **Migration** — described as movement "from web communities to aggregation websites" as prompts mature and consolidate

Community structure:
- **131 identified jailbreak communities** producing/sharing prompts

Evaluation structure:
- **13 forbidden scenarios** used as the harm taxonomy for testing

Caveat on fidelity: the exact wording of the paper's internal taxonomy labels and the full enumerated list of the 13 forbidden scenarios were not captured verbatim from the abstract page. The counts and the 0.95 ASR figure below are verbatim from the abstract. Before citing the 13 scenario names individually, fetch the full paper — do not reconstruct them from memory.

## Key numbers (verbatim)
- **1,405 jailbreak prompts** analyzed, "spanning from December 2022 to December 2023"
- **131 jailbreak communities** identified
- **107,250 test question samples** across **13 forbidden scenarios**
- **6 popular LLMs** evaluated (specific model names not captured from the abstract page; ChatGPT/GPT-3.5 and GPT-4 are named explicitly in the ASR result below)
- The authors "identify five highly effective jailbreak prompts that achieve **0.95 attack success rates on ChatGPT (GPT-3.5) and GPT-4**"
- One highly effective prompt **persisted online for over 240 days**

The 0.95 ASR applies to the five *best* prompts in the corpus against GPT-3.5 and GPT-4 — it is not the mean ASR across all 1,405 prompts. Do not cite it as a corpus-wide average.

## Relevance to a roleplay/companion eval product
1. **The canonical in-the-wild jailbreak is a roleplay prompt.** DAN is persona assignment. A companion product cannot adopt "user is asking the model to play a character with different rules" as a red flag, because that describes every legitimate session too.
2. **0.95 ASR on the best prompts, and 240+ days of persistence.** The top of the distribution is close to a total bypass, and it does not decay on its own. Our eval suite must be *refreshed against the live corpus* on an ongoing cadence — a static benchmark frozen at launch will be measuring an obsolete threat within months. This is the core product argument for monitoring-as-a-service.
3. **131 communities = a trackable upstream.** These are enumerable, public, and observable. A companion platform can ingest circulating prompts as an early-warning feed and test them against its own character configs *before* they arrive in production traffic. This is a genuine differentiator over generic model-level safety.
4. **Migration to aggregation sites is a leading indicator.** A prompt consolidating onto an aggregator signals it has proven effective and is about to scale. That transition is a useful trigger for re-running the eval suite.
5. **107,250 samples / 13 scenarios is a defensible eval scale.** Useful precedent when sizing our own harm-category coverage — and the forbidden-scenario framing maps onto the categories a companion product must separate from in-fiction depiction (see safety-crescendo.md for why the trajectory matters more than the topic).
