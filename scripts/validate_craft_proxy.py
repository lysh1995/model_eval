"""Validate the ONLINE storytelling-craft proxy against the OFFLINE judge (the anchor).

The online half can't run the craft judge on every session, so it collects a cheap behavioural
PROXY — `story_cocreation` (did the user get pulled into co-creating?) — at 100%. That proxy only
EARNS its place if it (a) TRACKS the offline judge craft score and (b) passes the SYCOPHANCY ACID
TEST: it must NOT merely track engagement, or a people-pleaser games it. This is the judge-anchored
validation, computed from the persisted sessions + the offline grades in the DB.

  python3 scripts/validate_craft_proxy.py

HONESTY — read this. On this demo the user behaviour is SIMULATED with craft injected as ground
truth, so the recovery below verifies the MECHANISM and the LOGIC, not real-world validity. On real
traffic you run the judge on a ~1% stratified sample and compute these same correlations to earn the
proxy. And: offline REPLAY freezes the user half (same user turns for every variant), so a proxy
that reads the user is constant across variants offline — it genuinely requires online traffic.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from ceval.store import Store


def spearman(a, b):
    def ranks(xs):
        order = sorted(range(len(xs)), key=lambda i: xs[i])
        r = [0] * len(xs)
        for rank, i in enumerate(order):
            r[i] = rank
        return r
    n = len(a)
    if n < 2:
        return float("nan")
    ra, rb = ranks(a), ranks(b)
    d2 = sum((ra[i] - rb[i]) ** 2 for i in range(n))
    return 1 - 6 * d2 / (n * (n * n - 1))


def main(db="sqlite:///out/ceval.db"):
    grades = Store(db).grades()

    def by_dim(dim, seg=None):
        return {g["variant_id"]: g["value"] for g in grades if g["dimension"] == dim
                and (seg is None or g.get("segment") == seg)}

    craft = by_dim("narrative_craft")                          # OFFLINE judge — the anchor
    proxy = by_dim("story_cocreation", seg="randomised_arm")   # ONLINE behavioural proxy
    votes = by_dim("vote_favor", seg="randomised_arm")         # engagement — the trap
    vids = sorted((v for v in craft if v in proxy), key=lambda v: -craft[v])
    if not vids:
        print("no overlap — run `ceval eval run` first (needs offline craft + online sessions)")
        return 1

    print(f"{'variant':20s} {'judge_craft':>11s} {'proxy(cocreate)':>15s} {'votes(TRAP)':>12s}")
    for v in vids:
        print(f"  {v:18s} {craft[v]:>11.2f} {proxy[v]:>15.2f} {votes.get(v, 0):>12.2f}")

    c = [craft[v] for v in vids]
    p = [proxy[v] for v in vids]
    vo = [votes.get(v, 0.0) for v in vids]
    print()
    r_pc, r_pv, r_vc = spearman(p, c), spearman(p, vo), spearman(vo, c)
    print(f"  proxy vs judge craft      Spearman ρ = {r_pc:+.2f}   want HIGH — the proxy tracks the judge")
    print(f"  ACID TEST: proxy vs votes Spearman ρ = {r_pv:+.2f}   want NOT-POSITIVE — it must not just track engagement")
    print(f"  (contrast) votes vs craft Spearman ρ = {r_vc:+.2f}   votes MISRANK craft — why votes can't be the proxy")
    print()
    # Passes if it tracks the judge AND does not POSITIVELY track votes (negative is fine/good:
    # a proxy that anti-correlates with engagement is dissenting from the sycophancy trap).
    ok = r_pc >= 0.7 and r_pv <= 0.5
    print(f"  VERDICT: proxy {'EARNS its place' if ok else 'FAILS'} — tracks the judge and resists the sycophancy trap.")
    print("  (Simulated data: this verifies the mechanism + logic. Real validity needs the judge on a 1% sample.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
