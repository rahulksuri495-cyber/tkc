#!/usr/bin/env python3
"""Generate the three Durga Puja 2026 keyword landing pages from the hub page shell."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HUB = ROOT / "durga-puja-2026" / "index.html"
BASE = "https://tkctalent.com"
IMG = "/durga-puja-2026/images"
WA = ("https://wa.me/919599599699?text=Hi%20TKC%20Talent%2C%20I%20want%20to%20book%20a%20stall%20%2F%20"
      "sponsorship%20for%20Durga%20Puja%202026%20at%20CR%20Park%2C%20Delhi.")

BTN_PRIMARY = ("inline-flex items-center justify-center rounded-full bg-amber-400 px-8 py-3 "
               "text-sm font-semibold text-[#0a0a0a] hover:bg-amber-300")
BTN_GHOST = ("inline-flex items-center justify-center rounded-full border border-amber-400/60 px-8 py-3 "
             "text-sm font-semibold text-amber-300 hover:bg-amber-400/10")


def shell() -> tuple[str, str]:
    source = HUB.read_text(encoding="utf-8")
    header = source[source.index('<nav class="flex items-center'):source.index('<main class="w-full">')]
    footer = source[source.index("</main>") + len("</main>"):]
    return header, footer


def picture(name: str, alt: str, sizes: str, eager: bool = False) -> str:
    srcset_webp = ", ".join(f"{IMG}/{name}-{w}.webp {w}w" for w in (480, 720, 1200))
    srcset_jpg = ", ".join(f"{IMG}/{name}-{w}.jpg {w}w" for w in (480, 720, 1200))
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (
        f'<picture><source type="image/webp" srcset="{srcset_webp}" sizes="{sizes}"/>'
        f'<img src="{IMG}/{name}-1200.jpg" srcset="{srcset_jpg}" sizes="{sizes}" alt="{alt}" title="{alt}" '
        f'width="1200" height="900" {loading} class="h-full w-full rounded-2xl object-cover"/></picture>'
    )


def cta_row() -> str:
    return (
        f'<div class="mt-8 flex flex-wrap gap-4">'
        f'<a href="tel:+919599599699" class="{BTN_PRIMARY}">Call +91 95995 99699</a>'
        f'<a href="{WA}" target="_blank" rel="noopener" class="{BTN_GHOST}">WhatsApp 95995 99699</a></div>'
    )


def faq_block(faqs: list[tuple[str, str]]) -> str:
    items = "".join(
        f'<details class="rounded-2xl border border-foreground/10 bg-[#0f0f0f] p-6">'
        f'<summary class="cursor-pointer font-display text-lg font-semibold">{q}</summary>'
        f'<p class="mt-3 text-sm text-foreground/70">{a}</p></details>'
        for q, a in faqs
    )
    return f'<div class="mt-8 grid gap-4">{items}</div>'


def head(page: dict) -> str:
    url = f"{BASE}{page['path']}"
    hero = f"{BASE}{IMG}/{page['hero']}-1200.jpg"
    ld = json.dumps(page["schema"], ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"""<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="author" content="The Kabir Company"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
