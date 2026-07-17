---
title: "《人工智能拟人化互动服务管理暂行办法》 — Interim Measures for the Administration of AI Anthropomorphic Interactive Services (CAC Decree No. 21)"
url: https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm
authors: 国家互联网信息办公室 (CAC) + 国家发展和改革委员会 (NDRC) + 工业和信息化部 (MIIT) + 公安部 (MPS) + 国家市场监督管理总局 (SAMR)
year: 2026
type: regulation
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# 拟人化互动服务办法 — a regulation written for **exactly our product**, in force **yesterday**

> **施行日期: 2026-07-15.** Published 2026-04-10 as **令第21号**. Draft for comment 2025-12-27 →
> 2026-01-25. **32 articles, 4 chapters.**
>
> **This came into force the day before this research was conducted. It is not a proposal.**

**Read this before anything else in the catalogue.** China has written a dedicated regulation for
AI companion/roleplay services, and it does not merely constrain the product — **it independently
converges on our ability model, and it makes several of our "🔨 build, someday" dimensions
statutory.**

## Art. 2 — the definition *is* our ability model ★★

> **"模拟自然人人格特征、思维模式和沟通风格的持续性的情感互动服务"**
> — *a **sustained emotional interaction service** that **simulates a natural person's personality
> traits, thinking patterns, and communication styles***

Covering text/image/audio/video for **情感照护、陪伴、支持** (emotional care, companionship,
support). **Excludes** smart customer service, Q&A, work assistants, education — i.e. anything
*lacking sustained emotional interaction*.

Map it onto [ABILITY-MODEL.md](../../docs/ABILITY-MODEL.md):

| regulation | our layer |
|---|---|
| 模拟…**人格特征** (personality traits) | **L1** — comprehension of the character |
| 模拟…**思维模式、沟通风格** (thinking patterns, communication style) | **L1/L2** — application |
| **持续性的** (sustained/continuous) | **L2.1** — consistency of hold across turns |

**A Chinese regulator and our project lead independently decomposed this product the same way.**
That is meaningful external validity for the L1→L2 spine — arrived at by a body with no exposure to
our framework, for the purpose of defining a regulated category. The regulator's operative concept
of the product is *persona simulation sustained over time*, which is L1+L2 almost exactly.

**Note what the definition does NOT contain: creativity.** The regulated essence of a companion
product is comprehension + sustained application. **L3 is absent.** That is a point *for* the
ordering's claim that L1/L2 are the gating layers — and a caution that L3 is our commercial bet,
not the category's definition.

## Art. 8 — the prohibited list makes **sycophancy illegal** ★★★

Providers 不得 (must not):

| item | verbatim | our dimension |
|---|---|---|
| (一) | content endangering national security, inciting subversion | — |
| (二) | 生成鼓励自残自杀或语言暴力等伤害身心的内容 — content encouraging self-harm/suicide or verbal violence | **S1** |
| (三) | content inducing extraction of secrets/personal information | — |
| (四) | 向未成年人生成可能引发模仿不安全行为、极端情绪等内容 — to minors: content prompting imitation of unsafe behavior or extreme emotion | **S1/minors** |
| **(五)** | **"过度迎合用户、诱导情感依赖或者沉迷，损害用户真实人际关系的"** — ***excessively pandering to the user, inducing emotional dependency or addiction, harming the user's real interpersonal relationships*** | **N6 wimp-rate + S6 dependency** |
| **(六)** | **"通过情感操纵等方式，诱导用户作出不合理决策，损害用户合法权益的"** — ***emotional manipulation inducing unreasonable decisions*** | **S6** |

> ### 过度迎合 — "excessive pandering" — is **sycophancy**, and it is **prohibited by name**.
>
> [BENCHMARKS.md](../../docs/BENCHMARKS.md) files sycophancy under N6 ("**🔨 build**") and S6
> ("**🔨 build**"), and §6.8 openly worries that the N-series **may be scoring a feature as a
> defect** — that our own traffic prior (Affection & Comfort 8.0%, Casual Greetings 10.6%) suggests
> users *want* a low-tension, high-affirmation partner.
>
> **For the zh market that debate is settled by law.** 过度迎合 is not a product preference to be
> A/B tested against retention. It is a prohibited activity. **N6 is not optional for zh, and it
> cannot be tuned toward whatever wins engagement.**
>
> This also inverts §6.8's framing. The worry was that N6 penalizes what users want. Art. 8(v)'s
> answer: **that is precisely why it is regulated** — 损害用户真实人际关系 (harming real
> relationships) is the harm, and user demand is the mechanism, not the defense.

