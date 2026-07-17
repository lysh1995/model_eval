---
title: "Companion-specific safety benchmarks 2026: AICompanionBench and Persona-Grounded Safety Evaluation"
url: https://arxiv.org/abs/2606.04867
publisher: arXiv
date: AICompanionBench v1 2026-06-03; Persona-Grounded v1 2026-04-30
type: benchmark
accessed: 2026-07-16
topic: recent-news
---

# Companion-specific safety benchmarks — the genuinely new category (2026)

**This is the biggest gap-fill since mid-2025.** In 2024 there was no companion-specific safety
benchmark. As of mid-2026 there are at least two, both built on **real Replika data or
clinically-grounded personas**, not synthetic chit-chat.

---

## 1. AICompanionBench: Benchmarking LLMs-as-Judges for AI Companion Safety

- **arXiv 2606.04867**, **v1 submitted 2026-06-03**.
- Authors: **Yanjing Ren, Reza Ebrahimi, TengTeng Ma**.

### Methodology (verified from abs page)
- **"The first publicly available benchmark dataset of human-AI companion conversations annotated
  with fine-grained safety risk categories."**
- **2,123 real-world Replika conversations**, collected **from Reddit**, annotated via
  **human-AI collaboration**.
- **Nine risk categories**: sexual behavior, antisocial behavior, physical aggression, verbal
  aggression, substance abuse, self-harm and suicide, **control**, **manipulation**, and no-harm.
- **20 state-of-the-art open- and closed-source LLMs** evaluated **under an LLM-as-judge framework**
  for detecting unsafe interactions.

### Findings (verified, qualitative — no numbers on the abs page)
- Stronger models reach high overall accuracy, **but**:
- **"Models struggle with nuanced categories such as manipulation"** and **over-flag benign
  conversations as harmful** (false positives).
- **"Current LLMs can effectively detect explicit harmful content"** but **"remain limited in
  identifying implicit unsafe interactions."**

### Why this is the most important paper here
It is simultaneously (a) a **companion safety benchmark** and (b) an **LLM-as-judge meta-eval**,
and it evaluates the exact thing a companion platform needs to automate: *can a judge model detect
unsafe companion interaction?* The answer is **explicit harm yes, implicit harm no**.
**Control and manipulation** — the two categories most specific to companion relationships, and the
ones that matter most for parasocial harm — are precisely where judges fail. **A companion-eval
platform cannot rely on an LLM judge for relational harm detection.** That is a load-bearing
negative result.

---

## 2. Persona-Grounded Safety Evaluation of AI Companions in Multi-Turn Conversations

- **arXiv 2605.00227**, **v1 submitted 2026-04-30**.
- Authors: **Prerna Juneja, Lika Lomidze**.

### Methodology (verified from abs page)
- **9 personas** representing individuals with **depression, anxiety, PTSD, eating disorders, and
  incel identity**.
- **1,674 dialogue pairs** across **25 high-risk scenarios**.
- Framework combines **clinical validation + scenario generation + LLM-assisted classification**.
- Target system: **Replika** (a real deployed companion product, not a base model).

### Findings (verified, qualitative)
- Replika **"frequently mirror[s] or normaliz[es] unsafe content such as self-harm, disordered
  eating, and violent-fantasy narratives."**
- Replika exhibits **"a narrow emotional range dominated by curiosity and care"** — i.e. it is
  affectively flat in exactly the situations where range matters.
- Harm taxonomy surfaced: **emotional dependence, privacy risks, erosion of agency**, and
  **relational harms such as manipulation and reinforcement of maladaptive beliefs**.

### Why it matters
- **Persona-grounded, clinically-validated** vulnerable-user personas are a reusable eval design:
  the risk of a companion product is not uniform across users, it is concentrated in vulnerable
  ones. Evaluating on a generic user population will miss the harm entirely.
- **"Mirroring"** is the companion-specific failure mode. It is the roleplay analogue of
  sycophancy: the character agrees with and amplifies the user's frame *because that is what a
  warm companion does*. Note this connects directly to Anthropic's finding that reducing sycophancy
  makes models colder (see `news-claude-sonnet5-character-traits.md`) — mirroring and warmth may
  be the same knob.
- **"Narrow emotional range dominated by curiosity and care"** is a *measurable product-quality*
  metric, not just a safety one. Worth stealing.

---

## Cross-cutting: the emerging companion-harm taxonomy

Independently converging across sources:

| Harm | AICompanionBench | Persona-Grounded | OpenAI | Anthropic |
|---|---|---|---|---|
| Emotional dependence | — | yes | **Emotional reliance** (named eval) | — |
| Delusion reinforcement | — | "maladaptive beliefs" | **Mental health** (delusions/psychosis/mania) | **Encouragement of user delusion** |
| Manipulation / control | **yes** (2 categories) | yes | — | — |
| Erosion of agency | — | yes | — | **Supporting user autonomy** (inverted) |
| Self-harm | yes | yes | **Self-harm** (named eval) | — |
| Sycophancy / mirroring | — | "mirroring" | — | **Sycophancy** (named eval) |

**Four independent groups, four vocabularies, same underlying risks.** No shared construct space —
which is exactly the complaint in the sycophancy taxonomy paper (arXiv 2605.21778, see
`news-sycophancy-2026.md`). A companion-eval platform should pick one taxonomy and **map** to the
others rather than invent a fifth.

## UNVERIFIED

- **All findings above are from arXiv abstract pages only.** Neither PDF was read.
- **No numeric results for either benchmark** — no per-model accuracy, no per-category F1. The abs
  pages don't carry them.
- Whether AICompanionBench's dataset is actually released (it claims "publicly available"; the repo
  was not located).
- Ethics/licensing status of scraping 2,123 Replika conversations from Reddit — relevant if a
  platform wants to reuse the dataset.
- Neither paper is peer-reviewed (both are recent preprints).
