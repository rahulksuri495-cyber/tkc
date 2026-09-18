#!/usr/bin/env python3
"""Describe TKC Talent as a booking agency without implying exclusive representation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SINGER_SLUGS = (
    "ar-rahman", "altaf-raja", "arijit-singh", "armaan-malik", "b-praak",
    "badshah", "darshan-raval", "diljit-dosanjh", "guru-randhawa",
    "hanumankind", "jasmine-sandlas", "jonita-gandhi", "jubin-nautiyal",
    "kanika-kapoor", "kumar-sanu", "lucky-ali", "meet-bros", "mohit-chauhan",
    "neha-bhasin", "neha-kakkar", "palak-muchhal", "pritam",
    "sachet-parampara", "sachin-jigar", "salim-sulaiman", "sara-gurpal",
    "shamsher-lehri", "shankar-mahadevan", "shreya-ghoshal", "sonu-nigam",
    "sunanda-sharma", "tanishk-bagchi", "vishal-shekhar",
)

REPLACEMENTS = (
    (
        " — a division of The Kabir Company since 2005 — manages availability confirmation,",
        " — an artist booking agency and a division of The Kabir Company since 2005 — manages availability confirmation,",
    ),
    (" represented for live bookings by TKC Talent ", " available for live booking through TKC Talent "),
    ("Official booking agency for ", "Artist booking agency for "),
    ("authorised booking agency for ", "booking agency for "),
    ("authorized booking agency for ", "booking agency for "),
)


def update(path: Path, replacements: tuple[tuple[str, str], ...]) -> bool:
    html = path.read_text(encoding="utf-8")
    revised = html
    for old, new in replacements:
        revised = revised.replace(old, new)
    if revised == html:
        return False
    path.write_text(revised, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for slug in SINGER_SLUGS:
        path = ROOT / f"book-{slug}" / "index.html"
        if path.exists() and update(path, REPLACEMENTS):
            changed += 1

    hub_replacements = (
        ("Direct Artist Access", "Singer Booking Agency"),
        (
            "First-hand relationships with celebrity managers across Bollywood, music and digital — built over 20+ years. No middlemen, no inflated markups.",
            "TKC Talent coordinates singer availability, commercial proposals, contracts and event delivery with artist management teams.",
        ),
    )
    for path in (
        ROOT / "singer-booking-india" / "index.html",
        ROOT / "assets" / "CategoryPageLayout-BZ1ShLCw.js",
    ):
        if update(path, hub_replacements):
            changed += 1

    print(f"Updated booking-agency wording on {changed} page(s).")


if __name__ == "__main__":
    main()