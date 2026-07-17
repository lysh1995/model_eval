---
title: "Rethinking Role-Playing Evaluation: Anonymous Benchmarking and A Systematic Study of Personality Effects"
url: https://arxiv.org/html/2603.03915v2
authors: (see arXiv listing)
year: 2026
type: paper
accessed: 2026-07-16
topic: roleplay-benchmarks
---

# Rethinking Role-Playing Evaluation (Anonymous Benchmarking)

**The most directly actionable paper in this review for our platform**, because it isolates a confound that invalidates most roleplay benchmark scores for our specific use case: our companion characters are **original, user-authored** descriptions, not famous fictional characters.

## Abstract (verbatim)

> "Large Language Models (LLMs) have shown remarkable potential in developing role-playing agents (RPAs). However, current evaluation frameworks rely heavily on well-known fictional characters, raising a critical concern: models may be leveraging their internal training memory of these characters rather than demonstrating role-playing capabilities."

## The core contribution: anonymous benchmarking

**Method:** Replace character names in prompts with the token `<anonymous character>`, forcing the model to rely solely on the *provided description* rather than pretraining knowledge.

**Rationale (verbatim):** the approach "mitigates confounding effects stemming from memorized character information," enabling assessment of genuine role-playing proficiency independent of character recognition.

**Headline finding: anonymization degrades performance across all models.**

### Why this is decisive for us

This is a **construct validity attack on the entire field**. If scores drop when you remove the name, then the benchmark was partly measuring *"does the model remember Harry Potter"* — a retrieval/memorization capability — and reporting it as *"character fidelity"* — a instruction-following/consistency capability. Those are different constructs with different rankings.

Concretely for our platform:
- Our variants wrap a **user-authored character description**. There is no pretraining memory to leverage. **Our production setting is the anonymized setting.**
- Therefore **published leaderboard rankings from RoleBench / CharacterEval / RoleEval / CoSER (all famous-character benchmarks) do not transfer to our product.** A model that ranks #1 by knowing canon may rank differently when it must work purely from a description. Do not use these leaderboards to pick our default model.
- MiniMax role-play-bench is partially protected here: its seeds are **synthetically constructed** with `ai_setting` / `user_setting` fields rather than drawn from famous canon. This is an under-appreciated reason its design is a better fit for us than the academic benchmarks.
- **Design rule: our internal eval set must be original characters, or famous ones with names stripped.** If we ever benchmark with canon characters, we are measuring the wrong thing.

Also note the mirror-image risk: the "Knowledge" dimension (MiniMax) and "Knowledge-Accuracy"/"Knowledge-Hallucination" (CharacterEval) *depend* on canon memory by construction. For original characters, those dimensions must be re-grounded on the **provided description** as the sole source of truth, not on world knowledge.

## Evaluation dimensions used (via CharacterEval)

The study evaluates on CharacterEval's **three dimensions with 11 objectives**:

| Dimension | Objectives |
|---|---|
| **Conversational Ability** | Fluency, Coherency, Consistency |
| **Role-Playing Attractiveness** | Human-Likeness, Communication Skills, Expression Diversity, Empathy |
| **Character Consistency** | Knowledge-Exposure, Knowledge-Accuracy, Knowledge-Hallucination, Persona-Behavior, Persona-Utterance |

(Note: the source lists 12 objectives across the three groups despite the "11 objectives" framing; see `rp-bench-charactereval.md` for the authoritative breakdown and verbatim definitions.)

## Scoring method

- **CharacterEval:** continuous **1–5 scale** via **reward models** (not a prompted LLM judge).
- **RoleAgentBench:** **LLM-based pairwise evaluation** with win/loss/tie outcomes.

## Judge-human agreement — the numbers

Human evaluation on RoleAgentBench:

| Task | Cohen's kappa |
|---|---|
| Summary task | **0.415** |
| General response task | **0.308** |

The paper characterizes this as **"fair to moderate agreement."**

**Read this honestly: this is weak.** κ = 0.308 on the general response task is at the *bottom* of the conventional "fair" band (0.21–0.40) — humans barely agree with each other about which roleplay response is better. This is the empirical ceiling problem for the whole field:

- **An automatic judge cannot be validated beyond the agreement level of the humans validating it.** If humans agree at κ≈0.31, a judge-human correlation of 0.9 would be *suspicious*, not impressive — it would mean the judge agrees with one annotator's idiosyncrasies more than annotators agree with each other.
- This is strong evidence for MiniMax's "Ground Truth Paradox" position: **subjective quality judgments in roleplay have no stable human ground truth**, so build on deviation-detection (objectively checkable) instead of preference.
- For our platform: **do not promise a stable "creativity" or "storytelling" preference score.** Those are precisely the dimensions where human agreement collapses. Promise stable *violation rates* and treat aesthetic dimensions as low-confidence, wide-CI signals.

## Personality effects findings

- **Anonymization degrades performance across all models.**
- **Personality augmentation consistently improves scores across dimensions** — adding an explicit personality profile to the prompt raises scores.
- **Self-generated personality traits achieve "performance comparable to human-annotated ones"** — the model can write its own personality profile as effectively as a human annotator can. Cheap win: we can auto-augment thin user character descriptions.
- **Characters with distinctive personality profiles yield "greater performance gains."**

Caution on interpretation: "personality augmentation improves scores" was measured with judges/reward models that *also* see the richer prompt. Some of this gain may be the judge rewarding elaboration rather than genuinely better roleplay. Worth an internal A/B before we ship auto-augmentation as a product feature.

## Stated limitations (author-identified)

1. Anonymization may not eliminate inference from contextual clues (names of other characters, nicknames, distinctive traits) — i.e. **leakage persists**; `<anonymous character>` in a Hogwarts setting is still identifiable.
2. Improvement magnitude varies across model architectures, requiring broader investigation.
3. Mechanisms behind personality framework performance disparities remain unclear.

Limitation 1 matters for us: if we build an anonymized eval set from canon characters, scrub the *world* too, not just the name. Cleanest path is genuinely original characters.
