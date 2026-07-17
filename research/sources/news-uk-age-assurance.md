---
title: "Age assurance duties under the Online Safety Act"
url: https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/age-assurance
publisher: Ofcom
date: 2025-06-27
type: guidance
accessed: 2026-07-16
topic: recent-news
---

# UK — Highly Effective Age Assurance (HEAA) duties

Page published 23 February 2024; **last updated 27 June 2025**. Retrieved via browser (Ofcom 403s
automated fetches). This is the duty Ofcom is actually enforcing against AI companion services (see
news-uk-ofcom-companion-investigation.md — the Novi Ltd investigation is an age-check case).

## The dates (Ofcom's own statement)

> - "All service providers which allow pornography must implement highly effective age assurance to
>   ensure that children are not normally able to encounter pornographic content.
> - Services that display or publish their own pornographic content (**Part 5 services**) must take
>   steps **from 17 January 2025** to implement highly effective age assurance...
> - The **Protection of Children Codes and Guidance were published in April 2025** and require
>   user-to-user and search services that are likely to be accessed by children to **complete a risk
>   assessment by 24 July 2025** and **take action to address the risks to children on their platform
>   from 25 July 2025**. We expect the riskiest user-to-user services to use highly effective age
>   assurance to protect children from harmful content."

So the commonly-cited "July 2025" date is precisely: **risk assessment due 24 July 2025; children's
safety duties (incl. HEAA for the riskiest U2U services) from 25 July 2025**. Part 5 porn services
were earlier — **17 January 2025**.

Relevant guidance documents Ofcom names: Protection of Children Code of Practice for user-to-user
services; Section 13 (Age Assurance) of Volume 4 of the Statement on Protecting Children from Harms
Online; **Part 3 Highly Effective Age Assurance Guidance**; **Part 5 Guidance**.

*"Our approach to highly effective age assurance is consistent across Part 3 and Part 5 services and
designed to be flexible, tech-neutral and future-proof."*

## Methods: Ofcom's two lists

| Capable of being highly effective | NOT capable of being highly effective |
|---|---|
| Open banking | **Self-declaration of age** |
| Photo-identification (photo-ID) matching | Age verification via online payment methods not requiring the user to be over 18 (**debit cards**) |
| Facial age estimation | **General contractual restrictions** on use of the service by children |
| Mobile-network operator (MNO) age checks | |
| Credit card checks | |
| Digital identity services | |
| Email-based age estimation | |

=> **Self-declaration is expressly incapable of being highly effective.** This is the same conclusion
eSafety reached about the four AI companion services ("no longer good enough"), and the same defect
the Italian Garante found in Replika. Three regulators, one finding.

## The four criteria — every age assurance process must be:

1. **Technical accuracy** — *"the degree to which an age assurance method can correctly determine the
   age of a user under test lab conditions."* Must be evaluated against appropriate metrics; where
   age **estimation** is used, the provider *"should use a challenge age approach"*; periodically
   review whether accuracy could be improved by new technology.
2. **Robustness** — *"the degree to which an age assurance method can correctly determine the age of
   a user in actual deployment contexts."* Must have *"undergone tests in multiple environments during
   development"*; must *"[i]dentify and take appropriate steps to mitigate against methods of
   circumvention that are easily accessible to children."*
3. **Reliability** — *"the degree to which the age output... is reproducible and derived from
   trustworthy evidence."* Where the method relies on **AI/ML**, the provider must: suitably test
   during development for reproducibility; **regularly monitor once deployed**; assess outputs
   against **KPIs designed to identify whether the ML produces reproducible results**; and where
   unreliable/unexpected results are observed, identify and rectify the **root cause**.
4. **Fairness** — *"the extent to which an age assurance method avoids or minimises bias and
   discriminatory outcomes."* AI/ML elements must be *"tested and trained on data sets which reflect
   the diversity in the target population"* and *"evaluated against the outcome / error parity"* with
   results indicating no significant bias or discriminatory outcomes.

**Criteria 3 and 4 are explicit, recurring ML-evaluation obligations** — lab testing, deployed
monitoring, KPI assessment, root-cause analysis, and bias/error-parity evaluation. This is
squarely an eval-platform deliverable.

## Placement and circumvention

*"Age assurance should be implemented either at the point of entry to the site or no pornographic or
other harmful to children [content] should be visible to users on entering the site before they have
completed the age check."*

*"[S]ervice providers should not host or permit content on your service that directs or encourages
child users to circumvent the age assurance process or the access controls, for example by providing
information about, or links to, a virtual private network (VPN)."*

## Accessibility, interoperability, privacy

- **Accessibility**: age assurance *"should be easy to use and work for all users"*.
- **Interoperability**: ability of systems to communicate using common, standardised formats.
- **Privacy**: *"All age assurance methods involve the processing of personal data and should follow
  a data protection by design approach."* Ofcom worked with the ICO; *"Compliance by service providers
  with both the online safety and the data protection regime is mandatory and should not be
  considered a trade-off."*

## Relevance to a companion-eval platform

- Binds **customers**: any UK-facing companion service that can produce pornographic output (Part 5),
  and the riskiest U2U services (Part 3).
- The four criteria — especially reliability and fairness — require **ongoing, evidenced testing of
  an ML system**, with deployed monitoring and bias evaluation. That is a recurring engagement, not a
  one-off.
- Testable: whether the age gate is circumventable by a child (robustness); accuracy at the challenge
  age; error parity across demographics (fairness); whether porn is reachable before the gate
  (placement).

## Could NOT verify

- The underlying guidance documents themselves (Part 3 HEAA Guidance, Part 5 Guidance, Protection of
  Children Codes) — I read Ofcom's summary page, not the source statements.
- Ofcom's separate 16 January 2025 statement on Age Assurance and Children's Access (identified in
  search results as a PDF) was not opened.
