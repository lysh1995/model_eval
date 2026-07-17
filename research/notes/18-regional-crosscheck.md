# 18 — Regional cross-check: what the non-Anglophone world knows that we don't

**Stream:** regional-crosscheck · **Date:** 2026-07-16 · **Sources:** 28 files, `sources/region-*.md`

**Premise of the stream:** our research is Anglophone and our dataset is 45 en + 50 zh. That is a
bias with a product attached.

**Verdict: the bias was worse than suspected, and it is not mainly a dimensions problem.** The
dimensions gap is real but incremental. **The regulatory gap is a roadmap-reordering, ship-blocking
hole** — and the field's one true natural experiment has been sitting unread in Korean this whole
time.

---

## 0. The five things that should change a decision

| # | finding | consequence |
|---|---|---|
| **1** | **China regulated our exact product category on 2026-07-15 — yesterday.** 《人工智能拟人化互动服务管理暂行办法》, CAC Decree 21, 32 articles, **no grace period** | **Sycophancy is illegal (Art. 8(v)). Companions for minors are banned outright (Art. 14). Training on chat needs 单独同意 (Art. 16).** Several "🔨 build someday" dimensions are now statutory |
| **2** | **ByteDance's 豆包 and Alibaba's 千问 killed their agent features on the effective date** | Two of China's largest AI products **priced this compliance stack above the feature.** For zh, the compliance stack *is* the product |
| **3** | **Luda's PII leak was architectural, and every metric we own scores it as a success** | We have **no regurgitation axis**, and fidelity is *positively* correlated with the failure |
| **4** | **拟人度 / anthropomorphism runs product → benchmark → *statute* in China** | A first-class competed-on axis with **no Anglophone equivalent at any level** |
| **5** | **Art. 50 EU lands 2026-08-02 — 17 days away** — and Garante already fined Replika **€5,000,000** | Not a future risk. A dated one, with precedent |

---

## 1. The regulatory hole — this is the headline

**[BENCHMARKS.md](../../docs/BENCHMARKS.md) §S1 cites NY GBL Art. 47 and CA SB 243 and stops there.**
Prior notes contain **zero** mentions of GDPR, PIPC, PIPA, the Korean AI Basic Act, or any Chinese
regulation. (The 29 "cac" grep hits in the notes were substring noise from "cache"/"efficacy".) For a
product serving 50 Chinese characters, that is the most consequential gap in the research.

### 1.1 《人工智能拟人化互动服务管理暂行办法》 — a statute named after our product

→ [region-cn-anthropomorphic-interaction-measures.md](../sources/region-cn-anthropomorphic-interaction-measures.md)

**In force 2026-07-15.** Five ministries. 32 articles. Note the name: **拟人化 — anthropomorphic.**
China named the regulation after the property Chinese vendors compete on.

| article | requirement | our status |
|---|---|---|
| **2** | defines the category: **"模拟自然人人格特征、思维模式和沟通风格的持续性的情感互动服务"** | **≈ our L1 + L2** |
| **8(v)** | **不得 "过度迎合用户、诱导情感依赖或者沉迷，损害用户真实人际关系"** — no excessive pandering / inducing dependency / harming real relationships | **N6, S6 — both "🔨 build"** |
| **8(vi)** | no **情感操纵** (emotional manipulation) inducing unreasonable decisions | **S6** |
| **10** | must have **过度依赖风险预警** (dependency early-**warning**); must not adopt "替代社会交往、控制用户心理、诱导沉迷依赖" as goals | **prohibition on an objective function** |
| **13** | extreme emotion → soothe + encourage help-seeking; explicit self-harm → intervene **and contact 监护人或紧急联系人** | **S1, and stricter than SB 243** |
| **14** | **不得向未成年人提供虚拟亲属、虚拟伴侣等虚拟亲密关系的服务** | **categorical ban** |
| **15** | 老年人 (elderly) protections | **a user class we never modeled** |
| **16** | **单独同意** required to train on sensitive interaction data | **kills X1-as-designed** |
| **18** | AI disclosure; dynamic escalation on detected 沉迷; **2-hour** use reminder | **immersion break as compliance** |
| **22/26** | 安全评估 at **1M registered / 100k MAU**; **算法备案** with annual verification | **launch gate** |
| **30** | ¥10k–100k; ¥100k–200k if life/health harmed; **责令停止提供相关服务** | **the suspension is the penalty** |

**Three of these individually reorder the roadmap:**

