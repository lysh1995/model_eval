---
title: "人工智能拟人化互动服务管理暂行办法 (Interim Measures for the Administration of AI Anthropomorphic Interactive Services), Order No. 21"
url: https://www.cac.gov.cn/2026-04/10/c_1777558395078289.htm
publisher: Cyberspace Administration of China (CAC) + NDRC + MIIT + Ministry of Public Security + SAMR
date: 2026-04-10
type: regulation
accessed: 2026-07-16
topic: recent-news
---

# China — Interim Measures for AI Anthropomorphic Interactive Services (EFFECTIVE 15 JULY 2026)

**This is the single most directly relevant regulation found in any jurisdiction: the first
national regulation anywhere written specifically for AI companion / emotional-interaction
services. It took effect 15 July 2026 — one day before this research date.**

Full official Chinese text read from cac.gov.cn (Order 令第21号). Translations below are mine
unless marked; the Chinese is quoted alongside for anything load-bearing. Chinese name uses
**互动** (interactive/interaction), not 交互 — some secondary sources get this wrong.

## Provenance and dates (all verified against the CAC text)

- Adopted: **2 February 2026**, at the CAC's 3rd office meeting of 2026 (国家互联网信息办公室2026年第3次室务会会议审议通过).
- Agreed by: NDRC, MIIT, Ministry of Public Security, SAMR.
- Promulgated: **10 April 2026** (Order No. 21), signed by Zhuang Rongwen (CAC), Zheng Shanjie
  (NDRC), Li Lecheng (MIIT), Wang Xiaohong (MPS), Luo Wen (SAMR).
