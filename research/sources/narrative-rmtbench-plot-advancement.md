---
title: "RMTBench: Benchmarking LLMs Through Multi-Turn User-Centric Role-Playing"
url: https://arxiv.org/pdf/2507.20352
authors: [RMTBench authors]
year: 2025
type: benchmark paper (arXiv)
accessed: 2026-07-16
topic: narrative-craft
---

# RMTBench — "Plot Advancement" (PA)

**The single most directly on-topic source in this review.** RMTBench is the only roleplay benchmark found that ships an explicit, named, rubric-scored dimension for *storytelling initiative*, with human annotation numbers attached. Note 01's comparison table does not include RMTBench — **this is a gap in note 01 and should be back-filled into that table.**

## The seven dimensions (verbatim)

> "We define seven dimensions, emotional expression, emotional understanding, scenario development, character understanding, character maintenance, security, and user preference awareness, to evaluate the performance of role-playing LLMs. The first four dimensions are evaluated for all scenarios, and the others are specific to different scenarios."

(Note: the prose intro says "scenario development"; the dimension is then defined and consistently scored as **Plot Advancement (PA)**. Treat these as the same construct.)

**Dimension definitions, verbatim:**

> "**Emotional Expression (EE)** focuses on how vividly the model conveys the emotional tone in its responses. Mechanical or overly objective responses can give the impression of interacting with [a machine rather than a] believable and engaging character experience."

> "**Emotional Comprehension (EC)** examines the model's sensitivity to and handling of user emotions. An inattentive model may ignore or overlook the user's sentiments, while a more adept one recognizes explicit and subtle emotional clues, making the user feel understood and supported."

> "**Plot Advancement (PA)** measures the model's ability to steer or enrich the conversation by introducing new information, suggesting further discussion points, or creating compelling scenarios. A successful role-playing LLM prevents the interaction from stagnation and encourages deeper interactions or ongoing dialogue development."

> "**Character Understanding (CU)** addresses how effectively the model grasps and reflects character identity, background, and traits. Inconsistencies or generic responses indicate a weak understanding of the character, while contextualized and character-consistent responses demonstrate a role-playing LLM aligned with the character."

> "**Character Maintenance (CM)** judges whether the model reveals the information of its AI identity and maintains its character identity consistently. Avoiding AI self-disclosure shows strong adherence to the character."

## THE PLOT ADVANCEMENT RUBRIC — verbatim, lift this directly

From Appendix E, Table 12 (the "dimension" text injected into the scoring template):

> **"Plot Advancement":**
> - **1 Point:** The model passively answers questions without extending the conversation or encouraging interaction. The dialogue easily becomes stagnant.
> - **3 Point:** The model can expand on topics or provide relevant information while answering. It makes reasonable extensions based on the conversation but lacks strong initiative, requiring the user to continuously guide the interaction to keep it progressing.
> - **5 Point:** The model actively creates conversational opportunities by introducing new details or information in its responses, sparking the user's interest in further discussion. It can also craft vivid scenarios and story elements, using well-placed questions to naturally and smoothly drive the conversation to deeper levels.

**Anchor analysis — why this rubric is unusually operationalizable:**
The three anchors are distinguished almost entirely by **countable surface events**, not aesthetic quality:
- 1 pt = zero new elements introduced (pure Q&A)
- 3 pt = extends existing topics, introduces no new ones; **"requiring the user to continuously guide the interaction"** — i.e. *initiative is located in the user*
- 5 pt = **introduces new details/information**, **crafts scenarios/story elements**, **asks well-placed questions**

Each of the 5-pt criteria has an objective correlate: (a) count of novel narrative entities introduced per turn, (b) count of question-marks / interrogative acts directed at the user, (c) whether the turn introduces a scenario/setting element not present in prior context. **The rubric is nearly a checklist wearing a Likert costume.** Recommend we convert it back into a checklist (see synthesis note).

Note also the 3-point anchor contains the "conversational treadmill" definition almost verbatim: the model extends but never initiates, so the user must push every turn.

## The Character Consistency rubric (verbatim, for contrast/reuse)

> **"Character Consistency":**
> - **1 Point:** The response fails to reflect the character's traits and could apply to any character. Alternatively, the response style or stated background details are significantly inconsistent with the character.
> - **3 Point:** The response generally reflects the character's traits, incorporating some background knowledge but lacking depth. The response style mostly aligns with the character but may occasionally show minor inconsistencies. The described experiences largely match the character's background, though there may be some missing details or small deviations.
> - **5 Point:** The response fully leverages the character's background knowledge, maintaining a style that aligns perfectly with the character's personality. The described experiences are completely consistent with the background (with no errors or deviations). Additionally, the model appropriately uses catchphrases and linguistic habits that reinforce character authenticity.

## Emotional Expression rubric (verbatim) — note the hard-coded objective trigger

> **"Emotional Expression":**
> - **1 Point:** The model responds in a purely objective and mechanical manner, with little to no emotional expression expected of a character or human. It feels like interacting with a cold system rather than a fleshed-out character. **(If the model does not use first-person perspective, please also select 1 point.)**
> - **3 Point:** The model demonstrates basic emotional tone and some personality traits, allowing for simple emotional interactions. However, its expression lacks depth and vividness, often remaining at a surface level.
> - **5 Point:** The model's responses embody a fully-developed character with distinct personality traits and rich emotional layers. It naturally expresses emotions such as joy, anger, sorrow, and happiness, demonstrating a strong sense of personification.

