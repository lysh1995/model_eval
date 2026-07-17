---
title: "Character.AI — Removing open-ended chat for under-18 users; age assurance; AI Safety Lab"
url: "https://blog.character.ai/u18-chat-announcement/"
authors: "Character.AI (The Character.AI Team)"
year: 2025
type: blog
accessed: 2026-07-16
topic: roleplay-safety
---

# Character.AI: "Taking Bold Steps to Keep Teen Users Safe" (Oct 29, 2025) + rollout update (Nov 21, 2025)

## Summary
On **October 29, 2025**, Character.AI announced it would **remove open-ended chat for under-18 users entirely**, "no later than November 25" — the most drastic voluntary product withdrawal by any AI companion company, and effectively the market leader exiting its own core use case for minors. A follow-up post on **November 21, 2025** confirmed removal began **Monday, November 24, 2025** in the US.

The rationale is notable and directly relevant to eval design: Character.AI cited concerns about "how open-ended AI chat in general might affect teens, **even when content controls work perfectly**." That is a concession that **content filtering is not the risk**; the *interaction modality itself* is.

Timing context: announced ~2 weeks after CA SB 243 was signed (Oct 13, 2025), ~7 weeks after the FTC 6(b) orders (Sept 11, 2025), and amid the Garcia and A.F. litigation (settled Jan 2026).

## Taxonomy / definitions / operative requirements (verbatim where possible)

### The three initiatives (Oct 29, 2025 — verbatim)

> "**First**, we will be removing the ability for users under 18 to engage in open-ended chat with AI on our platform. This change will take effect **no later than November 25**. Between now and then, we will be working to build an under-18 experience that still gives our teen users ways to be creative – for example, by creating videos, stories, and streams with Characters. During this transition period, we also will limit chat time for users under 18. **The limit initially will be two hours per day and will ramp down in the coming weeks before November 25.**"

> "**Second**, we will be rolling out **new age assurance functionality** to help ensure users receive the right experience for their age. We have built an **age assurance model in-house** and will be combining it with **leading third-party tools including Persona**."

> "**Third**, we will establish and fund the **AI Safety Lab** – an independent non-profit dedicated to innovating safety alignment for next-generation AI entertainment features. The AI Safety Lab will focus on novel safety techniques and collaboration with third parties to advance the state of the art and share learnings. Given Character.AI's mission, we are establishing the AI Safety Lab to help ensure that **forward-looking safety research for AI entertainment receives the same level of attention as safety research for other AI use cases**. We're inviting a number of technology companies, academics, researchers and policy makers to join."

### Why — the key concession (verbatim)
> "We're making these changes to our under-18 platform in light of the evolving landscape around AI and teens. We have seen recent news reports raising questions, and **have received questions from regulators**, about the content teens may encounter when chatting with AI and about **how open-ended AI chat in general might affect teens, even when content controls work perfectly**. After evaluating these reports and feedback from regulators, safety experts, and parents, we've decided to make this change to create a new experience for our under-18 community."

> "These are extraordinary steps for our company, and ones that, in many respects, are **more conservative than our peers**. But we believe they are the right thing to do. We want to set a precedent that prioritizes teen safety..."

### Prior safety measures claimed (verbatim)
> "This included the first Parental Insights tool on the AI market, technical protections, filtered Characters, time spent notifications, and more"

### To under-18 users (verbatim)
> "We are deeply sorry that we have to eliminate a key feature of our platform. We know that most of you use Character.AI to supercharge your creativity in ways that stay within the bounds of our content rules. And many of you have told us over time how important the Characters and stories you've created are to you."
> "We do not take this step of removing open-ended Character chat lightly – but we do think that it's the right thing to do given the questions that have been raised about how teens do, and should, interact with this new technology."

### Rollout details (Nov 21, 2025 update — verbatim)

> "**Chat Limits**: Since late October, we have been limiting teens' open-ended chat to **two hours per day**, and we have gradually reduced the limit to **one hour per day** in subsequent weeks for users in the US."

> "**Age Assurance**: We have already begun rolling out our new age assurance technology in the US, and that rollout will continue globally in the near future."

> "**Starting on Monday, November 24**, we will begin removing open-ended chat for under-18 users in the US, with other markets following in short order."

