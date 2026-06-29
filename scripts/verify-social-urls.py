#!/usr/bin/env python3
"""Build-time check: every footer link and JSON-LD sameAs URL pointing at
a known social platform MUST match the canonical handle table below.

Fails the build if any page drifts (e.g. an old `thekabirco` Facebook
URL re-appears, an unofficial @TKCTalent X handle is added, or a
JSON-LD sameAs is missing the trailing slash that the live page uses).

Usage:  python3 scripts/verify-social-urls.py
Exit:   0 on success, 1 on any mismatch.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Canonical handles — single source of truth. Update here, run the check,
# and any HTML / JSON-LD that drifts will be reported.
CANONICAL = {
    "facebook.com":  "https://www.facebook.com/thekabircompany",
    "x.com":         "https://x.com/thekabircompany",
    "twitter.com":   "https://x.com/thekabircompany",  # legacy → migrate
    "instagram.com": "https://www.instagram.com/thekabircompany/",
    "youtube.com":   "https://www.youtube.com/@TheKabirCompany",
    "pinterest.com": "https://in.pinterest.com/thekabircompany/",
    "imdb.com":      "https://www.imdb.com/title/tt35350271/",
}

# Hosts we audit (suffix match on the URL hostname)
HOSTS = tuple(CANONICAL.keys())

URL_RE = re.compile(r'https?://[^\s"\'<>)]+', re.IGNORECASE)
JSONLD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)

def canonical_for(url: str) -> str | None:
    low = url.lower()
    for host, target in CANONICAL.items():
        if host in low:
            return target
    return None

def scan_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [f"{path}: read error {e}"]

    # 1) Raw URLs in HTML (footer links, anchor hrefs, meta tags)
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip('.,;)')
        target = canonical_for(url)
        if target and url != target:
            errors.append(f"{path}: {url} → expected {target}")

    # 2) JSON-LD sameAs arrays — parse and check each entry
    for block in JSONLD_RE.findall(text):
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue
        for url in _collect_sameas(data):
            target = canonical_for(url)
            if target and url != target:
                errors.append(f"{path} [JSON-LD sameAs]: {url} → expected {target}")
    return errors

def _collect_sameas(node) -> list[str]:
    out: list[str] = []
    if isinstance(node, dict):
        sa = node.get("sameAs")
        if isinstance(sa, str): out.append(sa)
        elif isinstance(sa, list): out.extend(x for x in sa if isinstance(x, str))
        for v in node.values():
            out.extend(_collect_sameas(v))
    elif isinstance(node, list):
        for v in node:
            out.extend(_collect_sameas(v))
    return out

SKIP_DIRS = {".git", "node_modules", "admin", ".github", "scripts"}

def main() -> int:
    targets: list[Path] = []
    for ext in ("*.html", "*.txt", "*.json", "*.js"):
        for p in ROOT.rglob(ext):
            if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts[:-1]):
                continue
            targets.append(p)

    all_errors: list[str] = []
    for p in targets:
        all_errors.extend(scan_file(p))

    if all_errors:
        print(f"❌ social URL drift detected in {len({e.split(':')[0] for e in all_errors})} file(s):\n")
        for e in all_errors:
            print("  -", e)
        print(f"\nCanonical handles are defined in {Path(__file__).name}. Update offending files or update the canonical table.")
        return 1
    print(f"✅ social URLs consistent across {len(targets)} files for hosts: {', '.join(HOSTS)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())