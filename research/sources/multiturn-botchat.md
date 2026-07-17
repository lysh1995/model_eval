---
title: "BotChat: Evaluating LLMs' Capabilities of Having Multi-Turn Dialogues"
url: https://aclanthology.org/2024.findings-naacl.201/
authors: Haodong Duan, Jueqi Wei, Chonghua Wang, Hongwei Liu, Yixiao Fang, Songyang Zhang, Dahua Lin, Kai Chen
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# BotChat (Findings of NAACL 2024, pp. 3184–3200)

Full text read from arxiv HTML: https://arxiv.org/html/2310.13650 (versioned URLs v1/v2/v3 all 404; ar5iv conversion failed with a fatal error). Also indexed at https://aclanthology.org/2024.findings-naacl.201.pdf and https://github.com/open-compass/BotChat.

## What it is

Evaluates LLMs' capacity for **human-style multi-turn chatting** by having **two LLM instances talk to each other**, then judging the resulting dialogue. Pipeline:

1. Start from real-world human dialogues; keep the **very first utterances as the ChatSEED**.
2. Prompt the LLM to generate a full multi-turn dialogue (**"tens of utterances"**) from the ChatSEED, **utterance by utterance**.
3. Use a SOTA LLM (**GPT-4**) as judge.

Key framing: this is *self-chat*, not model-vs-user. The model plays both sides. Relevant to us because that is exactly the cheap-simulation shape a companion eval would reach for.

## UNIT OF EVALUATION — per-DIALOGUE, not per-response

The judge's object is **an entire generated dialogue**, scored as a whole. UniEval asks the judge, of a whole dialogue:

1. whether the dialogue involves a chatbot,
2. if yes, **the index of the first AI-generated utterance**,
3. an explanation.

So the primary metric is a **per-dialogue binary "did it pass as human"**, not a per-turn quality score. Note the interesting hybrid: question (2) recovers a **turn-level breakdown point** — *where* the dialogue stopped being human-like — while still scoring the dialogue as one unit. That "first utterance at which the mask slips" index is arguably the most portable idea in this paper for companion evals.

BotChat Arena's unit is **a pair of whole dialogues** (pairwise preference). GTEval's unit is **a generated dialogue vs its ground-truth human counterpart**.

## Three evaluation protocols

**1. UniEval (unitary / Turing-style)** — judge sees one dialogue in isolation, decides if a chatbot is involved. "Pass" = judged human. Per-dialogue.

**2. BotChat Arena (pairwise)** — LLM pairs compared head-to-head; scored with **Bootstrap ELO**, shuffled **1000 times** rather than vanilla ELO for stability:

> "Bootstrap ELO is a stable metric, the standard deviation of the Bootstrap ELO of LLMs across different runs is at most 1.4."

**3. GTEval (ground-truth)**:

> "GTEval involves a comprehensive comparison of the generated conversations with the 'Ground Truth' conversations in the test split of MuTual."

**Judge**: GPT-4-0613 across all experiments, prompted with in-context examples to strengthen instruction-following.

## Dataset / ChatSEED counts

- Major data source of human dialogues: **MuTual**.
- > "We employ the first two utterances of each dialogue in its test split as the ChatSEED for dialogue generation."
- **MuTual-Test comprises 547 distinct dialogues → 547 ChatSEEDs** (first two utterances retained).
- For **GTEval / Arena**, a filtered subset: > "we select a subset of 222 conversations from MuTual-Test, with each conversation comprises at least 4 utterances." → **222 ChatSEEDs**.
- Ground-truth reference dialogues in that subset run **4–15 utterances, averaging 7.4**; generated dialogues are truncated to match reference length for GTEval.
- Total generated dialogues reported ≈ **7,658** (547 × 14 models).

## TURN-DEPTH FINDING — quality degrades sharply as N grows (the headline result)

**N counts total utterances in the dialogue, including the two ChatSEED utterances.**

> "we set the dialogue round to N (N=16 in our experiments, including the initial two utterances) to generate dialogues."

N settings swept: **N = 4, 8, 16**.

The explicit degradation statement, verbatim:

> "For all LLMs, the quality of generated dialogues declined quickly as long as the dialogue turns increase."

The gap between models **widens dramatically with N** — models are near-indistinguishable at short N and separate at long N:

> "For N=4 (only 2 utterances are generated), the gap for two InternLM variants is merely 1.5% success rate,"

…but that gap widens sharply by N=16. At **N=16**:

> "GPT-4 demonstrates a remarkable success rate of over 65%, while the second best Vicuna-13B and the third best InternLM-20B achieve only 55% and 36%."

This is the load-bearing finding for us: **at N=4 the eval has almost no discriminative power (1.5% spread); at N=16 it spreads models across ~30 points.** Short dialogues do not just under-measure — they fail to *rank*. Any companion eval that stops at 2–4 exchanges is measuring noise.

Bootstrap ELO also spreads with N (GPT-4 pulls away):
- **N=8**: GPT-4 1103.9; Vicuna-13B 1096.5; InternLM-20B 1092.8 (tightly bunched, ~11 points total)
- **N=16**: GPT-4 1167.2; Vicuna-13B 1113.3; InternLM-20B 1094.4 (~73 points total)

Same story: **discriminative power is a function of dialogue depth.**

## SINGLE-TURN vs MULTI-TURN GAP

BotChat has **no single-turn arm** — it does not run a single-turn vs multi-turn comparison, so it offers no direct single-vs-multi-turn delta. Its analogue is the **short-N vs long-N gap** documented above (N=4 → N=16), which is where all its turn-depth evidence lives.

The paper's qualitative account of *why* long dialogues fail — the failure modes we should expect to see in companion transcripts:
- **poor instruction-following capability**
- **tendency to generate lengthy utterances** (verbosity drift; utterance length measured in tokens via the CL100K tokenizer)
- **limited general capability**

Overall conclusion: GPT-4 generates human-style multi-turn dialogues with "impressive quality" and "significantly outperforms its counterparts" — > "It's difficult for a discriminator to distinguish between GPT-4 generated dialogues and human dialogues." Other LLMs struggle. Generating lengthy dialogues remains hard, **especially in Chinese**.

## HUMAN AGREEMENT — NOT MEASURED (do not cite a number here)

**The paper reports no original human-agreement or judge-human-correlation numbers.** I checked for this specifically and found none. The framing is explicitly that human evaluation is what they are *avoiding*:

> "However, human-based evaluation of such capability involves intensive manual labor."

They cite prior work (Zheng et al., 2023 — MT-Bench) for high GPT-4/human agreement, but **run no human study of their own and publish no agreement percentage for BotChat's judges.** The paper's internal validity claim is instead *convergence across protocols*: "With different evaluation protocols, we come to substantially identical conclusions" — agreement between UniEval / Arena / GTEval, not agreement with humans.

If we cite BotChat for judge reliability, that is the honest claim available: **cross-protocol convergence, not human validation.** Any human-agreement figure attributed to BotChat would be fabricated.

## Takeaways for a companion/roleplay eval platform

- **Sweep dialogue length; do not fix it short.** The N=4 → N=16 widening (1.5% → ~30-point spread) is the cleanest published evidence that short dialogues cannot rank models.
- **The "index of first AI-generated utterance" is a directly stealable metric** — a turn-indexed breakdown point, giving turn-level diagnosis while keeping a per-dialogue unit.
- **Self-chat is a viable cheap harness** but note the models play both sides, so failures compound; this measures *dialogue-generation* quality, not response quality against a fixed interlocutor.
- **Bootstrap ELO (1000 shuffles, SD ≤ 1.4)** is a cheap stability upgrade over vanilla ELO for our pairwise arena.
- Verbosity drift and instruction-following decay are the named long-dialogue failure modes to instrument for.

## Verification notes

- The abstract, the "declined quickly as long as the dialogue turns increase" quote, the N definition (N=16 incl. two ChatSEED utterances), the N=16 pass rates (GPT-4 >65% / Vicuna-13B 55% / InternLM-20B 36%), the N=4 InternLM 1.5% gap, the Bootstrap ELO stability quote (SD ≤ 1.4), the ChatSEED counts (547 and 222), the GTEval definition, and the 4–15 / avg 7.4 utterance reference lengths were read from the arxiv HTML full text.
- **UniEval per-model pass rates at every N are presented as a figure (Fig. 4), not a table.** Only the N=16 narrative values above are recorded verbatim; per-N values for the full model roster were not extractable from text and are **not** reproduced here rather than guessed.
- The Bootstrap ELO values at N=8 and N=16 were read from a results table via HTML extraction; treat as **medium confidence** and re-verify against the PDF before publishing. The N=16 ordering and the widening trend are separately corroborated by the narrative text.
- The ~7,658 total-dialogue figure (547 × 14 models) was derived by the extraction and should be re-checked against the paper's model count before citing.
- **No human-agreement number exists in this paper** — see section above.
