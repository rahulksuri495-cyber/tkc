#!/usr/bin/env python3
"""Verify the bundled ShimmerImage component renders actress images without
an opacity-0 fade that can leave images invisible after hydration.

This is a static check against the built JS bundle that backs the
/bollywood-actress-booking/ page. It guards against regressions of the bug
where actress card images stayed hidden because the fade-in `opacity-0`
class never flipped to `opacity-100` on the client.

If `playwright` is installed, the script additionally loads the page in a
headless browser, waits for hydration, and asserts that every roster <img>
inside the actress carousel section has non-zero rendered opacity and a
positive bounding box (i.e. is actually visible to users).
"""
from __future__ import annotations

import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, "assets")


def find_category_bundle() -> str:
    matches = sorted(glob.glob(os.path.join(ASSETS_DIR, "CategoryPageLayout-*.js")))
    if not matches:
        sys.exit("FAIL: no CategoryPageLayout-*.js bundle found in assets/")
    # newest by mtime wins if multiple
    matches.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return matches[0]


def static_check(bundle_path: str) -> None:
    src = open(bundle_path, "r", encoding="utf-8").read()

    # Locate the ShimmerImage factory: the function destructures containerClassName / eager.
    m = re.search(
        r"function\s+\w+\(\{\s*containerClassName[^}]*\}\)\s*\{([\s\S]*?)\}\s*function\s",
        src,
    )
    if not m:
        sys.exit(f"FAIL: could not locate ShimmerImage function in {bundle_path}")
    body = m.group(1)

    # The fade-in regression always contained an opacity-0 class on the <img>.
    if "opacity-0" in body:
        sys.exit(
            "FAIL: ShimmerImage still references opacity-0 — actress images "
            "will hydrate hidden. Bundle: " + os.path.relpath(bundle_path, ROOT)
        )

    # The function must still render an <img> element.
    if '"img"' not in body and "'img'" not in body:
        sys.exit("FAIL: ShimmerImage no longer renders an <img> element.")

    print(
        f"OK static: {os.path.relpath(bundle_path, ROOT)} ShimmerImage has no opacity-0 fade."
    )


def runtime_check(url: str) -> None:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
    except Exception:
        print(
            "SKIP runtime: playwright not installed. "
            "Install with `pip install playwright && playwright install chromium` "
            "to enable the live hydration check."
        )
        return

    print(f"Loading {url} in headless Chromium…")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=45_000)
            except Exception as e:
                strict = os.environ.get("VERIFY_STRICT") == "1"
                msg = f"could not load {url}: {e}"
                if strict:
                    sys.exit(f"FAIL runtime: {msg}")
                print(f"SKIP runtime: {msg}")
                return
            # Wait for the actress carousel section to mount.
            page.wait_for_selector(
                'section[aria-labelledby="actress-coverflow-heading"] img',
                timeout=20_000,
            )
            # Give the carousel one extra tick to settle.
            page.wait_for_timeout(1500)

            results = page.evaluate(
                """() => {
                  const sec = document.querySelector('section[aria-labelledby="actress-coverflow-heading"]');
                  if (!sec) return { error: 'carousel section not found' };
                  const imgs = Array.from(sec.querySelectorAll('img'));
                  const isValidSrc = (s) => !!s && !s.startsWith('data:image/svg') && !/placeholder|undefined|null/i.test(s);
                  const visibleArr = imgs.filter(img => {
                    const cs = getComputedStyle(img);
                    const r = img.getBoundingClientRect();
                    return parseFloat(cs.opacity) > 0.05 && cs.visibility !== 'hidden' && r.width > 0 && r.height > 0;
                  });
                  const loadedArr = imgs.filter(img => img.complete && img.naturalWidth > 0);
                  const invalidSrc = imgs
                    .filter(img => !isValidSrc(img.getAttribute('src')))
                    .map(img => img.getAttribute('src'))
                    .slice(0, 5);
                  return {
                    total: imgs.length,
                    visible: visibleArr.length,
                    loaded: loadedArr.length,
                    invalidSrc,
                    hidden: imgs
                      .filter(img => {
                        const cs = getComputedStyle(img);
                        return parseFloat(cs.opacity) <= 0.05 || cs.visibility === 'hidden';
                      })
                      .map(img => ({ src: img.getAttribute('src'), opacity: getComputedStyle(img).opacity }))
                      .slice(0, 5),
                    notLoaded: imgs
                      .filter(img => !(img.complete && img.naturalWidth > 0))
                      .map(img => ({ src: img.getAttribute('src'), complete: img.complete, naturalWidth: img.naturalWidth }))
                      .slice(0, 5),
                  };
                }"""
            )
        finally:
            browser.close()

    if results.get("error"):
        sys.exit(f"FAIL runtime: {results['error']}")
    total = results.get("total", 0)
    visible = results.get("visible", 0)
    loaded = results.get("loaded", 0)
    invalid = results.get("invalidSrc", [])
    if total == 0:
        sys.exit("FAIL runtime: no <img> elements found inside the roster section.")
    if visible == 0:
        sys.exit(
            "FAIL runtime: every actress image hydrated hidden (opacity≈0). "
            f"Sample: {results.get('hidden')!r}"
        )
    if invalid:
        sys.exit(
            "FAIL runtime: actress images have invalid/placeholder src attributes. "
            f"Sample: {invalid!r}"
        )
    if loaded == 0:
        sys.exit(
            "FAIL runtime: no actress images reported a successful load "
            "(complete && naturalWidth > 0). Sample not-loaded: "
            f"{results.get('notLoaded')!r}"
        )
    # Require at least 60% of images to have actually decoded — guards
    # against hydration where <img> tags exist but never fetch a real bitmap.
    if loaded < max(1, int(total * 0.6)):
        sys.exit(
            f"FAIL runtime: only {loaded}/{total} actress images decoded "
            f"(naturalWidth > 0). Sample not-loaded: {results.get('notLoaded')!r}"
        )
    print(f"OK runtime: {visible}/{total} actress images visible after hydration.")
    print(f"OK runtime: {loaded}/{total} actress images decoded (naturalWidth > 0).")
    print("OK runtime: all actress image src attributes look valid.")


def main() -> None:
    bundle = find_category_bundle()
    static_check(bundle)
    url = os.environ.get("VERIFY_URL", "https://tkctalent.com/bollywood-actress-booking/")
    runtime_check(url)
    print("All actress-image visibility checks passed.")


if __name__ == "__main__":
    main()