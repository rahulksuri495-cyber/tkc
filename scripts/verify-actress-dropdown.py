#!/usr/bin/env python3
"""Verify every book-*/ actress page slug appears in the Bollywood Actresses
desktop dropdown and mobile drawer arrays inside assets/nav-enhance.js.

Source of truth for which book-*/ slugs are actresses: the static dropdown
rendered in bollywood-actress-booking/index.html. We compare that set against
the `actresses` and `actressNameMap` arrays in assets/nav-enhance.js.

Exit codes:
  0 - all slugs present in both desktop list and name map
  1 - mismatch detected (missing/extra slugs); diff printed to stderr
"""
from __future__ import annotations
import re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
NAV = ROOT / "assets" / "nav-enhance-v2.js"
# An actress page is any book-<slug>/index.html whose BreadcrumbList points
# back to /bollywood-actress-booking/. This is the authoritative signal —
# the category page HTML also cross-links singers/comedians and can't be
# trusted as a slug source.
BREADCRUMB_RE = re.compile(r'"item"\s*:\s*"https://tkctalent\.com/bollywood-actress-booking/"')

def fail(msg: str) -> None:
    print(f"[verify-actress-dropdown] FAIL: {msg}", file=sys.stderr)
    sys.exit(1)

def main() -> int:
    if not NAV.exists(): fail(f"missing {NAV}")

    expected = set()
    for p in sorted(ROOT.glob("book-*/index.html")):
        try:
            if BREADCRUMB_RE.search(p.read_text(encoding="utf-8", errors="ignore")):
                expected.add(p.parent.name[len("book-"):])
        except OSError:
            pass
    if not expected:
        fail("no actress book-*/index.html pages found via breadcrumb signal")

    nav_js = NAV.read_text(encoding="utf-8")
    # actresses = [[label, href], ...]
    m = re.search(r"var\s+actresses\s*=\s*(\[[\s\S]*?\]);", nav_js)
    if not m: fail("could not locate `var actresses = [...]` in nav-enhance-v2.js")
    desktop_slugs = set(re.findall(r'/book-([a-z0-9-]+)/', m.group(1)))

    m2 = re.search(r"var\s+actressNameMap\s*=\s*(\{[\s\S]*?\});", nav_js)
    if not m2: fail("could not locate `var actressNameMap = {...}` in nav-enhance-v2.js")
    map_slugs = set(re.findall(r'/book-([a-z0-9-]+)/', m2.group(1)))

    errors = []
    missing_desktop = expected - desktop_slugs
    missing_map     = expected - map_slugs
    extra_desktop   = desktop_slugs - expected
    extra_map       = map_slugs - expected

    if missing_desktop:
        errors.append(f"missing from desktop `actresses` array ({len(missing_desktop)}): "
                      + ", ".join(sorted(missing_desktop)))
    if missing_map:
        errors.append(f"missing from `actressNameMap` ({len(missing_map)}): "
                      + ", ".join(sorted(missing_map)))
    if extra_desktop:
        errors.append(f"extra in desktop array (no matching actress page) ({len(extra_desktop)}): "
                      + ", ".join(sorted(extra_desktop)))
    if extra_map:
        errors.append(f"extra in name map (no matching actress page) ({len(extra_map)}): "
                      + ", ".join(sorted(extra_map)))

    # The desktop dropdown drives the mobile drawer (same `actresses` array is
    # injected by ensureActressSubmenus for both), so verifying the desktop
    # array also covers the mobile drawer. Sanity check the function uses it:
    if "ensureActressSubmenus" not in nav_js or "mobile-nav-drawer" not in nav_js:
        errors.append("ensureActressSubmenus / mobile-nav-drawer hook missing in nav-enhance-v2.js")

    if errors:
        for e in errors: print("  - " + e, file=sys.stderr)
        fail(f"{len(errors)} issue(s) found; dropdown is out of sync with actress pages")

    print(f"[verify-actress-dropdown] OK: {len(expected)} actress slugs present in "
          f"desktop dropdown, mobile drawer, and name map.")
    return 0

if __name__ == "__main__":
    sys.exit(main())