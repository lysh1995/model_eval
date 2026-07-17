---
title: "Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
url: https://arxiv.org/abs/2501.13956
authors: Preston Rasmussen, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, Daniel Chalef (Zep AI)
year: 2025
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Zep / Graphiti — Temporal Knowledge Graph for Agent Memory

**Status: this is the closest existing implementation of the world-state record we want to build, including automatic contradiction detection. It is also a cautionary tale: it publishes no error rate for the step we care about most.**

Full text: https://arxiv.org/html/2501.13956v1. Engine is open-source as **Graphiti**. Note: this is a **vendor paper** — Zep AI is a commercial memory product and every number is self-reported against baselines they chose. Read accordingly.

## Architecture — three-tier subgraph

| Tier | Contents |
|---|---|
| **Episode subgraph 𝒢ₑ** | "episodic nodes contain raw input data in messages, text, or JSON"; "serve as non-lossy data store" |
| **Semantic entity subgraph 𝒢ₛ** | extracted + resolved entities and the semantic edges (facts) between them |
| **Community subgraph 𝒢ₓ** | "community nodes represent clusters of strongly connected entities" |

**The non-lossy episode tier is a design idea worth stealing**: the raw text is retained and every extracted fact points back at the episode it came from. That gives provenance — a contradiction flag can always be traced to two specific turns and shown to a human. Without it, an auditor's output is unfalsifiable.

## Extraction

- Processes "the current message content and the last **n** messages" (**n=4**) for context.
- Speaker extraction automatic; then a "**reflection** technique inspired by reflexion to minimize hallucinations."
- Entity resolution = dual search: "embedding each entity name into a **1024-dimensional** vector space" + "full-text search on existing entity names and summaries."
- "the same fact can be extracted multiple times between different entities, enabling Graphiti to model complex multi-entity facts through **hyper-edges**."
- Edge dedup: "hybrid search for relevant edges constrained to edges existing between the same entity pairs."

## ⭐ The temporal model — bi-temporal, and this is the part that matters

Two timelines:
- **T (event timeline)** — "chronological ordering of events"
- **T' (transaction timeline)** — "transactional order of data ingestion"

Four timestamps per edge:
- **t'_created, t'_expired ∈ T'** — "when facts are created or invalidated in the system"
- **t_valid, t_invalid ∈ T** — "temporal range during which facts held true"

**The invalidation mechanism, verbatim:**

> "The system employs an **LLM to compare new edges against semantically related existing edges to identify potential contradictions**. When system identifies temporally overlapping contradictions, it invalidates affected edges by setting their t_invalid to the t_valid of the invalidating edge."

> "Graphiti consistently **prioritizes new information** when determining edge invalidation."

⇒ **This is exactly the contradiction auditor sketched in note 13, already built.** Two consequences:
1. **Good news:** the design is validated as buildable, and the bi-temporal separation is the right answer to note 08's "superseded facts" gap — you never delete, you close a validity interval. A superseded fact and a contradicted fact are the *same data structure*, distinguished only by whether the user sanctioned the change.
2. **⚠️ Bad news:** the contradiction check is *itself an LLM call*. It inherits LLM error rates, and Zep **never measures it**. "Prioritize new information" is a *policy*, not a detector — it is exactly the wrong default for our use case, where the model contradicting itself should be flagged as an *error*, not silently accepted as an update.

## Results

### DMR (Deep Memory Retrieval, from MemGPT)

| Memory | Model | Score |
|---|---|---|
| Recursive Summarization | gpt-4-turbo | 35.3% |
| Conversation Summaries | gpt-4-turbo | 78.6% |
| MemGPT | gpt-4-turbo | 93.4% |
| Full-conversation | gpt-4-turbo | 94.4% |
| **Zep** | gpt-4-turbo | **94.8%** |
| Conversation Summaries | gpt-4o-mini | 88.0% |
| Full-conversation | gpt-4o-mini | 98.0% |
| **Zep** | gpt-4o-mini | **98.2%** |

⚠️ **Zep beats full-conversation by 0.4pp and 0.2pp.** With no CI and no n stated, these are noise. Zep's own critique of DMR is the honest part: "Each conversation contains only **60 messages**, easily fitting within current LLM context windows"; "The evaluation relies exclusively on **single-turn, fact-retrieval questions** that fail to assess complex memory understanding"; "Many questions contain **ambiguous phrasing**." **DMR is a dead benchmark and Zep says so while still reporting it.**

### LongMemEval

