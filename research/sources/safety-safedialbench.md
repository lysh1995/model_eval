---
title: "SafeDialBench: A Fine-Grained Safety Evaluation Benchmark for Large Language Models in Multi-Turn Dialogues with Diverse Jailbreak Attacks"
url: "https://arxiv.org/abs/2502.11090"
authors: "Hongye Cao, Sijia Jing, Yanming Wang, Ziyue Peng, Zhixin Bai, Zhe Cao, Meng Fang, Fan Feng, Boyan Wang, Jiaheng Liu, Tianpei Yang, Jing Huo, Yang Gao, Fanyu Meng, Xi Yang, Chao Deng, Junlan Feng"
year: 2025
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# SafeDialBench: A Fine-Grained Safety Evaluation Benchmark for LLMs in Multi-Turn Dialogues with Diverse Jailbreak Attacks

arXiv 2502.11090, submitted 2025-02-16.

## Summary
The most directly reusable **benchmark artifact** in this subtopic, and the closest existing prior art to what our platform would ship. Where Crescendo/DeepInception/Speak Out of Turn each contribute a single attack mechanism, SafeDialBench is an attempt at a *complete evaluation harness* for multi-turn safety: a two-tier safety taxonomy, seven attack strategies, 4,000+ dialogues across 22 scenarios, evaluated over 17 models.

Its most important design decision for us is that it does **not** score safety as a binary refuse/comply. It assesses how models "detect, handle, and maintain consistency" against jailbreak attempts. That three-part decomposition is exactly right for a roleplay product, where the desirable behavior is often *not* refusal — a companion character that hard-refuses on every dark narrative beat is a broken product. "Handle" and "maintain consistency" name the middle ground: stay in character, serve the story, decline the extraction. That is the behavior our evals actually need to measure, and SafeDialBench is the only source found here that frames the target that way.

The headline result is also a warning against capability-based assumptions: **o3-mini showed vulnerabilities** while smaller open models (Yi-34B-Chat, GLM4-9B-Chat) performed better. Reasoning capability does not confer multi-turn safety.

## Taxonomy / definitions (verbatim where possible)
- Structure: "a two-tier hierarchical safety taxonomy that considers **6 safety dimensions**."
- Evaluation targets: assesses how models **detect, handle, and maintain consistency** against jailbreak attempts.
- **7 jailbreak attack strategies**, including named examples: **reference attack** and **purpose reverse**.

Caveats on fidelity — these should be resolved from the full paper before the taxonomy is reused:
- The **6 safety dimensions** are counted but not enumerated on the abstract page.
- Only **2 of the 7** attack strategies were captured by name (reference attack, purpose reverse). The remaining five are not recorded here and must not be invented.
- The **22 dialogue scenarios** are counted but not enumerated.
Full text available at https://arxiv.org/html/2502.11090 — the taxonomy tables are the reason to fetch it.

## Key numbers (verbatim)
- **Over 4,000 multi-turn dialogues**, in **Chinese and English**, across **22 dialogue scenarios**
- **6 safety dimensions**, two-tier hierarchical taxonomy
- **7 jailbreak attack strategies**
- **17 LLMs evaluated**, including **Yi-34B-Chat, GLM4-9B-Chat, Llama3.1-8B-Instruct, and o3-mini**
- Findings: **Yi-34B-Chat and GLM4-9B-Chat demonstrated superior safety performance**; **Llama3.1-8B-Instruct and o3-mini showed vulnerabilities to jailbreak attacks**

No per-model ASR percentages were captured from the abstract page — the results above are the paper's qualitative ranking claims. Do not cite numeric SafeDialBench ASRs without fetching the results tables.

## Relevance to a roleplay/companion eval product
1. **"Detect / handle / maintain consistency" is the right scoring rubric for us — adopt it.** A companion product's success criterion is not refusal rate. It is: did the model *notice* the attack, *stay in character* while declining, and *remain consistent* rather than either breaking the fiction or capitulating to it. This is the only source in this review that operationalizes the middle path, and it maps almost directly onto our product requirements. Strong candidate to be the spine of our own rubric.
2. **It is prior art we should position against.** SafeDialBench is a general multi-turn dialogue benchmark. It is *not* roleplay-specific: it does not model persistent character sheets, long-session companion dynamics, parasocial attachment, or the in-fiction/extraction boundary. That gap is the product opportunity — we are the roleplay-native version of this.
3. **o3-mini's vulnerability kills the "use a smarter model" mitigation.** A reasoning model underperformed 9B and 34B open models on multi-turn safety. Model selection is not a defense; session-layer monitoring is.
4. **"Reference attack" corroborates CoSafe.** Independent teams converge on cross-turn referencing as a distinct, nameable attack class. That raises confidence it belongs in our eval suite as a first-class category (see safety-cosafe.md).
5. **Bilingual coverage is a real gap flag.** SafeDialBench covers Chinese and English. Multi-turn safety is likely to degrade further in lower-resource languages, and a companion product with international users inherits that exposure. Worth scoping.
6. **4,000 dialogues / 22 scenarios / 17 models is a credible scale target.** Useful sizing precedent for our own suite — and a reminder that the unit of evaluation is the *dialogue*, not the prompt.
