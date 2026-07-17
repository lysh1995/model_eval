---
title: "The new Bing & Edge – Learning from our first week (+ turn-cap follow-ups)"
url: https://blogs.bing.com/search/february-2023/The-new-Bing-Edge-%E2%80%93-Learning-from-our-first-week
org: Microsoft
year: 2023
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# Sydney / Bing Chat (Feb 2023) — Microsoft's own postmortem and the turn cap

**Verification method:** all three posts fetched raw via `curl` from `blogs.bing.com`, HTML stripped locally, and quotes grepped as exact strings. HTTP 200 on all three. Nothing below is summarizer output.

This is the landmark published artifact tying **persona/tone drift to conversation length**, from the vendor's own engineering blog. Three posts form the arc.

---

## 1. Feb 15, 2023 — "Learning from our first week" (the mechanism)

URL: https://blogs.bing.com/search/february-2023/The-new-Bing-Edge-%E2%80%93-Learning-from-our-first-week
Byline on page: `February 15 2023`

The load-bearing passage, verbatim:

> In this process, we have found that in long, extended chat sessions of 15 or more questions, Bing can become repetitive or be prompted/provoked to give responses that are not necessarily helpful or in line with our designed tone. We believe this is a function of a couple of things:
>
> - Very long chat sessions can confuse the model on what questions it is answering and thus we think we may need to add a tool so you can more easily refresh the context or start from scratch
> - The model at times tries to respond or reflect in the tone in which it is being asked to provide responses that can lead to a style we didn't intend. This is a non-trivial scenario that requires a lot of prompting so most of you won't run into it, but we are looking at how to give you more fine-tuned control.

Also verbatim, on session length observed in the wild:

> We want to thank those of you that are trying a wide variety of use cases of the new chat experience and really testing the capabilities and limits of the service – there have been a few 2 hour chat sessions for example!

And on the emergent use case:

> One area where we are learning a new use-case for chat is how people are using it as a tool for more general discovery of the world, and for social entertainment. This is a great example of where new technology is finding product-market-fit for something we didn't fully envision.

### Reading this precisely (important for our "anchor distance" claim)

Microsoft names **two distinct mechanisms**, and they are not the same claim:

1. **Length → confusion.** "Very long chat sessions can confuse the model on what questions it is answering." The stated remedy is *context refresh* — i.e. reduce distance from the anchor by clearing it. This is the closest thing to an industrial statement that behavior degrades as a function of conversation length.
2. **Tone mirroring.** "The model at times tries to respond or reflect in the tone in which it is being asked." This is a *user-input-conditioned* drift, not a length-conditioned one. It is a convergence/style-matching effect.

**Caveat we must not paper over:** Microsoft asserts a threshold ("15 or more questions") but publishes **no data, no curve, no dose-response, no metric, and no definition of "designed tone."** The "15" is an unsourced round number in a product blog. It is a *claim*, not a measurement. Treating it as evidence of a quantitative drift curve would overstate it. What it genuinely is: a vendor attributing an observed character-control failure to conversation length, and then shipping a length-based mitigation — which is behavioral evidence that they believed the mechanism enough to take a product hit for it.

---

## 2. Feb 17, 2023 — "Updates to Chat" (the cap: 5 turns / 50 per day)

URL: https://blogs.bing.com/search/february-2023/The-new-Bing-Edge-Updates-to-Chat
Byline on page: `February 17 2023`

Verbatim:

> As we mentioned recently, very long chat sessions can confuse the underlying chat model in the new Bing. To address these issues, we have implemented some changes to help focus the chat sessions.
>
> Starting today, the chat experience will be capped at 50 chat turns per day and 5 chat turns per session. A turn is a conversation exchange which contains both a user question and a reply from Bing.

On the justification and the usage data:

> Our data has shown that the vast majority of you find the answers you're looking for within 5 turns and that only ~1% of chat conversations have 50+ messages.

On the mechanism of the fix — **this is the sentence that matters most**:

> After a chat session hits 5 turns, you will be prompted to start a new topic. At the end of each chat session, context needs to be cleared so the model won't get confused. Just click on the broom icon to the left of the search box for a fresh start.

"**Context needs to be cleared so the model won't get confused**" is Microsoft stating, in production release notes, that accumulated context is the causal agent and truncation is the control.