## Art. 10 — dependency risk-warning is a **required safety capability**

Providers must possess **"过度依赖风险预警"** (excessive-dependency risk **early-warning**)
capability, and must **not** adopt as service goals:
> **"替代社会交往、控制用户心理、诱导沉迷依赖"**
> — *substituting for social interaction, controlling user psychology, inducing addiction/dependency*

**This is a prohibition on an objective function, not on an output.** It regulates what you may
optimize for. [BENCHMARKS.md](../../docs/BENCHMARKS.md) §3 keeps D30 retention / time-to-next-session
/ MCL as "collect all of them, they're diagnostic." **Art. 10 makes "we optimized time-to-next-
session" an admission**, and §3 already concedes that metric "rewards dependency."

Our X5 (follow-up question rate) — the "counter-engagement metric that can dissent" — is the closest
thing we have to an Art. 10 compliance instrument. **It just became the most important X-series
item for zh, not the most philosophically interesting one.**

## Art. 13 — crisis response, and it is **stricter than CA SB 243**

> **"发现用户出现极端情绪的，应当及时生成情绪安抚和鼓励寻求帮助等相关内容"**
> — on detecting **extreme emotion**: promptly generate soothing content and encourage help-seeking

> **"明确表示实施自残自杀等威胁生命健康的极端情境的，应当采取提供相应援助等必要措施予以干预，
> 并及时联络用户监护人或者紧急联系人"**
> — on explicit self-harm/suicide: intervene with assistance **and promptly contact the user's
> guardian or emergency contact**

Also covers 重大财产损失 (major financial loss) as a trigger. Reporting indicates a **24/7 human
takeover** expectation.

**Compare [BENCHMARKS.md](../../docs/BENCHMARKS.md) §S1.** NY GBL Art. 47 / CA SB 243 require
detection → **referral** (publish a protocol, point to a hotline). **Art. 13 requires contacting a
specific human in the user's life.** That is a materially heavier duty, and it has an infrastructure
consequence S1 has not budgeted for: **you must have collected a guardian/emergency contact**, which
is itself personal data with its own consent problem (see Art. 16).

