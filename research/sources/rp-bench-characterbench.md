---
title: "CharacterBench: Benchmarking Character Customization of Large Language Models"
url: https://arxiv.org/abs/2412.11912
authors: Jinfeng Zhou, Yongkang Huang, Bosi Wen, Guanqun Bi, Yuxuan Chen, Pei Ke, Zhuang Chen, Xiyao Xiao, Libiao Peng, Kuntian Tang, Rongsheng Zhang, Le Zhang, Tangjie Lv, Zhipeng Hu, Hongning Wang, Minlie Huang
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# CharacterBench

- **arXiv:** 2412.11912 (submitted 16 Dec 2024)
- **Published venue:** **AAAI 2025**, pp. 26101–26110
- **Code/data:** <https://github.com/thu-coai/CharacterBench>
- **Affiliation:** THU-CoAI (Tsinghua Conversational AI) + NetEase Fuxi — note the industry co-authorship (Rongsheng Zhang, Tangjie Lv, Zhipeng Hu are Fuxi/NetEase Games), which explains the product-grade dimension set.

## Abstract (VERBATIM)

> Character-based dialogue (aka role-playing) enables users to freely customize characters for interaction, which often relies on LLMs, raising the need to evaluate LLMs' character customization capability. However, existing benchmarks fail to ensure a robust evaluation as they often only involve a single character category or evaluate limited dimensions. Moreover, the sparsity of character features in responses makes feature-focused generative evaluation both ineffective and inefficient. To address these issues, we propose CharacterBench, the largest bilingual generative benchmark, with 22,859 human-annotated samples covering 3,956 characters from 25 detailed character categories. We define 11 dimensions of 6 aspects, classified as sparse and dense dimensions based on whether character features evaluated by specific dimensions manifest in each response. We enable effective and efficient evaluation by crafting tailored queries for each dimension to induce characters' responses related to specific dimensions. Further, we develop CharacterJudge model for cost-effective and stable evaluations. Experiments show its superiority over SOTA automatic judges (e.g., GPT-4) and our benchmark's potential to optimize LLMs' character customization. Our repository is at https://github.com/thu-coai/CharacterBench.

## The 11 dimensions across 6 aspects

**Fidelity note:** definitions marked ✅ are verbatim from the paper. Definitions marked ⚠️ were returned in paraphrased form by extraction and should be re-verified against the PDF before being quoted externally. The dimension *names*, *aspect groupings*, *sparse/dense labels*, and *scales* are all confirmed.

### Aspect 1 — Memory (1 dimension, SPARSE)

| Dimension | Definition | Scale |
|---|---|---|
| **Memory Consistency** | ⚠️ "how stably the character retains information about facts and events from conversational interactions" (ensuring alignment with what was established earlier) | 4-point |

### Aspect 2 — Knowledge (2 dimensions, SPARSE)

| Dimension | Definition | Scale |
|---|---|---|
| **Fact Accuracy** | ✅ "the accuracy with which the character's response reflects factual knowledge related to itself" | 4-point |
| **Boundary Consistency** | ⚠️ "how consistently the response distinguishes the knowledge inherent to the worldview established in the character profile" (from knowledge outside it) | 3-point |

*Boundary Consistency ≈ CharacterEval's Knowledge-Hallucination: does the character stay inside its worldview and decline out-of-world knowledge?*

### Aspect 3 — Persona (2 dimensions, SPARSE)

| Dimension | Definition | Scale |
|---|---|---|
| **Attribute Consistency** | ⚠️ alignment between response and attributes (identity, views) specified in the character profile — "attributes and behaviors presented to fulfill expectations of societal role" | 4-point |
| **Behavior Consistency** | ⚠️ how well responses align with behavioral patterns (linguistic style, actions) in the profile | 3-point (human query) / 4-point (bot) |

*Behavior Consistency uniquely uses two different scales depending on whether the eliciting query is human-authored or bot-generated.*

### Aspect 4 — Emotion (2 dimensions, SPARSE)