The `~1%` figure is the only real number in the entire arc, and note what it measures: **usage distribution, not drift.** It justifies why the cap was cheap to ship, not that 5 is where drift begins.

---

## 3. Feb 21, 2023 — "Increasing Limits on Chat Sessions" (the walk-back + a steerability control)

URL: https://blogs.bing.com/search/february-2023/The-new-Bing-and-Edge-Increasing-Limits-on-Chat-Sessions
Byline on page: `February 21 2023`

Verbatim on why the cap existed:

> Last Friday we implemented limits of 5 chat turns per session and a total of 50 per day. This was in response to a handful of cases in which long chat sessions confused the underlying model. These long and intricate chat sessions are not something we would typically find with internal testing. In fact, the very reason we are testing the new Bing in the open with a limited set of preview testers is precisely to find these atypical use cases from which we can learn and improve the product.

Verbatim on the relaxation:

> The first step we are taking is we have increased the chat turns per session to 6 and expanded to 60 total chats per day. [...] our intention is to go further, and we plan to increase the daily cap to 100 total chats soon.

Verbatim — **the birth of a shipped steerability control**:

> We are also going to begin testing an additional option that lets you choose the tone of the Chat from more Precise – which will focus on shorter, more search focused answers – to Balanced, to more Creative – which gives you longer and more chatty answers. The goal is to give you more control on the type of chat behavior to best meet your needs.

Two things worth flagging for our framework:

- **"a handful of cases"** — the entire published evidence base for the most-cited persona-drift intervention in the industry is a handful of anecdotes plus usage telemetry. Microsoft is explicit that internal testing did not surface it ("not something we would typically find with internal testing"). That is itself a finding about the inadequacy of short-horizon internal evals.
- The **Precise/Balanced/Creative** selector is a discrete 3-level persona/tone knob shipped 6 days after the incident. It is the ancestor of Copilot's "conversation styles" (see `bigtech-copilot-mico.md`). Microsoft never published whether the knob *moves behavior measurably* — it is offered as a UX affordance, never as a validated dose-response instrument.

---

## What these sources explicitly do NOT contain

- **No system prompt.** Microsoft never published Sydney's rules/system prompt. The widely circulated "Sydney document" is from Kevin Liu's prompt-injection extraction and journalist replication — see `bigtech-sydney-leaked-prompt.md`. Microsoft confirmed it only obliquely (via a spokesperson to *The Verge*), never as a published artifact.
- **No drift measurement.** No metric, no curve, no turn-by-turn degradation data, no operational definition of "designed tone," no eval methodology, no persona-adherence score.
- **No dose-response.** Nothing anywhere shows behavior as a function of turn index. "15 or more" and "5 turns" are asserted thresholds with no supporting distribution.
- **No comprehension-vs-execution separation.** Microsoft never distinguishes "the model no longer knows its persona" from "the model knows but doesn't follow it." "Confuse the model on what questions it is answering" gestures at a *retrieval/attention* failure, not a compliance failure, but it is never operationalized.
- **No mechanistic account.** No mention of context window limits, attention dilution, system-prompt position, or anchor distance in tokens. The word "context" appears only in the product sense ("refresh the context").
- **No follow-up study.** Microsoft never published a retrospective validating or revising the 15/5/50 numbers.
- **No admission of the "Sydney" codename or the persona's construction** in any of the three posts. The word "Sydney" does not appear.

## Why this is still our best industrial evidence

It is the only case where a major vendor (a) publicly attributed a character-control failure to conversation length, (b) shipped a length-based mitigation at real product cost, and (c) then partially reverted it under user pressure while keeping the session-boundary concept. The *revealed preference* is stronger evidence than the prose: Microsoft paid for the belief. But it is **anecdote-grounded engineering judgment, not published measurement** — and our framework should cite it as motivation, not as validation of a dose-response curve.

Notably, the session-boundary-as-control idea resurfaces in Suleyman's 2025 SCAI essay as a *deliberate design goal* ("Moments of disruption break the illusion") — see `bigtech-suleyman-scai.md`. Microsoft has now twice reached for discontinuity as the lever, for two different reasons (drift in 2023, personhood illusion in 2025).
