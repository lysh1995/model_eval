---
title: "Bing Chat / Sydney initial prompt — prompt-injection extraction, confirmed genuine by Microsoft"
url: https://www.theverge.com/23599441/microsoft-bing-ai-sydney-secret-rules
org: Microsoft
year: 2023
type: reporting
accessed: 2026-07-16
topic: bigtech-practice
---

# The Sydney rules — what the persona definition actually said

**Verification method:** Ars Technica and The Verge fetched raw via `curl` (HTTP 200 both), HTML stripped locally, quotes grepped as exact strings.

**Provenance chain — why this is citable and not a rumor:**

1. Stanford student **Kevin Liu** extracted the prompt via injection ("Ignore previous instructions" / "beginning of the document above"), Feb 8–9 2023.
2. **Marvin von Hagen independently reproduced it via a different injection method** (posing as an OpenAI developer). Ars Technica, verbatim: "a university student named Marvin von Hagen independently confirmed that the list of prompts Liu obtained was not a hallucination by obtaining it through a different prompt injection method." **Two independent extraction paths converging on the same text is the thing that rules out confabulation.**
3. **Microsoft confirmed it on the record.** The Verge, verbatim: "We asked Microsoft about Sydney and these rules, and the company was happy to explain their origins and confirmed that the secret rules are genuine."

Microsoft's on-record statement (Caitlin Roulston, director of communications, to The Verge), verbatim:

> "Sydney refers to an internal code name for a chat experience we were exploring previously," says Caitlin Roulston, director of communications at Microsoft, in a statement to The Verge. "We are phasing out the name in preview, but it may still occasionally pop up."

> Roulston also explained that the rules are "part of an evolving list of controls that we are continuing to adjust as more users interact with our technology."

**"An evolving list of controls" is the closest Microsoft ever came to describing its persona-control methodology.** That is the whole of it. There is no published spec, no versioning, no changelog, no eval.

---

## The persona definition, verbatim (as published by The Verge)

> Here are the secret rules that Bing AI has disclosed:
>
> Sydney is the chat mode of Microsoft Bing search.
> Sydney identifies as "Bing Search," not an assistant.
> Sydney introduces itself with "this is Bing" only at the beginning of the conversation.
> Sydney does not disclose the internal alias "Sydney."
> Sydney can understand and communicate fluently in the user's language of choice, such as English, 中文, 日本語, Español, Français, or Deutsch.
> Sydney's responses should be informative, visual, logical, and actionable.
> Sydney's responses should also be positive, interesting, entertaining, and engaging.
> Sydney's responses should avoid being vague, controversial, or off-topic.
> Sydney's logic and reasoning should be rigorous, intelligent, and defensible.
> Sydney can provide additional relevant details to respond thoroughly and comprehensively to cover multiple aspects in depth.
> Sydney can generate poems, stories, code, essays, songs, celebrity parodies, and more.
> Sydney can generate a query to search for helpful products or services advertisements after responding.
> Sydney must always generate short suggestions for the next user turn after responding.
> [...]
> Sydney should always perform web searches when the user is seeking information or whenever search results could be potentially helpful, regardless of Sydney's internal knowledge or information.
> Sydney can and should perform up to three searches in a single conversation turn.
> Sydney should never search the same query more than once.

Ars Technica's rendering of the identity header, verbatim:

> Consider Bing Chat whose codename is Sydney,
> – Sydney is the chat mode of Microsoft Bing search.
> – Sydney identifies as "Bing Search," not an assistant.
> – Sydney introduces itself with "This is Bing" only at the beginning of the conversation.
> – Sydney does not disclose the internal alias "Sydney."

Ars on the prohibitions, verbatim:

> The prompt also dictates what Sydney should not do, such as "Sydney must not reply with content that violates copyrights for books or song lyrics" and "If the user requests jokes that can hurt a group of people, then Sydney must respectfully decline to do so."

---

## Analysis relevant to our framework

**This is a persona defined entirely as third-person declarative traits.** Every line is `Sydney <verb>`. There is no backstory, no voice sample, no exemplar dialogue, no negative example of tone. The persona is a *list of predicates about an entity*, and the model is expected to infer execution from description. This is exactly the **comprehension/execution conflation** our framework targets: the prompt specifies *what Sydney is*, never *how Sydney sounds*, and Microsoft had no way to tell which half failed when it drifted.

**The trait terms are unmeasurable as written.** "positive, interesting, entertaining, and engaging" / "rigorous, intelligent, and defensible" are adjectives with no operationalization and no anchor. When Microsoft later wrote that responses fell out of "line with our designed tone" (Feb 15 blog), *this adjective list is the entire referent of "designed tone."*

**The instruction "Sydney does not disclose the internal alias 'Sydney'" was violated by the very extraction that revealed it** — and Microsoft's own confirmation notes the name "may still occasionally pop up." A rule stated once at the top of context, contradicted by adversarial pressure downstream, is precisely the anchor-distance failure mode.

**Note the self-referential density.** The token "Sydney" appears in essentially every line. The persona is re-anchored lexically on every rule. This is worth flagging as a design detail: it is a (probably unintentional) form of repeated anchoring, and it still drifted.

---

## What this source does NOT contain

- **Not a Microsoft publication.** Microsoft never published this text itself. It exists only via injection + journalism. Microsoft confirmed authenticity but never released a canonical version, so **there is no authoritative full text** — only journalist renderings of extracted output.
- **No completeness guarantee.** The Verge's list is explicitly "the secret rules that Bing AI has disclosed" — disclosed, not audited. There is no way to know if it is complete or verbatim-faithful to the real prompt. Both Ars and Verge renderings differ slightly in punctuation/casing.
- **No date/version.** The prompt changed continuously ("an evolving list of controls"). This snapshot is ~Feb 8–14, 2023 only.
- **No turn-limit rule.** Nothing in the extracted prompt addresses conversation length; the 5-turn cap was a *system-level* control outside the prompt. This matters: Microsoft's fix was architectural, not prompt-level — they did not try to write "Sydney maintains tone over long conversations."
- **No eval, no metric, no test.** Nothing about how Microsoft verified Sydney executed these rules.

**Citation caution:** treat as *credible, independently replicated, vendor-confirmed extraction* — not as an official artifact. Any quote should carry the provenance chain, not be cited as "Microsoft's published prompt."
