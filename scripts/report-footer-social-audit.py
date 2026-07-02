#!/usr/bin/env python3
"""Detailed build-failure report for footer social icons.

Emits, per issue, the exact:
  - file path
  - element / context snippet (the offending <a>, JSON-LD sameAs entry,
    or icon <svg> tile)
  - URL (or `<missing>` when a required platform icon is absent)
  - failure category (URL_DRIFT | MISSING_PLATFORM | MISSING_ALT | DUP_ICON)

Categories audited:
  1. URL_DRIFT       — brand-owned social URL in a footer asset or HTML page
                        differs from CANONICAL (scripts/verify-social-urls.py).
  2. MISSING_PLATFORM — a required platform (Facebook, Instagram, YouTube,
                        X, Pinterest, IMDb) has no icon tile in a footer asset.
  3. MISSING_ALT     — a footer social <a> / icon has no aria-label, title,
                        or accessible text (screen-reader "alt").
  4. DUP_ICON        — the same platform is rendered more than once in the
                        same footer asset (would double-render on screen).

Writes:
  - human report → admin/seo-monitor/footer-social-report.md
  - JSON report  → admin/seo-monitor/footer-social-report.json
  - stdout summary + exit 1 if any issue found.
"""
from __future__ import annotations
import importlib.util, json, re, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "admin" / "seo-monitor"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Reuse canonical handle table
spec = importlib.util.spec_from_file_location(
    "verify_social_urls", ROOT / "scripts" / "verify-social-urls.py"
)
vsu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vsu)  # type: ignore
CANONICAL: dict[str, str] = vsu.CANONICAL
is_brand_url = vsu.is_brand_url

REQUIRED_HOSTS = {
    "facebook.com": "Facebook",
    "instagram.com": "Instagram",
    "youtube.com": "YouTube",
    "x.com": "X (Twitter)",
    "pinterest.com": "Pinterest",
    "imdb.com": "IMDb",
}

FOOTER_ASSETS = ["assets/footer-social-icons.js", "assets/Footer-*.js"]
URL_RE = re.compile(r'https?://[^\s"\'<>)]+', re.IGNORECASE)
ANCHOR_RE = re.compile(r'<a\b[^>]*>.*?</a>', re.IGNORECASE | re.DOTALL)


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def canonical_for(url: str) -> str | None:
    low = url.lower()
    for host, target in CANONICAL.items():
        if host in low:
            return target
    return None


def platform_for(url: str) -> str | None:
    low = url.lower()
    for host in REQUIRED_HOSTS:
        if host in low:
            return host
    # legacy twitter.com -> x.com
    if "twitter.com" in low:
        return "x.com"
    return None


def audit_footer_asset(path: Path) -> list[dict]:
    findings: list[dict] = []
    text = path.read_text(encoding="utf-8", errors="ignore")

    # --- URL drift + platform coverage ---
    seen_platforms: dict[str, list[int]] = defaultdict(list)
    for m in URL_RE.finditer(text):
        url = m.group(0).rstrip('.,;)')
        if not is_brand_url(url):
            continue
        target = canonical_for(url)
        if target:
            plat = platform_for(url)
            if plat:
                seen_platforms[plat].append(m.start())
            if url != target:
                findings.append({
                    "category": "URL_DRIFT",
                    "file": str(path.relative_to(ROOT)),
                    "line": line_of(text, m.start()),
                    "element": f"footer asset embedded URL literal",
                    "url_found": url,
                    "url_expected": target,
                })

    # For the enhancer, presence is measured by the keyword in detect() switch
    is_enhancer = path.name == "footer-social-icons.js"
    for host, label in REQUIRED_HOSTS.items():
        needle = host.split(".")[0] if is_enhancer else CANONICAL[host]
        if needle not in text:
            findings.append({
                "category": "MISSING_PLATFORM",
                "file": str(path.relative_to(ROOT)),
                "line": None,
                "element": f"icon tile for {label}",
                "url_found": "<missing>",
                "url_expected": CANONICAL[host],
            })

    # --- Duplicate icons for same platform (>1 canonical URL literal) ---
    for plat, positions in seen_platforms.items():
        if len(positions) > 1 and not is_enhancer:
            # dedupe by line — the SPA bundle may reference the URL once in
            # JSX and once in JSON-LD; only flag if same file has >1 literal
            # on distinct lines
            lines = sorted({line_of(text, p) for p in positions})
            if len(lines) > 1:
                findings.append({
                    "category": "DUP_ICON",
                    "file": str(path.relative_to(ROOT)),
                    "line": lines[0],
                    "element": f"multiple literals for {plat} at lines {lines}",
                    "url_found": CANONICAL.get(plat, plat),
                    "url_expected": "single canonical reference",
                })

    # --- Missing aria-label / title on rendered anchor tiles ---
    for m in ANCHOR_RE.finditer(text):
        chunk = m.group(0)
        href_m = re.search(r'href=["\']([^"\']+)["\']', chunk)
        if not href_m:
            continue
        href = href_m.group(1)
        if not platform_for(href):
            continue
        has_aria = 'aria-label' in chunk.lower()
        has_title = 'title=' in chunk.lower()
        # A text node between tags is also fine
        inner = re.sub(r'<[^>]+>', '', chunk).strip()
        if not (has_aria or has_title or inner):
            findings.append({
                "category": "MISSING_ALT",
                "file": str(path.relative_to(ROOT)),
                "line": line_of(text, m.start()),
                "element": chunk[:160].replace("\n", " ") + ("…" if len(chunk) > 160 else ""),
                "url_found": href,
                "url_expected": f"add aria-label=\"{REQUIRED_HOSTS.get(platform_for(href), 'social')}\"",
            })
    return findings


