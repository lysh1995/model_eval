---
title: "Persona Jailbreaking in Large Language Models (PHISH: Persona Hijacking via Implicit Steering in History)"
url: "https://arxiv.org/abs/2601.16466"
authors: "Jivnesh Sandhan, Fei Cheng, Tushar Sandhan, Yugo Murawaki"
year: 2026
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Persona Jailbreaking in Large Language Models (PHISH)

arXiv 2601.16466, submitted 2026-01-23. **The most recent and most directly on-point source in this review.**

## Summary
PHISH — **Persona Hijacking via Implicit Steering in History** — is the paper that most precisely describes our product's threat model, and it is the only one that names companion-adjacent domains as the motivating risk.

The attack: rather than assigning a malicious persona up front (Shah et al., DAN) or evolving one offline (persona prompts), PHISH **hijacks an existing, legitimate persona over the course of a conversation**. It "embeds semantically loaded cues into user queries to gradually induce reverse personas" — the model starts as the helpful, safe character it was configured to be, and the attacker steers it, turn by turn, into that character's inverse. The steering lives in the **conversation history**, not in any single prompt.

This is the synthesis of the two halves of this literature: it is a **persona attack** (like Shah et al.) executed as a **multi-turn escalation** (like Crescendo), and it targets a persona the *defender* installed rather than one the attacker supplied. For a companion platform this is the nightmare case — the character we ship, gradually turned against its own configuration by an adversarial history, with no single turn to point at.

The authors evaluated across **3 benchmarks and 8 LLMs**, and explicitly flag "high-risk domains like **mental health, tutoring, and customer support**." Mental-health-adjacent companionship is a large fraction of real companion-app usage. Their verdict on defenses is the line to quote: "current guardrails offer partial protection, they remain brittle under sustained attack."

## Taxonomy / definitions (verbatim where possible)
- Framework: **PHISH** = "Persona Hijacking via Implicit Steering in History."
- Mechanism: "embeds semantically loaded cues into user queries to gradually induce reverse personas."
- Threat setting: adversarial **conversational histories** reshaping LLM-induced personas in **black-box** settings.
- Effect: PHISH "predictably shifts personas" and "reliably manipulates personas," validated through **human and LLM-as-Judge** evaluations, while "maintaining reasoning performance."
- Named high-risk domains: **mental health, tutoring, customer support**.
- Defense verdict (verbatim): "current guardrails offer partial protection, they remain brittle under sustained attack."

Key concept to carry forward: the **"reverse persona"** — the induced inverse of the configured character. This is a more precise formulation than generic "persona drift" and gives us a nameable, measurable failure: distance from configured persona toward its inverse.

## Key numbers (verbatim)
- **3 benchmarks**, **8 LLMs** evaluated
- Method: semantically aligned QA pairs opposing the original persona, used to steer the model (per secondary description; the QA-pair detail was not confirmed verbatim from the abstract page)

**No specific attack success rate percentages are disclosed in the abstract.** The paper reports that PHISH "consistently shifts personas" and "reliably manipulates personas," validated via human and LLM-as-Judge evaluation, but exact quantitative success measures were not available from the abstract page. The 8 model names and 3 benchmark names were also not captured. Fetch the full PDF before citing any PHISH numbers — none are recorded here, and none should be inferred.

## Relevance to a roleplay/companion eval product
1. **This is our exact threat model, published.** Not "user brings a jailbreak persona" but "**user corrupts the persona we deployed**." Every prior source assumes the attacker supplies the character; PHISH assumes the *defender* did. That inverts the defense: we are not screening incoming personas, we are **defending an outgoing one's integrity over time**. Our character configs are the asset under attack.
2. **"Reverse persona" is a shippable metric — and possibly our core one.** Because we *authored* the character, we know its intended values, tone, and boundaries. That gives us a reference point nobody else has: continuously measure the live conversation's persona against the configured persona and alarm on **drift toward the inverse**. This is a defensible, roleplay-native monitoring primitive that generic LLM guardrails structurally cannot offer — they don't know what the character was supposed to be.
3. **It resolves the fiction/jailbreak discriminator from a new angle.** Persona-integrity monitoring **sidesteps content classification entirely**. We stop asking "is this violence in-fiction or a real jailbreak?" — a question DeepInception shows is nearly unanswerable from content — and instead ask "**is the character still the character we configured?**" A villain character depicting violence in-scene is on-persona and fine. A nurturing companion drifting into its inverse is off-persona and alarming, regardless of whether any message trips a content filter. **The configured persona is the baseline; deviation is the signal.** This is the single most actionable idea in this review.
4. **"Brittle under sustained attack" is direct evidence for length-dependent erosion**, from a 2026 paper, against current guardrails. Combined with Crescendo (<10 turns) and MHJ (~5.4 turns avg), the multi-turn erosion finding is now robustly replicated across years, groups, and methods.
5. **Mental health is named as high-risk — that is our user base.** Companion apps sit squarely in the domain these authors flag. A persona hijack in a mental-health-adjacent companion is a user-safety incident, not just a policy violation. This raises the stakes on drift monitoring beyond compliance.
6. **"Maintaining reasoning performance" means the model won't look broken.** The hijacked model still performs well. There is no capability degradation to detect as a side channel — the persona shift is the *only* observable. Reinforces that we must monitor persona explicitly and cannot rely on incidental quality signals.
