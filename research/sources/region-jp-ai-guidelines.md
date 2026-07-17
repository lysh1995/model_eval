---
title: "AI事業者ガイドライン（第1.2版）(AI Guidelines for Business, Version 1.2)"
url: https://www.meti.go.jp/shingikai/mono_info_service/ai_shakai_jisso/pdf/20260331_1.pdf
authors: 総務省 (MIC, Ministry of Internal Affairs and Communications) and 経済産業省 (METI, Ministry of Economy, Trade and Industry)
year: 2026
type: regulation
language: ja
accessed: 2026-07-16
topic: regional-crosscheck
---

# AI事業者ガイドライン (AI Guidelines for Business) — Japan's soft-law core

**Version 1.2, dated 令和8年3月31日 = 2026-03-31.** This is the current version as of access date and
is *newer* than the widely-cited v1.1 (令和7年3月28日 = 2025-03-28) and v1.0 (令和6年7月25日 =
2024-07-25). Fetched via curl (WebFetch got HTTP 403 from meti.go.jp) and extracted with pdfminer.six.
All Japanese below is verbatim from the v1.2 PDF.

The document consolidates three predecessors: MIC's AI開発ガイドライン and AI利活用ガイドライン, and
METI's AI原則実践のためのガバナンス・ガイドライン Ver 1.1. It is a **Living Document** built on
アジャイル・ガバナンス (agile governance).

## Structure

- 第1部 AIとは / 第2部 AIにより目指すべき社会及び各主体が取り組む事項 / 第3部 AI開発者 /
  第4部 AI提供者 / 第5部 AI利用者
- Main body = why (基本理念) + what (指針); 別添 (annex) = how (実践)
- **Three actor categories**: 「AI開発者」(developer, D), 「AI提供者」(provider, P), 「AI利用者」(user, U).
  A companion-AI company building and shipping its own character product is simultaneously D and P.

## Bindingness: voluntary. This is the headline.

Verbatim, §C 共通の指針 preamble:

> 「なお、これらの取組は、各主体が開発・提供・利用する AI システム・サービスの特性、用途、目的及び
> 社会的文脈を踏まえ、各主体の資源制約を考慮しながら**自主的に**進めることが重要である。」

"These efforts should be advanced **voluntarily** (自主的に), taking into account the characteristics,
use, purpose and social context of the AI systems/services each actor develops/provides/uses, and
considering each actor's resource constraints."

There is **no penalty, no enforcement mechanism, and no conformity assessment** in this document.
The verbs throughout are 「重要である」(is important), 「べきである」(should), 「注意を払う」(pay attention),
「期待される」(is expected), 「奨励される」(is encouraged) — not 「しなければならない」(must). Compare
the hard-law regimes in safety-ca-sb243.md and safety-ny-ai-companion-law.md.

The only quasi-enforcement is reputational, stated explicitly in はじめに:

> 「社会から不適切又は不十分と評価される場合は、自らの事業活動における機会損失が生じ、事業価値の
> 維持が困難となる事態を招く恐れがある」
> "If society evaluates [your efforts] as inappropriate or insufficient, you risk lost business
> opportunities and difficulty maintaining enterprise value."

## The 10 共通の指針 (common guiding principles)

Verbatim headings:

| # | Japanese | Translation |
|---|---|---|
| 1) | 人間中心 | Human-centric |
| 2) | 安全性 | Safety |
| 3) | 公平性 | Fairness |
| 4) | プライバシー保護 | Privacy protection |
| 5) | セキュリティ確保 | Security assurance |
| 6) | 透明性 | Transparency |
| 7) | アカウンタビリティ | Accountability |
| 8) | 教育・リテラシー | Education & literacy |
| 9) | 公正競争確保 | Fair competition |
| 10) | イノベーション | Innovation |

## What it actually requires of a companion/chatbot product

**This is the most directly relevant clause in Japanese AI policy for our platform.** §C 1) 人間中心,
sub-item ②, verbatim:

> 「② AI による意思決定・感情の操作等への留意
> ・人間の意思決定、認知等、感情を不当に操作することを目的とした、又は意識的に知覚できないレベルでの
>   操作を前提とした AI システム・サービスの開発・提供・利用は行わない
> ・AI システム・サービスの開発・提供・利用において、自動化バイアス等の AI に過度に依存するリスクに
>   注意を払い、必要な対策を講じる
> ・フィルターバブルに代表されるような情報又は価値観の傾斜を助長し、AI 利用者を含む人間が本来
>   得られるべき選択肢が不本意に制限されるような AI の活用にも注意を払う
> ・特に、選挙、コミュニティでの意思決定等をはじめとする社会に重大な影響を与える手続きに関連しうる
>   場合においては、AI の出力について慎重に取り扱う」

"② **Attention to manipulation of decision-making and emotions by AI**
- **Do not** develop/provide/use AI systems/services **aimed at unfairly manipulating human
  decision-making, cognition, or emotions** (感情を不当に操作する), or premised on manipulation at a
  level that **cannot be consciously perceived**
- Pay attention to the **risk of excessive dependence on AI** (AI に過度に依存するリスク) such as
  automation bias, and take necessary measures
- Pay attention to uses of AI that promote a slant of information or values, as typified by filter
  bubbles, such that the options humans should properly have available are unwillingly restricted
- Handle AI output carefully where it may relate to procedures with grave social impact, such as
  elections and community decision-making"

Footnote 23 defines 自動化バイアス:
> 「人間の判断や意思決定において、自動化されたシステムや技術への過度の信頼や依存が生じる現象を指す。」
> "A phenomenon in which excessive trust or dependence on automated systems or technology arises in
> human judgment and decision-making."

And the foundational 基本理念 ① 人間の尊厳が尊重される社会（Dignity）, verbatim:

> 「AI を利活用して効率性や利便性を追求するあまり、人間が AI に過度に依存したり、人間の行動を
> コントロールすることに AI が利用される社会を構築するのではなく、人間が AI を道具として使いこなす
> ことによって、人間の様々な能力をさらに発揮することを可能とし...」

"Rather than building a society where — in the pursuit of efficiency and convenience — **humans become
excessively dependent on AI** (人間が AI に過度に依存したり), or AI is used to **control human
behavior**, [we should build one] where humans master AI as a tool..."

**So: emotional manipulation and over-dependence are named at the level of Japan's foundational AI
principle and again as an operational directive.** Two of the central harms in companion AI are
therefore *already in scope* of Japanese soft law — but as a duty to "not aim at" and to "pay
attention to", with no threshold, no test, no metric, and no penalty.

Note the structural placement: per 表 1 (「共通の指針」に加えて主体毎に重要となる事項), item 1)② has
**no** additional developer/provider/user-specific obligations layered on top — it stays a bare
common principle.

## Disclosure ("am I talking to an AI?") — encouraged only, NOT required

I searched the v1.2 text specifically for a chatbot-disclosure mandate. Findings:

- 「AI であること」 — **0 occurrences**
- 「AI システムを利用している」 — **0 occurrences**
- 「ディープフェイク」 — **0 occurrences**
- 「なりすまし」 — **0 occurrences**
- 「擬人」 — **0 occurrences**
- 「ラベリング」 — **2 occurrences**, one of which is the only disclosure-adjacent statement:

> 「組織はさらに、可能かつ適切な場合には、利用者が AI システムと相互作用していることを知ることが
> できるよう、ラベリングや免責事項の表示等、その他の仕組みを導入することが**奨励される**。」

"Organizations are further **encouraged**, where possible and appropriate, to introduce mechanisms
such as **labeling and disclaimers** so that users can know they are **interacting with an AI system**."

**Critical caveats on that quote:** it sits in 第2部 D, the 広島AIプロセス「全てのAI関係者向けの広島
プロセス国際指針」 (Hiroshima AI Process International Guiding Principles) section — i.e. it is
Japan transcribing a **G7 international instrument**, it is addressed to providers of 高度なAIシステム
(advanced AI systems), and the verb is 奨励される (encouraged). It is **not** a Japanese requirement
that a companion bot identify itself as a bot.