| Memory | Model | Score | Latency | Latency IQR | Avg Context Tokens |
|---|---|---|---|---|---|
| Full-context | gpt-4o-mini | 55.4% | 31.3 s | 8.76 s | 115k |
| **Zep** | gpt-4o-mini | **63.8%** | **3.20 s** | 1.31 s | **1.6k** |
| Full-context | gpt-4o | 60.2% | 28.9 s | 6.01 s | 115k |
| **Zep** | gpt-4o | **71.2%** | **2.58 s** | 0.684 s | **1.6k** |

> "Zep achieved accuracy improvements of up to 18.5% while reducing response latency by 90%."

**The 115k → 1.6k token reduction is the real result** — a 72× context reduction with an accuracy *gain*. For us that is a cost argument: a maintained state record is cheaper to audit against than the raw transcript, and our 100-turn dialogues are exactly the regime where this bites.

### Per-question-type (the interesting table)

**gpt-4o** (full-context → Zep):

| Type | Full-context | Zep | Δ |
|---|---|---|---|
| Single-session-preference | 20.0% | 56.7% | **+184%** |
| Single-session-assistant | 94.6% | 80.4% | **−17.7%** |
| Temporal-reasoning | 45.1% | 62.4% | +38.4% |
| Multi-session | 44.3% | 57.9% | +30.7% |
| **Knowledge-update** | 78.2% | 83.3% | +6.52% |
| Single-session-user | 81.4% | 92.9% | +14.1% |

**gpt-4o-mini** (full-context → Zep):

| Type | Full-context | Zep | Δ |
|---|---|---|---|
| Single-session-preference | 30.0% | 53.3% | +77.7% |
| Single-session-assistant | 81.8% | 75.0% | **−9.06%** |
| Temporal-reasoning | 36.5% | 54.1% | +48.2% |
| Multi-session | 40.6% | 47.4% | +16.7% |
| **Knowledge-update** | 76.9% | 74.4% | **−3.36%** |
| Single-session-user | 81.4% | 92.9% | +14.1% |

⭐ **Read the losses, not the wins.** The KG **hurts** single-session-assistant on both models (−17.7%, −9.06%) and **hurts knowledge-update on the weaker model** (−3.36%). Extraction is lossy: turning prose into triples throws away exactly the things that don't fit a triple. The one category where a state record should obviously dominate — knowledge-update, i.e. superseded facts — shows **+6.5% / −3.4%**, i.e. *nothing*. **The structured record does not reliably beat raw context on the very task it was designed for.** That is the most important number in this paper for us and it is buried.

## Stated limitations

> "The decrease in performance for single-session-assistant questions—17.7% for gpt-4o and 9.06% for gpt-4o-mini—represents a notable exception to Zep's otherwise consistent improvements, and suggest further research and engineering work is needed."

> "additional development may be needed to improve less capable models' understanding of Zep's temporal data"

> "No existing benchmarks adequately assess Zep's capability to process and synthesize conversation history with structured business data"

**No error rate is reported for entity extraction, edge extraction, or edge invalidation.** The pipeline is evaluated only end-to-end on downstream QA. So: how often does the LLM contradiction-checker fire falsely? **Unknown, and unknowable from this paper.** Anyone building this must measure it themselves.

## Relevance to companion-eval-platform

1. **⭐ Adopt the bi-temporal edge model wholesale.** t_valid/t_invalid on the event timeline + t'_created/t'_expired on the ingestion timeline is the correct data structure for our world-state record, and it dissolves the superseded-fact problem: a fact that stops being true is an edge whose validity interval closed, not a deletion.
2. **⭐ Invert their policy.** Zep "prioritizes new information" — it treats every contradiction as an update. **We want the opposite**: a contradiction is a *finding* unless the user licensed the change. The distinction between "retcon" (error) and "revision" (correct behavior) is *who introduced the change* — and that is mechanically checkable from turn attribution, since we know which turns are the user's. This is the crux of our whole design and Zep hands us the mechanism while making the wrong choice with it.
3. **Steal the episode tier for provenance.** Every flag must cite two turn indices or it cannot be adjudicated.
4. **Their unmeasured step is our entire product.** Zep gets to skip measuring extraction/invalidation accuracy because it's judged on downstream QA. We can't — the flag *is* the output. **The error rate of the auditor is the deliverable, not an implementation detail.**
5. **n=4 message window for extraction is a red flag for us.** Roleplay facts are established across arcs, not adjacent turns. Their window is tuned for assistant chat.
6. **The −17.7% loss is the honest warning against KG-only auditing.** Run the auditor against the record *and* keep the raw transcript; do not let extraction be the only path to a flag.
