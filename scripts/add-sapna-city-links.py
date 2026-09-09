#!/usr/bin/env python3
"""Insert a localised 'Book Sapna Choudhary in <City>' block into city pages
and the event/artist listing pages, so her booking page is reachable and
localised from Delhi, Mumbai, Kolkata and Bangalore intent pages."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARK = "sapna-city-block"

CARD = ("rounded-2xl border border-foreground/10 bg-foreground/[0.03] p-6")

TARGETS = {
    "celebrity-booking-delhi": ("Delhi NCR", "farmhouse weddings, sangeet nights, melas and college fests across Delhi, Gurgaon and Noida", "&#8377;10&#8211;15 lakh"),
    "celebrity-booking-mumbai": ("Mumbai", "brand launches, club nights and corporate shows in Mumbai, with flights, stay and local production handled", "&#8377;10&#8211;15 lakh + travel"),
    "celebrity-booking-gurgaon": ("Gurgaon", "hotel weddings, corporate annual days and society melas in Gurgaon", "&#8377;10&#8211;15 lakh"),
    "celebrity-booking-noida": ("Noida", "corporate events, college fests and open-ground stage shows in Noida and Greater Noida", "&#8377;10&#8211;15 lakh"),
    "celebrity-booking-jaipur": ("Jaipur", "destination weddings, palace sangeets and cultural nights in Jaipur", "&#8377;10&#8211;15 lakh + travel"),
    "durga-puja-2026": ("Kolkata &amp; CR Park", "Durga Puja pandal cultural nights and festival ground stage shows", "&#8377;10&#8211;15 lakh + travel"),
    "corporate-event-management": ("Bangalore &amp; pan-India", "corporate annual days, dealer meets and campus festivals with GST-compliant invoicing", "&#8377;12&#8211;15 lakh"),
    "haryanvi-artist-booking": None,  # already lists her
}


def block(city, blurb, fee):
    return (
        f'<section class="mt-14 px-6 sm:px-10" data-{MARK}>'
        f'<div class="mx-auto max-w-5xl {CARD}">'
        f'<h2 class="font-display text-xl font-bold sm:text-2xl">Book Sapna Choudhary in {city}</h2>'
        f'<p class="mt-3 text-sm text-foreground/80">Sapna Choudhary — Haryanvi stage dancer and singer — is '
        f'booked through TKC Talent for {blurb}. Indicative fee: <strong>{fee}</strong>, plus 18% GST, travel and stay.</p>'
        f'<ul class="mt-4 list-disc space-y-1 pl-5 text-sm text-foreground/80">'
        f'<li>Stage show / mela &#8377;10 lakh · Wedding &amp; sangeet &#8377;15 lakh</li>'
        f'<li>College fest &#8377;8&#8211;10 lakh · Corporate event &#8377;12&#8211;15 lakh</li>'
        f'<li>Signed contract, artist rider, travel, security and production handled end to end</li></ul>'
        f'<p class="mt-4 text-sm"><a class="underline font-semibold" href="/book-sapna-choudhary/">See Sapna Choudhary booking price &amp; contact</a>'
        f' · <a class="underline" href="tel:+919599599699">+91 95995 99699</a>'
        f' · <a class="underline" href="/haryanvi-artist-booking/">Haryanvi artists</a></p>'
        f'</div></section>'
    )


def main():
    changed = []
    for slug, cfg in TARGETS.items():
        if cfg is None:
            continue
        p = ROOT / slug / "index.html"
        if not p.is_file():
            print("skip (missing):", slug)
            continue
        src = p.read_text(encoding="utf-8")
        if MARK in src:
            print("already linked:", slug)
            continue
        if "</main>" not in src:
            print("no </main>:", slug)
            continue
        src = src.replace("</main>", block(*cfg) + "</main>", 1)
        p.write_text(src, encoding="utf-8")
        changed.append(slug)
    print("updated:", ", ".join(changed) or "none")


if __name__ == "__main__":
    main()