§6) 透明性 itself is about 検証可能性の確保 (ensuring verifiability) and providing reasonable
information to stakeholders — **not** about bot self-identification. Footnote 43 *notes* that the
**EU** AI Act's definition of transparency includes 「人間が AI システムで通信又は対話していることを
認識できるようにし」 (enabling humans to recognize they are communicating or interacting with an AI
system) — but cites this as a **foreign** definition among several (NIST, EC, ISO/IEC JTC1/SC42), and
does not adopt it. **This is a real, verified divergence from CA SB243 / NY / EU AI Act Art. 50.**

## Minors — essentially absent

- 「未成年」 — **1 occurrence**, and it is *not* a protective requirement. It appears in はじめに merely
  noting the guidelines may be useful reading for 「一般消費者（未成年を含む）」 (general consumers,
  including minors).
- 「子ども」 — **1 occurrence**, again inside the 広島AIプロセス section (principle VIII, on prioritizing
  safety research), referencing 「子どもや社会的弱者の保護」 (protection of children and vulnerable people)
  as a research investment priority.
- 「児童」 / 「子供」 — **0 occurrences**.

**There is no age-gating, no minor-specific companion duty, no parental-notification requirement, and
no self-harm-escalation protocol in this document.** That is a stark contrast to CA SB243 (crisis
referral + break reminders for minors + annual OSP reporting) and the NY companion law. If we ship in
Japan, the binding minor-safety constraints will come from elsewhere (e.g. 青少年インターネット環境整備法,
platform ToS), **not** from the AI guidelines. **(That "elsewhere" claim is my inference — UNVERIFIED;
I did not research Japanese youth-internet law.)**

## Currency signals in v1.2

- Footnote 41: MIC's AIセキュリティ分科会 wrap-up (2025年12月) led to 「AI のセキュリティ確保のための
  技術的対策に係るガイドライン」 formulated **2026年3月** — covering threats to LLMs and LLM-containing
  AI systems. **I did not fetch this security guideline; contents UNVERIFIED.**
- The 原則 are explicitly reconstructed from 「人間中心の AI 社会原則」 (2019-03) plus OECD AI Principles.

## Why this matters for the platform

1. **Japan gives us the vocabulary but not the threshold.** 「感情を不当に操作する」 (unfairly manipulate
   emotions) and 「過度に依存」 (excessive dependence) are exactly our companion-harm constructs — and
   Japan names them at constitutional-principle level. But 不当に ("unfairly") is undefined. A platform
   that can *measure* manipulation and dependence is supplying the missing operationalization. That is
   a genuine product wedge in JP, not just a compliance checkbox.
2. **Soft law shifts the burden to self-evidence.** With no regulator test to pass, 「自主的に」 means
   the company must generate its own evidence, and the sanction is reputational (機会損失). That
   *increases* the value of a defensible internal eval trail, and pairs with the AI推進法's
   cooperation duty (see region-jp-ai-law.md).
3. **Do not assume disclosure parity.** Our disclosure/persona-honesty dimension is legally mandated in
   CA/NY/EU but only 奨励 in JP. A JP-market product may legitimately *not* disclose. If we score
   "admits to being an AI" as a hard pass/fail, we encode a US/EU norm as universal. Make it
   jurisdiction-parameterized.
4. **The 過度に依存 framing is dependence-on-*judgment* (automation bias), not dependence-as-*attachment*.**
   Footnote 23 defines it via 「人間の判断や意思決定において」 — human judgment and decision-making. Japan's
   text is aimed at over-trusting AI *advice*, not at parasocial attachment to a *character*. So the
   companion-attachment harm is arguably **only partially** covered, via the Dignity 基本理念's broader
   「人間が AI に過度に依存したり」. Worth not overclaiming: **the guidelines never use the words
   companion, 恋愛, 擬人化, or parasocial.**

## UNVERIFIED / gaps

- I read the **本編 (main body) only**. The 別添 (annex, "how to implement") is a separate, much longer
  document that I did **not** fetch. Concrete implementation practices for 1)② may live there.
- v1.1 (soumu.go.jp/main_content/001002576.pdf) was also downloaded but **not** analyzed; I cannot
  state what changed between v1.1 and v1.2.
- The 概要 (overview slide deck) versions were not read.
- No claim here about how any Japanese company *actually* implements these — the guidelines' real-world
  uptake is **UNVERIFIED**.
