"""Local HTTP server for the dashboard — the platform as a live service.

Renders FRESH FROM THE DB on each request (stdlib http.server, no dependencies). So the loop
is: `ceval eval run` / `ceval data add` -> refresh the browser -> new data. The dashboard is a
service reading the DB, not a static file.

Routes:
  /                 the interactive dashboard (select / compare / evidence)
  /static           the static dashboard (renders anywhere)
  /api/grades.json  the grade book as JSON
  /api/variants.json the variant manifest
  /healthz          ok

Bind is 127.0.0.1 (local only) by design — this is a local service.
"""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .store import Store
from .report import build_html, _prep


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
            path = self.path.split("?")[0].rstrip("/") or "/"
            try:
                store = Store(db_url)   # fresh connection per request (thread-safe for sqlite)
                if path in ("/", "/index.html"):
                    _, inter = build_html(store)
                    self._send(inter.encode())
                elif path == "/static":
                    static, _ = build_html(store)
                    self._send(static.encode())
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
                    self._send(b"<h1>404</h1><p>try / or /static</p>", code=404)
            except Exception as e:
                self._send(f"<h1>500</h1><pre>{type(e).__name__}: {e}</pre>".encode(), code=500)
    return H


def serve(db_url: str, port: int = 8787, host: str = "127.0.0.1"):
    httpd = ThreadingHTTPServer((host, port), _make_handler(db_url))
    print(f"─" * 62)
    print(f"  ceval dashboard service  ·  reading {db_url}")
    print(f"  →  http://{host}:{port}/           interactive dashboard")
    print(f"  →  http://{host}:{port}/static     static dashboard")
    print(f"  →  http://{host}:{port}/api/grades.json")
    print(f"  renders fresh from the DB on every request — edit data, refresh.")
    print(f"  Ctrl-C to stop.")
    print(f"─" * 62)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  stopped.")
        httpd.server_close()
