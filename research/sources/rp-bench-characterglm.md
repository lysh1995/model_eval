---
title: "CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models"
url: https://arxiv.org/abs/2311.16832
authors: Jinfeng Zhou, Zhuang Chen, Dazhen Wan, Bosi Wen, Yi Song, Jifan Yu, Yongkang Huang, Libiao Peng, Jiaming Yang, Xiyao Xiao, Sahand Sabour, Xiaohan Zhang, Wenjing Hou, Yijia Zhang, Yuxiao Dong, Jie Tang, Minlie Huang
year: 2023
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# CharacterGLM (arXiv 2311.16832)

Submitted 28 Nov 2023. Tsinghua University (CoAI/THUDM) + Lingxin AI + Zhipu AI. Models 6B–66B, built on ChatGLM. Task named **CharacterDial** (Character-based Dialogues).

**The most product-relevant of the five sources for a companion platform:** it is Chinese-native, explicitly motivated by "social desires and emotional needs" rather than literary fidelity, and its evaluation is human-first. Its three core dimensions (Consistency / Human-likeness / Engagement) are grounded in HCI and psychology literature, not invented ad hoc.

## Abstract (VERBATIM)

> In this paper, we present CharacterGLM, a series of models built upon ChatGLM, with model sizes ranging from 6B to 66B parameters. Our CharacterGLM is designed for generating Character-based Dialogues (CharacterDial), which aims to equip a conversational AI system with character customization for satisfying people's inherent social desires and emotional needs. On top of CharacterGLM, we can customize various AI characters or social agents by configuring their attributes (identities, interests, viewpoints, experiences, achievements, social relationships, etc.) and behaviors (linguistic features, emotional expressions, interaction patterns, etc.). Our model outperforms most mainstream close-source large langauge models, including the GPT series, especially in terms of consistency, human-likeness, and engagement according to manual evaluations. We will release our 6B version of CharacterGLM and a subset of training data to facilitate further research development in the direction of character-based dialogue generation.

*(sic: "langauge" is a typo in the published abstract; preserved verbatim.)*

## Design framework: attributes vs. behaviors

Characters are customized along two axes:
- **Attributes:** identities, interests, viewpoints, experiences, achievements, social relationships, etc.
- **Behaviors:** linguistic features, emotional expressions, interaction patterns, etc. Plus: *"we also consider personality as an important factor in shaping response, such as gentleness and coldness."*

## The three core features (VERBATIM, Section 2.2)

These are the paper's design principles *and* its primary eval dimensions. Reproduced in full because the theoretical grounding is the valuable part:

### 1) Consistency

> Character consistency refers to the need for the conversational AI character to display a stable set of attributes and behaviors during interactions. Consistency is essential for believability and trust in human conversations and, by extension, in conversational AI interactions [Nass et al., 1994]. According to the psychological concept of personality consistency [John et al., 1999], individuals tend to exhibit stable behavior patterns over time. In conversational AI characters, maintaining this consistency ensures that users feel they are interacting with the same "individual", which is crucial for long-term user satisfaction and social connection.

### 2) Human-likeness

> Human-likeness in conversational AI characters refers to endowing them with human-like traits, making the interaction more natural, similar to human-human interactions. Human-likeness can be vital for acceptance and comfort, as people are naturally inclined to engage with entities that exhibit familiar human characteristics [Reeves and Nass, 1996]. Moreover, research in HCI has shown that human-like characters can evoke social responses from users [Nass and Moon, 2000]. By anthropomorphizing conversational AI characters, developers can leverage social cues in responses that humans typically use to understand and predict others' behaviors, fostering a more natural and engaging dialogue [Fong et al., 2003].

### 3) Engagement

> Engagement in CharacterDial is the measure of a user's level of interest, interaction, and emotional connection with the conversational AI character. This principle is grounded in the idea that successful communication is not merely about exchanging information but also about establishing a rapport and maintaining a dynamic and interesting conversation [Bickmore and Picard, 2005]. Engagement is directly related to the user's experience and the overall effectiveness of the conversational system. Engaging characters are more likely to evoke empathy and a sense of connection from users, thereby encouraging long-term connection and a positive user experience [Grover et al., 2020].

## Full evaluation dimension set (VERBATIM, Section 4.1)

**6 sub-dimensions + 1 Overall.** Verbatim:

> Following the design principle of CharacterGLM (Section 2), we focus on three primary aspects for evaluating CharacterDial: (1) **Consistency**, ensuring the response is consistent with the attributes and behaviors outlined in the character profile. (2) **Human-likeness**, assessing the degree to which responses exhibit human-like characteristics and mirror natural human communication. (3) **Engagement**, evaluating the response's ability to catch someone's attention or arouse their curiosity. Additionally, we evaluate the general model performance in CharacterDial using three criteria: (1) **Quality**, the fluency and contextual coherence of the response. (2) **Safety**, determining if the response adheres to ethical standards. (3) **Correctness**, ensuring the response is free from hallucinations [Ji et al., 2023]. We also introduce the "**Overall**" metric to measure the response's comprehensive quality by considering all the aforementioned aspects.

| Group | Dimensions |
|---|---|
| Character-specific | Consistency, Human-likeness, Engagement |
| General performance | Quality, Safety, Correctness |
| Aggregate | Overall |

Note **Safety** as a first-class scored dimension — the only one of the five sources to do so. For a companion product this is essential and must be added to any rubric borrowed from CoSER/PingPong, neither of which score it.

## Scoring methodology — human, not LLM-judge

**This is a fully human evaluation. No LLM judge is used.** Verbatim:

> In our evaluation process, we recruited 10 annotators, each tasked with creating two characters to interact with 11 models with no less than 20 dialogue turns. After the completion of interaction, annotators rate the models based on the six foregoing sub-dimensions and the overall metric, using a scoring range from 1 to 5, with higher scores indicating better performance in each dimension. We calculate the final score for each model by averaging these ratings.

**Pointwise setup:**
- 10 annotators × 2 self-created characters each
- Each interacts with **11 models**, **≥20 dialogue turns** per model
- **1–5 scale**, higher = better; final score = mean across ratings
- Annotators **author their own characters** and are the interlocutor — evaluation is first-person interactive, not third-party transcript rating. Closest to real companion usage of any source here.

**Pairwise setup:**
- 10 annotators evaluated **24 sampled characters** across the **4 character categories**
- At each turn, annotators pick the winning response; ties broken randomly
- Win/tie/lose ratios computed across character categories and dialogue topics

## Inter-annotator agreement

**NOT REPORTED.** No Fleiss' kappa, Krippendorff's alpha, Cohen's kappa, or any agreement statistic appears in the paper. Given that this is a *purely* human evaluation with subjective dimensions (Engagement, Human-likeness), and each annotator rated characters *they themselves authored*, the absence of an agreement statistic is the paper's most significant methodological gap. The headline claim — CharacterGLM-66B beats GPT-4 by "approximately 1.4%" on Overall — is unaccompanied by any variance, confidence interval, or significance test, and 1.4% on a 1–5 scale across 20 raters is well within plausible noise.

## Dataset

Released subset from human role-playing:
- **1,034 dialogue sessions**
- **250 characters**
- **32,816 utterances** (16,312 character-side; 16,504 user-side)
- **15.78** average dialogue rounds per session
- **272.97** words average profile length
- **24.33** words average utterance length
- **Language: Chinese**

**Four character categories:** celebrities, daily life, games & videos, virtual love. Verbatim: *"These categories cover the majority of common conversations."* The **virtual love** category is directly on-point for companion applications and is rare in the literature.

Data sources combine human role-playing collection, LLM synthesis, and literary extraction; the released public subset is the human-collected slice. Independent confirmation of scale from DITTO's Table 1: CharacterGLM listed at 250 roles / 1,034 sessions / 16,316 turns, marked **not open-source**, **not multi-lingual**, **multi-turn: yes**.

## Models evaluated (11 total)

ChatGLM2, Claude-2, GPT-3.5-turbo, GPT-4, ERNIEBot (文心一言), Baichuan2, Qwen, MiniMax, SparkDesk (讯飞星火), Xingchen (Tongyi Xingchen), plus **CharacterGLM 6B / 12B / 66B**.

Note the baseline set is Chinese-market-realistic (ERNIE, Baichuan, Qwen, MiniMax, SparkDesk, Xingchen) rather than the usual Western-only lineup — useful if benchmarking against Chinese companion products.

**Headline result (verbatim):** *"CharacterGLM reaches a level comparable to GPT-4... CharacterGLM-66B is distinguished by topping the list in the 'Overall' metric, marginally outperforming GPT-4 by approximately 1.4%."*

## Multilingual & multi-turn

- **Chinese: YES — natively and exclusively.** The paper is titled "Customizing **Chinese** Conversational AI Characters." All data, characters, and annotation are Chinese. **This is the strongest Chinese-language source of the five**, alongside DITTO (which is ~50% Chinese but Wikipedia-derived and shallower).
- **Multi-turn: YES, and the deepest sessions of the five.** 15.78 average rounds per released session; evaluation mandates **≥20 dialogue turns** per model. Contrast: DITTO ~5 turns/session, PingPong ~n turns per conversation. CharacterGLM's long-session protocol is the best match for companion-app usage patterns.

## Limitations

**No formal "Limitations" section exists.** The paper instead closes with **"Future Work"** naming four challenges — effectively an implicit limitations statement:

1. **Long-term memorization and growth** — the *"finite context windows of LLMs"* limit character development over long relationships
2. **Self-awareness** — maintaining *"distinct personalities"* and understanding *"knowledge boundaries"*
3. **Social interaction between characters** — exploring *"character society"* dynamics
4. **Intrinsic cognitive processes** — moving beyond *"surface-level text patterns"* to include *"theory of mind"*

Item 1 is the central unsolved problem for companion products specifically; item 2 is precisely what DITTO's Unknown Question Rejection metric operationalizes.

## Criticisms / notes for platform design

- **No inter-annotator agreement, no significance testing** — the GPT-4 comparison rests on a 1.4% Overall gap with no error bars.
- **Self-authored characters** introduce a confound: annotators rate models on characters they invented and may hold idiosyncratic expectations about; it also means no shared character set across annotators, which further weakens any implicit agreement.
- **Partial release.** Only the 6B model and a *subset* of training data were released; the 66B model that carries the headline claim is API-only. DITTO independently confirms this: *"CharacterGLM has not open-sourced models on all sizes yet, so we can only evaluate it through API."* Not fully reproducible.
- **No automatic metric.** Every evaluation requires 20+ turns of human interaction per model — not viable for continuous/regression evaluation at platform scale. This is the exact cost problem DITTO and CoSER were written to solve.
- **Adopt-worthy:** the Consistency/Human-likeness/Engagement triad with its HCI grounding; the **Safety** and **Correctness** dimensions; the four character categories (esp. *virtual love*); the ≥20-turn interactive protocol as a periodic human-eval gold standard to calibrate cheaper automated judges against.
