---
title: "Needle-in-a-Haystack critiques: why NIAH is a weak and saturated test (NoLiMa + RULER + NoCha convergent evidence)"
url: https://arxiv.org/abs/2502.05167
authors: "Primary source — NoLiMa: Ali Modarressi, Hanieh Deilamsalehy, Franck Dernoncourt, Trung Bui, Ryan Rossi, Seunghyun Yoon, Hinrich Schütze. Secondary: Hsieh et al. (RULER), Karpinska et al. (NoCha), Liu et al. (Lost in the Middle)"
year: 2025
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# Why needle-in-a-haystack is a weak test

This file synthesizes the critique across four sources. **Primary new source: NoLiMa (arxiv 2502.05167), "Long-Context Evaluation Beyond Literal Matching", 2025** — full text from https://arxiv.org/html/2502.05167v2. Cross-references RULER, NoCha, and Lost in the Middle (see their own files).

## What the vanilla NIAH test actually is

Insert a sentence (the "needle" — typically a random fact or UUID, e.g. "The best thing to do in San Francisco is eat a sandwich in Dolores Park on a sunny day") into a long body of filler text (the "haystack" — commonly Paul Graham essays), then ask a question whose wording **directly and lexically overlaps** the needle. Vary depth and context length; plot a heatmap. Originated as an informal engineering probe (Greg Kamradt), not a peer-reviewed benchmark — **it was never designed to measure comprehension, and its adoption as the industry-standard long-context claim is an accident of convenience.** It is cheap, it makes a pretty green heatmap, and vendors ship it in launch blogs.

## Critique 1 — NIAH tests literal lexical matching, not reasoning (NoLiMa)

NoLiMa's core question (VERBATIM):
> "Do such literal matches make it easier for language models to locate relevant information and output correct answers?"

The paper's argument: existing long-context benchmarks, **particularly NIAH, contain problematic literal matches between questions and relevant information**, which lets models exploit **surface-level matching** rather than demonstrate real long-context reasoning. The needle is *lexically alien* to its surroundings — it pops out on simple token matching. **This is closer to `grep` than to memory.** An attention head that does approximate string matching solves it.

**NoLiMa's design:** needles and questions have **minimal lexical overlap**, "requiring models to infer latent associations to locate the needle within the haystack." One-hop and two-hop associative reasoning; **58 curated question-needle pairs.**

E.g. rather than asking "who went to Dolores Park?" about a needle saying "X went to Dolores Park", the needle says something that requires an associative hop — you must know the semantic link to find it. This is the realistic case: **real recall is cued by meaning, not by matching strings.**

### NoLiMa results — Table 3 (EXACT)

| Model | Base (1K) | 4K | 8K | 16K | 32K |
|---|---|---|---|---|---|
| GPT-4o | 99.3% | 95.7% | 89.2% | 81.6% | **69.7%** |
| Llama 3.3 70B | 97.3% | 81.5% | 72.1% | 59.5% | **42.7%** |
| Llama 3.1 405B | 94.7% | 74.5% | 60.1% | 48.4% | **38.0%** |
| Llama 3.1 70B | 94.5% | 71.2% | 62.7% | 51.8% | **43.2%** |
| Gemini 1.5 Pro | 92.6% | 75.4% | 63.9% | 55.5% | **48.2%** |
| Jamba 1.5 Mini | 92.4% | 70.8% | 62.2% | 52.7% | **43.6%** |
| Command R+ | 90.9% | 66.3% | 39.5% | 21.3% | **7.4%** |
| Claude 3.5 Sonnet | 87.6% | 77.6% | 61.7% | 45.7% | **29.8%** |
| Mistral Large 2 | 87.9% | 73.3% | 51.5% | 32.6% | **18.7%** |
| GPT-4o mini | 84.9% | 44.1% | 32.6% | 20.6% | **13.7%** |
| Gemini 1.5 Flash | 84.7% | 51.0% | 44.4% | 35.5% | **28.6%** |
| Llama 3.1 8B | 76.7% | 44.1% | 31.9% | 22.6% | **14.2%** |

**Headline (VERBATIM):**
> "At 32K, for instance, 10 models drop below 50% of their strong short-length baselines. Even GPT-4o, one of the top-performing exceptions, experiences a reduction from an almost-perfect baseline of 99.3% to 69.7%."

**Effective context length (85%-of-base threshold):** models claim **128K–2M** tokens, but **most achieve only ≤2K effective length; GPT-4o reaches only 8K.**

**Sit with that.** Remove the lexical shortcut and GPT-4o's *effective* context is **8K** against a claimed **128K** — a **16x** overstatement. Most models: **≤2K** against claims of 128K–2M — up to **1000x**. Command R+ falls to **7.4% at 32K** from a 90.9% base. These are *far* more brutal than RULER's numbers (which gave GPT-4 an effective 64K), and the *only* difference is that NoLiMa removed the word-matching crutch. **Nearly the entire apparent long-context capability of these models, as measured by NIAH, is literal string matching.**

## Critique 2 — NIAH is saturated and has no discriminative power (RULER)

> "The needle-in-a-haystack (NIAH) test... has been widely adopted to evaluate long-context language models. However, this simple retrieval-based test is indicative of only a superficial form of long-context understanding."