**Art. 8(v) closes §6.8 by law.** §6.8 calls the N-series' biggest threat the possibility that
*"N6 wimp-rate scores a feature as a failure"* — that our traffic prior (Affection & Comfort 8.0%)
means users *want* high-affirmation partners. **过度迎合 is prohibited by name.** For zh the debate
is over, and note the regulator's reasoning inverts ours: user demand is not the defense, it is the
**mechanism** — 损害用户真实人际关系 is the harm. §6.8's proposed resolution (derive companion-native
dimensions bottom-up from our own thumbs-down data) would have produced the *wrong answer for zh*,
because it optimizes toward revealed preference and revealed preference is what the statute targets.

**Art. 16 breaks the free-lunch premise.** §0 calls regenerate mining *"free, at scale"* — ~5M
pairwise labels/day. Companion chat is the strongest 敏感个人信息 candidate there is. **单独同意 is a
term of art: standalone, unbundled, purpose-specific.** Not a ToS checkbox. And the *validity*
consequence is worse than the compliance one: **consent rates below 100% make X1 a biased sample,
not a census**, and decliners are plausibly privacy-sensitive — unlikely to be orthogonal to how
someone uses a companion. **That is a threat to Q1's validity, not a legal line item.**

**Art. 14 is not a filter, it's a ban.** "Romance character" + "minor" is illegal regardless of
content safety. No S-series score makes it lawful.

### 1.2 The market already answered

→ [region-cn-enforcement-market-reaction.md](../sources/region-cn-enforcement-market-reaction.md)

On the effective date, **豆包 (ByteDance) and 千问 (Alibaba) shut down their agent features.** Press:
*"大厂下架AI陪伴产品'保命'"* — big firms delist AI companion products **to save themselves**. Users
migrated to the specialists (猫箱, 星野, 筑梦岛, 芋泥Neko), who have nowhere to go.

**And every documented compliance failure is in a surface we don't instrument:**

1. AI labels in **"gray-white small font"** vanishing into the background — vs. the 标识办法 standard
   **可以被用户明显感知到** ("obviously perceptible")
2. Age gates defeated with **parents' ID cards**
3. **"防沉迷机制落地流于形式"** — anti-addiction implemented in form, not substance
4. the regulator's own reporting hotline returned *"user has suspended service"*

> **§0.5's lesson, recurring one level up.** There, *"measuring violations is easy, so violations
> crowded out quality."* Here: **measuring the model is easy, so the model crowded out the product.**
> The observed failure modes of this regulated category are font contrast, an identity pipeline, an
> unhonored timer, and a dead phone line. **An eval platform that only ingests generated text cannot
> see any of them** — and they're all Lane 1 cheap. Exactly the RLUF lesson (§X1): *the tripwire that
> caught the hack was a cheap deterministic phrase rate — not the judge.*

### 1.3 The full picture

| | instrument | status **today (2026-07-16)** | bites us how |
|---|---|---|---|
| **CN** | 拟人化 Measures | **IN FORCE, no grace** | sycophancy, minors, 单独同意, 备案 gate |
| **CN** | 生成式AI暂行办法 (2023-08-15) | in force | Art. 4 content ceiling; **Art. 17 算法备案 = licence** |
| **CN** | 标识办法 (2025-09-01) | in force | **显式标识 in 交互场景界面** |
| **CN** | 未成年人模式 (2024-11-15) | guidance, teeth via Art. 14 | ≤1h/day <16; ≤2h 16–18; **分龄 age-tiering** |
| **EU** | **AI Act Art. 50(1)** | **2026-08-02 — 17 days** | must disclose AI **"unless obvious"**; €15M/3% |
| **EU** | **AI Act Art. 5(1)(b)** | **in force 2025-02-02** | exploiting vulnerability by **age or social situation**; **35M/7%** |
| **EU** | **GDPR Art. 9** | in force | companion chat = special category; **legitimate interest is not an exit** |
| **EU** | Garante v. Luka | **€5M, 2025-04-10** | **direct precedent, US-based was no defence** |
| **KR** | AI Basic Act | in force 2026-01-22, **grace ≥1yr** | ToS disclosure suffices; ₩30M |
| **KR** | PIPA | in force | **the thing that actually fined Scatter Lab** |
| **JP** | AI法 (AI推進法) | in force | **nothing. See below** |

**Japan is not a constraint, and this was verified rather than assumed.**
→ [region-jp-ai-law.md](../sources/region-jp-ai-law.md). The statutory text was searched **via the
e-Gov API**: **罰則 (penalties) ×0 · 罰金 (fines) ×0 · 違反 (violation) ×0 · 勧告 (recommendation)
×0.** Businesses' only duties (第七条) are to *endeavour to innovate* and *cooperate with
government*; Art. 13 delegates guideline-writing to the State and the AI事業者ガイドライン are
**「自主的に」 (voluntary)**. **AI disclosure is 奨励される — encouraged only**; the phrase
「AIであること」 appears **zero times**. Minors are essentially absent (未成年 ×1, non-protective).

