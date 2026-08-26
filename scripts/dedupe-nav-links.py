#!/usr/bin/env python3
"""Remove duplicate navigation links from static HTML.

Scope is limited to header/nav/mobile-drawer regions so page body content is
never touched. Within those regions a leaf <li><a href="X">…</a></li> item is
removed when the same href already appeared in the *same* <ul> (menu level).
Cross-menu links (e.g. a singer listed under both Booking and Fees menus) are
left alone.
"""
import re
import sys
from pathlib import Path

REGION_RE = re.compile(
    r"<header[\s\S]*?</header>|<nav[\s\S]*?</nav>|<aside[^>]*id=\"mobile-nav-drawer\"[\s\S]*?</aside>",
    re.I,
)
# leaf item: <li ...><a href="...">text</a></li> with no nested <ul>
ITEM_RE = re.compile(r"<li[^>]*>\s*<a href=\"([^\"]+)\"[^>]*>(?:(?!</li>)[\s\S]){0,400}?</a>\s*</li>")
TOKEN_RE = re.compile(r"<ul\b[^>]*>|</ul>|" + ITEM_RE.pattern)


def dedupe_region(region: str):
    out = []
    pos = 0
    removed = 0
    stack = [set()]
    for m in TOKEN_RE.finditer(region):
        tok = m.group(0)
        if tok.startswith("<ul"):
            stack.append(set())
            continue
        if tok.startswith("</ul"):
            if len(stack) > 1:
                stack.pop()
            continue
        href = m.group(1)
        if href in stack[-1]:
            out.append(region[pos:m.start()])
            pos = m.end()
            removed += 1
        else:
            stack[-1].add(href)
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
