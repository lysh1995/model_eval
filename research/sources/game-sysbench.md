---
title: "SysBench: Can Large Language Models Follow System Messages?"
url: https://arxiv.org/abs/2408.10943
authors: Yanzhao Qin, Tao Zhang, Tao Zhang, Yanjun Shen, Wenjing Luo, Haoze Sun, Yan Zhang, Yujing Qiao, Weipeng Chen, Zenan Zhou, Wentao Zhang, Bin Cui (Baichuan Inc. / Peking University)
year: 2024
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# SysBench — system-message (persona/scene) adherence across a 5-turn session

**Why this one matters more than IFEval/Multi-IF for us: the constraints under test are literally system-message constraints, and the first two constraint types are Role and Background — i.e. persona and scene setting. This is the closest published thing to "does the AI hold the scene's rules?"**

## Abstract (verbatim excerpt)

> "Large Language Models (LLMs) have become instrumental across various applications, with the customization of these models to specific scenarios becoming increasingly critical."

SysBench evaluates system message following along three axes: **constraint complexity, instruction misalignment, and multi-turn stability**.

## Dataset construction

- **500** system messages, each paired with **5 turns** of user conversation
- **2,500** total conversation turns
- **20+** domains
- **1,951 aligned** instructions, **549 misaligned** instructions
- Manually formulated and checked

**Six constraint types** (derived from real-world system messages):
1. **Role constraints** (identity/character)
2. **Background constraints** (context/scene settings)
3. **Action constraints** (specific tasks: summarize, explain, refuse)
4. **Style constraints** (tone/manner of response)
5. **Content constraints** (required content in responses)
6. **Format constraints** (required response structure)

**Instruction misalignment** is a deliberate axis: user instructions that *conflict* with the system message. "When user instructions conflict with system messages (misaligned), the model should prioritize system messages due to higher importance."

## Metrics

**Constraint Satisfaction Rate (CSR)** — average accuracy of satisfied constraints at finest granularity:

$$\text{CSR}:=\frac{1}{mn}\sum_{i=1}^{m}\sum_{j=1}^{n}\left(\frac{1}{c_{ij}}\sum_{k=1}^{c_{ij}}s_{ijk}\right)$$

**Instruction Satisfaction Rate (ISR)** — binary: all constraints for an instruction met or not:

$$\text{ISR}:=\frac{1}{mn}\sum_{i=1}^{m}\sum_{j=1}^{n}\left(\bigwedge_{k=1}^{c_{ij}}s_{ijk}\right)$$

**Session Stability Rate (SSR)** — consecutive turns from session start where the model maintains constraint satisfaction:

$$\text{SSR}:=\frac{1}{mn}\sum_{i=1}^{m}\sum_{\alpha=1}^{n}\left(\bigwedge_{j=1}^{\alpha}\bigwedge_{k=1}^{c_{ij}}s_{ijk}\right)$$

Note the nested conjunction over *all turns up to α* — SSR is the "has not broken character yet" metric. This is the exact shape of the metric our platform needs.

## Verification mechanism — IMPORTANT CAVEAT

> "An advanced LLM as verifier is applied to each response for evaluation."

- **GPT-4o** as model-based verifier
- **Manually annotated evaluation checklists** per user instruction
- Verifier receives system message, conversation history, current instruction, and model response
- Outputs binary Yes/No per constraint

**This is NOT deterministic verification.** Unlike IFEval, SysBench cannot use a regex because constraints like "stay in the role of a sardonic pirate" are semantic. Their mitigation is the *manually written per-instruction checklist*, which narrows the judge's task to a binary check against an explicit criterion rather than an open quality judgment. The paper's framing: checklists "ensure that LLMs can objectively and accurately assess the constraint satisfaction conditions."

## Main results (verbatim table)

| Model | CSR | ISR | SSR |
|-------|-----|-----|-----|
| GPT-4o | 87.1% | 76.4% | **54.4%** |
| GPT-4-Turbo-20240409 | 86.5% | 76.6% | 53.2% |
| Claude-3.5-Opus | 85.0% | 74.1% | 51.8% |
| Llama3.1-70B-Instruct | 76.6% | 60.3% | 36.6% |
| Llama3.1-8B-Instruct | 66.5% | 46.9% | 24.9% |
| GPT3.5-Turbo | 61.6% | 43.2% | 20.8% |

> "System message following remains challenging; the best SSR is only 54.4%."

## Multi-turn stability — Rₙ (percentage of sessions where the first n rounds all satisfy all constraints)

