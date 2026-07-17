---
title: "Introducing New AI Experiences Across Our Family of Apps and Devices (Meta's 28 celebrity AI personas) + AI Studio"
url: https://about.fb.com/news/2023/09/introducing-ai-powered-assistants-characters-and-creative-tools/
org: Meta
year: 2023
type: blog
accessed: 2026-07-16
topic: bigtech-practice
---

# Meta's celebrity personas — shipped 28 characters, published ZERO character evals, killed them in <1 year, and never announced it

**Verification:** fetched the Meta newsroom post raw (812KB HTML), stripped tags, normalized,
grepped. All quotes below matched against the extracted text. Also verified the AI Studio post
(`https://about.fb.com/news/2024/07/create-your-own-custom-ai-with-ai-studio/`, HTTP 200).

## THE LAUNCH (Sept 27 2023) — verbatim

> "We're also launching **28 more AIs in beta, with unique interests and personalities**. Some are
> played by cultural icons and influencers, including Snoop Dogg, Tom Brady, Kendall Jenner, and
> Naomi Osaka."

> "we've been creating AIs that have more personality, opinions, and interests, and are a bit more
> fun to interact with. Along with Meta AI, there are 28 more AIs that you can message on WhatsApp,
> Messenger, and Instagram. You can think of these AIs as a **new cast of characters – all with
> unique backstories**. And because interacting with them should feel like talking to familiar
> people, we did something to build on this even further. **We partnered with cultural icons and
> influencers to play and embody some of these AIs.** They'll each have profiles on Instagram and
> Facebook, so you can explore what they're all about."

The roster, verbatim (partial, verified):

> "Charli D'Amelio as **Coco**, Dance enthusiast
> Chris Paul as **Perry**, Pro golfer helping you perfect your stroke
> Dwyane Wade as **Victor**, Ironman triathlete motivating you to be your best self
> Izzy Adesanya as **Luiz**, Showy MMA prospect who can back up his trash talk
> Kendall Jenner as **Billie**, **No-BS, ride-or-die companion**
> LaurDIY as **Dylan**, Quirky DIY and Craft expert and **companion for Gen Z**
> MrBeast as **Zach**, The big brother who will roast you — because he cares
> Naomi Osaka as **Tamika**, Anime-obsessed Sailor Senshi in training
> Paris Hilton as **Amber**, Detective partner for solving whodunnits
> Raven Ross as **Angie**, Workout class queen who balances fitness with meditation
> Roy Choi as **Max**, Seasoned sous chef for culinary tips and tricks
> Sam Kerr as **Sally**, Free-spirited friend who'll tell you when to take a deep breath"

Note **"ride-or-die companion"** and **"companion for Gen Z"** — Meta explicitly shipped
*companion* characters, in Meta's own words, in 2023.

## THE ABSENCE — this is the point

Each of those 28 is a **character spec**: a name, a backstory, a voice, a relationship stance
("big brother who will roast you", "ride-or-die"). Meta built, staffed, licensed likenesses for,
and shipped 28 of them.

**Meta has never published a single evaluation of whether any of them stayed in character.**

Verified greps across Meta's published corpus for any eval of these characters:
- Llama 3 paper (92pp): `\bpersonas?\b` = 3, all steerability-definition or jailbreak. **No product persona eval.**
- Llama 4 card: `\bpersonas?\b` = 0, `\bcharacters?\b` = 0.
- Llama Guard paper: 0 / 0.
- The launch post itself: contains **no evaluation, no metric, no benchmark, no testing methodology.**

The launch post's only risk language is generic (verbatim):

> "These new AI experiences also come with a new set of challenges for our industry. We're rolling
> out our new AIs slowly and…"

There is no answer to: does Billie sound like Billie? Does Zach stay a big brother 40 turns in?
Does Coco know she's Coco? **Meta shipped 28 characters and measured none of them publicly.**

## THE DEATH — and the missing primary source

The celebrity personas were **discontinued in summer 2024**, under a year after launch.

**I could not find any Meta primary source announcing the discontinuation.** This is itself a
finding, and I want to be precise about the evidentiary status:

- **Meta announced the launch** on its own newsroom (verified above, HTTP 200).
- **Meta did not announce the shutdown** on its newsroom. I found no about.fb.com post.
- The discontinuation was **first reported by The Information** ("Meta Scraps Celebrity AI Chatbots
  That Fell Flat With Users") — **paywalled; I did not verify the text firsthand. UNVERIFIED.**
- Corroborated across trade press (Social Media Today, Artnet, spyglass.org) reporting low
  engagement as the cause. **These are journalism, not primary. The stated reason — "lack of public
  interest" / low followings — is UNVERIFIED by any Meta document.**

**Asymmetry worth recording:** Meta issues a primary source when a persona product launches and
none when it dies. Any "what happened to Meta's celebrity personas" claim rests on paywalled
reporting, not on Meta.

## THE SUCCESSOR: AI Studio (July 29 2024) — verified, and equally eval-free

> "We're rolling out **AI Studio**, a place for people to create, share and discover AIs to chat
> with – **no tech skills required**."

> "Built with Llama 3.1, AI Studio lets anyone **create and discover AI characters** and allows
> creators to build an AI as an extension of themselves to reach more fans."

> "To get started building your AI character, visit ai.meta.com/ai-studio or start a new message on
> Instagram and then tap "AI chats." From there, you can customize your **AI character's name,
> personality, tone, avatar and tagline**."

So Meta's shipping product exposes **persona, tone, and character** as first-class user-editable
fields — the exact axes Llama 3 §4.3.7 declared as steerability dimensions and never measured.

**Grep of the AI Studio announcement:** `evaluat*` = **0**, `test*` = **0**, `restrict*` = **0**.
The only `safety` hits are site-footer navigation boilerplate ("Meta Quest safety center"), not
body text. **Meta handed persona authoring to every user on Instagram and published zero
evaluation methodology with it.**

(Timeline note: Meta later shut down the AI *character accounts* on Facebook/Instagram in Jan 2025
after user backlash — reported by NBC News. **Journalism, not primary. UNVERIFIED here.**)

## Answers to the four key questions

1. **Steerability / dose-response?** **No.** AI Studio lets users set personality/tone with no
   feedback on whether it took effect. The product exposes the knob and measures nothing.
2. **Comprehension vs. execution separated?** **No.**
3. **Published character/persona eval suite?** **No** — despite shipping 28 licensed characters and
   then a character-authoring platform to hundreds of millions of users.
4. **Creative writing pairwise or absolute?** **Not evaluated.**
