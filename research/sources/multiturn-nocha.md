---
title: "One Thousand and One Pairs: A 'novel' challenge for long-context language models (NoCha)"
url: https://arxiv.org/abs/2406.16264
authors: Marzena Karpinska, Katherine Thai, Kyle Lo, Tanya Goyal, Mohit Iyyer
year: 2024
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# NoCha — A Novel Challenge for Long-Context Language Models

Submitted 2024-06-24. Published EMNLP 2024. Full text read from https://arxiv.org/html/2406.16264v2

**This is the strongest single piece of evidence for the synthetic-vs-real validity gap — (b) in the brief.**

## Dataset

- **67 books** total: 63 recently-published (2023–2024) English fiction + 4 classic novels.
  - *Why recent:* published after model training cutoffs, so the task **cannot be solved from parametric knowledge / memorized plot summaries.** This is a contamination control, and it is why the 4 classics are broken out separately.
- **Average length: 127,324 tokens (98,587 words)** — genuinely book-length, at/beyond many models' claimed windows.
- **1,001 minimal pairs** of true/false claims, **written by human readers** who had actually read the books.
- Collection cost: **$3,330 USD.** (Notable: real comprehension data is expensive. Synthetic needles are free. This is much of why the field defaults to NIAH.)

## Task design — minimal pairs

Each item is a **pair**: one true claim and one false claim about the *same event/entity*, differing **only** by the false information.

Rationale (VERBATIM intent): the minimal-pair design prevents models from being **"correct for the wrong reason"** and enables straightforward quality control.

**Scoring — Pair Accuracy:** the model gets credit **only if it correctly labels BOTH the true and the false claim in a pair. No partial credit.**