def audit_html_page(path: Path) -> list[dict]:
    """Only inspect the visible <footer>…</footer> block of static pages,
    to catch drift or missing alt text at the page level (not just the
    asset)."""
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    fm = re.search(r'<footer\b[^>]*>(.*?)</footer>', text, re.IGNORECASE | re.DOTALL)
    if not fm:
        return findings
    footer = fm.group(1)
    base_line = line_of(text, fm.start())
    for m in ANCHOR_RE.finditer(footer):
        chunk = m.group(0)
        href_m = re.search(r'href=["\']([^"\']+)["\']', chunk)
        if not href_m:
            continue
        href = href_m.group(1)
        plat = platform_for(href)
        if not plat:
            continue
        # URL drift
        target = CANONICAL.get(plat)
        if is_brand_url(href) and target and href != target:
            findings.append({
                "category": "URL_DRIFT",
                "file": str(path.relative_to(ROOT)),
                "line": base_line + footer.count("\n", 0, m.start()),
                "element": chunk[:160].replace("\n", " "),
                "url_found": href,
                "url_expected": target,
            })
        # Missing alt / aria-label
        has_aria = 'aria-label' in chunk.lower()
        has_title = 'title=' in chunk.lower()
        inner_img = re.search(r'<img\b[^>]*>', chunk, re.IGNORECASE)
        has_img_alt = False
        if inner_img and re.search(r'\balt=["\'][^"\']+["\']', inner_img.group(0), re.IGNORECASE):
            has_img_alt = True
        inner_text = re.sub(r'<[^>]+>', '', chunk).strip()
        if not (has_aria or has_title or has_img_alt or inner_text):
            findings.append({
                "category": "MISSING_ALT",
                "file": str(path.relative_to(ROOT)),
                "line": base_line + footer.count("\n", 0, m.start()),
                "element": chunk[:160].replace("\n", " "),
                "url_found": href,
                "url_expected": f"add aria-label / <img alt> for {REQUIRED_HOSTS.get(plat, plat)}",
            })
    return findings


def main() -> int:
    all_findings: list[dict] = []

    # 1. Footer assets
    asset_paths: list[Path] = []
    for pat in FOOTER_ASSETS:
        asset_paths.extend(sorted(ROOT.glob(pat)))
    for p in asset_paths:
        all_findings.extend(audit_footer_asset(p))

    # 2. Static HTML pages
    skip_dirs = {".git", "node_modules", "admin", ".github", "scripts", "assets"}
    html_paths: list[Path] = []
    for p in ROOT.rglob("*.html"):
        rel_parts = p.relative_to(ROOT).parts
        if any(part in skip_dirs for part in rel_parts[:-1]):
            continue
        html_paths.append(p)
    for p in html_paths:
        all_findings.extend(audit_html_page(p))

    # Group + write reports
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for f in all_findings:
        by_cat[f["category"]].append(f)

    summary = {
        "assets_audited": [str(p.relative_to(ROOT)) for p in asset_paths],
        "html_pages_audited": len(html_paths),
        "total_issues": len(all_findings),
        "by_category": {k: len(v) for k, v in by_cat.items()},
        "findings": all_findings,
    }
    (OUT_DIR / "footer-social-report.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    # Markdown report
    md: list[str] = []
    md.append("# Footer Social Icon — Build Failure Report")
    md.append("")
    md.append(f"- Footer assets audited: **{len(asset_paths)}**")
    md.append(f"- HTML pages audited: **{len(html_paths)}**")
    md.append(f"- Total issues: **{len(all_findings)}**")
    md.append("")
    md.append("## Category counts")
    for cat in ("URL_DRIFT", "MISSING_PLATFORM", "MISSING_ALT", "DUP_ICON"):
        md.append(f"- {cat}: **{len(by_cat.get(cat, []))}**")
    md.append("")
    if not all_findings:
        md.append("> No issues found — footer social layer is consistent.")
    else:
        for cat in ("URL_DRIFT", "MISSING_PLATFORM", "MISSING_ALT", "DUP_ICON"):
            items = by_cat.get(cat, [])
            if not items:
                continue
            md.append(f"## {cat} ({len(items)})")
            md.append("")
            md.append("| # | File | Line | Element | URL found | Expected |")
            md.append("|---|------|------|---------|-----------|----------|")
            for i, f in enumerate(items, 1):
                el = (f["element"] or "").replace("|", "\\|")
                md.append(f"| {i} | `{f['file']}` | {f['line'] or '-'} | {el} | `{f['url_found']}` | `{f['url_expected']}` |")
            md.append("")

    (OUT_DIR / "footer-social-report.md").write_text("\n".join(md), encoding="utf-8")

    # Stdout summary
    print(f"Assets audited : {len(asset_paths)}  → {[str(p.name) for p in asset_paths]}")
    print(f"HTML pages     : {len(html_paths)}")
    print(f"Total issues   : {len(all_findings)}")
    for cat, items in by_cat.items():
        print(f"  - {cat}: {len(items)}")
    print()
    print(f"Reports written:")
    print(f"  - {OUT_DIR / 'footer-social-report.md'}")
    print(f"  - {OUT_DIR / 'footer-social-report.json'}")
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())