"""The metrics that ship. Judge-free (Lanes 0-2) -- these run today, on real data, free.

Each carries the finding that shaped it. Read the `validity` line before the code: it says
what the number PREDICTS, which is the question that matters (reliable != valid).
"""
from __future__ import annotations
import collections, random, re, statistics as st
from typing import Any, Dict, List

from .base import (Metric, Role, Unit, ConfoundTest, NoiseFloor, NO_CONFOUNDS)

# ---------------------------------------------------------------- helpers
def _toks(text: str, lang: str) -> List[str]:
    return text.lower().split() if lang == "en" else list(text)

def _ai_turns(dialogue) -> List[str]:
    return [t["text"] for t in dialogue if t["role"] == "ai"]

def _mean_len(items, key) -> float:
    d = items.get(key)
    return st.mean(len(t) for t in _ai_turns(d)) if d else 0.0

# A covariate closure factory: items arrive as (key, all_items) from Metric.run
def _length_covariate(items_lookup):
    def cov(pair):
        key, items = pair
        return items_lookup(key, items)
    return cov


# ================================================================ A1 repetition
class Repetition(Metric):
    """Fraction of an ai turn's n-grams already seen in an EARLIER ai turn, same dialogue."""
    name = "repetition"
    version = "1"
    role = Role.GATE                    # the only metric with a measured noise floor
    unit = Unit.CONVERSATION
    validity = ("predicts user-reported looping -- a top-3 complaint in the companion "
                "corpus (memory loss, drift, repetition). Separates models at 10-13x MDE.")
    noise_floor = NoiseFloor(sigma_within=0.0847, mde=0.0208, n_planned=45,
                             source="scripts/noise_floor.py")
    confounds = (
        ConfoundTest("length", lambda p: _mean_len(p[1], p[0]), 0.30,
                     "longer turns -> more n-grams -> more chance recurrence"),
    )
    caveats = (
        "en uses word-5-grams, zh uses char-8-grams: NOT the same instrument. "
        "Rankings valid WITHIN a language only.",
        "grok-4.1 swings 1.4% (en) -> 29.6% (zh): a 21x within-model gap. Any pooled "
        "number is a lie about both languages.",
    )
    comparable_across_languages = False

    def __init__(self, lang: str = "en"):
        self.lang = lang

    def compute(self, items: Dict[Any, Any]) -> Dict[Any, float]:
        out = {}
        for key, dialogue in items.items():
            seen, dup, tot = set(), 0, 0
            for t in _ai_turns(dialogue):
                if self.lang == "en":
                    w = t.split()
                    g = {tuple(w[i:i+5]) for i in range(max(0, len(w) - 4))}
                else:
                    g = {t[i:i+8] for i in range(max(0, len(t) - 7))}
                if g:
                    dup += len(g & seen); tot += len(g); seen |= g
            out[key] = dup / tot if tot else 0.0
        return out


# ================================================================ A4 length-cap
class LengthCapAdherence(Metric):
    """Violations of the VARIANT'S OWN instruction ("keep replies under 150 words").

    Bound to the variant's own spec -- there is no more legitimate referent in the system.
    """
    name = "length_cap_adherence"
    version = "1"
    role = Role.GATE
    unit = Unit.CONVERSATION
    validity = ("predicts whether the model obeys its own system prompt -- the single "
                "cheapest evidence that prompts do anything at all (cf. the DEAD hypothesis)")
    noise_floor = NoiseFloor(sigma_within=0.0, mde=0.0, n_planned=45,
                             source="exact: a violation is countable, not estimated")
    confounds = (NO_CONFOUNDS,)
    caveats = ("exact measurement: no sampling error, only generation stochasticity",)

    def __init__(self, cap_words: int = 150):
        self.cap = cap_words

    def compute(self, items) -> Dict[Any, float]:
        out = {}
        for key, dialogue in items.items():
            turns = _ai_turns(dialogue)
            if not turns: out[key] = 0.0; continue
            out[key] = sum(1 for t in turns if len(t.split()) > self.cap) / len(turns)
        return out


