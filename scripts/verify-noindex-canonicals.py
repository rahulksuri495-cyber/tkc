#!/usr/bin/env python3
"""Build-time linter: noindex pages must not point canonical/og:url at
indexable counterparts.

When a page is marked `<meta name="robots" content="noindex">`, its
canonical and og:url tags become a strong signal to crawlers and AI
answer engines about *which other URL* should receive the link equity
and be cached for previews. If that target is itself an indexable page
on the same site, social platforms and search engines end up caching
the noindex page's title/description/image under the indexable URL —
causing duplicate-content confusion and stale preview cards.

Rules enforced (per noindex page):
  1. If canonical / og:url is self-referential, it's fine.
  2. If it points OFF-site, it's fine.
  3. If it points to another tkctalent.com URL, that target must ALSO
     be noindex (or non-existent in the build). Pointing a noindex page
     at an indexable page is the bug we prevent.
  4. canonical and og:url must agree with each other.

Exit code 1 on any violation. Wire into `bun run build`.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tkctalent.com"
SKIP_PARTS = {"dist", "node_modules", ".git", "admin", ".lovable",
              ".agents", ".claude", ".workspace", "public"}

CANON_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', re.I)
OG_URL_RE = re.compile(
    r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']', re.I)
ROBOTS_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']', re.I)


def page_route(path: Path) -> str:
    rel = path.parent.relative_to(ROOT).as_posix()
    return "/" if rel in ("", ".") else f"/{rel}/"


def url_to_path(url: str) -> Path | None:
    """Map a tkctalent.com URL back to its local index.html, if any."""
    if not url.startswith(SITE):
        return None
    route = url[len(SITE):].split("?")[0].split("#")[0]
    if not route or route == "/":
        return ROOT / "index.html"
    return ROOT / route.strip("/") / "index.html"


def robots_of(html: str) -> str:
    m = ROBOTS_RE.search(html)
    return m.group(1).lower() if m else ""


def main() -> int:
    pages = [p for p in sorted(ROOT.glob("**/index.html"))
             if not SKIP_PARTS.intersection(p.parts)]
    errors: list[str] = []
    noindex_count = 0

    for p in pages:
        html = p.read_text(encoding="utf-8", errors="ignore")
        if "noindex" not in robots_of(html):
            continue
        noindex_count += 1
        rel = p.relative_to(ROOT).as_posix()
        self_url = f"{SITE}{page_route(p)}"

        canon = CANON_RE.search(html)
        ogurl = OG_URL_RE.search(html)
        canon_url = canon.group(1) if canon else ""
        og_url = ogurl.group(1) if ogurl else ""

        if canon_url and og_url and canon_url != og_url:
            errors.append(f"{rel}: noindex page has mismatched canonical "
                          f"({canon_url}) vs og:url ({og_url})")

        for label, val in (("canonical", canon_url), ("og:url", og_url)):
            if not val:
                continue
            if not val.startswith(SITE):
                continue  # off-site target, not our concern
            if val.rstrip("/") == self_url.rstrip("/"):
                continue  # self-referential, fine
            target = url_to_path(val)
            if target is None or not target.is_file():
                errors.append(f"{rel}: noindex {label} points at unknown "
                              f"on-site URL {val} (target file missing)")
                continue
            target_html = target.read_text(encoding="utf-8", errors="ignore")
            if "noindex" not in robots_of(target_html):
                errors.append(
                    f"{rel}: noindex {label} points at INDEXABLE page "
                    f"{val} — would split SEO/preview cache. Either make "
                    f"the target noindex too, or point {label} at the "
                    f"noindex page itself ({self_url}).")

    print(f"noindex canonical audit: {noindex_count} noindex page(s) "
          f"scanned (of {len(pages)} total)")
    for e in errors:
        print(f"  ERROR: {e}")
    if errors:
        print(f"\n{len(errors)} violation(s) — fix before deploy.")
        return 1
    print("  no noindex→indexable canonical leaks ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())