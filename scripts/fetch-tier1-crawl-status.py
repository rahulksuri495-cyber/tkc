#!/usr/bin/env python3
"""Inspect the 5 Tier 1 URLs in GSC and write admin/gsc-priority/tier1-status.json.

Tracks: coverage state (Discovered/Crawled/Indexed/Unknown), first-seen date,
last crawl, and days-since-discovery.
"""
import json, os, sys, urllib.request, urllib.error
from datetime import date, datetime, timezone
from pathlib import Path

SITE = "https://tkctalent.com/"
TIER1 = [
    "celebrity-management-company",
    "artist-management-india",
    "event-management-mumbai",
    "event-management-delhi",
    "celebrity-brand-ambassador",
]
GATEWAY = "https://connector-gateway.lovable.dev/google_search_console/v1/urlInspection/index:inspect"
HEADERS = {
    "Authorization": f"Bearer {os.environ['LOVABLE_API_KEY']}",
    "X-Connection-Api-Key": os.environ['GOOGLE_SEARCH_CONSOLE_API_KEY'],
    "Content-Type": "application/json",
}

STATE_FILE = Path("admin/gsc-priority/tier1-status.json")
prev = {}
if STATE_FILE.exists():
    try:
        prev = {p["slug"]: p for p in json.loads(STATE_FILE.read_text()).get("pages", [])}
    except Exception:
        prev = {}

def inspect(url):
    body = {"inspectionUrl": url, "siteUrl": SITE}
    req = urllib.request.Request(GATEWAY, data=json.dumps(body).encode(), headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("ERR", url, e.code, e.read()[:300], file=sys.stderr)
        return {}

def days_between(iso, ref):
    if not iso: return None
    try:
        d = datetime.fromisoformat(iso.replace("Z","+00:00")).date()
        return (ref - d).days
    except Exception:
        return None

today = date.today()
out_pages = []
for slug in TIER1:
    url = f"https://tkctalent.com/{slug}/"
    print("inspect", slug, file=sys.stderr)
    res = inspect(url).get("inspectionResult", {})
    idx = res.get("indexStatusResult", {})
    verdict = idx.get("verdict", "VERDICT_UNSPECIFIED")
    coverage = idx.get("coverageState", "Unknown")
    last_crawl = idx.get("lastCrawlTime")
    indexing_state = idx.get("indexingState", "INDEXING_STATE_UNSPECIFIED")
    google_canonical = idx.get("googleCanonical")
    submitted = "URL is on Google" in coverage or verdict == "PASS"

    is_unknown = "unknown to google" in (coverage or "").lower()
    p = prev.get(slug, {})
    # first_discovered: sticky — first time GSC surfaced the URL (any state other than Unknown)
    first_discovered = p.get("first_discovered")
    if coverage and not is_unknown and not first_discovered:
        first_discovered = today.isoformat()
    first_indexed = p.get("first_indexed")
    if submitted and not first_indexed:
        first_indexed = today.isoformat()

    out_pages.append({
        "slug": slug,
        "url": url,
        "verdict": verdict,
        "coverage_state": coverage,
        "indexing_state": indexing_state,
        "last_crawl_time": last_crawl,
        "google_canonical": google_canonical,
        "first_discovered": first_discovered,
        "first_indexed": first_indexed,
        "days_since_discovery": days_between(first_discovered, today),
        "days_since_last_crawl": days_between(last_crawl, today),
        "is_indexed": submitted,
        "is_unknown": is_unknown,
    })

out = {
    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "site": SITE,
    "pages": out_pages,
    "summary": {
        "total": len(out_pages),
        "indexed": sum(1 for p in out_pages if p["is_indexed"]),
        "discovered_not_indexed": sum(1 for p in out_pages if p["first_discovered"] and not p["is_indexed"]),
        "unknown": sum(1 for p in out_pages if p.get("is_unknown")),
    },
}
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
STATE_FILE.write_text(json.dumps(out, indent=2))
print("wrote", STATE_FILE)
