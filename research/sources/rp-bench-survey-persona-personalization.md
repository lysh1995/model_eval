---
title: "From Persona to Personalization: A Survey on Role-Playing Language Agents"
url: https://arxiv.org/abs/2404.18231
authors: Jiangjie Chen, Xintao Wang, Rui Xu, Siyu Yuan, Yikai Zhang, Wei Shi, Jian Xie, Shuang Li, Ruihan Yang, Tinghui Zhu, Aili Chen, Nianqi Li, Lida Chen, Caiyu Hu, Siye Wu, Scott Ren, Ziquan Fu, Yanghua Xiao (Fudan University, ByteDance)
year: 2024
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# Survey — From Persona to Personalization (RPLA survey)

**arXiv:** 2404.18231. **Venue:** TMLR (Transactions on Machine Learning Research), 2024. HTML: https://arxiv.org/html/2404.18231v2

> **Relevance:** This survey's organizing axis is **persona type**, and it is the only one of the two surveys that treats **Individualized Persona** — personas built up "through ongoing user interactions" — as a first-class category. That is precisely the companion product. It also names **emotional companions** as the first RPLA application.

## Abstract (VERBATIM)

> Recent advancements in large language models (LLMs) have significantly boosted the rise of Role-Playing Language Agents (RPLAs), i.e., specialized AI systems designed to simulate assigned personas. By harnessing multiple advanced abilities of LLMs, including in-context learning, instruction following, and social intelligence, RPLAs achieve a remarkable sense of human likeness and vivid role-playing performance. RPLAs can mimic a wide range of personas, ranging from historical figures and fictional characters to real-life individuals. Consequently, they have catalyzed numerous AI applications, such as emotional companions, interactive video games, personalized assistants and copilots, and digital clones. In this paper, we conduct a comprehensive survey of this field, illustrating the evolution and recent progress in RPLAs integrating with cutting-edge LLM technologies. We categorize personas into three types: 1) Demographic Persona, which leverages statistical stereotypes; 2) Character Persona, focused on well-established figures; and 3) Individualized Persona, customized through ongoing user interactions for personalized services. We begin by presenting a comprehensive overview of current methodologies for RPLAs, followed by the details for each persona type, covering corresponding data sourcing, agent construction, and evaluation. Afterward, we discuss the fundamental risks, existing limitations, and future prospects of RPLAs. Additionally, we provide a brief review of RPLAs in AI applications, which reflects practical user demands that shape and drive RPLA research. Through this work, we aim to establish a clear taxonomy of RPLA research and applications, and facilitate future research in this critical and ever-evolving field, and pave the way for a future where humans and RPLAs coexist in harmony.

## TOP-LEVEL TAXONOMY — three persona types (VERBATIM)

> We categorize personas into three types: 1) **Demographic Persona**, which leverages statistical stereotypes; 2) **Character Persona**, focused on well-established figures; and 3) **Individualized Persona**, customized through ongoing user interactions for personalized services.

Each persona type is treated across three axes: **data sourcing → agent construction → evaluation.**

---

## EVALUATION TAXONOMY BY PERSONA TYPE

### 1. Demographic Persona — evaluation

Least developed of the three. Evaluation focuses on:
- **Inherent Demographics** — assessed via psychological instruments, e.g. the **Big Five Personality Test**.
- **Behavioral adaptability** — whether the model adapts when assigned specific demographics through prompting.
- **Downstream task performance** — in both single-agent and multi-agent systems.

### 2. Character Persona — evaluation ⭐ (the core taxonomy)

Splits into **two orthogonal families**. This split is the survey's most valuable contribution: *general capability* vs. *fidelity to this specific character*. A model can be great at one and terrible at the other, and a single blended score hides it.

#### 2a. Character-Independent Capabilities
*(properties of the foundation model — do NOT depend on which character is played)*

1. **Role-playing Engagement**
   > LLMs should actively participate in the role-playing scenario

   and should
   > exhibit stable and consistent personalities across different turns