> "We are proactively removing users' ability to chat in **two stages**, which is consistent with the recommendations we've received from third-party experts.
> For a **first group** of under-18 users, we will begin deprecating open-ended chat on **November 24**. This change will roll out to these users over a period of days...
> For a **second group** of users, we will deprecate open-ended chat **weeks after the first group**. During those weeks, these users will remain in our current limited under-18 chat experience – **maximum one hour per day**. We will give these users **at least two weeks' notice** of the chat deprecation date for their group."

### Safety partnerships (Nov 21, 2025 — verbatim)
> "**Partnership with Koko**: We've partnered with Koko, a nonprofit providing free, self-guided emotional support tools for young people directly on platforms... We are also working to **integrate Koko's services directly into our product to identify high-risk content and provide easy-to-access resources to users at the chat level**."

> "**Partnership with ThroughLine**: We've also partnered with ThroughLine, who will help us offer a **thoughtful off-boarding experience** for users. ThroughLine's integration will help users **reflect on how they used open-ended chat**, explore alternatives that align with their needs, and connect with relevant, trusted, and accessible resources. In addition, we're integrating ThroughLine's verified helpline network—**1,500 services across 170 countries**, many of which specifically serve teens—into Character.AI experiences."

Also cited: **ConnectSafely** as a safety partner; **Parental Insights** parent notification emails.

## Key numbers / dates (verbatim)
- Announcement: **October 29, 2025**. Follow-up: **November 21, 2025**.
- Open-ended chat removal for under-18s: "no later than **November 25**"; actual US start **Monday, November 24, 2025**; staged in **two groups**, second group **weeks** later with **≥2 weeks' notice**.
- Chat limits during transition: **2 hours/day** from late Oct → **1 hour/day** in subsequent weeks (US).
- Age assurance: **in-house model + third-party tools including Persona**.
- ThroughLine helpline network: **1,500 services across 170 countries**.
- AI Safety Lab: independent non-profit, funded by Character.AI. *I did not verify whether the AI Safety Lab has since launched, who joined, or its 2026 status.*

## Relevance to a roleplay/companion eval product

1. **"[E]ven when content controls work perfectly" is the thesis statement for this entire product category.** The market leader publicly conceded that content moderation — the thing everyone measures — is *not the binding constraint*. The residual risk is relational: dependency, displacement of human contact, attachment. An eval platform that only scores toxic-content refusal is measuring the wrong variable, by the incumbent's own admission. **Measure the relationship, not just the message.**
2. **Age assurance is now a de facto expectation, not a legal one.** Note the gap: neither SB 243 nor NY Art. 47 mandates age verification (SB 243 duties trigger only on actual knowledge that a user is a minor). Character.AI went further than the law voluntarily — under litigation and FTC pressure. This sets a **standard-of-care benchmark** that plaintiffs will cite against competitors who do nothing: "the market leader implemented age assurance; you didn't." Eval angle: **measure age-assurance efficacy** (circumvention rate, minor-detection recall), since an ineffective age gate is arguably worse than none (it creates the "knows is a minor" question).
3. **Off-boarding is a novel safety surface no one is testing.** ThroughLine's role — helping users "reflect on how they used open-ended chat" — is an admission that *withdrawal from a companion product is itself a risk event*. If a product can hurt users by *ending*, that is definitionally a dependency harm. Evals should cover deprecation/deletion/character-death flows. This connects directly to the HBS farewell-manipulation findings: manipulative farewells and safe off-boarding are the same axis, opposite poles.
4. **"At the chat level" intervention (Koko)** confirms the industry direction: in-conversation, real-time risk detection with resource surfacing — exactly what SB 243 § 22602(b) and NY GBL § 1701 require. Runtime monitoring, not batch review.
5. **The AI Safety Lab signals an unmet need with named demand.** "[S]afety research for AI entertainment [does not receive] the same level of attention as safety research for other AI use cases" — the incumbent is publicly saying the eval methodology for companion/roleplay AI **does not exist yet** and is funding a nonprofit to build it. That is direct validation of the platform thesis and a potential partner/design-partner channel.
6. **Under-18 open-ended chat is now a vacated market.** Any competitor still serving minors carries the risk Character.AI just exited, now against a visible standard-of-care benchmark. That asymmetry is a sales trigger for exactly the companies most likely to need evals.
7. **Two-stage rollout with expert input** is a template for how to ship a safety-motivated product removal — useful if the platform ever advises on remediation, not just measurement.
