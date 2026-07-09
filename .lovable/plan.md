## Goal

Add a dedicated "IITEO Legacy" section to the homepage that summarizes the `/iiteo/` page and shows the dignitary/leader photos already used there. This strengthens E-E-A-T by surfacing real, verifiable event heritage (Presidents, PM, CMs, Governors hosted by TKC / The Kabir Company) directly on the homepage, with a clear internal link to the full `/iiteo/` article.

The current homepage already has a text-only `tkc-legacy` band (injected by `assets/tkc-homepage-blocks.js`). We will keep it and add a NEW, richer IITEO Legacy section *below* it — different purpose (people + proof), different visuals, so no duplication.

## What to build

A new client-side injector script `assets/tkc-iiteo-legacy.js` that:

1. Runs only on `/` (homepage).
2. Injects a `<section id="tkc-iiteo-legacy">` right after the existing `#tkc-legacy` block (or, if not found, before the roster/pricing area — same anchor logic already used in `tkc-homepage-blocks.js`).
3. Adds its own scoped CSS (dark premium band, gold accent to match brand — matches the existing legacy band styling language).

### Section content

- **Eyebrow:** "IITEO × The Kabir Company — Two-Decade Event Legacy"
- **H2:** "From India's biggest trade fairs to the country's most-booked stage."
- **Lead paragraphs (~120–140 words, SEO-tuned around: IITEO, India International Trade Event Organisation, The Kabir Company, event management Delhi NCR, exhibitions, concerts, celebrity bookings)** — condensed summary of `/iiteo/`:
  - Origins in India's trade-fair and exhibition ecosystem via IITEO (India International Trade Event Organisation).
  - Evolution into concerts, corporate events, luxury weddings, celebrity bookings.
  - HQ New Delhi; pan-India delivery; hosted by top political and cultural leadership across two decades.
- **Proof gallery — 10 dignitaries** (already in `assets/iiteo-leaders/`):
  - Pranab Mukherjee — 13th President of India
  - Pratibha Patil — 12th President of India
  - Narendra Modi — Prime Minister of India
  - Rajnath Singh — Defence Minister
  - Sheila Dikshit — CM Delhi
  - Bhupinder Singh Hooda — CM Haryana
  - Akhilesh Yadav — CM Uttar Pradesh
  - Omar Abdullah — CM Jammu & Kashmir
  - Arjun Munda — CM Jharkhand
  - Ramesh Pokhriyal — CM Uttarakhand
  - (+ Jagannath Pahadia, Syed Ahmed — Governors, as overflow)
  - Rendered as a responsive grid of portrait cards: circular/rounded photo, name, role caption. Descriptive `alt` text for SEO/a11y (e.g. "Shri Pranab Mukherjee, 13th President of India, hosted by The Kabir Company / TKC Talent leadership").
  - `loading="lazy"` and `decoding="async"` on every `<img>`.
- **Stat row (3 KPIs):** "20+ Yrs Legacy", "10+ Heads of State & CMs Hosted", "500+ Talents · Pan-India".
- **CTA row:** primary button "Read the full IITEO legacy →" linking to `/iiteo/` (internal link — real SEO juice), secondary WhatsApp/contact link.

### Styling

- Dark premium background to visually separate from the light cream `tkc-legacy` band above it.
- Gold accent (#c9a84c) on eyebrow and H2 highlight — brand-consistent.
- Portrait cards: rounded top, subtle gold hairline border, name in Space Grotesk bold + role caption in Inter.
- Reveal-on-scroll animation (reuse the same `.tkc-reveal` IntersectionObserver pattern from `tkc-homepage-blocks.js`).
- Respects `prefers-reduced-motion`.

### SEO / structured data

Append a JSON-LD `<script type="application/ld+json">` inside the injected section with an `ItemList` of the dignitaries as `Person` entries (name + jobTitle) — extends `/iiteo/`'s existing schema onto the homepage. Does not conflict with the existing homepage JSON-LD graph.

### Wiring

- Add `<script src="/assets/tkc-iiteo-legacy.js" defer></script>` to the homepage shell. The React app hydrates the DOM; the existing `tkc-homepage-blocks.js` and `tkc-clients-scroller.js` are already loaded the same way — locate where they're registered (likely `_shell.html` or `index.html`) and add the new one alongside them.

## Files touched

- **Create** `assets/tkc-iiteo-legacy.js` — the injector (styles + DOM + reveal + JSON-LD).
- **Edit** `_shell.html` (or wherever the sibling `tkc-homepage-blocks.js` / `tkc-clients-scroller.js` are registered) — add one `<script defer>` tag.

No changes to the React bundle, no changes to `/iiteo/` itself, no new image assets (reuse `assets/iiteo-leaders/*`).

## Verification

Playwright headless: load `http://localhost:8080/`, screenshot the new section, confirm all 10 leader images load (status 200), confirm the internal `/iiteo/` link is present, confirm the section does not appear on non-home routes.
