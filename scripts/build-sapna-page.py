#!/usr/bin/env python3
"""Build /book-sapna-choudhary/ and /haryanvi-artist-booking/ from the shared
header/footer templates so nav + footer stay identical to the rest of the site."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
HEADER = (ROOT / "_templates" / "header.html").read_text(encoding="utf-8")
FOOTER = (ROOT / "_templates" / "footer.html").read_text(encoding="utf-8")

CSS = '/assets/styles-B3eDpzGa.css'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"/>'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous"/>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;'
         'family=Space+Grotesk:wght@500;700&amp;display=swap"/>')
SCRIPTS = ('<script src="/assets/nav-enhance-v3.js" defer></script>'
           '<script src="/assets/footer-social-icons.js" defer></script>')
TAIL = ('<p style="margin-top:24px;font-size:.9rem;opacity:.7">Enquire: '
        '<a href="tel:+919599599699">+91 95995 99699</a> · '
        '<a href="mailto:hello@tkctalent.com">hello@tkctalent.com</a> · '
        '<a href="/contact-us/">Booking enquiry form</a></p>')


def head(title, desc, url, img, jsonld, og_type="profile"):
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/>'
        '<meta name="viewport" content="width=device-width, initial-scale=1"/>'
        f'<title>{title}</title>'
        '<meta name="author" content="The Kabir Company"/>'
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>'
        '<meta name="theme-color" content="#0a0a0a"/><meta name="geo.region" content="IN"/>'
        f'<meta name="description" content="{desc}"/>'
        '<meta property="og:site_name" content="TKC Talent"/>'
        f'<meta property="og:type" content="{og_type}"/><meta property="og:locale" content="en_IN"/>'
        f'<meta property="og:url" content="{url}"/><meta property="og:title" content="{title}"/>'
        f'<meta property="og:description" content="{desc}"/>'
        f'<meta property="og:image" content="{img}"/><meta property="og:image:width" content="1200"/>'
        '<meta property="og:image:height" content="630"/>'
        '<meta property="og:image:alt" content="Haryanvi stage show produced by TKC Talent — book Sapna Choudhary for events."/>'
        '<meta name="twitter:card" content="summary_large_image"/><meta name="twitter:site" content="@tkctalent"/>'
        f'<meta name="twitter:title" content="{title}"/><meta name="twitter:description" content="{desc}"/>'
        f'<meta name="twitter:image" content="{img}"/>'
        f'<link rel="canonical" href="{url}"/>' + FONTS +
        f'<link rel="stylesheet" href="{CSS}"/>'
        f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>'
        + SCRIPTS + '</head>'
    )


URL = "https://tkctalent.com/book-sapna-choudhary/"
IMG = "https://tkctalent.com/assets/haryanvi/sapna-choudhary-booking-og.jpg"
TITLE = "Sapna Choudhary Booking Price &amp; Contact — Book for Events &amp; Shows | TKC Talent"
DESC = ("Book Sapna Choudhary for stage shows, dance performances, weddings and corporate events. "
        "Get her show booking price, fees and official contact for booking via TKC Talent.")

FAQS = [
    ("How to book Sapna Choudhary for a show?",
     "Call or WhatsApp TKC Talent on +91 95995 99699, email hello@tkctalent.com, or send the booking "
     "enquiry form with your event date, city and budget. TKC Talent checks Sapna Choudhary's availability "
     "and sends a confirmed quote."),
    ("How do I contact Sapna Choudhary for booking?",
     "Booking enquiries are handled by TKC Talent, an authorised agency. Call or WhatsApp "
     "+91 95995 99699 or email hello@tkctalent.com. A booking manager responds within 24 hours."),
    ("How much does Sapna Choudhary charge for a show?",
     "Sapna Choudhary's indicative booking fees are: stage show / mela ₹10 lakh, club show ₹10 lakh, "
     "college fest ₹8–10 lakh, corporate event ₹12–15 lakh, wedding / sangeet ₹15 lakh. Final price depends "
     "on date, city, performance duration and travel. GST at 18%, travel, stay and technical requirements are "
     "billed in addition to the artist fee."),
    ("What is Sapna Choudhary's stage show price for a wedding?",
     "Wedding and sangeet performances start from ₹15 lakh. The exact price depends on the date, city and "
     "performance length. Peak wedding dates cost more than off-season weekdays."),
    ("Can I book Sapna Choudhary for a college fest or corporate event?",
     "Yes. Sapna Choudhary performs at college festivals, corporate annual days, brand activations, melas "
     "and government-backed cultural events. TKC Talent handles the contract, artist rider, travel, security "
     "and on-ground coordination."),
    ("How far in advance should I book Sapna Choudhary?",
     "Book 45–90 days before the event date. For peak wedding season (November–February) and festival "
     "dates, 4–6 months in advance is safer because live dates fill quickly."),
    ("Does TKC Talent book Sapna Choudhary across India?",
     "Yes. TKC Talent books Haryanvi artists for events in Delhi NCR, Gurgaon, Noida, Haryana, Punjab, "
     "Rajasthan, Uttar Pradesh and other states, plus international shows."),
]

JSONLD = {"@context": "https://schema.org", "@graph": [
    {"@type": "Person", "name": "Sapna Choudhary",
     "alternateName": "सपना चौधरी",
     "jobTitle": "Haryanvi Dancer, Singer & Stage Performer",
     "description": "Sapna Choudhary is one of India's best-known Haryanvi stage dancers and singers, famous for large live stage shows, ragini and Haryanvi dance performances.",
     "nationality": "Indian",
     "image": IMG,
     "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
     "knowsAbout": ["Haryanvi dance", "Stage shows", "Live performances", "Wedding performances"]},
    {"@type": "Service", "name": "Sapna Choudhary Booking",
     "serviceType": "Celebrity and artist booking",
     "description": "Official booking service for Sapna Choudhary stage shows, dance performances, weddings, college fests and corporate events in India.",
     "areaServed": [{"@type": "Country", "name": "India"},
                    {"@type": "City", "name": "Delhi"}, {"@type": "City", "name": "Mumbai"},
                    {"@type": "City", "name": "Kolkata"}, {"@type": "City", "name": "Bangalore"}],
     "provider": {"@type": "Organization", "name": "TKC Talent — The Kabir Company",
                  "url": "https://tkctalent.com/", "email": "hello@tkctalent.com"},
     "offers": {"@type": "Offer", "availability": "https://schema.org/InStock",
                "priceCurrency": "INR", "url": URL,
                "priceSpecification": {"@type": "PriceSpecification", "priceCurrency": "INR",
                                       "description": "Booking fee on request — quoted per event based on city, date, event type and performance duration."}}},
    {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tkctalent.com"},
        {"@type": "ListItem", "position": 2, "name": "Celebrity Booking India", "item": "https://tkctalent.com/celebrity-booking-india/"},
        {"@type": "ListItem", "position": 3, "name": "Haryanvi Artist Booking", "item": "https://tkctalent.com/haryanvi-artist-booking/"},
        {"@type": "ListItem", "position": 4, "name": "Book Sapna Choudhary", "item": URL}]},
]}

CARD = "rounded-2xl border border-foreground/10 bg-foreground/[0.03] p-6"
LEAD = "mt-2 text-base text-foreground/80"
H2 = "font-display text-2xl font-bold sm:text-3xl"
H3 = "font-display text-lg font-semibold"
BTN = ("inline-flex items-center gap-2 rounded-full bg-brand px-6 py-3 font-display text-sm font-bold "
       "text-brand-foreground shadow-lg transition hover:scale-[1.03] hover:opacity-90")
BTN2 = ("inline-flex items-center gap-2 rounded-full border border-foreground/20 px-6 py-3 "
        "font-display text-sm font-bold text-foreground transition hover:bg-foreground hover:text-background")


GALLERY = [
    ("sapna-choudhary-haryanvi-dance-performance", 1200, 887,
     "Sapna Choudhary Haryanvi dance performance — TKC Talent booking",
     "Sapna Choudhary mid-dance in a silver embellished lehenga on a live stage, smiling with arms open during a Haryanvi dance performance.",
     "Sapna Choudhary performing her signature Haryanvi dance set on a live stage."),
    ("sapna-choudhary-wedding-sangeet-performance", 1200, 887,
     "Sapna Choudhary wedding and sangeet performance booking",
     "Sapna Choudhary dancing with a red dupatta under red stage lights during a wedding sangeet style performance.",
     "Wedding and sangeet night performance — booked from ₹15 lakh."),
    ("sapna-choudhary-live-stage-show-crowd", 1200, 887,
     "Sapna Choudhary stage show and mela booking — TKC Talent",
     "Wide view of a Sapna Choudhary stage show at a mela ground with fire jets, dance troupe and a large audience.",
     "Open-ground stage show and mela performance with full production."),
    ("sapna-choudhary-tkc-talent-artist-poster", 800, 1066,
     "Sapna Choudhary official artist poster — TKC Talent",
     "Official TKC Talent artist poster of Sapna Choudhary in an ivory embroidered saree with the tagline Rooted in Culture, Fearless on Stage.",
     "Official TKC Talent artist profile poster for Sapna Choudhary."),
]


JSONLD["@graph"].append({
    "@type": "ImageGallery",
    "name": "Sapna Choudhary live show photos",
    "url": URL + "#photos",
    "associatedMedia": [
        {"@type": "ImageObject",
         "contentUrl": f"https://tkctalent.com/assets/haryanvi/{g[0]}-{'1200' if g[1] >= 1200 else '800'}.jpg",
         "name": g[3], "description": g[4], "caption": g[5],
         "creditText": "TKC Talent — The Kabir Company",
         "representativeOfPage": g[0].endswith("crowd")}
        for g in GALLERY]})

JSONLD["@graph"][0]["image"] = [
    f"https://tkctalent.com/assets/haryanvi/{g[0]}-{'1200' if g[1] >= 1200 else '800'}.jpg" for g in GALLERY]


def gallery_html():
    out = []
    for slug, w, h, title, alt, cap in GALLERY:
        out.append(
            f'<figure class="overflow-hidden rounded-2xl border border-foreground/10">'
            f'<picture><source type="image/webp" srcset="/assets/haryanvi/{slug}-800.webp 800w'
            + (f', /assets/haryanvi/{slug}-1200.webp 1200w' if w >= 1200 else '')
            + '" sizes="(max-width: 640px) 100vw, 460px"/>'
            f'<img src="/assets/haryanvi/{slug}-800.jpg" srcset="/assets/haryanvi/{slug}-800.jpg 800w'
            + (f', /assets/haryanvi/{slug}-1200.jpg 1200w' if w >= 1200 else '')
            + '" sizes="(max-width: 640px) 100vw, 460px" width="800" height="'
            + str(round(800 * h / w)) + '" loading="lazy" decoding="async" '
            f'title="{title}" alt="{alt}" class="h-auto w-full object-cover"/></picture>'
            f'<figcaption class="px-4 py-3 text-xs text-foreground/60">{cap}</figcaption></figure>')
    return "".join(out)


def faq_html():
    out = []
    for q, a in FAQS:
        out.append(f'<details class="{CARD} mt-3"><summary class="cursor-pointer font-display text-base font-semibold">{q}</summary>'
                   f'<p class="mt-3 text-sm text-foreground/80">{a}</p></details>')
    return "".join(out)



MAIN = f"""
<main class="mx-auto w-full max-w-5xl px-6 pb-24 pt-10 sm:px-10">
<nav aria-label="Breadcrumb" class="text-xs text-foreground/60"><a href="/" class="hover:opacity-70">Home</a> ›
<a href="/celebrity-booking-india/" class="hover:opacity-70">Celebrity Booking India</a> ›
<a href="/haryanvi-artist-booking/" class="hover:opacity-70">Haryanvi Artists</a> ›
<span>Book Sapna Choudhary</span></nav>

