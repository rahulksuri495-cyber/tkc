## Blog launch — `/blog/` magazine-grid hub + 4 SEO articles

Brand-consistent blog matching the site's existing aesthetic (Inter + Space Grotesk, dark `#0a0a0a` foreground, brand accent, newsroom-style typography). Same static HTML pattern as `/book-{name}/` and `/iiteo/`, so it ranks like the rest of the site and is easy to extend.

### URL structure
```text
/blog/                                                    → magazine index
/blog/event-management-company-india/                     → article 1
/blog/celebrity-booking-agency-india/                     → article 2
/blog/artist-booking-agency-india/                        → article 3
/blog/corporate-event-management-india/                   → article 4
```

### Keyword targeting (one primary per article)
1. **Event management company in India** (~22k/mo) — pillar guide, links to `/ourservice/` + city pages
2. **Celebrity booking agency India** — transactional, links to `/celebrity-booking-india/` + actor pages
3. **Artist booking agency India** — links to `/singer-booking-india/`, `/comedian-booking-india/`, `/celebrity-dj-booking/`
4. **Corporate event management India** — links to `/corporate-event-management/` + Delhi/Mumbai/Gurgaon city pages

Each article: 1,400–1,700 words, H1/H2/H3 hierarchy, TL;DR + Key Details block, 6-Q FAQ, long-tail variants woven in (e.g. "how to book Bollywood celebrity for corporate event", "event management company in Faridabad / Delhi NCR").

### Design — magazine grid (matches `/newsroom` editorial style, no new colors/fonts)
```text
/blog/ layout
┌─────────────────────────────────────────────────────────┐
│  ★ Insights                                              │
│  The TKC                                                 │
│  Journal.                  ← big display H1, brand accent│
│  Field notes on celebrity booking & event craft         │
├─────────────────────────────────────────────────────────┤
│  FEATURED                                                │
│  ┌──────────────────────┐  ┌──────────────────────┐    │
│  │  Hero image          │  │ CATEGORY · 8 MIN     │    │
│  │  (16:9)              │  │ Event Management     │    │
│  │                      │  │ Company in India:    │    │
│  │                      │  │ 2026 Buyer's Guide   │    │
│  │                      │  │ Excerpt 2 lines…     │    │
│  │                      │  │ Read story →         │    │
│  └──────────────────────┘  └──────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│  ALL ARTICLES        [All] [Booking] [Events] [Guides]  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│  │ img 4:3 │  │ img 4:3 │  │ img 4:3 │                  │
│  │ chip    │  │ chip    │  │ chip    │                  │
│  │ Title   │  │ Title   │  │ Title   │                  │
│  │ excerpt │  │ excerpt │  │ excerpt │                  │
│  └─────────┘  └─────────┘  └─────────┘                  │
└─────────────────────────────────────────────────────────┘
```
Visual rules: existing nav + footer untouched; brand accent only on hover/eyebrow; numbered section labels ("(01)") like newsroom; category chips use 1px border + uppercase tracking; no purple gradients, no new fonts, no new colors.

### Article page template
- Eyebrow (category) → H1 → meta row (date · reading time · author "TKC Editorial") → 16:9 hero image
- TL;DR box + Key Details bullets (matches existing service/location pages)
- Body H2/H3 sections, pull-quotes, in-content internal links with keyword anchors
- 6-question FAQ (FAQPage JSON-LD)
- "Related reading" card row → 3 related articles + relevant service/booking page
- Sticky bottom CTA → `/contact-us/` with phone + WhatsApp

### SEO/AEO/GEO per article
- Unique title (<60c) + meta description (<160c) with primary keyword
- Canonical, `og:image` (custom 1200×630 generated per article), `twitter:card`
- JSON-LD: `Article` + `BreadcrumbList` + `FAQPage` + `Organization` ref + `SpeakableSpecification`
- City variants ("Delhi NCR", "Faridabad", "Mumbai", "Gurgaon") woven naturally
- Added to `sitemap.xml`, `llms-full.txt`, and city `llms-{city}.txt` where relevant
- `og/` per-article cards via existing `scripts/generate-og-images.py` pipeline

### Navigation
Add "Blog" as a top-level nav item placed before "Contact" across the 30+ core HTML pages using the same Python patcher used for previous nav updates. Bump SW to `tkc-v24`.

### Review-before-publish flow
Per your "show me before publishing" requirement, I will build everything **set to `<meta name="robots" content="noindex, follow">`** and **excluded from `sitemap.xml`** on first pass. You'll get:
1. Preview URLs for `/blog/` and all 4 articles
2. A short visual review note
Once you approve, I flip robots to `index, follow`, add entries to `sitemap.xml` + `llms.txt`, regenerate OG images, ping IndexNow, and bump the SW.

### Build steps (in order)
1. Generate 4 hero images (1600×900) + 4 OG cards (1200×630) into `assets/blog/`
2. Create `/blog/index.html` (magazine grid, featured + 3 cards, category filter via simple anchor chips)
3. Create 4 article HTML files with full template above
4. Run `scripts/seo-monitor.py` to validate JSON-LD/canonical/OG on all 5 new pages
5. Patch navigation across core pages to add "Blog"
6. Hold publish (noindex) → await your approval
7. On approval: flip robots, update sitemap + llms files, IndexNow ping, SW bump
