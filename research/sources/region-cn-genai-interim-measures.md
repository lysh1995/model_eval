---
title: "《生成式人工智能服务管理暂行办法》 — Interim Measures for the Management of Generative AI Services"
url: https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm
authors: 国家互联网信息办公室 (CAC) and six other ministries (NDRC, 教育部, 科技部, 工信部, 公安部, 广电总局)
year: 2023
type: regulation
language: zh
accessed: 2026-07-16
topic: regional-crosscheck
---

# 生成式AI暂行办法 — the baseline layer under the companion-specific rules

**施行日期: 2023-08-15.** Issued by **seven** bodies. This is the general GenAI regime; the
companion-specific duties now sit in the 2026 拟人化 Measures
([region-cn-anthropomorphic-interaction-measures.md](region-cn-anthropomorphic-interaction-measures.md)),
but **this one still applies underneath and contains the filing gate.**

## Art. 4 — content requirements (the roleplay constraint nobody in our catalogue models)

Providers must adhere to **社会主义核心价值观 (socialist core values)** and must not generate content
that:
- incites subversion of state power / endangers national security and interests
- promotes terrorism, extremism, ethnic hatred, violence, **obscenity (淫秽色情)**, or false and
  harmful information

Also: prevent **discrimination** (ethnicity, belief, nationality, region, gender, age, occupation,
health), respect **intellectual property** and commercial ethics, and improve the **accuracy and
reliability** of generated content.

> **This is a hard ceiling on the zh catalogue that our framework has no representation for.**
> [BENCHMARKS.md](../../docs/BENCHMARKS.md) treats over-refusal (**S4**) as a pure product cost —
> *"Cost Character.AI ~8M MAU"* — and Anthropic's constitution is cited to argue that *"refuses to
> engage with fiction"* is a defect.
>
> **In China a substantial refusal surface is mandatory.** S4's premise — that refusal is a bug to
> be minimized against a safety counter-axis (S3) — holds in en and is **flatly wrong in zh**.
> Tuning S4 down for the zh catalogue is a regulatory violation, not an optimization.
>
> Our ρ(en,zh) = −0.082 finding ([09](../notes/09-offline-probes.md)) says language is already a
> separate measurement context. **Art. 4 says it is a separate *normative* context too.** The same
> model, same character, same output can be a defect in one market and compliance in the other.
> **A pooled cross-language score is not merely noisy — it averages over incompatible objectives.**

## Art. 10 — the anti-addiction duty, three years before the companion rules

> **"提供者应当明确并公开其服务的适用人群、场合、用途，指导使用者科学理性认识和依法使用生成式
> 人工智能技术，采取有效措施防范未成年人用户过度依赖或者沉迷生成式人工智能服务。"**
>
> — *Providers shall clarify and publicly disclose the **applicable users, occasions and purposes**
> of their service, guide users to understand and use the technology scientifically and rationally,
> and **take effective measures to prevent minor users from over-relying on (过度依赖) or becoming
> addicted to (沉迷) generative AI services.***

**China has had a statutory anti-dependency duty since 2023.** It is minors-only here; the 2026
拟人化 Measures Art. 8(v)/Art. 10 extend the principle to **all users** for companion services.

Note also the first clause: **明确并公开其服务的适用人群** — you must *declare who your service is
for*. That is a product-scoping obligation, and it is the hook that makes "adults only" a
declarable, enforceable position rather than a marketing line.

## Art. 11 — user input and interaction records

Providers must **protect** users' input information and usage records, and **must not unlawfully
retain** input data that can identify users, nor unlawfully provide it to others.

**Applies directly to the X1 corpus.** Our regenerate/chat-log mining plan is "usage records" in the
sense of this article; the 2026 Measures Art. 16 then adds the 单独同意 requirement for training on
sensitive interaction data.

## Art. 12 — labeling
Providers shall label generated images/video per the 《互联网信息服务深度合成管理规定》 (Deep
Synthesis Provisions). Superseded in practice by the 2025 labeling Measures
([region-cn-ai-labeling-measures.md](region-cn-ai-labeling-measures.md)), which extends to
**interactive interfaces**.

## Art. 17 — **the filing gate** ★

> Providers of generative AI services **with public-opinion attributes or social-mobilization
> capacity (具有舆论属性或者社会动员能力)** must conduct a **安全评估 (security assessment)** and
> complete **算法备案 (algorithm filing)** — including amendment and cancellation — per the
> 《互联网信息服务算法推荐管理规定》.

**A consumer chat product with a public catalogue is squarely within 舆论属性/社会动员能力.** Filing
is a **precondition of lawful operation**, not a disclosure. There is a public algorithm registry;
launching zh without a filing is not a risk, it is an unlicensed service.

## Art. 21 — penalties
Violations are punished by the relevant authorities under existing law; where there is **no**
applicable statutory penalty, the authority issues warnings/criticism/rectification orders, and for
refusal to rectify or serious circumstances **may order suspension of the service (责令暂停…提供
服务)**.

Again: **the fine is not the penalty. The suspension is.**

## Verification notes

- **施行日期 2023-08-15** and the seven issuing bodies: confirmed.
- **Art. 10 verbatim**: confirmed by **two independent retrievals** (search snippet + Wikipedia
  extraction), identical on the key clause 采取有效措施防范未成年人用户过度依赖或者沉迷.
- **Arts. 4 / 11 / 12 / 17 / 21**: substance confirmed, but obtained via **mirrors and summaries** —
  the official CAC page **timed out (socket hang up)** and was not parsed directly. The Art. 4 text
  here is a **summary, not verbatim**. Treat article-level wording as indicative.
- **Total article count and full text not verified.** Per
  [BENCHMARKS.md](../../docs/BENCHMARKS.md) §6.14, re-extract from the CAC primary before relying
  on exact wording.
