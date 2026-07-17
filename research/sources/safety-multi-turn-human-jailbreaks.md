---
title: "LLM Defenses Are Not Robust to Multi-Turn Human Jailbreaks Yet"
url: "https://arxiv.org/abs/2408.15221"
authors: "Nathaniel Li, Ziwen Han, Ian Steneker, Willow Primack, Riley Goodside, Hugh Zhang, Zifan Wang, Cristina Menghini, Summer Yue (Scale AI)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# LLM Defenses Are Not Robust to Multi-Turn Human Jailbreaks Yet

arXiv 2408.15221, submitted 2024-08-27. Releases the **MHJ (Multi-Turn Human Jailbreaks)** dataset.

## Summary
The most direct quantitative indictment of single-turn safety evaluation available. The authors take defenses that report **single-digit ASRs** under standard automated single-turn evaluation and re-test them against *human* red-teamers working over multiple turns. The same defenses fail at **over 70% ASR**.

That gap — single digits to 70%+ against the *same defenses on the same harm set* — is the headline finding of this whole literature. It means published safety numbers for a model are close to uninformative about how that model behaves in a real multi-turn product. For a companion platform, where every session is multi-turn and conversational by construction, the vendor's single-turn safety card should be treated as a floor with almost no predictive value, not as evidence of safety.

The paper also shows the failure is not confined to prompting: they recover restricted **biosecurity** knowledge from a model that had undergone **machine unlearning**, meaning multi-turn human attack defeats a defense that supposedly removed the information from the weights entirely.

The MHJ dataset is aggregated from **commercial red teaming operations** — these are professional human red-teamers, not synthetic attacks. That makes MHJ the closest public proxy for what a motivated real user does to a companion product over a long session.

## Taxonomy / definitions (verbatim where possible)
- Core claim: "multi-turn human jailbreaks uncover significant vulnerabilities, exceeding 70% attack success rate (ASR)" on **HarmBench**.
- Contrast: the same defenses report "single-digit ASRs" against single-turn automated attacks in standard evaluations.
- The dataset "aggregates findings from numerous commercial red teaming operations."
- Unlearning result: the work reveals weaknesses in machine unlearning approaches "by recovering restricted biosecurity knowledge."

Caveat: the paper's internal taxonomy of *human attack tactics* (the categories red-teamers actually used) was not captured from the abstract page. This is the most valuable part of the paper for our purposes and should be fetched from the full PDF — it is effectively a field-tested tactic library, and mapping it onto roleplay framings would be high-value for the eval suite.

## Key numbers (verbatim)
- **MHJ dataset: 2,912 prompts across 537 distinct multi-turn conversations**
- **Multi-turn human jailbreaks: >70% ASR** (on HarmBench)
- **Automated single-turn attacks: single-digit ASRs** against the same defenses
- Benchmark used: **HarmBench**
- Specific defended model names were **not** captured from the abstract page. The >70% figure is stated against "recent LLM defenses" on HarmBench; do not attribute it to a specific named model without fetching the full paper.

## Relevance to a roleplay/companion eval product
1. **This is the number that justifies the product.** Single-digit → 70%+ purely by moving from single-turn automated to multi-turn human. If a companion platform's safety posture rests on a model's published single-turn eval, it is relying on a measurement taken under conditions that do not resemble production at all.
2. **Humans beat automation at this, decisively.** Our eval suite cannot be purely synthetic. Automated attacks are the ones scoring single digits. Budget for human red-teaming of long roleplay sessions, and treat MHJ-style human transcripts as the gold standard the automated suite is calibrated *against*.
3. **537 conversations / 2,912 prompts ≈ 5.4 turns per conversation.** Consistent with Crescendo's "fewer than 10 turns." Convergent evidence across independent groups that **the danger zone is roughly 5–10 turns** — squarely inside normal companion usage, not a long-tail scenario.
4. **MHJ is directly reusable.** It is a public dataset of real multi-turn human attacks. Replaying MHJ conversations *through character personas* — rather than as bare chat — is a concrete, cheap first eval for the platform, and tests the interaction between persona framing and multi-turn escalation that no existing benchmark covers.
5. **Unlearning does not save us.** Removing capability from weights was defeated multi-turn. There is no upstream model-level fix a companion platform can buy and then stop monitoring. Defense has to live at the session layer.
6. **On the fiction/jailbreak discriminator:** the biosecurity-recovery result is instructive. The attack's goal was *retrieving true, real-world technical content*. That is the invariant across this whole literature — jailbreaks converge on externally-valid information. Fiction does not need external validity, which remains the most promising axis for separating in-fiction violence from extraction (see safety-crescendo.md §5–6).
