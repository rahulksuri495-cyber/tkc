# Add "Book Sunil Grover" page

## Goal
Create a new prerendered static page at `/book-sunil-grover` that matches the visual style, fonts, and SEO depth of the existing `/book-shah-rukh-khan` and `/book-alia-bhatt` pages, and wire it into the Comedian dropdown so it's reachable from `/comedian-booking-india`.

## What gets built

1. **New page** — `book-sunil-grover/index.html`
   - Cloned from `book-shah-rukh-khan/index.html` (same header, footer, fonts Inter + Space Grotesk, shared `styles-B3eDpzGa.css`, main JS bundle).
   - Sunil-specific content:
     - Hero with name, tagline, signature roles (Gutthi, Dr. Mashoor Gulati, Sunflower, Tandav, United Kacche).
     - Fee block: ~₹35–50 L per show (corporate / private) — consistent with the ₹35 L figure already on the comedian page.
     - "Why book Sunil Grover" — versatility, character comedy, brand-safe, family-friendly, wedding/sangeet favourite.
     - Event types: corporate annual days, brand launches, weddings & sangeets, award shows, HNI private events.
     - 3-step booking process (same template as SRK).
     - 8-question FAQ block (fees, advance notice, customisation, international, weddings, NDA, rider, what TKC manages).
     - Sticky / dark CTA section with WhatsApp + call + email.
   - SEO: unique title, meta description, canonical, OG, Twitter cards, JSON-LD `Person` + `FAQPage` + `BreadcrumbList` + `HowTo`.

2. **Images** — copy the 7 uploaded photos into `assets/` as `sunil-1.webp … sunil-7.webp` (convert the .jpg uploads to .webp via `cwebp` so file sizes match the rest of the site). Used for the hero, gallery strip, and OG image.

3. **Sitemap** — add `<url><loc>https://tkctalent.com/book-sunil-grover</loc>…` to `sitemap.xml`.

4. **llms.txt** — add a `Book Sunil Grover` line under Pages.

5. **Comedian dropdown nav** — the nav is baked into every prerendered HTML page. The comedian sub-menu currently has no individual-artist links. Adding "Sunil Grover" to the dropdown across the whole site means a mechanical search-and-replace insert into the comedian `<ul>` of each existing `index.html` (~14 files).

## Technical notes

- This working tree is a prerendered static export — no `src/` or `package.json`. All edits are direct HTML/asset edits, same workflow used for the recent `sitemap.xml`, `.htaccess`, and `llms.txt` changes.
- Fonts load from Google Fonts and `styles-B3eDpzGa.css` — both already referenced on every page, so the new page inherits styling automatically.
- OG image: `assets/sunil-1.webp` (Jim Beam / floral-shirt portrait).
- After files land, redeploy to Hostinger via the existing FTP / zip-and-extract flow.

## Out of scope

- No rebuild of the React/TanStack source (not present in this workspace).
- No route-tree edits — purely static additions.