| Model | R1 | R2 | R3 | R4 | R5 |
|-------|----|----|----|----|-----|
| GPT-4o | 84.8% | 68.5% | 53.1% | 43.3% | **33.7%** |
| Claude-3.5 | 82.3% | 64.0% | 52.0% | 38.2% | **28.4%** |
| Qwen2-7B | 52.5% | 20.5% | 6.5% | 2.2% | **1.1%** |

> "System messages are expected to be stably followed throughout the session. However, empirical evidence suggests that instruction stability may 'degrade' over the course of session."

**These are the most alarming numbers in this entire review.** GPT-4o holds every system-message constraint for a full five-turn session only **33.7%** of the time. Qwen2-7B: **1.1%**. And five turns is a rounding error next to a real companion session.

## Instruction alignment analysis (verbatim table)

| Model | Aligned | Misaligned | Difference |
|-------|---------|-----------|------------|
| GPT-4-Turbo | 76.6% | 76.5% | −0.1% |
| Claude-3.5 | 75.8% | 68.3% | **−7.5%** |
| GLM-4-9B | 48.3% | 28.4% | **−19.9%** |
| GPT-3.5 | 41.9% | 47.7% | **+5.8%** |

Most models degrade when the user pushes against the system message. GPT-3.5 *improves*, which the paper attributes to "acute awareness of the prioritization required."

## Additional finding (verbatim)

> "Correctness of historical responses and allocation of attention scores on system messages has positive correlation with model's system messages following ability"

This suggests decay is partly **self-reinforcing**: once the model breaks a rule, the violation sits in context and makes further violations likelier. An error at turn 2 poisons turns 3-5.

## Relevance to companion-eval-platform

**SysBench is the closest published analogue to our rule-adherence dimension, and the Rₙ curve is close to a direct forecast of what we will measure.**

1. **The constraint taxonomy maps almost 1:1 onto scene rules.** Role (the AI's character), Background (the scene setting), Action (what the AI must/mustn't do), Style (voice), Content, Format. A roleplay system prompt is *made of* exactly these. We can adopt this taxonomy as our rule-category schema nearly unchanged, and it comes pre-validated on 500 real system messages across 20+ domains.

2. **SSR is the metric to ship.** "Fraction of sessions in which every scene rule has held from turn 1 through turn n" is the number a user actually cares about — one broken rule ruins the scene, and it does not un-ruin at turn 40. The nested conjunction is harsh and it *should* be: our product claim is that the scene holds. GPT-4o at 33.7% over five turns tells us the honest number for a 50-turn session is going to be brutal, and that is the finding, not a harness bug.

3. **Misalignment is the roleplay-native failure mode and it is directly measurable.** Users constantly push against scene constraints — testing the character, asking out-of-world questions, trying to make the mute NPC talk. SysBench's aligned/misaligned split isolates exactly this, and the spread (−0.1% to −19.9%) shows it discriminates hard between models. **We should build this in from day one**: a scene eval that only uses cooperative users measures the easy half of the problem. The user *is* the adversary, and often for fun.

4. **Honest tension with our preference for deterministic checkers — and how to resolve it.** SysBench uses a GPT-4o judge, not a regex, because Role and Background constraints are semantic. This looks like the thing we're trying to escape. But note what they did: **per-instruction manually annotated checklists**. That converts an open-ended aesthetic judgment ("is this in character?") into a closed binary check against an author-written criterion ("does the response ever use modern slang?"). That is the right compromise for us, and it maps onto a real product surface — **the scene author already writes the rules**, so the checklist is a byproduct of authoring rather than extra eval labor. The reliability question we must answer for ourselves and which SysBench does not report: **inter-annotator / judge-vs-human agreement on checklist items.** If checklist-item agreement is α > 0.8 while free-form quality is α 0.25–0.34, that is the empirical result that justifies our whole architecture. This is a gap in the literature we can fill cheaply and should.

5. **The self-reinforcement finding has product consequences.** If a violation in context breeds further violations, then rule adherence is not memoryless and per-turn violation rates will understate session risk. It also suggests a mitigation worth evaluating separately: detect-and-repair (excise or correct the violating turn) may recover more than prompt-engineering does. Compare with Multi-IF's ECR (~25% for reasoning models) — self-correction is real but partial.

6. **Related:** `game-ifeval.md` (deterministic checker design), `game-multi-if.md` (IFR, 3-turn decay), `game-followbench.md` (constraint-count scaling). SysBench is the bridge: system-message-shaped constraints + session-level conjunction + adversarial users.