<meta name="theme-color" content="#0a0a0a"/>
<meta name="geo.region" content="IN-DL"/><meta name="geo.placename" content="Chittaranjan Park, New Delhi"/>
<meta name="geo.position" content="28.5355;77.2503"/><meta name="ICBM" content="28.5355, 77.2503"/>
<title>{page['title']}</title>
<meta name="description" content="{page['description']}"/>
<meta name="keywords" content="{page['keywords']}"/>
<link rel="canonical" href="{url}"/>
<link rel="alternate" hreflang="en-IN" href="{url}"/><link rel="alternate" hreflang="x-default" href="{url}"/>
<meta property="og:site_name" content="TKC Talent"/><meta property="og:type" content="website"/><meta property="og:locale" content="en_IN"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{page['title']}"/>
<meta property="og:description" content="{page['description']}"/>
<meta property="og:image" content="{hero}"/><meta property="og:image:type" content="image/jpeg"/>
<meta property="og:image:width" content="1200"/><meta property="og:image:height" content="900"/>
<meta property="og:image:alt" content="{page['hero_alt']}"/>
<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:site" content="@tkctalent"/><meta name="twitter:creator" content="@tkctalent"/>
<meta name="twitter:title" content="{page['title']}"/>
<meta name="twitter:description" content="{page['description']}"/>
<meta name="twitter:image" content="{hero}"/><meta name="twitter:image:alt" content="{page['hero_alt']}"/>
<meta name="news_keywords" content="{page['keywords']}"/>
<link rel="alternate" type="text/markdown" href="{BASE}/llms.txt" title="LLM-friendly site index"/>
<meta name="ai-content-declaration" content="human-authored, expert-reviewed"/>
<meta name="content-usage" content="ai-input=yes, search=yes"/>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;700&amp;display=swap"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;700&amp;display=swap"/>
<link rel="stylesheet" href="/assets/styles-B3eDpzGa.css"/>
<link rel="preload" as="image" href="{BASE}{IMG}/{page['hero']}-1200.jpg" fetchpriority="high"/>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WQF5WX2TTB"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-WQF5WX2TTB');</script>
<script type="application/ld+json">{ld}</script>
<script defer src="/assets/nav-enhance-v3.js"></script>
<script defer src="/assets/durga-tracking.js"></script>
</head><body class="bg-background text-foreground antialiased" data-tkc-page="{page['path']}">
"""


def breadcrumb(name: str, path: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Durga Puja 2026 — CR Park",
                     "item": f"{BASE}/durga-puja-2026/"},
                    {"@type": "ListItem", "position": 3, "name": name, "item": f"{BASE}{path}"},
                ],
            }
        ],
    }


def with_service(name: str, path: str, service: dict, faqs: list[tuple[str, str]]) -> dict:
    schema = breadcrumb(name, path)
    schema["@graph"].append(service)
    schema["@graph"].append({
        "@type": "FAQPage",
        "@id": f"{BASE}{path}#faq",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
            for q, a in faqs
        ],
    })
    return schema


CR_PARK_FAQS = [
    ("When is Durga Puja 2026 at CR Park?",
     "CR Park Durga Puja 2026 runs from Maha Shashti on 16 October to Vijaya Dashami on 20 October 2026, with pandals open from early morning until late night."),
    ("Which are the biggest pandals in CR Park?",
     "Co-operative Ground (B Block), Mela Ground (K Block), Nabapalli, Pocket 40 and Kali Mandir Society draw the largest crowds, together attracting several lakh visitors across the five days."),
    ("How do brands get visibility in CR Park during Durga Puja?",
     "Through stalls, pandal title sponsorship, gate and archway branding, sampling activations, food-court presence and cultural-night title rights. TKC Talent handles committee approvals for all of these."),
    ("How do I reach CR Park during Durga Puja?",
     "Nearest Metro stations are Nehru Enclave and Greater Kailash on the Magenta Line; roads inside CR Park are largely pedestrianised during the five days, so plan parking outside the market blocks."),
]

STALL_FAQS = [
    ("How much does a Durga Puja stall cost in 2026?",
     "CR Park and Delhi NCR stall rates for 2026 start around Rs 60,000 for a compact 6x6 ft FMCG or accessories counter and go up to Rs 3.5 lakh+ for large food-court and automobile display spaces for the full five days."),
    ("What is included in a Durga Puja stall booking?",
     "Space allotment, fabrication and branding, electrical load, vendor and staff passes, committee approvals, and on-ground support from set-up before Shashti through Dashami."),
    ("Which stall categories perform best at Durga Puja?",
     "Food and beverage, ethnic fashion and jewellery, FMCG sampling, mobile and electronics, automobile displays, banking and insurance lead-generation desks, and kids' activity zones."),
    ("How early should I book a Durga Puja stall?",
     "Gate-facing, stage-facing and food-court frontage is usually gone by July. Book by June-July 2026 for the best positions; a 50% advance blocks the space."),
]

SPONSOR_FAQS = [
    ("What Durga Puja sponsorship packages are available in 2026?",
     "Title sponsorship, co-powered-by, associate sponsor, cultural-night sponsor, gate and archway branding, and category-exclusive sampling rights across CR Park and Delhi NCR pandals."),
    ("How much does Durga Puja title sponsorship cost?",
     "Title sponsorship of a major CR Park pandal typically ranges from Rs 12 lakh to Rs 40 lakh depending on footfall, while co-powered and associate slots start from roughly Rs 3 lakh."),
    ("What reach does a Durga Puja sponsorship deliver?",
     "Large CR Park pandals record 1-3 lakh visitors each over five days, plus press coverage, live-stream mentions, influencer content and cultural-night stage branding."),
    ("Can sponsorship include celebrity or artist performances?",
     "Yes. TKC Talent is an artist booking agency, so sponsorship can bundle singers, bands, anchors and influencers for cultural nights with your brand as presenting partner."),
]


PAGES = [
    {
        "path": "/cr-park-durga-puja/",
        "hero": "durga-puja-2026-cr-park-pandal-crowd",
        "hero_alt": "Crowds at a CR Park Durga Puja pandal in South Delhi during Durga Puja 2026",
        "title": "CR Park Durga Puja 2026 | Pandals, Dates & Brand Guide",
        "description": "CR Park Durga Puja 2026 guide: pandal list, 16-20 Oct dates, footfall, timings and how brands book stalls or sponsorship. Call/WhatsApp 95995 99699.",
        "keywords": "cr park durga puja, cr park durga puja 2026, chittaranjan park durga puja, durga puja delhi cr park, cr park pandal list",
        "h1": "CR Park Durga Puja 2026 — Pandals, Dates and Brand Opportunities",
        "intro": "Chittaranjan Park is Delhi's Bengali heartland and the epicentre of Durga Puja in North India. Across five days in October 2026, its blocks host more than a dozen major pandals with lakhs of visitors moving between them from morning pushpanjali to midnight dhunuchi naach.",
        "name": "CR Park Durga Puja",
        "faqs": CR_PARK_FAQS,
        "service": {
            "@type": "Place",
            "@id": f"{BASE}/cr-park-durga-puja/#place",
            "name": "Chittaranjan Park (CR Park) Durga Puja",
            "address": {"@type": "PostalAddress", "addressLocality": "Chittaranjan Park",
                        "addressRegion": "Delhi", "postalCode": "110019", "addressCountry": "IN"},
            "geo": {"@type": "GeoCoordinates", "latitude": 28.5355, "longitude": 77.2503},
        },
        "sections": [
            ("pandals", "Major CR Park Durga Puja pandals in 2026", [
                "Co-operative Ground, B Block — the largest and oldest CR Park puja, known for its themed pandal and evening cultural programme.",
                "Mela Ground, K Block — the busiest food and shopping circuit, ideal for F&B and FMCG stalls.",
                "Nabapalli Puja — a traditional daaker saaj idol with strong family footfall.",
                "Pocket 40 Puja — younger crowd, music-led cultural nights.",
                "Kali Mandir Society — devotional focus with heavy morning aarti footfall.",
            ]),
            ("footfall", "Footfall, timings and visitor profile", [
                "Peak footfall runs Saptami to Navami between 6 PM and midnight, with a second morning peak for Ashtami pushpanjali.",
                "Each major ground records roughly 1-3 lakh visitors across the five days; the whole CR Park circuit crosses 10 lakh visits.",
                "Audience skews affluent South Delhi families, young professionals from GK, Kalkaji and Nehru Place, plus tourists and press.",
            ]),
            ("brands", "Why brands activate at CR Park", [
                "High-intent festive spending window with families shopping for apparel, gold, electronics and cars.",
                "Concentrated pedestrian traffic — a single stall can reach a full-city audience without media buying.",
                "Cultural-night stages give sponsors on-stage branding, anchor mentions and press pick-up.",
            ]),
        ],
    },
    {
        "path": "/book-stalls-durga-puja/",
        "hero": "durga-puja-2026-themed-pandal-delhi",
        "hero_alt": "Illuminated themed Durga Puja pandal in Delhi where brand stalls are set up for Durga Puja 2026",
        "title": "Book Stalls in Durga Puja 2026 | Delhi & CR Park Rates",
        "description": "Book stalls in Durga Puja 2026 at CR Park and Delhi NCR. Food, FMCG, fashion and auto stall sizes, 2026 rates and booking steps. Call/WhatsApp 95995 99699.",
        "keywords": "book stalls in durga puja, durga puja stall booking, durga puja stall booking delhi, durga puja food stall booking, durga puja stall price 2026",
        "h1": "Book Stalls in Durga Puja 2026 — CR Park &amp; Delhi NCR",
        "intro": "Stall space at Delhi's Durga Puja grounds is the single highest-ROI festive retail buy of the year: five days, pedestrian-only footfall and a buying audience. TKC Talent books, fabricates and runs stalls across CR Park and Delhi NCR pandals.",
        "name": "Book Stalls in Durga Puja",
        "faqs": STALL_FAQS,
        "service": {
            "@type": "Service",
            "@id": f"{BASE}/book-stalls-durga-puja/#service",
            "name": "Durga Puja 2026 stall booking — CR Park and Delhi NCR",
            "serviceType": "Exhibition stall booking",
            "areaServed": {"@type": "City", "name": "Delhi NCR"},
            "provider": {"@type": "Organization", "name": "TKC Talent", "url": BASE,
                         "telephone": "+91-95995-99699"},
            "offers": {"@type": "AggregateOffer", "priceCurrency": "INR", "lowPrice": "60000",
                       "highPrice": "350000", "offerCount": "6"},
        },
        "sections": [
            ("sizes", "Stall sizes and 2026 indicative rates", [
                "6x6 ft kiosk (FMCG, accessories, sampling) — from Rs 60,000 for five days.",
                "10x10 ft standard stall (fashion, jewellery, services) — from Rs 1.2 lakh.",
                "10x20 ft food-court stall with kitchen load — from Rs 2.2 lakh.",
                "Automobile / large display bay near the gate — from Rs 3.5 lakh.",
                "Rates vary by pandal, position and category exclusivity; final quotes are shared with the site map.",
            ]),
            ("categories", "Best-performing stall categories", [
                "Food and beverage — highest conversion, strongest repeat footfall across all five evenings.",
                "Ethnic fashion, sarees and jewellery — peaks on Ashtami and Navami.",
                "FMCG sampling and new-product launches — sample volumes of 10,000+ per pandal.",
                "Banking, insurance and telecom lead desks — walk-in lead capture at scale.",
                "Automobile test-drive bookings and kids' activity zones.",
            ]),
            ("process", "How the stall booking process works", [
                "Share your category, preferred size and budget on call or WhatsApp.",
                "Receive pandal-wise site maps, footfall data and the 2026 rate card within 24 hours.",
                "Block position with a 50% advance — frontage sells out first.",
                "We handle fabrication, branding artwork, electrical load, passes and committee approvals.",
                "On-ground managers support your team through 16-20 October.",
            ]),
        ],
    },
    {
        "path": "/durga-puja-sponsorship/",
        "hero": "durga-puja-2026-evening-aarti-lights",
        "hero_alt": "Durga idol framed by festive lights at a sponsored Delhi Durga Puja 2026 pandal",
        "title": "Durga Puja Sponsorship 2026 | Delhi & CR Park Packages",
        "description": "Durga Puja sponsorship 2026 in Delhi and CR Park: title, co-powered, gate branding and cultural-night packages with reach data. Call/WhatsApp 95995 99699.",
        "keywords": "durga puja sponsorship, durga puja sponsorship 2026, durga puja title sponsor delhi, pandal sponsorship cr park, durga puja brand activation",
        "h1": "Durga Puja Sponsorship 2026 — Delhi &amp; CR Park Packages",
        "intro": "Durga Puja sponsorship puts your brand on the pandal gate, the cultural-night stage and every visitor photograph for five days. TKC Talent negotiates and executes sponsorship rights with CR Park and Delhi NCR puja committees.",
        "name": "Durga Puja Sponsorship",
        "faqs": SPONSOR_FAQS,
        "service": {
            "@type": "Service",
            "@id": f"{BASE}/durga-puja-sponsorship/#service",
            "name": "Durga Puja 2026 sponsorship and brand activation — Delhi NCR",
            "serviceType": "Event sponsorship",
            "areaServed": {"@type": "City", "name": "Delhi NCR"},
            "provider": {"@type": "Organization", "name": "TKC Talent", "url": BASE,
                         "telephone": "+91-95995-99699"},
            "offers": {"@type": "AggregateOffer", "priceCurrency": "INR", "lowPrice": "300000",
                       "highPrice": "4000000", "offerCount": "5"},
        },
        "sections": [
            ("packages", "Sponsorship packages and indicative investment", [
                "Title sponsor (Pandal presented by) — Rs 12 lakh to Rs 40 lakh at flagship CR Park grounds.",
                "Co-powered by — Rs 6 lakh to Rs 12 lakh with gate and stage branding.",
                "Associate sponsor — Rs 3 lakh to Rs 6 lakh with banner, anchor mentions and sampling rights.",
                "Cultural-night sponsor — Rs 4 lakh upwards for one evening's stage, LED and artist association.",
                "Gate, archway and selfie-point branding — Rs 1.5 lakh upwards.",
            ]),
            ("deliverables", "What sponsors receive", [
                "Naming rights across pandal gate, archways, banners, LED walls and volunteer merchandise.",
                "Stage mentions by anchors through every cultural programme, plus artist meet-and-greets.",
                "Category exclusivity within the ground and sampling or lead-capture rights.",
                "Press releases, influencer coverage, live-stream logo presence and a post-event reach report.",
            ]),
            ("reach", "Reach and measurement", [
                "1-3 lakh visitors per major pandal over five days, largely affluent South Delhi households.",
                "Earned media across Delhi city press, Bengali community media and social creators.",
                "Post-event report with footfall estimates, sampling counts, leads captured and media clippings.",
            ]),
        ],
    },
]


def render(page: dict, header: str, footer: str) -> str:
    schema = with_service(page["name"], page["path"], page["service"], page["faqs"])
    page = {**page, "schema": schema}
    sections = ""
    for index, (sid, heading, bullets) in enumerate(page["sections"]):
        tone = ' class="bg-[#0f0f0f] px-6 py-16 sm:px-10 lg:py-20"' if index % 2 else ' class="px-6 py-16 sm:px-10 lg:py-20"'
        items = "".join(
            f'<li class="rounded-2xl border border-foreground/10 bg-background p-5 text-sm text-foreground/75">{b}</li>'
            for b in bullets
        )
        sections += (
            f'<section id="{sid}"{tone}><div class="mx-auto max-w-6xl">'
            f'<h2 class="font-display text-3xl font-bold sm:text-4xl">{heading}</h2>'
            f'<ul class="mt-8 grid gap-4 md:grid-cols-2">{items}</ul></div></section>\n'
        )

    related = "".join(
        f'<a href="{other["path"]}" class="rounded-2xl border border-foreground/10 bg-background p-5 '
        f'text-sm font-semibold text-amber-300 hover:border-amber-400/50">{other["name"]} &rarr;</a>'
        for other in PAGES if other["path"] != page["path"]
    )

    hero_sizes = "(max-width:1024px) 92vw, 45vw"
    return (
        head(page)
        + header
        + '<main class="w-full">\n'
        + '<nav aria-label="Breadcrumb" class="px-6 pt-6 sm:px-10"><ol class="flex flex-wrap gap-2 text-xs text-foreground/60">'
        + '<li><a href="/" class="hover:opacity-70">Home</a></li><li aria-hidden="true">/</li>'
        + '<li><a href="/durga-puja-2026/" class="hover:opacity-70">Durga Puja 2026</a></li><li aria-hidden="true">/</li>'
        + f'<li aria-current="page" class="text-foreground/80">{page["name"]}</li></ol></nav>\n'
        + '<section id="hero" class="px-6 py-14 sm:px-10 sm:py-20"><div class="mx-auto grid max-w-7xl gap-10 lg:grid-cols-2 lg:items-center">'
        + '<div class="space-y-6"><p class="text-sm font-semibold uppercase tracking-widest text-amber-400">16 &ndash; 20 October 2026 &middot; Chittaranjan Park, South Delhi</p>'
        + f'<h1 class="font-display text-4xl font-bold leading-tight sm:text-5xl">{page["h1"]}</h1>'
        + f'<p class="text-lg text-foreground/80">{page["intro"]}</p>'
        + cta_row()
        + '<p class="text-sm text-foreground/60">Part of our complete <a href="/durga-puja-2026/" class="text-amber-300 underline">Durga Puja 2026 CR Park stall booking &amp; sponsorship hub</a>.</p>'
        + '</div>'
        + f'<div class="aspect-[4/3]">{picture(page["hero"], page["hero_alt"], hero_sizes, eager=True)}</div>'
        + '</div></section>\n'
        + sections
        + '<section id="faq" class="px-6 py-16 sm:px-10 lg:py-20"><div class="mx-auto max-w-5xl">'
        + f'<h2 class="font-display text-3xl font-bold sm:text-4xl">{page["name"]} &mdash; FAQs</h2>'
        + faq_block(page["faqs"]) + '</div></section>\n'
        + '<section id="related" class="bg-[#0f0f0f] px-6 py-16 sm:px-10 lg:py-20"><div class="mx-auto max-w-6xl">'
        + '<h2 class="font-display text-3xl font-bold sm:text-4xl">Continue on the Durga Puja 2026 hub</h2>'
        + '<div class="mt-8 grid gap-4 md:grid-cols-3">'
        + f'<a href="/durga-puja-2026/" class="rounded-2xl border border-amber-400/50 bg-background p-5 text-sm font-semibold text-amber-300">Durga Puja 2026 &mdash; CR Park hub &rarr;</a>{related}</div>'
        + cta_row()
        + '</div></section>\n</main>'
        + footer
    )


def main() -> None:
    header, footer = shell()
    for page in PAGES:
        target = ROOT / page["path"].strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(page, header, footer), encoding="utf-8")
        print("wrote", target.relative_to(ROOT))


if __name__ == "__main__":
    main()
