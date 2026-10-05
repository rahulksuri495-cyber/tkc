#!/usr/bin/env python3
"""Priority keyword fix (Oct 2026). Safe to re-run.

1. Builds/rewrites the event pages from scripts/priority_pages_content.py
2. Targeted title/H1/answer edits on celebrity + corporate pages (one page per keyword)
3. Sitewide static footer link block + menu label fix
4. Homepage + services link sections
"""
import re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from priority_pages_lib import build, ROOT  # noqa: E402
from priority_pages_content import PAGES  # noqa: E402

MARK = "<!-- tkc-priority-links -->"


def rd(p):
    return (ROOT / p).read_text(encoding="utf-8")


def wr(p, s):
    (ROOT / p).write_text(s, encoding="utf-8")


def set_meta(s, title=None, desc=None):
    if title:
        s = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", s, count=1)
        s = re.sub(r'(<meta (?:property="og:title"|name="twitter:title") content=")[^"]*"', lambda m: m.group(1) + title + '"', s)
    if desc:
        s = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*"', lambda m: m.group(1) + desc + '"', s)
    return s


def insert_after_first(s, pattern, block, key):
    if key in s:
        return s
    m = re.search(pattern, s, re.S)
    if not m:
        raise SystemExit(f"pattern not found for {key}")
    return s[:m.end()] + block + s[m.end():]


def box(key, html):
    return (f'<div data-fix="{key}" class="mt-6 max-w-3xl rounded-2xl border border-foreground/15 bg-foreground/[0.03] p-5 text-left text-sm leading-relaxed text-foreground/85" data-speakable="answer">{html}</div>')


# ------------------------------------------------------------------ 1. pages
for slug, d in PAGES.items():
    build(slug, d)
    print("built", slug)

# ------------------------------------------------------------------ 2. targeted edits
# celebrity-booking-india: main page for "celebrity booking" / "book celebrity"
p = "celebrity-booking-india/index.html"; s = rd(p)
s = set_meta(s, "Celebrity Booking India — Book a Celebrity for Events | TKC Talent",
             "Celebrity booking in India: book a Bollywood celebrity, singer or comedian for your event. 2026 fee ranges, how booking works and an itemised quote from TKC Talent.")
s = s.replace('Celebrity Booking <span class="italic text-foreground/60">in India.</span></h1>',
              'Celebrity Booking in India — <span class="italic text-foreground/60">Book a Celebrity for Your Event</span></h1>')
s = insert_after_first(s, r'Book a Celebrity for Your Event</span></h1><p[^>]*>.*?</p>', box("cbi-answer",
    '<strong>How celebrity booking works in India:</strong> share your event date, city, audience and budget; TKC Talent (The Kabir Company, New Delhi, since 2005) checks the artist\'s availability with their management, sends an itemised quote, signs the contract and manages travel, riders and the show day. '
    'Celebrity fees in India range from about ₹5 lakh to ₹14 crore depending on the artist. For weddings see <a class="underline" href="/book-celebrity-for-wedding/">book a celebrity for your wedding</a>; for tours across several cities see <a class="underline" href="/pan-india-celebrity-booking/">multi-city celebrity tours</a>.'),
    'data-fix="cbi-answer"')
wr(p, s); print("edited", p)

# pan-india: refocus on multi-city tours, hand "celebrity booking" back to the main page
p = "pan-india-celebrity-booking/index.html"; s = rd(p)
s = set_meta(s, "Multi-City Celebrity Tours &amp; Appearances in India | TKC",
             "Plan multi-city celebrity tours and appearances across Delhi NCR, Mumbai, Jaipur, Udaipur, Goa and abroad, with travel, riders and logistics managed by TKC Talent.")
s = re.sub(r'Pan-India stars,(<!-- -->)? <span class="italic text-foreground/60">directly booked\.</span></h1>',
           'Multi-city celebrity tours,<!-- --> <span class="italic text-foreground/60">managed end to end.</span></h1>', s)
s = insert_after_first(s, r'managed end to end\.</span></h1><p[^>]*>.*?</p>', box("pan-handoff",
    'This page covers <strong>multi-city tours and appearances</strong>: one artist across several cities, or events in more than one state. '
    'To book a celebrity for a single event, see <a class="underline" href="/celebrity-booking-india/">celebrity booking in India</a>.'),
    'data-fix="pan-handoff"')
wr(p, s); print("edited", p)

# book-celebrity-for-wedding: the only wedding celebrity page
p = "book-celebrity-for-wedding/index.html"; s = rd(p)
s = set_meta(s, "Book Celebrity for Wedding in India 2026 | Fees &amp; Booking | TKC",
             "Book a celebrity for your wedding: Bollywood singers, actors, comedians and DJs for sangeet and reception. 2026 fee ranges, lead times and how booking works.")
