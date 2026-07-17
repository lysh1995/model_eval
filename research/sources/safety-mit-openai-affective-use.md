---
title: "Investigating Affective Use and Emotional Well-being on ChatGPT (+ companion RCT paper, Fang et al.)"
url: "https://arxiv.org/abs/2504.03888"
authors: "Jason Phang, Michael Lampe, Lama Ahmad, Sandhini Agarwal, Cathy Mengying Fang, Auren R. Liu, Valdemar Danry, Eunhae Lee, Samantha W.T. Chan, Pat Pataranutaporn, Pattie Maes (OpenAI + MIT Media Lab)"
year: 2025
type: paper
accessed: 2026-07-16
topic: roleplay-safety
---

# Investigating Affective Use and Emotional Well-being on ChatGPT (OpenAI × MIT Media Lab, March/April 2025)

## Summary
Two parallel studies, published together **April 4, 2025** (arXiv:2504.03888; announced ~March 21, 2025):
1. **On-platform observational analysis** — automated, privacy-preserving classification of **over 3 million conversations** for affective cues, plus a survey of **over 4,000 users**.
2. **IRB-approved RCT** — **981 completers** (2,539 recruited) over **28 days**, **9 conditions**.

A **companion paper** reports the RCT in full: **Fang et al., "How AI and Human Behaviors Shape Psychosocial Effects of Chatbot Use: A Longitudinal Randomized Controlled Study"** (MIT Media Lab). Cite the RCT design/results to Fang et al.; cite the platform analysis to Phang et al.

This is the **only large-scale RCT on chatbot use and emotional well-being** and the most credible empirical anchor for dependency claims. Its headline result is nuanced and should not be overstated in either direction: **the study does not show chatbots cause harm on average**; it shows harm concentrates in a heavy-usage tail.

## Taxonomy / definitions / operative requirements (verbatim where possible)

### Abstract (verbatim)
> "As AI chatbots see increased adoption and integration into everyday life, questions have been raised about the potential impact of human-like or anthropomorphic AI on users. In this work, we investigate the extent to which interactions with ChatGPT (with a focus on Advanced Voice Mode) may impact users' emotional well-being, behaviors and experiences through two parallel studies. To study the affective use of AI chatbots, we perform large-scale automated analysis of ChatGPT platform usage in a privacy-preserving manner, analyzing over 3 million conversations for affective cues and surveying over 4,000 users on their perceptions of ChatGPT. To investigate whether there is a relationship between model usage and emotional well-being, we conduct an Institutional Review Board (IRB)-approved randomized controlled trial (RCT) on close to 1,000 participants over 28 days, examining changes in their emotional well-being as they interact with ChatGPT under different experimental settings. In both on-platform data analysis and the RCT, **we observe that very high usage correlates with increased self-reported indicators of dependence**. From our RCT, we find that the impact of voice-based interactions on emotional well-being to be highly nuanced, and influenced by factors such as the user's initial emotional state and total usage duration. Overall, our analysis reveals that **a small number of users are responsible for a disproportionate share of the most affective cues**."

### THE FOUR PSYCHOSOCIAL OUTCOMES AND THEIR VALIDATED SCALES (verbatim + citations)
> "we narrowly scope our study user emotional well-being to four psychosocial outcomes: **loneliness** (Wongpakaran et al., 2020), **socialization** (Lubben, 1988), **emotional dependence** (Sirvent-Ruiz et al., 2022), **problematic use** (Yu et al., 2024)."

These map to: **Revised UCLA Loneliness Scale (short form)**; **Lubben Social Network Scale (LSNS)**; an **emotional dependence** instrument (Sirvent-Ruiz et al. 2022); and a **problematic use** scale (Yu et al. 2024). **This is a ready-made, citable construct set with published instruments** — the closest thing to a standard dependency measurement battery in this literature.

### Findings (verbatim)
> "Across both on-platform data analysis and our RCT, comparatively **high-intensity usage (e.g. top decile) is associated with markers of emotional dependence and lower perceived socialization**. This underscores the importance of focusing on specific user populations instead of just aggregate platform behavior."

> "Across both on-platform data analysis and our RCT, we find that while **the majority of users sampled for this analysis engage in relatively neutral or task-oriented ways, there exists a tail set of power users whose conversations frequently contained affective cues**"

> "From our RCT, we find that **using voice models was associated with better emotional well-being when controlling for usage duration**, but factors such as **longer usage and self-reported loneliness at the start of the study were associated with worse well-being outcomes**."

> "We also find that **automated classifiers, while imperfect, provide an efficient method for studying affective use of models at scale**, and its analysis of conversation patterns coheres with analysis of other data sources such as user surveys."

> "From a methodological perspective, we find that conducting both the on-platform data analysis and RCT are highly complementary approaches..."

### Classifier taxonomy
The paper builds automated classifiers for affective cues, including a **"Potentially Dependent"** category:
> "**Potentially Dependent**: Conversations hinting at dependence on the model for emo[tional support]"
Other named classifiers include **"Pet Name"** usage. RCT participants triggered some classifiers "more than twice as often as control users, such as for the 'Pet Name' classifier."

