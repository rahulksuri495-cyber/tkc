#!/usr/bin/env python3
"""Insert contextual internal links to /durga-puja-2026/ on relevant pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BLOCKS = {
    "index.html": (
        "Durga Puja 2026 &mdash; CR Park, Delhi",
        "Stall booking and sponsorship for Delhi's biggest Durga Puja are open. See "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 stall booking and sponsorship in CR Park</a> "
        "for dates (16&ndash;20 October), rate cards and package tiers.",
    ),
    "event-planners-delhi/index.html": (
        "Durga Puja 2026 in Delhi",
        "Planning a festive activation? Our "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 CR Park stall booking guide</a> "
        "covers pandal footfall, kiosk sizes and sponsorship slots across South Delhi.",
    ),
    "event-management-gurgaon/index.html": (
        "Durga Puja 2026 activations near Gurgaon",
        "Brands from Gurgaon and Delhi NCR book festive kiosks every October. Compare "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 stall and sponsorship packages at CR Park</a> "
        "before slots close.",
    ),
    "ourservice/index.html": (
        "Festival stall booking &amp; sponsorship",
        "Beyond celebrity bookings, we handle festival retail and branding. Explore "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 stall booking in CR Park</a> "
        "and title, co-powered and cultural-night sponsorship options.",
    ),
    "celebrity-management-company/index.html": (
        "Durga Puja 2026 cultural nights",
        "We programme celebrity cultural nights at Delhi pandals. See "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 sponsorship and cultural night packages at CR Park</a>.",
    ),
    "blog/corporate-event-management-india/index.html": (
        "Festive-season corporate activations",
        "October is peak season for brand activations in Delhi. Our "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 CR Park stall booking and sponsorship guide</a> "
        "lists 2026 rate bands and lead times.",
    ),
    "book-celebrity-for-wedding/index.html": (
        "Festival bookings: Durga Puja 2026",
        "Booking artists for a festival instead of a wedding? See "
        "<a href=\"/durga-puja-2026/\" class=\"text-amber-300 underline underline-offset-4\">Durga Puja 2026 at CR Park, Delhi</a> "
        "for cultural night, stall and sponsorship options.",
    ),
}

TPL = ('<section class="px-6 py-12 sm:px-10"><div class="mx-auto max-w-7xl rounded-3xl border '
       'border-amber-400/20 bg-[#0f0f0f] p-8 sm:p-10"><h2 class="font-display text-2xl font-bold '
       'sm:text-3xl">{h}</h2><p class="mt-4 max-w-3xl text-foreground/70">{p}</p></div></section>')


def main():
    for rel, (h, p) in BLOCKS.items():
        f = ROOT / rel
        if not f.is_file():
            print(f"skip (missing): {rel}")
            continue
        src = f.read_text(encoding="utf-8")
        if "/durga-puja-2026/" in src:
            print(f"skip (already linked): {rel}")
            continue
        block = TPL.format(h=h, p=p)
        if "</footer>" in src:
            src = src.replace("</footer>", block + "</footer>", 1)
        elif "</main>" in src:
            src = src.replace("</main>", block + "</main>", 1)
        else:
            print(f"skip (no anchor): {rel}")
            continue
        f.write_text(src, encoding="utf-8")
        print(f"linked: {rel}")


if __name__ == "__main__":
    main()
