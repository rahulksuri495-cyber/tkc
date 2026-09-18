#!/usr/bin/env python3
"""Remove exclusivity marketing claims while retaining fee and contract terminology."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKIP = {"dist", "node_modules", ".git", ".lovable", ".agents", ".claude", ".workspace"}
TEXT_SUFFIXES = {".html", ".js", ".txt", ".xml"}

REPLACEMENTS = (
    ("exclusive access, the best pricing and complete event management support", "booking management, transparent pricing and complete event support"),
    ("exclusive access, the best pricing, and complete event management support", "booking management, transparent pricing, and complete event support"),
    ("exclusive relationships with Bollywood's top celebrity managers", "established booking relationships with Bollywood's top celebrity managers"),
    ("exclusive relationships with Bollywood&#x27;s top celebrity managers", "established booking relationships with Bollywood&#x27;s top celebrity managers"),
    ("exclusive relationships with India's most influential celebrity managers", "established booking relationships with India's most influential celebrity managers"),
    ("exclusive relationships with India&#x27;s most influential celebrity managers", "established booking relationships with India&#x27;s most influential celebrity managers"),
    ("assigned exclusively to your event", "assigned to your event"),
    ("India's most exclusive private weddings", "India's highest-profile private weddings"),
    ("India&#x27;s most exclusive private weddings", "India&#x27;s highest-profile private weddings"),
    ("India's most exclusive wedding celebrations", "India's highest-profile wedding celebrations"),
    ("India&#x27;s most exclusive wedding celebrations", "India&#x27;s highest-profile wedding celebrations"),
    ("Book Tamannah Bhatia exclusively with TKC Talent.", "Book Tamannaah Bhatia through TKC Talent's booking management team."),
    ("featured exclusively by TKC Talent", "featured by TKC Talent for booking enquiries"),
    ("posing for an exclusive TKC Talent celebrity booking feature", "featured for TKC Talent celebrity booking management"),
    ("Celebrity appearances and live entertainment for exclusive private villa parties", "Celebrity appearances and live entertainment for private villa parties"),
)


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if SKIP.intersection(path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        revised = text
        for old, new in REPLACEMENTS:
            revised = revised.replace(old, new)
        if revised != text:
            path.write_text(revised, encoding="utf-8")
            changed += 1
    print(f"Removed exclusivity claims from {changed} file(s).")


if __name__ == "__main__":
    main()