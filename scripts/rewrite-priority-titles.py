#!/usr/bin/env python3
"""Rewrite title tags and meta descriptions for priority artist pages."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

PRIORITY = [
    "book-varun-dhawan",
    "book-munawar-faruqui",
    "book-sonu-nigam",
    "book-palak-muchhal",
    "book-anushka-sharma",
    "book-ar-rahman",
    "book-shahid-kapoor",
    "book-b-praak",
    "book-sidharth-malhotra",
    "book-pankaj-tripathi",
    "book-kriti-sanon",
    "book-salman-khan",
    "book-shah-rukh-khan",
    "book-alia-bhatt",
    "book-deepika-padukone",
    "book-diljit-dosanjh",
    "book-shreya-ghoshal",
    "book-darshan-raval",
    "book-katrina-kaif",
    "book-ranbir-kapoor",
    "book-akshay-kumar",
    "book-nora-fatehi",
]

# Event-type hints for known artists
ARTIST_EVENTS = {
    "book-munawar-faruqui": "Comedy, Corporate & Private Shows",
    "book-ar-rahman": "Concert, Corporate & Wedding",
    "book-sonu-nigam": "Wedding, Sangeet & Concert",
    "book-palak-muchhal": "Wedding, Sangeet & Concert",
    "book-b-praak": "Wedding, Sangeet & Concert",
    "book-shreya-ghoshal": "Wedding, Sangeet & Concert",
    "book-darshan-raval": "Wedding, Sangeet & Concert",
    "book-diljit-dosanjh": "Wedding, Concert & Corporate",
    "book-sidharth-malhotra": "Brand, Corporate & Wedding",
    "book-pankaj-tripathi": "Corporate, Brand & Wedding",
    "book-varun-dhawan": "Brand, Corporate & Wedding",
    "book-shahid-kapoor": "Brand, Corporate & Wedding",
    "book-kriti-sanon": "Brand, Corporate & Wedding",
    "book-salman-khan": "Brand, Wedding & Corporate",
    "book-shah-rukh-khan": "Brand, Wedding & Corporate",
    "book-alia-bhatt": "Brand, Wedding & Corporate",
    "book-deepika-padukone": "Brand, Wedding & Corporate",
    "book-katrina-kaif": "Brand, Wedding & Corporate",
    "book-ranbir-kapoor": "Brand, Wedding & Corporate",
    "book-akshay-kumar": "Brand, Corporate & Wedding",
    "book-anushka-sharma": "Brand, Corporate & Wedding",
    "book-nora-fatehi": "Brand, Wedding & Private Event",
}

def display_name(slug):
    return slug.replace("book-", "").replace("-", " ").title().replace("Ar ", "AR ").replace("B Praak", "B Praak")

def proper_artist_name(slug):
    mapping = {
        "book-varun-dhawan": "Varun Dhawan",
        "book-munawar-faruqui": "Munawar Faruqui",
        "book-sonu-nigam": "Sonu Nigam",
        "book-palak-muchhal": "Palak Muchhal",
        "book-anushka-sharma": "Anushka Sharma",
        "book-ar-rahman": "AR Rahman",
        "book-shahid-kapoor": "Shahid Kapoor",
        "book-b-praak": "B Praak",
        "book-sidharth-malhotra": "Sidharth Malhotra",
        "book-pankaj-tripathi": "Pankaj Tripathi",
        "book-kriti-sanon": "Kriti Sanon",
        "book-salman-khan": "Salman Khan",
        "book-shah-rukh-khan": "Shah Rukh Khan",
        "book-alia-bhatt": "Alia Bhatt",
        "book-deepika-padukone": "Deepika Padukone",
        "book-diljit-dosanjh": "Diljit Dosanjh",
        "book-shreya-ghoshal": "Shreya Ghoshal",
        "book-darshan-raval": "Darshan Raval",
        "book-katrina-kaif": "Katrina Kaif",
        "book-ranbir-kapoor": "Ranbir Kapoor",
        "book-akshay-kumar": "Akshay Kumar",
        "book-nora-fatehi": "Nora Fatehi",
    }
    return mapping.get(slug, display_name(slug))

def new_title(artist, slug):
    events = ARTIST_EVENTS.get(slug, "Wedding, Corporate & Private Events")
    return f"{artist} Booking Fees, Price & Availability 2026 | {events} | TKC Talent"

def new_description(artist, slug):
    events = ARTIST_EVENTS.get(slug, "weddings, corporate events and private shows")
    # Lowercase event types for description
    events_lower = events.lower().replace(" &", ",").replace(", private event", " private event")
    return f"Verified 2026 {artist} booking fees and price. Book {artist} for {events_lower} across India. Pan-India bookings, direct management access & quote in 24 hrs via TKC Talent."

def rewrite_page(slug):
    p = ROOT / slug / "index.html"
    if not p.is_file():
        print(f"SKIP: {p} not found")
        return False
    src = p.read_text(encoding="utf-8")
    artist = proper_artist_name(slug)
    title = new_title(artist, slug)
    desc = new_description(artist, slug)

    # Replace <title>... </title>
    src = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", src, count=1)
    # Replace meta description content
    src = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{desc}"', src, count=1)
    # Replace og:title
    src = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{title}"', src, count=1)
    # Replace og:description
    src = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{desc}"', src, count=1)
    # Replace twitter:title
    src = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{title}"', src, count=1)
    # Replace twitter:description
    src = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{desc}"', src, count=1)

    p.write_text(src, encoding="utf-8")
    print(f"UPDATED {slug}: {title}")
    return True

if __name__ == "__main__":
    updated = 0
    for slug in PRIORITY:
        if rewrite_page(slug):
            updated += 1
    print(f"\nUpdated {updated} pages.")