<section class="mt-6">
<h1 class="font-display text-3xl font-bold leading-tight sm:text-5xl">Book Sapna Choudhary for Events, Stage Shows &amp; Weddings</h1>
<p class="{LEAD} max-w-3xl">Sapna Choudhary is booked through TKC Talent for stage shows, live Haryanvi dance
performances, weddings, college fests and corporate events across India. Send your date and city to get her
show booking price and confirmed availability.</p>
<div class="mt-6 flex flex-wrap gap-3">
<a href="#book" class="{BTN}">Check Availability &amp; Price <span aria-hidden="true">→</span></a>
<a href="https://wa.me/919599599699?text=Hi%20TKC%20Talent%2C%20I%20want%20to%20book%20Sapna%20Choudhary%20for%20an%20event." target="_blank" rel="noopener" class="{BTN2}">WhatsApp +91 95995 99699</a>
<a href="mailto:hello@tkctalent.com" class="{BTN2}">Email hello@tkctalent.com</a>
</div>
<figure class="mt-8 overflow-hidden rounded-3xl border border-foreground/10">
<picture>
<source type="image/webp" srcset="/assets/haryanvi/sapna-choudhary-live-stage-show-crowd-800.webp 800w, /assets/haryanvi/sapna-choudhary-live-stage-show-crowd-1200.webp 1200w" sizes="(max-width: 768px) 100vw, 960px"/>
<img src="/assets/haryanvi/sapna-choudhary-live-stage-show-crowd-1200.jpg"
 srcset="/assets/haryanvi/sapna-choudhary-live-stage-show-crowd-800.jpg 800w, /assets/haryanvi/sapna-choudhary-live-stage-show-crowd-1200.jpg 1200w"
 sizes="(max-width: 768px) 100vw, 960px" width="1200" height="887" fetchpriority="high" decoding="async"
 title="Sapna Choudhary live stage show booking — TKC Talent"
 alt="Sapna Choudhary live stage show at night — her face on the giant LED screen with fire jets, dance troupe and a huge crowd at a mela ground."
 class="h-auto w-full object-cover"/>
