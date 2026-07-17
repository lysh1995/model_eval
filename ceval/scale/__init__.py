"""Scale. C2: 'demonstrate your design holds at that volume with real numbers.'

Every number carries provenance: MEASURED (timed here, real data) / BORROWED (a published
price) / ASSUMED (a guess about production we cannot check). A cost model built from
citations is an essay; one built from measurements is a demonstration.
"""
from .units import Provenance, Quantity, Benchmark, TokenProfile, Price, count_tokens, time_it
from .costmodel import CostModel, Workload, TierPlan, CostLine
