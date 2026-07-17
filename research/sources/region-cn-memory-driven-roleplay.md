---
title: "Memory-Driven Role-Playing: Evaluation and Enhancement of Persona Knowledge Utilization in LLMs (MREval / MRPrompt / MRBench)"
url: https://arxiv.org/abs/2603.19313
authors: Kai Wang, Haoyang You, Zhongjie Wang (Harbin Institute of Technology, China); Yang Zhang (Macquarie University, Australia)
year: 2026
type: paper
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# Memory-Driven Role-Playing (MREval / MRBench)

Findings of ACL 2026. Chinese-led (Harbin Institute of Technology) with an Australian
co-author. **Bilingual Chinese/English benchmark** — relevant as a case of Chinese
groups building zh/en-parallel roleplay evaluation rather than zh-only.

ACL Anthology: https://aclanthology.org/2026.findings-acl.1175/
arXiv: https://arxiv.org/abs/2603.19313 · HTML: https://arxiv.org/html/2603.19313v1

## Core framing

Treats persona knowledge as the LLM's **internal memory store**, to be retrieved and
applied from dialogue context alone. Explicitly inspired by **Stanislavski's "emotional
memory"** acting theory — note this is a *Western* theatrical framework, so despite the
Chinese authorship the theoretical grounding is not Chinese-specific.

## MREval — four memory-driven abilities (exact names, verified from paper §3.2 / Table 1)

| Ability | Definition (quoted from paper) |
|---|---|
| **Memory-Anchoring (MA)** | "ability to anchor its behavior to the designated persona" |
| **Memory-Selecting (MS)** | "ability to extract cues from the STM dialogue context and retrieve relevant persona facets" |
| **Memory-Bounding (MB)** | "ability to adhere to the temporal and epistemic boundaries in persona knowledge" |
| **Memory-Enacting (ME)** | "ability to transform the selected and bounded persona knowledge into a coherent, natural utterance" |

⚠️ **Naming trap:** secondary sources (and one search summary) render the second ability
as **"Recalling"**. The paper says **Selecting**. I verified this against the HTML full
text. Use *Selecting*.

**Memory-Bounding is the interesting one for us.** It scores adherence to **temporal and
epistemic boundaries** — i.e. the character must not know things it *couldn't* know
(events after its timeline; facts outside its epistemic access). This decomposes what
most benchmarks lump into "hallucination" into a *character-relative knowledge boundary*
property. Related to but more general than TimeChara (see `rp-bench-timechara.md`).

## MRBench composition (verified)

- Characters derived from **10 English and 6 Chinese novels**
- **200 English + 200 Chinese instances per ability family**
- **Single-turn dialogues only**
- Total dialogue count: not specified in the text

## Models evaluated (12 total)

- **Open-source (7):** Llama-3-8B, Llama-3.2-3B, Qwen3-0.6B, Qwen3-4B, Qwen3-8B,
  GLM-4-9B-Chat, InternLM2.5-7B
- **Closed-source (5):** GPT-5.2, GLM-4.7, DeepSeek-Chat, Qwen3-Max, Doubao-Seed-1.6

Note the heavy Chinese-model representation (Qwen, GLM, DeepSeek, InternLM, Doubao) —
useful for us, since Anglophone benchmarks under-cover exactly these models.

## Results — only what I actually read

**Verified quote from the paper:** "Qwen3-8B equipped with MRPrompt achieves **8.12**,
surpassing GLM-4.7 (**8.11**) and Qwen3-Max (**8.08**)".

That is the **only** numeric result I extracted. I did **not** read the full results
table. **Do not add further numbers to this file without reading the paper directly.**
The scale appears to be out of 10 but I did **not** confirm this — **UNVERIFIED**.

## ⚠️ Important caveat — this is NOT a long-conversation drift benchmark

The title and framing suggest memory/长对话 evaluation, but the authors **explicitly list
as a limitation** that this is an *"episodic, single-turn setting"* with *"no
within-session memory update"*, and state it *"has not yet addressed interactive
scenarios where persona memory is gradually accumulated...over time."*

**So: despite appearances, this does not answer the 长对话 persona-drift question.** It
measures whether a model can *use* persona knowledge correctly in a single turn, not
whether it *retains* persona across a long session.

### Gap finding (this is the takeaway)

I searched specifically for Chinese work on **长对话 persona drift** and **记忆 eval**
and did **not find a dedicated Chinese benchmark** for it. What exists:

- Chinese *product/practitioner* discourse treats 记忆能力 (memory ability) as a headline
  companion-quality dimension (see `region-cn-companion-product-landscape.md`) and openly
  says 记忆存储能力欠缺 ("memory storage ability is lacking") is the main product failure.
- Chinese *architecture* discourse splits 短期记忆 (short-term memory — a dynamic cache of
  the current conversation) vs 长期记忆 (long-term memory — session summaries encoded as
  vectors). **UNVERIFIED** — this came from a search-level summary, not a primary source
  I fetched.
- But the *benchmark* work (this paper) is explicitly single-turn.

**The Chinese long-conversation persona-drift eval gap mirrors the Anglophone one.** Our
existing `multiturn-persona-drift.md` and `multiturn-time-to-inconsistency-survival.md`
are not being duplicated by Chinese work. This is a genuine open area, not a
we-missed-it area.

## Sources

- https://arxiv.org/html/2603.19313v1 (full text, used for verification)
- https://aclanthology.org/2026.findings-acl.1175/
