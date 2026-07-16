#!/usr/bin/env python3
"""Validate LocalBusiness / Review / FAQPage / Person / BreadcrumbList JSON-LD
on every artist (book-*) page. Fails CI on parse errors or missing required
fields so schema regressions are caught before deploy.

Also spot-checks that city hubs (celebrity-booking-<city>) and service
listing hubs (singer-booking-india, comedian-booking-india, etc.) carry a
BreadcrumbList so internal linking + crawl signals stay consistent.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARTIST_GLOB = "book-*/index.html"
HUB_PATHS = [
    "celebrity-booking-delhi/index.html",
    "celebrity-booking-mumbai/index.html",
    "celebrity-booking-gurgaon/index.html",
    "celebrity-booking-noida/index.html",
    "celebrity-booking-jaipur/index.html",
    "celebrity-booking-goa/index.html",
    "celebrity-booking-india/index.html",
    "singer-booking-india/index.html",
    "comedian-booking-india/index.html",
    "influencer-booking-india/index.html",
    "pan-india-celebrity-booking/index.html",
    "celebrity-dj-booking/index.html",
    "ourservice/index.html",
]

JSONLD_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.S | re.I,
)

# Artist-page requirements
ARTIST_REQUIRED_TYPES = {"Person", "FAQPage", "LocalBusiness", "BreadcrumbList"}
PERSON_REQUIRED = {"name", "image", "jobTitle"}
LOCALBUSINESS_REQUIRED = {"name", "address", "telephone"}
FAQ_MIN_QUESTIONS = 4
BREADCRUMB_MIN_ITEMS = 2


def iter_nodes(node):
    """Yield every dict inside a JSON-LD block (handles @graph and arrays)."""
    if isinstance(node, list):
        for n in node:
            yield from iter_nodes(n)
    elif isinstance(node, dict):
        yield node
        for v in node.values():
            if isinstance(v, (list, dict)):
                yield from iter_nodes(v)


def types_of(n: dict) -> set[str]:
    t = n.get("@type")
    if isinstance(t, list):
        return set(t)
    if isinstance(t, str):
        return {t}
    return set()


def collect_by_type(nodes, wanted: str):
    return [n for n in nodes if wanted in types_of(n)]


def validate_artist(path: Path) -> list[str]:
    errors: list[str] = []
    html = path.read_text(encoding="utf-8", errors="ignore")
    blocks = JSONLD_RE.findall(html)
    if not blocks:
        return [f"{path}: no JSON-LD blocks"]

    all_nodes: list[dict] = []
    for i, block in enumerate(blocks):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError as e:
            errors.append(f"{path}: JSON-LD block #{i+1} invalid JSON: {e}")
            continue
        all_nodes.extend(iter_nodes(data))

    present_types = {t for n in all_nodes for t in types_of(n)}
    for req in ARTIST_REQUIRED_TYPES:
        if req not in present_types:
            errors.append(f"{path}: missing {req} JSON-LD")

    for person in collect_by_type(all_nodes, "Person"):
        missing = [f for f in PERSON_REQUIRED if not person.get(f)]
        if missing:
            errors.append(f"{path}: Person missing fields: {', '.join(missing)}")

    for lb in collect_by_type(all_nodes, "LocalBusiness"):
        missing = [f for f in LOCALBUSINESS_REQUIRED if not lb.get(f)]
        if missing:
            errors.append(f"{path}: LocalBusiness missing fields: {', '.join(missing)}")
        agg = lb.get("aggregateRating")
        if agg and isinstance(agg, dict):
            if not agg.get("ratingValue") or not agg.get("reviewCount"):
                errors.append(f"{path}: AggregateRating missing ratingValue/reviewCount")

    for review in collect_by_type(all_nodes, "Review"):
        rating = review.get("reviewRating") or {}
        if not (isinstance(rating, dict) and rating.get("ratingValue")):
            errors.append(f"{path}: Review missing reviewRating.ratingValue")
        if not review.get("author"):
            errors.append(f"{path}: Review missing author")

    for faq in collect_by_type(all_nodes, "FAQPage"):
        qs = faq.get("mainEntity") or []
        if not isinstance(qs, list) or len(qs) < FAQ_MIN_QUESTIONS:
            errors.append(
                f"{path}: FAQPage has {len(qs) if isinstance(qs,list) else 0} "
                f"question(s), need ≥{FAQ_MIN_QUESTIONS}")
        else:
            for q in qs:
                if not (isinstance(q, dict) and q.get("name")
                        and isinstance(q.get("acceptedAnswer"), dict)
                        and q["acceptedAnswer"].get("text")):
                    errors.append(f"{path}: FAQ Question missing name/acceptedAnswer.text")
                    break

    for bc in collect_by_type(all_nodes, "BreadcrumbList"):
        items = bc.get("itemListElement") or []
        if len(items) < BREADCRUMB_MIN_ITEMS:
            errors.append(f"{path}: BreadcrumbList needs ≥{BREADCRUMB_MIN_ITEMS} items")
        for it in items:
            if not (isinstance(it, dict) and it.get("position")
                    and it.get("name") and it.get("item")):
                errors.append(f"{path}: BreadcrumbList item missing position/name/item")
                break

    return errors


def validate_hub(path: Path) -> list[str]:
    if not path.is_file():
        return [f"{path}: hub page missing"]
    errors: list[str] = []
    html = path.read_text(encoding="utf-8", errors="ignore")
    blocks = JSONLD_RE.findall(html)
    all_nodes: list[dict] = []
    for i, block in enumerate(blocks):
        try:
            all_nodes.extend(iter_nodes(json.loads(block.strip())))
        except json.JSONDecodeError as e:
            errors.append(f"{path}: JSON-LD block #{i+1} invalid JSON: {e}")
    if not collect_by_type(all_nodes, "BreadcrumbList"):
        errors.append(f"{path}: missing BreadcrumbList JSON-LD")
    return errors


def main() -> int:
    all_errors: list[str] = []
    artist_pages = sorted(ROOT.glob(ARTIST_GLOB))
    for p in artist_pages:
        all_errors.extend(validate_artist(p))
    for rel in HUB_PATHS:
        all_errors.extend(validate_hub(ROOT / rel))

    print(f"Artist pages scanned: {len(artist_pages)}")
    print(f"Hub pages scanned:    {len(HUB_PATHS)}")
    if all_errors:
        print(f"\n{len(all_errors)} schema issue(s):\n")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print("All artist + hub JSON-LD blocks parse cleanly and satisfy required fields ✓")
    return 0


if __name__ == "__main__":
    sys.exit(main())