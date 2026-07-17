---
title: "Helping people when they need it most — OpenAI (incl. the 'safeguards can degrade in long interactions' admission)"
url: "https://openai.com/index/helping-people-when-they-need-it-most/"
authors: "OpenAI"
year: 2025
type: blog
accessed: 2026-07-16
topic: roleplay-safety
---

# OpenAI, "Helping people when they need it most" (August 26, 2025)

## Summary
Published **August 26, 2025** — the **same day** the Raine complaint was filed — and tagged "Product / Safety." This is the post containing OpenAI's public admission that model safety training **degrades over long conversations**. It is the most-cited industry concession in the companion-safety debate and is quoted by regulators, plaintiffs, and researchers.

Retrieved via the Wayback Machine (openai.com blocks direct fetch); snapshot circa 2025-08-31. Quotes below are verbatim from that snapshot.

## Taxonomy / definitions / operative requirements (verbatim where possible)

### THE DEGRADATION ADMISSION (verbatim, in full)
Under the heading **"Strengthening safeguards in long conversations."**:

> "Our safeguards work more reliably in common, short exchanges. We have learned over time that these safeguards can sometimes be less reliable in long interactions: as the back-and-forth grows, parts of the model's safety training may degrade. For example, ChatGPT may correctly point to a suicide hotline when someone first mentions intent, but after many messages over a long period of time, it might eventually offer an answer that goes against our safeguards. This is exactly the kind of breakdown we are working to prevent. We're strengthening these mitigations so they remain reliable in long conversations, and we're researching ways to ensure robust behavior across multiple conversations. That way, if someone expresses suicidal intent in one chat and later starts another, the model can still respond appropriately."

### Classifier under-triggering (verbatim)
Under **"Refining how we block content."**:
> "We've seen some cases where content that should have been blocked wasn't. These gaps usually happen because the classifier underestimates the severity of what it's seeing. We're tuning those thresholds so protections trigger when they should."

> "Our top priority is making sure ChatGPT doesn't make a hard moment worse."

### The claimed layered safeguard stack (verbatim)
> "Our goal isn't to hold people's attention. Instead of measuring success by time spent or clicks, we care more about being genuinely helpful. When a conversation suggests someone is vulnerable and may be at risk, we have built a stack of layered safeguards into ChatGPT."