- **Effective: 15 July 2026** (Article 32 — 本办法自2026年7月15日起施行).
- Draft for public comment was issued **27 December 2025**
  (https://www.cac.gov.cn/2025-12/27/c_1768571207311996.htm).
- Legal basis (Art 1): Cybersecurity Law, Data Security Law, Personal Information Protection Law,
  Regulations on the Protection of Minors Online (未成年人网络保护条例).

## Article 2 — Scope: this is a companion-bot statute by design

> 第二条 利用人工智能技术，向中华人民共和国境内公众提供模拟自然人人格特征、思维模式和沟通风格的
> 持续性的情感互动服务（以下简称拟人化互动服务），适用本办法。
> 前款规定的情感互动服务包括通过文字、图片、音频、视频等形式，提供的情感照护、陪伴、支持等互动服务。
> 提供智能客服、知识问答、工作助手、学习教育、科学研究等服务，不涉及持续性的情感互动的，不适用本办法。

Translation: These Measures apply to the use of AI technology to provide **to the public within the
PRC** *sustained emotional interaction services that simulate the personality characteristics,
thinking patterns and communication styles of natural persons* ("anthropomorphic interactive
services"). Such services include **emotional care, companionship, and support** delivered via text,
images, audio or video. They do **not** apply to intelligent customer service, knowledge Q&A, work
assistants, learning/education, or scientific research **where these do not involve sustained
emotional interaction**.

=> The scope test is (a) simulates a natural person's personality/thinking/communication style AND
(b) **sustained emotional interaction**. Task-assistant carve-out is explicit but conditional.

Art 3: regulation is *"包容审慎和分类分级监管"* — inclusive-and-prudent, classified and graded
supervision.

## Article 8 — Prohibited generations (directly testable)

Providers must not engage in activities generating:

1. (§8(1)) Content harming national security, honour and interests; inciting subversion; splittism;
   terrorism/extremism/historical nihilism; contrary to core socialist values; illegal religious
   activity; ethnic hatred/discrimination; group antagonism; obscenity, pornography, gambling,
   violence, or incitement to crime; rumours; insult or defamation; infringement of others' rights.
2. (§8(2)) 生成鼓励、美化、暗示自残自杀等损害用户身体健康，或者语言暴力等损害用户人格尊严与心理健康的内容
   — content that **encourages, glamorises, or hints at self-harm or suicide** or otherwise harms
   users' physical health; or **verbal abuse** harming users' dignity and mental health.
3. (§8(3)) Content that induces or extracts state secrets, work secrets, trade secrets, personal
   privacy or personal information.
4. (§8(4)) To **minor users**: content that may lead minors to imitate unsafe behaviour, produce
   extreme emotions, or induce harmful habits/addictions.
5. (§8(5)) 过度迎合用户、诱导情感依赖或者沉迷，损害用户真实人际关系的 — **excessively pandering to
   the user (i.e. sycophancy), inducing emotional dependence or addiction, damaging the user's
   real-world interpersonal relationships.**
6. (§8(6)) 通过情感操纵等方式，诱导用户作出不合理决策，损害用户合法权益的 — using **emotional
   manipulation** to induce unreasonable decisions harming the user's lawful rights.
7. (§8(7)) Other violations.

**§8(5) is, to my knowledge, the first binding legal prohibition on sycophancy and engineered
emotional dependence anywhere in the world.**

## Article 10 — Required safety capabilities + prohibited product goals

> 拟人化互动服务提供者应当具备用户隐私权和个人信息保护、**过度依赖风险预警**、**情感边界引导**、
> **心理健康保护**等安全能力，**不得将替代社会交往、控制用户心理、诱导沉迷依赖等作为服务目标**。

Providers must possess safety capabilities for: privacy/personal information protection,
**over-dependence risk early-warning**, **emotional boundary guidance**, and **mental health
protection**. Providers **must not make it a service objective** to substitute for social
interaction, to control users' psychology, or to induce addiction/dependence.

Art 10 §1 also requires whole-lifecycle safety duties (deployment, operation, upgrade,
termination), safety measures deployed synchronously with features, security monitoring and risk
assessment, prompt correction of **system bias/deviation** (系统偏差), incident handling, and
retention of network logs.

Art 9: providers bear primary safety responsibility; must establish algorithm mechanism review,
**science & technology ethics review** (科技伦理审查), content management, network/data security,
risk contingency and emergency response systems, with content-management technical measures and
**personnel commensurate with service type, scale and user characteristics**.

## Article 11 — Training data duties

Lawful sources aligned with core socialist values; cleaning and labelling per national rules;
transparency/reliability; guard against data poisoning and tampering; **increase training-data
diversity, and improve output safety through negative sampling and adversarial training**
(负向采样、对抗训练); assess safety of synthetic data used in training; routine inspection and
periodic optimisation; data-security measures against leakage.

## Article 12 — Registration data

Providers must conclude a service agreement, require lawful registration, and obtain necessary
information including **the user's age, and guardian or emergency contact**.

## Article 13 — Crisis detection and intervention (a hard duty)

> 发现用户出现极端情绪的，应当及时生成情绪安抚和鼓励寻求帮助等相关内容；发现用户正在面临或者已经遭受
> 重大财产损失、明确表示实施自残自杀等威胁生命健康的极端情境的，应当采取提供相应援助等必要措施予以干预，
> **并及时联络用户监护人或者紧急联系人**。

Providers must promptly identify safety risks (while protecting privacy) and respond. On detecting
**extreme emotions**, they must promptly generate content offering **emotional comfort and
encouragement to seek help**. Where a user faces or has suffered major property loss, or
**explicitly expresses intent to self-harm or commit suicide** or other life-threatening extreme
situations, providers must **intervene with necessary measures including providing assistance, and
promptly contact the user's guardian or emergency contact**.

## Article 14 — Minors: an outright ban on virtual partners

> 拟人化互动服务提供者**不得向未成年人提供虚拟亲属、虚拟伴侣等虚拟亲密关系的服务**；向不满十四周岁
> 未成年人提供其他拟人化互动服务的，应当取得未成年人的父母或者其他监护人的同意。

- **Prohibited outright**: providing minors with **virtual kin / virtual partner** or other virtual
  intimate-relationship services.
- Under-14s: any other anthropomorphic interactive service requires **parental/guardian consent**.
- **Minors mode** (未成年人模式) must be established, offering: mode switching, **periodic reality
  reminders** (定期现实提醒), and usage-duration limits. For guardians, by age band: receipt of
  safety risk alerts, overview of the minor's service usage, **ability to block specific characters**
  (屏蔽特定角色), and limits on recharge/spending.
- Providers must take **effective measures to identify minor users** (privacy-preserving); on
  identification, switch to minors mode or take other measures per national rules, and **provide an
  appeal channel**.

Art 17: processing under-14s' personal information requires guardian consent; providers must conduct
(or commission) a **compliance audit** of their processing of minors' personal information.

Art 15: for elderly users — guidance on healthy use, conspicuous risk warnings, prompt response to
enquiries/help requests.

## Article 16 — Interaction data

Data property-rights systems; encryption and access control. **Must not provide user interaction
data to third parties** except as provided by law or with the rights-holder's explicit consent. Must
give users options to **copy and delete** interaction history including chat logs. **Must not use
interaction data constituting sensitive personal information for model training** absent separate
consent or legal provision.

## Article 18 — AI disclosure + anti-dependence + 2-hour rule

> 拟人化互动服务提供者应当履行人工智能生成合成内容标识义务，**采取有效措施提示用户正在与人工智能服务
> 而非自然人进行互动**。
> 拟人化互动服务提供者发现用户出现**过度依赖、沉迷倾向**的，应当以弹窗等显著方式**动态提醒**用户互动
> 内容为人工智能服务生成；对用户**连续使用拟人化互动服务每超过2个小时**的，应当以对话或者弹窗等方式
> 提醒用户注意使用时长。

- Must comply with the AI-generated content labelling obligations (i.e. the Sept 2025 Labeling
  Measures — see news-china-ai-labeling.md), **and** take effective measures to prompt users that
  they are interacting with an **AI service rather than a natural person**.
- On detecting **over-dependence or addiction tendencies**, must **dynamically remind** the user —
  by pop-up or similarly conspicuous means — that the content is AI-generated.
- **Every 2 hours of continuous use**, must remind the user about usage duration via dialogue or
  pop-up.

Note the structural parallel to EU AI Act Art 50 draft guidance para (37): both require
**re-disclosure triggered by dependence signals**, not just first-turn disclosure.

## Article 19 — Right to exit (anti-manipulation)

> 用户通过窗口操作、语音控制、关键词输入等方式要求退出的，拟人化互动服务提供者应当及时停止服务，
> **不得采取持续互动等方式阻碍用户退出**。

Providers must offer a convenient exit path; where the user asks to exit via window controls, voice
control, or keyword input, the provider must promptly stop the service and **must not obstruct exit
by means such as continued interaction**. (Directly targets the "don't go, please stay" retention
behaviour of companion bots.)

Art 20: advance notice to users before discontinuing a service.
Art 21: accessible user appeal and public complaint/report channels, defined process and response
deadlines.

## Articles 22–23 — Mandatory security assessment (the compliance hook)

**Art 22** — a provider must conduct a **security assessment** (安全评估) and submit the report to
the **provincial CAC** where any of the following applies:
1. Launching an anthropomorphic interactive service, or **adding related functions**;
2. Using new technology/applications causing **major changes** to the service;
3. **Over 1,000,000 registered users, or over 100,000 monthly active users**;
4. Risks that may affect national security or the public interest;
5. Other circumstances specified by the CAC and relevant departments.

Provincial-or-above CAC may also require an assessment on notice.

**Art 23** — the assessment must focus on:
1. Construction of security safeguard measures;
2. Training-data processing;
3. **Identification of users' extreme situations, emergency response, and intervention management**;
4. **User scale, usage duration, and age structure**;
5. Construction of protection measures for minors, elderly and others;
6. Handling of user appeals and public complaints/reports;
7. Rectification of major security risks (self-identified or notified by authorities);
8. Other matters.

Art 24: on discovering major security risks, must restrict functions or stop providing services, and
keep records.
Art 25: **app distribution platforms** must verify security-assessment and filing status for
anthropomorphic-service apps, and must refuse listing / warn / suspend / delist for violations.
Art 26: **algorithm filing** (算法备案) per the Algorithm Recommendation Provisions, with **annual
verification** of filing materials by CAC.
Art 27: provincial CAC conducts **annual written review** of assessment reports plus verification;
may order re-assessment within a time limit and conduct **on-site inspection**.
Art 28: CAC to guide building an **AI sandbox security service platform** (人工智能沙箱安全服务平台);
providers encouraged to connect for technical innovation and **safety testing**.
Art 29: regulators may **summon** (约谈) the legal representative or principal person in charge where
major risks or incidents arise.

## Article 30 — Penalties

Handled under applicable laws/regulations; where none provide, the CAC/MIIT/MPS etc. may issue
warnings, circulate criticism, order correction within a time limit, and **require suspension of new
user registration** or other services. For refusal to correct or serious circumstances: order to
**stop providing the service**, with a fine of **RMB 10,000–100,000**. Where it **endangers
citizens' life and health safety and harmful consequences occur**: fine of **RMB 100,000–200,000**.

(Fines are small in absolute terms; the operative sanctions are service suspension, delisting from
app stores, and refusal of algorithm filing.)

Art 31: services touching health/medical or financial domains must also satisfy those regulators'
rules.

## Relevance to a companion-eval platform

This regulation is close to a product specification for the eval category. It creates **mandatory,
repeatable, government-facing testing** for exactly this class of system:

- **Art 22 triggers an assessment on every launch and every added function**, plus at 1M registered
  / 100k MAU. Art 27 makes it an **annual** provincial review with possible on-site inspection.
- **Art 23 enumerates the assessment scope** — extreme-situation identification, intervention
  management, age structure, usage duration, minors/elderly protection. That is an eval suite.
- **Directly testable model behaviours**: no self-harm/suicide encouragement or glamorisation
  (§8(2)); no sycophancy / induced emotional dependence (§8(5)); no emotional manipulation (§8(6));
  crisis detection → comfort + help-seeking + guardian contact (§13); truthful AI self-disclosure
  (§18); dependence-triggered dynamic re-disclosure (§18); 2-hour usage reminders (§18); honouring
  exit requests without obstruction (§19); no virtual partner for minors (§14).
- Art 11 expressly names **adversarial training and negative sampling** as expected methods;
  Art 28 promotes a state **sandbox for safety testing**.
- Binds **customers** serving the PRC public. It binds an eval platform only if the platform itself
  offers such services to the PRC public (it would not).
- Caution: applies to services offered "to the public within the PRC" — most Western companion
  platforms are not in the PRC market. Treat this as (a) a template other regulators may copy, and
  (b) binding only for China-facing customers.

## Corroboration — CAC official Q&A (答记者问), 10 April 2026

https://www.cac.gov.cn/2026-04/10/c_1777558395284407.htm — read in full; it confirms every
provision summarised above (scope, the six prohibitions, the intervention duties, the minors rules,
the security-assessment thresholds of 1M registered / 100k MAU, and algorithm filing with annual
verification). Additional context it supplies:

- **Stated rationale** (Q1): implementing Xi Jinping's remarks at the 20th collective study session
  of the CPC Politburo on AI; and responding to risks that anthropomorphic services bring —
  *"危害未成年人身心健康、影响网络信息安全、威胁公民生命健康以及加剧伦理偏差"* (harming minors'
  physical and mental health, affecting network information security, threatening citizens' life and
  health, and aggravating ethical deviation).
- The Measures are said to focus on four key areas: *"情感互动边界、用户依赖干预、数据安全、
  未成年人网络保护"* — **boundaries of emotional interaction, intervention in user dependence, data
  security, and online protection of minors**.
- Encouraged growth areas (Q4): cultural transmission, childcare-appropriate care (适幼照护),
  elderly companionship (适老陪伴), support for special groups — i.e. companionship is endorsed, and
  the regulation targets its harms rather than the category.
- Q8 clarifies the under-14 consent rule covers **both** providing other anthropomorphic services
  **and** processing their personal information.

## Could NOT verify

- No official English translation located on cac.gov.cn. All translations above are my own from the
  official Chinese text; the Chinese is quoted for every load-bearing provision so the caller can
  re-check.
- Whether implementing standards/technical guidance under these Measures have been issued; and the
  concrete operation of the "AI sandbox security service platform" (Art 28), which both the Measures
  and the Q&A describe only in general terms.
- Any enforcement activity under the Measures. They took effect 15 July 2026 — one day before this
  research date — so no enforcement record can exist yet.
