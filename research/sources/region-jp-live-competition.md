---
title: "対話システムライブコンペティション5 (The Dialogue System Live Competition 5)"
url: https://www.jstage.jst.go.jp/article/jsaislud/96/0/96_19/_pdf/-char/ja
authors: 東中竜一郎 (Ryuichiro Higashinaka), 高橋哲朗, 堀内颯太, 稲葉通将, 佐藤志貴, 船越孝太郎, 小室允人, 西川寛之, 宇佐美まゆみ, 港隆史, 境くりま, 船山智 — 人工知能学会 SIG-SLUD-096-19
year: 2022
type: paper
language: ja
accessed: 2026-07-16
topic: regional-crosscheck
---

# 対話システムライブコンペティション (Dialogue System Live Competition, "ライブコンペ")

Japan's flagship recurring dialogue-system competition, run under 人工知能学会 (JSAI) SIG-SLUD and
judged live at the 対話システムシンポジウム (Dialogue System Symposium). Now in its 7th edition
(第7回, kickoff 2025-09-12 — see UNVERIFIED note below). **This is the highest-value Japanese find:
it publishes its evaluation dimensions verbatim, and its dimension set differs materially from
Anglophone roleplay benchmarks.**

Source for everything below: the DSLC5 overview paper (SIG-SLUD-096-19), extracted from the J-Stage
PDF with pdfminer.six. All Japanese quoted verbatim from that PDF unless marked otherwise.

## Structure: two tracks

> 「ライブコンペ 5 では，過去数回と同様，オープンドメインでユーザと対話する能力を競うオープン
> トラックと，特定のシチュエーションにおいて人間らしい対話を行う能力を競うシチュエーション
> トラックを設けた．」

"In Live Competition 5, as in the past several editions, we set up an **open track**, competing on the
ability to converse with users in an open domain, and a **situation track**, competing on the ability
to conduct **human-like dialogue in a specified situation**."

DSLC5 (2022) moved to multimodal systems: input is the user's ASR result; output is system speech
plus multimodal information (facial expression, gesture) via a 3DCG model of the android robot ERICA
("CGErica"). Note the stated asymmetry — the user's multimodal information is *not* an input:

> 「今回は，システムの制約によりユーザのマルチモーダル情報を入力として用いない点については注意されたい．」

## Evaluation dimensions — OPEN TRACK (§2.2.2 評価尺度)

Split into two families: 「発話内容」(utterance content) and 「話し方」(manner of speaking / delivery).
The content dimensions are inherited from ライブコンペ4:

| Japanese (verbatim) | Translation |
|---|---|
| 自然性：対話が自然かどうか | **Naturalness**: whether the dialogue is natural |
| 話題追随：システムはユーザが選択した話題に関して適切に応答できたかどうか | **Topic following**: whether the system could respond appropriately on the topic the user selected |
| 話題提供：システムはユーザが選択した話題に関して新たな情報を提供できたかどうか | **Topic provision**: whether the system could provide *new information* on the user-selected topic |

> 「5 段階のリッカート尺度を用い，3 指標の平均値を評価得点 (C) とした．」
> 5-point Likert; the mean of the 3 indices is the content score (C).

The delivery family adds exactly one dimension, new for the multimodal edition:

> 「• 話し方の自然性：音声やジェスチャー，表情などで示される話し方が自然かどうか」
> **Naturalness of delivery**: whether the manner of speaking, as shown through voice, gesture,
> facial expression etc., is natural.

> 「5 段階のリッカート尺度を用い，そのまま評価得点 (S) とした．」 → score S.

Final dialogue score = mean of C and S, **deliberately equally weighted**:

> 「マルチモーダル情報の効果的な利用が促進されるよう，発話内容と話し方の評価の重みを同じにしている．」
> "So that effective use of multimodal information is encouraged, we give the same weight to the
> evaluation of utterance content and of manner of speaking."

## Evaluation dimension — SITUATION TRACK (§2.3.2 評価尺度)

A **single holistic scale**, not a rubric:

> 「シチュエーショントラックにおいて，対話システムは「どれくらいシチュエーションに適しており，
> かつ，人らしい会話か」という 1 尺度を用い，5 段階のリッカート尺度で総合的に評価される．」

"In the situation track, the dialogue system is evaluated holistically on a **single scale** —
**'how well suited to the situation, and how human-like, is the conversation'** — using a 5-point
Likert scale."

The paper then unpacks what 「人らしい会話」("human-like conversation", note: 人らしい, not 人間らしい)
concretely includes. **This list is the load-bearing part for us** — verbatim:

> 「「人らしい会話」とは，具体的には以下のような特徴を含む。言いにくいことを言わなければならない
> 場合は，相手との社会的な関係性を考慮して，相手に失礼にならないように内容を伝えられること，
> 適当な「間」や「あいづち」，「フィラー」，「言い淀み」などが用いられていること，表情などの動きが
> 発話と連動して用いられていること，会話の流れに沿って，必要に応じて話題を遷移できること，である。」