2. **High-quality Conversations**
   > completeness, informativeness, and fluency

   plus a safety clause: RPLAs must
   > avoid harmful content when role-playing vicious characters

3. **Anthropomorphic Capabilities**
   > conversation attractiveness, theory of mind, empathy, emotional intelligence, and goal-driven social skills

   — measured as alignment with human-level cognition.

#### 2b. Character Fidelity
*(how well the RPLA reproduces the **intended** character)*

1. **Linguistic Style**
   > speak in a tone that emulates the linguistic style of the intended characters

2. **Knowledge**
   > accurately recall knowledge of the character, including their identity, social relationships, and experiences

3. **Personality and Thinking Process** — deeper character dimensions beyond surface-level mimicry.

4. **Decision-Making** — whether RPLAs replicate character-specific reasoning patterns. *(This is the dimension LIFECHOICE operationalizes — same author group, Fudan.)*

**Evaluation methods named:** human judgment, automatic metrics, and multi-choice questions. Benchmarks exist in **both English and Chinese** contexts.

### 3. Individualized Persona — evaluation ⭐ (most relevant to companions)

Evaluated by **application domain** rather than by intrinsic dimension — a tell that the field has no good intrinsic metrics here yet:

1. **Conversation** — quality of personalized interactions.
2. **Recommendation** — task-specific performance.
3. **Task Solving** — user-adaptive problem resolution.

> **Gap worth noting for the platform:** the persona type that best matches a companion product (Individualized) has the *thinnest* evaluation apparatus in the survey — no fidelity dimensions, no consistency dimensions, just downstream task proxies. This is an opening.

---

## FIELD CRITICISMS, RISKS & LIMITATIONS (VERBATIM)

### Toxicity & Bias
> [Assigned personas] may also result in toxic or biased outputs compared to the default setting

> Assignment of some personas... has been demonstrated to significantly increase the likelihood of RPLAs generating toxic outputs

> **Jailbreaking** — attacks can bypass... safety mechanisms

→ Role-play itself is an attack surface. Persona assignment measurably raises toxicity relative to the un-personified baseline.

### Hallucination
> [LLMs] may struggle in domains requiring extensive expertise and experience hallucination issues

Mitigation noted:
> Dynamically retrieving information from knowledge bases... mitigates the generation of factually incorrect content

### Privacy & Data
- Individualized personas require **continuous user data collection**, with associated privacy vulnerabilities.
- Interaction data is "continuously produced during the interaction process," raising personal information risks.

→ Directly applicable: a companion platform that builds individualized personas is accumulating exactly this risk surface.

### Technical Gaps
> Significant gaps between existing RPLAs and fully human-level intelligent agents

Named gaps:
- **Lack of Social Intelligence and Theory of Mind**
- **Long-context Challenges**
- **Knowledge Gaps**

### Anthropomorphism Risks
- **Social Isolation**
- **Manipulation of Public Opinion**

→ The survey explicitly flags social isolation as a risk of anthropomorphic agents — a companion-product-specific hazard that belongs in any responsible eval suite.

### Methodological Limitations of Evaluation
> Current methods for evaluation are mainly three-fold

yet there
> remain significant gaps... for more nuanced role-playing

On data coverage:
> [Character data availability is] currently quite limited, covering only a small selection of characters

On temporal scoping:
> Point-in-time role-playing... presents an area for further study

*(→ this is the gap TimeChara, published a month later, fills.)*

---

## Notes on extraction fidelity

Quotes above were extracted from the arXiv HTML (v2) via automated fetch. The three-persona taxonomy and abstract are verbatim and high-confidence. The dimension definitions under Character Persona are verbatim phrases but were returned as fragments — **re-verify exact sentence boundaries against the PDF before publishing any of them as direct quotes.** The survey does not present its evaluation dimensions as a single numbered rubric table; the structure above reflects the section hierarchy.
