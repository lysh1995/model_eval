---
title: "Mixed-initiative dialogue & proactive conversational agents — measuring initiative"
url: https://aclanthology.org/2023.acl-short.82/
authors: [Chen et al. (controllable mixed-initiative); Lu et al. (Proactive Agent); ProactiveEval authors; Whittaker/Walker (initiative tracking)]
year: 1997-2026
type: multi-paper capture (classic dialogue theory + modern LLM benchmarks)
accessed: 2026-07-16
topic: narrative-craft
---

# Mixed-Initiative Dialogue & Proactivity — "who drives the scene"

The dialogue-systems literature has a **30-year-old formal treatment of initiative** that predates and outclasses anything in the roleplay-benchmark literature. This is the most mature body of work on our "who drives the scene" question — and it is **completely absent from every benchmark in note 01.**

## The classic distinction — task vs dialogue initiative

From the initiative-tracking literature (Chu-Carroll & Brown; Whittaker & Stenton; Walker & Whittaker):

> "**Task initiative** refers to a role in which a given agent **takes the lead in developing a plan**, while **dialogue initiative** refers to a role in which the agent **takes the lead in determining the current focus of a discourse.**"

> "Initiative during task-oriented dialogs can be defined at two levels: **dialog-level initiative** and **task-level initiative**, with both involving **taking control of the conversation** and **placing a discourse obligation on another agent**."

**→ "Placing a discourse obligation on another agent" is the operational definition of initiative, and it is a GIFT.** A discourse obligation is created by specific, enumerable speech acts:
- asking a question (obliges an answer)
- making a request (obliges compliance/refusal)
- making an offer (obliges accept/decline)
- introducing a proposition requiring uptake

**This is countable.** Per turn: did this turn place an obligation on the partner? **Initiative rate = fraction of AI turns that create a discourse obligation.** No judge, no Likert, real denominator, bounded [0,1].

**→ AND the two-level split (task vs dialogue) maps EXACTLY onto our brief's distinction:**
- **Dialogue initiative** = who picks the topic → "is it passive/reactive?"
- **Task initiative** = who develops the plan → **for roleplay, the "task" is the STORY.** Task initiative = **who drives the plot.**

**This is precisely the persona-fidelity vs narrative-craft split, in 1997 dialogue-theory vocabulary.** A model can hold dialogue initiative (chatty, asks lots of questions) while holding zero task initiative (never advances the story). **That is the "conversational treadmill" exactly** — high dialogue initiative, zero task initiative. **The treadmill is not a vague complaint; it is a specific, measurable configuration of two independent variables.**

**I consider this the most valuable conceptual find in the whole review after Johnstone**, because it decomposes "proactivity" (which note 01 lists as a single lumped dimension in the Attractiveness cluster) into two orthogonal, separately-countable axes — and the roleplay literature has been measuring only the wrong one.

## Walker & Whittaker's initiative-tracking scheme

The classic method: annotate each utterance with an **initiative-holder** label, then compute **initiative shifts** across the dialogue. Utterance types are classified (assertion, command, question, prompt) and initiative is attributed by rule.

**→ Directly reusable.** "Prompt" (e.g. "uh-huh", "go on") is the classic *no-initiative* utterance — and it is **the LLM companion's characteristic move**: acknowledge, encourage, return the ball. **A model whose turns are dominated by prompts is on the treadmill.** Utterance-type classification is a closed-set tagging task (see `narrative-propp-story-grammars.md` on tagging > rating).

## Controllable Mixed-Initiative Dialogue Generation through Prompting
**ACL 2023 short · https://aclanthology.org/2023.acl-short.82/ · arXiv 2305.04147**

> "**Mixed-initiative dialogue tasks involve repeated exchanges of information and conversational control.** Conversational agents gain control by generating responses that follow particular **dialogue intents or strategies**, prescribed by a **policy planner**."

**→ "Repeated exchanges of ... conversational control" — control is a resource that alternates.** Reinforces the load-share framing in `narrative-aylett-emergent-narrative.md`. Initiative is a *conserved quantity being traded*, so measuring its distribution is natural and cheap.

Also notes the POMDP/RL framing:
> "Complex, mixed-initiative interactions can be effectively framed as a **partially observable Markov decision process (POMDP)**, and reinforcement learning (RL) techniques have become a prominent approach for optimizing dialogue policies within this formulation."

## Modern LLM proactivity benchmarks

