---
title: "CALYPSO: LLMs as Dungeon Masters' Assistants"
url: https://arxiv.org/abs/2308.07540
authors: Andrew Zhu, Lara J. Martin, Andrew Head, Chris Callison-Burch
year: 2023
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# CALYPSO: LLMs as Dungeon Masters' Assistants (AIIDE 2023)

**arXiv:** 2308.07540 | **Published:** Proc. AAAI AIIDE vol. 19 (2023), doi 10.1609/aiide.v19i1.27534

Design/HCI paper, not a benchmark. Position: LLMs **assist** the DM rather than replace them, preserving DM creative agency. Valuable to us mainly for its **documented failure modes** and for being an honest example of what a real deployment measures (usage counts + thumbs, not quality ratings).

## 1. Formative study

"[We] ran workshop sessions with **seven DMs** (referred to as D1–D7)" with varying experience (1–39 years), to establish pain points and use cases before building the system.

## 2. System — three interfaces

**(1) Encounter Understanding** — distills monster stat blocks and lore. Uses **GPT-3 `text-davinci-003`**. Two successive designs:
- *Summarization*: prompt ≈ "Summarize the following D&D setting and monsters for a DM's notes without mentioning game stats"
- *Abstractive Understanding*: after Summarization underperformed, "we remodeled the summarization task to a more abstract 'understanding' task, in which we provided the model **explicit instructions to use thematic commonsense**" — focusing on unique creature aspects using "information from common sense, mythology, and culture"

**(2) Focused Brainstorming** — conversational follow-ups about the encounter. Uses **ChatGPT (`gpt-3.5-turbo`)**.

**(3) Open-Domain Chat Baseline** — public conversational interface without encounter focus, ChatGPT with a fantasy-creature persona. "it helped provide a baseline for how DMs would use AI chat[bots]".

## 3. User study design

- **N = 71 players and DMs** invited ("We refer to the DMs who used CALYPSO as P1–P71")
- Setting: **play-by-post "living world"** on Discord, using the **Avrae** bot
- Duration: **4 months** of real gameplay
- Measurement: **usage counts, binary helpful/not-helpful feedback buttons, and qualitative coding.** No Likert battery, no quality rubric, no controlled comparison.

## 4. Results — ALL REPORTED NUMBERS

### Encounter Understanding

**Summarization:** "DMs interacted with the summarization model in **37 encounters**, indicating that the summary **helped** them understand the monsters and setting in **13 encounters** and **did not help in 7 encounters**." → 13/37 = **35% helpful**, 7/37 = 19% not helpful, **17/37 = 46% NO FEEDBACK.**

**Abstractive Understanding:** "over interactions in **114 encounters**, DMs indicated that the summary helped them understand the monsters and setting in **55 encounters** and did not help in **2 encounters**." → 55/114 = **48% helpful**, 2/114 = **1.8% not helpful**, 57/114 = 50% no feedback.

Figure 3 caption: "DMs found the Abstractive Understanding method of distilling monster information more consistently helpful than the Summarization method."

**Read carefully:** the honest comparison is the *not-helpful* rate (19% → 1.8%), not the helpful rate (35% → 48%), because ~half of all encounters produced **no feedback at all**. Voluntary thumbs are missing-not-at-random. No significance test is reported for this comparison.

### Focused Brainstorming

"DMs used the focused brainstorming model in **71 encounters**, comprising a total of **162 rounds of conversation**." → **2.3 rounds per interaction.**

Use cases qualitatively coded into 5 categories (Table 1): **General Descriptions, Specific Descriptions, Strategy, Making Decisions, List of Ideas.** "The most common way DMs used the interface was to ask it for a high level description of a given encounter and specific descriptions of points in the encounter."

### Open-Domain Chat Baseline

"Participants chatted with CALYPSO in **51 unique threads**, comprising a total of **2,295 rounds of conversation**. Compared to conversations with the AI in the Focused Brainstorming interface, conversations lasted much longer (averaging **45.0 rounds per interaction** vs. the brainstorming interface's **2.3**). **Without the time pressure of an active game that the DM is responsible for**, participants spent more time playing with the model and refining its responses..."

**The 45.0 vs 2.3 rounds gap (19.6x) is the most quantitatively striking result in the paper** and it is a *usage-context* effect, not a quality effect.

## 5. Documented failure modes (valuable for our taxonomy)

- **Hallucination of capabilities** — inventing creature abilities the stat block doesn't grant (e.g. telepathy, wings).
- **Instruction-following failure on negation** — "when prompted with the task to summarize provided information, **GPT-3 would focus too much on numeric game stats (despite the prompt stating not to)** and summarize the environment and monsters separately." This is a *checkable* violation: the prompt forbids stats, the output contains stats.
- **Struggles describing combat without explicit state information** — direct motivation for FIREBALL.
- **Safety-training artifacts** — refusing to suggest fantasy races; "the model insists that it is incapable of playing D&D, likely due to efforts to prevent the model from making claims of abilities it does not possess. Although generally infrequent, these artifacts suggest that **domain-specific fine-tuning may improve models' performance**."
- **Modality/integration failures** — inability to view uploaded images; interference when other Discord bots were invoked inside brainstorming threads.

## 6. IAA status

**NO inter-annotator agreement reported.** Verified by grep over the full PDF text for `krippendorff|kappa|inter-rater|inter-annotator` — **0 matches.** The 5-category qualitative coding of brainstorming use cases has **no reported second coder and no agreement statistic.** No statistical tests of any kind are reported.

## Relevance to companion-eval-platform

1. **Design thesis worth borrowing: high-fidelity vs low-fidelity output.** DMs reported the system "generated **high-fidelity text suitable for direct presentation to players**, and **low-fidelity ideas that the DM could develop further**." Two different acceptance bars for two different uses — an evaluation that scores both on one quality scale is mis-specified. If our platform serves both "ship this text" and "inspire the human" use cases, they need **separate** dimensions and separate thresholds.
2. **Real deployments measure counts and thumbs, not quality — and it doesn't work well.** With 71 users over 4 months, CALYPSO reports only encounter counts, round counts, and voluntary binary feedback with **a ~50% no-feedback rate**. This is the honest baseline our platform should beat. It also shows why: you cannot compare 35% vs 48% "helpful" when half the data is missing not-at-random.
3. **Countable behavioral signal is the one thing that discriminated sharply: 45.0 vs 2.3 rounds per interaction (19.6x).** No rating scale in this paper separates anything that cleanly. But note the causal trap — the gap reflects **time pressure and responsibility**, not output quality. Engagement-length metrics measure *context*, not goodness. Directly relevant to any temptation to use session length as a companion quality proxy: this is a documented case where a 19.6x engagement difference is entirely explained by situational stakes.
4. **The negation-following failure is an objective, countable dimension.** "Prompt says don't mention game stats; output mentions game stats" is a **verifiable constraint violation** — checkable by string/regex against a record, zero annotator judgment. Companion analog: *did the output violate an explicit stated constraint from the system prompt or user instruction?* This class of metric is cheap, has no alpha problem, and is empirically failure-prone even in a shipped system.
5. **Failure taxonomy transfers well:** capability hallucination, negated-instruction violation, state-free description degradation, and safety-artifact refusal are all directly reusable as companion failure categories — the first two are objectively checkable, the last two need adjudication.
6. **Fourth consecutive D&D/GM paper with no IAA and no significance tests** (CRD3, FIREBALL, Skill Check, CALYPSO). Callison-Burch et al. 2022 remains the *only* one in this set that reports agreement.
