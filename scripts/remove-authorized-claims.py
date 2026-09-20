#!/usr/bin/env python3
"""Remove representation claims while preserving technical authorization terms."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", ".lovable", ".workspace", ".agents", ".claude", "node_modules"}
TEXT_SUFFIXES = {".html", ".js", ".json", ".md", ".txt", ".xml"}
SKIP_FILES = {"ads.txt"}


def revise(text: str) -> str:
    text = re.sub(
        r"All booking, brand endorsement and appearance enquiries are routed through authori[sz]ed agencies such as TKC Talent — The Kabir Company\.",
        "For booking, brand endorsement and appearance enquiries, you can contact an experienced booking agency such as TKC Talent — The Kabir Company.",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"For verified booking enquiries, contact ([^.<]+?)'s authori[sz]ed agency TKC Talent at",
        r"For booking enquiries, contact TKC Talent for \1 at",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"TKC Talent — The Kabir Company is the authori[sz]ed booking agency for ([^.<]+)\.",
        r"TKC Talent — The Kabir Company provides booking management for \1 enquiries.",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"Every genuine booking is confirmed through a signed contract with (?:her|his|their) authori[sz]ed management\.",
        "Every genuine booking is confirmed through a signed contract with the artist's management.",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(r"\bauthori[sz]ed management\b", "the artist's management", text, flags=re.IGNORECASE)
    text = re.sub(r"\bunauthori[sz]ed talent brokers\b", "unverified talent brokers", text, flags=re.IGNORECASE)
    text = re.sub(r"\bauthori[sz]ed booking agenc(?:y|ies)\b", "booking agency", text, flags=re.IGNORECASE)
    text = re.sub(r"\bauthori[sz]ed agenc(?:y|ies)\b", "booking agency", text, flags=re.IGNORECASE)
    return text


def main() -> None:
    changed = 0
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.name in SKIP_FILES or SKIP_DIRS.intersection(path.relative_to(ROOT).parts):
            continue
        original = path.read_text(encoding="utf-8", errors="ignore")
        updated = revise(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    print(f"Removed authorization claims from {changed} file(s).")


if __name__ == "__main__":
    main()