# Add 13 individual Bollywood actress booking pages

## Goal
Create 13 new static, prerendered pages under `/book-{name}` for Deepika Padukone, Priyanka Chopra, Anushka Sharma, Kriti Sanon, Kiara Advani, Kangana Ranaut, Taapsee Pannu, Vaani Kapoor, Nora Fatehi, Tamannaah Bhatia, Esha Gupta, Jacqueline Fernandez, Sunny Leone — matching the visual style and SEO depth of the existing `/book-alia-bhatt` and `/book-kareena-kapoor` pages, and wire them into the "Bollywood Actresses" dropdown across the whole site.

## URLs (added to dropdown in this order, after Alia and Kareena)

3. `/book-deepika-padukone` — Deepika Padukone
4. `/book-priyanka-chopra` — Priyanka Chopra
5. `/book-anushka-sharma` — Anushka Sharma
6. `/book-kriti-sanon` — Kriti Sanon
7. `/book-kiara-advani` — Kiara Advani
8. `/book-kangana-ranaut` — Kangana Ranaut
9. `/book-taapsee-pannu` — Taapsee Pannu
10. `/book-vaani-kapoor` — Vaani Kapoor
11. `/book-nora-fatehi` — Nora Fatehi
12. `/book-tamannaah-bhatia` — Tamannaah Bhatia
13. `/book-esha-gupta` — Esha Gupta
14. `/book-jacqueline-fernandez` — Jacqueline Fernandez
15. `/book-sunny-leone` — Sunny Leone

## What gets built

### 1. 13 new static HTML pages
Each page cloned from `book-kareena-kapoor/index.html` as the template (same header, footer, fonts Inter + Space Grotesk, shared CSS bundle). **No 3D carousel** on any of these pages — just static content blocks.

Per-page unique content:
- **Hero**: actress name, tagline, signature films/roles
- **Fee block**: indicative per-event range (consistent with `/bollywood-celebrity-charges`)
- **Why book {name}**: 4–6 USPs (audience pull, brand fit, event types she's known for)
- **Event types**: corporate, brand launches, weddings/sangeets, award shows, private events
- **3-step booking process** (same template)
- **8-question FAQ** (fees, advance notice, customisation, international, weddings, NDA, rider, what TKC manages)
- **Strong CTA section** (sticky/dark) with WhatsApp + call + email
- **SEO head**: unique `<title>`, meta description, canonical, OG, Twitter cards
- **JSON-LD**: `Person` + `FAQPage` + `BreadcrumbList` schemas for AEO / LLM-rankability

### 2. Hero images
Reuse existing `/actresses/{slug}.png` images already in the repo (verified present for all 13). Wire each into hero, OG image, and `twitter:image`. No new image generation needed.

Image map:
- deepika-padukone.png, priyanka-chopra.png, anushka-sharma.png, kirti-sanan.png (Kriti), kiara-adwani.png (Kiara), kangana-ranaut.png, taapsee-pannu.png, vaani-kapoor.png, nora-fatehi.png, tamanna-bhatia.png, esha-gupta.png, jacqueline-fern-ndez.png, sunny-leone.png

### 3. Dropdown nav update (sitewide)
The Bollywood Actresses sub-menu lives in `assets/Footer-Cl7ZiBEX.js` AND is baked into every prerendered `index.html` (~15 files). Mechanical search-and-replace insert into the `children:[{label:"Book Alia Bhatt",...},{label:"Book Kareena Kapoor Khan",...}]` array to append the 13 new entries in order.

### 4. Sitemap
Append 13 `<url>` entries to `sitemap.xml`.

### 5. llms.txt
Append 13 `Book {Name}` lines under Pages section.

## Technical notes

- Static prerendered export — no `src/` rebuild. All edits direct HTML/asset edits.
- Fonts and CSS load from already-referenced bundles — new pages inherit styling automatically.
- React hydration script is intentionally omitted on individual-artist pages (same approach as Sunil Grover / SRK / Alia / Kareena) to avoid the React #418 hydration error on mobile.
- No 3D carousel JS injected — these pages are pure HTML + CSS.

## Out of scope

- No new images (use existing `/actresses/*.png`).
- No edits to the parent `/bollywood-actress-booking` page content beyond the dropdown nav.
- No rebuild of React source.
