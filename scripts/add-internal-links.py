#!/usr/bin/env python3
"""Insert internal link blocks to new hub pages on the homepage and service pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def add_to_homepage():
    p = ROOT / "index.html"
    src = p.read_text(encoding="utf-8")
    if "/book-celebrity-for-wedding/" in src:
        print("Homepage already links to wedding hub.")
        return
    # Insert a small section before </footer>
    block = '''<section class="px-6 py-16 sm:px-10 lg:py-20"><div class="mx-auto max-w-7xl rounded-3xl border border-foreground/10 bg-[#0f0f0f] p-8 sm:p-12"><h2 class="font-display text-2xl font-bold sm:text-3xl">Explore Our Celebrity Booking Guides</h2><p class="mt-4 text-foreground/70">Detailed, city-wise and event-specific guides to help you book the right artist at the right fee.</p><div class="mt-8 flex flex-wrap gap-4"><a href="/book-celebrity-for-wedding/" class="inline-flex items-center rounded-full bg-amber-400 px-6 py-3 text-sm font-semibold text-[#0a0a0a] hover:bg-amber-300">Book Celebrity for Wedding</a><a href="/celebrity-management-company/" class="inline-flex items-center rounded-full border border-foreground/20 px-6 py-3 text-sm font-semibold hover:bg-foreground/5">Celebrity Management Company</a><a href="/top-indian-celebrities/" class="inline-flex items-center rounded-full border border-foreground/20 px-6 py-3 text-sm font-semibold hover:bg-foreground/5">Top Indian Celebrities 2026</a></div></div></section>'''
    src = src.replace("</footer>", f"{block}</footer>", 1)
    p.write_text(src, encoding="utf-8")
    print("Added hub links to homepage.")


def add_to_service_page():
    p = ROOT / "ourservice" / "index.html"
    if not p.is_file():
        print("ourservice page not found.")
        return
    src = p.read_text(encoding="utf-8")
    if "/book-celebrity-for-wedding/" in src:
        print("ourservice already links to wedding hub.")
        return
    block = '''<section class="px-6 py-16 sm:px-10 lg:py-20"><div class="mx-auto max-w-7xl rounded-3xl border border-foreground/10 bg-[#0f0f0f] p-8 sm:p-12 text-center"><h2 class="font-display text-2xl font-bold sm:text-3xl">Book a Celebrity for Your Wedding</h2><p class="mx-auto mt-4 max-w-2xl text-foreground/70">From sangeet singers to Bollywood reception appearances, we handle celebrity bookings for weddings across India.</p><a href="/book-celebrity-for-wedding/" class="mt-8 inline-flex items-center rounded-full bg-amber-400 px-8 py-3 text-sm font-semibold text-[#0a0a0a] hover:bg-amber-300">View Wedding Booking Guide</a></div></section>'''
    src = src.replace("</footer>", f"{block}</footer>", 1)
    p.write_text(src, encoding="utf-8")
    print("Added wedding hub link to ourservice.")


if __name__ == "__main__":
    add_to_homepage()
    add_to_service_page()