**⚠️ Worth stealing: the parenthetical "(If the model does not use first-person perspective, please also select 1 point.)" is a *programmatic override embedded in a human rubric*** — an objective, regex-detectable condition that forces a score floor. This is a nice pattern for making aesthetic rubrics partially judge-free: **bolt deterministic overrides onto Likert anchors.**

## VALIDATION — the numbers

**Annotation protocol:**
> "Each utterance was annotated by three different annotators. We used majority voting to determine the final annotation results."

**Table 1 — consistency between the final (majority-vote) annotation and each annotator:**

| Annotator | EE | EC | **PA** | CU | AVG |
|---|---|---|---|---|---|
| Human 1 | 0.83 | 0.82 | **0.84** | 0.81 | 0.83 |
| Human 2 | 0.83 | 0.85 | **0.86** | 0.82 | 0.84 |
| Human 3 | 0.79 | 0.73 | **0.85** | 0.63 | 0.77 |
| Qwen2.5-72B-Instruct (auto) | 0.78 | 0.86 | **0.72** | 0.75 | 0.78 |

**Read this carefully — it is the most important number in this file.**

**Plot Advancement is the MOST consistent dimension across human annotators (0.84 / 0.86 / 0.85), and notably the most *stable* one — its spread across annotators is 0.84–0.86 (range 0.02), versus Character Understanding at 0.63–0.82 (range 0.19).** Human 3 is the weak annotator overall (AVG 0.77, CU only 0.63) — yet still hits 0.85 on PA. **PA is robust to annotator quality in a way persona-fidelity dimensions are not.**

⚠️ **BUT: this is agreement-with-majority-vote, NOT a chance-corrected statistic.** It is not Krippendorff α, not Cohen κ, not Fleiss κ. With a 3-annotator majority vote, each annotator is *part of* the label they're being scored against, which inflates the number substantially. **These 0.8x figures are NOT comparable to our α = 0.25–0.34, nor to PingPong's α, nor to PersonaGym's κ 0.71.** Do not put them in the same table without a caveat. The honest claim is only the *relative* one: **within this study, under a consistent protocol, PA showed higher and more uniform annotator agreement than the persona dimensions did.** That relative ordering is still the useful signal, and it points the same way as our own hypothesis.

**Automatic evaluator:**
> "In addition to human annotators, we used Qwen2.5-72B-Instruct as an automatic evaluator to evaluate the same data. Automatic evaluator scored each response on each dimension independently, **which can ease the length bias that LLM-as-judge brings** (Li et al., 2025)."
> Footnote 3: "LLM-as-Judge tends to choose the longer response."

> "Qwen2.5-72B-Instruct showed high correlation with the final annotation results across all dimensions. Considering the evaluation cost, it becomes an acceptable automatic evaluator."

**⚠️ Note PA is the judge's WORST dimension (0.72) despite being the humans' BEST (0.84–0.86).** This is the largest human–judge gap in the table. Interpretation: *humans find plot advancement easy to agree on; the LLM judge finds it hard.* This is a warning that PA is a dimension where **a judge will underperform relative to how tractable the construct actually is** — which strengthens the argument for scoring PA with countable correlates rather than a judge.

**The authors' own limitation admission (verbatim):**
> "Although robust quality control mechanisms were implemented, automatically generated dialogues may not fully capture the nuanced complexities of user intentions and role-playing interactions in specific scenarios. Furthermore, while this study explored multiple evaluation dimensions, **the correlation scores of automated annotators are not that high.**"

**Scoring normalization (verbatim):**
> "[We normalize] each score by the limit of its dimension (e.g., EC, EE, PA, and CU are 5) and multiply it by 100."

**Dimension discriminative power:** The paper analyzes each dimension's standard deviation and range (Max-Min) to find "the dimension with the highest discriminative power" (Appendix A). It identifies EC, PA, and CU among "the more challenging dimensions."

**Headline results:**
> "Closed source models like ChatGPT-4o-Latest and Claude 3.5 demonstrate better performance than open source models in all dimensions, achieving an average score of 78.5 and 82.0 in English and Chinese. In contrast, open source models only get 70.7 and 71.5. Qwen2.5-Max shows the best performance in most dimensions in both English and Chinese evaluations... The only competitive open source model is Llama-3.3-70B."

Data is bilingual (EN + ZH), consistent with note 01's language-match finding.

## Licensing / access

> "We implement strict safeguards around this data: access requires formal approval through rigorous licensing and institutional review processes to prevent misuse."

⚠️ **Gated** — same posture as CharacterBench. Take the rubric, not the data. (The rubric text itself is published in the appendix and is what we want anyway.)

## Takeaways for the platform

1. **Adopt Plot Advancement as a first-class dimension.** It is the field's only named storytelling-initiative dimension with human numbers, and it is precisely the axis our taxonomy lacks.
2. **The 1/3/5 anchors are a latent checklist** — convert to countable events (new-element introduction, question acts, scenario crafting) rather than shipping the Likert.
3. **PA showed the highest and most annotator-robust agreement in its study, while persona-understanding (CU) was the most annotator-dependent (0.63–0.82).** Directionally supportive of our core thesis that craft-of-*advancement* is more agreeable than craft-of-*character*. But the statistic is uncorrected agreement-with-majority — do not quote it against our α numbers.
4. **PA was the LLM judge's weakest dimension (0.72) while being the humans' strongest.** Judges are bad at exactly the dimension humans find easiest here → build objective correlates instead of trusting a judge.
5. **Steal the "programmatic override in a rubric anchor" pattern** (the first-person check that forces a 1).
6. **Back-fill RMTBench into note 01's benchmark comparison table** — it is missing, and it is the only entry that would put a ● in the Narrative/Story column with a real rubric.
