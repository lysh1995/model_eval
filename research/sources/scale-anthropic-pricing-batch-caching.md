---
title: "Claude model pricing, Batch API, and prompt caching economics"
url: https://platform.claude.com/docs/en/about-claude/models/overview
org: Anthropic
year: 2026
type: docs
accessed: 2026-07-16
topic: production-scale
---

# Claude model pricing (cached 2026-06-24, via claude-api skill — authoritative)

| Model | Model ID | Context | Input $/1M | Output $/1M |
|---|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | 1M | $10.00 | $50.00 |
| Claude Opus 4.8 | `claude-opus-4-8` | 1M | $5.00 | $25.00 |
| Claude Opus 4.7 | `claude-opus-4-7` | 1M | $5.00 | $25.00 |
| Claude Opus 4.6 | `claude-opus-4-6` | 1M | $5.00 | $25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | $3.00 ($2.00 intro through 2026-08-31) | $15.00 ($10.00 intro) |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M | $3.00 | $15.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

**Relevance to eval platform:** Haiku 4.5 is the cheap-judge tier ($1/$5). Sonnet 5 is
the mid tier ($3/$15). Opus 4.8 is the strong-judge / gold tier ($5/$25). The
Haiku→Opus input price ratio is 5x; output ratio is 5x. This is the core lever for
tiered/cascade judging.

---

## Batch API (Message Batches) — 50% discount

Verbatim from the Anthropic docs (`python/claude-api/batches.md`):

> The Batches API (`POST /v1/messages/batches`) processes Messages API requests
> asynchronously at 50% of standard prices.
>
> ## Key Facts
> - Up to 100,000 requests or 256 MB per batch
> - Most batches complete within 1 hour; maximum 24 hours
> - Results available for 29 days after creation
> - 50% cost reduction on all token usage
> - All Messages API features supported (vision, tools, caching, etc.)

**Effective batch pricing (50% off):**

| Model | Batch Input $/1M | Batch Output $/1M |
|---|---|---|
| Claude Haiku 4.5 | $0.50 | $2.50 |
| Claude Sonnet 5 | $1.50 | $7.50 |
| Claude Opus 4.8 | $2.50 | $12.50 |

**Constraints that matter for a monitoring platform:**
- Batch latency: "Most batches complete within 1 hour; maximum 24 hours." This makes
  batch UNSUITABLE for inline guardrails and marginal for fast regression detection,
  but ideal for the daily/periodic deep-judge tier.
- Results arrive in **any order** — key by `custom_id`, never by position.
- Batch is **not available** on Amazon Bedrock, Vertex AI, or Microsoft Foundry
  (per `shared/platform-availability.md`). Available on first-party Claude API and
  Claude Platform on AWS.
- Batch **rejects** the `fallbacks` parameter and carries no fallback-credit tokens.

Batches support prompt caching — the docs show a "Batch with Prompt Caching" pattern
where a shared `system` block carries `cache_control: {"type": "ephemeral"}` across
all requests in the batch. **This stacks with the 50% batch discount.**

---

## Prompt caching economics

Verbatim from `shared/prompt-caching.md`:

> **Economics:** Cache reads cost ~0.1× base input price. Cache writes cost
> **1.25× for 5-minute TTL, 2× for 1-hour TTL**. Break-even depends on TTL: with
> 5-minute TTL, two requests break even (1.25× + 0.1× = 1.35× vs 2× uncached);
> with 1-hour TTL, you need at least three requests (2× + 0.2× = 2.2× vs 3× uncached).

**Minimum cacheable prefix (model-dependent) — critical gotcha:**

| Model | Minimum |
|---|---:|
| Opus 4.8, Opus 4.7, Opus 4.6, Opus 4.5, Haiku 4.5 | 4096 tokens |
| Fable 5, Sonnet 4.6, Haiku 3.5, Haiku 3 | 2048 tokens |
| Sonnet 4.5, Sonnet 4.1, Sonnet 4, Sonnet 3.7 | 1024 tokens |

> A 3K-token prompt caches on Sonnet 4.5 and Fable 5 but silently won't on Opus 4.8.

