---
title: "MemGPT: Towards LLMs as Operating Systems"
url: https://arxiv.org/abs/2310.08560
authors: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez (UC Berkeley)
year: 2023
type: paper
accessed: 2026-07-16
topic: multi-turn-eval
---

# MemGPT — memory architecture + how it's evaluated

Submitted 2023-10-12; revised 2024-02-12. Full text read from https://ar5iv.labs.arxiv.org/html/2310.08560
(Later renamed/productized as **Letta**.)

**This is the ONLY paper in this cluster that evaluates memory over a CONVERSATION rather than a document — (c) in the brief.**

## Architecture — OS-inspired virtual context management

Core analogy (VERBATIM framing): **"virtual context management, a technique drawing inspiration from hierarchical memory systems in traditional operating systems."** The LLM context window is treated as **physical RAM**; external storage is **disk**; MemGPT is the **OS kernel** paging between them. The LLM itself issues the paging calls.

### Main context (= RAM, what's actually in the context window)
1. **System instructions** — read-only. Describes the memory hierarchy and available functions to the LLM.
2. **Working context** — read/write **unstructured text**. The agent's curated scratchpad of key facts (e.g. persona, user facts). **Self-edited by the LLM via function calls.**
3. **FIFO queue** — rolling message history, plus **recursive summaries** of what's been evicted.

### External context (= disk, outside the context window)
4. **Recall storage** — full message database (raw conversation log, searchable).
5. **Archival storage** — read/write long-text objects, arbitrary size.

### Control flow
- The LLM manages its own memory via **function calls** — it decides when to retrieve or evict data. Memory management is *learned behavior expressed as tool use*, not a fixed heuristic.
- **Queue manager** handles overflow:
  - **Memory pressure warning at 70% capacity** — a signal is inserted into context so the agent knows to start saving things.
  - **Forced eviction at 100%** — evicted messages get **recursive summarization**.
- **Interrupts** manage control flow between the agent and the user (yield vs. continue).

**Key design insight for us:** the distinction between *working context* (a small curated set of facts the agent actively maintains) and *recall storage* (the raw log) is exactly the distinction a companion needs. The raw conversation log is the wrong thing to stuff in context — see Lost in the Middle's below-closed-book result. The curated working context sits at a **privileged position** in the window (near the top, with the system prompt) — which is, per Lost in the Middle, exactly where **primacy** makes retrieval most reliable. **The architecture is implicitly a mitigation for the U-shaped curve: promote important facts out of the sagging middle and into the primacy zone.** The paper does not frame it this way, but that is what it is doing.

## Evaluation 1 — Deep Memory Retrieval (DMR) — THE KEY EVAL

**Setup:** Built on the **Multi-Session Chat (MSC)** dataset (Xu et al. 2021) — multi-session human conversations with persistent personas. The agent is asked a question whose answer requires recalling a fact from a **prior conversation session**. Tests consistency/recall across sessions.

This is the closest thing in the literature to **actual conversational memory evaluation**. Metrics: **accuracy** (does it recall the right fact) and **ROUGE-L** (overlap with the gold answer).

| Model | Accuracy | ROUGE-L |
|---|---|---|
| GPT-3.5 Turbo | 38.7% | 0.394 |
| **GPT-3.5 Turbo + MemGPT** | **66.9%** | **0.629** |
| GPT-4 | 32.1% | 0.296 |
| **GPT-4 + MemGPT** | **92.5%** | **0.814** |
| GPT-4 Turbo | 35.3% | 0.359 |
| **GPT-4 Turbo + MemGPT** | **93.4%** | **0.827** |

**Read these numbers carefully — several things are remarkable:**

1. **Baselines are terrible: 32.1–38.7%.** Off-the-shelf frontier models, given a conversation history, recall a prior-session fact **about a third of the time.** Conversational memory is *badly* unsolved at the base-model level.

2. **GPT-4 (32.1%) scores LOWER than GPT-3.5 Turbo (38.7%)** on the baseline. The *stronger* model is *worse* at conversational recall. The paper attributes this to GPT-4 being more conservative/refusing to answer when unsure, but whatever the cause: **raw model capability does not predict conversational memory.** You cannot infer memory performance from general benchmark strength. **This is a direct argument for a dedicated memory eval — no existing general benchmark would have surfaced this inversion.**

3. **MemGPT roughly triples GPT-4's accuracy (32.1% → 92.5%).** Architecture matters enormously — far more than base-model choice. The gap between architectures (32.1→92.5, +60.4 points) dwarfs the gap between models (38.7 vs 32.1, 6.6 points).

