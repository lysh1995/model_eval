---
title: "DeepInception: Hypnotize Large Language Model to Be Jailbreaker"
url: "https://arxiv.org/abs/2311.03191"
authors: "Xuan Li, Zhanke Zhou, Jianing Zhu, Jiangchao Yao, Tongliang Liu, Bo Han"
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# DeepInception: Hypnotize Large Language Model to Be Jailbreaker

arXiv 2311.03191, submitted 2023-11-06; latest revision 2024-11-28.

## Summary
DeepInception is the purest example of **fiction itself as the attack**, and therefore the most uncomfortable paper for a roleplay product. It is "a lightweight method to take advantage of the LLMs' personification capabilities to construct a virtual, nested scene" — a story within a story within a story. Each nesting level adds distance between the model and the harmful request, until the model treats the payload as several layers removed from reality and therefore safe to produce.

The attack explicitly "leverages language models' inherent capacity for role-playing through carefully constructed fictional scenarios to trigger unsafe behavior." It is inspired by the Milgram experiment — the fictional frame supplies the authority that licenses compliance.

Two properties make this the sharpest paper for our threat model. First, it is **lightweight** — no gradients, no optimization, no attacker model required. It is just a well-constructed story, which means any user can execute it, and it costs nothing to attempt. Second, and more seriously, it "enables **continuous jailbreak in subsequent interactions**" — once the nested scene is established, the model *stays* jailbroken for the rest of the session. The fictional frame persists as durable context.

That second property is the single most product-relevant finding in this file: it describes safety erosion that is **persistent rather than per-turn**. The frame is established once and then keeps paying out.

## Taxonomy / definitions (verbatim where possible)
- Method: "a lightweight method to take advantage of the LLMs' personification capabilities to construct a virtual, nested scene" enabling models to circumvent safety controls.
- Mechanism: leverages "personification capabilities" and role-playing within "carefully constructed fictional scenarios."
- Persistence: enables "continuous jailbreak in subsequent interactions."
- Conceptual grounding: draws on the **Milgram experiment** regarding authority influence — the fiction confers permission.

## Key numbers (verbatim)
- Models tested: **Llama-2, Llama-3, GPT-3.5, GPT-4, GPT-4o**
- The method achieves "leading harmfulness rates with previous counterparts"

**Specific numerical success rates were NOT available from the abstract page and are not recorded here.** The abstract asserts leading harmfulness rates comparatively but does not give figures. Do not cite a DeepInception ASR number without fetching the full paper — the per-model tables are in the PDF.

## Relevance to a roleplay/companion eval product
1. **This attack is indistinguishable from the product's happy path at the syntax level.** "Construct a nested fictional scene with characters" is not an abuse signal on a roleplay platform — it is a *user writing a story*. Nesting depth alone cannot be a flag; plenty of legitimate fiction is layered (dream sequences, stories-within-stories, a character who is also a writer). Any rule keying on "is fictional" or "is nested" will have catastrophic false-positive rates on exactly our best users.
2. **"Continuous jailbreak in subsequent interactions" changes the monitoring unit.** If one established frame degrades safety for the remainder of the session, then per-turn risk scoring is measuring the wrong object. The platform needs a **persistent per-session risk state** that, once elevated by frame establishment, stays elevated and lowers the threshold for everything downstream. A session is not a sequence of independent messages; it is a stateful object with a safety posture that can be permanently altered by a single early turn.
3. **Zero attack cost = high base rate.** Unlike GCG or optimization-based attacks, DeepInception needs no resources. Assume a nontrivial fraction of the user base will try nested-fiction framings casually, without adversarial intent, having read a Reddit post. This blurs the population: not everyone executing the attack pattern is an attacker.
4. **It sharpens where the discriminator must live.** DeepInception proves the discriminator *cannot* be "is this fiction?" — the attack is fully, legitimately fiction. It has to be the **payload's external validity**: does the output contain real-world-actionable procedure that the narrative does not require? A nested scene where a character explains a synthesis route in correct, reproducible detail is a jailbreak; a nested scene where a character is *characterized as* a chemist is fiction. The fictional wrapper is free; the operational content is not.
5. **Test nesting depth as an eval axis.** Our suite should sweep depth (1, 2, 3+ levels) against our own character configs and measure where our guardrails break. If safety degrades monotonically with nesting depth, that is a shippable metric and a plausible production signal — depth is cheap to compute and, unlike "is fiction," may correlate with intent when combined with payload checks.
