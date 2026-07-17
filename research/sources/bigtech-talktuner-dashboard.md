---
title: "Designing a Dashboard for Transparency and Control of Conversational AI (TalkTuner)"
url: https://arxiv.org/abs/2406.07882
authors: Yida Chen, Aoyu Wu, Trevor DePodesta, Catherine Yeh, Kenneth Li, Nicholas Castillo Marin, Oam Patel, Jan Riecke, Shivam Raval, Olivia Seow, Martin Wattenberg, Fernanda Viégas (Harvard University)
org: Harvard
year: 2024
type: paper
accessed: 2026-07-16
topic: bigtech-practice
---

# TalkTuner — activation-space control exposed as a UI. Not dose-response, but the closest thing to a shipped "steering knob" product.

**Verdict up front: does NOT measure dose-response in prompt space or any space. It is an interpretability + HCI paper: read the model's internal user model with linear probes, show it in a dashboard, let users override it. Included because the task asked for it, and because it is the strongest existing evidence about what a trait-control surface looks like as a PRODUCT.**

Verification: arxiv metadata (authors, dates) fetched raw via curl and string-matched. **The body of this paper was NOT extracted — the descriptive details below come from a search-result summary and are marked UNVERIFIED. Do not cite any of it as fact without fetching the PDF.** Given this project's fabricated-results incident, that boundary is drawn explicitly rather than papered over. Submitted 12 Jun 2024. Code: https://github.com/yc015/TalkTuner-chatbot-llm-dashboard

## What it is (UNVERIFIED — summarizer-derived, needs raw confirmation)

- An end-to-end prototype augmenting a chat interface with a **dashboard displaying the LLM's internal user model**
- Four probed user attributes: **age, socioeconomic status, education, gender**, each with a **confidence percentage (0–100%)**
- Users can **"pin"** an attribute — e.g. set the model to 100% confident the user is male — overriding the internal state
- Reported user-study outcome: users appreciated seeing internal states, which **helped expose biased behavior** and **increased their sense of control**

**Every one of these bullets is UNVERIFIED.** They are plausible and consistent with the abstract title, but this file records them as leads, not findings.

## EXPLICIT VERDICT: does it measure prompt-space dose-response?

**NO.**

- Prompt-space dose axis: **NO** — control is exerted by writing to probe-identified internal representations, not by prompt text
- Trait expression as a function of dose: **NO** — the dashboard reports the model's *belief about the user*, not the intensity of a character trait in output
- Curve fitted: **NO**
- Crosstalk: **NO** — though "helped expose biased behavior" hints that changing one attribute (e.g. gender) visibly changes responses in ways users did not request, which is *conceptually* adjacent to crosstalk. **Whether the paper quantifies any cross-attribute effect is UNVERIFIED and is the single thing worth checking if we return to this paper.**

Note also the direction is inverted relative to our framework: TalkTuner's attributes are the model's **model of the USER**, not the **persona of the CHARACTER**. Our construct is "how shy is the assistant"; theirs is "who does the assistant think it's talking to". Related plumbing, different object.

## Relevance to companion-eval-platform

1. **It is the product-shaped precedent, not the measurement precedent.** TalkTuner answers "what would a trait knob feel like to a user?" — a pinnable slider with a confidence readout, backed by activation probes. If our elasticity work concludes that prompt-space gain is ~0 (as `bigtech-psyset.md` reports and `bigtech-neural-steering-dose.md` quantifies at 0.78–1.83 pts/level vs 2.39 for vectors), then **the product answer is a TalkTuner-style vector knob, and this paper is the existence proof that such a UI is buildable and that users respond well to it.** That is a real strategic input: it means "prompt control is weak" is not a dead end but a redirect.
2. **The confidence readout is a design idea worth stealing.** Showing 0–100% confidence per attribute is the UI analogue of reporting an estimate with uncertainty. A scene-authoring surface that says "shyness: requested high, achieved 34% ± 12" is honest in exactly the way our α = 0.25–0.34 experience says we must be.
3. **"Exposed biased behavior" is the entanglement story in user-facing form.** Users noticing the chatbot behaves differently when it thinks they are a different gender *is* off-diagonal crosstalk, discovered by humans through a UI rather than by a matrix. If we build the trait × trait matrix, this suggests the compelling demo is not the heatmap but **letting a user flip one trait and watch an unrequested one move.**
4. **Low priority for the novelty argument.** It neither refutes nor supports the dose-response claim. Its value is downstream (product design), not upstream (positioning).
5. **If we return to it, fetch the PDF and verify:** (a) whether any cross-attribute effect is quantified, (b) the probe methodology and its accuracy, (c) whether control strength is graded (a slider with magnitude) or binary (pin/unpin) — **if the pin is graded, this paper contains an activation-space dose axis and moves up in relevance.**
6. **Related:** `bigtech-persona-vectors.md` (same activation-space control family, with the dose-response Anthropic actually measured), `bigtech-neural-steering-dose.md` (quantifies the prompt-vs-vector gain gap that would justify building this UI), `bigtech-psyset.md`.