4. **Note the metric caveat:** ROUGE-L is n-gram overlap. It rewards surface lexical match with the gold answer, not truth. A response can score well by parroting phrasing while getting the fact wrong, or score poorly by paraphrasing correctly. Given NoCha's finding that ~20% of *correct-labeled* explanations are confabulated, **ROUGE-L on a memory task is a weak proxy** and these numbers should be treated as optimistic. Worth flagging if we adopt this eval.

## Evaluation 2 — Conversation Opener (engagement, not recall)

**Setup:** the agent must produce an engaging opening message drawing on its stored persona knowledge. Scored by **CSIM** similarity against a **human baseline (1.000)**.

| Model | SIM-1 | SIM-3 | SIM-H |
|---|---|---|---|
| GPT-3.5 Turbo | 0.830 | 0.812 | 0.817 |
| GPT-4 | 0.868 | 0.843 | 0.773 |
| GPT-4 Turbo | 0.857 | 0.828 | 0.767 |

MemGPT occasionally **exceeded human performance**, which the paper attributes to being **"more verbose"** — covering more of the persona.

**This is a cautionary tale for companion eval and worth dwelling on.** The metric rewards *persona coverage*, so a model that mechanically enumerates every stored fact ("I know you like hiking, jazz, and your cat Mia!") beats a human who mentions one thing naturally. **Superhuman on the metric, worse as a companion.** This is Goodhart in miniature, and it is a *directly relevant* trap for us — verbosity/fact-dumping is a plausible degenerate strategy for any companion memory metric we build. **Any recall metric we design must penalize unnatural fact-dumping**, or we will optimize toward an agent that recites a dossier at the user. Note this is the *same* underlying failure as sycophancy: the metric rewards a surface behavior that correlates with the target on average but diverges under optimization.

## Evaluation 3 — Document QA

Fixed-context baselines **plateau near the retriever's limit**; MemGPT maintains **consistent accuracy regardless of document count** via iterative retrieval (paging). GPT-3.5 showed **"significantly degraded performance."**

Honest limitation acknowledged in the paper: **"MemGPT will often stop paging"** prematurely — the agent terminates its own search too early. Self-directed retrieval is not reliably exhaustive; the agent doesn't know what it doesn't know.

## Evaluation 4 — Nested Key-Value Retrieval (multi-hop synthetic)

Values may themselves be keys, requiring 0–4 levels of nested lookup.

- **GPT-3.5: 0% accuracy at 1+ nesting levels.**
- **GPT-4: 0% accuracy at 3+ nesting levels.**
- **MemGPT + GPT-4: unaffected across all nesting levels.**

**Direct NIAH critique embedded here.** Flat key-value retrieval is the classic needle test and models do fine. Add **one hop** and GPT-3.5 goes to **absolute zero**. GPT-4 survives two hops and hits zero at three. The needle test is a *single-hop special case* — the easiest possible point in the task space — and performance falls off a cliff the moment you leave it. Converges with RULER's Variable Tracking motivation and with NoCha's evidence-scope gradient (59.8 → 47.6 → 41.6): **the more distributed the evidence, the worse models get, and NIAH sits at the maximally-concentrated extreme.**

## Relevance to companion / conversational memory eval

1. **DMR on MSC is the closest existing analogue to what we need** — recall a fact from a *prior session* of an ongoing relationship. If we adopt one existing eval as a starting point, this is it. **MSC (Xu et al. 2021) is the dataset to look at next.**
2. **The 32.1–38.7% baselines are the strongest single argument that our platform is measuring something real and unsolved.** Frontier models fail conversational recall ~2/3 of the time without a memory architecture.
3. **GPT-4 < GPT-3.5 on baseline DMR** = conversational memory is orthogonal to general capability. Justifies a dedicated benchmark; no general leaderboard would surface this.
4. **The architecture is the intervention, not the model.** +60.4 points from MemGPT vs 6.6 points between base models. If our platform evaluates *companion products*, it is mostly evaluating their memory architecture.
5. **Both cautionary metric findings are ours to inherit:** the conversation-opener verbosity artifact (Goodhart on coverage) and ROUGE-L's insensitivity to truth. Design against both.
6. **CAVEATS on MemGPT as evidence:**
   - The evaluation is **by the authors, of their own system** — no independent replication captured here.
   - **MSC sessions are short** relative to a real companion relationship (months, thousands of turns). 92.5% on MSC does not mean 92.5% at month six.
   - **DMR probes retrieval of a static fact.** It does **not** test facts that **change** (user's job changed, preference reversed), which is arguably the central hard case for a companion and where naive retrieval architectures should fail worst — retrieval by similarity will surface *both* the old and new fact with no signal about which supersedes. **Nothing in this cluster evaluates superseded facts. That is the clearest open gap and the most defensible contribution available to us.**
