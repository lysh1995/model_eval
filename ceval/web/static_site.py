"""Static export of the site — bilingual (EN + 中文), viewable straight from GitHub.

`ceval site --out docs` renders every page to standalone .html with the current DB baked in:
English at docs/*.html, Chinese at docs/zh/*.html, cross-linked with RELATIVE links (no server,
no JavaScript, inline CSS). Point GitHub Pages at /docs and a reviewer opens the platform — in
either language — with nothing installed. The EN / 中文 interface switch flips between the two.

Why it works with no server: the whole site is already CSS-only (tabs, the data-language switch,
and the interface-language switch are hidden-radio/link + :checked, no JS) and every asset is
inlined, so a flat file renders identically to the live view — only the live ② Run form (which
POSTs to the server) is inert, and we say so.
"""
from __future__ import annotations
import re
import pathlib
from typing import List, Tuple

from ..store import Store
from . import site


_ROUTES = {"/": "index.html", "/compare": "compare.html", "/design": "design.html", "/run": "run.html"}


def _banner(loc: str) -> str:
    site.set_locale(loc)
    return ('<div style="background:var(--signal-soft);border:1px solid var(--signal);'
            'border-radius:9px;padding:9px 13px;margin:2px 0 14px;font-size:11.5px;color:var(--ink)">'
            + site.t("<b>Static snapshot</b> — rendered from the local database, viewable straight from GitHub. "
                     "Every page, score, and transcript is real data. The only inert part is the live "
                     "<b>② Run</b> form (it needs the local server); everything else, including the "
                     "<b>EN / 中文</b> switches and all tabs, works here with no JavaScript.",
                     "<b>静态快照</b>——由本地数据库渲染,可直接在 GitHub 上查看。每一页、每个分数、每段记录都是真实数据。"
                     "唯一失效的是实时 <b>② 运行</b> 表单(它需要本地服务器);其余一切,包括 <b>EN / 中文</b> "
                     "切换和所有标签页,在这里无需 JavaScript 即可使用。")
            + '</div>')


def _file_for(path: str, qs: str) -> str:
    if path == "/variant":
        m = re.search(r"id=([A-Za-z0-9_]+)", qs)
        return f"variant_{m.group(1)}.html" if m else "compare.html"
    return _ROUTES.get(path, "index.html")


def _rewrite_links(html: str, cur: str) -> str:
    """Route hrefs → relative static filenames, honoring the ?ui=<loc> interface switch.
    cur is the locale of THIS page ('en' → docs/, 'zh' → docs/zh/)."""
    def repl(m):
        path, qs = m.group(1), m.group(2) or ""
        fname = _file_for(path, qs)
        mui = re.search(r"ui=(en|zh)", qs)
        target = mui.group(1) if mui else cur
        if target == cur:
            return f'href="{fname}"'
        if cur == "en" and target == "zh":
            return f'href="zh/{fname}"'
        if cur == "zh" and target == "en":
            return f'href="../{fname}"'
        return f'href="{fname}"'
    return re.sub(r'href="(/[a-z]*)(\?[^"]*)?"', repl, html)


def _document(title: str, body: str, cur: str) -> str:
    lang_attr = "zh-Hans" if cur == "zh" else "en"
    return (f'<!doctype html><html lang="{lang_attr}"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title></head><body>{_rewrite_links(body, cur)}</body></html>')


def render_static(store: Store, out_dir: str = "docs") -> Tuple[pathlib.Path, List[str]]:
    out = pathlib.Path(out_dir)
    variants = store.list_variants()

    def render_all():
        pages = {
            "index.html":   site.page_data(store),
            "compare.html": site.page_compare(store),
            "design.html":  site.page_design(store),
            "run.html":     site.page_run(store),
        }
        for v in variants:
            pages[f"variant_{v['id']}.html"] = site.page_variant(store, v["id"])
        return pages

    written = []
    for loc, subdir in (("en", ""), ("zh", "zh")):
        site.set_locale(loc)
        target = out / subdir
        target.mkdir(parents=True, exist_ok=True)
        banner = _banner(loc)
        site.set_locale(loc)                       # _banner touched the locale; reset
        title = site.t("ceval — companion evaluation", "ceval — 伴侣模型评测")
        for fname, body in render_all().items():
            body = body.replace("</nav>", "</nav>" + banner, 1)
            (target / fname).write_text(_document(title, body, loc))
            written.append(f"{subdir + '/' if subdir else ''}{fname}")
    site.set_locale("en")
    return out, written
