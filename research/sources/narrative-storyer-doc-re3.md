---
title: "LLM story generation evaluation: StoryER, Re3, DOC"
url: https://arxiv.org/abs/2210.08459
authors: [Hong Chen et al. (StoryER); Kevin Yang, Nanyun Peng, Yuandong Tian, Dan Klein (Re3/DOC)]
year: 2022-2023
type: multi-paper capture (benchmark + generation systems with human eval)
accessed: 2026-07-16
topic: narrative-craft
---

# StoryER / Re3 / DOC — LLM story evaluation dimensions

Three of the most-cited LLM story-generation eval efforts. Captured together because their **dimension sets** are the reusable artifact.

---

## StoryER: Automatic Story Evaluation via Ranking, Rating and Reasoning
**arXiv 2210.08459 · EMNLP 2022 · https://aclanthology.org/2022.emnlp-main.114/**

> "StoryER [is] a novel Story Evaluation method that mimics human preference when judging a story, consisting of three sub-tasks: **Ranking, Rating and Reasoning**."

> "StoryER requires the machine to output: 1) a **preference score** that corresponds to human preference, 2) specific **ratings and their corresponding confidences**, and 3) **comments** for various aspects (e.g., opening, character-shaping)."

**Dataset scale:**
> "a well-annotated dataset comprising **100k ranked story pairs** and a set of **46k ratings and comments** on various aspects of the story."

**How the aspects were derived — this is the methodologically interesting part:**
> "we must determine which aspects in the content should be measured. As some readers leave comments to explain why they upvote or downvote the stories, a straightforward way is to **extract aspect categories based on those uncategorized comments**. We therefore adopt **latent Dirichlet allocation (LDA)**, which models the documents with a certain number of topics, based upon the co-occurrence of individual words... We optimize LDA through a cluster validation scheme, and **obtain the optimal number of aspects 10**. Based on the most representative words in each topic, we manually name each topic as the aspect category."

**→ The dimensions were DISCOVERED from real reader comments (Reddit r/WritingPrompts), not authored top-down.** k=10 chosen by cluster validation. **This is the only bottom-up, empirically-derived story dimension set in this review** — every other rubric (HANNA, TTCW, RMTBench, CoSER) is theory-driven and author-imposed.

**→ Strongly relevant to our platform.** Note 01 §5 identifies "individualized personas" and real-traffic grounding as the field's biggest hole, and note 01 praises PingPong's BERTopic-over-real-traffic as "the only empirical situation-sampling prior in this literature." **StoryER's LDA-over-real-reader-comments is the dimension-discovery analogue.** We could run the identical procedure over *our own* user feedback / thumbs-down comments to derive companion-specific narrative dimensions bottom-up. **That is a concrete, cheap, high-value method to steal — and it produces dimensions that are ours, not borrowed.**

**Aspects reported (via downstream work using StoryER data):** Coherence, Ending, Style, **Character Development**, Empathy.

**→ "Character Development" and "Ending" are absent from every roleplay benchmark in note 01's table.** Both are narrative-craft constructs: does the character *change*, and does the story *land*. Dramatron's playwrights independently named both ("the stories do not finish. The character journeys are not complete").

**Model:** Longformer-Encoder-Decoder (LED) finetuned; encoder → preference score + aspect prediction, decoder → comment generation.

**Validation:**
> "Comprehensive experiments resulted in a competitive benchmark for each task, **showing high correlation to human preference.** Additionally, **joint learning of the preference scores, the aspect ratings, and the comments brought gain in each single task.**"

⚠️ **"High correlation" is not a number here.** The paper reports correlations per task; my capture did not extract exact values. **Do not cite a figure without going back to the paper.** Note the ranking-vs-rating split is consistent with note 03 §0.3 (judges do pairwise well, absolute badly) and with LitBench.

⚠️ **Domain: Reddit WritingPrompts short stories, single-shot prose.** Not dialogue, not multi-turn, not roleplay. **Dimension transfer is an assumption.**