</picture>
<figcaption class="px-4 py-3 text-xs text-foreground/60">Sapna Choudhary performing a live Haryanvi stage show to a mela crowd. Booking managed by TKC Talent.</figcaption>
</figure>

</section>

<section class="mt-10">
<div class="grid gap-4 sm:grid-cols-2">
<div class="{CARD}">
<h2 class="{H3}">How to book Sapna Choudhary?</h2>
<p class="mt-2 text-sm text-foreground/80">Call or WhatsApp TKC Talent on <a href="tel:+919599599699" class="font-semibold underline">+91 95995 99699</a>, email <a href="mailto:hello@tkctalent.com" class="font-semibold underline">hello@tkctalent.com</a>, or send the booking enquiry form with your event date, city and budget. TKC Talent checks her availability and sends a confirmed quote.</p>
</div>
<div class="{CARD}">
<h2 class="{H3}">Sapna Choudhary booking fees</h2>
<p class="mt-2 text-sm text-foreground/80">Indicative fees: stage show / mela <strong>₹10 lakh</strong>, club show <strong>₹10 lakh</strong>, college fest <strong>₹8–10 lakh</strong>, corporate event <strong>₹12–15 lakh</strong>, wedding / sangeet <strong>₹15 lakh</strong>. Final price depends on date, city, duration and travel.</p>
</div>
</div>
</section>

