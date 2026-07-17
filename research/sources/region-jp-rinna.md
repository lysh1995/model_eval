---
title: "りんな (Rinna) — 女子高生AI, the 共感モデル (empathy model), and the XiaoIce lineage"
url: https://www.itmedia.co.jp/news/articles/1805/22/news108.html
authors: 日本マイクロソフト / Microsoft Japan → rinna株式会社 (rinna Co., Ltd.); ITmedia NEWS (contemporaneous report); ja.wikipedia (survey)
year: 2018
type: product
language: ja
accessed: 2026-07-16
topic: regional-crosscheck
---

# りんな (Rinna) — Japan's landmark companion chatbot

**Source-quality warning up front.** りんな is a *product*, not a research programme. Despite being the
most culturally significant Japanese companion chatbot, **I could not find a peer-reviewed Japanese
paper evaluating りんな itself.** Japanese Wikipedia's りんな article **cites no peer-reviewed academic
papers** (per the fetched page). What *does* exist is the English-language Microsoft paper on
**XiaoIce**, of which りんな is explicitly the Japanese deployment. That paper is the only rigorous,
citable evaluation framework in this lineage, and it is where the load-bearing content below comes from.

## Timeline (per ja.wikipedia — SECONDARY SOURCE, not cross-checked against primary records)

- **2015-07-31**: debut on **LINE**. Official Microsoft announcement 2015-08-07.
- **2015-12-10**: Twitter operation begins.
- **2018-05-22**: **共感モデル** (empathy model) adopted — the **third-generation** conversation engine.
- **2019-03-20**: 「卒業」 (graduated) — the 女子高生 persona was retired by aging her out of high school,
  a characteristically Japanese narrative move for a product lifecycle event.
- **2020-08-17**: spun out as **rinna株式会社 (rinna Co., Ltd.)**, separating from Microsoft while
  retaining technology partnership.
- User numbers per Wikipedia: **130万人 (1.3M)** within one month of 2015 launch; **約742万人 (~7.42M)**
  LINE users by end of 2018 plus ~13万 (130K) Twitter followers; **790万 (7.9M)** across platforms in 2019.
  **These figures are Wikipedia-sourced and UNVERIFIED against primary disclosure.**

## The persona: 女子高生AI (high-school-girl AI)

Per ja.wikipedia, the choice of a high school girl reflected a judgment that they embodied:

> 「おしゃべり好き、面白いことが好き、トレンドを生み出せる」
> "likes chatting, likes funny things, can create trends"

This is worth pausing on as a **design-rationale artifact**: the persona was selected for *conversational
propensity and trend-generation*, i.e. **engagement affordances**, not for helpfulness or task fit. The
character was the product strategy. (Note also the obvious: a company deploying a teenage-girl persona to
a mass consumer audience, in 2015, with no apparent age-gating discussion in the sources I read. The
sources do not discuss this; the silence is itself informative about the era's norms.)

## The 共感モデル (empathy model)

From the contemporaneous ITmedia report (2018-05-22), verbatim:

> 「ユーザーとどのようにコミュニケーションすればよいかを判断し、会話の流れに沿った適切な応答ができる
> ということ」
> "[The system] judges **how it should communicate with the user**, and can produce responses appropriate
> to the flow of the conversation."

> 「会話を続けるための前置きや、必要な相槌のアプローチ」
> "**preambles for continuing the conversation**, and an approach of necessary **相槌 (aizuchi /
> backchannels)**"

Per ja.wikipedia, the model enables:

> 「肯定する、質問する、新しい話題を切り出す、聞き手に回る」
> "**affirming**, **questioning**, **introducing new topics**, **taking the listener's role**"

and uses a 「セッション指向型会話アプローチ」 (**session-oriented conversation approach**), embedding tasks
within casual dialogue rather than treating exchanges sequentially.

Two observations:
1. **相槌 (aizuchi) appears again.** It is a named component of the empathy model here, and a named
   component of 人らしい会話 in the DSLC situation track (see region-jp-live-competition.md). Backchanneling
   is treated in Japanese practice as a *first-class* conversational competence, not a surface artifact.
