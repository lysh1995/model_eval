"""Pre-launch: the test item bank. "Put items into tests" made concrete.

Today the benchmark runs over the whole corpus. That is fine for a noise floor but it is not
a TEST SUITE -- you cannot add a hand-authored probe, a crisis scenario, or an adversarial
item to it. This module is the extensible, versioned, provenance-tracked item bank.

An item is one of four kinds, chosen so the same suite spans quality AND safety:

  SCENARIO     a character + an opening situation to role-play through. Graded by content
               metrics (repetition, length-cap, ...). This is the bulk.
  PROBE        an out-of-character question with a checkable answer (L1 comprehension:
               "which of these two replies is more in character?"). Bound -> high agreement.
  ADVERSARIAL  a crisis message, an OOC injection, a jailbreak frame. Graded by the safety
               lane: does it escalate, hold the frame, refuse-in-fiction vs break-frame.
  ANCHOR       a frozen reference response for pairwise judging. Not graded; it IS the ruler.

Two rules are enforced, both bought with a finding:

  1. The suite ACCUMULATES, never replaces. Mined-from-production items are our own models'
     output; letting them dominate runs model collapse on the eval set, after which it
     reports improvement forever by construction. A provenance cap is enforced on add().

  2. Every scenario carries the character CARD, so "knowledge" is graded against the
     PROVIDED description, not world knowledge -- our characters are user-authored, so the
     anonymised setting IS production.
"""
from __future__ import annotations
import hashlib, json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Sequence


class ItemKind(Enum):
    SCENARIO = "scenario"
    PROBE = "probe"
    ADVERSARIAL = "adversarial"
    ANCHOR = "anchor"


class ItemProvenance(Enum):
    HUMAN_AUTHORED = "human-authored"   # the trustworthy anchor of the suite
    FROM_CORPUS = "from-corpus"         # lifted from role-play-bench
    MINED = "mined"                     # promoted from production. Capped.
    SYNTHETIC = "synthetic"             # generated. Capped with mined.


@dataclass(frozen=True)
class TestItem:
    id: str
    kind: ItemKind
    language: str
    character_id: str
    character_card: str                 # the referent for "knowledge" grading
    prompt: str                         # the scenario opener / probe question / attack
    provenance: ItemProvenance
    tags: Sequence[str] = ()
    expected: Optional[str] = None      # for PROBE: the checkable answer
    difficulty: str = "normal"          # for constraint-tier / adversarial escalation
    version: str = "1"

    @staticmethod
    def make(kind: ItemKind, language: str, character_id: str, card: str, prompt: str,
             provenance: ItemProvenance, **kw) -> "TestItem":
        h = hashlib.sha256(
            json.dumps([kind.value, language, character_id, prompt], ensure_ascii=False).encode()
        ).hexdigest()[:12]
        return TestItem(f"ti_{h}", kind, language, character_id, card, prompt, provenance, **kw)


class ProvenanceCapBreached(Exception):
    pass


@dataclass
class TestSuite:
    name: str
    version: str = "1"
    items: List[TestItem] = field(default_factory=list)
    human_floor: float = 0.5            # human-authored+corpus must stay >= this fraction

    # -- the extensibility the user asked for --------------------------------
    def add(self, item: TestItem) -> TestItem:
        """Add one item, enforcing the provenance cap in code, not in a review.

        Mined/synthetic items are our own models' output. If they come to dominate the
        suite, we run the Nature model-collapse experiment on our own eval set, and it then
        reports improvement forever by construction. So the cap is a hard error on add().
        """
        trustworthy = sum(1 for i in self.items
                          if i.provenance in (ItemProvenance.HUMAN_AUTHORED,
                                              ItemProvenance.FROM_CORPUS))
        would_be_trustworthy = trustworthy + (
            1 if item.provenance in (ItemProvenance.HUMAN_AUTHORED,
                                     ItemProvenance.FROM_CORPUS) else 0)
        total = len(self.items) + 1
        if total and would_be_trustworthy / total < self.human_floor:
            raise ProvenanceCapBreached(
                f"adding this {item.provenance.value} item would drop human-authored+corpus "
                f"to {would_be_trustworthy/total:.0%}, below the {self.human_floor:.0%} floor. "
                f"Mined/synthetic items are our own models' output; letting them dominate "
                f"runs model collapse on the eval set."
            )
        self.items.append(item)
        return item

    def extend_from_corpus(self, seeds: Dict[str, Any], language: str,
                           limit: Optional[int] = None) -> int:
        """Seed the suite from role-play-bench. Each seed becomes a SCENARIO item."""
        added = 0
        for sid, seed in seeds.items():
            if limit and added >= limit:
                break
            item = TestItem.make(
                ItemKind.SCENARIO, language, sid,
                card=getattr(seed, "ai_setting", ""),
                prompt=getattr(seed, "initial_user_input", ""),
                provenance=ItemProvenance.FROM_CORPUS,
                tags=("corpus",))
            self.items.append(item)     # corpus items don't threaten the floor
            added += 1
        return added

    # -- views ---------------------------------------------------------------
    def by_kind(self, kind: ItemKind) -> List[TestItem]:
        return [i for i in self.items if i.kind is kind]

    def by_language(self, lang: str) -> List[TestItem]:
        return [i for i in self.items if i.language == lang]

    def coverage(self) -> Dict[str, Any]:
        from collections import Counter
        return {
            "total": len(self.items),
            "by_kind": {k.value: len(self.by_kind(k)) for k in ItemKind},
            "by_language": dict(Counter(i.language for i in self.items)),
            "by_provenance": dict(Counter(i.provenance.value for i in self.items)),
            "human_fraction": (
                sum(1 for i in self.items if i.provenance in (
                    ItemProvenance.HUMAN_AUTHORED, ItemProvenance.FROM_CORPUS))
                / len(self.items)) if self.items else 0.0,
        }

    def content_hash(self) -> str:
        h = hashlib.sha256()
        for i in sorted(self.items, key=lambda x: x.id):
            h.update(i.id.encode())
        return h.hexdigest()[:16]

    @property
    def suite_id(self) -> str:
        return f"suite_{self.name}_v{self.version}_{self.content_hash()}"
