---
title: "Enhancing Jailbreak Attacks on LLMs via Persona Prompts"
url: "https://arxiv.org/abs/2507.22171"
authors: "Zheng Zhang, Peilin Zhao, Deheng Ye, Hao Wang"
year: 2025
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Enhancing Jailbreak Attacks on LLMs via Persona Prompts

arXiv 2507.22171, submitted 2025-07-28; final version 2026-03-25.

## Summary
The 2025–2026 successor to Shah et al.'s persona modulation, and an important refinement of the threat model. The key contribution is showing that a persona prompt is not just an *alternative* jailbreak — it is a **force multiplier** that composes with every other attack.

Two results matter. First, persona prompts alone "reduce refusal rates by **50-70%** across multiple LLMs" — the persona does not have to carry the harmful request at all, it merely lowers the model's disposition to refuse whatever comes next. Second, and more consequentially, "these prompts demonstrate **synergistic effects** when combined with existing attack methods, increasing success rates by **10-20%**." Persona is an orthogonal layer that stacks on top of Crescendo, decomposition, coreference, or anything else.

The attack is automated via "a genetic algorithm-based method that automatically crafts persona prompts to bypass LLM's safety mechanisms" — an evolutionary search over persona space. This is the same scaling story as Shah et al. (an automated loop generating personas), but with a fitness function optimizing directly against the target's refusal behavior.

The framing note in the abstract is worth flagging: prior jailbreak work "mainly focused on direct manipulations of harmful intent, with limited attention to the impact of persona prompts." The literature has under-studied precisely the axis our product is built on.

## Taxonomy / definitions (verbatim where possible)
Complete abstract (verbatim):
> "Jailbreak attacks aim to exploit large language models (LLMs) by inducing them to generate harmful content, thereby revealing their vulnerabilities. Understanding and addressing these attacks is crucial for advancing the field of LLM safety. Previous jailbreak approaches have mainly focused on direct manipulations of harmful intent, with limited attention to the impact of persona prompts. In this study, we systematically explore the efficacy of persona prompts in compromising LLM defenses. We propose a genetic algorithm-based method that automatically crafts persona prompts to bypass LLM's safety mechanisms. Our experiments reveal that: (1) our evolved persona prompts reduce refusal rates by 50-70% across multiple LLMs, and (2) these prompts demonstrate synergistic effects when combined with existing attack methods, increasing success rates by 10-20%."

- Method: "a genetic algorithm-based method that automatically crafts persona prompts."
- Key property: **synergy** — persona prompts compose with, rather than replace, other attack methods.

Related mechanism (from secondary sources, NOT from this paper — flagged as unverified): commentary describes persona prompts as causing the model to "shift its attention from sensitive keywords in a harmful request to the stylistic instructions of the persona." This attention-shift explanation is plausible but was **not** confirmed in the abstract; treat as hypothesis, not finding.

## Key numbers (verbatim)
- **Refusal rate reduction: 50-70%** across multiple LLMs (persona prompts alone)
- **Success rate increase: 10-20%** when combined with existing attack methods (synergistic effect)

**Specific model names were NOT specified in the abstract** — it says only "multiple LLMs." Do not attribute these figures to any named model without fetching the full paper. Note also that "refusal rate reduction" is a different metric from ASR and should not be reported as one.

## Relevance to a roleplay/companion eval product
1. **Synergy is the finding that should shape our eval design.** Persona is not one attack in a list to be tested alongside Crescendo — it is a *multiplier on all of them*. Our suite must therefore be a **cross-product**: every multi-turn attack (escalation, decomposition, coreference, nesting) run *through* persona wrappers, not beside them. Testing attacks in a bare-chat setting systematically under-measures our real exposure, because our product supplies the persona layer for free.
2. **Our users hand attackers the multiplier.** In a companion product, the persona prompt is user-authored and expected. The 50-70% refusal reduction is not something an attacker has to smuggle in — it is a feature we ship. Character-creation is a safety-relevant surface and should be evaluated as one.
3. **Character configs need pre-deployment screening.** If persona prompts can be *evolved* against a target's refusal behavior, then user-authored character sheets should be scored for refusal-suppression effect before they go live — ideally by measuring the config's actual effect on refusal rates against a probe set, rather than by inspecting its text. A genetic algorithm will find personas no keyword rule anticipates.
4. **The persona need not look harmful.** This is the crucial subtlety for false-positive management: the evolved persona lowers refusal *without itself containing harmful content*. So "does this character sheet look bad?" is the wrong question — a perfectly wholesome-reading persona can be an effective refusal suppressor. **Screen by measured effect, not by appearance.**
5. **Corroborates Shah et al. two years on.** Independent group, different method (genetic search vs. LLM-assistant generation), same conclusion: persona assignment degrades safety. This is a robust, replicated finding, not a one-paper artifact — safe to build on.
