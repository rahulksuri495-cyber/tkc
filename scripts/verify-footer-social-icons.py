#!/usr/bin/env python3
"""Build-time check: footer social icon URLs (both the SPA Footer
bundle and the static-page enhancer at assets/footer-social-icons.js)
must match the canonical brand handles used in JSON-LD and HTML.

Two assertions per footer asset:
  1. Every brand-owned social URL it ships matches the canonical
     entry in scripts/verify_social_urls.CANONICAL.
  2. Every canonical platform we expect to render an icon for is
     actually present in the asset (no silently missing icons).

Usage:  python3 scripts/verify-footer-social-icons.py
Exit:   0 on success, 1 on any drift / missing platform.
"""
from __future__ import annotations
import importlib.util, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Reuse the canonical handle table from the sibling script.
spec = importlib.util.spec_from_file_location(
    "verify_social_urls", ROOT / "scripts" / "verify-social-urls.py"
)
vsu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vsu)  # type: ignore
CANONICAL: dict[str, str] = vsu.CANONICAL
is_brand_url = vsu.is_brand_url

# Platforms that MUST appear in any rendered footer icon set.
REQUIRED_HOSTS = {
    "facebook.com", "instagram.com", "youtube.com",
    "x.com", "pinterest.com", "imdb.com",
}

# Footer assets to audit. Globs cover hashed Vite output.
TARGETS = [
    "assets/footer-social-icons.js",
    "assets/Footer-*.js",
]

URL_RE = re.compile(r'https?://[^\s"\'<>)]+', re.IGNORECASE)

def audit(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    urls = {m.group(0).rstrip('.,;)') for m in URL_RE.finditer(text)}
    brand_urls = {u for u in urls if is_brand_url(u)}

    # 1) Every brand URL must equal its canonical form.
    for url in sorted(brand_urls):
        low = url.lower()
        for host, target in CANONICAL.items():
            if host in low and url != target:
                errors.append(f"{path}: {url} → expected {target}")
                break

    # 2) Every required platform must appear at least once.
    #    The footer-social-icons.js enhancer only renders icons for
    #    links present in the host page, so we check it differently:
    #    its detect() switch must reference every required host so a
    #    future page that adds the link gets a proper icon. The SPA
    #    Footer bundle must literally embed the canonical URL.
    is_enhancer = path.name == "footer-social-icons.js"
    for host in REQUIRED_HOSTS:
        needle = host if is_enhancer else CANONICAL[host]
        if needle not in text:
            errors.append(f"{path}: missing required platform {host} ({needle!r} not found)")
    return errors

def main() -> int:
    paths: list[Path] = []
    for pat in TARGETS:
        paths.extend(sorted(ROOT.glob(pat)))
    if not paths:
        print("❌ no footer assets matched", TARGETS)
        return 1

    all_errors: list[str] = []
    for p in paths:
        all_errors.extend(audit(p))

    if all_errors:
        print(f"❌ footer social icon drift in {len({e.split(':')[0] for e in all_errors})} file(s):\n")
        for e in all_errors:
            print("  -", e)
        print("\nCanonical handles live in scripts/verify-social-urls.py (CANONICAL).")
        print("Required platforms:", ", ".join(sorted(REQUIRED_HOSTS)))
        return 1

    print(f"✅ footer social icons consistent across {len(paths)} asset(s); "
          f"all {len(REQUIRED_HOSTS)} required platforms present.")
    return 0

if __name__ == "__main__":
    sys.exit(main())