| Dimension | Definition | Scale |
|---|---|---|
| **Emotional Self-regulation** | ✅ "assess the character's ability to identify and manage its own emotions" | 4-point |
| **Empathetic Responsiveness** | ✅ "evaluate how well responses recognize and soothe user's emotions" | 4-point |

### Aspect 5 — Morality (2 dimensions, DENSE)

| Dimension | Definition | Scale |
|---|---|---|
| **Morality Stability** | ✅ "LLMs' ability to maintain positive morality when the context is injected with toxic queries" | 2-point |
| **Morality Robustness** | ✅ "ability to uphold positive morality even when the character profile endows toxic settings" | 2-point |

*This is the pair no other benchmark of the four has. Stability = adversarial **user**; Robustness = adversarial **persona definition**. For a companion platform where users author their own characters, Morality Robustness is the single most product-critical dimension in any of these four benchmarks — it directly tests "user writes a toxic character card, does the model comply?"*

### Aspect 6 — Believability (2 dimensions, DENSE)

| Dimension | Definition | Scale |
|---|---|---|
| **Human-likeness** | ✅ "evaluates the naturalness of the character's response in dialogues" | 5-point |
| **Engagement** | ✅ "measures the depth of users' interest and their emotional connection with the character" | 5-point |

## Sparse vs. dense dimensions (VERBATIM)

> "Dense (dimensions in morality and believability aspects) and sparse (dimensions in other 4 aspects) dimensions"

classified by

> "whether character features evaluated by specific dimensions will always manifest in each response."

- **Dense** = Morality (2) + Believability (2) = **4 dimensions**. The feature is present in *every* response — you can always ask "is this natural?" or "is this moral?"
- **Sparse** = Memory, Knowledge, Persona, Emotion aspects = **7 dimensions**. The feature only shows up if the response happens to touch it — you can't score Memory Consistency on a response that recalls nothing.

**This is the paper's core methodological insight**, and the reason the abstract says feature-focused generative evaluation is otherwise "both ineffective and inefficient": if you sample random dialogue and score all 11 dimensions, most sparse dimensions get no signal and you burn judge calls on N/A.

## Target guidance / target-oriented generation (VERBATIM)

> "For sparse dimensions, we introduce target-oriented generation."

The method extracts information fragments from character profiles or dialogue context and crafts queries designed to

> "induce the character to generate responses related to the specific dimension"

— enabling focused evaluation of particular character features.

I.e. **the benchmark writes a bespoke probe query per sparse dimension** to force the feature to manifest, rather than hoping it shows up. This turns a sparse dimension into a densely-measurable one. Target guidance is also fed to the judge at scoring time — see the ablation below, where removing it costs ~17 Pearson points, the largest single ablation effect.

## How it scores

- **Method:** **generative evaluation with a trained LLM judge** (CharacterJudge), scored on **per-dimension rubric scales of varying length (2/3/4/5-point)** — not a uniform scale. Deliberately mixed: binary for morality, fine-grained for believability.
- **Judge base model:** **Qwen2-7B-Chat**
- **Judge training data:** **19,609 samples** from the CharacterBench training set with human annotations
- **Decoding:** "adopt the self-consistency method to generate multiple outcomes and use a majority vote to determine the final score"
- **Language handling:** "bilingual fine-tuning is less effective than training each language separately" → **separate ZH and EN judge models** (hence `run_zh.sh` / `run_en.sh` in the repo)

### Rating scales by dimension (consolidated)

| Scale | Dimensions |
|---|---|
| **2-point** | Morality Stability, Morality Robustness |
| **3-point** | Boundary Consistency, Behavior Consistency (human query) |
| **4-point** | Memory Consistency, Fact Accuracy, Attribute Consistency, Behavior Consistency (bot), Emotional Self-regulation, Empathetic Responsiveness |
| **5-point** | Human-likeness, Engagement |

## Judge–human correlation numbers

### CharacterJudge vs. SOTA judges (Pearson correlation, %)

| Judge | Chinese | English |
|---|---|---|
| **CharacterJudge (Qwen2-7B-Chat)** | **68** | **64** |
| GPT-4-1106-TG | 45 | 46 |
| GLM-4-TG | 48 | 47 |

