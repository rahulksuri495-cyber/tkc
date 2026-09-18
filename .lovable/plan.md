# Take down Arijit Singh, Badshah & Kapil Sharma booking pages

Take down three artist pages — `/book-arijit-singh/`, `/book-badshah/`, `/book-kapil-sharma/` — following the same proven process used for Sunidhi Chauhan and Asees Kaur, so the URLs return **410 Gone** and every mention is removed from the site.

## What happens

1. **410 Gone rules in `.htaccess`** — add three permanent rules (same style as Sunidhi/Asees):
   ```
   RewriteRule ^book-arijit-singh/?$  - [R=410,L]
   RewriteRule ^book-badshah/?$       - [R=410,L]
   RewriteRule ^book-kapil-sharma/?$  - [R=410,L]
   ```
2. **Delete the page folders and images** — `book-arijit-singh/`, `book-badshah/`, `book-kapil-sharma/`; their gallery images and `assets/og/actor-*.jpg` cards.
3. **Remove navigation links** — from `assets/nav-enhance-v3.js`, `_templates/header.html`, footer bundle, and the global artist search data (`assets/main-*.js`, `index-*.js`).
4. **Remove from hub and listing pages** — singer hub (`singer-booking-india`), comedian hub, bollywood-celebrity-booking, bollywood-celebrity-charges fee table, bollywood-actress-booking, event hubs, and blog posts that link to or mention these artists as bookable.
5. **Remove cross-links on other artist pages** — strip "related artist" links to these three pages from remaining book-* pages (e.g. book-darshan-raval, book-armaan-malik, book-aakash-gupta, etc.).
6. **Update data files** — remove from `.well-known/agent-skills/artist-catalog.json`, `llms-full.txt` (URL + FAQ blocks), `sitemap.xml`, `image-sitemap.xml`, admin diagnostic reports, and `scripts/generate-hub-pages.py` / `admin/gsc-priority/data.json` so they are never regenerated.
7. **Validate** — re-run `verify-canonical-urls.py`, `verify-artist-schema.py`, and confirm zero remaining references (except the `.htaccess` 410 rules). Confirm sitemap still parses.

## Traffic note

These are high-traffic pages (Arijit Singh especially is a Tier 1 keyword page). Taking them down means losing that organic traffic permanently — Google will drop the URLs within days of the 410. The equivalent for Sunidhi/Asees was low-traffic; these three are among your top pages. If the intent is only to stop bookings (not lose rankings), an alternative is keeping the pages live with a "not available for booking" notice — say the word and I'll switch approach.

## After you approve

I'll apply the changes, run all verification scripts, and the 410s take effect on tkctalent.com at your next publish.