**Why this matters methodologically:** a model that always answers "true" scores 50% on individual claims but **0% on pairs**. Pair accuracy destroys the degenerate strategy. Random baseline is therefore **25%** (0.5 × 0.5), not 50%. This is a design pattern worth stealing wholesale for companion memory eval — probe each remembered fact with a matched true/false pair so "agreeable sycophancy" (a companion's *characteristic* failure mode — these models are tuned to affirm) scores zero rather than 50%.

Annotators confirmed most pairs require reasoning across the **entire book**, not surface retrieval.

## Results — full table (EXACT)

| Model | Pair Accuracy | Correct/Total |
|---|---|---|
| **Human baseline** | **96.9%** | 124/128 |
| GPT-4o | 55.8% | 344/617 |
| Claude-3-Opus | 49.4% | 463/937 |
| Gemini Pro 1.5 | 48.1% | 247/514 |
| Claude-3.5-Sonnet | 41.0% | 384/937 |
| GPT-4-Turbo | 40.2% | 248/617 |
| Gemini Flash 1.5 | 34.2% | 176/515 |
| **Random baseline** | **25.0%** | 250/1001 |
| Command R | 19.6% | 87/445 |
| Command R+ | 17.3% | 77/445 |
| LongLLaMA | 4.9% | 61/937 |
| Phi-3-mini | 9.3% | 23/247 |
| Gemma-10M | 3.9% | 39/1001 |

**Read this table carefully:**
- Best model **GPT-4o: 55.8%** vs **human 96.9%** — a **41.1-point gap.**
- **Every open-weight model scores at or BELOW the 25% random baseline.** Command R (19.6%), Command R+ (17.3%), LongLLaMA (4.9%), Phi-3-mini (9.3%), Gemma-10M (3.9%). Below-random on a pair metric means systematic bias (e.g. answering "true" too often), not just ignorance.
- **Gemma-10M claims a 10M-token context and scores 3.9%.** The context-length number on the box is marketing.
- Note the **unequal denominators** (617, 937, 514, 445, 247, 1001) — models were only scored on books that fit their context window / that they could process. Cross-model comparison is therefore **not strictly apples-to-apples**; a model with a smaller denominator was evaluated on an easier (shorter) subset. Worth flagging when citing.

## The NIAH validity gap — the money finding (VERBATIM)

> "needle-in-the-haystack" tasks measure **"surface-level retrieval capabilities"** rather than genuine comprehension.

> "synthetic long-context LLM benchmarks (e.g., 'needle-in-the-haystack') test only surface-level retrieval capabilities"

**The direct quantitative comparison:**
> Despite models achieving **84.8–89.6% on NIAH variants**, **GPT-4-Turbo dropped to 40.2%** and **Command R dropped to 19.6%** on NoCha.

**This is the single most citable number pair in the whole cluster.** Same models, same context lengths. ~85–90% on the synthetic needle test → 40.2% / 19.6% on real narrative comprehension. Command R falls from ~85% to *below random chance*. NIAH is not merely an imperfect proxy for comprehension — for some models it is **anti-correlated with it at the decision boundary**. A NIAH score of 90% is consistent with a comprehension score of 19.6%.

## Evidence-scope analysis — a graded difficulty axis

| Claim scope | Accuracy |
|---|---|
| Sentence-level (evidence in one sentence) | 59.8% |
| Passage-level | 47.6% |
| Global reasoning (whole book) | 41.6% |

Monotonic decline as required evidence gets more distributed: **59.8 → 47.6 → 41.6**.

Crucially: **even sentence-level claims — the case closest to NIAH, where the evidence sits in a single locatable sentence — only reach 59.8%**, still far below the 84.8–89.6% NIAH scores. So the gap is *not* purely explained by "global reasoning is hard." Even *localized* retrieval on **real prose** is much harder than localized retrieval on **synthetic needles**. The artificiality of the needle itself is doing a lot of work: a UUID in an essay is lexically alien and pops out; a true fact about a character is camouflaged in semantically similar surrounding narrative. **The distractors in real text are the problem.**

## Genre effects

| Genre | Accuracy |
|---|---|
| Historical fiction | 56.4% |
| Contemporary fiction | 46.8% |
| Speculative fiction | 38.8% |

Speculative fiction is hardest — the authors attribute this to **world-building**: the model cannot fall back on real-world priors when the story invents its own rules/entities, so it must actually track the text.

**Highly relevant to us:** a roleplay companion with an invented persona, invented backstory, and an invented shared history with the user is *exactly the speculative-fiction case*. The model cannot lean on world priors; it must track what was actually established in the conversation. **38.8% is the closest analogue in this paper to our setting, and it is the worst number in the table.**

## Explanation accuracy — models are right for the wrong reasons

Error rates in model-generated **justifications**, even when the label was **correct**:
- Claude-3-Opus: **16.9%**
- GPT-4o: **21.7%**
- Gemini Flash 1.5: **65.9%**

**Major methodological warning.** Even on items scored correct, ~1 in 5 of GPT-4o's explanations contain errors — and **two-thirds** of Gemini Flash's. The label was right; the reasoning was confabulated. Accuracy on the label **overstates** true comprehension.

For a companion platform this is the whole ballgame: the product surface *is* the explanation. A companion that recalls the right fact but confabulates the surrounding circumstances ("I remember you love hiking — that trip with your brother!" when it was your sister) is **experienced as a memory failure even though a fact-recall metric scores it correct.** Any companion memory eval that only scores fact-match will systematically miss the failure mode users actually notice and resent. **We need to score the justification, not just the recall.** This finding alone argues for an LLM-judge or human-rated explanation component in our rubric rather than pure string/fact matching.

## Relevance to companion / conversational memory eval

1. **The 85–90% NIAH → 40.2%/19.6% NoCha drop is the headline argument** that needle tests do not license claims about comprehension or memory. Cite this whenever someone says "the model has a 1M context, memory is solved."
2. **Minimal pairs + pair accuracy** is a directly stealable design: it kills sycophantic "yes" bias, which is the dominant confound in companion models specifically.
3. **Contamination control via recency** (books published after cutoff) is a real design constraint. Our analogue is easy: conversations we generate are inherently novel and uncontaminated — a genuine advantage of synthetic *conversations* over synthetic *documents*.
4. **The speculative-fiction result (38.8%)** is the best available estimate for how models handle invented, self-contained worlds — i.e. personas.
5. **The explanation-error result** means label-only metrics overstate performance; score the reasoning too.
6. **CAVEAT / remaining gap:** NoCha is still *documents* — novels, third-person narrative, read all at once. It has **no turn structure, no interlocutor, no facts that change over time, and no stake in the reader's own life.** It is much closer to real comprehension than RULER, but it is **still not conversational memory.** Nothing in this cluster evaluates the thing we actually need.
