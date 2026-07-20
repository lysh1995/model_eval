"""Static export of the 4-page site — self-contained HTML, viewable straight from GitHub.

`ceval site --out docs` renders every page to a standalone .html file with the current DB baked
in, cross-linked with RELATIVE links (no server, no JavaScript, inline CSS). Point GitHub Pages
at /docs and a reviewer opens the platform in a browser with nothing installed.

Why it works with no server: the whole site is already CSS-only (tabs and the EN/中文 switch are
hidden-radio + :checked, no JS) and every asset is inlined, so a flat file renders identically to
the live view — only the live ② Run form (which POSTs to the server) is inert, and we say so.
"""
from __future__ import annotations
import re
import pathlib
from typing import List, Tuple

from ..store import Store
from . import site


_BANNER = ('<div style="background:var(--signal-soft);border:1px solid var(--signal);'
           'border-radius:9px;padding:9px 13px;margin:2px 0 14px;font-size:11.5px;color:var(--ink)">'
           '<b>Static snapshot</b> — rendered from the local database, viewable straight from GitHub. '
           'Every page, score, and transcript is real data. The only inert part is the live '
           '<b>② Run</b> form (it needs the local server); everything else, including the '
           '<b>EN / 中文</b> switch and all tabs, works here with no JavaScript.</div>')


def _rewrite_links(html: str) -> str:
    """Route hrefs -> relative static filenames."""
    html = re.sub(r'href="/variant\?id=([A-Za-z0-9_]+)"', r'href="variant_\1.html"', html)
    html = html.replace('href="/compare"', 'href="compare.html"')
    html = html.replace('href="/design"', 'href="design.html"')
    html = html.replace('href="/run"', 'href="run.html"')
    html = html.replace('href="/"', 'href="index.html"')      # exact: the Data/home nav link
    return html


def _document(title: str, body: str) -> str:
    """Wrap a page fragment in a standalone HTML document (charset matters for the zh text)."""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title></head><body>{_rewrite_links(body)}</body></html>')


def render_static(store: Store, out_dir: str = "docs") -> Tuple[pathlib.Path, List[str]]:
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    variants = store.list_variants()

    pages = {
        "index.html":   ("① Test data",      site.page_data(store)),
        "compare.html": ("③ Cross-compare",  site.page_compare(store)),
        "design.html":  ("⑤ Design",         site.page_design(store)),
        "run.html":     ("② Run",            site.page_run(store)),
    }
    for v in variants:
        pages[f"variant_{v['id']}.html"] = (f"④ {v.get('label') or v['id']}",
                                            site.page_variant(store, v["id"]))

    written = []
    for fname, (title, body) in pages.items():
        # drop the static banner in right after the nav so every page announces itself
        body = body.replace("</nav>", "</nav>" + _BANNER, 1)
        (out / fname).write_text(_document(f"ceval — {title}", body))
        written.append(fname)
    return out, written