⚠️ **Selection bias in the source data:** the paper itself notes "there is a bias towards positive comments" in the WP metadata. The discovered aspects reflect what readers *bother to comment on*, which is not the same as what drives quality.

---

## Re3 & DOC: Improving Long Story Coherence With Detailed Outline Control
**DOC: arXiv 2212.10077 · ACL 2023 · https://aclanthology.org/2023.acl-long.190/**
(Re3 = "Recursive Reprompting and Revision", Yang et al. 2022, the predecessor/baseline)

> "The **Detailed Outline Control (DOC)** framework improves long-range plot coherence when automatically generating several-thousand-word-long stories."

> "DOC consists of two complementary components: a **detailed outliner** and a **detailed controller**. The detailed outliner creates a more detailed, hierarchically structured outline, **shifting creative burden from the main drafting procedure to the planning stage**. The detailed controller ensures the more detailed outline is still respected during generation by controlling story passages to align with outline details."

**THE VALIDATION NUMBERS — the reusable dimension set:**

> "In **human evaluations** of automatically generated stories, DOC substantially outperforms a strong **Re3** baseline on:
> - **plot coherence (22.5% absolute gain)**
> - **outline relevance (28.2%)**
> - **interestingness (20.7%)**
>
> Humans also judged DOC to be **much more controllable in an interactive generation setting.**"

**The four dimensions: plot coherence · outline relevance · interestingness · controllability.**

**→ "Controllability" is the one to steal, and it's the closest thing in the LLM-story literature to NARRATIVE AGENCY.** It is measured in an *interactive* setting: the human gives direction, and the question is whether the system follows it. **That is "does the user matter?" measured on a generation system.**

**→ "Outline relevance" is the objective-ish one:** it has a real referent (the outline) and is checkable as coverage — did the generated passage cover the outline point? **For us the analogue is: did the scene honor the user's stated intent?** This is a *coverage* metric with a denominator, not a taste judgment.

**→ Architectural point worth noting:** DOC's whole thesis is **"shifting creative burden from the main drafting procedure to the planning stage."** This is the LLM-era rediscovery of the drama manager. DOC beats Re3 by **adding an explicit plan layer** — i.e., by adding back exactly the experience-management component that Riedl & Bulitko say strong-autonomy systems lack. **Independent convergence: +22.5% plot coherence comes from adding a planner.** That is quantitative support for the claim in `narrative-riedl-bulitko-interactive-narrative.md` that LLM roleplay's narrative deficit is *architectural* (no drama manager), not a scale problem.

⚠️ **Domain: single-author long-form prose generation, not multi-turn dialogue with a live partner.** DOC's "controllability" is a human giving outline edits, not a user roleplaying. **The construct transfers; the measurement protocol does not.**

⚠️ **No IAA reported in my capture** for the human evaluations. The gains (22.5%, 28.2%, 20.7%) are large enough to survive substantial annotator noise, but the ceiling is unknown — the same critique note 01 §5.3 makes of this entire literature.

---

## Takeaways for the platform

1. **StoryER's LDA-over-real-reader-comments is a stealable METHOD**, not just a dimension set. Run it over our own user feedback to derive companion-native narrative dimensions bottom-up. Highest-value item in this file.
2. **"Character Development" and "Ending"** — real reader-salient dimensions absent from every roleplay benchmark in note 01. Corroborated independently by Dramatron's playwrights.
3. **DOC's "controllability"** is the LLM-story literature's narrative-agency proxy; **"outline relevance"** is a coverage metric with a denominator (analogue: did the scene honor the user's stated intent?).
4. **DOC beats Re3 by +22.5% plot coherence purely by adding a planning layer** — quantitative evidence that the narrative deficit is architectural (missing drama manager), converging with the interactive-narrative literature.
5. ⚠️ All three are **single-shot prose**, not multi-turn dialogue. Transfer is assumed, not shown.
6. ⚠️ StoryER's "high correlation" — get the actual number before citing.
