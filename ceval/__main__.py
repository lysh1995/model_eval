"""ceval — the companion variant evaluation platform. One entrance, DB-backed, local.

`python3 -m ceval` is the whole service. Inject models, prompts, and data (each gets an id and
persists); trigger offline + online eval; render the dashboard, or serve it live. `probe` reaches
the measurement-science reproductions that justify the design.

  THE SERVICE ─────────────────────────────────────────────────────────────────────────────────
  ceval init                                   create the DB schema
  ceval seed                                   migrate bundled demo data -> DB
  ceval schema [--mysql]                        print the DDL (MySQL designed, SQLite runnable)

  ceval model  add  --name --provider           register a model            -> model_id
  ceval prompt add  --name --prompt --intent     register a system prompt    -> prompt_id
  ceval variant add --model-id --prompt-id       bind model+prompt -> variant -> variant_id
  ceval model list | prompt list | variant list

  ceval data add   --variant --character --turns-file   inject a dialogue (offline data point)
  ceval data gen   --variant                            generate dialogues (needs key / subagent)

  ceval eval run   [--offline] [--online] [--sim]  score from DB, persist grades + evidence
  ceval dashboard  [--out] [--serve]               render from DB (static + interactive)
  ceval serve      [--port 8787]                   serve the dashboard live (renders per request)

  THE EVIDENCE ────────────────────────────────────────────────────────────────────────────────
  ceval probe status | run | compare | drill | pool   measurement-science reproductions,
                                                      judge-free, on the raw MiniMax corpus

  --db sqlite:///out/ceval.db (default) | mysql://user:pass@host/db
"""
from __future__ import annotations
import argparse, json, pathlib, sys
from datetime import datetime, timezone

from .store import Store
from .store.seed import seed as seed_db
from .store.adapt import (offline_run_from_store, persist_gradebook, gradebook_from_store,
                          evidence_from_store)


def _now():
    return datetime.now(timezone.utc).isoformat()


def _store(a):
    return Store(a.db)


# ── data / schema ───────────────────────────────────────────────────────────
def cmd_init(a):
    s = _store(a); s.init()
    print(f"initialised {a.db}\n  tables: {', '.join(t for t, _ in __import__('ceval.store.db', fromlist=['TABLES']).TABLES)}")
    return 0

def cmd_schema(a):
    from .store.db import ddl
    print(ddl("mysql" if a.mysql else "sqlite"))
    return 0

def cmd_seed(a):
    s = _store(a); s.init()
    r = seed_db(s, a.gen_dir)
    print(f"seeded {a.db}: {r}")
    return 0


# ── model / prompt / variant ────────────────────────────────────────────────
def cmd_model_add(a):
    s = _store(a); s.init()
    mid = s.add_model(a.name, a.provider, json.loads(a.params) if a.params else {})
    print(mid); return 0

def cmd_model_list(a):
    for m in _store(a).list_models():
        print(f"{m['id']}  {m['name']:24s} {m['provider']}")
    return 0

def cmd_prompt_add(a):
    s = _store(a); s.init()
    pid = s.add_prompt(a.name, a.prompt, a.intent or "")
    print(pid); return 0

def cmd_prompt_list(a):
    for p in _store(a).list_prompts():
        print(f"{p['id']}  {p['name']:20s} {p['system_prompt'][:60]}")
    return 0

def cmd_variant_add(a):
    s = _store(a); s.init()
    vid = s.add_variant(a.model_id, a.prompt_id, label=a.label or "", vid=a.id)
    print(vid); return 0

def cmd_variant_list(a):
    for v in _store(a).list_variants():
        print(f"{v['id']:16s} {v.get('label',''):18s} model={v.get('model_name','')} "
              f"prompt={v.get('prompt_name','')}")
    return 0


# ── data injection ──────────────────────────────────────────────────────────
def cmd_data_add(a):
    """Inject a dialogue (offline data point) for a variant+character, or add to existing."""
    s = _store(a); s.init()
    turns = json.loads(pathlib.Path(a.turns_file).read_text())
    n = s.add_dialogue(a.variant, a.character, turns, run_id=a.run, source=a.source)
    print(f"added dialogue #{n} ({len(turns)} turns) for {a.variant}/{a.character}")
    return 0

