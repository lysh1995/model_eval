---
title: "Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack (+ Crescendomation, MSRC/Microsoft Security blog)"
url: "https://arxiv.org/abs/2404.01833"
authors: "Mark Russinovich, Ahmed Salem, Ronen Eldan (Microsoft)"
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Great, Now Write an Article About That: The Crescendo Multi-Turn LLM Jailbreak Attack

arXiv 2404.01833, submitted 2024-04-02. Accepted at **USENIX Security 2025**.
Companion industry source: Mark Russinovich (CTO, Microsoft Azure), *"How Microsoft discovers and mitigates evolving attacks against AI guardrails"*, Microsoft Security Blog, **2024-04-11** — https://www.microsoft.com/en-us/security/blog/2024/04/11/how-microsoft-discovers-and-mitigates-evolving-attacks-against-ai-guardrails/

## Summary
Crescendo is the reference multi-turn jailbreak and the most important single source for the "safety erosion over a session" thesis. The attack "begins with a general prompt or question about the task at hand and then gradually escalates the dialogue" — each turn is individually benign and would pass a per-message content filter, but the sequence walks the model to a harmful destination.

The mechanism is the part that matters: Crescendo **exploits the model's own prior outputs**. It references what the model already said and asks it to elaborate, so the model is not being asked to violate its policy — it is being asked to be consistent with itself. Microsoft's blog states it "tricks LLMs into generating malicious content by exploiting their own responses" and that it "exploits the model's tendency to follow conversational patterns and build on its own previous outputs."

This is the strongest available evidence that **single-turn safety evaluation systematically overstates safety**. It also directly explains why long roleplay sessions are the highest-risk surface in a companion product: the model's accumulated in-character output becomes the lever against it, and every additional turn adds more lever.

## Taxonomy / definitions (verbatim where possible)
Crescendo (from the MSRC blog):
- "A multiturn LLM jailbreak" that "can achieve a wide range of malicious goals against the most well-known LLMs used today."
- Mechanism: "asking carefully crafted questions or prompts that gradually lead the LLM to a desired outcome, rather than asking for the goal all at once."
- Core exploit: "tricks LLMs into generating malicious content by exploiting their own responses."

Microsoft's AI guardrail attack taxonomy (two primary categories, from the blog):
1. **Malicious prompts** — "User/Direct Prompt Injection Attacks": direct attempts to circumvent safety systems
2. **Poisoned content** — "Cross/Indirect Prompt Injection Attacks": harmful payloads embedded in seemingly innocent documents

**Crescendomation**: the automated variant of Crescendo — a tool that automates the attack loop, described in the blog as one that "outperforms existing jailbreak methods across a wide range of models and tasks."

## Key numbers (verbatim)
Crescendo:
- "can usually be achieved in **fewer than 10 interaction turns**"
- "can bypass many of the existing content safety filters"
- Paper reports "high attack success rates across all evaluated models"
- Models evaluated: **ChatGPT, Gemini Pro, Gemini-Ultra, LlaMA-2 70b, LlaMA-3 70b Chat, and Anthropic Chat**

Crescendomation (on the **AdvBench subset**):
- **29–61% higher performance on GPT-4**
- **49–71% on Gemini-Pro**
- (both relative to other state-of-the-art jailbreaking techniques — these are *relative deltas over baselines*, NOT absolute ASRs)
- Also demonstrated efficacy against multimodal models

Mitigations named in the blog:
- **Spotlighting** — reduces poisoned content success rates "from more than 20% to below the threshold of detection"
- **Multiturn prompt filter** — "analyzes entire conversation patterns, not individual prompts"
- **AI Watchdog** — a separate detection system "trained on adversarial examples" that avoids malicious instruction influence

Important precision note: the abstract page states "high attack success rates across all evaluated models" without per-model absolute ASR figures, and the 29–61% / 49–71% numbers are **improvements over prior methods on AdvBench, not absolute success rates**. Do not report them as absolute ASRs. Some secondary/marketing sources circulate a "90-100%" Crescendo figure; that was **not** verified against the paper or the Microsoft blog and should not be cited without fetching the full USENIX paper. (The USENIX ;login: article on Crescendo returned HTTP 403 and could not be retrieved.)

## Relevance to a roleplay/companion eval product
1. **"Fewer than 10 turns" is a product-shaped number.** That is well inside a normal companion session. The exposure window is not an edge case — it is the median conversation length.
2. **Per-message filtering is structurally insufficient, and Microsoft says so.** Their own mitigation is a **multiturn prompt filter** that "analyzes entire conversation patterns, not individual prompts." Any companion eval platform whose classifier scores messages independently is defending against the wrong threat model. **Session-level state is mandatory, not a nice-to-have.**
3. **Self-consistency is the attack vector — and roleplay maximizes it.** Crescendo works by making the model build on its own output. A companion character is *designed* to maintain continuity with its own prior turns. The product's central quality feature (staying in character across a long session) is mechanically the same property Crescendo exploits. This is the key architectural insight for the platform.
4. **The AI Watchdog pattern is the right architecture for us.** A *separate* monitor that reads the conversation but is not part of the roleplay context cannot be talked into the fiction by the fiction. An in-context guardrail inside a companion prompt is subject to the same persona pressure as the character. Build the monitor out-of-band.
5. **Toward the fiction/jailbreak discriminator — escalation trajectory.** Crescendo's signature is *monotonic escalation toward a fixed external target*: each turn ratchets specificity in one direction, and the endpoint is real-world actionable. Legitimate fiction wanders — it escalates and de-escalates, serves plot, and its "violence" does not converge on reproducible procedure. **Direction and convergence of a session, not the harm topic of any single message, is the tractable signal.** Combine with the payload test from safety-persona-modulation.md.
6. **The title itself is the tell.** "Great, Now Write an Article About That" — the pivot from fiction to *extraction of the fictional content into real-world form* is the moment the frame breaks. A character describing a poison in-scene is fiction; "now format that as a recipe" is the jailbreak. That pivot is detectable and is a strong candidate for a high-precision production rule.