s = re.sub(r'(<h1[^>]*>)\s*Book Celebrities for Weddings in India\s*</h1>', r'\1Book a Celebrity for Your Wedding in India</h1>', s, count=1)
s = s.replace('href="tel:+919599599699"', 'href="/contact-us/"')
s = insert_after_first(s, r'Book a Celebrity for Your Wedding in India</h1>\s*<p[^>]*>.*?</p>', box("wed-answer",
    '<strong>Quick answer:</strong> to book a celebrity for a wedding in India, share the date, city, function (sangeet, reception or mehendi) and budget with TKC Talent. '
    'We confirm availability with the artist\'s management, send an itemised quote, sign the contract and manage travel, sound, riders and on-day coordination. '
    'Book 90–120 days ahead, or 6+ months for October–February weddings. Planning the whole wedding? See our <a class="underline" href="/wedding-planner-delhi/">wedding planner in Delhi</a>.'),
    'data-fix="wed-answer"')
wr(p, s); print("edited", p)

# celebrity-booking-delhi: remove wedding targeting, own "book celebrity for event"
p = "celebrity-booking-delhi/index.html"; s = rd(p)
s = set_meta(s, "Celebrity Booking in Delhi 2026 — Hire Stars for Events | TKC",
             "Book Bollywood celebrities for corporate events, brand launches and private events in Delhi NCR. TKC Talent, Delhi-based for 20+ years, with 2026 fee ranges.")
s = s.replace("Hire Bollywood Stars for Weddings, Corporate Events &amp; Brand Launches in Delhi NCR",
              "Hire Bollywood Stars for Corporate Events, Brand Launches &amp; Private Events in Delhi NCR")
s = s.replace("Hire Bollywood Stars for Weddings, Corporate Events & Brand Launches in Delhi NCR",
              "Hire Bollywood Stars for Corporate Events, Brand Launches & Private Events in Delhi NCR")
s = s.replace("How do I book a celebrity for a wedding in Delhi?", "How do I book a celebrity for an event in Delhi?")
s = s.replace(">Luxury Weddings Delhi<", ">Weddings (see wedding page)<")
s = s.replace("Luxury wedding celebrity booking Delhi", "Book a celebrity for your wedding")
s = insert_after_first(s, r'Private Events in Delhi NCR</h1>\s*<p[^>]*>.*?</p>', box("delhi-event-answer",
    '<strong>How to hire a celebrity for an event in Delhi:</strong> (1) send the date, venue, audience and budget; (2) get an availability check and itemised quote; '
    '(3) sign the contract and pay the advance; (4) we manage travel, riders, security and show-day coordination. '
    'For weddings, see <a class="underline" href="/book-celebrity-for-wedding/">book a celebrity for your wedding</a>. For full event production, see <a class="underline" href="/event-management-delhi/">event management in Delhi NCR</a>.'),
    'data-fix="delhi-event-answer"')
wr(p, s); print("edited", p)

# bollywood-celebrity-booking: clear H1, no wedding targeting
p = "bollywood-celebrity-booking/index.html"; s = rd(p)
s = set_meta(s, "Hire Bollywood Celebrities for Events | Actors &amp; Stars | TKC",
             "Hire Bollywood celebrities for corporate events, brand campaigns and private events. Actor fee ranges for 2026 and an itemised quote from TKC Talent.")
s = re.sub(r'Bollywood Celebrity(<!-- -->)? <span class="italic text-foreground/60">booking, fully managed\.</span></h1>',
           'Hire Bollywood Celebrities<!-- --> <span class="italic text-foreground/60">for Events</span></h1>', s)
s = insert_after_first(s, r'for Events</span></h1><p[^>]*>.*?</p>', box("bolly-handoff",
    'Booking a star for a wedding? See <a class="underline" href="/book-celebrity-for-wedding/">book a celebrity for your wedding</a>. '
    'For all artist types and fees, see <a class="underline" href="/celebrity-booking-india/">celebrity booking in India</a>.'),
    'data-fix="bolly-handoff"')
wr(p, s); print("edited", p)

# corporate-event-management: main page for "corporate event management company"
p = "corporate-event-management/index.html"; s = rd(p)
s = set_meta(s, "Corporate Event Management Company in India &amp; Delhi NCR | TKC",
             "Corporate event management company since 2005: annual days, award nights, dealer meets, conferences and launches across India and Delhi NCR, with celebrity booking in-house.")
s = insert_after_first(s, r'<h1[^>]*>Corporate Event Management Company.*?</h1>\s*<p[^>]*>.*?</p>', box("corp-answer",
    '<strong>Quick answer:</strong> TKC Talent (The Kabir Company) is a <strong>corporate event management company</strong> based in New Delhi since 2005. '
    'It plans and runs annual days, award nights, dealer meets, conferences, offsites and product launches across India, with production, permits and celebrity booking handled in-house. '
    'Typical budgets: ₹3 lakh for boutique events to ₹2 crore+ for large dealer meets. Read the <a class="underline" href="/blog/corporate-event-management-india/">corporate event cost and planning guide</a>.'),
    'data-fix="corp-answer"')
wr(p, s); print("edited", p)