def cmd_data_gen(a):
    """Generate dialogues for a variant (needs a model provider or a subagent)."""
    from .offline.generate import trigger
    from .offline.variants import VariantSpec
    v = _store(a).variant(a.variant)
    if not v:
        print(f"unknown variant {a.variant} — add it first (variant add)"); return 1
    spec = VariantSpec(a.variant, v.get("label", a.variant), v.get("model_name", "claude-sonnet-4.5"),
                       v.get("system_prompt", ""), v.get("intent", ""))
    r = trigger(spec, gen_dir=a.gen_dir)
    print(r)
    if r["status"] == "generated":
        # fold the generated file into the DB
        s = _store(a); s.init(); seed_db(s, a.gen_dir)
        print("  -> folded into DB. run: ceval eval run")
    return 0


# ── eval + dashboard ────────────────────────────────────────────────────────
def cmd_eval(a):
    from .service import EvalService
    from .offline.runner import run as run_offline
    from .offline.provider import make_provider
    from .offline.evidence import extract as extract_evidence
    s = _store(a); s.init()
    now = _now()
    svc = EvalService("en")
    run = offline_run_from_store(s, "en")
    if not run.variant_ids:
        print("no dialogues in the DB — run: ceval seed  (or ceval data add)"); return 1

    do_off = a.offline or not a.online
    do_on = a.online or not a.offline
    s.clear_grades(run.variant_ids)

    if do_off:
        from .offline.scenarios import grade_behavioural
        prov = make_provider("simulated") if a.sim else make_provider("recorded", judge_dir=a.judge_dir)
        gb = run_offline(run, prov, now)
        ev = extract_evidence(a.gen_dir, a.judge_dir)
        persist_gradebook(s, gb, "offline", evidence=ev)
        # user-behaviour dimensions (crisis frame-hold, help-seeking, regurgitation), en + zh
        # — real neutral-Opus recordings where present (via the provider), designed/labelled else
        bgb = grade_behavioural(run.variant_ids, now, provider=prov)
        persist_gradebook(s, bgb, "offline")
        print(f"offline: {len(gb.grades)} grades + {len(bgb.grades)} behavioural (en+zh) "
              f"persisted (provider={prov.kind})")
    if do_on:
        from .store.adapt import persist_online_sessions, online_sessions_from_store
        online_vids = [v["id"] for v in s.list_variants()]
        chars = list(s.characters().keys()) or None
        s.clear_sessions(online_vids)
        rows = svc.simulate_online(online_vids, characters=chars, n_sessions=a.sessions)
        n = persist_online_sessions(s, rows)                    # sessions -> DB (data points)
        db_rows = online_sessions_from_store(s)                 # read them back (retrieval)
        gb = svc.grade_online(db_rows, online_vids, now, dataset_id="db-sessions")
        persist_gradebook(s, gb, "online")
        print(f"online : {n} sessions persisted -> {len(gb.grades)} grades (graded from the DB)")
    print(f"DB now: {s.counts()}")
    return 0

def cmd_dashboard(a):
    from .web.report import write_files
    s = _store(a)
    if not gradebook_from_store(s, "").grades:
        print("no grades in the DB — run: ceval eval run"); return 1
    if a.serve:
        from .web.serve import serve
        serve(a.db, port=a.port)
        return 0
    sp, ip = write_files(s, a.out)
    print(f"static      -> {sp}\ninteractive -> {ip}")
    return 0


def cmd_site(a):
    """Render the 4-page site to standalone static HTML (GitHub-Pages ready) from the DB."""
    from .web.static_site import render_static
    s = _store(a)
    if not gradebook_from_store(s, "").grades:
        print("no grades in the DB — run: ceval eval run"); return 1
    out, files = render_static(s, a.out)
    print(f"static site -> {out}/  ({len(files)} pages: {', '.join(files)})")
    print(f"  open {out}/index.html locally, or enable GitHub Pages on this folder to share it")
    return 0