**This is directly load-bearing for an LLM-judge rubric.** A judge prompt is a large
stable rubric + a small varying (transcript) suffix — the textbook "shared prefix,
varying suffix" caching pattern. But on **Haiku 4.5 the rubric must exceed 4096
tokens** or the cache silently won't engage (no error — `cache_creation_input_tokens: 0`).

**Placement pattern for a judge (verbatim from the docs):**

> ### Shared prefix, varying suffix
> Many requests share a large fixed preamble (few-shot examples, retrieved docs,
> instructions) but differ in the final question. Put the breakpoint at the end of
> the **shared** portion, not at the end of the whole prompt — otherwise every
> request writes a distinct cache entry and nothing is ever read.

```json
"messages": [{"role": "user", "content": [
  {"type": "text", "text": "<shared context>", "cache_control": {"type": "ephemeral"}},
  {"type": "text", "text": "<varying question>"}  // no marker — differs every time
]}]
```

**Cache invalidation hierarchy (matters for evaluator versioning):**

| Change | Tools cache | System cache | Messages cache |
|---|:---:|:---:|:---:|
| Tool definitions (add/remove/reorder) | ❌ | ❌ | ❌ |
| Model switch | ❌ | ❌ | ❌ |
| System prompt content | ✅ | ❌ | ❌ |
| `tool_choice`, images, `thinking` enable/disable | ✅ | ✅ | ❌ |
| Message content | ✅ | ✅ | ❌ |

Implication for us: **bumping the evaluator prompt version invalidates the judge's
cache** — expect a cold-write spike at every evaluator rollout. Caches are also
**model-scoped**, so a Haiku→Opus escalation cannot share a cache with the Haiku tier.

**Concurrent-request timing (matters for high-QPS judging):**

> A cache entry becomes readable only after the first response **begins streaming**.
> N parallel requests with identical prefixes all pay full price — none can read
> what the others are still writing.
>
> For fan-out patterns: send 1 request, await the first streamed token (not the full
> response), then fire the remaining N−1.

At 50M gen/day with a sampled judge fleet running wide parallelism, a naive fan-out
pays **full input price on every concurrent request**. The mitigation is either the
send-1-then-fan-out pattern, or a **pre-warm** call.

**Pre-warming (`max_tokens: 0`):**

> To eliminate the cache-miss latency on the *first* real request, send a
> **`max_tokens: 0`** request at startup (or on an interval). The API runs prefill —
> writing the cache at your `cache_control` breakpoint — and returns immediately with
> `content: []`, `stop_reason: "max_tokens"`, and a populated `usage` block (zero
> output tokens billed; normal cache-write charge on `cache_creation_input_tokens`).

Docs note pre-warming is NOT needed when traffic is continuous (requests ≤ TTL apart) —
which is our case for a steady judge fleet. A 5-minute TTL stays warm on its own at
any meaningful judge QPS.

**Verifying cache hits:**

| Field | Meaning |
|---|---|
| `cache_creation_input_tokens` | Tokens written to cache (paid ~1.25×) |
| `cache_read_input_tokens` | Tokens served from cache (paid ~0.1×) |
| `input_tokens` | Tokens processed at full price (not cached) |

> Total prompt size = `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`

**Silent cache invalidators to audit in a judge harness** (verbatim list):
- `datetime.now()` / `time.time()` in system prompt → prefix changes every request
- `uuid4()` / request IDs early in content
- `json.dumps(d)` without `sort_keys=True` / iterating a `set` → non-deterministic serialization
- f-string interpolating session/user ID into system prompt
- Conditional system sections (`if flag: system += ...`)
- `tools=build_tools(user)` where the set varies per user

For our judge: **do not interpolate the variant ID, character name, or timestamp into
the rubric prefix.** Put them in the varying suffix after the cache breakpoint.

Max **4** `cache_control` breakpoints per request.

**20-block lookback window:**

> Each breakpoint walks backward **at most 20 content blocks** to find a prior cache
> entry. If a single turn adds more than 20 blocks (common in agentic loops with many
> tool_use/tool_result pairs), the next request's breakpoint won't find the previous
> cache and silently misses.