<section class="mt-14">
<h2 class="{H2}">About Sapna Choudhary</h2>
<p class="{LEAD} max-w-3xl">Sapna Choudhary is one of India's most in-demand Haryanvi stage performers — a dancer
and singer known for ragini and Haryanvi dance shows drawing very large live crowds across North India. Her
performances are built around high-energy Haryanvi dance sets with a live troupe, which is why she is booked
most often for open-ground stage shows, melas, weddings and college festivals.</p>
</section>

<section class="mt-14">
<h2 class="{H2}">Sapna Choudhary Booking Price &amp; Show Fees</h2>
<p class="{LEAD} max-w-3xl">Indicative booking fees for Sapna Choudhary by event type. TKC Talent confirms the
final written quote once your date and city are locked.</p>
<div class="mt-6 overflow-x-auto">
<table class="w-full min-w-[520px] border-collapse text-left text-sm">
<thead><tr class="border-b border-foreground/15 text-foreground/60">
<th class="py-3 pr-4 font-medium">Booking type</th><th class="py-3 pr-4 font-medium">Typical format</th><th class="py-3 font-medium">Fee (indicative)</th></tr></thead>
<tbody class="text-foreground/85">
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Stage show / mela</td><td class="py-3 pr-4">Live dance set with troupe</td><td class="py-3">&#8377;10 lakh</td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Wedding &amp; sangeet</td><td class="py-3 pr-4">Private performance</td><td class="py-3">&#8377;15 lakh</td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">College fest</td><td class="py-3 pr-4">Campus stage show</td><td class="py-3">&#8377;8&#8211;10 lakh</td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Corporate event</td><td class="py-3 pr-4">Annual day / brand activation</td><td class="py-3">&#8377;12&#8211;15 lakh</td></tr>
<tr><td class="py-3 pr-4">Club show</td><td class="py-3 pr-4">Club appearance / live set</td><td class="py-3">&#8377;10 lakh</td></tr>
</tbody></table></div>
<p class="mt-3 text-xs text-foreground/60">Indicative starting fees. Final quote depends on date, city, performance duration and technical requirements, plus 18% GST, travel and stay.</p>
<p class="mt-4 text-sm text-foreground/85">For the best deals, call or WhatsApp <a href="tel:+919599599699" class="font-semibold underline">+91 95995 99699</a> or send the enquiry form below.</p>
<h3 class="{H3} mt-8">Booking fees at a glance</h3>
<ul class="mt-2 list-disc space-y-1 pl-5 text-sm text-foreground/80">
<li><strong>Stage show / mela:</strong> &#8377;10 lakh</li>
<li><strong>Wedding &amp; sangeet:</strong> &#8377;15 lakh</li>
<li><strong>College fest:</strong> &#8377;8&#8211;10 lakh</li>
<li><strong>Corporate event:</strong> &#8377;12&#8211;15 lakh</li>
<li><strong>Club show:</strong> &#8377;10 lakh</li>
<li><strong>Add-ons:</strong> 18% GST, travel, stay and technical requirements billed over the artist fee</li></ul>
<h3 class="{H3} mt-8">What changes the price</h3>
<ul class="mt-2 list-disc space-y-1 pl-5 text-sm text-foreground/80">
<li>City and travel distance</li><li>Event type — public stage show, wedding, corporate or college fest</li>
<li>Performance duration and number of sets</li><li>Date — peak wedding and festival dates cost more</li>
<li>Sound, light and stage requirements, plus 18% GST on the artist fee</li></ul>
</section>