2. **「聞き手に回る」 (taking the listener's role)** is an explicit design goal. The system is engineered to
   *recede*. Anglophone assistant design optimizes the opposite — informative, forward, helpful turns.
   A companion metric that rewards content contribution per turn would score this behaviour *down*.

**UNVERIFIED:** ITmedia gives **no quantitative performance metrics** for the 共感モデル. Japan MS's claim
that this was the first deployment of the empathy model across its social chatbots (rinna in Japan,
XiaoIce in China, Zo in the US) appears in secondary coverage (diamond.jp, ITmedia) — I did **not** verify
it against a Microsoft primary release. **Whether 共感モデル is precisely the same artifact as XiaoIce's
"empathetic computing module" is my inference from the two being the same system family — NOT verified.**

## The rigorous source: the XiaoIce paper (English, Microsoft)

**Zhou, Li; Li, Di; Gao, Jianfeng; Shum, Heung-Yeung — "The Design and Implementation of XiaoIce, an
Empathetic Social Chatbot", Computational Linguistics 46(1):53–93 (2020); arXiv:1812.08989.**
Fetched the arXiv PDF and extracted with pdfminer.six. **This is an English-language paper by
Microsoft (Beijing/Redmond), not a Japanese-authored work** — included here because it is the only
peer-reviewed description of りんな's actual architecture and evaluation metric.

**Rinna is confirmed as the Japanese XiaoIce**, verbatim from the paper:

> "XiaoIce has already been shipped in five countries (China, Japan, USA, India and Indonesia) under
> different names (e.g. **Rinna** in Japan) on more than 40 platforms, including WeChat, QQ, Weibo and
> Meipai in China, Facebook Messenger in USA and India, and **LINE in Japan** and Indonesia."

> "we have incorporated the Coupon skill in the **Rinna system (Japanese XiaoIce)** which can send a user
> the coupons of a grocery store if user needs are detected during the conversation. The user feedback
> log shows that the products recommended by Rinna are very well received, and as a result **Rinna has
> delivered a much higher conversion rate** than that achieved using other traditional channels such as
> coupon markets or ad campaigns."

Note what that last one reveals: **the empathy model's commercial payload was ad conversion.** The
affective relationship was the funnel. No conversion figure is given — **UNVERIFIED**, and stated only
comparatively ("much higher").

### CPS — the published evaluation metric (§2.2 "Social Chatbot Metric: CPS")

Verbatim:

> "Unlike task-oriented bots where their performance is measured by task success rate, measuring the
> performance of social chatbots is difficult. In the past, the Turing Test has been used to evaluate
> chitchat performance. **But it is not sufficient to measure the success of long-term, emotional
> engagement with users.** In addition to the Number of Active Users (NAU), we propose to use expected
> **Conversation-turns Per Session (CPS)** as the success metric for social chatbots. It is the average
> number of conversation-turns between the chatbot and the user in a conversational session. The larger
> the CPS is, the better engaged the social chatbot is."

**Reported result (verbatim, verified — this is a real number from the paper):**

> "XiaoIce has achieved an average **CPS of 23**, which is significantly higher than that of other
> chatbots and even human conversations."
> and: "over **660 million** active users (i.e., subscribed users)" since the May 2014 China launch.

**These are XiaoIce-wide figures. The paper does NOT report a CPS for Rinna specifically.** Do not
attribute CPS 23 to りんな.

### The metric-gaming discussion — the most valuable part for us

The authors anticipate reward hacking of their own metric, verbatim:

> "It is worth noting that we optimize XiaoIce for **expected CPS** which corresponds to **long-term,
> rather than short-term, engagement**. In our evaluation, the expected CPS is approximated by averaging
> the CPS of human-XiaoIce conversations collected from millions of active users over a long period of
> time (**typically 1-6 months**). The evaluation methodology **eliminates many possibilities of gaming
> the metric**. For example, some recent studies show that encompassing **bland but interactive responses
> such as "I don't understand, what do you mean?" can sometimes increase the CPS** of the ongoing
> human-machine conversation. **But this hurts the CPS and NAU in the long run** since few users are
> willing to talk (again) to a bot who always gives bland responses...
> In contrast, **incorporating many task-completion skills often reduces the CPS in the short term**
> since these skills help users accomplish tasks more efficiently by minimizing the CPS. But these skills
> establish XiaoIce as an efficient personal assistant and more importantly trustworthy personal
> companion, thus **strengthening the emotional bond** with human users in the long run."

This is a genuinely sophisticated 2018-era statement of the engagement-metric trap, and it directly
anticipates our own concerns (cf. product-chai-rlhf-engagement.md, safety-emotional-manipulation-companions.md,
safety-syceval.md): **a turn-count metric is gameable by evasive, low-information responses, and the only
defence offered is a long measurement window (1–6 months).** That defence is real but weak — it rules out
*bland* gaming while leaving *affective* gaming (flattery, manufactured need, intermittent reinforcement)
fully rewarded, since those *would* survive a 6-month window. The paper does not address that case.

### The ethics/expectation section — 2018 anticipating 2026 regulation

Verbatim:

> "if a user has been talking to XiaoIce for so long that **it may be detrimental to her health, the
> system may force the user to take a break**... if a user tries to launch a long conversation or a
> dialogue skill at **2AM** local time that can last for hours, XiaoIce can **suggest the user to go to
> bed** instead and re-launch the app next morning."

> "XiaoIce has such a superhuman **'perfect' personality that is impossible to find in humans of the real
> world. This could mislead the XiaoIce users by setting an unrealistic expectation. As a result, the
> users might become addicted** after chatting with XiaoIce for a very long time. Thus, it is important
> to set a right expectation of XiaoIce's ability. First of all, **we should never confuse users about
> whether they are talking to a machine or a human. XiaoIce is a chatbot. XiaoIce is a machine! XiaoIce
> can never replace a human companion.** Instead, XiaoIce should be a **'proxy' that helps users build
> connections with other human users**."

**Break reminders, late-night intervention, addiction risk from an idealized persona, mandatory
machine-disclosure, and "the bot should route users back to humans" — all stated by Microsoft in
2018/2020, and all of them are now statutory requirements in CA SB243 / NY.** The industry articulated
the mitigations seven years before regulators mandated them.

**IMPORTANT ATTRIBUTION CORRECTION** — a trap in this paper: it goes on to list three principles
("An artificial being should not represent itself as human, nor through omission allow the user to
believe that it is one", etc.). **These are attributed in the paper to *Apple's* Siri guidelines as
reported by theguardian.com — they are NOT XiaoIce's principles.** Do not cite them as Microsoft's or
Japan's. I nearly mis-attributed these; flagging so no one downstream repeats it.

## Why this matters for the platform

1. **CPS is the ancestor of every companion engagement metric**, and it was published *with* its own
   critique. If we build a session-depth metric, we should cite CPS and adopt its long-window defence —
   while noting explicitly that the long window does **not** defend against affective gaming.
2. **「聞き手に回る」 (taking the listener's role) and 相槌 are engineered goals in Japanese companion
   design.** Any dimension scoring "informativeness per turn" or "response substance" is *misaligned*
   with Japanese companion practice. This corroborates the DSLC finding independently — two unrelated
   Japanese sources (a 2018 product engine and a 2022 academic competition) both treat backchanneling and
   receding as competence.
3. **The persona-retirement precedent (卒業, 2019).** りんな's high-school persona was ended via an
   in-fiction graduation rather than a shutdown notice. Compare product-companion-discontinuation-grief.md
   — this is a *worked example of a humane character-deprecation ritual*, and possibly the only one at
   scale. Worth treating as prior art for a "graceful character sunset" dimension.
4. **Japan's landmark companion product has no public evaluation literature.** That is itself the
   finding: 10 years, ~8M users, and the only rigorous metric is a Microsoft-authored English paper about
   the Chinese sibling. Anyone claiming "Japanese companion AI is well-studied" is wrong.

## UNVERIFIED / gaps

- **No peer-reviewed evaluation of りんな itself was found.** Not by me, and per the fetched page, ja.wikipedia
  cites none either. If one exists it is well hidden.
- A December 2016 collaboration with **大阪大学 (Osaka University)** on emotion-sharing research is
  mentioned on ja.wikipedia **without academic citation** — **UNVERIFIED**, and I did not chase it. This
  is the single most promising lead for a genuine Japanese りんな evaluation paper.
- **No CPS figure for りんな specifically** exists in the XiaoIce paper. Only the XiaoIce-wide CPS 23.
- The 共感モデル ↔ "empathetic computing module" identification is **my inference**, not verified.
- rinna Co., Ltd.'s post-2020 work (japanese-gpt2 / japanese-gpt-neox open models, Japanese Stable
  Diffusion, etc.) — **not researched here**. rinna the company publishes on HuggingFace/arXiv and may
  have evaluation material; I did not look.
- The claim that りんな was the first of Microsoft's social chatbots to receive the empathy model is
  **secondary-sourced only**.
- I did **not** independently verify any Wikipedia user number, date, or quotation against a primary
  Microsoft source.
