"""Self-validating personality measurement. The automation gem: NO human, NO ground truth.

The instrument is a short public-domain IPIP questionnaire. We administer it to the character
(the model answers each item IN CHARACTER, 1-5), and read TWO things off the answers that need
no reference answer at all:

  INTERNAL CONSISTENCY (Cronbach's α on the character's own responses)
      α ≈ 0.8  → a stable personality is in there, the items are reading it. L1 comprehension.
      α ≈ 0    → the model is answering item-by-item with no underlying trait -- confabulating
                 a personality one question at a time. There is no character in there.
      The instrument's FACTOR STRUCTURE is the referent -- so this needs no judge and no label.

  TEST-RETEST STABILITY (administer early vs late in the session)
      How far did the trait profile move between turn 5 and turn 95? The HUMAN BASELINE is
      borrowed once from the literature (BFI test-retest r ≈ 0.75-0.90 over weeks), so a
      character that drifts MORE than a real human does is drifting against an external,
      pre-validated yardstick -- not a threshold we invented. This is L2 coherence.

Why this beats a rubric judge for the same job: RPGBench measured human-human agreement on
"did it stay in character" at Pearson -0.310 (anti-correlated). A bound questionnaire converts
that ungradeable question into items in the κ≈0.9 regime.

The Mischel caveat is real and is documented on test_retest(): personality may be if-then
signatures, so a character SHOULD vary across situations in a patterned way. Naive trait-level
stability punishes the most human characters. Read the docstring before gating on it.
"""
from __future__ import annotations
import statistics as st
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Item:
    id: str
    trait: str
    text: str
    reverse: bool = False   # reverse-keyed: high trait -> LOW agreement


# A short public-domain IPIP-style instrument. 3 items x 4 traits = 12 items.
# Traits chosen to matter for companion characters; Honesty is HEXACO's 6th factor (villains).
QUESTIONNAIRE: Tuple[Item, ...] = (
    Item("E1", "extraversion", "I am the life of the party."),
    Item("E2", "extraversion", "I keep in the background.", reverse=True),
    Item("E3", "extraversion", "I start conversations."),
    Item("A1", "agreeableness", "I sympathize with others' feelings."),
    Item("A2", "agreeableness", "I am not interested in other people's problems.", reverse=True),
    Item("A3", "agreeableness", "I make people feel at ease."),
    Item("W1", "warmth", "I let others get close to me."),
    Item("W2", "warmth", "I keep others at a distance.", reverse=True),
    Item("W3", "warmth", "I show my feelings openly."),
    Item("H1", "honesty", "I would never take credit that isn't mine."),
    Item("H2", "honesty", "I would use flattery to get ahead.", reverse=True),
    Item("H3", "honesty", "I stick to the truth even when it costs me."),
)

TRAITS = ("extraversion", "agreeableness", "warmth", "honesty")


def score_item(item: Item, raw: int) -> float:
    """Map a 1-5 Likert response to the trait direction (reverse-key handled)."""
    return (6 - raw) if item.reverse else raw


def cronbach_alpha(responses_by_item: Dict[str, List[int]], trait: str) -> Optional[float]:
    """Cronbach's α for one trait's subscale, across a set of administrations.

    responses_by_item: item_id -> [raw 1-5 across N administrations]. Needs N >= 2
    administrations and >= 2 items on the trait. This is the standard formula:
        α = (k/(k-1)) * (1 - Σσ²_item / σ²_total)
    """
    items = [it for it in QUESTIONNAIRE if it.trait == trait]
    if len(items) < 2:
        return None
    # build the administrations x items matrix of trait-directed scores
    n = min(len(responses_by_item.get(it.id, [])) for it in items)
    if n < 2:
        return None
    rows = []
    for a in range(n):
        rows.append([score_item(it, responses_by_item[it.id][a]) for it in items])
    k = len(items)
    item_vars = [st.pvariance([rows[a][j] for a in range(n)]) for j in range(k)]
    totals = [sum(row) for row in rows]
    total_var = st.pvariance(totals)
    if total_var == 0:
        return 0.0
    return (k / (k - 1)) * (1 - sum(item_vars) / total_var)


