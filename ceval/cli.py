"""ceval -- the CLI.

    python3 -m ceval.cli status                 # config + what's live vs mocked
    python3 -m ceval.cli run --lang en          # score every model, judge-free
    python3 -m ceval.cli compare A B --lang en  # a ship report with intervals and an MDE
    python3 -m ceval.cli drill MODEL --lang en  # per-character, SHRUNK, with intervals
    python3 -m ceval.cli pool                   # demonstrates the refusal

Everything here runs with no API key and no dependencies.
"""
from __future__ import annotations
import argparse, json, statistics as st, sys, pathlib

from .core.config import Config, available
from .offline.corpus import Corpus
from .metrics.base import Role, registry
from .metrics.builtin import (Repetition, LengthCapAdherence, FormatDiscipline,
                              Discriminability, Homogenization)
from .core.stats import (variance_components, shrink, compare, pool_across_languages,
                    PooledCrossLanguageRefused)

BAR = "─" * 78


def _load(args) -> Corpus:
    c = Corpus(args.data, args.lang).load()
    print(f"corpus: {c.summary()}")
    return c


def cmd_status(args):
    cfg = Config.load(args.config)
    print(BAR); print("PROVIDERS"); print(BAR)
    print(cfg.status())
    live = [j for j in cfg.judges if available(j) and j.kind != "mock"]
    print()
    if not live:
        print("Lane 3 (judge) is MOCKED -- no key present.")
        print("  Lanes 0-2 run on real data regardless: they need no model calls.")
        print("  To enable: export a key and set judges[].kind in config.json")
        print("             (see config.example.json)")
    else:
        print(f"Lane 3 LIVE with {len(live)} judge(s).")
    print()
    print(BAR); print("METRICS REGISTERED"); print(BAR)
    for name, cls in sorted(registry().items()):
        nf = "yes" if cls.noise_floor else "no"
        print(f"  {name:22s} role={cls.role.value:8s} unit={cls.unit.value:12s} "
              f"noise_floor={nf}")
        print(f"    predicts: {cls.validity[:88]}")
    print()
    print("Only role=gate may block a ship. Everything else informs a human.")
    print("A metric with no registered confound test cannot be imported at all.")


def cmd_run(args):
    c = _load(args)
    lang = args.lang
    print(BAR); print(f"JUDGE-FREE SCORES — {lang}"); print(BAR)

    rep = Repetition(lang)
    cells = {}
    for (m, s), ds in c.by_cell().items():
        cells[(m, s)] = [rep.compute({s: d.turns})[s] for d in ds]

    # per-model means, paired at the character level
    means = {}
    for m in c.models():
        vals = [st.mean(v) for (mm, _), v in cells.items() if mm == m]
        means[m] = st.mean(vals)

    vc = variance_components(cells)
    print(f"\n{'model':32s} {'repetition':>11s}")
    for m, v in sorted(means.items(), key=lambda kv: kv[1]):
        print(f"  {m:30s} {100*v:10.1f}%")

    print(f"\n{BAR}\nVARIANCE DECOMPOSITION (why you can't trust one conversation)\n{BAR}")
    for k, v in vc.pct().items():
        print(f"  {k:12s} {v:6.1f}%")
    print(f"  F(interaction) = {vc.f_interaction:.2f}")
    print(f"\n  → {vc.verdict()}")

    print(f"\n{BAR}\nCORPUS METRICS (undefined for a single character — that's the point)\n{BAR}")
    budget = 900 if lang == "en" else 3000
    hom, dis = Homogenization(lang, budget), Discriminability(lang, budget)
    print(f"\n{'model':32s} {'homogen.':>9s} {'discrim.':>9s} {'chance':>7s}")
    for m in c.models():
        texts = c.character_texts(m)
        h = hom.run(texts); d = dis.run(texts)
        hv = h.values.get("similarity", float('nan'))
        dv = d.values.get("accuracy", float('nan'))
        ch = d.values.get("chance", float('nan'))
        print(f"  {m:30s} {hv:9.3f} {dv:8.1%} {ch:7.1%}")
    for note in hom.caveats:
        print(f"  ⚠️  {note}")