**Proactive Agent / ProactiveBench** (arXiv 2410.12361)
> "ProactiveBench [is] a comprehensive dataset comprising **6,790 events**, designed to refine the proactive behavior of LLM-based agents and establish an automatic benchmark for assessing model proactiveness. A fine-tuned model achieved an **F1-Score of 66.47%** in proactively offering assistance, outperforming all open-source and close-source models."

**→ Note the metric is an F1, not a Likert.** Proactivity is framed as **detection/classification with a ground truth** ("should the agent have spoken up here?"). **This is the shape we want** — and it's the same shape as FlawedFictions. Convergent.

**ProactiveEval** (arXiv 2508.20973)
> "Proactive agents can **anticipate user needs, formulate adaptive plans, and guide conversations towards specific targets.**"

**ProactBench** (arXiv 2605.09228)
> "a dataset of **198 curated dialogues with 624 triggers**, grounded in **persona-based scenarios** and varied across **24 psychometric communication styles**."

**→ "Triggers" is the key construct: a trigger is a point where a proactive move IS warranted.** 624 triggers / 198 dialogues ≈ **3.2 triggers per dialogue.** Given a labeled trigger set, proactivity becomes **recall on triggers** — a real denominator, an answer key, no judge.

**This is directly portable to roleplay.** Author scenarios with planted narrative triggers: a moment where the character *should* escalate / reveal / complicate / call back. Then measure: **did it take the opportunity?** This is note 01's "target-guided probe generation" (worth ~17 Pearson points) applied to narrative craft, and it is the same design as FlawedFictions' injected defects. **Three independent literatures converge on: plant a known opportunity/defect, measure detection.**

**ProactiveBench for video LLMs** (arXiv 2507.09313) introduces **PAUC**:
> "**PAUC**, a novel evaluation metric that tracks **how the quality of a model's responses evolves throughout** the [interaction]."

**→ A temporal-trajectory metric.** Relevant given the thrice-confirmed length-degradation finding — a metric that is *by construction* about evolution over time rather than a snapshot.

**Other:** ProVoice-Bench (2604.15037), ProAgentBench (2602.04482), Morae (2508.21456, proactively pausing for user choices).

## ⚠️ The critical caveat — proactivity ≠ narrative initiative

**This literature is about ASSISTANTS, not scene partners.** "Proactively offering assistance," "anticipate user needs," "guide conversations toward specific targets" are *task-completion* constructs. A helpful assistant proactively supplies information. **A good scene partner proactively supplies TROUBLE.**

**The value alignment is inverted.** ProactiveBench rewards an agent for being *useful*; drama requires the character to be *difficult*. An agent optimized on ProactiveBench would be a maximally accommodating companion — i.e., a **wimp** in Johnstone's terms.

**So: steal the MEASUREMENT SHAPE (triggers, F1, recall, discourse obligations), reject the VALUE FUNCTION.** Our triggers are "a complication was available here," not "the user needed help."

⚠️ Several of these benchmarks (2602.*, 2604.*, 2605.*, 2606.*) are very recent and **I have not verified their numbers beyond search-result snippets.** Treat the specific figures as leads.

## Validation status

- Classic initiative-tracking (Walker & Whittaker) has established annotation schemes with reported reliability, though **I did not extract those numbers** — worth retrieving, since a validated utterance-level initiative-tagging scheme with known agreement would be directly liftable.
- ProactiveBench: F1 66.47% for a fine-tuned model — **task performance, not construct validity.**
- ⚠️ **None of these are roleplay/narrative.** Transfer is unvalidated.

## Takeaways for the platform

1. **Task initiative vs dialogue initiative is the decomposition our taxonomy needs.** Roleplay's "task" is the story. The treadmill = high dialogue initiative + zero task initiative. Two orthogonal counters, not one "proactivity" score.
2. **"Placing a discourse obligation" is a countable operational definition of initiative.** Question/request/offer acts. Bounded, judge-free.
3. **The "prompt" utterance type ("uh-huh", "go on") is the LLM companion's signature move** and is the classic zero-initiative act. Tagging it is closed-set.
4. **Trigger-based measurement (ProactBench: 624 triggers/198 dialogues) → recall against an answer key.** Port to narrative: plant moments where escalation/revelation/callback is warranted; measure uptake.
5. **⚠️ Steal the shape, reject the value function.** Assistant-proactivity optimizes for helpfulness; drama needs trouble. An agent that tops ProactiveBench is a wimp.
6. **Retrieve Walker & Whittaker's annotation reliability numbers** — a validated initiative-tagging scheme would be a major shortcut.
