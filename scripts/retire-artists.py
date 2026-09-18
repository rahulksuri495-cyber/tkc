#!/usr/bin/env python3
"""Retire artist pages sitewide: remove every reference to retired artists
(nav links, gallery cards, fee-table rows, FAQ items, JSON-LD, sitemaps,
minified JS data objects, llms txt files, admin reports).

Retired artists are returned as 410 Gone via .htaccess; this script strips
their mentions so no broken links or stale references remain.

Usage: python3 scripts/retire-artists.py
Idempotent — safe to re-run after regenerating pages.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARTISTS = [
    {
        "slug": "arijit-singh",
        "name": "Arijit Singh",
        "images": ["arijit-singh.jpeg", "actor-arijit-singh.jpg"],
    },
    {
        "slug": "badshah",
        "name": "Badshah",
        "images": ["badshah.jpeg", "actor-badshah.jpg"],
    },
    {
        "slug": "kapil-sharma",
        "name": "Kapil Sharma",
        "images": ["actor-kapil-sharma.jpg"],
    },
]

MARKERS: list[str] = []
for a in ARTISTS:
    MARKERS += [a["slug"], f"book-{a['slug']}", a["name"], *a["images"]]

TEXT_SUFFIXES = {".html", ".js", ".txt", ".md", ".xml"}
JSONLD_RE = re.compile(
    r'(<script[^>]+type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)',
    re.S | re.I,
)

SKIP_DIRS = {"node_modules", ".git", ".lovable"}
SKIP_FILES = {"retire-artists.py"}


def contains_marker(blob: str) -> bool:
    return any(m in blob for m in MARKERS)


def clean_json_node(node):
    """Recursively remove list items / dict entries that reference a retired artist."""
    if isinstance(node, list):
        out = []
        for item in node:
            if isinstance(item, (dict, list)):
                if contains_marker(json.dumps(item, ensure_ascii=False)):
                    continue
                out.append(clean_json_node(item))
            elif isinstance(item, str):
                if contains_marker(item):
                    continue
                out.append(item)
            else:
                out.append(item)
        return out
    if isinstance(node, dict):
        return {k: clean_json_node(v) for k, v in node.items()}
    return node


def renumber_itemlists(node):
    if isinstance(node, dict):
        t = node.get("@type")
        types = set(t) if isinstance(t, list) else {t} if isinstance(t, str) else set()
        if "ItemList" in types and isinstance(node.get("itemListElement"), list):
            for i, item in enumerate(node["itemListElement"], 1):
                if isinstance(item, dict) and item.get("@type") == "ListItem":
                    item["position"] = i
        for v in node.values():
            renumber_itemlists(v)
    elif isinstance(node, list):
        for item in node:
            renumber_itemlists(item)


def clean_json_text(text: str, pretty: bool) -> str:
    data = json.loads(text)
    data = clean_json_node(data)
    renumber_itemlists(data)
    if pretty:
        return json.dumps(data, ensure_ascii=False, indent=2)
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def clean_jsonld_blocks(html: str) -> str:
    def repl(m: re.Match) -> str:
        body = m.group(2).strip()
        if not contains_marker(body):
            return m.group(0)
        try:
            cleaned = clean_json_text(body, pretty=("\n" in body))
        except json.JSONDecodeError:
            return m.group(0)
        return m.group(1) + cleaned + m.group(3)

    return JSONLD_RE.sub(repl, html)


def remove_name_tokens(text: str) -> str:
    for a in ARTISTS:
        n = re.escape(a["name"])
        possessive = n + r"(?:&#x27;|'|&rsquo;)?s?\s+"  # "Arijit Singh's "
        # list-leading: "Name, "
        text = re.sub(possessive + r",\s+", "", text)  # safety no-op ordering
        text = re.sub(n + r"(?:&#x27;|'|&rsquo;)?s?,\s+", "", text)
        # list-trailing: ", Name" / ", and Name" / " and Name"
        text = re.sub(r",\s+(?:and\s+)?" + n + r"\b", "", text)
        text = re.sub(r"\band\s+" + n + r"\b", "", text)
        # "Name and " at start of a list
        text = re.sub(n + r"\s+and\s+", "", text)
        # "Name & " / " & Name"
        text = re.sub(n + r"\s+&amp;\s+", "", text)
        text = re.sub(r"&amp;\s+" + n + r"\b", "", text)
    # tidy leftovers
    text = re.sub(r"—\s*&amp;\s*More", "— India's Top Artists", text)
    text = re.sub(r"—\s*&\s*More", "— India's Top Artists", text)
    text = re.sub(r"(\b(?:like|including|from|such as)\s+),\s+", r"\1 ", text)
    text = re.sub(r",(\s*[).])", r"\1", text)
    text = re.sub(r",\s*,", ",", text)
    text = re.sub(r"\(\s*,", "(", text)
    text = re.sub(r",\s*\)", ")", text)
    text = re.sub(r"  +", " ", text)
    return text


def clean_text(text: str, suffix: str) -> str:
    # 1. <li>...<a href="/book-slug/">...</a></li>  (nav items + gallery cards)
    for a in ARTISTS:
        slug = a["slug"]
        text = re.sub(
            r'<li[^>]*>\s*<a\b[^>]*href="[^"]*book-' + slug + r'[^"]*"[^>]*>[\s\S]*?</a>\s*</li>',
            "",
            text,
        )
        # standalone anchors (cards not wrapped in li, inline links)
        text = re.sub(
            r'<a\b[^>]*href="[^"]*book-' + slug + r'[^"]*"[^>]*>[\s\S]*?</a>',
            "",
            text,
        )
        # fee-table rows
        text = re.sub(r"<tr\b[^>]*>(?:(?!</tr>).)*book-" + slug + r"[\s\S]*?</tr>", "", text)
        text = re.sub(
            r"<tr\b[^>]*>(?:(?!</tr>).)*>" + re.escape(a["name"]) + r"<[\s\S]*?</tr>",
            "",
            text,
        )
    # 2. visible FAQ blocks: <div class="py-7"><dt>...name...</dt><dd>...</dd></div>
    def faq_repl(m: re.Match) -> str:
        return "" if contains_marker(m.group(0)) else m.group(0)

    text = re.sub(
        r'<div class="py-7"><dt\b[\s\S]*?</dd>\s*</div>', faq_repl, text
    )
    # 3. JSON-LD blocks
    text = clean_jsonld_blocks(text)
    # 4. minified JS objects / string entries referencing the slugs
    for a in ARTISTS:
        slug = a["slug"]
        text = re.sub(r"\{[^{}]*book-" + slug + r"[^{}]*\},?", "", text)
        text = re.sub(r'"[^"]*book-' + slug + r'[^"]*",?', "", text)
        for img in a["images"]:
            text = re.sub(r"\{[^{}]*" + re.escape(img) + r"[^{}]*\},?", "", text)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    text = re.sub(r"([\[{])\s*,", r"\1", text)
    text = re.sub(r",\s*,+", ",", text)
    # 5. sitemap <url> / <image:image> blocks
    if suffix == ".xml":
        text = re.sub(
            r"\s*<url>[\s\S]*?</url>",
            lambda m: "" if contains_marker(m.group(0)) else m.group(0),
            text,
        )
        text = re.sub(
            r"\s*<image:image>[\s\S]*?</image:image>",
            lambda m: "" if contains_marker(m.group(0)) else m.group(0),
            text,
        )
    # 6. prose name-token removal
    text = remove_name_tokens(text)
    # 7. llms-style: drop lines that are pure URL entries for retired pages
    if suffix == ".txt":
        lines = []
        for line in text.splitlines():
            if any(f"book-{a['slug']}" in line for a in ARTISTS):
                continue
            lines.append(line)
        text = "\n".join(lines)
    return text


def clean_json_file(path: Path) -> None:
    raw = path.read_text(encoding="utf-8")
    if not contains_marker(raw):
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # fallback: line / regex cleanup
        cleaned = clean_text(raw, ".json")
        path.write_text(cleaned, encoding="utf-8")
        print(f"  cleaned (regex): {path.relative_to(ROOT)}")
        return
    pretty = raw.startswith("{\n") or raw.startswith("[\n")
    cleaned = clean_json_node(data)
    renumber_itemlists(cleaned)
    out = json.dumps(cleaned, ensure_ascii=False, indent=2 if pretty else None)
    path.write_text(out + ("\n" if raw.endswith("\n") else ""), encoding="utf-8")
    print(f"  cleaned (json):  {path.relative_to(ROOT)}")


def main() -> None:
    changed = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if path.name in SKIP_FILES:
            continue
        suffix = path.suffix.lower()
        if suffix == ".json":
            clean_json_file(path)
            continue
        if suffix not in TEXT_SUFFIXES:
            continue
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if not contains_marker(raw):
            continue
        cleaned = clean_text(raw, suffix)
        if cleaned != raw:
            path.write_text(cleaned, encoding="utf-8")
            print(f"  cleaned: {rel}")
            changed += 1
    print(f"\nDone — {changed} text files updated.")


if __name__ == "__main__":
    main()