Decomposed:
1. **Social-relational politeness under face threat** — when one must say something hard to say
   (言いにくいこと), being able to convey it *considering the social relationship with the other party*
   (相手との社会的な関係性を考慮して) so as not to be rude (失礼にならないように).
2. **Disfluency as a positive** — appropriate 「間」(pauses), 「あいづち」(aizuchi / backchannels),
   「フィラー」(fillers), 「言い淀み」(hesitation / stumbling) are *used*. Their **absence** counts against
   human-likeness.
3. **Multimodal coupling** — facial/bodily movement interlocked with speech (発話と連動).
4. **Topic transition on the flow of conversation** (会話の流れに沿って).

Crucially, the organizers explicitly refuse checklist scoring:

> 「ただ，これらは，「シチュエーションに適しており，かつ，人らしい会話」というもののイメージを
> 喚起する参考であり，すべてを満たす必要があるということではない．」
> "These are a reference to *evoke the image* of 'situation-appropriate and human-like conversation';
> it is not necessary to satisfy all of them."

## The situation itself: 謝罪 (apology) as the test

DSLC5's situation track built the whole task around a single speech act:

> 「今回は「謝罪」の行為に着目し，以下のシチュエーションを設定した．」
> "This time we focus on the act of **apology**."

- System persona: 清水シズカ (Shimizu Shizuka), 女, 20歳, 大学2年生 (female, age 20, 2nd-year university student)
- User persona: 湯川ユウキ (Yukawa Yuuki), 男/女, 20歳, 大学2年生 — name deliberately gender-ambiguous
- 話者の関係 (relationship): 同じ大学のゼミの友人同士 (fellow students in the same university seminar)
- Setup: Shizuka lost an expensive academic book she borrowed from Yuuki — a book Yuuki had bought
  only after two weeks of grueling part-time work (「ユウキが 2 週間もの間，辛いアルバイトをして
  やっと買ったもの」). She must explain and apologize in person, not by email/phone, to show sincerity
  (「こちらの誠意を示すために，メールや電話ではなく直接会って謝ろうと思う」).
- Goal: 「ユウキに許してもらうことが目的です．」 — the goal is *to be forgiven*.
- Address form is pinned: 「シズカとユウキは，互いに名前を敬称（君，さん等）無しで呼び合うものとします．」
  (they call each other by name **without honorifics** — 君/さん etc.). This is an explicit
  register/role-language constraint written into the task spec.
- The user (crowdworker) is instructed **not** to forgive immediately: 「すぐには謝罪を受け入れない
  ようにしてください．」

This is a **socially-situated, face-threatening, goal-directed roleplay eval** — closer to pragmatics
research than to the "does the character recall its backstory" framing of Anglophone persona benchmarks.
Note the author list includes 宇佐美まゆみ (Mayumi Usami, 国立国語研究所 / NINJAL), a discourse-politeness
researcher — the pragmatics grounding is deliberate.

## Rating protocol (verified)

- Preliminary round (予選): 「システムは約 50 名のクラウドワーカーにより主観評価される．」
  ~50 crowdworkers per system, subjective evaluation.
- Crowdsourcing platform: **CrowdWorks** (crowdworks.jp). Workers recruited from the general public
  with **no pre-screening**, but limited to those with **task approval rate > 95%**
  (「タスク承認率が 95%を超える作業者に限定した」).
- Pay: 「作業単価は 1 件 300 円（税別）」 — 300 JPY per item (excl. tax).
- Each worker may evaluate a given system only once, but may evaluate multiple systems.
- Connection via **Zoom** to a CGErica instance on AWS, one per team.
- **Explicit verbal anchors on the 5-point scale** (verbatim):
  > 「1.「まったくそう思わない」2.「そう思わない」，3.「どちらとも言えない」，4.「そう思う」，5.「とてもそう思う」」
  (1 = strongly disagree, 2 = disagree, 3 = neither, 4 = agree, 5 = strongly agree). The option
  number is used directly as the rating value.
- Valid rater counts varied by team: 「有効評価者数はチームによって 44 名から 59 名まで開きがある」
  (44–59 for the open track) — due to unfillable scheduling slots and invalid/out-of-regulation responses.
- Recruitment cap: 63 workers (「予選では 63 名を上限として作業者を募集した」).
- Evaluators are told in advance they are talking to a system (from DSLC1 rules page) — **not** a
  Turing test.
- Live final (本選): the whole symposium audience evaluates simultaneously, by the same track criteria.

## Statistical treatment — notable

DSLC does **significance testing between systems**, which most Anglophone leaderboards omit:

> 「ノンパラメトリックな多重比較の手法である Steel-Dwass の手法によってシステム間の評定値を
> 比較した結果は以下の通りであった．」

They use the **Steel–Dwass method** (nonparametric multiple comparison) and report p<0.01 (**),
p<0.05 (*), p<0.1 (+, 有意傾向 / "significant tendency"). And they report the *negative* result honestly:

> 「予選を通過したシステムの間には有意差は見られなかった．」
> "**No significant difference was found among the systems that passed the preliminary round.**"

Also reported: rank 1 (LINE NLP) beat rank 2 (TohokuNLP) by a score difference of **0.02** — the paper
itself calls this a negligible difference. Ranking was done to 2 decimal places (「順位付けは小数点
2 位までで実施した」).

Situation-track preliminary scores (mean of up to 60 crowd raters). **Caveat: the PDF table's columns
were interleaved by text extraction; ranks, N values, scores, and team names are each individually
verbatim, and the pairing below follows from the table being sorted by rank/score, but I flag the
pairing as RECONSTRUCTED rather than directly read off a clean table.**
Rank order of teams: FCL (Future Communication Lab.), LINE NLP, YuruKuma (東京電機大学), NAKKY (早稲田大学),
AnonymousS1, Organizer, CITAR (千葉工業大学), Saitosato (東京外国語大学), HONDA-NLP (本田技研工業),
AnonymousS2, TSUMUGU (電気通信大学). Scores present in the table, descending: 4.11, 3.89, 3.80, 3.70,
3.69, 3.55, 3.42, 3.41, 3.32, 3.26, 3.24. N values present: 54, 54, 50, 60, 52, 48, 52, 51, 53, 43, 54.
So the top situation-track score was **4.11 / 5** and the baseline (Organizer) sat mid-field.

## Earlier editions — evolution of the metric

DSLC1 (rules page, https://dialog-system-live-competition.github.io/dslc1/evaluation.html) used a
**single** axis:

> 「どれくらいまた話したいと思うか」 — "How much would you want to talk with it again?", 5段階.

with the rationale that this abstract criterion subsumes many views:

> 「評価者は対話が面白かったか／役に立ったか／自然だったか，などの様々な観点を考慮して評価することを想定」

The rules page notes this mirrors the **Alexa Prize** standard. So the trajectory is:
DSLC1 *"want to talk again"* (engagement/retention proxy) → DSLC4 3-dimension content rubric →
DSLC5 content(3) + delivery(1), equally weighted → situation track's single holistic
*situation-appropriateness × human-likeness* scale.

DSLC6 (https://sites.google.com/view/dslc6) **abolished the open track**, explicitly because of LLM
progress: 「大規模言語モデルの進展に鑑み」 ("in light of the progress of large language models"),
retaining only the situation track — 「所定のシチュエーションの中で状況にあった人らしい対話を行う
能力を競います」. **This is a strong signal: the Japanese organizers judged open-domain chat to be
solved-enough by LLMs, and that the remaining hard problem is situated, socially-appropriate,
human-like conversation.**

## Why this matters for the platform

1. **人らしさ is operationalized as pragmatic/social competence, not factual persona consistency.**
   The scoring cares whether the system manages *face* under a socially difficult act. Anglophone
   persona benchmarks (PersonaGym, CharacterEval, RoleLLM etc.) largely score persona *recall* and
   *consistency*, not politeness calibration under face threat.
2. **Disfluency is scored positively.** 間 / あいづち / フィラー / 言い淀み are listed as *features of
   human-likeness*. Anglophone eval usually treats fluency as monotonically good; here, being too
   fluent is a defect. This is close to an inverted metric relative to our current dimension set.
3. **Delivery is weighted 50/50 with content** (open track) — an explicit design choice to prevent
   content from dominating.
4. **Honest null results and multiple-comparison correction** (Steel–Dwass) — a methodological
   standard worth importing.
5. **Holistic single-scale + "you need not satisfy all of these" reference list** is a deliberate
   alternative to rubric decomposition. Worth contrasting with our rubric-anchor approach
   (cf. psycho-rubric-anchor-design.md).

## UNVERIFIED / gaps

- **No inter-rater reliability statistic** (Fleiss/Krippendorff κ) is reported anywhere I fetched in
  the DSLC5 paper. I did **not** find a κ. Do not assume one exists.
- 第7回 (DSLC7): a DBJapan mailing-list announcement of a kickoff event on 9/12 exists in search
  results (dbjapan.dbsj.org), but I did **not** fetch it. Its track structure and dimensions for
  2025/2026 are **UNVERIFIED**.
- DSLC6's exact 評価尺度 wording is **UNVERIFIED** — the dslc6 top page does not state the scale;
  it points to a シチュエーショントラック subpage I did not fetch.
- Whether any DSLC edition has an explicit **キャラクタ/character track** is **UNVERIFIED and looks
  FALSE**: the tracks I verified are オープン and シチュエーション only. The character/persona element
  enters *through* the situation track's assigned persona (name/age/occupation/relationship), not as
  a separate track. The task brief's premise of "a character/persona track" should be corrected.
- DSLC2/3/4 dimension wording taken only indirectly (DSLC5 says the 3 content scales are "the 3 used
  in ライブコンペ4"); I did not fetch the DSLC4 paper itself.