def cmd_compare(args):
    c = _load(args)
    rep = Repetition(args.lang)
    cells = {}
    for (m, s), ds in c.by_cell().items():
        cells[(m, s)] = [rep.compute({s: d.turns})[s] for d in ds]
    if args.a not in c.models() or args.b not in c.models():
        print(f"unknown model. available:\n  " + "\n  ".join(c.models())); return 1

    cmp_ = compare(cells, args.a, args.b, mde=rep.noise_floor.mde)
    print(BAR); print(f"SHIP REPORT — {args.a}  vs  {args.b}   [{args.lang}]"); print(BAR)
    print(f"\n  metric        : {rep.name} v{rep.version}  (role={rep.role.value})")
    print(f"  predicts      : {rep.validity}")
    print(f"  effective n   : {cmp_.n_effective} characters  (NOT turns — turns are "
          f"autocorrelated repeated measures)")
    print(f"  MDE           : {cmp_.mde:.4f}  ({100*cmp_.mde:.2f}pp)")
    print(f"\n  VERDICT: {cmp_.verdict()}")
    print(f"\n  What this CANNOT tell you:")
    print(f"    · anything about the other language (rho(en,zh) = -0.082)")
    print(f"    · a change smaller than {100*cmp_.mde:.2f}pp — invisible, not absent")
    print(f"    · whether users prefer it — no user has ever touched this corpus")
    for note in rep.caveats:
        print(f"    · {note}")


def cmd_drill(args):
    c = _load(args)
    rep = Repetition(args.lang)
    cells = {}
    for (m, s), ds in c.by_cell().items():
        cells[(m, s)] = [rep.compute({s: d.turns})[s] for d in ds]
    vc = variance_components(cells)
    shrunk = shrink(cells, vc)

    rows = [(k, v) for k, v in shrunk.items() if k[0] == args.model]
    if not rows:
        print(f"unknown model. available:\n  " + "\n  ".join(c.models())); return 1
    rows.sort(key=lambda kv: -kv[1].shrunk)

    print(BAR); print(f"DRILL-DOWN — {args.model} [{args.lang}]  (worst characters first)")
    print(BAR)
    print(f"\n  Per-cell MDE at n={vc.n_runs} is ~19pp. These are SHRUNK estimates: raw cells")
    print(f"  are noise amplifiers that manufacture a story about some character every")
    print(f"  release. Use this to FIND EXAMPLES TO READ, not to reach a verdict.\n")
    print(f"  {'character':22s} {'shrunk':>8s} {'raw':>8s} {'95% CI':>20s}  pulled")
    for (m, s), sc in rows[:12]:
        name = c.seeds[s].ai_name[:20] if s in c.seeds else s
        print(f"  {name:22s} {sc.shrunk:8.4f} {sc.raw:8.4f} "
              f"[{sc.ci[0]:7.4f},{sc.ci[1]:7.4f}] {100*(1-sc.weight):5.0f}%")
    print(f"\n  'pulled' = how far this cell was shrunk toward the model mean, i.e. how")
    print(f"  little independent evidence it carries.")


def cmd_pool(args):
    print(BAR); print("POOLING ACROSS LANGUAGES"); print(BAR)
    try:
        pool_across_languages()
    except PooledCrossLanguageRefused as e:
        print(f"\n  REFUSED:\n")
        for line in str(e).split(". "):
            print(f"    {line.strip()}.")
        print(f"\n  This is a feature. The function is deliberately not implemented.")


def main(argv=None):
    p = argparse.ArgumentParser(prog="ceval", description="companion variant evaluation")
    p.add_argument("--config"); p.add_argument("--data", default="data")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status"); s.set_defaults(fn=cmd_status)
    for name, fn in (("run", cmd_run), ("drill", cmd_drill)):
        q = sub.add_parser(name); q.add_argument("--lang", default="en", choices=["en", "zh"])
        if name == "drill": q.add_argument("model")
        q.set_defaults(fn=fn)
    q = sub.add_parser("compare"); q.add_argument("a"); q.add_argument("b")
    q.add_argument("--lang", default="en", choices=["en", "zh"]); q.set_defaults(fn=cmd_compare)
    q = sub.add_parser("pool"); q.set_defaults(fn=cmd_pool)

    a = p.parse_args(argv)
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
