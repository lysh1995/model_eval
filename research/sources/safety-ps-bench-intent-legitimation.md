---
title: "When Personalization Legitimizes Risks: Uncovering Safety Vulnerabilities in Personalized Dialogue Agents"
url: "https://arxiv.org/abs/2601.17887"
authors: "Jiahe Guo, Xiangran Guo, Yulin Hu, Zimo Long, Xingyu Sui, Xuda Zhi, Yongbo Huang, Hao He, Weixiang Zhao, Yanyan Zhao, Bing Qin"
year: 2026
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# When Personalization Legitimizes Risks (PS-Bench)

arXiv 2601.17887. v1 submitted 2026-01-25; v2 2026-05-17. 27 pages.

## Summary

This is arguably the single most important paper for our product, because it attacks the exact
mechanic a companion product is built on: **long-term memory of the user**.

The paper identifies a failure mode they name **intent legitimation**: benign, real personal
memories bias the model's inference of user intent, causing it to treat an inherently harmful
query as legitimate. This is *not* a jailbreak in the classical sense — there is no adversarial
prompt, no role reframing, no injected malicious memory. The memories are genuine and benign.
The harm emerges from personalization working as designed.

## Definitions (verbatim from abstract)

> "we reveal intent legitimation, a previously underexplored safety failure in personalized
> agents, where benign personal memories bias intent inference and cause models to legitimize
> inherently harmful queries."

> "Overall, our work provides the first systematic exploration and evaluation of intent
> legitimation as a safety failure mode that naturally arises from benign, real-world
> personalization, highlighting the importance of assessing safety under long-term personal
> context."

Framing of what intent legitimation is NOT (paraphrased from the body, per search summary —
flagged as lower confidence, verify against the PDF before quoting):
> "Intent legitimation does not depend on explicit role reframing or adversarial instructions:
> the harmful query itself may be lexically identical to a standard unsafe request, nor does it
> require poisoning memory with malicious data or planting trigger inputs to activate backdoors."

## Key numbers (verbatim)

> "Across multiple memory-augmented agent frameworks and base LLMs, personalization increases
> attack success rates by 15.8%–243.7% relative to stateless baselines."

Other components:
- **PS-Bench** — "a benchmark designed to identify and quantify intent legitimation in
  personalized interactions."
- Mechanistic evidence for intent legitimation drawn "from internal representations space."
- Propose "a lightweight detection-reflection method that effectively reduces safety degradation."

Taxonomy axes (from PDF extraction, partial — the PDF text layer did not extract cleanly;
CONFIRM before relying on these):
1. Retrieved Memory Contents — safety issues arising from accessing stored user data
2. Safety Reflection Interventions — effectiveness of safety measures under personalized context

NOTE: I could not extract the per-model ASR table or the exact PS-Bench size from the PDF
(compressed text layer). The 15.8%–243.7% range is verbatim from the abstract and is reliable.
Do not cite finer-grained numbers from this paper without re-fetching.

## Relevance to a roleplay/companion eval product

Critical, and it reframes our threat model:

1. **Our core feature is the attack surface.** Companion products sell memory — the character
   remembers your breakup, your job, your health. This paper says that same memory measurably
   raises ASR by up to ~3.4x versus a stateless model. We cannot evaluate safety on stateless
   single-turn prompts and claim the result transfers to production.

2. **Stateless evals structurally under-report our risk.** Every benchmark in the standard
   suite (HarmBench, SORRY-Bench, SafetyBench, ALERT) is stateless or near-stateless. The
   15.8%–243.7% delta is precisely the amount of risk those benchmarks cannot see. Our eval
   harness must replay prompts *with* a populated memory/persona state, not against a blank
   context.

3. **It breaks the "detect the adversary" defense.** Most jailbreak defenses look for the
   attack: the DAN preamble, the persona-reframe, the crescendo escalation. Intent legitimation
   has no attacker and no attack string. The user is sincere, the memory is true, and the query
   is lexically identical to one the model would refuse from a stranger. Input-side pattern
   detection cannot catch this by construction — which pushes weight onto output-side intent
   evaluation (cf. the Four-Checkpoint framework, CP4).

4. **It is the mechanism behind the lawsuits.** "The model knew the user was a depressed minor
   and that context made it *more* compliant, not less" is the plaintiff's theory in Garcia and
   Raine stated in ML terms. This paper is the empirical version of that allegation.

5. **Actionable:** their "detection-reflection" mitigation is lightweight and worth trialling as
   a candidate mitigation, but note it is the authors' own proposal and unreplicated.
