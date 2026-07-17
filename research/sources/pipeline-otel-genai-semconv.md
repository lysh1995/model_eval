---
title: "OpenTelemetry GenAI Semantic Conventions (spans, events, metrics, registry)"
url: https://github.com/open-telemetry/semantic-conventions-genai
org: OpenTelemetry / CNCF
year: 2026
type: standard-spec
accessed: 2026-07-16
topic: eval-lifecycle
---

# OpenTelemetry GenAI Semantic Conventions

> **IMPORTANT STATUS NOTE.** The GenAI semconv have **moved out of the main
> `semantic-conventions` repo** into a dedicated repo:
> `open-telemetry/semantic-conventions-genai`. The pages at
> `opentelemetry.io/docs/specs/semconv/gen-ai/*` and
> `.../registry/attributes/gen-ai/` now render a **"moved / no longer maintained"**
> notice, and the mirrored attributes there are marked **deprecated**. Anything
> citing the old opentelemetry.io URL is citing a stale mirror.
>
> **Everything below is transcribed verbatim from the raw markdown of
> `semantic-conventions-genai@main`, fetched 2026-07-16.**
>
> **Stability: nearly every `gen_ai.*` attribute is `Development`** (OTel's
> pre-stable tier) — i.e. it MAY break. `error.type`, `server.address`,
> `server.port` are `Stable`. Do not assume this namespace is frozen.

Source files transcribed:
- `docs/gen-ai/gen-ai-spans.md`
- `docs/gen-ai/gen-ai-events.md`
- `docs/gen-ai/gen-ai-metrics.md`
- `docs/registry/attributes/gen-ai.md`
- `docs/gen-ai/gen-ai-agent-spans.md`, `docs/gen-ai/anthropic.md`

---

## 1. Span naming & kind (verbatim)

```
**Span name** SHOULD be `{gen_ai.operation.name} {gen_ai.request.model}`.
Semantic conventions for individual GenAI systems and frameworks MAY specify
different span name format and MUST follow the overall guidelines for span names.

**Span kind** SHOULD be `CLIENT` and MAY be set to `INTERNAL` on spans representing
calls to ... running in the same process.
```

Other span-name forms in the spec:
- retrieval: `` `{gen_ai.operation.name} {gen_ai.data_source.id}` ``
- memory: `` `{gen_ai.operation.name}` ``
- tool execution: `` `execute_tool {gen_ai.tool.name}` ``

---

## 2. The complete `gen_ai.*` attribute registry

Every attribute name present in `docs/registry/attributes/gen-ai.md` (exhaustive,
sorted, verbatim names):

```
gen_ai.agent.description
gen_ai.agent.id
gen_ai.agent.name
gen_ai.agent.version
gen_ai.conversation.compacted
gen_ai.conversation.id
gen_ai.data_source.id
gen_ai.embeddings.dimension.count
gen_ai.evaluation.explanation
gen_ai.evaluation.name
gen_ai.evaluation.score.label
gen_ai.evaluation.score.value
gen_ai.input.messages
gen_ai.memory.query.text
gen_ai.memory.record.count
gen_ai.memory.record.id
gen_ai.memory.records
gen_ai.memory.store.id
gen_ai.operation.name
gen_ai.output.messages
gen_ai.output.type
gen_ai.prompt.name
gen_ai.prompt.variable
gen_ai.prompt.version
gen_ai.provider.name
gen_ai.request.choice.count
gen_ai.request.encoding_formats
gen_ai.request.frequency_penalty
gen_ai.request.max_tokens
gen_ai.request.model
gen_ai.request.presence_penalty
gen_ai.request.reasoning.level
gen_ai.request.seed
gen_ai.request.stop_sequences
gen_ai.request.stream
gen_ai.request.temperature
gen_ai.request.top_k
gen_ai.request.top_p
gen_ai.response.finish_reasons
gen_ai.response.id
gen_ai.response.model
gen_ai.response.time_to_first_chunk
gen_ai.retrieval.documents
gen_ai.retrieval.query.text
gen_ai.retrieval.top_k
gen_ai.system_instructions
gen_ai.token.type
gen_ai.tool.call.arguments
gen_ai.tool.call.id
gen_ai.tool.call.result
gen_ai.tool.definitions
gen_ai.tool.description
gen_ai.tool.name
gen_ai.tool.type
gen_ai.usage.cache_creation.input_tokens
gen_ai.usage.cache_read.input_tokens
gen_ai.usage.input_tokens
gen_ai.usage.output_tokens
gen_ai.usage.reasoning.output_tokens
gen_ai.workflow.name
```

