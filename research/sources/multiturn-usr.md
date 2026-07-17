---
title: "USR: An Unsupervised and Reference Free Evaluation Metric for Dialog Generation"
url: https://aclanthology.org/2020.acl-main.64/
authors: Shikib Mehri, Maxine Eskenazi (Dialog Research Center, Language Technologies Institute, Carnegie Mellon University)
year: 2020
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# USR — UnSupervised and Reference-free evaluation metric for dialog

Venue: ACL 2020, pages 681–707. arXiv: 2005.00456.
**Source used: the ACL Anthology PDF full text (2020.acl-main.64.pdf), text-extracted locally. All numbers below are transcribed from the paper's own tables.**

## UNIT OF EVALUATION — RESPONSE-LEVEL (per-response)

**USR is strictly a per-response metric.** Every correlation it reports is either *turn-level* (one generated response scored against a dialog context) or *system-level* (per-response scores averaged up to rank a system). There is **no per-conversation / dialog-level unit anywhere in USR.** This is the axis on which FED (the same authors' SIGdial 2020 follow-up) supersedes it.

Contrast, from the FED paper's own related-work section:
> "Similar to FED, USR uses pre-trained models to assess several dialog qualities. However, they are limited to five qualities with hand-designed models and unsupervised tasks for each quality. In comparison, FED is more general and encapsulates eighteen dialog qualities."

USR scores `r` given context `c` (and fact/persona `f`). It never scores a conversation as a whole, never measures anything across turns, and none of its five qualities require more than one system turn to evaluate.

Design goals, verbatim: USR "(1) is reference-free, (2) is composed of multiple sub-metrics that evaluate specific qualities of dialog, (3) has a definition of good dialog that is configurable."

## Headline result (abstract, verbatim)

> "USR is shown to strongly correlate with human judgment on both Topical-Chat (turn-level: 0.42, system-level: 1.0) and PersonaChat (turn-level: 0.48 and system-level: 1.0)."

## Datasets and annotation (exact)

### Topical-Chat
- Task: produce a response conditioned on **both a dialog context and a fact**. "Following the same experimental setup as Gopalakrishnan et al. (2019), heuristics are employed to identify the most relevant fact for each response."
- **60 dialog contexts** randomly sampled from the *frequent test set*, **6 responses each = 360 responses** scored on six qualities.

> "For Topical-Chat, the full annotation consisted of 60 dialog contexts randomly sampled from the frequent test set, for a total of 360 responses scored on six different qualities."

- The 6 responses per context = 4 model decodings + 1 original ground-truth + 1 new human-generated. Model: a Transformer (6 layers, hidden size 512, randomly-initialized 300-dim word embeddings, dropout 0.1, trained 50 epochs), decoded with **argmax sampling** plus **nucleus sampling at p = {0.3, 0.5, 0.7}**.

### PersonaChat
- Corpus (Zhang et al., 2018): **10,907 dialogs and 162,064 utterances**. Persona is "analogous to the facts in the Topical-Chat corpus."
- **60 dialog contexts** sampled from the ConvAI2 validation set, **5 responses each = 300 responses** scored on six qualities.

> "For PersonaChat, 60 dialog contexts were sampled from the ConvAI2 validation set, with a total of 300 responses scored on six different qualities."

- Models: **Seq2Seq**, an **LSTM language model (LM)**, and a **Key-Value Profile Memory Network (KV-MemNN)** — pre-trained ParlAI models from the ConvAI2 competition. Plus original ground-truth and new human-generated. "A fourth open-source model was also used to produce output for quality annotation, however it was ultimately excluded from the released dataset and experiments due to possible data leakage."

### Annotators
> "Each response was labeled by three different annotators. Annotators were randomly assigned to each dialog context."

**Annotation was done by 6 dialog researchers, NOT crowdworkers:**
> "Quality annotation was performed by six dialog researchers. Using a crowdsourcing platform, such as Amazon Mechanical Turk (AMT), would have allowed for more efficient and scalable annotation. However, crowdsourcing was not used because (1) the annotation instructions are lengthy, (2) a preliminary annotation pass was carried out, followed by a group discussion, (3) having many annotations from a few annotators allows examination of annotator-specific subjectivity."

Preliminary pass: "each individual annotating 5 dialog contexts (for a total of 30 responses)." Instructions were then refined — "e.g., Maintains Context was changed to be a 3-point rating instead of a 2-point rating."

**Total annotated responses across both datasets: 660 (360 + 300).** This is a small evaluation set — worth noting for a platform weighing how much to trust these coefficients.

## The six annotated dialog qualities (verbatim definitions)

> • **Understandable (0 - 1):** Is the response understandable given the previous context?
> • **Natural (1 - 3):** Does the response seem to be something that a person would naturally say?
> • **Maintains Context (1 - 3):** Does the response serve as a valid continuation of the preceding conversation?
> • **Interesting (1 - 3):** Is the response dull or interesting?
> • **Uses Knowledge (0 - 1):** Given the fact that the response is conditioned on, how well does the response use that fact?
> • **Overall Quality (1 - 5):** Given your answers above, what is your overall impression of the quality of this utterance?

Five specific qualities + Overall Quality. Note **Overall Quality is explicitly defined as an utterance-level judgment** ("the quality of this utterance") — again confirming the per-response unit.

**Completeness check of the five qualities (verbatim):**
> "a regression can be trained to produce the overall score conditioned on the quality ratings. The Spearman correlation between the predicted score and the original overall score is 0.9654, which signifies that the set of qualities is thorough and contains enough information to reflect the overall quality of the response."

This 0.9654 regression is reused as USR's combination function.

## USR sub-metrics — exact definitions

USR "leverages pre-trained language models, specifically RoBERTa (Liu et al., 2019), to measure properties of dialog. USR is designed to be reference-free because there is no one right answer due to the inherent one-to-many nature of dialog."

### USR-MLM (Masked Language Modelling) → Understandable, Natural

> "The masked language modelling (MLM) metric uses a fine-tuned RoBERTa (Liu et al., 2019) model to estimate the likelihood of a response. RoBERTa is pre-trained on a massive amount of English data and fine-tuned on the corpus being evaluated (either Topical-Chat or PersonaChat), making it capable of identifying unnatural and incorrect responses. The likelihood estimated by the fine-tuned RoBERTa model is used as an automatic metric for evaluating the understandability and naturalness of responses."

Mechanics:
> "The input sequence to MLM is a concatenation of a dialog context, c, and a response, r. One word at a time, each word in r is masked and its log likelihood is computed. Given the masked log-likelihood for the i-th word of r as l_i, the value of the metric is then computed to be −Σ_i^{|r|} l_i."

Setup: **RoBERTa-base**, fine-tuned on the Topical-Chat training set using the Wolf et al. (2019a) implementation, **on only the dialog, without any of the facts, for a single epoch.**

### USR-DR (Dialog Retrieval) → Maintains Context, Interesting, Uses Knowledge

> "The fine-tuned RoBERTa model described in Section 4.2.1 is further fine-tuned for the retrieval task. This task is set up in the same manner as the Ubuntu dialog corpus (Lowe et al., 2015). The model is trained given a context x, a response r, and a binary label y indicating whether r is the true response or randomly sampled. The context x may consist of the dialog history and the fact, denoted c, or just the fact, denoted f. Two different versions of the dialog retrieval (DR) metric are trained, with different values of x. The DR metric score is defined to be the probability P(y = 1|x, r) a given DR metric model produces."

**The two variants (this distinction matters — they behave very differently):**
- **USR-DR (x = c):** context = dialog history **+** the fact/persona.
- **USR-DR (x = f):** context = **only** the fact.

Why it counts as unsupervised:
> "Though the DR metric is trained for the task of retrieval, this is done in an unsupervised manner. The retrieval task is an unsupervised task since it requires no additional labels during training (e.g., explicit quality annotations)."

Quality mapping:
> "The DR metric is appropriate for Maintains Context, Interesting and Uses Knowledge. If a retrieval model predicts that a generated response is contextually relevant to a dialog context, it indicates that the response Maintains Context. Likewise, if a retrieval model predicts that the response r is contextually relevant to fact f, it signifies that r most likely Uses Knowledge."

How DR captures *Interesting* (the clever part):
> "The DR metric is trained to distinguish between a ground-truth response (y = 1) and a randomly sampled response (y = 0). Generic responses are applicable to many contexts, and will often appear as both ground-truth responses and randomly sampled responses. As such, the model will likely learn to assign a low probability distribution to these generic responses and will often output P(y = 1|r, x) = 0.5. As such, generic responses will generally be scored lower than other contextually relevant, interesting responses. The DR metrics will learn to favor responses that are unique to a given context x, rather than being applicable to many different contexts."

### The USR composite

> "Given meaningful automatic metrics for each of the five dialog qualities, USR combines the scores into an overall measure that correlates well with Overall Quality ratings."

The **same regression** from §3.5 (the one that hit 0.9654 Spearman reproducing human Overall from human sub-ratings) is applied on top of the *automatic* sub-metrics. Scores were z-score normalized before training the regression; a softmax was computed over the weights for interpretability.

> "USR combines its sub-metrics into one measure of overall quality. This combination is configurable, adaptable to different datasets or tasks. For example, if a specific application prefers natural responses over interesting ones, the weights of the regression model can be adjusted."

**Configurability is the platform-relevant property:** the definition of "good" is a reweightable regression, so a companion product can re-weight toward e.g. Interesting/Natural over Uses Knowledge without retraining sub-metrics.

## RESULTS

**Note on evaluation protocol:** "The annotations for the original ground-truth are not used for evaluation, in order to accurately compare referenced and reference-free metrics." And "The best sub-metrics for each dialog quality are used as input for the regression model of the USR metric."

### Table 5 — Topical-Chat, turn-level correlations with Overall Quality (ALL metrics)

| Metric | Spearman | Pearson |
|---|---|---|
| **Word-Overlap Metrics** | | |
| F-1 | 0.1645 | 0.1690 |
| BLEU-1 | 0.2728 | 0.2876 |
| BLEU-2 | 0.2862 | 0.3012 |
| BLEU-3 | 0.2569 | 0.3006 |
| BLEU-4 | 0.2160 | 0.2956 |
| METEOR | 0.3365 | 0.3908 |
| ROUGE-L | 0.2745 | 0.2870 |
| **Embedding Based Metrics** | | |
| Greedy Matching | 0.1712 | 0.1943 |
| Embedding Average | 0.1803 | 0.2038 |
| Vector Extrema | 0.2032 | 0.2091 |
| Skip-Thought | 0.1040 | 0.1181 |
| BERTScore (base) | 0.3229 | 0.3540 |
| BERTScore (large) | 0.2982 | 0.3252 |
| **Reference Free Metrics** | | |
| USR - MLM | 0.3086 | 0.3345 |
| USR - DR (x = c) | 0.3245 | 0.4068 |
| USR - DR (x = f) | 0.1419 | 0.3221 |
| **USR** | **0.4192** | **0.4220** |

("All values with p > 0.05 are italicized" — italics not recoverable from text extraction.)

**Deltas vs baselines on Topical-Chat (Spearman):** USR 0.4192 vs best word-overlap METEOR 0.3365 = **+0.0827**; vs BLEU-4 0.2160 = **+0.2032**; vs ROUGE-L 0.2745 = **+0.1447**; vs F-1 0.1645 = **+0.2547**; vs best embedding BERTScore(base) 0.3229 = **+0.0963**.

### Table 6 — PersonaChat, turn-level correlations with Overall Quality (ALL metrics)

| Metric | Spearman | Pearson |
|---|---|---|
| **Word-Overlap Metrics** | | |
| F-1 | 0.1422 | 0.1241 |
| BLEU-1 | 0.0434 | 0.0469 |
| BLEU-2 | 0.1122 | 0.0943 |
| BLEU-3 | 0.1202 | 0.0924 |
| BLEU-4 | 0.1353 | 0.0899 |
| METEOR | 0.2527 | 0.2713 |
| ROUGE-L | 0.0659 | 0.0385 |
| **Embedding Based Metrics** | | |
| Greedy Matching | 0.0916 | 0.0625 |
| Embedding Average | 0.1182 | 0.1428 |
| Vector Extrema | 0.1570 | 0.1410 |
| Skip-Thought | -0.0393 | -0.0452 |
| BERTScore (base) | 0.1690 | 0.1526 |
| BERTScore (large) | 0.1518 | 0.1211 |
| **Reference Free Metrics** | | |
| USR-MLM | 0.0795 | 0.0788 |
| USR-DR (x = f) | -0.0495 | -0.0454 |
| USR-DR (x = c) | **0.4814** | **0.6087** |
| **USR** | 0.4693 | 0.4115 |

**Deltas vs baselines on PersonaChat (Spearman):** USR 0.4693 vs METEOR 0.2527 = **+0.2166**; vs ROUGE-L 0.0659 = **+0.4034**; vs BLEU-4 0.1353 = **+0.3340**; vs F-1 0.1422 = **+0.3271**; vs BERTScore(base) 0.1690 = **+0.3003**.

**Important caveat the paper states itself — USR does NOT win on PersonaChat:**
> "However, DR (x = c) outperforms USR despite the fact that four out of the five sub-metrics input into the USR regression are DR (x = c). This result is probably due to PersonaChat's strong dependancy on both dialog context and persona, both of which DR (x = c) explicitly leverages."

USR-DR(x=c) beats full USR on PersonaChat on both Spearman (0.4814 vs 0.4693) and Pearson (0.6087 vs 0.4115). The Pearson gap is large (**+0.1972** for the sub-metric). Note also **Skip-Thought and USR-DR(x=f) are negatively correlated** with human judgment on PersonaChat.

### Table 3 — Topical-Chat, turn-level correlations per dialog quality
Shows (1) best non-USR metric, (2) best USR sub-metric, (3) USR. "All measures in this table are statistically significant to p < 0.01."

| Metric | Spearman | Pearson |
|---|---|---|
| **Understandable** | | |
| BERTScore (base) | 0.2502 | 0.2611 |
| USR - MLM | **0.3268** | **0.3264** |
| USR | 0.3152 | 0.2932 |
| **Natural** | | |
| BERTScore (base) | 0.2094 | 0.2260 |
| USR - MLM | **0.3254** | **0.3370** |
| USR | 0.3037 | 0.2763 |
| **Maintains Context** | | |
| METEOR | 0.3018 | 0.2495 |
| USR - DR (x = c) | 0.3650 | 0.3391 |
| USR | **0.3769** | **0.4160** |
| **Interesting** | | |
| BERTScore (base) | 0.4121 | 0.3901 |
| USR - DR (x = c) | **0.4877** | 0.3533 |
| USR | 0.4645 | **0.4555** |
| **Uses Knowledge** | | |
| METEOR | 0.3909 | **0.3328** |
| USR - DR (x = f) | **0.4468** | 0.2220 |
| USR | 0.3353 | 0.3175 |

> "USR is shown to strongly outperform both word-overlap and embedding-based metrics across all of the dialog qualities. Interestingly, the best non-USR metric is consistently either METEOR or BERTScore – possibly because both methods are adept at comparing synonyms during evaluation. For some dialog qualities, the overall USR metric outperforms the best sub-metric. For example, USR does better for Maintains Context than USR-DR. This is likely because the information from the other sub-metrics (e.g., Uses Knowledge) is valuable and effectively leveraged by USR."

### Table 4 — PersonaChat, turn-level correlations per dialog quality
"All values with p > 0.05 are italicized."

| Metric | Spearman | Pearson |
|---|---|---|
| **Understandable** | | |
| BERTScore (base) | 0.0685 | 0.0672 |
| USR - MLM | 0.1186 | **0.1313** |
| USR | **0.1324** | 0.1241 |
| **Natural** | | |
| VectorExtrema | 0.1375 | 0.1458 |
| USR - DR (x = c) | 0.2291 | 0.1733 |
| USR | **0.2430** | **0.1862** |
| **Maintains Context** | | |
| METEOR | 0.2564 | 0.2500 |
| USR - DR (x = c) | **0.5625** | 0.6021 |
| USR | 0.5280 | **0.6065** |
| **Interesting** | | |
| BERTScore (base) | 0.0491 | 0.0325 |
| USR - DR (x = c) | **0.2634** | **0.0606** |
| USR | 0.0171 | 0.0315 |
| **Uses Knowledge** | | |
| METEOR | 0.1719 | 0.1678 |
| USR - DR (x = c) | **0.6309** | **0.4508** |
| USR | 0.3177 | 0.4027 |

> "Across all dialog qualities, USR strongly outperforms the word-overlap and embedding-based metrics. Conversations in PersonaChat generally consist of individuals communicating facts from their own persona in a relevant and coherent manner. As such, when models trained on PersonaChat produce subpar outputs, it is generally because the outputs either (1) do not effectively use the persona or (2) are not relevant/coherent to the dialog context. This explains why the correlations are significantly higher for Maintains Context and Uses Knowledge. As a consequence of PersonaChat's strong dependency on both the dialog context and the persona, USR-DR (x = c) which uses both the dialog context and the persona to perform dialog retrieval, generally outperforms all other metrics."

Note **USR's Interesting on PersonaChat collapses to 0.0171 Spearman** — worse than its own DR sub-metric (0.2634) and effectively no signal. Relevant to a companion platform: USR cannot measure interestingness in a persona-grounded setting.

### System-level correlations

> "We compute the system-level correlation between all automatic metrics and the Overall Quality ratings. USR significantly (p < 0.01) outperforms all other metrics with a Spearman correlation of 1.0 on both datasets and Pearson correlations of 0.92 (Topical-Chat) and 0.82 (PersonaChat). The full set of system-level correlations can be found in the appendix."

- **Topical-Chat system-level: Spearman 1.0, Pearson 0.92**
- **PersonaChat system-level: Spearman 1.0, Pearson 0.82**

Interpret Spearman 1.0 with care: it is a rank correlation over a **very small number of systems** (5 response types per dataset after excluding ground-truth). Perfect rank correlation over ~5 points is a weak claim. The paper does not caveat this; I flag it. The per-metric appendix table (Appendix) was not extracted here — **the full system-level table per baseline metric is NOT reproduced in this file.**

## Table 2 — Average human scores per system/response type

Qualities: Und (0-1), Nat (1-3), MCtx (1-3), Int (1-3), UK (0-1), OQ (1-5).

| System | Und | Nat | MCtx | Int | UK | OQ |
|---|---|---|---|---|---|---|
| **Topical-Chat** | | | | | | |
| Original Ground-Truth | 0.95 | 2.72 | 2.72 | 2.64 | 0.72 | 4.25 |
| Argmax Decoding | 0.60 | 2.08 | 2.13 | 1.94 | 0.47 | 2.76 |
| Nucleus Sampling (0.3) | 0.51 | 2.02 | 1.90 | 1.82 | 0.42 | 2.40 |
| Nucleus Sampling (0.5) | 0.48 | 1.92 | 1.93 | 1.72 | 0.34 | 2.29 |
| Nucleus Sampling (0.7) | 0.52 | 2.01 | 1.87 | 1.80 | 0.37 | 2.39 |
| New Human Generated | 0.99 | 2.92 | 2.93 | 2.90 | 0.96 | 4.80 |
| **PersonaChat** | | | | | | |
| Original Ground-Truth | 0.99 | 2.89 | 2.82 | 2.67 | 0.56 | 4.36 |
| Language Model | 0.97 | 2.63 | 2.02 | 2.24 | 0.08 | 2.98 |
| LSTM Seq2Seq | 0.92 | 2.64 | 2.49 | 2.29 | 0.47 | 3.47 |
| KV-MemNN | 0.93 | 2.70 | 2.18 | 2.56 | 0.17 | 3.25 |
| New Human Generated | 1.00 | 2.97 | 2.88 | 2.87 | 0.96 | 4.80 |

## TURN-DEPTH / SINGLE-TURN vs MULTI-TURN EVIDENCE (critical)

**USR contains NO turn-index analysis.** It does not measure how quality varies with turn depth, does not report correlations by conversation position, and has no multi-turn evaluation unit. Any claim that USR shows quality degrading over turns would be fabricated.

**However, USR contains one direct and quotable piece of evidence that per-response optimization diverges from per-conversation quality** — and it appears as an *incidental observation*, which makes it more credible:

> "Across both datasets and all qualities, the new human generated response strongly outperforms all other response types, even the original ground truth. This may be because the new human generated response was written with this quality annotation in mind, and as such is optimized for turn-level evaluation. On the other hand, the workers who produced the original ground-truth response, were more concerned with the quality of the overall dialog than with the quality of each individual response."

This is the whole per-response-vs-per-conversation problem in miniature. The **New Human Generated** response — written to be *judged in isolation* — beats the **Original Ground-Truth** — written by someone actually *having the conversation*:
- Topical-Chat Overall Quality: **4.80 vs 4.25 (+0.55)**
- PersonaChat Overall Quality: **4.80 vs 4.36 (+0.44)**
- And on every single quality in both datasets (e.g. Topical-Chat Uses Knowledge **0.96 vs 0.72**; PersonaChat Uses Knowledge **0.96 vs 0.56**).

A real conversational turn *loses* to a turn engineered for the rubric. Turn-level rubrics reward locally-optimized responses that a real interlocutor would not produce — the ground-truth speaker was sacrificing local score for dialog-level goals (setting up topics, leaving room to reply, not front-loading every fact). **A per-response metric scores that sacrifice as a defect.**

This aligns exactly with FED's Table 4 result (Meena beats Human at turn level, loses at dialog level). Two papers, same authors, same year, two independent demonstrations that **per-response evaluation systematically over-rewards locally-punchy output and under-rewards conversation-level competence.**

For a companion/roleplay platform this is the caution: USR-style per-response scoring will select for characters that produce impressive standalone lines and against characters that build a conversation.

## Stated limitations (verbatim)

> "USR should be used alongside human evaluation. USR was created to facilitate development and tuning of dialog models. As such, USR can be used for model selection and hyperparameter tuning. USR should not be used to claim superior performance over another method."

> "USR may not work with non-generative models, which were not addressed here. Responses produced by a model that is too similar to the evaluation models (e.g., to DR) are a particular concern."

## Why standard metrics fail (the paper's framing)

> "(1) The one-to-many nature of dialog (Zhao et al., 2017) makes word-overlap metrics ineffective for scoring valid system output that deviates from the ground-truth response... (2) Human evaluation of dialog typically measures multiple properties (e.g., appropriate, interesting, consistent). Automatic metrics on the other hand, condense the multi-faceted nature of dialog quality to a single uninterpretable metric."

**The F-1 adversarial example (memorable, and a good argument for reference-free evals):**
> "Dinan et al. (2019) described a simple adversarial example that attains a high F-1 score on PersonaChat. We produce a similar example for the Topical-Chat dataset and find that always outputting a concatenation of the ten most common tokens in the dataset ('. i the , that a to it is of') attains an F-1 score of 25.6 which is a +3.6 improvement over the Transformer presented by Gopalakrishnan et al. (2019)."

On BERTScore specifically:
> "although it is a more sophisticated metric, it still compares word similarity between a reference and a generated sequence. While this method may work well for tasks where there is a limited space of outputs for each input (e.g., captioning, translation), it is ineffective at dealing with the one-to-many nature of dialog."

## Inter-annotator agreement (Table 1) — NOT metric performance

**Do not confuse with the metric correlation tables.** This is agreement between annotator pairs, averaged over pairs. "For all the correlations presented in this table, p < 0.01."

| Metric | Spearman | Pearson |
|---|---|---|
| **Topical-Chat** | | |
| Understandable | 0.5102 | 0.5102 |
| Natural | 0.4871 | 0.4864 |
| Maintains Context | 0.5599 | 0.5575 |
| Interesting | 0.5811 | 0.5754 |
| Uses Knowledge | 0.7090 | 0.7090 |
| Overall Quality | 0.7183 | 0.7096 |
| **PersonaChat** | | |
| Understandable | 0.2984 | 0.2984 |
| Natural | 0.4842 | 0.4716 |
| Maintains Context | 0.6125 | 0.6130 |
| Interesting | 0.4318 | 0.4288 |
| Uses Knowledge | 0.8115 | 0.8115 |
| Overall Quality | 0.6577 | 0.6603 |

> "Most inter-annotator correlations are above 0.4, which indicates moderate to strong agreement. The low agreement for Understandable on PersonaChat is likely a consequence of the simple language in the dataset."

> "The agreement for Overall Quality is relatively high (0.71 for Topical-Chat and 0.66 for PersonaChat) which suggests that any ambiguity in the specific dialog qualities is mitigated when the annotator is asked for an overall impression."

**Ceiling context:** annotator agreement on Overall Quality is 0.7183 (Topical-Chat) / 0.6577 (PersonaChat), while USR reaches 0.4192 / 0.4693. USR attains roughly **58% / 71%** of the human-agreement ceiling on each dataset.

## Annotator subjectivity (Figure 2) — relevant to companion-persona evals

A separate regression was trained per annotator (for the five Topical-Chat annotators), mapping the five ratings to Overall.

> "Annotators attributed different weights to the specific features. For example, A3 emphasized naturalness while A2 paid more attention to whether a response was grounded on knowledge. Despite the differences across annotators, a good response was generally expected to be natural, maintain context, and be interesting. These annotator-specific weights demonstrate that individuals define good dialog differently. Future work could explore personalized dialog evaluation wherein the evaluation metric is tailored to a specific individual."

(The exact per-annotator weights are shown only as a heatmap in Figure 2 — **numeric values are not recoverable from the text and are not reproduced here.**)

"There are many definitions of what a good dialog is" — the paper treats this as a core motivation for the configurable regression. For a companion platform where different users want different things from a character, this per-user reweighting idea is directly applicable.
