# Add 3 singers to Singer Booking India page

Add Altaf Raja, Sara Gurpal, and Sunanda Sharma to the singer roster with prices and photos.

## Singer entries

| Name | Tier | Fee | Events |
|---|---|---|---|
| Altaf Raja | Mid Tier | ₹5 L – ₹7 L | Weddings, sangeet nights, retro nights |
| Sara Gurpal | Emerging | ₹5 L | Sangeet, Punjabi weddings, corporate |
| Sunanda Sharma | Mid Tier | On Demand | Weddings, sangeet, Punjabi events |

## Steps

1. **Source photos via Google Images** — fetch one clean portrait per artist (Wikipedia/press photo preferred for licensing). Save as `singers/altaf-raja.jpeg`, `singers/sara-gurpal.jpeg`, `singers/sunanda-sharma.jpeg`.
2. **Update roster data** in bundled `assets/main-CQYOkFRR.js` — append 3 objects to the singers roster array (`{name, tier, fee, events, slug, image}`) matching existing schema.
3. **Update static `singer-booking-india/index.html`** — append 3 roster cards mirroring existing Jasmine Sandlas / Neha Bhasin card markup, and append 3 entries to the `BreadcrumbList` JSON-LD (positions 33–35).
4. **Update `sitemap.xml`** to include the new `/book-altaf-raja`, `/book-sara-gurpal`, `/book-sunanda-sharma` URLs (no detail HTML pages will be created — same as other singers in roster which only link to slugs).
5. **Verify** in the preview at `/singer-booking-india` that the 3 new cards render with images, names, tier badges, and fees.

## Notes
- No individual `book-*` detail pages exist for any singer in this roster, so we won't create new ones — slugs link to placeholder paths matching the existing pattern.
- If a clean Google image cannot be fetched, fallback to an AI-generated placeholder portrait.