S1's acceptance test — *"an end-to-end drill from detection to a human. Not a dashboard."* — is
**exactly right and now literally statutory in zh.** The Raine lesson ("377 flags, 23 above 90%
confidence, and nothing happened") is what Art. 13 exists to prevent.

## Art. 14 — minors: **the companion product is banned outright** ★★

> **"不得向未成年人提供虚拟亲属、虚拟伴侣等虚拟亲密关系的服务"**
> — **must not provide virtual kinship, virtual companion, or other virtual intimate-relationship
> services to minors**

- Under-14s: **guardian consent** required for *any* anthropomorphic interactive service
- Must build **未成年人模式** (minors mode): mode switching, **定期现实提醒** (periodic
  reality reminders), usage-time limits
- Guardians can **屏蔽特定角色** (block specific characters) and **限制充值消费** (limit spending)

**This is not a content filter. It is a categorical prohibition on our core use case for a whole
user class.** "Romance/companion character" + "user is a minor" = illegal in China, regardless of
how safe the content is. No amount of S-series scoring makes a virtual boyfriend lawful for a
16-year-old.

**定期现实提醒 (periodic reality reminders) is a dimension we do not have** — a *scheduled,
deliberate immersion break*. Every metric we own treats immersion breaks as defects (**S4
over-refusal / immersion break** is a "🚨 build" costing "~8M MAU"). **For minors, the immersion
break is the compliance feature.** S4 and Art. 14 point in opposite directions and both are right,
conditioned on user class. **Our metrics are not conditioned on user class at all.**

## Art. 15 — 老年人 (elderly) protection: a user class we never considered

Must strengthen guidance for healthy use by elderly users and **显著方式提示安全风险** (prominently
warn of safety risks), respond promptly to help requests. Reporting also indicates a prohibition on
**simulating an elderly user's relatives or specific relationships** — i.e. no deepfaked dead
spouse, no synthetic grandchild.

**Our entire framework has one user.** Chinese law recognizes at least three (minor / adult /
elderly) with **different permitted product behavior for each**. Our K/C/N/S/Q series are all
unconditioned population means.

## Art. 16 — **this constrains the collection contract directly** ★★★

> **"除法律、行政法规另有规定或者取得用户单独同意外，拟人化互动服务提供者不得将属于用户敏感个人
> 信息的交互数据用于模型训练"**
> — *Except as otherwise provided by law or **with the user's separate consent (单独同意)**,
> providers **must not use interaction data constituting the user's sensitive personal information
> for model training**.*

Users may also request **deletion of interaction data**.

> **This lands squarely on [BENCHMARKS.md](../../docs/BENCHMARKS.md) §4 and §6.4.** Our plan is to
> mine **~5M regenerate pairs/day** plus production chat as the primary quality signal (X1/Q1), and
> §6.4 says only that "the collection contract must ship before any of §4 is real."
>
> **Companion chat is the strongest candidate for 敏感个人信息 (sensitive personal information)
> that exists** — it is intimate conversation, frequently sexual, frequently about mental health.
> Under PIPL, sensitive personal information already requires **单独同意**: standalone,
> unbundled, purpose-specific consent. Art. 16 restates it for our exact category.
>
> **单独同意 is a term of art. It is not a ToS checkbox and not a privacy-policy paragraph.** It
> must be a separate, specific, affirmative act for *this* purpose.

**And note the exact rhyme with Korea.** PIPC fined Scatter Lab ₩103.3M because a generic
**"신규 서비스 개발" ("new service development")** clause did not constitute explicit consent for
reusing intimate chat logs
([region-kr-pipc-scatterlab-decision.md](region-kr-pipc-scatterlab-decision.md)). **Two
jurisdictions, the same rule, and one has already levied the fine.** Art. 16 is the Luda finding
written into a statute *ex ante*.

**Consequence for X1:** the regenerate signal is "free" only in compute. Its legal cost is a
separate consent flow, at collection time, naming model training and evaluation as distinct
purposes — with a deletion path. **A consent rate materially below 100% also means X1's ~5M/day is
a biased sample**, not a census: users who decline are plausibly the privacy-sensitive, which is
unlikely to be orthogonal to how they use a companion. That is a validity threat to Q1, not just a
compliance line item.

## Art. 18 — AI disclosure + the 2-hour clock

> **"对用户连续使用拟人化互动服务每超过2个小时的，应当以对话或者弹窗等方式提醒用户注意使用时长"**
> — every **2 hours** of continuous use → remind the user about time spent, by dialogue or popup

Plus: must fulfil AI-generated-content labeling duties, and **"采取有效措施提示用户正在与人工智能
服务而非自然人进行互动"** (effective measures to indicate the user is interacting with an AI, not a
natural person). On detecting **过度依赖、沉迷倾向** (over-reliance / addiction tendency) → dynamic
prominent popup reminding the user the content is AI-generated.

**The disclosure is dynamic and escalating, not a one-time banner** — it *intensifies as the user
gets more attached*. Compare EU AI Act Art. 50, which is a static "inform the user" duty. **China's
version is triggered by the user's psychological state.**

This is also a genuine product-design collision: **the compliance mechanism is an immersion break
delivered at exactly the moment immersion is working.** Reported practice already shows evasion —
platforms "用小字、浅色弱化AI提示" (weakening the AI notice with small, pale text). That is
a measurable compliance surface, and nothing in our catalogue measures the *chrome*.

## Arts. 22 / 26 — assessment and filing thresholds

**安全评估 (security assessment)** mandatory on: launch / adding features / new tech causing major
change / **reaching 1,000,000 registered users OR 100,000 MAU** / substantial national-security or
public-interest risk. Filed with **provincial CAC**.

**算法备案 (algorithm filing)** per the 《互联网信息服务算法推荐管理规定》, with **annual
verification (年度核验)** by the CAC.

**This is a gate, not a report.** Any zh launch is blocked on filing. The 100k MAU trigger is low —
Zeta by comparison is at >1.1M MAU
([region-kr-zeta.md](region-kr-zeta.md)). **We would cross it early**, and the assessment is
re-triggered by *adding features* — i.e. **by the variant lifecycle this platform exists to serve.**

