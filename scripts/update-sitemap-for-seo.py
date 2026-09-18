#!/usr/bin/env python3
"""Update sitemap.xml with new hub page and refreshed lastmod for rewritten pages."""
from pathlib import Path
import re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SITEMAP = ROOT / "sitemap.xml"
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

PRIORITY = [
    "book-varun-dhawan",
    "book-munawar-faruqui", "book-sonu-nigam", "book-palak-muchhal",
    "book-anushka-sharma", "book-ar-rahman", "book-shahid-kapoor",
    "book-b-praak", "book-sidharth-malhotra", "book-pankaj-tripathi",
    "book-kriti-sanon", "book-salman-khan",
    "book-shah-rukh-khan", "book-alia-bhatt", "book-deepika-padukone",
    "book-diljit-dosanjh", "book-shreya-ghoshal", "book-darshan-raval",
    "book-katrina-kaif", "book-ranbir-kapoor", "book-akshay-kumar",
    "book-nora-fatehi",
]

text = SITEMAP.read_text(encoding="utf-8")

# Update lastmod for each priority artist page (operate on the whole <url> block so
# a <lastmod> on a following line is replaced, never duplicated)
for slug in PRIORITY:
    loc = f"https://tkctalent.com/{slug}/"

    def update_block(match, loc=loc):
        block = match.group(0)
        if f"<loc>{loc}</loc>" not in block:
            return block
        if "<lastmod>" in block:
            state = {"n": 0}

            def repl(m):
                state["n"] += 1
                return f"<lastmod>{today}</lastmod>" if state["n"] == 1 else ""

            block = re.sub(r"\s*<lastmod>[^<]*</lastmod>", repl, block)
            block = re.sub(r"\n\s*\n", "\n", block)
            return block
        return block.replace(f"<loc>{loc}</loc>", f"<loc>{loc}</loc><lastmod>{today}</lastmod>", 1)

    text = re.sub(r"<url>.*?</url>", update_block, text, flags=re.S)


# Add new hub if not present
if "https://tkctalent.com/book-celebrity-for-wedding/" not in text:
    new_url = f"  <url><loc>https://tkctalent.com/book-celebrity-for-wedding/</loc><lastmod>{today}</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>\n"
    text = text.replace("</urlset>", new_url + "</urlset>")

SITEMAP.write_text(text, encoding="utf-8")
print(f"Updated sitemap.xml with {today} lastmod for {len(PRIORITY)} pages and added new hub.")
