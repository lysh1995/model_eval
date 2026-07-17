---
title: "OpenInference Semantic Conventions"
url: https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md
org: Arize AI
year: 2026
type: spec
accessed: 2026-07-16
topic: eval-lifecycle
---

# OpenInference Semantic Conventions

The de-facto alternative to OTel GenAI semconv, used by Arize Phoenix / Arize AX.
Compatible with OpenTelemetry (it is an attribute schema layered on OTel spans), but
**it is a different namespace and not wire-compatible with `gen_ai.*`.**

## Span kinds — `openinference.span.kind` (REQUIRED on every span)

Ten kinds:

```
LLM         - Large Language Model calls
EMBEDDING   - Embedding service calls
CHAIN       - Application workflow connectors
RETRIEVER   - Data retrieval operations
RERANKER    - Document relevance reordering
TOOL        - External tool/function invocations
AGENT       - LLM-guided reasoning with tools
GUARDRAIL   - Safety filtering components
EVALUATOR   - Output assessment functions
PROMPT      - Template rendering operations
```

> **Two of these do not exist in OTel GenAI at all: `GUARDRAIL` and `EVALUATOR`.**
> OpenInference treats the guardrail and the evaluator as **first-class spans in the same
> trace as the generation they judge.** OTel GenAI models evaluation as a detached
> *event*, and has no guardrail concept whatsoever.
>
> This is the single most useful idea in OpenInference for us: our Tier 0 guardrail and
> Tier 2 judge are *spans*, with their own latency, cost, model, and error semantics —
> exactly the things we need to monitor about them (note 06: guardrail latency budget,
> judge abstention rate). An OTel `gen_ai.evaluation.result` event has no duration and no
> token usage, so **you cannot monitor your judge's own cost/latency in the OTel model.**

## Attribute namespaces

**LLM:** `llm.model_name`, `llm.system`, `llm.provider`, `llm.invocation_parameters`,
`llm.input_messages`, `llm.output_messages`, `llm.prompts`, `llm.choices`,
`llm.finish_reason`, `llm.function_call`, `llm.token_count.*`, `llm.cost.*`, `llm.tools`,
`llm.prompt_template.*`

**Message:** `message.role`, `message.content`, `message.contents`,
`message.function_call_name`, `message.function_call_arguments_json`,
`message.tool_calls`, `message.tool_call_id`, `message.name`, `message_content.type`,
`message_content.text`, `message_content.image`, `message_content.id`,
`message_content.signature`, `message_content.data`, `message_content.encrypted_content`

**Document:** `document.id`, `document.content`, `document.score`, `document.metadata`

**Embedding:** `embedding.model_name`, `embedding.text`, `embedding.vector`,
`embedding.embeddings`, `embedding.invocation_parameters`

**Retrieval/rerank:** `retrieval.documents`, `reranker.input_documents`,
`reranker.output_documents`, `reranker.query`, `reranker.top_k`, `reranker.model_name`

**Tool:** `tool.name`, `tool.description`, `tool.json_schema`, `tool.parameters`,
`tool.id`, `tool_call.id`, `tool_call.function.name`, `tool_call.function.arguments`,
`tool_call.reasoning_signature`

**I/O:** `input.value`, `input.mime_type`, `output.value`, `output.mime_type`

**Context (the important ones for us):** `user.id`, `session.id`, `metadata`,
`tag.tags`, `agent.name`, `prompt.vendor`, `prompt.id`, `prompt.url`

**Media:** `image.url`, `audio.url`, `audio.mime_type`, `audio.transcript`

**Exception:** `exception.type`, `exception.message`, `exception.stacktrace`,
`exception.escaped`

**Graph:** `graph.node.id`, `graph.node.name`, `graph.node.parent_id`

## Flattened list indexing convention

Lists use zero-based indices in flattened attribute names: `<prefix>.<index>.<suffix>`.

```
llm.input_messages.0.message.role
llm.input_messages.0.message.content
llm.output_messages.0.message.tool_calls.0.tool_call.id
llm.input_messages.0.message.contents.0.message_content.type
llm.prompts.0.prompt.text
llm.choices.0.completion.text
llm.tools.0.tool.json_schema
embedding.embeddings.0.embedding.vector
retrieval.documents.0.document.id
reranker.input_documents.0.document.score
```

> **This flattening exists because OTel span attributes were historically scalar-only.**
> OTel GenAI went the other way and made `gen_ai.input.messages` a single `any`-typed
> structured value. **The two specs made opposite choices on the same problem.**
>
> Consequence for us: OpenInference's flattening produces **unbounded attribute-name
> cardinality** (a 100-turn roleplay session = `llm.input_messages.0..99.*`), which is
> exactly the cardinality hazard note 06 §6 warns about — except here it's in the *column
> namespace*, not the GROUP BY. For a 102-turn corpus this is a real argument against
> OpenInference as our storage schema.

## `session.id` vs `gen_ai.conversation.id`

OpenInference uses a generic `session.id` (plus `user.id`) as a **context attribute**
propagated onto spans. Same structural weakness as OTel: a bare correlation label, no
session entity, no lifecycle. Neither spec models a session as a thing with a start, an
end, or attributes of its own.

## Verdict for our platform

| | OTel GenAI | OpenInference |
|---|---|---|
| Governance | CNCF standard | single vendor (Arize) |
| Guardrail span | ✗ | ✓ `GUARDRAIL` |
| Evaluator span | ✗ (detached event) | ✓ `EVALUATOR` |
| Message encoding | structured `any` | flattened indices (cardinality risk) |
| Evaluator identity | ✗ | ✗ (also missing) |
| Session entity | ✗ (`conversation.id` label) | ✗ (`session.id` label) |

**Neither carries evaluator identity. Neither models a session.** Both gaps are ours to
fill regardless of which we adopt.
