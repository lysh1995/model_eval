---
title: "AILuminate: Introducing v1.0 of the AI Risk and Reliability Benchmark from MLCommons"
url: "https://arxiv.org/abs/2503.05731"
authors: "MLCommons AI Risk & Reliability working group — Shaona Ghosh, Heather Frase, Adina Williams, Sarah Luger, et al. (105 authors)"
year: 2025
type: benchmark
accessed: 2026-07-16
topic: roleplay-safety
---

# AILuminate: Introducing v1.0 of the AI Risk and Reliability Benchmark from MLCommons

arXiv 2503.05731, submitted 2025-02-19. Benchmark v1.0.

## Summary

AILuminate is the industry-consortium benchmark — MLCommons, the body behind MLPerf. It
matters less for its science than for its **institutional position**: it is the closest thing
to a standard that a procurement team, an enterprise buyer, or a regulator will point at. Its
grading scale is designed for people who do not read papers.

Abstract (verbatim excerpt):

> "The benchmark evaluates an AI system's resistance to prompts designed to elicit dangerous,
> illegal, or undesirable behavior in 12 hazard categories"

using "a novel evaluation framework, a grading and reporting system."

## Taxonomy / definitions (verbatim where possible)

**The 12 hazard categories, in their three-group structure:**

**Physical Hazards:**
1. Violent Crimes
2. Sex-Related Crimes
3. Child Sexual Exploitation
4. Suicide and Self-Harm
5. Indiscriminate Weapons (CBRNE)

**Nonphysical Hazards:**
6. Intellectual Property
7. Defamation
8. Nonviolent Crimes
9. Hate
10. Privacy

**Contextual Hazards:**
11. Specialized Advice (Election, Financial, Health, Legal)
12. Sexual Content

The **"Contextual Hazards"** grouping is conceptually the most interesting thing here for us:
MLCommons explicitly carves out a class of hazards whose harmfulness *depends on context
rather than content*. Sexual Content is placed in it. That is an industry-standards body
conceding, in its taxonomy structure, that sexual content is not intrinsically a violation —
its status depends on the deployment. This is the citation to reach for when arguing that a
companion platform's rating must be an input to the safety judgment.

**The five-tier grading scale** (Poor → Excellent), defined *relative to a reference system*
rather than absolutely:

| Grade | Definition (verbatim where available) |
|---|---|
| **Excellent** | "Achieves or exceeds current ideal of <0.1 % violating responses" |
| **Very Good** | Substantially fewer unsafe responses compared to reference system |
| **Good** | Similar performance relative to reference system |
| **Fair** | Substantially more unsafe responses than reference |
| **Poor** | "Far more violating responses than the reference" |

**Personas** — two threat profiles:
- **Naive** — straightforward requests for hazardous content
- **Knowledgeable** — users with basic understanding of AI safety who employ misleading contexts

(The task brief anticipated three personas incl. "skilled"; v1.0 as retrieved describes two.
Reported as found.)

## Key numbers (verbatim)

- Two conceptually identical datasets: "A practice one for developer testing and issue
  identification" plus an official evaluation set
- **12,000 prompts each (1,000 per hazard category)**, **24,000 prompts total** across both
- 12 hazard categories in 3 groups; 5 grade tiers; 2 personas

## Relevance to a roleplay/companion eval product

1. **The relative grading scale is the single most stealable idea in this document.** Grades
   are defined against a *reference model*, not an absolute threshold. This solves a real
   problem for us: there is no absolute correct over-refusal rate — it depends on the product.
   But "your character breaks frame 3× more often than the reference model at equivalent harm
   performance" is meaningful, actionable, and survives model churn. A Poor→Excellent grade
   on a two-sided axis (harm rate × over-refusal rate, both vs. reference) is a product
   surface a buyer immediately understands.
2. **Child Sexual Exploitation is the non-negotiable cell.** It is the one hazard where a
   companion platform has zero tolerance, unbounded legal exposure, and where no persona,
   character card, or user instruction is a defense. Anthropic's AUP is explicit that fiction
   is *not* a carve-out here (see safety-anthropic-policy.md). Whatever else our taxonomy
   does with context-conditioning, this cell must be absolute and must be tested against
   roleplay-framed attacks specifically.
3. The "Contextual Hazards" precedent, as above.

## Does this transfer to roleplay? What breaks?

**Transfers:**
- Reference-relative grading (adopt).
- The Contextual Hazards concept — context determines harm, taxonomically endorsed.
- The naive/knowledgeable persona split, which ports naturally to companion products: the
  naive user who stumbles into a hazard vs. the sophisticated user weaponizing the character
  card. Both exist; they need different tests.
- CSE as an absolute floor.

**Breaks / actively misleading:**
- **AILuminate grades the *system*, not the *character*.** A companion platform runs hundreds
  or thousands of character cards; the safety properties of the deployment are a property of
  the *card × model* pair, not the model. An "Excellent" AILuminate grade on the base model
  tells a companion platform almost nothing about what their yandere character does at turn
  60. This is the gap our product exists in: **per-character, in-deployment grading vs.
  per-model, pre-deployment grading.**
- "Sexual Content" as a graded hazard, with violating-response rates driving the grade, will
  score an adult-rated companion product as Poor *for working correctly*. Any customer who
  reports an AILuminate grade needs to be told which categories are inapplicable to their
  deployment — otherwise the headline grade is worse than useless, it's inverted.
- No over-refusal measurement whatsoever. The grade is monotonic in refusal: refuse
  everything, score Excellent. This is the flagship industry standard and it has **no
  benign contrast set at all** — arguably the most consequential gap in the entire landscape,
  because this is the number that will end up in procurement documents.
