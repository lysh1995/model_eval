"""Loading role-play-bench, with the facts we measured about it baked in.

Shape (measured, not taken from the card): 95 characters (45 en / 50 zh), 11 models,
3 runs, exactly 102 turns each = 3,135 dialogues, ~320k turns. Balanced factorial, no
missing cells.

Two things the loader enforces, because both were mistakes waiting to happen:
  - `dialogue` is a JSON STRING, not an object. Double-parse.
  - data/_quarantine/ holds the dataset's PUBLISHED SCORES. The brief forbids using them.
    load() will not read that directory.
"""
from __future__ import annotations
import collections, hashlib, json, pathlib
from dataclasses import dataclass
from typing import Dict, Iterator, List, Optional, Tuple

from .core.registry import Dataset


@dataclass
class Seed:
    id: str
    ai_name: str
    ai_setting: str          # the character description -> {{character_description}}
    user_name: str
    user_setting: str
    ai_prologue: str         # turn 0, scripted
    initial_user_input: str  # user turn 0, scripted -- CARD-DERIVED BY CONSTRUCTION.
                             # Any leakage audit must exclude it (note 21 v1 did not).


@dataclass
class Dialogue:
    seed_id: str
    model_name: str
    run_id: str
    num_turns: int
    turns: List[dict]

    def ai_texts(self) -> List[str]:
        return [t["text"] for t in self.turns if t["role"] == "ai"]

    def user_texts(self, skip_scripted: bool = True) -> List[str]:
        return [t["text"] for t in self.turns
                if t["role"] == "user" and (t["round"] > 1 or not skip_scripted)]


class Corpus:
    def __init__(self, root: str = "data", lang: str = "en"):
        self.root = pathlib.Path(root); self.lang = lang
        self.seeds: Dict[str, Seed] = {}
        self.dialogues: List[Dialogue] = []

    def load(self, models: Optional[List[str]] = None,
             runs: Optional[List[str]] = None) -> "Corpus":
        sp = self.root / self.lang / "seeds.jsonl"
        dp = self.root / self.lang / "dialogues.jsonl"
        if not sp.exists() or not dp.exists():
            raise FileNotFoundError(
                f"corpus not found under {self.root}/{self.lang}/. Fetch it:\n"
                f"  see README.md -- it is gitignored (171MB) and redownloadable"
            )
        with sp.open() as f:
            for line in f:
                r = json.loads(line)
                self.seeds[r["id"]] = Seed(**{k: r[k] for k in Seed.__annotations__})
        with dp.open() as f:
            for line in f:
                r = json.loads(line)
                if models and r["model_name"] not in models: continue
                if runs and r["run_id"] not in runs: continue
                self.dialogues.append(Dialogue(
                    r["seed_id"], r["model_name"], r["run_id"], r["num_turns"],
                    json.loads(r["dialogue"]),          # a JSON STRING. double-parse.
                ))
        return self

    # -- views --------------------------------------------------------------
    def models(self) -> List[str]:
        return sorted({d.model_name for d in self.dialogues})

    def by_cell(self) -> Dict[Tuple[str, str], List[Dialogue]]:
        out = collections.defaultdict(list)
        for d in self.dialogues:
            out[(d.model_name, d.seed_id)].append(d)
        return dict(out)

    def dialogues_for(self, model: str, run: str = "run_1") -> Dict[str, list]:
        return {d.seed_id: d.turns for d in self.dialogues
                if d.model_name == model and d.run_id == run}

    def character_texts(self, model: str) -> Dict[str, List[str]]:
        """character -> all ai turns across runs. The unit for CORPUS metrics."""
        out = collections.defaultdict(list)
        for d in self.dialogues:
            if d.model_name == model:
                out[d.seed_id] += d.ai_texts()
        return dict(out)

    def dataset_id(self) -> Dataset:
        h = hashlib.sha256()
        for p in sorted((self.root / self.lang).glob("*.jsonl")):
            h.update(p.name.encode())
            h.update(str(p.stat().st_size).encode())     # cheap content proxy
        return Dataset("role-play-bench", h.hexdigest()[:16],
                       len(self.seeds), (self.lang,))

    def summary(self) -> str:
        cells = self.by_cell()
        runs = {len(v) for v in cells.values()}
        turns = {d.num_turns for d in self.dialogues}
        return (f"{self.lang}: {len(self.seeds)} characters x {len(self.models())} models "
                f"x {sorted(runs)} runs = {len(self.dialogues)} dialogues, "
                f"turns={sorted(turns)}")