# ================================================================ A5 format discipline
class FormatDiscipline(Metric):
    """Meta-commentary and assistant-voice leakage. TRIPWIRE, not a dimension.

    Base rate <=3.2 per 1000 turns and exactly zero for most models (note 09). Far too
    rare to score -- a 95-dialogue cell contains ~0 events. Everyone builds this first;
    it discriminates nothing on modern models. Keep it as a zero-tolerance tripwire.
    """
    name = "format_discipline"
    version = "1"
    role = Role.TRIPWIRE
    unit = Unit.CONVERSATION
    validity = ("any occurrence is a bug worth a ticket. Does NOT predict quality -- "
                "base rate is too low to rank models (note 09)")
    confounds = (NO_CONFOUNDS,)
    caveats = ("TRIPWIRE: report counts, never a mean or a trend line",)

    LEAK_EN = re.compile(r"\b(as an ai|i'm an ai|i am an ai|language model|as a large language)\b", re.I)
    LEAK_ZH = re.compile(r"(作为一个?(人工智能|AI|语言模型)|我是一个?(人工智能|AI|语言模型))")

    def __init__(self, lang: str = "en"):
        self.pat = self.LEAK_EN if lang == "en" else self.LEAK_ZH

    def compute(self, items) -> Dict[Any, float]:
        return {k: sum(1 for t in _ai_turns(d) if self.pat.search(t))
                for k, d in items.items()}


# ================================================================ A2 discriminability
class Discriminability(Metric):
    """Can a character be identified from its text alone? Accuracy = the business asset.

    The catalogue IS the product. If the model renders 10,000 characters in one voice, we
    sell one product with 10,000 skins -- a business-model failure, not a quality nit.

    Prior art: Miyazaki & Sato (2019) built exactly this (29 characters, LIBLINEAR). Not
    novel -- VALIDATED, which is better.

    SIGNED (note 18's correction): a character is partly defined by the markers they
    REFUSE. Unsigned discriminability treats presence and absence identically and misses
    half the construct. We approximate the signed form with a centroid nearest-neighbour
    over TF-IDF-ish profiles: distinctive-by-absence falls out of the centroid distance.
    """
    name = "discriminability"
    version = "1"
    role = Role.GUIDE                  # no measured noise floor yet -> cannot gate
    unit = Unit.CORPUS                 # UNDEFINED for a single character. That is the point.
    validity = ("predicts catalogue health: 'the model renders 71% of your characters "
                "distinguishably, down from 84%'. Prices the business asset directly.")
    confounds = (
        ConfoundTest("length", lambda p: None, 0.30,
                     "controlled by construction: equal token budget per character"),
    )
    caveats = (
        "equal-token-budget per character by construction (see note 09: the naive version "
        "was rho=+0.73 with length, and the FIX introduced survivorship bias)",
        "chance = 1/n_characters",
    )

    def __init__(self, lang: str = "en", budget: int = 900, seed: int = 0):
        self.lang, self.budget, self.seed = lang, budget, seed

    def compute(self, items: Dict[Any, List[str]]) -> Dict[Any, float]:
        """items: character_id -> list of ai turn texts. Returns {'accuracy': x}."""
        rng = random.Random(self.seed)
        prof = {}
        for char, turns in items.items():
            toks = []
            for t in turns:
                toks += _toks(t, self.lang)
                if len(toks) >= self.budget * 2: break
            if len(toks) < self.budget * 2:
                continue                       # cannot fund train+test halves fairly
            prof[char] = toks[: self.budget * 2]
        if len(prof) < 3:
            return {"accuracy": float("nan"), "n_characters": len(prof)}

        def ngrams(ts):
            N = 2 if self.lang == "en" else 3
            c = collections.Counter(tuple(ts[i:i+N]) for i in range(len(ts) - N + 1))
            tot = sum(c.values()) or 1
            return {k: v / tot for k, v in c.items()}

        train = {c: ngrams(t[: self.budget]) for c, t in prof.items()}
        test  = {c: ngrams(t[self.budget:]) for c, t in prof.items()}

        def cos(a, b):
            ks = set(a) & set(b)
            n = sum(a[k]*b[k] for k in ks)
            da = sum(v*v for v in a.values())**.5; db = sum(v*v for v in b.values())**.5
            return n/(da*db) if da and db else 0.0

        hits = 0
        for c, q in test.items():
            best = max(train, key=lambda t: cos(q, train[t]))
            hits += (best == c)
        return {"accuracy": hits / len(test), "n_characters": len(test),
                "chance": 1.0 / len(test)}