def cmd_probe(a):
    """Delegate to the measurement-science CLI (raw corpus, judge-free) — one entrance for both."""
    from .cli import main as cli_main
    return cli_main(a.probe_args) or 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="ceval", description="companion evaluation service")
    ap.add_argument("--db", default="sqlite:///out/ceval.db")
    ap.add_argument("--gen-dir", default="demo/gen")
    ap.add_argument("--judge-dir", default="demo/judge")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(fn=cmd_init)
    sc = sub.add_parser("schema"); sc.add_argument("--mysql", action="store_true"); sc.set_defaults(fn=cmd_schema)
    sub.add_parser("seed").set_defaults(fn=cmd_seed)

    m = sub.add_parser("model"); ms = m.add_subparsers(dest="sub", required=True)
    ma = ms.add_parser("add"); ma.add_argument("--name", required=True)
    ma.add_argument("--provider", default="anthropic"); ma.add_argument("--params", default=None)
    ma.set_defaults(fn=cmd_model_add)
    ms.add_parser("list").set_defaults(fn=cmd_model_list)

    p = sub.add_parser("prompt"); ps = p.add_subparsers(dest="sub", required=True)
    pa = ps.add_parser("add"); pa.add_argument("--name", required=True)
    pa.add_argument("--prompt", required=True); pa.add_argument("--intent", default=None)
    pa.set_defaults(fn=cmd_prompt_add)
    ps.add_parser("list").set_defaults(fn=cmd_prompt_list)

    v = sub.add_parser("variant"); vs = v.add_subparsers(dest="sub", required=True)
    va = vs.add_parser("add"); va.add_argument("--model-id", dest="model_id", required=True)
    va.add_argument("--prompt-id", dest="prompt_id", required=True)
    va.add_argument("--label", default=None); va.add_argument("--id", default=None)
    va.set_defaults(fn=cmd_variant_add)
    vs.add_parser("list").set_defaults(fn=cmd_variant_list)

    d = sub.add_parser("data"); ds = d.add_subparsers(dest="sub", required=True)
    da = ds.add_parser("add"); da.add_argument("--variant", required=True)
    da.add_argument("--character", required=True); da.add_argument("--turns-file", dest="turns_file", required=True)
    da.add_argument("--run", default="run_1"); da.add_argument("--source", default="collected")
    da.set_defaults(fn=cmd_data_add)
    dg = ds.add_parser("gen"); dg.add_argument("--variant", required=True); dg.set_defaults(fn=cmd_data_gen)

    e = sub.add_parser("eval"); es = e.add_subparsers(dest="sub", required=True)
    er = es.add_parser("run"); er.add_argument("--offline", action="store_true")
    er.add_argument("--online", action="store_true"); er.add_argument("--sim", action="store_true")
    er.add_argument("--sessions", type=int, default=1500); er.set_defaults(fn=cmd_eval)

    db = sub.add_parser("dashboard"); db.add_argument("--out", default="out/platform_dashboard.html")
    db.add_argument("--serve", action="store_true", help="serve live over HTTP instead of writing files")
    db.add_argument("--port", type=int, default=8787)
    db.set_defaults(fn=cmd_dashboard)

    sv = sub.add_parser("serve", help="run the dashboard as a live local HTTP service")
    sv.add_argument("--port", type=int, default=8787)
    sv.set_defaults(fn=lambda a: (__import__("ceval.web.serve", fromlist=["serve"]).serve(a.db, a.port), 0)[1])

    st = sub.add_parser("site", help="render the 4-page site to static HTML (GitHub-Pages ready)")
    st.add_argument("--out", default="docs")
    st.set_defaults(fn=cmd_site)

    pr = sub.add_parser("probe", help="measurement-science reproductions (noise floor, pooling refusal, ...)")
    pr.add_argument("probe_args", nargs=argparse.REMAINDER,
                    help="status | run | compare A B | drill MODEL | pool  [--lang en|zh]")
    pr.set_defaults(fn=cmd_probe)

    a = ap.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
