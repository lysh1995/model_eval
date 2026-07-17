---
title: "LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding; and LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks"
url: https://arxiv.org/abs/2308.14508 (v1); https://arxiv.org/abs/2412.15204 (v2)
authors: "v1: Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, Yuxiao Dong, Jie Tang, Juanzi Li. v2: Yushi Bai, Shangqing Tu, Jiajie Zhang, Hao Peng, Xiaozhi Wang, Xin Lv, Shulin Cao, Jiazheng Xu, Lei Hou, Yuxiao Dong, Jie Tang, Juanzi Li (Tsinghua/THUDM)"
year: 2023 (v1), 2024 (v2)
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# LongBench v1 and v2

Sources: abstract pages + https://longbench2.github.io/ leaderboard + https://aclanthology.org/2025.acl-long.183/
Note: full-text HTML for v2 was not retrievable (404s / oversized); some per-category details are marked UNVERIFIED below.

---

## LongBench v1 (arxiv 2308.14508)

**"LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding"** — submitted 2023-08-28, accepted **ACL 2024**.

- **21 datasets** across **6 task categories**: single-document QA, multi-document QA, summarization, few-shot learning, synthetic tasks, code completion.
- **Bilingual: English and Chinese.**
- **Average context lengths: 6,711 words (English) and 13,386 characters (Chinese).**
- Finding: "Commercial model (GPT-3.5-Turbo-16k) outperforms other open-sourced models."
- **Exact per-model accuracy numbers were NOT retrieved** — the abstract page does not carry the results table. NOT FABRICATED HERE. If needed, pull from the full PDF or https://github.com/THUDM/LongBench.

**Assessment for our purposes:** v1's average context (~6.7K words) is **short by modern standards** — well inside every current model's effective length per RULER/NoLiMa. It is largely **saturated** and is superseded by v2. Its "synthetic tasks" category is NIAH-family and inherits all the critiques in `multiturn-niah-critique.md`. Low value for us except as historical baseline.

---

## LongBench v2 (arxiv 2412.15204) — the relevant one

**"LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks"** — submitted 2024-12-19, revised 2025-01-03. **ACL 2025** (https://aclanthology.org/2025.acl-long.183/).

### Design
- **503 challenging multiple-choice questions.**
- **Context length range: 8k to 2M words.**
- Annotated by **"nearly 100 highly educated individuals with diverse professional backgrounds"**, with manual and automated quality review.
- **Multiple-choice format** is a deliberate choice: it makes evaluation **reliable and automatic** (no LLM judge, no ROUGE), at the cost of not testing generation. Contrast with NoCha's minimal-pairs, which also uses a forced binary but pairs items to kill answer bias — **v2's plain MC does not have that protection**, so a 4-way MC has a 25% floor from guessing alone.

### The 6 task categories
1. Single-document QA
2. Multi-document QA
3. Long in-context learning
4. **Long-dialogue history understanding** ← the directly relevant one
5. Code repository understanding
6. Long structured data understanding

**UNVERIFIED / NOT FOUND:** the exact number of questions in the long-dialogue-history category, precisely what it tests (agent-agent vs user-assistant dialogue), and any **per-category accuracy breakdown**. Neither the abstract page, the ACL Anthology landing page, nor the leaderboard site exposed these; the arxiv HTML full text 404'd/overflowed. **Not fabricated.** To resolve: fetch the PDF (https://aclanthology.org/2025.acl-long.183.pdf) or inspect the HF dataset `zai-org/LongBench-v2`, which has a category field and can be counted directly. **Worth doing — this is the single closest existing item to a conversational-memory benchmark task in the mainstream long-context literature, and knowing its size and construction would tell us how much prior art we're up against.**

### Results (EXACT, from the official leaderboard)

**Human experts (15-minute constraint): 53.7% overall.**
- **100% on the Easy subset**
- **25.1% on the Hard subset**

| Model | Overall |
|---|---|
| Gemini-2.5-Pro (w/ CoT) | 63.3% |
| Gemini-2.5-Flash (w/ CoT) | 62.1% |
| Qwen3-235B-A22B-Thinking | 60.6% |
| DeepSeek-R1 | 58.3% |
| **o1-preview** | **57.7%** |
| **Human expert (15 min)** | **53.7%** |
| GPT-4o (Aug 2024) | 50.1% |
| Qwen2.5-72B | 42.1% |
| Claude 3.5 Sonnet | 41.0% |
| Llama 3.1 70B | 31.6% |

By difficulty across top models: "Easy subset shows 46.7–75% accuracy; Hard subset ranges 41.5–56.7%". Short contexts (0–32k words) generally outperform long contexts (128k–2M words).

At publication (Dec 2024): best model **without** extended reasoning = **50.1% (GPT-4o)**; **o1-preview at 57.7% surpassed the human baseline by 4 points.**

### Critical caveat on the human baseline — read before citing

**The 53.7% human number is under a 15-minute time limit on contexts up to 2M words.** That is not a measure of human comprehension; it is a measure of **human skimming speed under extreme time pressure.** A human cannot read 2M words — or even 128k — in 15 minutes. The tell is in the split: humans score **100% on Easy** and **25.1% on Hard**. On a 4-way MC, **25.1% is exactly chance.** So the human baseline decomposes into "perfect when they could find it, coin-flip when they couldn't." The number reflects **retrieval-under-time-budget**, not understanding.

**Therefore "o1-preview (57.7%) beats humans (53.7%)" is a badly misleading headline** and should not be repeated without this context. It reports that a model with unlimited reading time beats a human given 15 minutes. NoCha's human baseline — **96.9%**, from readers who actually read the books — is the honest comparison, and there the best model (GPT-4o, 55.8%) is **41 points behind.** The two human baselines differ by **43 points** and the difference is almost entirely **methodological**, not a fact about humans.

**Lesson for our platform:** how you construct a human baseline determines whether you conclude "superhuman" or "41 points behind." Time-boxed human baselines on long contexts measure the time box. If we build a human baseline for companion memory, **give humans the time they need**, or we will manufacture a flattering result. This is the most transferable methodological warning in the LongBench line of work.

## Relevance to companion / conversational memory eval

1. **v2's "long-dialogue history understanding" category is the closest mainstream-benchmark analogue** to what we need, but it is **one of six categories in a 503-question set** — so it is at most ~80 questions, likely fewer. Nowhere near a dedicated conversational memory benchmark. **The niche is open.**
2. **v2 is genuinely hard and not saturated** (best ~63.3%), unlike v1 and unlike NIAH. Difficulty is a design achievement worth emulating: they hard-filtered for questions experts get wrong under time pressure.
3. **Multiple-choice = cheap reliable scoring** but can't assess generation quality — for a companion, *how* a memory is surfaced matters as much as *whether* (cf. NoCha's 16.9–65.9% explanation error rates, and MemGPT's verbosity artifact). MC would score all of those as correct. **MC is the wrong format for us**, though it's tempting for automation.
4. **Still document-shaped.** Even the dialogue category is *reading a transcript*, third-party, after the fact — not *being a participant* with a stake, a persona to maintain, and facts that changed. The model is a reader, not an interlocutor.
5. **The human-baseline lesson (above) is the most valuable takeaway from this paper for us.**
