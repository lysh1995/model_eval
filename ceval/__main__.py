"""The platform CLI. One entry point for the whole evaluation service.

    python3 -m ceval                 # run the full service: offline + online -> dashboard
    python3 -m ceval --offline-only  # pre-launch only
    python3 -m ceval --sim           # use the simulated judge (no real Claude recordings)

INPUT  (mock variants)  ->  DOMAIN (dimensions + scoring)  ->  OUTPUT (dashboard)
"""
from __future__ import annotations
import argparse, pathlib, sys
from datetime import datetime, timezone

from .service import EvalService
from .dashboard import render
from .offline import SCHEME


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ceval", description="companion variant evaluation service")
    ap.add_argument("--gen-dir", default="out/gen")
    ap.add_argument("--tasks", default="out/gen/tasks.json")
    ap.add_argument("--out", default="out/platform_dashboard.html")
    ap.add_argument("--offline-only", action="store_true")
    ap.add_argument("--sim", action="store_true", help="simulated judge instead of real recordings")
    ap.add_argument("--sessions", type=int, default=1500)
    a = ap.parse_args(argv)

    now = datetime.now(timezone.utc).isoformat()
    svc = EvalService("en")
    provider = "simulated" if a.sim else "recorded"

    print("─" * 68)
    print("EVALUATION SERVICE")
    print("  INPUT  : variants (prompts + model) exercised offline"
          + ("" if a.offline_only else " + online (faked traffic)"))
    print(f"  DOMAIN : {len(SCHEME)} dimensions across L1/L2/L3/safety · judge={provider}")
    print("  OUTPUT : one dashboard")
    print("─" * 68)

    offline_gb, offline_run = svc.evaluate_offline(a.gen_dir, a.tasks, now, provider)
    profiles = svc.ability(offline_run)
    print(f"  offline: {len(offline_gb.grades)} grades over {offline_gb.variant_ids}")

    online_gb = None
    if not a.offline_only:
        online_gb = svc.evaluate_online(offline_run.variant_ids, now, n_sessions=a.sessions)
        print(f"  online : {len(online_gb.grades)} grades from {2*a.sessions} faked sessions")

    merged = svc.merge(offline_gb, online_gb, now)
    merged.title = "Companion variant evaluation — one platform, offline + online"
    path = render(merged, a.out, ability_profiles=profiles, scheme=SCHEME)
    p = pathlib.Path(path)
    if "<title>" not in p.read_text():
        p.write_text("<title>Companion Variant Evaluation</title>\n" + p.read_text())
    print("─" * 68)
    print(f"  {merged.to_dict()['counts']}  ->  {path}")
    print("─" * 68)
    return 0


if __name__ == "__main__":
    sys.exit(main())