<section class="mt-14">
<h2 class="{H2}">Events You Can Book Her For</h2>
<p class="{LEAD} max-w-3xl">Sapna Choudhary is booked for four main event types, each with a different format and price.</p>
<div class="mt-6 grid gap-4 sm:grid-cols-2">
<div class="{CARD}"><h3 class="{H3}">Stage Shows &amp; Live Dance Performances</h3>
<p class="mt-2 text-sm text-foreground/80">Open-ground stage shows, melas and cultural nights with a full live
Haryanvi dance set. TKC Talent arranges stage, sound, light, artist security and crowd management.</p>
<a href="#book" class="mt-4 inline-block text-sm font-semibold underline">Get stage show price →</a></div>
<div class="{CARD}"><h3 class="{H3}">Weddings &amp; Private Functions</h3>
<p class="mt-2 text-sm text-foreground/80">Sangeet nights, receptions and private family celebrations with a
shorter curated set, handled under a confidentiality agreement.</p>
<a href="#book" class="mt-4 inline-block text-sm font-semibold underline">Get wedding performance quote →</a></div>
<div class="{CARD}"><h3 class="{H3}">Corporate Events &amp; College Fests</h3>
<p class="mt-2 text-sm text-foreground/80">Annual days, dealer meets, brand activations and campus festivals,
with GST-compliant invoicing and a signed contract.</p>
<a href="#book" class="mt-4 inline-block text-sm font-semibold underline">Get corporate quote →</a></div>
<div class="{CARD}"><h3 class="{H3}">Festival &amp; Government Cultural Events</h3>
<p class="mt-2 text-sm text-foreground/80">Melas, city festivals and cultural programmes, including large
public-ground shows with permissions and on-ground execution support.</p>
<a href="#book" class="mt-4 inline-block text-sm font-semibold underline">Get festival quote →</a></div>
</div>
</section>

