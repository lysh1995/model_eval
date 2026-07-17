---
title: "Symmetry-Aware LLM-Driven Generation and Repair of Interactive Fiction Graphs in Twine/Twee"
url: https://doi.org/10.3390/sym18010113
authors: (MDPI Symmetry 18(1):113; author list not retrieved — mdpi.com returns HTTP 403 to automated fetch)
year: 2026
type: paper
accessed: 2026-07-16
topic: game-simulation
---

# Symmetry-Aware Generation and Repair of Interactive Fiction Graphs (Symmetry, Jan 2026)

⚠️ **Provenance caveat: mdpi.com 403s automated fetch; content below is from the abstract via search indexing and a secondary listing, NOT from a full-text read.** Treat every claim as unverified. MDPI *Symmetry* is a low-selectivity venue. **Do not cite this as evidence for anything.** It is here for one architectural idea, which stands on its own logic regardless of the paper's quality.

⚠️ Also note: an earlier search attributed the symmetry/asymmetry formalism to **GENEVA** (Leandro et al., IEEE CoG 2024). **That attribution is wrong** — the terms do not appear in GENEVA's text (verified by extracting GENEVA's PDF). GENEVA is a branching-narrative *generation and visualization* tool with no such formalism. Recorded here so nobody re-derives the error.

## The concept

> "Symmetric convergence captures situations in which multiple branches with compatible narrative states legitimately reconverge, while asymmetric convergence reveals **structurally invalid merges of incompatible states**."

The canonical failure it names: *entering a scene in which an item or companion is present, via a path where they were never acquired or met.* This is the branching-narrative version of a canon violation, and it is **decidable**.

## ⭐ The method — and the trick that makes it work

The system pairs LLM generation with "formal analysis of the resulting narrative graph and an iterative repair loop."

Failure modes they report from LLM-generated Twine: "missing passages, trap-like cycles without exits, dead-end passages, narrative discontinuities, incorrect use of Twine macro commands, and **inconsistent handling of story variables**."

**The key move:**

> "they deliberately **abandon all macro- and variable-based logic** and instead **encode story state directly within passage names** through structured, token-based naming."

Then: "algorithms to detect **naming-based asymmetries, cycles, unreachable endings, and structurally defective branches**," fed into "a repair loop that prompts the LLM to rewrite missing or inconsistent parts."

Result claim (vague, no numbers): "Experiments with several LLM backends indicate that this approach **can yield** structurally robust and locally coherent interactive stories by reducing state inconsistencies and structural defects."

**No precision/recall, no counts, no baseline, no human validation.** The claim is qualitative.

## Relevance to companion-eval-platform

**The idea is worth more than the paper.** Strip it to the principle:

> **Make state structural, and consistency checking stops being a judgment and becomes an algorithm.**

They got a *deterministic, free, 100%-precision* consistency checker — but only by paying for it in representation: they forced state into the graph's own naming, giving up expressiveness so that a graph walk could decide compatibility. Precision came from constraint, not from cleverness.

**This defines the axis our whole design sits on**, and it maps directly onto note 11's lane structure:

| Representation | Checker | Precision | Expressiveness | Note-11 lane |
|---|---|---|---|---|
| State encoded in graph structure (this paper) | graph algorithm | ~100% (by construction) | very low — authored branches only | Lane 1 (deterministic) |
| State as typed JSON w/ code oracle (ByteSized32-SP) | exact match | ~100% vs oracle | low — enumerable objects | Lane 1 |
| State as extracted triples (Zep/Graphiti) | LLM edge comparison | **unmeasured** | medium | Lane 3 (judge) |
| State as free prose (our dialogues) | LLM/NLI auditor | ? — see note 13 | full | Lane 3 |

**Our product lives at the bottom row and cannot move up** — we cannot make users author a Twine graph or a JSON schema. So we do **not** inherit these papers' precision. Every "objective world-state" result in this literature buys its objectivity with a representational constraint we can't impose.

**But the axis is a lever, not just a constraint.** Two live options:
1. **Move a slice of our eval up the table.** For an *evaluation* scenario (not production traffic), we control the character card and the seed. We could author scenarios with a small set of **pre-declared trackable facts** — a typed mini-schema (inventory, location, relationship flags, injuries) — and get a Lane-1 checker on that slice. It gives up generality and gains a mechanical ground truth. **This is the single most promising design in this review** — it is the ByteSized32 trick applied to roleplay, and it is how we escape the α=0.3 trap without pretending our auditor is more accurate than it is.
2. Accept the bottom row and measure the auditor's error rate honestly (note 13).

**These are not exclusive — (1) is how you validate (2).** An authored-schema slice provides the *labeled set* against which the free-prose auditor's precision/recall can be measured. That is the bootstrap, and it resolves the "who audits the auditor" problem without a large human labeling spend.
