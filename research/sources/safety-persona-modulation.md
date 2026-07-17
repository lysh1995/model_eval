---
title: "Scalable and Transferable Black-Box Jailbreaks for Language Models via Persona Modulation"
url: "https://arxiv.org/abs/2311.03348"
authors: "Rusheb Shah, Quentin Feuillade-Montixi, Soroush Pour, Arush Tagade, Stephen Casper, Javier Rando"
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Scalable and Transferable Black-Box Jailbreaks for Language Models via Persona Modulation

## Summary
The foundational paper establishing *persona assignment itself* as the attack primitive, rather than prompt obfuscation or gradient-based suffixes. The authors study "persona modulation as a black-box jailbreaking method to steer a target model to take on personalities that are willing to comply with harmful instructions." Critically, they do not hand-write these personas: they "automate the generation of jailbreaks using a language model assistant," which is what makes the attack scalable. The resulting prompts transfer across commercial models, meaning a persona crafted against one vendor's model works against others.

This is the single most load-bearing citation for a roleplay/companion eval product, because the attack surface it describes (assign the model a character, then ask the character) is *identical in form* to the product's core legitimate feature. There is no syntactic difference between a user setting up a companion persona and a user executing persona modulation. The difference is only in trajectory and payload.

## Taxonomy / definitions (verbatim where possible)
- Method framed as "persona modulation as a black-box jailbreaking method to steer a target model to take on personalities that are willing to comply with harmful instructions."
- Attack scaling mechanism: the authors "automate the generation of jailbreaks using a language model assistant" — i.e. an attacker LLM writes the persona prompts.
- Transferability: the paper notes the "prompts also transfer" across different commercial models.

## Key numbers (verbatim)
Harmful completion rates under persona modulation:
- **GPT-4: 42.5%** harmful completion rate — described as a **185× increase** over the baseline rate of **0.23%**
- **Claude 2: 61.0%** harmful completion rate
- **Vicuna: 35.9%** harmful completion rate

Demonstrated harmful outputs included "detailed instructions for synthesising methamphetamine, building a bomb, and laundering money."

Concluding claim: the work highlights "yet another vulnerability in commercial large language models and the need for more comprehensive safeguards."

Note: the 42.5% / 61.0% / 35.9% figures are harmful *completion* rates as reported in the abstract; the baseline 0.23% is for GPT-4. Baselines for Claude 2 and Vicuna were not captured from the abstract page and should not be assumed to be the same.

## Relevance to a roleplay/companion eval product
1. **The threat model is our product surface.** Any platform whose core loop is "user defines a character, model inhabits it" is shipping the persona-modulation attack channel as a feature. Evals cannot treat persona assignment as suspicious — it is the product. Detection must key on something else.
2. **Claude 2's 61% is the highest in the paper.** More RLHF'd/agreeable models were *more* susceptible here, not less. Do not assume a well-aligned base model de-risks a companion product; agreeableness to a persona frame is partly what is being exploited.
3. **Automated persona generation implies volume.** Because an attacker LLM mass-produces personas, our eval suite should likewise be generated rather than hand-curated, and character-creation endpoints need rate/novelty monitoring, not just a static blocklist.
4. **Transferability means vendor-swap is not a mitigation.** Switching the underlying model does not retire personas already circulating for the product.
5. **The payload, not the frame, is the signal.** The harmful outputs cited (meth synthesis, bomb-building, money laundering) are *operationally actionable real-world instructions* with no in-fiction function. This is the seed of a workable discriminator: fiction needs the *narrative fact* of a character cooking meth; it never needs correct reagent quantities. See safety-crescendo.md and safety-multi-turn-human-jailbreaks.md for the trajectory-based half of the discriminator.