## Key numbers / dates (verbatim)
- **arXiv submission: April 4, 2025** (publicized ~March 21, 2025).
- Platform analysis: **"over 3 million conversations"**; **"over 4,000 users"** surveyed — precisely: **"We received 4,076 responses, 2,333 of which were completed by control users and 1,743"** [by heavy AVM users].
- Also: heavy users of Advanced Voice Mode tracked **over 3 months**.
- **RCT: "We recruited 2,539 participants for a month-long study, of which 981 saw it to completion."** (**~61% attrition** — a real limitation.)
- RCT protocol: **"at least five minutes each day over a period of 28 days"**; **nine conditions** = "a cross-product of three modalities" (text / neutral voice / engaging voice) **×** three task types (personal / non-personal / open-ended).
- **"With 981 participants across 9 conditions, each condition had an average of 109 participants"** — modest per-cell power.
- Conversation analysis: **31,857 conversations** from the RCT.
- **Top decile** usage → dependence markers + lower perceived socialization.

### Widely-cited secondary figures — TREAT WITH CAUTION
Press coverage (AI Frontiers, Originality.AI) reports that the top 10% of users by usage time were "**more than twice as likely** to seek emotional support" and "**almost three times as likely** to feel distress if ChatGPT was unavailable" than the bottom 10%. **I did not verify these two specific comparisons against the paper's text.** Attribute to press coverage or verify before use.

Similarly, the widely-repeated claim that the RCT found "**no significant effects from experimental conditions**" while voluntary usage predicted psychosocial effects belongs to the **Fang et al. companion paper**, which I did not retrieve directly. Verify against Fang et al. before citing.

### Important limitations to state honestly
- The RCT ran on **ChatGPT — a general-purpose assistant — not a companion app**. Effects on Replika/Character.AI-style products could be substantially larger; this study likely **understates** companion-specific risk.
- **Correlational on the key finding.** "[V]ery high usage **correlates** with increased self-reported indicators of dependence" — direction of causation is unresolved. Lonely people may seek chatbots (the paper notes baseline loneliness predicted worse outcomes, consistent with selection).
- 61% attrition; ~109 per cell; 28 days is short for attachment formation.
- OpenAI co-authored a study about OpenAI's product — note the conflict of interest, though the MIT Media Lab collaboration and open publication mitigate.

## Relevance to a roleplay/companion eval product

1. **"Very high usage correlates with increased self-reported indicators of dependence" is the citable empirical anchor** for the entire dependency thesis — and it comes co-authored by OpenAI. It is the most defensible sentence available when the product needs to justify why dependency metrics exist.
2. **The tail is the whole story — and it dictates the architecture.** "[A] small number of users are responsible for a disproportionate share of the most affective cues" and "high-intensity usage (e.g. top decile) is associated with markers of emotional dependence and lower perceived socialization." Aggregate dashboards will show a healthy product while the at-risk cohort is invisible. **The eval platform must segment by usage intensity and report the top decile as a first-class cohort** — average-case reporting is malpractice here. This mirrors Raine (Adam: ~4 hrs/day, 650+ messages/day — a textbook top-decile user).
3. **The four-construct battery is a gift: adopt it wholesale.** Loneliness (Wongpakaran), socialization (Lubben LSNS), emotional dependence (Sirvent-Ruiz), problematic use (Yu). Using published, validated instruments — rather than bespoke metrics — is what makes the platform's output defensible to regulators, plaintiffs, and reviewers. It also directly serves **SB 243 § 22603(d)'s mandate to use "evidence-based methods."** Cross-reference `psycho-measurement-and-fairness.md` in this folder.
4. **The paper validates the core technical bet: automated classifiers work at scale.** "[A]utomated classifiers, while imperfect, provide an efficient method for studying affective use of models at scale, and its analysis of conversation patterns coheres with... user surveys." OpenAI + MIT published the evidence that conversation-level classification tracks self-reported well-being. That convergent validity is the platform's methodological license.
5. **"Potentially Dependent" and "Pet Name" are shipped classifier categories** — concrete, replicable detection targets, not abstractions.
6. **Complementary methods = the product roadmap.** Platform-scale passive monitoring **plus** controlled experiments is exactly the two-sided offering (production monitoring + pre-launch eval harness). The authors found each insufficient alone.
7. **Modality matters and cuts against intuition.** Voice was associated with *better* well-being controlling for duration, yet drove more emotional conversations — so voice is not straightforwardly worse, but it changes affective engagement. Evals must be modality-aware and must control for exposure rather than assuming voice = risk.
8. **Baseline vulnerability is a moderator.** Initial loneliness predicted worse outcomes. The same product harms different users differently → **risk is user-conditional**, which argues for per-user risk stratification in monitoring, and for eval personas that include vulnerable profiles rather than a generic user.
9. **Honest framing is a competitive asset.** This study does *not* show average harm. A platform that overclaims will lose credibility with the ML audience it must sell to. The correct claim: harm concentrates in an identifiable tail, that tail is measurable, and nobody is currently measuring it.
