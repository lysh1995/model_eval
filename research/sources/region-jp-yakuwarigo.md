---
title: "発話テキストへのキャラクタ性付与のための音変化表現の分類 (Classification of Phonological Changes Reflected in Text: Toward a Characterization of Written Utterances)"
url: https://www.jstage.jst.go.jp/article/jnlp/26/2/26_407/_article/-char/ja/
authors: 宮崎千明 (Chiaki Miyazaki), 佐藤理史 (Satoshi Sato) — 名古屋大学大学院工学研究科 / Nagoya University
year: 2019
type: paper
language: ja
accessed: 2026-07-16
topic: regional-crosscheck
---

# 役割語 (yakuwarigo / role language) and キャラクタ性 (character-ness) in Japanese NLP

Journal: 自然言語処理 (Journal of Natural Language Processing), Vol. 26, No. 2, pp. 407–440,
published 2019-06-15. Full PDF: https://www.jstage.jst.go.jp/article/jnlp/26/2/26_407/_pdf
(fetched and extracted with pdfminer.six; all Japanese below is verbatim from that PDF).

**This answers the task's core question: yes, 役割語 is used in Japanese NLP character generation and
evaluation, and it yields a dimension the Anglophone literature lacks.**

## The 役割語 concept, as NLP researchers actually cite it

From §1 はじめに, verbatim:

> 「物語でも対話エージェントでも，それぞれのキャラクタの発話には，それぞれのキャラクタらしさが
> 表れる．特定の人物像（キャラクタ）と結びついた話し方の類型は役割語 (金水 2011a) と呼ばれ，
> 「老人語」「幼児語」「お嬢様言葉」など，どのようなキャラクタがどのような表現を使うのか，文法的な
> 特徴はあるか (金水 2011b) などについて，様々な研究が行われてきた．」

"In both narratives and dialogue agents, each character's utterances exhibit that character's
character-ness (キャラクタらしさ). A **type of speech style bound to a specific persona (character)
is called 役割語 (role language)** (Kinsui 2011a), and much research has been done on which
characters use which expressions — 「老人語」(old-man language), 「幼児語」(infant language),
「お嬢様言葉」(young-lady speech) — and on whether they have grammatical characteristics."