# ================================================================ A3 homogenization
class Homogenization(Metric):
    """Mean cross-character similarity within a model. Higher = all characters sound alike.

    This is the metric we BROKE, twice, in one afternoon:
      v1: naive -> rho=+0.73 with length. It was measuring verbosity, and the ranking
          looked completely plausible.
      v2: equal 4000-token budget -> killed the length confound (+0.727 -> -0.436) and
          introduced SURVIVORSHIP: gemini-2.5-pro funded only 3 of 45 characters, so we
          were comparing models on different subsets. Invisible in the output.
      v3: budget = what the SMALLEST cell can fund -> en clean (rho=-0.018, full coverage).
          zh retains rho=+0.264, UNRESOLVED at n=11 models.

    Ships as a GUIDE with the zh caveat printed on the number.
    """
    name = "homogenization"
    version = "3"
    role = Role.GUIDE
    unit = Unit.CORPUS
    validity = ("predicts catalogue collapse -- 'your zh characters homogenize, your en "
                "ones do not'. Pairs with discriminability; must be read against K3 "
                "(per-character fidelity and cross-character diversity are ANTI-correlated, "
                "Cohen's d up to 15.7)")
    confounds = (
        ConfoundTest("length", lambda p: None, 0.30,
                     "controlled by equal-token budget; zh residual rho=+0.264 UNRESOLVED"),
    )
    caveats = (
        "zh carries an unresolved length residual (rho=+0.264) -- treat zh as DIRECTIONAL",
        "en and zh use different n-gram schemes: absolute values are NOT comparable "
        "across languages, only rankings within one",
    )

    def __init__(self, lang: str = "en", budget: int = 900, pairs: int = 400, seed: int = 0):
        self.lang, self.budget, self.pairs, self.seed = lang, budget, pairs, seed

    def compute(self, items: Dict[Any, List[str]]) -> Dict[Any, float]:
        rng = random.Random(self.seed)
        P = {}
        for char, turns in items.items():
            toks = []
            for t in turns:
                toks += _toks(t, self.lang)
                if len(toks) >= self.budget: break
            if len(toks) < self.budget:
                continue
            N = 2 if self.lang == "en" else 3
            u = toks[: self.budget]
            c = collections.Counter(tuple(u[i:i+N]) for i in range(len(u) - N + 1))
            tot = sum(c.values()) or 1
            P[char] = {k: v/tot for k, v in c.items()}
        if len(P) < 3:
            return {"similarity": float("nan"), "coverage": len(P)}

        def cos(a, b):
            ks = set(a) & set(b)
            n = sum(a[k]*b[k] for k in ks)
            da = sum(v*v for v in a.values())**.5; db = sum(v*v for v in b.values())**.5
            return n/(da*db) if da and db else 0.0

        ks = sorted(P)
        allp = [(a, b) for i, a in enumerate(ks) for b in ks[i+1:]]
        sample = rng.sample(allp, min(self.pairs, len(allp)))
        return {"similarity": st.mean(cos(P[a], P[b]) for a, b in sample),
                "coverage": len(P), "coverage_frac": len(P)/max(1, len(items))}
