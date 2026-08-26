#!/usr/bin/env python3
"""Remove duplicate navigation links from static HTML.

Scope is limited to header/nav/mobile-drawer regions so page body content is
never touched. Within those regions, an <li><a href="X">…</a></li> item is
dropped when the immediately preceding sibling item points at the same href.
"""
import re
import sys
from pathlib import Path

REGION_RE = re.compile(
    r"<header[\s\S]*?</header>|<nav[\s\S]*?</nav>|<aside[^>]*id=\"mobile-nav-drawer\"[\s\S]*?</aside>",
    re.I,
)
ITEM_RE = re.compile(r"<li[^>]*>\s*<a href=\"([^\"]+)\"[^>]*>[\s\S]{0,300}?</a>\s*</li>")


def dedupe_region(region: str):
    out = []
    pos = 0
    prev_href = None
    prev_end = None
    removed = 0
    for m in ITEM_RE.finditer(region):
        href = m.group(1)
        adjacent = prev_end is not None and region[prev_end:m.start()].strip() == ""
        if adjacent and href == prev_href:
            out.append(region[pos:m.start()])
            pos = m.end()
            prev_end = m.end()
            removed += 1
            continue
        prev_href = href
        prev_end = m.end()
    out.append(region[pos:])
    return "".join(out), removed


def process(path: Path) -> int:
    html = path.read_text(encoding="utf-8", errors="ignore")
    total = 0
    result = []
    last = 0
    for m in REGION_RE.finditer(html):
        cleaned, n = dedupe_region(m.group(0))
        total += n
        result.append(html[last:m.start()])
        result.append(cleaned)
        last = m.end()
    result.append(html[last:])
    if total:
        path.write_text("".join(result), encoding="utf-8")
    return total


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    grand = 0
    files = 0
    for p in sorted(root.rglob("*.html")):
        if "node_modules" in p.parts or ".git" in p.parts:
            continue
        n = process(p)
        if n:
            grand += n
            files += 1
            print(f"{p}: removed {n}")
    print(f"Total: removed {grand} duplicate nav links across {files} files")


if __name__ == "__main__":
    main()