*(TG = with Target Guidance.) A 7B fine-tuned judge beats GPT-4 by ~20 Pearson points in both languages — a stronger margin than CharacterEval's CharacterRM achieved (0.631 vs 0.385).*

### Ablations (Pearson, Chinese / English)

| Configuration | ZH | EN |
|---|---|---|
| **Full CharacterJudge** | **68** | **64** |
| w/o Self-Consistency | 64 | 60 |
| w/o Target Guidance | 51 | 48 |
| w/o Both | 47 | 45 |

**Reading:** Target Guidance is the dominant ingredient (−17 ZH / −16 EN when removed); self-consistency adds ~4. Stripped of both, CharacterJudge (47/45) falls to roughly GPT-4-with-TG's level (45/46) — i.e., **the gain is mostly method, not model scale**. This is the most actionable finding in the paper for anyone building a judge.

### Generalizability (Pearson, In-domain / Out-of-domain)

| Split | ZH | EN |
|---|---|---|
| In-domain | 67 | 64 |
| Out-of-domain | 68 | 65 |

**No degradation on unseen characters** — out-of-domain actually ties or slightly beats in-domain. Strong evidence the judge learned dimension semantics rather than memorizing characters. This is the key property for a companion platform with user-authored characters the judge has never seen.

### Consistency with human evaluation, cross-benchmark (Spearman / Kendall, %)

| Benchmark | Spearman | Kendall |
|---|---|---|
| **CharacterBench** | **73.1** | **61.8** |
| SocialBench | 38.1 | 35.7 |
| CharacterEval | 21.4 | 14.3 |

*CharacterJudge transfers poorly to CharacterEval (21.4/14.3) — this cuts both ways. It may indicate CharacterEval's labels are noisy/idiosyncratic, or that CharacterJudge is over-fit to CharacterBench's rubric semantics. Do not read this as a clean win.*

## Inter-annotator agreement

**Not reported as a statistic.** The paper describes the *process* but gives no Krippendorff's α or Fleiss' κ:

> "Each sample is annotated by two different annotators. If results are inconsistent, a third annotator re-annotates and discusses to reach consensus."

So: **2 annotators + 3rd-annotator adjudication to consensus**, but no quantified agreement. Same gap as CharacterEval. Notable given this is the "largest human-annotated" claim — 22,859 samples annotated with unreported reliability.

## Dataset statistics

| Statistic | Value |
|---|---|
| **Total human-annotated samples** | **22,859** |
| **Characters** | **3,956** |
| **Character categories** | **25 sub-categories** across **4 main categories** |
| **Languages** | Bilingual — Chinese + English |
| **Translation pass rate** | **96%** |
| **Avg. turns per dialogue** | **11.22** |
| **Train split** | **19,609** |
| **Test split** | **3,250** — 1,625 in-domain / 1,625 out-of-domain |