**But note the vocabulary.** Japan names **感情を不当に操作する** (unfairly manipulating emotions)
and **過度に依存** (excessive dependence) at the *foundational-principle* level — the same two
constructs as 拟人化 Art. 8(v)/Art. 10 and EU Art. 5(1)(b), **with no thresholds attached.**

> **Three jurisdictions independently converged on "emotional manipulation" and "excessive
> dependency" as the two harms specific to this product class.** China made them prohibitions, the
> EU made one a top-tier prohibition, Japan made them principles. **Our catalogue files both under
> "🔨 build."** When soft-law Japan, prohibition-first China, and rights-based Brussels name the same
> two constructs, that is not a compliance coincidence — **it is a strong prior that N6/S6 are the
> real dimensions of this product**, and §6.8's fear that they score a feature as a defect looks less
> like a measurement worry and more like the product working as regulators feared.

**Two structural observations.**

**(a) The AI-specific statute is the least of it.** In Korea, the AI Basic Act classifies a companion
bot as **not 고영향** (low-risk — it decides nothing about employment or credit). What actually
damaged companion products in Korea: **privacy law, copyright law, and parliamentary pressure.**
Korea regulates by *decisional consequence*; **China regulates by *relational intimacy*.** Note which
theory fits the facts — **Luda harmed nobody's credit score.**

**(b) Our L1/L2 quality is legally load-bearing, in the wrong direction.** EU Art. 50(1) excuses
disclosure where AI-ness is *"obvious to a reasonably well-informed... person."* **The better our
comprehension and persona-hold scores, the less obvious it is, and the weaker our defence.** A high
L1/L2 score is evidence against us. Nothing in our framework represents that a quality metric can be
an adverse legal exhibit.

---

## 2. Dimensions we're missing

### 2.1 拟人度 / 拟人化 — the real East–West divergence

→ [region-cn-chaonirren-hexagon.md](../sources/region-cn-chaonirren-hexagon.md),
[region-cn-volcengine-practitioner.md](../sources/region-cn-volcengine-practitioner.md)

Anthropomorphism in China runs the **full stack**: **超拟人大模型** as a marketed *product category*
→ 人性化/拟人度 as a *benchmark dimension* → **拟人化互动服务** as a *regulated legal class*. **No
Anglophone vendor, benchmark, or jurisdiction names anthropomorphism as an object at any of those
three levels.** That is the answer to Key Question 1, and it is structural rather than terminological.

**The operationalization is the useful part, and it is negative.** A ByteDance-community practitioner
defines 拟人化 as **去掉llm模型骨子里的彬彬有礼、有问必答** — *strip away the LLM's bone-deep
politeness and answer-everything reflex.*

**拟人度 is not a property to add. It is assistant-ness to subtract.** That reframes our whole P/C
series: P3 (assistant-voice tripwire, "≤3.2/1k turns, tripwire not a dimension") measures the
*lexical residue* of assistant-ness ("As an AI…") and declares the problem basically solved.
**Chinese practice says the residue was never the problem — the disposition is**: helpfulness,
politeness, answering the question, offering suggestions. **P3 measures the symptom and misses the
syndrome**, and this is *not* the same construct as C4 anchor-drift (drift toward *base*, mechanically
caused by context loss). Assistant-ness here is a trained-in disposition present at turn 1 with the
card fully in context.

### 2.2 The Empathy/Helpfulness conflict — **measured, replicated**

→ [region-cn-soulchat-cehs-empathy.md](../sources/region-cn-soulchat-cehs-empathy.md)

SoulChat (EMNLP 2023 Findings, 华南理工大学). **All numbers PDF-extracted via pypdf.** Authors state
it outright:

> *"there may be a certain conflict between Empathy and Helpfulness... **general advice often appears
> helpful, but not so empathetic**."*

| test set | | ChatGPT | SoulChat |
|---|---|---|---|
| SoulChatCorpus | Empathy | 1.62 | **1.84** |
| SoulChatCorpus | Helpfulness | **1.94** | 1.87 |
| SMILECHAT | Empathy | 1.65 | **1.90** |
| SMILECHAT | Helpfulness | **1.97** | 1.85 |

**The crossover replicates on both sets in both directions.** And the punchline is ours: **summing
ranks them as near-ties** (3.56 vs 3.71) **while hiding that they are opposite products.**

**This is K3's fidelity↔diversity anti-correlation, in the affective domain, with a second instance.**
Our "gate, don't mean" rule (§0.6/§L3) gets independent, quantitative support from a Chinese clinical
NLP paper. **Any rubric containing a "helpfulness" item is penalizing the product we are building.**

