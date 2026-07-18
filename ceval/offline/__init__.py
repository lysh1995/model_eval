"""The offline testing system, as three delivered components:

  1. TEST TARGETS   variants (model + params + system prompt) — see variants defined by the
     generation harness; scored subjects are real Claude Sonnet output under 3 system prompts.
  2. TEST SCHEME    scheme.py — the declarative dimension catalogue (level × lane), the
     6-filter method for DECIDING dimensions, cases, validation, and score calculation.
     psychometric.py — the self-validating personality instrument (α, test-retest).
     provider.py — judge/psychometric backends (subagent | simulated).
  3. PLATFORM       runner.py — variant + scheme -> GradeBook; the dashboard renders it with
     cross-variant comparison.
"""
from .scheme import SCHEME, Dimension, Level, Lane, FILTERS, decide_dimension, by_level, summary
from .psychometric import QUESTIONNAIRE, analyse, retest, cronbach_alpha, administer_prompt
from .provider import make_provider, SimulatedProvider, SubagentProvider
from .runner import load_run, run, reconstruct, OfflineRun
