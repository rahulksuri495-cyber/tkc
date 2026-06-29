#!/usr/bin/env python3
"""Build-time check: og:url and canonical match the final redirected URL.

Apache (.htaccess) enforces:
  - https only (HSTS)
  - apex hostname (www.tkctalent.com -> tkctalent.com)
  - directory routes carry a trailing slash (/foo -> /foo/)

Crawlers cache the *final* URL after redirects. If og:url or canonical point
at a pre-redirect form (http://, www., or missing trailing slash), social
platforms and search engines treat the page as a different URL than what
they actually fetched - causing duplicate-content and cache-mismatch bugs.

This script walks every index.html under the project root and asserts:
  - <link rel="canonical"> exists, is absolute, https, apex host, and ends
    with "/" because every page lives at <dir>/index.html.
  - <meta property="og:url"> matches the canonical exactly.
  - The URL self-references the page's own route.

Exit code 1 on any error. Wired into `bun run build` via package.json.
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

CANON_FULL_RE = re.compile(
    r'<link[^>]+rel=["\']canonical["\'][^>]*>', re.I)
OG_URL_FULL_RE = re.compile(
    r'<meta[^>]+property=["\']og:url["\'][^>]*>', re.I)


def expected_url(path: Path) -> str:
    rel = path.parent.relative_to(ROOT).as_posix()
    return f"{SITE}/" if rel in ("", ".") else f"{SITE}/{rel}/"


def check_url(label: str, url: str, want: str, rel: str) -> list[str]:
    errs: list[str] = []
    if not url:
        return [f"{rel}: missing {label}"]
    if url.startswith("http://"):
        errs.append(f"{rel}: {label} uses http (must be https): {url}")
    if "//www.tkctalent.com" in url:
        errs.append(f"{rel}: {label} uses www host (must be apex): {url}")
    # query/fragment must not appear on canonical/og:url
    if "?" in url or "#" in url:
        errs.append(f"{rel}: {label} has query/fragment: {url}")
    # trailing slash rule — every index.html lives at /<dir>/index.html
    if not url.endswith("/"):
        errs.append(f"{rel}: {label} missing trailing slash (Apache 301s to slashed form): {url}")
    # self-reference
    if url.rstrip("/") + "/" != want:
        errs.append(f"{rel}: {label}={url} expected {want}")
    return errs


def audit(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8", errors="ignore")
    rel = path.relative_to(ROOT).as_posix()
    robots = (ROBOTS_RE.search(html).group(1).lower()
              if ROBOTS_RE.search(html) else "")
    if "noindex" in robots:
        return []  # noindex pages don't need canonical/og:url integrity

    canon = CANON_RE.search(html)
    ogurl = OG_URL_RE.search(html)
    want = expected_url(path)
    errs: list[str] = []
    errs += check_url("canonical", canon.group(1) if canon else "", want, rel)
    errs += check_url("og:url", ogurl.group(1) if ogurl else "", want, rel)

    # consistency: canonical and og:url must agree byte-for-byte
    if canon and ogurl and canon.group(1) != ogurl.group(1):
        errs.append(f"{rel}: canonical ({canon.group(1)}) != og:url ({ogurl.group(1)})")
    return errs


def fix(path: Path) -> bool:
    """Rewrite canonical + og:url to the expected self-referential URL."""
    html = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()
    robots = (ROBOTS_RE.search(html).group(1).lower()
              if ROBOTS_RE.search(html) else "")
    if "noindex" in robots:
        return False
    want = expected_url(path)
    changed = False
    new_canon = f'<link rel="canonical" href="{want}"/>'
    new_og = f'<meta property="og:url" content="{want}"/>'
    if CANON_FULL_RE.search(html):
        new_html = CANON_FULL_RE.sub(new_canon, html, count=1)
        if new_html != html:
            html = new_html
            changed = True
    else:
        html = html.replace("</head>", new_canon + "\n</head>", 1)
        changed = True
    if OG_URL_FULL_RE.search(html):
        new_html = OG_URL_FULL_RE.sub(new_og, html, count=1)
        if new_html != html:
            html = new_html
            changed = True
    else:
        html = html.replace("</head>", new_og + "\n</head>", 1)
        changed = True
    if changed:
        path.write_text(html, encoding="utf-8")
    return changed


def main() -> int:
    do_fix = "--fix" in sys.argv
    pages = [p for p in sorted(ROOT.glob("**/index.html"))
             if not SKIP_PARTS.intersection(p.parts)]
    if do_fix:
        fixed = [p for p in pages if fix(p)]
        print(f"canonical/og:url fix: rewrote {len(fixed)} page(s)")
    all_errs: list[str] = []
    for p in pages:
        all_errs.extend(audit(p))
    print(f"canonical/og:url audit: {len(pages)} page(s) scanned")
    for e in all_errs:
        print(f"  ERROR: {e}")
    if all_errs:
        print(f"\n{len(all_errs)} mismatch(es) — fix before deploy to avoid social/SEO cache splits.")
        return 1
    print("  all canonical + og:url tags match final redirected URL ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())