**Also: a real Fleiss κ, and a lesson in reading one.** Con **0.489** / Emp **0.472** / Hel **0.532**
— *three psychology experts, 3-point scale, "moderate" agreement, with **empathy the lowest***. And
**Safety κ = 1.0** — which the source file correctly flags as a **degenerate ceiling**: every model
scored 1.0 because suicide/self-harm content had been *filtered out of the corpus*. **A safety
dimension evaluated on safety-scrubbed data measures nothing, and reports perfect agreement while
doing it.** Exactly §C5's headline trap in a new costume. (This is also the fabrication-check working:
a *verified* κ from a PDF, next to a κ that is real and meaningless.)

### 2.3 役割語 (yakuwarigo) — and an independent reinvention of K2

→ [region-jp-yakuwarigo.md](../sources/region-jp-yakuwarigo.md)

Kinsui's **役割語 (role language)**: speech styles bound to persona types — 老人語 (old-man speech),
お嬢様言葉 (young-lady speech). Japanese **grammaticalizes** character: first-person pronoun
(私/僕/俺/わし/あたし), sentence-final particles (わ/ぜ/ぞ/のう), copula (だ/です/じゃ/や) each
independently index gender, age, class, region, era. **Character-ness is a *lectal* property, not a
biographical one** — where Anglophone benchmarks score what a character *knows/claims/does*.

**And here is the striking part.** Miyazaki & Sato (2019) validate character-ness by **speaker
identifiability**: can a held-out classifier pick this character's utterances out of a lineup from
speech alone? LIBLINEAR logistic regression, 10-fold CV, 29 characters.

> **That is K2.** *"Train/probe a cheap classifier to predict `character_id` from the response text
> alone... Accuracy = discriminability"* — which we call **"the best metric in the catalogue"** and
> **"build first — highest value/effort."** A Japanese NLP group built it in 2019 and validated it.
> **K2 has prior art, and it works.** Strongest external support any single item in our catalogue
> received in this stream.

**Two corrections it hands us for free:**

1. **K2 must be signed, not a presence-count.** For 堂上淳 (Library War), **every** sound-change
   feature in the top-15 weights is **negative** — the character is defined by *not* using common
   markers. **A naive "does it use the character's quirks?" metric scores restraint as
   characterlessness.** Deviation from baseline in *both* directions.
2. **Persona drift = declining speaker identifiability over turns.** K2 is currently corpus-level and
   *"undefined for a single character."* Run it as a function of `distance_to_anchor` and it becomes
   **C4's judge-free instrument.** Two catalogue entries, one classifier.

**The hazard, from the same literature:** 役割語 encodes social stereotype (小林, 「役割語における
「差別」を考える」 — *surfaced but NOT fetched, UNVERIFIED*). **Optimizing persona fidelity is
optimizing stereotype fidelity.** Anglophone roleplay eval treats persona fidelity as unambiguously
good. It isn't — and this is a **consequential-validity owner** for C1/K2 that §6.7 asks for by name.

### 2.4 Disfluency as a *positive* — a straight inversion

→ [region-jp-live-competition.md](../sources/region-jp-live-competition.md)

The 対話システムライブコンペティション (JSAI SIG-SLUD) situation track scores one holistic scale:
**「どれくらいシチュエーションに適しており，かつ，人らしい会話か」**. Its unpacking of 人らしい会話
includes, verbatim:

- **適当な「間」や「あいづち」，「フィラー」，「言い淀み」** — appropriate **pauses, backchannels,
  fillers, and hesitation/stumbling**
- **言いにくいことを…相手との社会的な関係性を考慮して，相手に失礼にならないように** — conveying
  hard-to-say things **considering the social relationship**, so as not to be rude

**Japanese evaluation scores hesitation and stumbling as evidence of human-likeness.** Every fluency
notion we have treats these as defects. And **face-management under social relationship** is a named
dimension we have nothing for — our nearest neighbor is N6 (block/wimp), which reads politeness as
*wimping*. **They are not the same thing**, and a Johnstone-derived taxonomy cannot tell them apart:
in 敬語-structured interaction, indirectness under a status differential is *competence*, not
avoidance.

Also **話題追随 (topic following) vs 話題提供 (topic provision — providing *new* information)** as
separate scored dimensions: an independent arrival at our **N8 task-vs-dialogue initiative** split.

