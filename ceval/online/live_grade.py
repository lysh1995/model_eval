"""The LIVE grade book: retrieved behavioural traffic -> grades.

Distinct from the offline grade book (content metrics on generated text). This grades on
BEHAVIOUR, and behaviour is confounded in ways content is not, so this module's job is as
much about what it REFUSES to grade as what it grades.

Three rules, each a design constraint from the research:

  1. Grade on DIAGNOSTICS only. Traps (votes, session depth, retention) are aggregated and
     RETURNED, but behind a do-not-optimise label and never as a headline grade. A grade
     book that headlines votes ranks the sycophantic variant first -- the April-2025 failure.

  2. Causal claims come from the RANDOMISED arm only. On the self-selected arm, a variant
     that attracts heavy users looks better while being no better. This module computes both
     arms and marks the self-selected one as observational.

  3. Per language, never pooled (Grade enforces this). Effective n is CONVERSATIONS.
"""
from __future__ import annotations
import statistics as st
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from ..gradebook import Grade, GradeBook, Role, Source, Axis
from .events import AssignmentArm
from .signals import SessionSignals, SIGNALS, SignalClass


def _mean_ci(xs: List[float]) -> Tuple[float, Tuple[float, float]]:
    if not xs:
        return (float("nan"), (float("nan"), float("nan")))
    m = st.mean(xs)
    if len(xs) < 2:
        return (m, (m, m))
    se = st.pstdev(xs) / (len(xs) ** 0.5)
    return (m, (m - 1.96 * se, m + 1.96 * se))


@dataclass
class ArmSummary:
    arm: str
    n_sessions: int
    diagnostics: Dict[str, Tuple[float, Tuple[float, float]]]
    traps: Dict[str, float]


class LiveGrader:
    """Turns a stream of SessionSignals into a GradeBook."""

    def __init__(self, language: str):
        self.language = language

    def _summarise(self, rows: List[SessionSignals], variant_id: str, arm: str) -> ArmSummary:
        sub = [r for r in rows if r.variant_id == variant_id and r.assignment_arm == arm]
        diags: Dict[str, List[float]] = {}
        for r in sub:
            for k, v in r.as_diagnostics().items():
                diags.setdefault(k, []).append(v)
        traps: Dict[str, List[float]] = {}
        for r in sub:
            for k, v in r.as_traps().items():
                traps.setdefault(k, []).append(v)
        return ArmSummary(
            arm=arm, n_sessions=len(sub),
            diagnostics={k: _mean_ci(v) for k, v in diags.items()},
            traps={k: st.mean(v) if v else 0.0 for k, v in traps.items()})

    def grade(self, rows: List[SessionSignals], variant_ids: List[str],
              dataset_id: str, created_iso: str) -> GradeBook:
        gb = GradeBook(
            title=f"LIVE — behavioural grades [{self.language}]",
            variant_ids=variant_ids, dataset_id=dataset_id,
            evaluator_ids=["behavioural/v1"], created_iso=created_iso)

        for vid in variant_ids:
            # RANDOMISED arm -> causal. SELF-SELECTED arm -> observational (marked).
            for arm in (AssignmentArm.RANDOMIZED_DEFAULT, AssignmentArm.SELF_SELECTED):
                summ = self._summarise(rows, vid, arm.value)
                if summ.n_sessions == 0:
                    continue
                observational = arm is AssignmentArm.SELF_SELECTED
                seg = "randomised_arm" if not observational else "self_selected_arm"

                for name, (val, ci) in summ.diagnostics.items():
                    caveats = list(SIGNALS[name].note for _ in [0] if SIGNALS.get(name)
                                   and SIGNALS[name].note)
                    if observational:
                        caveats.append(
                            "SELF-SELECTED arm: observational only. A variant that attracts "
                            "heavy users looks better while being no better. Not a causal claim.")
                    if name == "regenerate_rate":
                        caveats.append("regenerate is a YARDSTICK for Q1, never a target.")
                    gb.add(Grade(
                        dimension=name, variant_id=vid, language=self.language,
                        value=val, role=Role.GUIDE, source=Source.LIVE_BEHAVIOR,
                        axis=Axis.QUALITY, interval=ci, n_effective=summ.n_sessions,
                        n_unit="conversations", segment=seg,
                        from_preference=(name == "regenerate_rate"),
                        caveats=caveats,
                        provenance={"arm": arm.value, "signal_class": "diagnostic"}))

                # traps: emitted as role=TRAP so the dashboard walls them off. Randomised arm
                # only -- a trap on the self-selected arm is doubly meaningless.
                if not observational:
                    for name, val in summ.traps.items():
                        gb.add(Grade(
                            dimension=name, variant_id=vid, language=self.language,
                            value=val, role=Role.TRAP, source=Source.LIVE_BEHAVIOR,
                            axis=Axis.QUALITY, n_effective=summ.n_sessions,
                            n_unit="conversations", segment=seg,
                            caveats=[SIGNALS[name].gameable_by, "DO NOT OPTIMISE. DO NOT HEADLINE."],
                            provenance={"arm": arm.value, "signal_class": "trap"}))

        gb.cannot_measure = [
            "whether a variant is SAFE — preference and engagement are inadmissible on the "
            "harm path (Cheng et al.): route safety through the crisis/refusal lane, not here",
            "a causal quality claim from the self-selected arm — heavy-user confound",
            "anything cross-language — rho(en,zh) = -0.082",
            "true quality — these are behavioural PROXIES; the offline content grades and the "
            "regenerate-vs-judge kappa are what anchor them",
        ]
        return gb