<section class="mt-14" id="book">
<h2 class="{H2}">Sapna Choudhary Contact for Booking</h2>
<p class="{LEAD} max-w-3xl">To contact Sapna Choudhary for a booking, call or WhatsApp TKC Talent on
<a href="tel:+919599599699" class="underline">+91 95995 99699</a>, email
<a href="mailto:hello@tkctalent.com" class="underline">hello@tkctalent.com</a> or send the enquiry form below.
Every genuine booking is confirmed through a signed contract with her authorised management.</p>
<div class="mt-6 overflow-x-auto">
<table class="w-full min-w-[520px] border-collapse text-left text-sm">
<caption class="sr-only">Sapna Choudhary booking contact details via TKC Talent</caption>
<thead><tr class="border-b border-foreground/15 text-foreground/60">
<th class="py-3 pr-4 font-medium">Contact</th><th class="py-3 pr-4 font-medium">Details</th><th class="py-3 font-medium">Best for</th></tr></thead>
<tbody class="text-foreground/85">
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Phone</td><td class="py-3 pr-4"><a class="underline" href="tel:+919599599699">+91 95995 99699</a></td><td class="py-3">Same-day availability check</td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">WhatsApp</td><td class="py-3 pr-4"><a class="underline" href="https://wa.me/919599599699" target="_blank" rel="noopener">+91 95995 99699</a></td><td class="py-3">Sharing event brief and dates</td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Email</td><td class="py-3 pr-4"><a class="underline" href="mailto:hello@tkctalent.com">hello@tkctalent.com</a></td><td class="py-3">Written quotes and contracts</td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Enquiry form</td><td class="py-3 pr-4"><a class="underline" href="#book">Booking enquiry form</a></td><td class="py-3">Full brief with budget</td></tr>
<tr><td class="py-3 pr-4">Agency</td><td class="py-3 pr-4">TKC Talent — The Kabir Company, New Delhi</td><td class="py-3">Pan-India and overseas shows</td></tr>
</tbody></table></div>
<ul class="mt-5 list-disc space-y-1 pl-5 text-sm text-foreground/80">
<li>Response within 24 hours on working days; within 30 minutes on WhatsApp during office hours</li>
<li>Share event date, city, venue, audience size and budget for a faster quote</li>
<li>Booking is confirmed only after a signed contract and advance payment</li>
<li>TKC Talent does not share the artist's personal number — all contact is through the agency</li></ul>
<div class="{CARD} mt-6">
<form action="https://formsubmit.co/thekabircompany@gmail.com" method="POST" class="grid gap-4 sm:grid-cols-2">
<input type="hidden" name="_subject" value="Sapna Choudhary Booking Enquiry — TKC Talent"/>
<input type="hidden" name="_template" value="table"/>
<input type="hidden" name="_captcha" value="false"/>
<input type="hidden" name="_next" value="https://tkctalent.com/book-sapna-choudhary/?sent=1"/>
<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off"/>
<label class="text-sm">Your name<input required name="Name" maxlength="100" class="mt-1 w-full rounded-lg border border-foreground/15 bg-background px-3 py-2 text-sm" placeholder="Full name"/></label>
<label class="text-sm">Phone / WhatsApp<input required name="Phone" maxlength="20" class="mt-1 w-full rounded-lg border border-foreground/15 bg-background px-3 py-2 text-sm" placeholder="+91"/></label>
<label class="text-sm">Event date<input required type="date" name="Event date" class="mt-1 w-full rounded-lg border border-foreground/15 bg-background px-3 py-2 text-sm"/></label>
<label class="text-sm">City<input required name="City" maxlength="80" class="mt-1 w-full rounded-lg border border-foreground/15 bg-background px-3 py-2 text-sm" placeholder="Delhi NCR"/></label>
<label class="text-sm">Event type<select name="Event type" class="mt-1 w-full rounded-lg border border-foreground/15 bg-background px-3 py-2 text-sm"><option>Stage show</option><option>Wedding / sangeet</option><option>College fest</option><option>Corporate event</option><option>Festival / mela</option></select></label>
<label class="text-sm">Budget (INR)<input name="Budget" maxlength="40" class="mt-1 w-full rounded-lg border border-foreground/15 bg-background px-3 py-2 text-sm" placeholder="Approx."/></label>
<input type="hidden" name="Artist" value="Sapna Choudhary"/>
<div class="sm:col-span-2"><button type="submit" class="{BTN}">Send booking enquiry <span aria-hidden="true">→</span></button></div>
</form>
<p class="mt-4 text-xs text-foreground/50">TKC Talent team: <a class="underline" href="/admin/sapna-bookings/" rel="nofollow">log this enquiry in the booking register</a>.</p></div>
</section>

<section class="mt-14">
<h2 class="{H2}">How to Book Sapna Choudhary — Step by Step</h2>
<p class="{LEAD} max-w-3xl">Booking takes four steps and usually closes within a week.</p>
<ol class="mt-6 grid gap-4 sm:grid-cols-2">
<li class="{CARD}"><span class="text-xs font-bold text-foreground/50">Step 1</span><p class="mt-1 text-sm text-foreground/85">Send your event date, city, venue and budget to TKC Talent.</p></li>
<li class="{CARD}"><span class="text-xs font-bold text-foreground/50">Step 2</span><p class="mt-1 text-sm text-foreground/85">We check availability with her management and send a written quote.</p></li>
<li class="{CARD}"><span class="text-xs font-bold text-foreground/50">Step 3</span><p class="mt-1 text-sm text-foreground/85">Contract signed, advance paid, artist rider and travel locked.</p></li>
<li class="{CARD}"><span class="text-xs font-bold text-foreground/50">Step 4</span><p class="mt-1 text-sm text-foreground/85">On-ground coordinator manages arrival, stage, security and show day.</p></li>
</ol>
</section>