**⚠️ Gap:** the enumerated list of the 4 main categories and 25 sub-categories was not recoverable from the HTML render (it's in Figure 3, a distribution plot). **Re-check the PDF Figure 3 / appendix if the category taxonomy is needed.**

**Construction:** data initially collected in **Chinese**, then translated to English via **GPT-4o** with human review (96% pass rate). So English is a *translation* of Chinese-native data, not independently sourced — English cultural coverage is therefore Chinese-character-skewed despite the "bilingual" framing.

**Scale comparison:** 3,956 characters vs CharacterEval's 77 and RoleBench's 100 — CharacterBench is ~40× more characters than either. This is what makes the out-of-domain generalization test meaningful.

## Models evaluated — 18 LLMs

**Closed-source / API:** GPT-3.5-turbo, GPT-4-1106, GPT-4o, Claude-3-opus, GLM-4, MiniMax-abab5.5s

**Roleplay-specialized:** CharacterGLM, Baichuan-NPC, CharacterYuyan

**Open-source:** Llama3, Qwen1.5, Qwen2, Mistral-7B, Yi1.5-9B, GLM4-9B

## Multilingual coverage and multi-turn support

- **Bilingual (ZH + EN)** — the only genuinely bilingual *generative* benchmark of the four (RoleEval is bilingual but multiple-choice; RoleBench is 95% English; CharacterEval is Chinese-only).
- **Caveat:** English is GPT-4o-translated from Chinese-native data (96% human-review pass rate), not natively authored. Judges are trained **separately per language** because "bilingual fine-tuning is less effective than training each language separately."
- **Multi-turn: YES** — average **11.22 turns** per dialogue, the longest of the four benchmarks. Memory Consistency explicitly depends on multi-turn context.

## Stated limitations and known criticisms

**No dedicated Limitations section.** (AAAI format doesn't mandate one, unlike ACL.)

**Ethical Considerations section covers:**
- Worker compensation "based on the market price"
- No personal information in collected data
- Data and models released for research purposes only
- Morality data constructed solely for research, contains "sensitive and unethical content"
- "Access to our data and models will be subject to rigorous licensing and review processes"

**Acknowledged constraints (in-text):**
- **Fact Accuracy evaluated on a limited celebrity subset — only 105 characters** (out of 3,956). So the Fact Accuracy numbers rest on ~2.7% of the character set.
- **Does not evaluate MBTI or Big-Five personality traits** — a deliberate scope choice, and arguably a *better* one than CharacterEval's contested MBTI back-testing.
- Data initially collected in Chinese with GPT-4o translation and human review.

**Criticisms / gaps:**
1. **No quantified inter-annotator agreement** despite 22,859 annotations and a "largest human-annotated" claim.
2. **English is translated, not native** — cultural/idiomatic authenticity of the English split is unverified beyond a 96% translation pass rate; character *selection* remains Chinese-centric.
3. **Gated access** — "rigorous licensing and review processes" for data and models limits reproducibility and independent verification.
4. **Fact Accuracy rests on 105 characters.**
5. **Poor cross-benchmark transfer** (CharacterEval: Spearman 21.4) — raises over-fitting-to-own-rubric concerns that the paper attributes to the other benchmark.
6. **Non-uniform scales (2/3/4/5-point)** complicate aggregation into a single score; the paper's "overall" numbers require normalization choices that aren't obviously neutral.
7. **Judge is a 7B model** — cheap and stable, but a fixed judge is a fixed target; models could overfit to CharacterJudge's idiosyncrasies over time.

## Relevance to a companion-eval platform

**This is the most directly applicable of the four.** Reasons:

- **Morality Robustness** is uniquely relevant: it tests whether the model resists a *user-authored toxic character profile* — exactly the threat model for a platform with user-created companions. No other benchmark here covers it.
- **Sparse/dense + target guidance** is a directly reusable architecture. The ablation shows target guidance is worth ~17 Pearson points — more than switching from GPT-4 to a fine-tuned judge. If we build one thing from this literature, build target-guided probe generation.
- **Out-of-domain generalization holds (68/65 vs 67/64 in-domain)** — the judge works on unseen characters, which is a hard requirement for user-authored personas.
- **Cost argument is strong:** Qwen2-7B judge beats GPT-4 by ~20 Pearson points at a fraction of inference cost.
- **Bilingual with separate per-language judges** — matches a ZH+EN product footprint, with the caveat that EN data is translated.
- **Engagement + Human-likeness (5-point)** are the closest things in this literature to companion-product north-star metrics.

**Watch-outs:** gated data/model access; unreported annotator agreement; English-is-translated; Fact Accuracy's narrow 105-character base.

## Citation

```bibtex
@inproceedings{zhou2025characterbench,
  author    = {Zhou, Jinfeng and Huang, Yongkang and Wen, Bosi and Bi, Guanqun and Chen, Yuxuan and Ke, Pei and Chen, Zhuang and Xiao, Xiyao and Peng, Libiao and Tang, Kuntian and Zhang, Rongsheng and Zhang, Le and Lv, Tangjie and Hu, Zhipeng and Wang, Hongning and Huang, Minlie},
  title     = {CharacterBench: Benchmarking Character Customization of Large Language Models},
  booktitle = {AAAI-25},
  pages     = {26101--26110},
  year      = {2025}
}
```
