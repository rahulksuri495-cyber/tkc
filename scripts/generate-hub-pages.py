#!/usr/bin/env python3
"""Generate new SEO hub pages by composing head template + header + custom content + footer."""
from pathlib import Path
import re
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent

HEAD = (ROOT / "_templates" / "head.html").read_text(encoding="utf-8")
HEADER = (ROOT / "_templates" / "header.html").read_text(encoding="utf-8")
FOOTER = (ROOT / "_templates" / "footer.html").read_text(encoding="utf-8")


def replace_tag(text, tag_pattern, new_tag, flags=re.S):
    return re.sub(tag_pattern, new_tag, text, flags=flags, count=1)


def build_head(title, description, canonical_path, keywords, faqs):
    url = f"https://tkctalent.com{canonical_path}"
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tkctalent.com/"},
                {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": url},
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": "TKC Talent",
            "image": "https://tkctalent.com/og-image.jpg",
            "url": url,
            "telephone": "+91-95995-99699",
            "email": "hello@tkctalent.com",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "600, CR Park",
                "addressLocality": "New Delhi",
                "addressRegion": "Delhi",
                "postalCode": "110019",
                "addressCountry": "IN",
            },
            "areaServed": "IN",
            "priceRange": "₹₹₹₹",
            "description": description,
        },
    ]
    if faqs:
        schemas.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faqs
            ],
        })

    schema_tags = "".join(
        f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schemas
    )

    head = HEAD
    head = replace_tag(head, r"<title>.*?</title>", f"<title>{title}</title>")
    head = replace_tag(head, r'<meta name="description" content=".*?"/>', f'<meta name="description" content="{description}"/>')
    head = replace_tag(head, r'<meta name="keywords" content=".*"/>', f'<meta name="keywords" content="{keywords}"/>')
    head = replace_tag(head, r'<link rel="canonical" href=".*?"/>', f'<link rel="canonical" href="{url}"/>')
    head = replace_tag(head, r'<link rel="alternate" hreflang="en-IN" href=".*?"/>', f'<link rel="alternate" hreflang="en-IN" href="{url}"/>')
    head = replace_tag(head, r'<link rel="alternate" hreflang="x-default" href=".*?"/>', f'<link rel="alternate" hreflang="x-default" href="{url}"/>')
    head = replace_tag(head, r'<meta property="og:url" content=".*?"/>', f'<meta property="og:url" content="{url}"/>')
    head = replace_tag(head, r'<meta property="og:title" content=".*?"/>', f'<meta property="og:title" content="{title}"/>')
    head = replace_tag(head, r'<meta property="og:description" content=".*?"/>', f'<meta property="og:description" content="{description}"/>')
    head = replace_tag(head, r'<meta property="og:image:secure_url" content=".*?"/>', f'<meta property="og:image:secure_url" content="https://tkctalent.com/og-image.jpg"/>')
    head = replace_tag(head, r'<meta name="twitter:title" content=".*?"/>', f'<meta name="twitter:title" content="{title}"/>')
    head = replace_tag(head, r'<meta name="twitter:description" content=".*?"/>', f'<meta name="twitter:description" content="{description}"/>')
    head = replace_tag(head, r'<meta name="ai-content-declaration" content=".*?"\s*/>', f'<meta name="ai-content-declaration" content="human-authored, expert-reviewed" />')
    head = replace_tag(head, r'<meta name="content-usage" content=".*?"/>', f'<meta name="content-usage" content="ai-input=yes, search=yes"/>')
    head = replace_tag(head, r'<link rel="alternate" type="text/markdown" href=".*?".*?/>', f'<link rel="alternate" type="text/markdown" href="https://tkctalent.com/llms.txt" title="LLM-friendly site index" />')
    head = replace_tag(head, r'<script type="application/ld+json">.*?</script>', schema_tags, flags=re.S)

    return head