### Requirement levels on the inference span / details event (verbatim table)

| Key | Requirement Level | Type | Example |
| --- | --- | --- | --- |
| `gen_ai.operation.name` | `Required` | string | `chat`; `generate_content`; `text_completion` |
| `gen_ai.provider.name` | `Required` | string | `openai`; `gcp.gen_ai`; `gcp.vertex_ai` |
| `error.type` | `Conditionally Required` If the operation ended in an error. | string | `timeout`; `500` |
| `gen_ai.conversation.id` | `Conditionally Required` When available. | string | `conv_5j66UpCpwteGg4YSxUnt7lPY` |
| `gen_ai.output.type` | `Conditionally Required` When applicable and if the request includes an output format. | string | `text`; `json`; `image` |
| `gen_ai.prompt.name` | `Conditionally Required` when a named prompt template is used | string | `analyze-code` |
| `gen_ai.prompt.version` | `Conditionally Required` when `gen_ai.prompt.name` is set and a version is available | string | `1.0.0`; `2025-05-01`; `prod`; `v2` |
| `gen_ai.request.choice.count` | `Conditionally Required` If available, in the request, and !=1. | int | `3` |
| `gen_ai.request.model` | `Conditionally Required` If available. | string | `gpt-4` |
| `gen_ai.request.seed` | `Conditionally Required` If applicable and if the request includes a seed. | int | `100` |
| `gen_ai.request.stream` | `Conditionally Required` | boolean | |
| `gen_ai.request.top_k` | `Conditionally Required` If applicable. | int | `40` |
| `server.port` | `Conditionally Required` If `server.address` is set. | int | `443` |
| `gen_ai.conversation.compacted` | `Recommended` when available | boolean | `true` |
| `gen_ai.request.frequency_penalty` | `Recommended` | double | `0.1` |
| `gen_ai.request.max_tokens` | `Recommended` | int | `100` |
| `gen_ai.request.presence_penalty` | `Recommended` | double | `0.1` |
| `gen_ai.request.reasoning.level` | `Recommended` When applicable. | string | `low`; `medium`; `high` |
| `gen_ai.request.stop_sequences` | `Recommended` | string[] | `["forest", "lived"]` |
| `gen_ai.request.temperature` | `Recommended` | double | `0.0` |
| `gen_ai.request.top_p` | `Recommended` | double | `1.0` |
| `gen_ai.response.finish_reasons` | `Recommended` | string[] | `["stop"]`; `["stop", "length"]` |
| `gen_ai.response.id` | `Recommended` | string | `chatcmpl-123` |
| `gen_ai.response.model` | `Recommended` | string | `gpt-4-0613` |
| `gen_ai.response.time_to_first_chunk` | `Recommended` If the request was a streaming request. | double | `0.5`; `1.2` |
| `gen_ai.usage.cache_creation.input_tokens` | `Recommended` | int | `25` |
| `gen_ai.usage.cache_read.input_tokens` | `Recommended` | int | `50` |
| `gen_ai.usage.input_tokens` | `Recommended` | int | `100` |
| `gen_ai.usage.output_tokens` | `Recommended` | int | `180` |
| `gen_ai.usage.reasoning.output_tokens` | `Recommended` When applicable. | int | `50` |
| `server.address` | `Recommended` | string | `example.com` |
| `gen_ai.input.messages` | **`Opt-In`** | any | (structured message array) |
| `gen_ai.output.messages` | **`Opt-In`** | any | (structured message array) |
| `gen_ai.prompt.variable` | **`Opt-In`** | string | `Alice`; `French` |
| `gen_ai.system_instructions` | **`Opt-In`** | any | (structured instruction array) |
| `gen_ai.tool.definitions` | **`Opt-In`** | any | (JSON schema array) |