---

## Token counting — do NOT estimate

Verbatim from `shared/token-counting.md`:

> Use the `count_tokens` endpoint (`POST /v1/messages/count_tokens`) for accurate
> token counts against Claude models. Token counts are **model-specific** — pass
> the same model ID you'll use for inference.
>
> **Do not use `tiktoken`.** It's OpenAI's tokenizer. It undercounts Claude
> tokens by ~15–20% on typical text, and by much more on code or non-English
> input.

**Directly relevant to our brief: the "2 languages" slicing.** If one of our two
languages is non-English, token-count estimates from an OpenAI tokenizer will be
badly wrong, which would corrupt the cost model per-slice. Use `count_tokens` per
model on a representative sample of each language.

**Tokenizer differences across models (from `shared/model-migration.md`):**
- Opus 4.7/4.8 and Fable 5 share a tokenizer.
- Claude Sonnet 5 uses that new tokenizer: **"approximately 30% more tokens than on
  Sonnet 4.6"** for the same input text. Per-token pricing is unchanged, so the cost
  of an equivalent request differs.
- Coming from Opus 4.6/Sonnet/Haiku or older, the Opus 4.7 tokenizer produces roughly
  **1×–1.35×** as many tokens.

**Implication for a tiered judge:** Haiku 4.5 and Opus 4.8 have *different tokenizers*.
A cost model cannot use one token count across tiers — count per model.

---

## Rate limits / throughput

- Rate limits are per-organization: requests per minute (RPM), tokens per minute
  (TPM), tokens per day (TPD).
- Response headers: `retry-after`, `x-ratelimit-limit-*`, `x-ratelimit-remaining-*`.
- SDKs auto-retry 408/409/429/5xx with exponential backoff (default `max_retries=2`).
- Haiku 4.5 has its **own rate-limit pool separate from Haiku 3/3.5**.
- Fast mode (Opus 4.8/4.7, beta `fast-mode-2026-02-01`, `speed: "fast"`) runs the same
  model at **up to 2.5x higher output tokens per second** at premium pricing, and has
  **its own rate limit separate from standard Opus**. Not available with the Batch API.

**Implication:** the eval platform's judge fleet competes for the same org TPM/RPM pool
as production generation traffic unless separated by workspace/key. At 50M gen/day this
is a real capacity-planning constraint, not a footnote — budget the judge tier's TPM
explicitly and consider a separate workspace so a judge backlog cannot throttle prod.

---

## Reproducibility / lineage hooks available in the API

- **`response._request_id`** (Python; `request-id` header) — populated on every response.
  Log it for end-to-end traceability with Anthropic.
- **`response.model`** — names the model that actually produced the message. Do not
  assume it equals the requested model (fallbacks, sticky routing).
- **`response.usage`** — `input_tokens`, `output_tokens`, `cache_creation_input_tokens`,
  `cache_read_input_tokens`. Per-attempt detail in `usage.iterations`.
- **`response.stop_reason`** — `end_turn` | `max_tokens` | `stop_sequence` | `tool_use` |
  `pause_turn` | `refusal`. A judge harness MUST branch on `refusal` and `max_tokens`
  before parsing a score, or it will silently record garbage.
- **Structured outputs** (`output_config.format` with a `json_schema`) guarantee the
  judge returns parseable JSON. Note: "New schemas incur a one-time compilation cost.
  Subsequent requests with the same schema use a **24-hour cache**." And: incompatible
  with citations; if `stop_reason: "max_tokens"` the output may be incomplete.
- **Models API** (`GET /v1/models/{id}`) returns live `max_input_tokens`, `max_tokens`,
  and a `capabilities` tree — usable to pin/verify evaluator model capabilities as part
  of lineage.

**Judge-harness correctness note:** with `output_config.format` set, `max_tokens: 0`
pre-warming is rejected (`invalid_request_error`), as are `stream: true`,
`thinking.type: "enabled"`, forced `tool_choice`, and Batch requests. So a
structured-output judge cannot be cache-pre-warmed via the `max_tokens: 0` trick —
warm it with a real request instead.