<section class="mt-14">
<h2 class="{H2}">Why Book Through TKC Talent</h2>
<p class="{LEAD} max-w-3xl">TKC Talent — The Kabir Company is a celebrity and artist booking agency working with
Bollywood actors, singers, comedians and regional stage artists since 2005.</p>
<ul class="mt-4 grid gap-3 sm:grid-cols-2 text-sm text-foreground/85">
<li class="{CARD}">Written quote, signed contract and GST-compliant invoicing</li>
<li class="{CARD}">Travel, stay, security and green-room handled end to end</li>
<li class="{CARD}">Stage, sound and light production available with the booking</li>
<li class="{CARD}">Events delivered across Delhi NCR, Haryana, Punjab, Rajasthan, UP and beyond</li>
</ul>
</section>

<section class="mt-14">
<h2 class="{H2}">Frequently Asked Questions</h2>
{faq_html()}
</section>

<section class="mt-14" id="photos">
<h2 class="{H2}">Sapna Choudhary Live Show Photos</h2>
<p class="{LEAD} max-w-3xl">Recent photographs from Sapna Choudhary's live Haryanvi dance shows and stage
performances booked through TKC Talent.</p>
<div class="mt-6 grid gap-5 sm:grid-cols-2">
{gallery_html()}
</div>
</section>


<section class="mt-14" id="cities">
<h2 class="{H2}">Book Sapna Choudhary in Delhi, Mumbai, Kolkata &amp; Bangalore</h2>
<p class="{LEAD} max-w-3xl">TKC Talent books Sapna Choudhary for shows in every major Indian city. Fees stay in
the same band; travel, stay and local production are added to the city quote.</p>
<div class="mt-6 overflow-x-auto">
<table class="w-full min-w-[560px] border-collapse text-left text-sm">
<caption class="sr-only">Sapna Choudhary booking by city</caption>
<thead><tr class="border-b border-foreground/15 text-foreground/60">
<th class="py-3 pr-4 font-medium">City</th><th class="py-3 pr-4 font-medium">Most booked for</th><th class="py-3 pr-4 font-medium">Indicative fee</th><th class="py-3 font-medium">City page</th></tr></thead>
<tbody class="text-foreground/85">
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Delhi NCR</td><td class="py-3 pr-4">Weddings, melas, college fests</td><td class="py-3 pr-4">&#8377;10&#8211;15 lakh</td><td class="py-3"><a class="underline" href="/celebrity-booking-delhi/">Celebrity booking Delhi</a></td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Mumbai</td><td class="py-3 pr-4">Brand events, club shows</td><td class="py-3 pr-4">&#8377;10&#8211;15 lakh + travel</td><td class="py-3"><a class="underline" href="/celebrity-booking-mumbai/">Celebrity booking Mumbai</a></td></tr>
<tr class="border-b border-foreground/10"><td class="py-3 pr-4">Kolkata</td><td class="py-3 pr-4">Puja pandals, cultural nights</td><td class="py-3 pr-4">&#8377;10&#8211;15 lakh + travel</td><td class="py-3"><a class="underline" href="/durga-puja-2026/">Durga Puja 2026 events</a></td></tr>
<tr><td class="py-3 pr-4">Bangalore</td><td class="py-3 pr-4">Corporate annual days, college fests</td><td class="py-3 pr-4">&#8377;10&#8211;15 lakh + travel</td><td class="py-3"><a class="underline" href="/corporate-event-management/">Corporate event management</a></td></tr>
</tbody></table></div>
<div class="mt-6 grid gap-4 sm:grid-cols-2">
<div class="{CARD}"><h3 class="{H3}">Sapna Choudhary booking in Delhi NCR</h3>
<p class="mt-2 text-sm text-foreground/80">Her home market — Delhi, Gurgaon, Noida, Faridabad and Ghaziabad
farmhouse weddings, sangeet nights and open-ground melas, with the shortest travel cost.</p></div>
<div class="{CARD}"><h3 class="{H3}">Sapna Choudhary booking in Mumbai</h3>
<p class="mt-2 text-sm text-foreground/80">Brand launches, club nights and reality-show style appearances,
with flights, hotel and local production coordinated by TKC Talent.</p></div>
<div class="{CARD}"><h3 class="{H3}">Sapna Choudhary booking in Kolkata</h3>
<p class="mt-2 text-sm text-foreground/80">Durga Puja pandal cultural nights, festival grounds and winter
stage shows, including permissions and crowd management support.</p></div>
<div class="{CARD}"><h3 class="{H3}">Sapna Choudhary booking in Bangalore</h3>
<p class="mt-2 text-sm text-foreground/80">Corporate annual days, dealer meets and campus festivals with
GST-compliant invoicing and a signed artist contract.</p></div>
</div>
<p class="mt-5 text-sm text-foreground/80">Send your city and date to <a class="underline" href="tel:+919599599699">+91 95995 99699</a> for a localised quote.</p>
</section>