# blog corporate guide: supporting guide, links to the service page
p = "blog/corporate-event-management-india/index.html"; s = rd(p)
old_h1 = "Corporate Event Management Company in India: Costs, Services &amp; Planning Guide 2026"
new_h1 = "Corporate Event Management in India: Costs &amp; Planning Guide 2026"
s = s.replace(old_h1, new_h1).replace(old_h1.replace("&amp;", "&"), new_h1.replace("&amp;", "&"))
s = set_meta(s, "Corporate Event Management Guide 2026: Costs &amp; Planning | TKC",
             "Guide to corporate event management in India: costs, planning timelines, venues and what to ask an agency. Updated for 2026 by TKC Talent.")
s = insert_after_first(s, re.escape(new_h1) + r"</h1>", box("corp-guide-link",
    'Looking to hire a team? See our <a class="underline" href="/corporate-event-management/">corporate event management company</a> page for services and quotes.'),
    'data-fix="corp-guide-link"')
wr(p, s); print("edited", p)

# blog top-50 guide: link to the service hub
p = "blog/event-management-company-india/index.html"; s = rd(p)
s = insert_after_first(s, r"Top 50 Guide</h1>", box("emc-guide-link",
    'Need an agency now? See TKC Talent\'s <a class="underline" href="/event-management-company/">event management company</a> services, or the city pages for '
    '<a class="underline" href="/event-management-delhi/">Delhi NCR</a> and <a class="underline" href="/event-management-gurgaon/">Gurgaon</a>.'),
    'data-fix="emc-guide-link"')
wr(p, s); print("edited", p)

# ------------------------------------------------------------------ 3. sitewide footer block + menu label
FOOT = (MARK + '<div class="mt-10 border-t border-foreground/10 pt-6 text-sm"><p class="mb-3 text-xs uppercase tracking-[0.25em] text-foreground/50">Event management &amp; bookings</p>'
        '<ul class="flex flex-wrap gap-x-5 gap-y-2 text-foreground/80">'
        + "".join(f'<li><a href="{u}" class="hover:opacity-70">{t}</a></li>' for t, u in [
            ("Event Management Company", "/event-management-company/"),
            ("Event Management Delhi NCR", "/event-management-delhi/"),
            ("Event Planners in Delhi", "/event-planners-delhi/"),
            ("Event Management Gurgaon", "/event-management-gurgaon/"),
            ("Wedding Planner Delhi", "/wedding-planner-delhi/"),
            ("Corporate Event Management", "/corporate-event-management/"),
            ("Celebrity Booking India", "/celebrity-booking-india/"),
            ("Book Celebrity for Wedding", "/book-celebrity-for-wedding/")])
        + "</ul></div>")
n = 0
for f in ROOT.rglob("*.html"):
    rp = f.relative_to(ROOT).as_posix()
    if rp.startswith(("node_modules/", "admin/", "_templates/", "public/")) or rp in ("404.html", "offline.html", "_shell.html"):
        continue
    s = f.read_text(encoding="utf-8")
    o = s
    s = s.replace(">Pan-India Celebrities</a>", ">Multi-City Celebrity Tours</a>")
    if MARK in s:
        s = re.sub(re.escape(MARK) + r'<div class="mt-10 border-t.*?</ul></div>', lambda m: FOOT, s, count=1, flags=re.S)
    elif "</footer>" in s:
        i = s.rfind("</footer>")
        s = s[:i] + FOOT + s[i:]
    if s != o:
        f.write_text(s, encoding="utf-8"); n += 1
print("footer/menu updated in", n, "pages")

# ------------------------------------------------------------------ 4. homepage + services sections
SECTION = ('<section data-fix="home-events" class="px-6 py-12 sm:px-10"><div class="mx-auto max-w-7xl rounded-3xl border border-foreground/10 bg-foreground/[0.03] p-8 sm:p-10">'
           '<h2 class="font-display text-2xl font-bold sm:text-3xl">Event management company in Delhi NCR and across India</h2>'
           '<p class="mt-4 max-w-3xl text-foreground/70">Besides celebrity booking, TKC Talent plans and produces complete events. Start with our '
           '<a href="/event-management-company/" class="text-amber-300 underline underline-offset-4">event management company</a> services, or go straight to '
           '<a href="/event-management-delhi/" class="text-amber-300 underline underline-offset-4">event management in Delhi NCR</a>, '
           '<a href="/event-planners-delhi/" class="text-amber-300 underline underline-offset-4">event planners in Delhi</a>, '
           '<a href="/event-management-gurgaon/" class="text-amber-300 underline underline-offset-4">event management in Gurgaon</a>, '
           '<a href="/corporate-event-management/" class="text-amber-300 underline underline-offset-4">corporate event management</a>, '
           '<a href="/wedding-planner-delhi/" class="text-amber-300 underline underline-offset-4">wedding planner in Delhi</a> and '
           '<a href="/book-celebrity-for-wedding/" class="text-amber-300 underline underline-offset-4">celebrity booking for weddings</a>.</p></div></section>')
for p in ["index.html", "ourservice/index.html"]:
    s = rd(p)
    if 'data-fix="home-events"' not in s:
        i = s.rfind("</footer>") if p == "index.html" else s.find("<footer")
        s = s[:i] + SECTION + s[i:]
        wr(p, s); print("section added", p)
print("done")
