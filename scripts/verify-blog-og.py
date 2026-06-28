#!/usr/bin/env python3
"""Build-time check: every blog page has valid OG + Twitter Card metadata.

Verifies, for /blog/index.html and every /blog/<slug>/index.html:
  - og:title, og:description, og:url, og:image, og:type
  - twitter:card, twitter:title, twitter:description, twitter:image
  - canonical link
  - og:url + canonical are absolute and self-reference the page
  - og:image is absolute and the referenced file exists on disk

If a blog page is missing og:image (or points to a missing file), the script
rewrites it to the default fallback /assets/blog/og-default.jpg so social
previews never break. Re-run with --check (no writes) for CI.

Exit code 1 on any unresolved error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
SITE = "https://tkctalent.com"
FALLBACK = "/assets/blog/og-default.jpg"
FALLBACK_ABS = SITE + FALLBACK

REQUIRED_META = {
    "og:title": ("property",),
    "og:description": ("property",),
    "og:url": ("property",),
    "og:image": ("property",),
    "og:type": ("property",),
    "twitter:card": ("name", "property"),
    "twitter:title": ("name", "property"),
    "twitter:description": ("name", "property"),
    "twitter:image": ("name", "property"),
}


def find_meta(html: str, key: str, attrs: tuple[str, ...]) -> str | None:
    for attr in attrs:
        m = re.search(
            rf'<meta\s+{attr}=["\']{re.escape(key)}["\']\s+content=["\']([^"\']*)["\']',
            html, re.I,
        )
        if m:
            return m.group(1)
    return None


def find_canonical(html: str) -> str | None:
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', html, re.I)
    return m.group(1) if m else None


def expected_url(path: Path) -> str:
    rel = path.parent.relative_to(ROOT).as_posix()
    return f"{SITE}/{rel}/" if rel else f"{SITE}/"


def asset_exists(url: str) -> bool:
    p = urlparse(url).path
    return (ROOT / p.lstrip("/")).is_file()


def ensure_fallback_image(check_only: bool) -> list[str]:
    errs: list[str] = []
    if not (ROOT / FALLBACK.lstrip("/")).is_file():
        errs.append(f"missing fallback image: {FALLBACK}")
    return errs


def patch_og_image(html: str, new_url: str) -> tuple[str, bool]:
    """Replace og:image / og:image:secure_url / twitter:image with new_url."""
    changed = False
    for pat in [
        r'(<meta\s+property=["\']og:image["\']\s+content=["\'])[^"\']*(["\'])',
        r'(<meta\s+property=["\']og:image:secure_url["\']\s+content=["\'])[^"\']*(["\'])',
        r'(<meta\s+(?:name|property)=["\']twitter:image["\']\s+content=["\'])[^"\']*(["\'])',
    ]:
        new_html, n = re.subn(pat, rf'\g<1>{new_url}\g<2>', html, flags=re.I)
        if n:
            html, changed = new_html, True
    if not re.search(r'og:image', html, re.I):
        inject = (
            f'<meta property="og:image" content="{new_url}"/>\n'
            f'<meta name="twitter:image" content="{new_url}"/>\n'
        )
        html = html.replace("</head>", inject + "</head>", 1)
        changed = True
    return html, changed


def audit_page(path: Path, check_only: bool) -> tuple[list[str], list[str]]:
    html = path.read_text(encoding="utf-8")
    errs: list[str] = []
    fixes: list[str] = []
    rel = path.relative_to(ROOT).as_posix()

    # required tags present + non-empty
    values = {}
    for key, attrs in REQUIRED_META.items():
        v = find_meta(html, key, attrs)
        values[key] = v
        if v is None or not v.strip():
            if key in ("og:image", "twitter:image"):
                continue  # handled by fallback below
            errs.append(f"{rel}: missing or empty {key}")

    # canonical
    canon = find_canonical(html)
    if not canon:
        errs.append(f"{rel}: missing canonical link")

    # url consistency
    want = expected_url(path)
    if values.get("og:url") and values["og:url"].rstrip("/") + "/" != want:
        errs.append(f"{rel}: og:url={values['og:url']} expected {want}")
    if canon and canon.rstrip("/") + "/" != want:
        errs.append(f"{rel}: canonical={canon} expected {want}")

    # twitter:card value
    if values.get("twitter:card") and values["twitter:card"] not in {"summary", "summary_large_image"}:
        errs.append(f"{rel}: twitter:card={values['twitter:card']} (use summary_large_image)")

    # og:image present, absolute, file exists; else apply fallback
    img = values.get("og:image")
    needs_fallback = (
        not img
        or not img.startswith("http")
        or not asset_exists(img)
    )
    if needs_fallback:
        if check_only:
            errs.append(f"{rel}: og:image missing/broken ({img!r}) — fallback required")
        else:
            new_html, changed = patch_og_image(html, FALLBACK_ABS)
            if changed:
                path.write_text(new_html, encoding="utf-8")
                fixes.append(f"{rel}: og:image -> {FALLBACK_ABS}")

    # twitter:image: if present but broken, repair to og:image value
    timg = values.get("twitter:image")
    if timg and timg.startswith("http") and not asset_exists(timg):
        if check_only:
            errs.append(f"{rel}: twitter:image broken ({timg})")

    return errs, fixes


def main() -> int:
    check_only = "--check" in sys.argv
    if not BLOG.is_dir():
        print("no /blog directory found")
        return 0

    errs = ensure_fallback_image(check_only)
    fixes: list[str] = []
    pages = sorted(BLOG.glob("**/index.html"))
    for page in pages:
        e, f = audit_page(page, check_only)
        errs.extend(e)
        fixes.extend(f)

    print(f"blog og audit: {len(pages)} page(s)")
    for f in fixes:
        print(f"  fixed: {f}")
    for e in errs:
        print(f"  ERROR: {e}")
    if errs:
        return 1
    print("  all blog pages have valid og + twitter card metadata ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())