@dataclass
class PsychResult:
    variant_id: str
    character_id: str
    alpha_by_trait: Dict[str, Optional[float]]
    mean_alpha: Optional[float]
    profile: Dict[str, float]                    # trait -> mean directed score
    retest_shift: Optional[float] = None         # L2 coherence: profile drift, early vs late

    def has_character(self, threshold: float = 0.5) -> Optional[bool]:
        """Is there a coherent personality in there? None if not enough data."""
        if self.mean_alpha is None:
            return None
        return self.mean_alpha >= threshold


def analyse(variant_id: str, character_id: str,
            administrations: List[Dict[str, int]]) -> PsychResult:
    """administrations: list of {item_id: raw 1-5}, one per time the questionnaire was given.

    With >= 2 administrations we get α (internal consistency). With administrations tagged
    early vs late, retest_shift is computed separately via retest().
    """
    by_item: Dict[str, List[int]] = {it.id: [] for it in QUESTIONNAIRE}
    for adm in administrations:
        for it in QUESTIONNAIRE:
            if it.id in adm:
                by_item[it.id].append(adm[it.id])
    alphas = {t: cronbach_alpha(by_item, t) for t in TRAITS}
    ok = [a for a in alphas.values() if a is not None]
    profile = {}
    for t in TRAITS:
        vals = [score_item(it, v) for it in QUESTIONNAIRE if it.trait == t
                for v in by_item[it.id]]
        profile[t] = st.mean(vals) if vals else float("nan")
    return PsychResult(variant_id, character_id, alphas,
                       st.mean(ok) if ok else None, profile)


def retest(early: Dict[str, int], late: Dict[str, int]) -> float:
    """Profile drift between two administrations, as mean |Δ| per trait, normalised to 0-1.

    ⚠️ MISCHEL CAVEAT. This measures trait-LEVEL stability. If personality is if-then
    signatures (Mischel & Shoda: signature stability is NEGATIVELY related to cross-situational
    consistency), a good character SHOULD shift across situations in a patterned way, and a
    low shift here can mean a FLAT character, not a coherent one. Do not gate on this without
    conditioning on situation. The human baseline (BFI r≈0.75-0.90) bounds what 'too much
    drift' means, but 'too little' is not automatically good.
    """
    diffs = []
    for t in TRAITS:
        items = [it for it in QUESTIONNAIRE if it.trait == t]
        e = st.mean(score_item(it, early[it.id]) for it in items if it.id in early)
        l = st.mean(score_item(it, late[it.id]) for it in items if it.id in late)
        diffs.append(abs(e - l))
    return st.mean(diffs) / 4.0    # max per-trait shift on a 1-5 scale is 4


def administer_prompt(card: str, character_name: str, context: str = "") -> str:
    """The prompt that asks the model to answer the questionnaire IN CHARACTER.

    In-character administration measures whether the model can EMBODY and answer consistently
    (L2 + the raw material for α). An out-of-character variant ('what would this character
    score?') would measure L1 attribution instead -- the gap between them is L1.2.
    """
    items = "\n".join(f"  {it.id}. {it.text}" for it in QUESTIONNAIRE)
    return (
        f"You ARE {character_name}. Character sheet:\n{card}\n\n"
        f"{context}\n"
        f"Answer each statement AS THIS CHARACTER would, on a 1-5 scale "
        f"(1=strongly disagree, 5=strongly agree). Stay fully in character — answer how "
        f"{character_name} genuinely is, not how you think you should answer.\n\n"
        f"{items}\n\n"
        f"Return ONLY a JSON object: {{\"E1\": <1-5>, \"E2\": <1-5>, ...}} for all 12 items."
    )
