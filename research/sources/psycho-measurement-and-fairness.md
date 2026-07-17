---
title: "Measurement and Fairness"
url: https://arxiv.org/abs/1912.05511
authors: Abigail Z. Jacobs, Hanna Wallach
year: 2021
venue: ACM FAccT '21
type: paper
accessed: 2026-07-16
topic: psychometrics
---

# Measurement and Fairness (Jacobs & Wallach, FAccT 2021)

## Core thesis

Proposes **measurement modeling** from the quantitative social sciences as a framework for
understanding fairness in computational systems.

Computational systems routinely involve **unobservable theoretical constructs** — socioeconomic
status, teacher effectiveness, risk of recidivism. Verbatim: "Such constructs cannot be measured
directly and must instead be inferred from measurements of observable properties."

A **measurement model** statistically links unobservable theoretical constructs (operationalized as
latent variables) with observable properties. This necessarily involves assumptions about how
constructs relate to measurable data.

Key claim: "many of the harms studied in the literature on fairness in computational systems are
direct results of such mismatches" between theoretical constructs and their operationalizations.

## Reliability

**Test-retest reliability**: whether measurements of the same construct at different time points
yield consistent results, assuming the construct itself has not changed. Illustrated with
teacher-effectiveness models producing dramatically variable scores between years — a red flag
indicating measurement problems, not real changes in teachers.

## The seven components of construct validity

### 1. Face validity
Whether measurements "look plausible — a 'sniff test' of sorts." Subjective, but a prerequisite for
the other aspects of validity.

### 2. Content validity
Three sub-aspects:
- **Contestedness** — whether the construct has multiple competing theoretical understandings.
- **Substantive validity** — whether the operationalization incorporates the appropriate observable
  properties.
- **Structural validity** — whether it captures the relationships between the incorporated
  variables.

### 3. Convergent validity
Verbatim: "the extent to which measurements obtained from a measurement model correlate with other
measurements of the same construct, obtained from measurement models for which construct validity
has already been established."

### 4. Discriminant validity
Whether measurements inadvertently capture unrelated constructs; measurements should correlate with
other constructs only in proportion to the actual relationships between those constructs.

### 5. Predictive validity
Whether measurements predict relevant observable properties **not incorporated** into the
operationalization. Addresses *utility* rather than *meaning*.

### 6. Hypothesis validity
Whether measurements support substantively interesting hypotheses about the construct.

### 7. Consequential validity
Verbatim: "concerned with identifying and evaluating the consequences of using the measurements
obtained from a measurement model, including any societal impacts." Asks: **what world do the
measurements bring into being?**

## Relevance to companion-eval

Every subjective dimension we score ("creativity", "character consistency", "empathy") is an
unobservable theoretical construct. The rubric IS the measurement model. Contestedness is the first
thing to nail down: if two people on the team mean different things by "creativity", no amount of
inter-rater reliability tooling will save the dimension.