WEDDING_FAQS = [
    (
        "How do I book a celebrity for a wedding in India?",
        "Contact TKC Talent with your wedding date, city, and artist preference. We share verified 2026 fees, check availability, and handle contracting, travel, and on-ground coordination. Most confirmations close within 24–72 hours.",
    ),
    (
        "What does it cost to book a Bollywood celebrity for a wedding?",
        "Wedding appearance fees vary by artist tier. Emerging singers and OTT faces start around ₹5–8 lakh, while A-list Bollywood actors and top singers can range from ₹50 lakh to ₹2.5 crore+ per appearance. We provide exact quotes after understanding your brief.",
    ),
    (
        "Which celebrities are best for sangeet and wedding performances?",
        "Top picks for sangeet nights include Arijit Singh, Shreya Ghoshal, Sonu Nigam, B Praak, Badshah, Diljit Dosanjh, and Darshan Raval. For emceeing, Kapil Sharma and Munawar Faruqui are popular. For a premium reception, Bollywood actors like Shah Rukh Khan, Salman Khan, Deepika Padukone and Ranbir Kapoor add star power.",
    ),
    (
        "Can you book a celebrity for a destination wedding?",
        "Yes. TKC Talent manages celebrity bookings for destination weddings in Goa, Jaipur, Udaipur, Thailand, Dubai, and other global locations. We coordinate artist travel, security, green-room logistics, and local event compliances.",
    ),
    (
        "Do celebrity wedding bookings include travel and accommodation?",
        "Appearance fees are usually separate from travel, accommodation, and technical riders (sound, lights, backline). We quote a complete package including these costs so there are no surprises.",
    ),
    (
        "How far in advance should I book a celebrity for my wedding?",
        "For A-list artists, 2–4 months in advance is ideal. For wedding season peak dates (November–February), we recommend 4–6 months. Last-minute bookings are possible depending on the artist's schedule.",
    ),
    (
        "Can the celebrity perform at a private residence or farmhouse?",
        "Yes, provided the venue meets safety, security, and technical requirements. We inspect the location and arrange necessary clearances, artist transport, and backstage areas.",
    ),
    (
        "What is the payment structure for wedding celebrity bookings?",
        "Typically 50% advance to block the date, with the balance 50% before the event. Exact terms vary by artist and are documented in the contract we share with you.",
    ),
    (
        "Do you also book celebrities for wedding brand endorsements?",
        "Yes. TKC Talent negotiates brand association and wedding gifting collaborations with celebrities, including Instagram mentions, red-carpet appearances, and curated content.",
    ),
    (
        "Which cities do you serve for wedding celebrity bookings?",
        "We book celebrities for weddings across Delhi NCR, Mumbai, Bangalore, Hyderabad, Chennai, Pune, Jaipur, Goa, and international destinations. We also have strong local event partners in every major market.",
    ),
]