> **Note the `Opt-In` tier.** The actual conversation content —
> `gen_ai.input.messages`, `gen_ai.output.messages`, `gen_ai.system_instructions`,
> `gen_ai.prompt.variable` — is **Opt-In, i.e. off by default**, explicitly because it
> is user data. A default OTel GenAI instrumentation logs **no text at all**.

---

## 3. `gen_ai.conversation.id` — the session key (verbatim note [4])

```
**[4] `gen_ai.conversation.id`:** Instrumentations SHOULD populate conversation id when
they have an identifier for the conversation readily available for a given operation,
for example:

- when client framework being instrumented manages conversation history
  (see LlamaIndex chat store)
- when instrumenting GenAI client libraries that maintain conversation on the backend side
  (see AWS Bedrock agent sessions, OpenAI Assistant threads)

When no identifier for the conversation is available, instrumentations SHOULD NOT
populate conversation id. For example, a new UUID, a trace identifier, or a hash
of request content SHOULD NOT be used as a fallback value.

Application developers that manage conversation history MAY add conversation id to GenAI and
other spans or logs using custom span or log record processors or hooks provided by
instrumentation libraries.
```

> **Read this carefully — it is the single most important sentence for our design.**
> `gen_ai.conversation.id` is an **opaque application-supplied string with no
> lifecycle, no start/end, no parent, and no attributes of its own.** The spec
> explicitly *forbids* synthesizing one. **There is no session/thread ENTITY in
> OTel GenAI — only a correlation label stamped on independent spans.** OTel gives
> us multi-turn *correlation*, not multi-turn *modeling*.

### `gen_ai.conversation.compacted` (verbatim)

```
| `gen_ai.conversation.compacted` | `Recommended` when available | boolean |
Indicates whether the effective conversation context used for this operation is a
compacted view of a prior conversation. | `true` |
```

> Directly relevant to note 11 §9 (distance-to-anchor): this boolean is the standard's
> only acknowledgement that context got truncated/summarized. It is a boolean, not a
> distance — insufficient for us, but it is the right hook to extend.

---

## 4. Event: `gen_ai.evaluation.result` — VERBATIM, COMPLETE

This is the entire normative definition. (Merged Aug 2025; shipped in semconv v1.39.0.)

```
## Event: `gen_ai.evaluation.result`

**Status:** Development

The event name MUST be `gen_ai.evaluation.result`.

This event captures the result of evaluating GenAI output for quality, accuracy, or
other characteristics. This event SHOULD be parented to GenAI operation span being
evaluated when possible or set `gen_ai.response.id` when span id is not available.

**Requirement level:** Recommended.
```

**Attributes — the complete list. There are six.**

| Key | Stability | Requirement Level | Value Type | Description | Example Values |
| --- | --- | --- | --- | --- | --- |
| `gen_ai.evaluation.name` | Development | `Required` | string | The name of the evaluation metric used for the GenAI response. | `Relevance`; `IntentResolution` |
| `error.type` | Stable | `Conditionally Required` If the operation ended in an error. | string | Describes a class of error the operation ended with. | `timeout`; `500` |
| `gen_ai.evaluation.score.label` | Development | `Conditionally Required` If applicable. | string | Human readable label for evaluation. | `relevant`; `not_relevant`; `correct`; `incorrect`; `pass`; `fail` |
| `gen_ai.evaluation.score.value` | Development | `Conditionally Required` If applicable. | double | The evaluation score returned by the evaluator. | `4.0` |
| `gen_ai.evaluation.explanation` | Development | `Recommended` | string | A free-form explanation for the assigned score provided by the evaluator. | `The response is factually accurate but lacks sufficient detail to fully address the question.` |
| `gen_ai.response.id` | Development | `Recommended` When available. | string | The unique identifier for the completion. | `chatcmpl-123` |

Notes verbatim:

```
**[2] `gen_ai.evaluation.score.label`:** This attribute provides a human-readable
interpretation of the evaluation score produced by an evaluator. For example, a score
value of 1 could mean "relevant" in one evaluation system and "not relevant" in
another, depending on the scoring range and evaluator. The label SHOULD have low
cardinality. Possible values depend on the evaluation metric and evaluator used;
implementations SHOULD document the possible values.

**[3] `gen_ai.response.id`:** The unique identifier assigned to the specific completion
being evaluated. This attribute helps correlate the evaluation event with the
corresponding operation when span id is not available.
```

### ⚠️ The gap that matters most to us

**`gen_ai.evaluation.result` has NO attribute for evaluator identity.** There is no
field for:

- the judge **model** (nothing like `gen_ai.evaluation.model`)
- the **rubric / prompt version** that produced the score
- the judge's **decoding params or seed**
- **who/what** the evaluator was at all (human? LLM? regex?)
- the **sampling inclusion probability** of the evaluated item
- any notion of a **pairwise comparison** — the schema is single-item, single-score

The spec's own note [2] concedes the semantics are evaluator-dependent
(*"a score value of 1 could mean 'relevant' in one evaluation system and 'not relevant'
in another"*) — **and then provides no field to record which evaluator it was.** A
`gen_ai.evaluation.result` event is therefore **not self-describing and not
reproducible**: two events with `name=Relevance, value=4.0` from different judge
versions are indistinguishable on the wire.

This is exactly the `evaluator_id` content-address requirement from note 06 §7, and the
standard does not carry it. **We must extend the event with our own namespace.** The
standard is a good wire format for the *generation* side and an incomplete one for the
*evaluation* side.

Note also: **the score value is a `double`.** Pairwise-comparison outcomes (note 11's
mandated format) do not fit this schema without a private encoding.

---

## 5. Enum values (verbatim)

### `gen_ai.operation.name`

| Value | Description |
| --- | --- |
| `chat` | Chat completion operation such as OpenAI Chat API |
| `create_agent` | Create GenAI agent |
| `create_memory` | Create new memory records |
| `create_memory_store` | Create or initialize a memory store |
| `delete_memory` | Delete memory records |
| `delete_memory_store` | Delete or deprovision a memory store |
| `embeddings` | Embeddings operation such as OpenAI Create embeddings API |
| `execute_tool` | Execute a tool |
| `generate_content` | Multimodal content generation operation such as Gemini Generate Content |
| `invoke_agent` | Invoke GenAI agent |
| `invoke_workflow` | Invoke GenAI workflow |
| `plan` | Agent planning or task decomposition phase |
| `retrieval` | Retrieval operation such as OpenAI Search Vector Store API |
| `search_memory` | Search/query memories from a memory store |
| `text_completion` | Text completions operation such as OpenAI Completions API (Legacy) |
| `update_memory` | Update existing memory records |
| `upsert_memory` | Create or update memory records without the caller choosing which |

### `gen_ai.output.type`
`image` | `json` | `speech` | `text`

### `gen_ai.provider.name`
`anthropic` | `aws.bedrock` | `azure.ai.inference` | `azure.ai.openai` | `cohere` |
`deepseek` | `gcp.gemini` | `gcp.gen_ai` | `gcp.vertex_ai` | `groq` | `ibm.watsonx.ai` |
`mistral_ai` | `moonshot_ai` | `openai` | `perplexity` | `x_ai`

### `gen_ai.token.type`
`input` | `output`

### `gen_ai.request.reasoning.level`
`low` | `medium` | `high`

---

## 6. Metrics (verbatim names)

```
gen_ai.client.operation.duration
gen_ai.client.operation.time_per_output_chunk
gen_ai.client.operation.time_to_first_chunk
gen_ai.client.token.usage
gen_ai.execute_tool.duration
gen_ai.invoke_agent.duration
gen_ai.invoke_agent.inference_calls
gen_ai.invoke_agent.tool_calls
gen_ai.server.request.duration
gen_ai.server.time_per_output_token
gen_ai.server.time_to_first_token
gen_ai.workflow.duration
```

Standard metric dimensions: `gen_ai.operation.name`, `gen_ai.provider.name`,
`gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.token.type`,
`gen_ai.tool.name`, `gen_ai.tool.type`, `gen_ai.agent.name`, `gen_ai.workflow.name`,
`error.type`, `server.address`, `server.port`.

> **There is no evaluation metric.** No `gen_ai.evaluation.*` counter or histogram
> exists. Evaluation is events-only in the standard; aggregation is left entirely to
> the backend. Our per-cell rollups (note 06 §6) are ours to build.

---

## 7. Event: `gen_ai.client.inference.operation.details` (verbatim)

```
The event name MUST be `gen_ai.client.inference.operation.details`.

Describes the details of a GenAI completion request including chat history and
parameters.

This event could be used to store input and output details independently from traces.

**Requirement level:** Opt-In.
```

> The "**store input and output details independently from traces**" line is the hook
> that matters: it is the standard-blessed way to send **full conversation payloads
> down a different pipe than the span**, at a different sampling rate. That is exactly
> the split note 06 §6 needs (metadata-only 200 B rollups vs 3–8 KB full traces).

Message payload shape (verbatim example, `gen_ai.input.messages`):

```json
[
  {"role": "user", "parts": [{"type": "text", "content": "Weather in Paris?"}]},
  {"role": "assistant", "parts": [{"type": "tool_call", "id": "call_VSPygqKTWdrhaFErNvMV18Yl",
     "name": "get_weather", "arguments": {"location": "Paris"}}]},
  {"role": "tool", "parts": [{"type": "tool_call_response",
     "id": "call_VSPygqKTWdrhaFErNvMV18Yl", "response": "rainy, 57°F"}]}
]
```

`gen_ai.output.messages`:

```json
[
  {"role": "assistant",
   "parts": [{"type": "text", "content": "The weather in Paris is currently rainy with a temperature of 57°F."}],
   "finish_reason": "stop"}
]
```

`gen_ai.system_instructions`:

```json
[{"type": "text", "content": "You are a language translator."},
 {"type": "text", "content": "Your mission is to translate text in English to French."}]
```

> **`role` + `parts[]` with a typed `content`** is the canonical shape. Note the
> system prompt is a **separate top-level attribute**, not message[0] — which is
> convenient for us, since *the system prompt is one of the three axes of a variant*.

---

## 8. `gen_ai.provider.name` note (verbatim) — why requested != served

```
The attribute SHOULD be set based on the instrumentation's best knowledge and may
differ from the actual upstream provider. For example, a client SDK may be configured
against a proxy or hosting platform that transparently relays requests to a different
provider.
```

Combined with the spec's separation of `gen_ai.request.model` (`Conditionally Required`
"If available") from `gen_ai.response.model` ("The name of the model that generated the
response"), this is the standard independently arriving at note 06 §7's rule:
**log the model that served, not the model you asked for.**

---

## 9. What we must add on top (nothing in the standard covers these)

| Our need | Standard coverage |
| --- | --- |
| `variant_id` = (model, params, system prompt) as one identity | **none** — scattered across `request.model` + `request.*` + `system_instructions` |
| evaluator identity / rubric content-hash | **none** |
| pairwise comparison outcomes | **none** — score is a scalar `double` |
| inclusion probability `π_i` | **none** |
| session as a first-class entity with lifecycle | **none** — `conversation.id` is a bare label |
| distance-to-anchor / re-anchoring | only `conversation.compacted` (boolean) |
| character_id, language | **none** — would be `gen_ai.prompt.variable.*` at best |
| rollout stage (shadow/canary/live) | **none** |

`gen_ai.prompt.name` + `gen_ai.prompt.version` are the closest the standard comes to a
variant identity, and note [8] says: *"The version string can follow any versioning
scheme chosen by the application (e.g., SemVer, date-based, or platform-specific tags).
When a prompt management system is in use, this SHOULD match the version identifier
used by that system."* — i.e. **a mutable human-assigned label**, exactly what note 06
§7 rules out. We should set `gen_ai.prompt.version` to our **content hash** to satisfy
both.