<section class="mt-14">

<h2 class="{H2}">Related Booking Pages</h2>
<ul class="mt-4 grid gap-2 text-sm text-foreground/85 sm:grid-cols-2">
<li><a class="underline" href="/haryanvi-artist-booking/">Haryanvi artist booking</a></li>
<li><a class="underline" href="/singer-booking-india/">Singer booking India</a></li>
<li><a class="underline" href="/celebrity-booking-india/">Celebrity booking India</a></li>
<li><a class="underline" href="/book-shehnaaz-gill/">Book Shehnaaz Gill</a></li>
<li><a class="underline" href="/book-sonam-bajwa/">Book Sonam Bajwa</a></li>
<li><a class="underline" href="/celebrity-booking-delhi/">Celebrity booking in Delhi</a></li>
<li><a class="underline" href="/celebrity-booking-gurgaon/">Celebrity booking in Gurgaon</a></li>
<li><a class="underline" href="/contact-us/">Contact TKC Talent</a></li>
</ul>
</section>
</main>
"""

page = head(TITLE, DESC, URL, IMG, JSONLD) + HEADER + MAIN + FOOTER + TAIL + "</body></html>"
out = ROOT / "book-sapna-choudhary" / "index.html"
out.parent.mkdir(exist_ok=True)
out.write_text(page, encoding="utf-8")
print("wrote", out, len(page))

# ---------------- Haryanvi hub ----------------
HUB_URL = "https://tkctalent.com/haryanvi-artist-booking/"
HUB_TITLE = "Haryanvi Artist Booking — Stage Show Dancers &amp; Singers | TKC Talent"
HUB_DESC = ("Book Haryanvi artists for stage shows, weddings, melas and college fests. "
            "Sapna Choudhary and other Haryanvi dancers and singers booked via TKC Talent.")
HUB_LD = {"@context": "https://schema.org", "@graph": [
    {"@type": "CollectionPage", "name": "Haryanvi Artist Booking", "url": HUB_URL,
     "description": HUB_DESC.replace("&amp;", "&")},
    {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Sapna Choudhary", "url": URL}]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://tkctalent.com"},
        {"@type": "ListItem", "position": 2, "name": "Celebrity Booking India", "item": "https://tkctalent.com/celebrity-booking-india/"},
        {"@type": "ListItem", "position": 3, "name": "Haryanvi Artist Booking", "item": HUB_URL}]},
]}

HUB_MAIN = f"""
<main class="mx-auto w-full max-w-5xl px-6 pb-24 pt-10 sm:px-10">
<h1 class="font-display text-3xl font-bold leading-tight sm:text-5xl">Haryanvi Artist Booking</h1>
<p class="{LEAD} max-w-3xl">TKC Talent books Haryanvi stage artists — dancers and singers — for stage shows,
melas, weddings, college fests and corporate events across North India. Send your date and city for a quote.</p>
<div class="mt-8 grid gap-4 sm:grid-cols-2">
<a href="/book-sapna-choudhary/" class="{CARD} block transition hover:bg-foreground/[0.06]">
<h2 class="{H3}">Book Sapna Choudhary</h2>
<p class="mt-2 text-sm text-foreground/80">Haryanvi stage dancer and singer — stage shows, weddings, college
fests. Booking price on request.</p></a>
</div>
<p class="mt-8 text-sm text-foreground/70">Looking for another Haryanvi artist? Email
<a class="underline" href="mailto:hello@tkctalent.com">hello@tkctalent.com</a> with the name, date and city.</p>
</main>
"""

hub = head(HUB_TITLE, HUB_DESC, HUB_URL, IMG, HUB_LD, og_type="website") + HEADER + HUB_MAIN + FOOTER + TAIL + "</body></html>"
hub_out = ROOT / "haryanvi-artist-booking" / "index.html"
hub_out.parent.mkdir(exist_ok=True)
hub_out.write_text(hub, encoding="utf-8")
print("wrote", hub_out, len(hub))