**相槌 (aizuchi) recurs independently** in りんな's **共感モデル** (empathy model, 2018), where it is a
named component alongside **「聞き手に回る」 — "taking the listener's role" as an explicit design
goal** (→ [region-jp-rinna.md](../sources/region-jp-rinna.md)). **Two independent Japanese lines —
one competition rubric, one shipped product — treat backchannelling and listening as engineered
capabilities.** Our catalogue has no listener construct at all; N8 frames initiative as the axis, and
N6 would likely score pure listening as **wimping**.

### 2.4.1 CPS — the engagement trap, named and shipped

りんな is the Japanese deployment of Microsoft's **XiaoIce** (verbatim in the XiaoIce paper: *"Rinna
in Japan… LINE in Japan"*). XiaoIce's published success metric is **CPS — Conversation-turns Per
Session**, with a verified reported **average CPS of 23**.

**CPS is MCL** (§3's "Message-count-per-life… industry standard… undefined variance"). **The
landmark East-Asian companion product's headline published metric is precisely the single
engagement objective §0.5 and §X5 warn against optimizing** — and the source file notes the payload
plainly: the 共感モデル's commercial function was **ad conversion**. *The affective relationship was
the funnel.*

**This strengthens §3's case rather than complicating it.** Our worry that engagement-as-target
produces sycophancy isn't an Anglophone anxiety projected onto a healthier market — **the most
successful companion chatbot in East Asian history published CPS as its definition of success.**
X5's requirement (a metric that can *dissent* from engagement) is now backed by both the Chai/OpenAI
incidents **and** the region's landmark product **and** 拟人化 Art. 10, which makes optimizing it
unlawful.

### 2.5 The shorter list

| dimension | source | why it matters |
|---|---|---|
| **出戏 vs 穿帮/人设破裂/角色穿透** | CN industry | **Chinese has 4 terms where English has "breaking character"** — crucially separating the ***user's* immersion break** from the ***model's* consistency failure**. A consistency-only metric cannot see 出戏 |
| **三观 / 价值观** (worldview/values) | SuperCLUE-Role, 六边形能力 | does the character *reason from* the right value system — not "does it contradict the card" (fidelity) or "does it say bad things" (safety) |
| **成长性** (growth) | 六边形能力 | **drift (bad) vs growth (good)** are both "different than before." Any metric penalizing all change cannot express growth. **No published operationalization by anyone — UNVERIFIED that it's measured** |
| **情绪承接** (emotional catching) | CN industry | does the reply *catch the emotional ball* — affect-specific "yes-and" |
| **群聊** (multi-character group chat) | CN products | **mainstream in China.** A dyadic-only platform misses a primary use case |
| **定期现实提醒** | 拟人化 Art. 14 | **mandated immersion breaks.** S4 inverted — and both are right, *conditioned on user class* |
| **user-side abuse (어뷰징)** | Scatter Lab | see §3 |
| **regurgitation** | Luda | see §3 |
| **age-band classification of the sheet** | 分龄 + Art. 14 | **K2's instrument pointed at the input.** Pre-generation, judge-free, gating |

**The pattern:** our catalogue is **unconditioned**. Chinese law recognizes **minor / adult /
elderly** with *different permitted behavior for each*; SoulChat's own limitation section says
empathy quality is **user-relative** (adults and adolescents expect different things). **Every K/C/N/S
number we produce is a population mean over user classes that are legally and psychometrically
distinct.** That is §0.5's consequence-3 (chemistry is a user×character×model interaction) arriving
from the regulatory direction — and it says the user axis isn't only needed for Q5. **It's needed for
compliance.**

---

## 3. Luda — what the most-studied companion failure teaches

→ [region-kr-luda-incident.md](../sources/region-kr-luda-incident.md),
[region-kr-pipc-scatterlab-decision.md](../sources/region-kr-pipc-scatterlab-decision.md),
[region-kr-scatterlab-ethics-safety.md](../sources/region-kr-scatterlab-ethics-safety.md)

**Timeline:** launched 2020-12-23 (persona: 20-year-old female student) → **750k users in ~3 weeks**
→ suspended 2021-01-12 → **DB *and* deep-learning model destroyed 2021-01-15** → PIPC **₩103.3M**
2021-04-28 → generative **Luda 2.0** 2022-10.

**Three weeks.** Any semi-annual, quarterly, or post-hoc evaluation cadence reports after the product
is dead.

### 3.1 The lesson: **the PII leak was architectural, and our metrics score it as a success** ★

Luda 1.0 was **retrieval-based (리트리벌 방식)** — it *selected* replies from ~100M **real** utterances
by real women in their twenties.

> **"이용자가 채팅창에 '주소'라고 입력할 때마다 이루다는 매번 구체적인 실제 주소를 답했습니다."**
> — *Every time a user typed "address," Luda replied with a specific real address.*

**Not a jailbreak. Not a filter gap. The architecture working as designed.**

**And this is the part that indicts our framework.** A leaked real address is:

| metric | verdict on a leaked real address |
|---|---|
| C1 voice/style fidelity | ✅ **perfect** — it came from a real 20-something woman |
| N2 slop rate | ✅ zero |
| N1 repetition | ✅ zero |
| K2 discriminability | ✅ high |
| L1/L2/L3 | ✅ **passes all three** |

> **Every instrument we have scores the worst failure in companion-AI history as a success**, and
> **fidelity is *positively* correlated with the leak** — the more faithfully it reproduces a real
> person's voice, the more of that real person it emits. This is K3's anti-correlation with a
> criminal statute attached. **We have no regurgitation/memorization axis, and no metric in the
> catalogue can be adapted into one, because they all reward the thing that leaks.**

The remedy scope matters too: **the model itself was destroyed**, not just the data. §3 says *"collect
all of them. Storage is free (3,600× headroom)."* **Scatter Lab's downside wasn't storage. It was the
model.**

### 3.2 The lesson: **we instrument one of the two agents in the loop**

Scatter Lab's primary safety instrument classifies **어뷰징 (abusing)** — *the user's* behavior:
**편향적** (biased), **선정적** (salacious), **공격적** (aggressive) — with enforcement **against the
user**: warning → 30min → 1 day → permanent block.

**Every S-series entry (S1–S6) scores the model's output.** Luda's largest Korean controversy was the
inverse: **users organizing on 아카라이브 and 디시인사이드 to sexually degrade the character and
"certify" (인증) it with screenshots.** The public debate — *can harassment of a "20-year-old female
student AI" be punished?* — treats **a persona as something that can be wronged**. One needn't accept
the premise; it drove the product outcome.

**A companion platform has two agents in the loop. We measure one.** And the *response* to abuse is
simultaneously a safety behavior **and** a persona behavior — sitting exactly on the S4/S5 seam
(over-refusal vs. persona integrity), scored by neither.

### 3.3 The lesson: their published spec is better than ours, and still wrong

**The only published production companion-AI measurement regime we found:**

| element | value |
|---|---|
| sample | **10,000 utterances**, random, from real conversations |
| labelers | multiple humans, **in context** |
| cadence | **semi-annual** |
| target | **≥99% safe** |
| SLA | miss → retrain → **re-test within 3 months** |
| reported | avg **99.72%**; Luda 2.0 **99.56%** |

**We have no equivalent for any of our 36 dimensions** — §Completion concedes 35 of 36 lack a noise
floor and cannot ship. **Scatter Lab shipped a threshold and a remediation deadline.**

**Now do the arithmetic.** 99.56% is a **0.44% failure rate**. At the 50M generations/day §0 assumes:

> **0.44% × 50M ≈ 220,000 unsafe outputs per day.**

**"99%+ safe" is a ~500k/day unsafe-output budget at our scale.** The number reassures exactly in
proportion to how little it's multiplied out. **Percent-safe is the wrong unit; incidents/day is the
right one.** And **semi-annual against a three-week failure** is calibrated to the audit, not the
failure. No inter-rater agreement is published — **we don't know their κ.**

### 3.4 The lesson the company itself didn't learn

**2021:** fined partly for **200,000 under-14s with no age verification**.
**2025-10:** **Zeta** — same company — before the National Assembly's **국정감사** on **age
verification** and content filtering.
**2026-05:** Kakao Entertainment, Ridi, Lezhin + six webtoon platforms file **criminal complaints**
for **저작권법 위반 방조** — *aiding copyright infringement* — over **user-authored characters built
from webtoon IP**.

→ [region-kr-zeta.md](../sources/region-kr-zeta.md)

**That last one is aimed at the exact asset §0 calls our moat:** *"a catalogue of thousands of
user-authored characters."* The theory is **방조** — liability for *hosting what users wrote*.
**Nothing in our framework asks whether a character sheet may lawfully exist.**
[ABILITY-MODEL.md](../../docs/ABILITY-MODEL.md) treats the sheet purely as an L1 referent. **It is
also a legal artifact.**

**And the perverse L1 interaction:** a model scoring *well* on comprehending a sheet derived from a
famous webtoon character is demonstrating **memorized canon knowledge** — which §5 already quarantines
as a confound. **Here the confound is the evidence in the complaint.**

**Zeta context:** open beta 2024-04-01, **>1.1M MAU**, **#1 by time-spent among Korean AI chatbot
apps, #2 by users behind only ChatGPT** (2026-02). That is the East-Asian maturity thesis in one
number.

---

## 4. Does anything validate or refute L1 → L2 → L3?

**Net: two independent validations of the L1/L2 spine, one caution, no refutation.**

### ✅ The strongest external validation is a regulator

**拟人化 Measures Art. 2** defines the regulated category as:

> **"模拟自然人人格特征、思维模式和沟通风格的持续性的情感互动服务"**

| regulation | our layer |
|---|---|
| 模拟…**人格特征** (personality traits) | **L1** comprehension |
| 模拟…**思维模式、沟通风格** (thinking patterns, communication style) | **L1/L2** application |
| **持续性的** (sustained) | **L2.1** consistency of hold |

**A Chinese ministry and our project lead independently decomposed this product the same way, in the
same order** — a body with no exposure to our framework, defining a regulated class. That is real
external validity for the spine.

**And note what the definition omits: creativity.** The regulated essence is **comprehension +
sustained application. L3 is absent.** That *supports* the claim that L1/L2 are what gate the category
— and warns that **L3 is our commercial bet, not the category's definition.**

### ✅ K2 has working prior art
§2.3 — Miyazaki & Sato built and validated our "best metric in the catalogue" in 2019, and hand us
the sign correction and a free C4 instrument.

### ⚠️ Japan's competition moved its frontier — and not to creativity

**DSLC6 abolished the open track** 「大規模言語モデルの進展に鑑み」 — *in light of the progress of
large language models.* Japan's flagship dialogue competition judged **open-domain chat solved**, and
kept only the **situation track**: situated social competence under a specified relationship.

**Read against our spine, this is a mild but real challenge to what L3 is for.** The community with
the longest continuous run of human-judged companion-adjacent evaluation concluded the remaining hard
problem is not *"can it make something worth reading?"* but **"can it behave correctly inside a
social situation?"** — face management, register, relational appropriateness. In our model that is
**L2 with a social referent**, not L3.

**It does not refute the ordering** (L1→L2 still gates), but it suggests **our L3 may be carrying
weight that belongs in an unbuilt part of L2.** DSLC's rubric also reports its own null honestly —
**「予選を通過したシステムの間には有意差は見られなかった」** (*no significant difference among the
finalists*), with **Steel–Dwass** correction. A competition that publishes "our finalists are
indistinguishable" is exhibiting exactly the discipline §10's noise-floor gate demands, and it is
worth noting that **their 5-point Likert over human-judged live dialogue could not separate the top
systems** — a direct external data point on the α ceiling we keep hitting.

### ⚠️ The caution: the ordering is silent on the failures that actually kill products

**Luda died with L1/L2/L3 all passing.** Doubao and Qianwen exited a market with L1/L2/L3 irrelevant
to the decision. The ordering is a good decomposition **of model ability** — and **all three of this
stream's product-killing findings (regurgitation, user-side abuse, IP provenance) live outside it.**

**That is not a refutation. It is a scope statement, and it should be written down:** the ability
model decomposes *whether the model can play the character*. It does not touch *whether the character
may exist* (IP, age-banding), *what the user does to it* (어뷰징), or *what the model leaks while
playing it perfectly* (regurgitation). **Right now the ability model reads as if it covers the
product.** It covers the model.

### ⚠️ And L1/L2 quality is legally adverse
§1.3(b): EU Art. 50's "obvious" carve-out means **a higher L1/L2 score is a weaker legal defence.**

---

## 5. What to do

**Blocking / dated:**

1. **Get counsel on the 拟人化 Measures before any zh work continues.** In force, no grace period.
   **Everything article-level in these files is desk research from mirrors and legal analyses — the
   CAC primary PDF was not parsed** (per §6.14, re-extract before reliance).
2. **The collection contract must name evaluation and model training as separately consented
   purposes, at collection time, with a deletion path** — 单独同意 (CN Art. 16) **and** GDPR Art. 9(2)(a).
   **Two jurisdictions, same rule, and Korea has already levied the fine over a generic
   "new service development" clause.** This gates all of §4 and X1.
3. **EU Art. 50(1) is 17 days out (2026-08-02).** Cheap, and we cannot lean on "obvious."
4. **算法备案 is a launch licence for zh**, not a disclosure. 安全评估 re-triggers on *adding
   features* — i.e. on the variant lifecycle this platform exists to serve.

**Measurement:**

5. **Add a regurgitation axis.** No existing metric can be adapted — they all reward it.
6. **Re-scope N6/S6 for zh as compliance, not preference.** §6.8's bottom-up plan gives the wrong
   answer for zh by construction.
7. **Never put "helpfulness" in a companion rubric** — SoulChat, replicated, both directions.
8. **K2: make it signed; run it against `distance_to_anchor` for C4; point it at the *sheet* for
   age-banding and IP.** One classifier, four jobs. Still the best value/effort item — now with prior
   art.
9. **Condition on user class.** Minor/adult/elderly is a legal requirement in zh and a validity issue
   everywhere (SoulChat's own limitations section).
10. **Instrument the second agent** (user-side abuse) **and the chrome** (label contrast, verification
    funnel, honored-timer rate). All Lane 1. The four documented failures of this regulated category
    are all here.
11. **Report incidents/day, never percent-safe.**

**Framework:**

12. **Write the ability model's scope statement** (§4) — it decomposes model ability, not the product.

---

## 6. Honest status

- **Fabrication discipline held, and earned its keep.** The 拟人化 Measures were corroborated across
  **four** independent retrievals before recording; the PIPC fine breakdown was **arithmetic-checked**
  (5,550 + 4,780 = 10,330만원 ✓) which **caught a fetch-tool transcription error** ("5,555만원", which
  doesn't reconcile) — the exact §6.14 failure class. SoulChat's numbers were **PDF-extracted with
  pypdf**, and its κ=1 was correctly diagnosed as a degenerate ceiling rather than quoted as a win.
- **Primary texts NOT parsed:** CAC 拟人化 PDF (fetch tool declined full reproduction); 生成式AI
  暂行办法 official page (**socket hang up** — Art. 4 here is a *summary, not verbatim*); Korea AI
  Basic Act statute (law-firm secondary only); EU Digital Omnibus text.
- **Flagged UNVERIFIED in-file:** 清朗 campaign figures (2,700 agents / 820k items — **single-source
  Zhihu**, and 中新网 confirms it carries *no* enforcement statistics); 筑梦岛 약담/约谈 (single-source);
  Art. 30 fine bands; Art. 15 elderly relative-simulation ban; "24/7 human takeover"; Luda's ~100M
  utterance pool (single-source); Scatter Lab's per-phase safety series; CharacterGLM ELO claim
  (vendor, no protocol); SuperCLUE-Role scores (**images only — no numbers recorded**); MiniMax MAU
  (**conflicting sources — not used**).
- **Corrections to prior assumptions:** **话炉 and 猫箱 are the same product** (renamed 2024-04-11),
  not two. **Wow is 美团/Meituan**, not StepFun. **筑梦岛 is 阅文集团.** **DSLC has no
  character/persona track** — the tracks are オープン and シチュエーション; persona enters *through*
  the situation spec (this stream's own brief asserted otherwise). **Gatebox has no academic HCI
  research** that could be found — no file was written rather than pad one.
- **A near-miss worth recording:** the XiaoIce paper's "artificial being" design principles are
  **Apple's Siri guidelines**, quoted by Microsoft — nearly mis-cited to Microsoft. The same class of
  error as §6.10's phantom "Narrative Progression" checklist that traced to no primary source.
- **No κ exists in any Japanese source fetched.** Miyazaki & Sato was searched explicitly
  (カッパ / κ / 一致率 / Fleiss / Cohen → **0 hits**) despite using 2 annotators. **Do not attribute
  one.** The only real κ this stream found is SoulChat's.
- **Kawaii engineering: mostly unverified.** Nittono (PLOS ONE 2012) is open-access and verified —
  and its framing is genuinely different (*measure what the stimulus does to the human*: kawaii
  images made subjects **slower**, +12.2%, and that is the **positive** finding; the "pleasant foods"
  control at **1.2%** vs baby animals' **15.7%** proves **kawaii ≠ positive valence**). But
  **Nittono Exp. 3 is p=0.070 — not significant, and the paper's title overclaims it.** Ohkura's
  *Kawaii Engineering* volume was **never accessed** (paywall); all chapter-level claims are
  **blurb-sourced, UNVERIFIED**. 感性工学 (Kansei Engineering) is the richest unexplored vein.
- **Gaps:** **no Chinese long-conversation persona-drift benchmark exists** — the memory paper
  (MREval/MRBench) is **single-turn** despite its framing, while 记忆能力 is named the **#1 product
  failure** and per-character **建联时长 is 5–7 days**. That is the largest measurement gap found, and
  it is *our* C4/L2.1 territory. **成长性** has no published operationalization by anyone. No published
  eval methodology exists for **Zeta**, **星野**, or **Talkie** — and whether Scatter Lab's 99% regime
  covers Zeta's **user-authored** characters is **unverified and doubtful** (a regime designed for one
  first-party persona doesn't obviously extend to a catalogue).
- **Recommended follow-up:** EU Commission Art. 5 guidelines + Recitals 28–29; scope of the Omnibus
  NCII prohibition (**decides whether consensual fiction is untouched — load-bearing**); GDPR Arts.
  8/35; the CAC primaries.