役割語 is Kinsui Satoshi's (金水敏, Osaka University) concept, introduced in Kinsui (2000) and
popularized by 『ヴァーチャル日本語 役割語の謎』(Virtual Japanese: The Mystery of Role Language,
Iwanami Shoten, 2003). Kinsui gave an invited talk at 言語処理学会 NLP2013 titled 「役割語研究の現在」
(https://www.anlp.jp/nlp2013/talk_kinsui.pdf) — i.e. the concept was **formally introduced to the
Japanese NLP community from the linguistics side**. (The talk abstract page was surfaced in search;
I did **not** fetch the talk PDF itself — its contents are UNVERIFIED.)

Note the paper explicitly names **りんな (Rinna)** as motivation for character-bearing agents:

> 「近年は，ユーザの命令に従ってタスクを実行したり，会話をしたりする対話エージェントにおいても，
> エージェントのキャラクタが重視されるようになり，マイクロソフトの「りんな」をはじめとして，
> 特定のキャラクタを冠した対話エージェントが数多く作られている．」

"In recent years, the character of the agent has come to be emphasized even in dialogue agents ...
and many dialogue agents bearing a specific character have been created, starting with Microsoft's
**Rinna**." — Direct evidence the Japanese academic and product lines are coupled.

## The research programme: two generations

**Generation 1 — 文末表現 (sentence-final expressions) / function-word lexical choice.** The authors'
prior work converted e.g. 「これはひどいな」→「これはひどいわね」 (Miyazaki, Hirano, Higashinaka,
Makino, and Matsuo 2015; 宮崎・平野・東中・牧野・松尾・佐藤 2016). Note **東中 (Higashinaka)** is
also the DSLC organizer — the same small community runs the competition and the character work.

They then state its **limitation**, verbatim:

> 「しかしながら，機能語の語彙選択による表現力には限界がある．具体的な課題としては，性別や年代と
> いった大まかなキャラクタらしさを表現することはできても，それ以上に細かなキャラクタらしさを
> 表現することが難しい点が挙げられる．」

"However, expressive power via function-word lexical choice has limits. Concretely: while it can
express **coarse** character-ness such as **gender and age bracket**, expressing character-ness
finer than that is difficult."

Worked example given: changing 「これはひどいな」's final 「な」 to 「や」 → 「これはひどいや」 conveys
roughly "somewhat masculine" and "probably not elderly", but a finer adjustment like
「もう少し粗野な感じにしたい」 ("I want it a bit more coarse/rough") is hard.

**Generation 2 — 音変化表現 (phonological-change expressions rendered in text).** e.g.
「こりゃひでえや」 from 「これはひどいや」; 「ひでえ」 vs 「ひどーい」 evoke different speakers.

## The taxonomy (verified)

Collected sound-change expressions from character utterances and organized them into
**137 patterns** (137 種類のパターン), a three-level hierarchy:

- 大分類 (major class): **L1–L11**
- 中分類 (middle class): **M1–M34**
- パターン (pattern): **P1–P137**

Major classes with section headings in the paper (L1–L9 verbatim):

| Code | Japanese | Translation |
|---|---|---|
| L1 | 長音挿入 | long-vowel insertion (e.g. ひどーい) |
| L2 | 促音挿入 | geminate (sokuon) insertion |
| L3 | 撥音挿入 | moraic-nasal insertion |
| L4 | 脱落 | deletion |
| L5 | 母音交替 | vowel alternation (e.g. ひどい→ひでえ) |
| L6 | 子音交替 | consonant alternation |
| L7 | 促音化 | gemination |
| L8 | 撥音化 | nasalization |
| L9 | ウ音便化 | u-onbin (u-euphonic change) |
| L10 | 縮約 | contraction — *named in §5.2 discussion, no section heading extracted* |
| L11 | **UNVERIFIED** | the paper's feature description says the major classes run L1–L11, but I could only verify names for L1–L10. L11's label is unknown to me. |

Coverage claim (verbatim from the abstract):

> 「これらのパターンが小説やコミックで用いられる音変化表現の 80%以上をカバーすることを確認した．」
> "We confirmed that these patterns cover **more than 80%** of the phonologically changed expressions
> used in novels and comics."

## The evaluation experiment (§5 発話のキャラクタ付けにおける音変化表現の有用性検証)

Design — **character-ness is validated by speaker identifiability**, which is a genuinely different
evaluation move:

- Data: **9 works** (9 作品), **29 characters** (excluding an 「その他」/other bucket), **200 utterances
  per work** (各作品 200 発話).
- Task: detect a given character's utterances among the 200.
- Model: **LIBLINEAR version 2.1** logistic regression with **L2 regularization**; **10-fold
  cross-validation**; detection threshold = probability **≥ 0.5**.
- Morphological analysis: **MeCab 0.996** with **UniDic (unidic-mecab ver. 2.1.2)**.
- Metrics: 再現率 (Recall), 適合率 (Precision), F 値 (F-measure).
- Three feature sets:
  - **Word** — surface morphemes + frequency
  - **Word+POS** — surfaces + POS + frequency
  - **Word+POS+Pattern** — the above + frequencies of detected L1–L11 / M1–M34 / P1–P137

Honest caveat the authors themselves raise: UniDic POS tags already encode some sound-change
information (e.g. 「連体形-撥音便」 as in 走んの, 「仮定形-融合」 as in 食べりゃ), so Word+POS is not a
clean control.

**Results (verbatim-sourced, do not extrapolate):**

> 「検出結果はキャラクタによってまちまちだが，いくつかのキャラクタにおいて，音変化表現の情報を
> 使うことで F 値が向上した．最も向上したのは『図書館戦争』の柴崎麻子で，形態素の表記と品詞を
> 用いる方法 (Word+POS) に音変化表現の情報を追加する（Word+POS+Pattern を用いる）ことで，
> F 値が 0.15 向上した．」

"Detection results **varied by character**, but for **several** characters, using sound-change
information **improved F**. The largest improvement was **柴崎麻子 (Shibasaki Mako) of 『図書館戦争』
(Library War), whose F improved by 0.15**" when adding pattern features to Word+POS.

> 「『ソードアートオンライン』については，対象としたキャラクタの全てにおいて，音変化表現の情報を
> 用いる方法 (Word+POS+Pattern) の F 値が最も高かった．」
> "For 『ソードアートオンライン』(Sword Art Online), Word+POS+Pattern had the highest F for **all**
> target characters."

Precision-recall curves: for Library War and SAO characters, Word+POS+Pattern is "概ね常に"
(almost always) highest-precision **in the recall ≥ 0.3 range**. Note the hedge — this is a
conditional, not a blanket, claim.

**The most interesting finding for us — character-ness by ABSENCE:** inspecting the top-15
largest-|weight| features of the logistic regression:

> 「堂上淳のモデル（重みの絶対値の上位 15 件）において音変化表現の情報に対する重みが全て負の値と
> なっていることである．これは，堂上淳というキャラクタが，L4（脱落）や L1（長音挿入）といった，
> ごく一般的な音変化表現をあまり用いない人物として特徴づけられていることを示唆している．」

For 堂上淳 (Dōjō Atsushi, Library War), **every** sound-change weight in the top 15 is **negative** —
the character is defined by *not* using very common sound changes. Same pattern for 茅場晶彦
(Kayaba Akihiko, SAO): negative weights on L4 (脱落) and L2 (促音挿入). Contrast クライン (Klein, SAO),
whose pattern weights are **all positive** — L5 (母音交替), L10 (縮約), M10 (語末の「う」の脱落) — an
actively coarse speaker.

Authors' conclusion: 「本研究で提案する音変化表現のパターンが発話のキャラクタらしさを特徴づけるうえで
有用であることが示されたと言える．」

## Why this is a dimension Anglophone work lacks

1. **役割語 makes character-ness a *lectal* property, not a biographical one.** Anglophone persona
   benchmarks (PersonaGym, CharacterEval, RoleLLM, CharacterBench, InCharacter…) overwhelmingly score
   *what the character knows/claims/does* — backstory recall, factual consistency, MBTI-style trait
   attribution. 役割語 scores **how the character's grammar and phonology encode a social type**.
   Japanese grammaticalizes this: first-person pronoun (私/僕/俺/わし/あたし/わたくし), sentence-final
   particles (わ/ぜ/ぞ/のう/じゃ), copula (だ/です/じゃ/や) each independently index gender, age,
   class, region, and era. English has *some* of this (dialect, register) but it is not a closed,
   enumerable, grammaticalized system, so Anglophone eval never had to build the dimension.
2. **Character-ness is measurable as speaker identifiability**, not as judge preference. A held-out
   classifier asks: can the character be picked out of a lineup from their speech alone? This is
   cheap, LLM-judge-free, and has an obvious drift analogue — *persona drift = declining speaker
   identifiability over turns*. Compare multiturn-persona-drift.md / multiturn-incharacter.md.
3. **Negative evidence counts.** A character can be defined by markers they *refuse*. A naive
   "does it use the character's speech quirks" metric scores 堂上淳 as characterless; the regression
   correctly reads him as *marked by restraint*. Any 役割語 dimension we build must be signed
   (deviation from a baseline in both directions), not a presence-count.
4. **Coarse vs fine granularity is an explicit, named problem.** The authors state function words get
   you gender/age only. That's a calibration warning for any "speech style consistency" metric: it
   will saturate at demographic stereotype unless it reaches phonology-in-orthography.
5. **The stereotype hazard is documented in the same literature.** 小林美恵子「役割語における「差別」を
   考える」 (surfaced in search; **NOT fetched — UNVERIFIED**) treats 役割語 as encoding social
   discrimination. Operationalizing 役割語 as a *reward* signal risks rewarding stereotype fidelity.
   This tension (character authenticity vs stereotype amplification) is a real design question and is
   basically absent from Anglophone roleplay eval, which treats persona fidelity as unambiguously good.

## UNVERIFIED / gaps

- **No inter-rater reliability statistic** is reported in this paper. I searched the extracted text
  for カッパ / κ / kappa / 一致率 / 一致度 / Fleiss / Cohen — **zero hits**. Annotation used 「2 名の作業者」
  (2 workers) for building the verification data, but no agreement coefficient is given. **Do not
  attribute a κ to this paper.**
- The exact 9 works and full 29-character list were not extracted (they are in 表 1, which I did not
  read). Only 『図書館戦争』 and 『ソードアートオンライン』 are confirmed as included.
- **Per-character F values are in 図 4 (a figure), not a table** — so I have *no* per-character
  numbers beyond the +0.15 delta for 柴崎麻子, which is stated in running text. Absolute F values are
  **UNVERIFIED**.
- L11's label is **UNVERIFIED** (see taxonomy table above).
- Kinsui 2011a / 2011b are cited by this paper but I did **not** fetch them; the 役割語 definition
  above is as *relayed by* Miyazaki & Sato, which is a reliable secondary use but not the primary text.
- Whether 役割語 features appear in any **modern LLM-era Japanese roleplay benchmark** is
  **UNVERIFIED** — I found no such benchmark. This 2019 paper predates the LLM roleplay-eval wave.
  Searches for a yakuwarigo-based LLM benchmark returned only linguistics/culture material and
  language-learning blog content, no benchmark. This looks like a **genuine open gap**, i.e. an
  opportunity, not just a hole in my search.
