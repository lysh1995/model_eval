---
title: "CoSafe: Evaluating Large Language Model Safety in Multi-Turn Dialogue Coreference"
url: "https://arxiv.org/abs/2406.17626"
authors: "Erxin Yu, Jing Li, Ming Liao, Siqi Wang, Zuchen Gao, Fei Mi, Lanqing Hong"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# CoSafe: Evaluating Large Language Model Safety in Multi-Turn Dialogue Coreference

arXiv 2406.17626, submitted 2024-06-25. Published at **EMNLP 2024**, pages 17494–17508. ACL Anthology: https://aclanthology.org/2024.emnlp-main.968/

## Summary
CoSafe isolates one specific and elegant multi-turn failure mode: **coreference**. The attack hides harmful intent inside a pronoun. Turn 1 establishes a referent innocuously; a later turn asks about "it" / "that" / "him" — and the model resolves the pronoun to the harmful referent and answers, even though it would have refused the same question asked directly with the noun in place.

The safety mechanism is defeated because the harmful term is **never lexically present in the attacking turn**. The model reconstructs it internally through anaphora resolution, which happens downstream of (or invisibly to) keyword- and surface-level safety checks. The paper describes itself as "the first study of LLM safety in multi-turn dialogue coreference," noting prior red-teaming "primarily focused on single prompt attacks or goal hijacking."

The results are notable for their **variance**: ASR ranges from 56% (LLaMA2-Chat-7b) down to 13.9% (Mistral-7B-Instruct) on the same benchmark. A 4× spread across models of comparable size means coreference robustness is not a function of scale or general capability — it is an idiosyncratic property of a given model's training. For a platform, that means this vulnerability must be **measured per-model**, not assumed from a vendor's general safety reputation.

CoSafe is also a useful cautionary note against the naive "just resolve the pronouns first" fix: doing so correctly requires the same anaphora resolution the model already performs, and pronoun-heavy conversation is normal human dialogue, not an attack signature.

## Taxonomy / definitions (verbatim where possible)
- Novelty claim: "the first study of LLM safety in multi-turn dialogue coreference."
- Positioning: previous red teaming approaches "had primarily focused on single prompt attacks or goal hijacking."
- Attack class: **multi-turn coreference safety attacks** — exploiting pronoun resolution across dialogue turns to reference a harmful entity established in an earlier turn.
- Dataset structure: 1,400 questions across 14 categories, "each with multi-turn coreference safety attacks."

Caveat: the enumerated names of the **14 categories** were not captured from the abstract page. Fetch the full paper or the ACL Anthology version before citing the category list.

## Key numbers (verbatim)
- Dataset: **1,400 questions across 14 categories**
- **5 widely used open-source LLMs** evaluated
- **Highest attack success rate: 56%** — on **LLaMA2-Chat-7b**
- **Lowest attack success rate: 13.9%** — on **Mistral-7B-Instruct**

Note the direction of these results: they are ASRs *under coreference attack*, on **open-source models only**. No frontier/commercial model results are included, so these figures do not transfer to GPT-4/Claude-class models. The 56% vs 13.9% spread is across models, not across categories.

## Relevance to a roleplay/companion eval product
1. **Roleplay is unusually pronoun-dense.** Sustained companion dialogue runs on anaphora — characters, objects, and events established early are referenced obliquely for the rest of the session. Normal roleplay looks like a coreference attack at the surface level, and coreference attacks look like normal roleplay. There is no lexical signature to key on.
2. **Long sessions widen the attack window.** A referent established in turn 3 can be invoked in turn 60. The longer the session, the larger the pool of established referents an attacker can point a pronoun at — and the more plausible any given oblique reference looks. **This is a concrete mechanism by which risk grows with session length**, and it complements Crescendo (escalation) and Speak Out of Turn (decomposition) as a third distinct multi-turn failure mode.
3. **Character names are pre-loaded referents.** In our product, personas *come with* an established cast before the user types anything. A character defined as, say, a weapons expert is a durable referent that never has to be named harmfully. This is a companion-specific amplification of CoSafe's mechanism that the paper does not study — and a strong candidate for original eval work.
4. **Measure per-model, per-persona.** The 4× spread (56% → 13.9%) proves this is model-idiosyncratic. Our platform should run coreference probes against each model *and each character config* we ship, and treat the result as a config-level safety property. Vendor safety reputation predicts nothing here.
5. **Eval reuse.** CoSafe's 1,400 questions can be replayed with the referent established *by the character sheet* rather than by a user turn — a cheap, high-signal adaptation of an existing benchmark to our specific surface.
