"""Local HTTP server — the platform as a live 4-page site, rendered FRESH FROM THE DB.

stdlib http.server, no dependencies. The loop is: edit data / `ceval eval run` (or the ② Run
form) -> refresh -> new data. Pages, not a static file:

  /            ① Data     models · prompts · offline dialogues · online behaviour sessions
  /run         ② Run      the CLI + a live form: pick model+prompt -> trigger eval -> output
  /compare     ③ Compare  the cross-compare grade book (headline = storytelling craft)
  /variant?id= ④ Detail   drill into one variant from ③
  /static      the single-page static dashboard (renders anywhere / email)
  /api/grades.json · /api/variants.json · /healthz

Bind is 127.0.0.1 (local only) by design.
"""
from __future__ import annotations
import io, json, contextlib
from types import SimpleNamespace
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

from .store import Store
from .report import build_html, _prep
from . import site


def _make_handler(db_url: str):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):  # quiet
            pass

        def _send(self, body: bytes, ctype="text/html; charset=utf-8", code=200):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")  # always live
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            u = urlparse(self.path)
            path = u.path.rstrip("/") or "/"
            try:
                store = Store(db_url)   # fresh connection per request (thread-safe for sqlite)
                if path in ("/", "/index.html", "/data"):
                    self._send(site.page_data(store).encode())
                elif path == "/run":
                    self._send(site.page_run(store).encode())
                elif path == "/compare":
                    self._send(site.page_compare(store).encode())
                elif path == "/variant":
                    vid = parse_qs(u.query).get("id", [""])[0]
                    self._send(site.page_variant(store, vid).encode())
                elif path == "/static":                 # the single-page dashboard
                    static, _ = build_html(store)
                    self._send(static.encode())
                elif path == "/dashboard":              # the combined interactive (legacy)
                    _, inter = build_html(store)
                    self._send(inter.encode())
                elif path == "/api/grades.json":
                    gb, *_ = _prep(store)
                    self._send(gb.to_json().encode(), "application/json")
                elif path == "/api/variants.json":
                    _, variants, *_ = _prep(store)
                    self._send(json.dumps(variants, ensure_ascii=False, indent=2).encode(),
                               "application/json")
                elif path == "/healthz":
                    self._send(b"ok", "text/plain")
                else:
                    self._send(b"<h1>404</h1><p>try / (Data), /run, /compare</p>", code=404)
            except Exception as e:
                import traceback
                self._send(f"<h1>500</h1><pre>{type(e).__name__}: {_e(e)}\n{_e(traceback.format_exc())}</pre>"
                           .encode(), code=500)

        def do_POST(self):
            if urlparse(self.path).path.rstrip("/") != "/api/eval":
                self._send(b"404", code=404); return
            try:
                n = int(self.headers.get("Content-Length", 0))
                form = parse_qs(self.rfile.read(n).decode())
                model_id = form.get("model_id", [""])[0]
                prompt_id = form.get("prompt_id", [""])[0]
                label = form.get("label", [""])[0]
                store = Store(db_url)
                # reuse an existing variant for this (model, prompt), else create one
                vid = next((v["id"] for v in store.list_variants()
                            if v["model_id"] == model_id and v["prompt_id"] == prompt_id), None)
                if not vid:
                    vid = store.add_variant(model_id, prompt_id, label=label or "custom")
                # run the exact `ceval eval run` pipeline, capturing its log
                from . import __main__ as M
                a = SimpleNamespace(db=db_url, gen_dir="demo/gen", judge_dir="demo/judge",
                                    sim=False, offline=False, online=False, sessions=800)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    M.cmd_eval(a)
                out = site.eval_output(Store(db_url), vid, buf.getvalue())
                self._send(site.page_run(Store(db_url), out).encode())
            except Exception as e:
                import traceback
                self._send(f"<h1>500</h1><pre>{_e(e)}\n{_e(traceback.format_exc())}</pre>".encode(), code=500)
    return H


def _e(s):
    import html
    return html.escape(str(s))


def serve(db_url: str, port: int = 8787, host: str = "127.0.0.1"):
    httpd = ThreadingHTTPServer((host, port), _make_handler(db_url))
    print("─" * 64)
    print(f"  ceval platform  ·  reading {db_url}")
    print(f"  →  http://{host}:{port}/          ① Data")
    print(f"  →  http://{host}:{port}/run       ② Run eval")
    print(f"  →  http://{host}:{port}/compare   ③ Compare")
    print(f"  →  http://{host}:{port}/variant?id=v_narrator   ④ Detail")
    print("  renders fresh from the DB every request. Ctrl-C to stop.")
    print("─" * 64)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped.")
        httpd.server_close()