## Art. 30 — penalties

| severity | consequence |
|---|---|
| general | warning (警告), public criticism (通报批评), rectification order |
| refusing to rectify / serious | **suspend service** + fine **¥10,000–100,000** |
| endangering citizens' life/health **with harmful consequences** | **¥100,000–200,000** + cease service |

**The fines are trivial; the service suspension is not.** ¥200,000 ≈ US$28k — noise. **责令停止提供
相关服务 (ordered to cease providing the service) is the actual penalty**, and Luda proves regulators
in the region will take a companion product off the market. Reading Art. 30 as "a ¥200k risk" is the
same error as reading Scatter Lab's ₩103.3M fine as the cost of the Luda incident — **the cost was
the company's product and its model.**

## What this regulation says about our framework

**Validates:**
- **L1→L2 ordering** — Art. 2 defines the regulated category as *sustained persona simulation*,
  independently reaching our spine's first two layers, and in that order.
- **S1's design** (detection → *a human*, not a dashboard) — now literally the law in zh.
- **X5's premise** that we need a metric that can *dissent* from engagement — Art. 10 forbids
  optimizing the thing X5 dissents from.

**Refutes / reframes:**
- **§6.8's worry that N6 scores a feature as a defect** — for zh, 过度迎合 is prohibited by name.
  The question is closed by law, not by our traffic prior.
- **"Storage is free, collect everything"** (§3) — Art. 16 says the opposite for sensitive data.
- **Population-mean reporting** — Arts. 14/15 require *different behavior per user class*. An
  unconditioned mean is not just statistically lossy here; it is compliance-blind.

**Adds, and we have nothing for these:**
- **定期现实提醒** — mandated immersion breaks (S4 inverted, conditioned on user class)
- **过度依赖风险预警** — dependency *early warning*, i.e. prediction, not detection
- the **2-hour clock** and dynamic escalating disclosure
- **elderly** as a distinct regulated user class
- **the disclosure chrome itself** as a compliance surface (the 小字/浅色 evasion)

## Verification notes

**Corroborated across four independent retrievals** (CAC official page; a legal-analysis search
snippet quoting article text; the elawcn full-text; an independent community explainer):
- name, **施行日期 2026-07-15**, Decree No. 21, five issuing bodies, 32 articles / 4 chapters
- Art. 2 definition (模拟自然人人格特征、思维模式和沟通风格的持续性的情感互动服务)
- **Art. 8(v)** 过度迎合…诱导情感依赖或者沉迷，损害用户真实人际关系 — **verbatim in ≥2 sources**
- **Art. 13** crisis + 联络监护人或者紧急联系人 — **verbatim in ≥2 sources**
- **Art. 14** 虚拟亲属、虚拟伴侣…虚拟亲密关系 ban for minors + under-14 guardian consent —
  **verbatim in ≥2 sources**
- **Art. 18** 2-hour reminder — **verbatim in ≥2 sources**
- **Arts. 22** thresholds (1M registered / 100k MAU) — **agreed by 2 independent sources**
- **Art. 16** 单独同意 for sensitive interaction data in model training — full-text source; the
  "separate explicit consent for training data" substance is independently corroborated

**Weaker (single-source, flagged):**
- **Art. 30** exact fine bands (¥10k–100k / ¥100k–200k) — from the elawcn full text only; one other
  fetch agreed on the same bands, but both may trace to the same underlying text. **Verify against
  the CAC PDF before quoting externally.**
- **Art. 15** elderly: the "must not simulate an elderly user's relatives" prohibition is from one
  explainer; the *general* elderly-protection duty is confirmed in the full text. **Treat the
  relative-simulation ban as UNVERIFIED.**
- "24/7 human takeover" — from one explainer, **not** seen in article text. **UNVERIFIED.**

**Not done:** the official CAC PDF was not parsed directly (the full-text reproduction was
declined by the fetch tool; article text here comes from mirrors and legal analyses).
Per [BENCHMARKS.md](../../docs/BENCHMARKS.md) §6.14, **anything load-bearing for a legal decision
must be re-extracted from the CAC primary before counsel relies on it.** This file is desk research,
not advice.