def build_wedding_hub():
    title = "Book Celebrities for Weddings in India 2026 | Singers, Actors & Comedians for Sangeet & Reception | TKC Talent"
    description = "Book celebrities for weddings in India — Bollywood actors, singers, comedians for sangeet, reception & destination weddings. Verified 2026 fees, pan-India bookings & quote in 24 hrs."
    keywords = "book celebrity for wedding, book singer for wedding, wedding celebrity booking, bollywood celebrity wedding, celebrity for sangeet, celebrity wedding appearance, destination wedding celebrity, book celebrity for reception, wedding singer india, celebrity wedding entertainment"
    canonical_path = "/book-celebrity-for-wedding/"

    head = build_head(title, description, canonical_path, keywords, WEDDING_FAQS)

    body = f'''
{HEADER}
<main class="w-full">

  <!-- Hero -->
  <section class="relative overflow-hidden bg-[#0a0a0a] px-6 py-20 sm:px-10 sm:py-28 lg:py-36">
    <div class="mx-auto max-w-7xl">
      <div class="grid gap-12 lg:grid-cols-2 lg:items-center">
        <div class="space-y-6">
          <p class="text-sm font-semibold uppercase tracking-widest text-amber-400">Wedding Entertainment Experts</p>
          <h1 class="font-display text-4xl font-bold leading-tight sm:text-5xl lg:text-6xl">
            Book Celebrities for Weddings in India
          </h1>
          <p class="text-lg text-foreground/80">
            Book Bollywood actors, playback singers, comedians and OTT stars for your sangeet, reception, destination wedding or private celebration. Verified 2026 fees, pan-India coordination, and dedicated artist management from TKC Talent.
          </p>
          <div class="flex flex-wrap gap-4">
            <a href="mailto:hello&#64;tkctalent.com?subject=Request%20Celebrity%20for%20Wedding" class="inline-flex items-center justify-center rounded-full bg-amber-400 px-8 py-3 text-sm font-semibold text-[#0a0a0a] hover:bg-amber-300">Request a Wedding Quote</a>
            <a href="tel:+919599599699" class="inline-flex items-center justify-center rounded-full border border-foreground/20 px-8 py-3 text-sm font-semibold hover:bg-foreground/5">Speak to Our Team</a>
          </div>
        </div>
        <div class="relative">
          <img src="/assets/break-weddings-u686lYKx.webp" alt="Celebrity performance at an Indian wedding reception" class="w-full rounded-2xl object-cover shadow-2xl" loading="lazy" width="800" height="600"/>
        </div>
      </div>
    </div>
  </section>

  <!-- Intro -->
  <section class="px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-4xl text-center">
      <h2 class="font-display text-3xl font-bold sm:text-4xl">Make Your Wedding the Event Everyone Talks About</h2>
      <p class="mt-6 text-lg text-foreground/70">
        A celebrity appearance at a wedding turns a celebration into a headline. Whether it is a soulful Arijit Singh ballad for the sangeet, a surprise Kapil Sharma comedy set for the cocktail, or a Shah Rukh Khan walk-in for the reception, TKC Talent has booked the biggest names for India's most prestigious weddings. With 20+ years of event management expertise and direct access to artist managers, we help you choose, contract, and execute the perfect celebrity moment — safely, on time, and on budget.
      </p>
    </div>
  </section>

  <!-- Wedding Moments -->
  <section class="bg-[#0f0f0f] px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-7xl">
      <h2 class="font-display text-center text-3xl font-bold sm:text-4xl">Celebrity Appearances for Every Wedding Moment</h2>
      <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-2xl border border-foreground/10 bg-background p-6">
          <h3 class="font-display text-xl font-bold">Sangeet Night</h3>
          <p class="mt-3 text-sm text-foreground/70">Book singers, bands or choreographed dance acts to electrify the sangeet stage.</p>
        </div>
        <div class="rounded-2xl border border-foreground/10 bg-background p-6">
          <h3 class="font-display text-xl font-bold">Cocktail Party</h3>
          <p class="mt-3 text-sm text-foreground/70">Comedians, DJs and performers create an intimate, high-energy vibe.</p>
        </div>
        <div class="rounded-2xl border border-foreground/10 bg-background p-6">
          <h3 class="font-display text-xl font-bold">Reception Grand Entry</h3>
          <p class="mt-3 text-sm text-foreground/70">A-list actor or singer appearances for a show-stopping reception moment.</p>
        </div>
        <div class="rounded-2xl border border-foreground/10 bg-background p-6">
          <h3 class="font-display text-xl font-bold">Destination Wedding</h3>
          <p class="mt-3 text-sm text-foreground/70">We coordinate travel, visas, security and technical production overseas.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Top Artists -->
  <section class="px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-7xl">
      <h2 class="font-display text-center text-3xl font-bold sm:text-4xl">Most Booked Celebrities for Weddings</h2>
      <p class="mx-auto mt-4 max-w-3xl text-center text-foreground/70">These artists are consistently requested for sangeet, reception and destination wedding events.</p>
      <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <a href="/book-arijit-singh/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Arijit Singh</h3>
          <p class="mt-2 text-sm text-foreground/60">Wedding & sangeet performances</p>
        </a>
        <a href="/book-shreya-ghoshal/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Shreya Ghoshal</h3>
          <p class="mt-2 text-sm text-foreground/60">Sangeet and classical fusion</p>
        </a>
        <a href="/book-diljit-dosanjh/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Diljit Dosanjh</h3>
          <p class="mt-2 text-sm text-foreground/60">Punjabi wedding energy</p>
        </a>
        <a href="/book-badshah/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Badshah</h3>
          <p class="mt-2 text-sm text-foreground/60">High-energy rap and dance</p>
        </a>
        <a href="/book-sonu-nigam/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Sonu Nigam</h3>
          <p class="mt-2 text-sm text-foreground/60">Elegant reception concerts</p>
        </a>
        <a href="/book-kapil-sharma/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Kapil Sharma</h3>
          <p class="mt-2 text-sm text-foreground/60">Comedy and hosting</p>
        </a>
        <a href="/book-shah-rukh-khan/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Shah Rukh Khan</h3>
          <p class="mt-2 text-sm text-foreground/60">Premium reception appearances</p>
        </a>
        <a href="/book-salman-khan/" class="group rounded-2xl border border-foreground/10 p-6 transition hover:border-amber-400/50">
          <h3 class="font-display text-lg font-bold group-hover:text-amber-400">Salman Khan</h3>
          <p class="mt-2 text-sm text-foreground/60">Grand entry and photo-ops</p>
        </a>
      </div>
    </div>
  </section>

  <!-- How It Works -->
  <section class="bg-[#0f0f0f] px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-7xl">
      <h2 class="font-display text-center text-3xl font-bold sm:text-4xl">How to Book a Celebrity for Your Wedding</h2>
      <div class="mt-12 grid gap-8 sm:grid-cols-3">
        <div class="relative rounded-2xl border border-foreground/10 bg-background p-8">
          <span class="font-display text-4xl font-bold text-amber-400">01</span>
          <h3 class="mt-4 font-display text-xl font-bold">Share Your Brief</h3>
          <p class="mt-3 text-sm text-foreground/70">Tell us the date, city, wedding moment, budget and artist wish-list. We respond within 24 hours.</p>
        </div>
        <div class="relative rounded-2xl border border-foreground/10 bg-background p-8">
          <span class="font-display text-4xl font-bold text-amber-400">02</span>
          <h3 class="mt-4 font-display text-xl font-bold">Get Verified Options</h3>
          <p class="mt-3 text-sm text-foreground/70">We confirm artist availability, share exact fees, and recommend alternatives that fit your budget.</p>
        </div>
        <div class="relative rounded-2xl border border-foreground/10 bg-background p-8">
          <span class="font-display text-4xl font-bold text-amber-400">03</span>
          <h3 class="mt-4 font-display text-xl font-bold">Confirm & Celebrate</h3>
          <p class="mt-3 text-sm text-foreground/70">Contract, advance, travel coordination and on-ground artist management — handled end-to-end.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Cities -->
  <section class="px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-7xl">
      <h2 class="font-display text-center text-3xl font-bold sm:text-4xl">Wedding Celebrity Bookings Across India</h2>
      <div class="mt-10 flex flex-wrap justify-center gap-3">
        <a href="/celebrity-booking-delhi/" class="rounded-full border border-foreground/20 px-5 py-2 text-sm hover:bg-foreground/5">Delhi NCR</a>
        <a href="/celebrity-booking-mumbai/" class="rounded-full border border-foreground/20 px-5 py-2 text-sm hover:bg-foreground/5">Mumbai</a>
        <a href="/celebrity-booking-jaipur/" class="rounded-full border border-foreground/20 px-5 py-2 text-sm hover:bg-foreground/5">Jaipur</a>
        <a href="/celebrity-booking-goa/" class="rounded-full border border-foreground/20 px-5 py-2 text-sm hover:bg-foreground/5">Goa</a>
        <a href="/event-planners-delhi/" class="rounded-full border border-foreground/20 px-5 py-2 text-sm hover:bg-foreground/5">Event Planners Delhi</a>
        <a href="/event-management-gurgaon/" class="rounded-full border border-foreground/20 px-5 py-2 text-sm hover:bg-foreground/5">Gurgaon</a>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="bg-[#0f0f0f] px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-4xl">
      <h2 class="font-display text-center text-3xl font-bold sm:text-4xl">Wedding Celebrity Booking FAQs</h2>
      <div class="mt-10 space-y-4">
        {''.join(f'''<details class="rounded-2xl border border-foreground/10 bg-background p-6">
          <summary class="cursor-pointer font-display text-lg font-semibold">{q}</summary>
          <p class="mt-4 text-foreground/70">{a}</p>
        </details>''' for q, a in WEDDING_FAQS)}
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="px-6 py-16 sm:px-10 lg:py-24">
    <div class="mx-auto max-w-4xl text-center">
      <h2 class="font-display text-3xl font-bold sm:text-4xl">Ready to Book a Celebrity for Your Wedding?</h2>
      <p class="mt-6 text-lg text-foreground/70">Share your wedding date, city, and preferred celebrity. Our team will reply within 24 hours with verified 2026 fees and availability.</p>
      <div class="mt-8 flex flex-wrap justify-center gap-4">
        <a href="mailto:hello&#64;tkctalent.com?subject=Book%20Celebrity%20for%20Wedding" class="inline-flex items-center justify-center rounded-full bg-amber-400 px-8 py-3 text-sm font-semibold text-[#0a0a0a] hover:bg-amber-300">Email Your Wedding Brief</a>
        <a href="tel:+919599599699" class="inline-flex items-center justify-center rounded-full border border-foreground/20 px-8 py-3 text-sm font-semibold hover:bg-foreground/5">Call +91 95995 99699</a>
      </div>
    </div>
  </section>

</main>
{FOOTER}
</body></html>
'''

    html = f"<!DOCTYPE html><html lang=\"en\">{head}{body}"
    out_dir = ROOT / "book-celebrity-for-wedding"
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {out_dir / 'index.html'} ({len(html)} bytes)")


if __name__ == "__main__":
    build_wedding_hub()