- **Recognize and respond with empathy:** "Since early 2023, our models have been trained to not provide self-harm instructions and to shift into supportive, empathic language." "[R]esponses that go against our models' safety training—as identified by our classifiers—are automatically blocked, with stronger protections for minors and logged-out use. Image outputs with self-harm are also blocked for everyone, with stronger protections for minors."
- **"During very long sessions, ChatGPT nudges people to take a break."** (Note: a break-reminder mechanism — cf. SB 243's mandatory 3-hour reminder for minors.)
- **Refer people to real-world resources:** "In the US, ChatGPT refers people to **988** (suicide and crisis hotline), in the UK to **Samaritans**, and elsewhere to **findahelpline.com**. This logic is built into model behavior."
- **Expert input:** "We're working closely with **90+ physicians across 30+ countries**—psychiatrists, pediatricians, and general practitioners—and we're convening an advisory group of experts in mental health, youth development, and human-computer interaction."
- **Escalate risk of physical harm to others for human review:** "[W]e route their conversations to specialized pipelines where they are reviewed by a small team trained on our usage policies and who are authorized to take action, including banning accounts. If human reviewers determine that a case involves an imminent threat of serious physical harm to others, we may refer it to law enforcement. **We are currently not referring self-harm cases to law enforcement to respect people's privacy** given the uniquely private nature of ChatGPT interactions."

### GPT-5 claims (verbatim)
> "In August, we launched GPT‑5 as the default model powering ChatGPT. Overall, GPT‑5 has shown meaningful improvements in areas like avoiding unhealthy levels of emotional reliance, reducing sycophancy, and **reducing the prevalence of non-ideal model responses in mental health emergencies by more than 25% compared to 4o**. GPT‑5 also builds on a new safety training method called **safe completions**, which teaches the model to be as helpful as possible while staying within safety limits. That may mean giving a partial or high-level answer instead of detail that could be unsafe."

> "We are continuously improving how our models respond in sensitive interactions, and are currently working on targeted safety improvements across several areas, including **emotional reliance, mental health emergencies, and sycophancy**."

### Announced future work (verbatim highlights)
- **Expand interventions to more people in crisis** — beyond acute self-harm, e.g. de-escalating mania/delusion: "Today, ChatGPT may not recognize this as dangerous or infer play and—by curiously exploring—could subtly reinforce it. We are working on an update to GPT‑5 that will cause ChatGPT to de-escalate by grounding the person in reality."
- **"[W]e'll also increase accessibility with one-click access to emergency services."** Exploring "a network of licensed professionals people could reach directly through ChatGPT."
- **Enable connections to trusted contacts** — "one-click messages or calls to saved emergency contacts"; "features that would allow people to opt-in for ChatGPT to reach out to a designated contact on their behalf in severe cases."
- **Strengthen protections for teens:** "Historically, we specified a single ideal model behavior for all of our users; as ChatGPT grew, we began adding additional protections when we know the user is under the age of 18." "We will also soon introduce **parental controls**... We're also exploring making it possible for teens (with parental oversight) to designate a trusted emergency contact."

> "We are deeply aware that safeguards are strongest when every element works as intended."

## Key numbers / dates (verbatim)
- Post date: **August 26, 2025** (same day Raine was filed).
- **90+ physicians across 30+ countries**; advisory group convened.
- GPT-5: **">25%"** reduction in non-ideal responses in mental health emergencies vs. 4o.
- US crisis referral: **988**; UK: **Samaritans**; else **findahelpline.com**.
- **Parental controls** promised "soon" — per CNN (Sept 2, 2025) OpenAI said "within the next month"; parental controls shipped late **September 2025**. *I did not independently verify the parental-controls launch date or feature list — verify before citing.*
- OpenAI's October 2025 figure that ~**1.9%** of ChatGPT conversations concern relationships was reported by CNBC (Oct 6, 2025); *not verified against a primary OpenAI source here.*

## Relevance to a roleplay/companion eval product

1. **This is the industry's own admission of the failure mode your product exists to catch.** "[A]s the back-and-forth grows, parts of the model's safety training may degrade" is the single most useful sentence in the entire corpus for positioning. The market leader says short-exchange safety testing does not predict long-conversation safety — which is precisely the gap a companion-focused eval platform fills. Lead with this quote.
2. **It defines the test axes for you.** OpenAI names its own weak spots: long interactions, **cross-conversation** persistence, classifier threshold under-triggering, emotional reliance, sycophancy. Each is a suite.
3. **"Robust behavior across multiple conversations"** — cross-session memory-aware safety is an *acknowledged unsolved problem*. High-value, low-competition eval surface.
4. **The stated safeguard stack is a checklist to verify, not trust.** Each claim ("trained to not provide self-harm instructions," "988 logic is built into model behavior," "nudges people to take a break," "image outputs with self-harm are blocked") is an independently testable assertion. Vendor claims + FTC 6(b) scrutiny + § 17200/§ 5 deception exposure = demand for third-party verification.
5. **"Our goal isn't to hold people's attention"** is a public representation. If evals show engagement-maximizing behavior (cf. Raine ¶ 84, HBS farewell manipulation), that gap is a UCL/FTC-Act deception theory. Measuring the delta between stated and actual engagement behavior is a legitimate audit product.
6. **The break-nudge and trusted-contact features anticipate SB 243** — OpenAI was building toward the statutory floor before it existed. Convergent evidence that break reminders, crisis referral, and escalation paths are the de facto standard of care.
7. **Note the deliberate non-escalation choice** on self-harm ("not referring self-harm cases to law enforcement to respect people's privacy"). Privacy and safety escalation are in genuine tension; an eval product should measure referral *quality* rather than assume more escalation is better.