> "Despite achieving nearly perfect accuracy in the vanilla NIAH test, almost all models exhibit large performance drops as the context length increases."

RULER: NIAH reveals "merely the retrieval capability, failing to gauge other forms of long-context understanding." **Everyone scores ~100% → the test cannot rank models.** A benchmark all models pass conveys **zero bits** about which model to use. Yet RULER shows those same models have effective lengths from **<4K to >128K** — a >32x spread that vanilla NIAH renders invisible.

## Critique 3 — the empirical gap to real comprehension (NoCha)

The most direct quantitative evidence:
> Despite models achieving **84.8–89.6% on NIAH variants**, **GPT-4-Turbo dropped to 40.2%** and **Command R dropped to 19.6%** on NoCha (real narrative claim verification).

Same models. Same context lengths. **~85–90% synthetic → 40.2% / 19.6% real.** Command R goes from ~85% to **below the 25% random baseline.** And NoCha's *sentence-level* claims — the subset most similar to NIAH, evidence in one locatable sentence — still only reach **59.8%**, proving the gap isn't just "global reasoning is hard": **localized retrieval in real prose is itself far harder than localized retrieval of a synthetic needle.** The artificial needle's alienness is doing the work.

## Critique 4 — NIAH hides positional effects that real tasks expose (Lost in the Middle)

Claude-1.3 does **"nearly perfectly on all evaluated input context lengths"** on key-value retrieval (essentially NIAH) — yet its multi-document QA **oracle** accuracy is only **76.1%**, the lowest of the models tested. **Perfect synthetic retrieval, weakest real comprehension, same model.**

Also: **query-aware contextualization** achieved "near-perfect performance on the 75, 140, and 300 key-value pair settings" but **"minimally affects performance trends in the multi-document question answering task."** A trivial prompt-order change erases the synthetic deficit and leaves the real one intact — **proof the two tasks measure different constructs.** If reformatting your prompt fixes the benchmark, the benchmark measured formatting.

## What NIAH fails to measure — consolidated

1. **Associative/semantic retrieval** — real recall is cued by meaning, not string overlap (NoLiMa: removing overlap collapses effective length to ≤2K–8K).
2. **Multi-hop / chained reasoning** — MemGPT: GPT-3.5 hits **0%** at 1+ nesting levels; GPT-4 **0%** at 3+. NIAH is the zero-hop special case.
3. **Aggregation / synthesis** — counting, summarizing, "what are the themes" (RULER's CWE/FWE).
4. **Distractor robustness** — a real haystack contains *near-miss* facts. NIAH's haystack is unrelated filler; the needle has **no competitors.** (RULER's MK-NIAH adds hard distractors and models degrade.)
5. **Multi-value / multi-query recall** — "tell me everything about X" (RULER MV/MQ-NIAH).
6. **Positional robustness** — a single depth-vs-length heatmap averages over the U-shaped curve.
7. **Global comprehension** — NoCha: 41.6% on whole-book reasoning.
8. **Faithful justification** — NoCha: **16.9%–65.9%** of explanations wrong *even when the label is right.*
9. **CONVERSATIONAL structure** — no turn boundaries, no speaker attribution, no interlocutor, **no facts that change over time.** The needle is static and true forever.

## The validity gap, stated plainly

**NIAH is a `grep` test with a lexical shortcut, administered on filler text with no competing information, probing a static fact that was never contradicted.** Real conversational memory requires **associative retrieval of possibly-superseded, emotionally-weighted facts, from semantically similar surrounding dialogue, spoken by a specific party, at a specific time, where the *wrong* recall is worse than none.** NIAH shares almost none of this structure. Passing it licenses **no** inference about companion memory.

The strongest sound bite, in one line: **remove the literal string match (NoLiMa) and GPT-4o's effective context drops from a claimed 128K to 8K; most models to ≤2K.** Everything vendors advertise as "1M context" rests on a test that measures string matching.

## Relevance to companion / conversational memory eval

1. **Never report NIAH-style metrics as evidence of companion memory.** They are saturated, lexically gameable, and empirically ~45 points optimistic vs real comprehension.
2. **NoLiMa's central design lesson is the one to steal: eliminate lexical overlap between probe and target.** If we ask "what's my cat's name?" and the history says "my cat is named Mia," we are running NIAH and will get a flattering, meaningless number. Probes must require an **associative hop** — the user *mentioned Mia*, and we ask something that requires knowing Mia is the cat without saying so. This is the difference between a benchmark that measures our product and one that measures `grep`.
3. **NoLiMa's "effective length at 85% of base" threshold method** (cf. RULER's Llama2-7B-at-4K threshold) is directly adaptable: define **"effective conversation length"** = max turns at which a companion holds ≥85% of its own short-conversation recall score. **Self-relative baselines are better than cross-model ones here** — they control for the model's ceiling and answer the question users actually have ("when does *this* companion start forgetting?").
4. **The convergent finding across all four papers** — RULER, NoLiMa, NoCha, Lost in the Middle — is that **claimed context length is near-meaningless** and every honest measurement produces a much smaller effective number. Our platform should report an effective conversational memory length, not a context window.
