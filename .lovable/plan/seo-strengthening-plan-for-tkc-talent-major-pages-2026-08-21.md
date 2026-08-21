# SEO Strengthening Plan for TKC Talent Major Pages

## Current State Snapshot
- **Semrush India**: 189 organic keywords, ~1,729/mo estimated traffic, Authority Score 9.
- **Top pages**: 137 individual `book-*` artist pages drive most traffic.
- **Top keywords**: artist-name + "fees/concert fees/contact number" queries (e.g., Arijit Singh concert fees, Kapil Sharma show ticket price).
- **Critical gap**: Competitor `bookmysinger.com` ranks for 1,463 keywords and ~21,605/mo traffic with Authority 31. It wins on artist-name branded searches and topical authority, not just booking-intent keywords.
- **On-page SEO**: already strong (passing SEO monitor), but CTR, authority, and hub coverage are the bottlenecks.
- **Spam risk**: many high-impression queries are "contact number / WhatsApp number" — these attract spam calls, not enquiries.

## Strategic Goal
Shift from "artist booking page SEO" to **topical authority in the Indian celebrity booking ecosystem** — artist fees, wedding entertainment, corporate events, brand endorsements, and city-specific booking guides — while improving conversion from existing rankings.

## Phase 1: Conversion & CTR Quick Wins (Week 1)
Target the pages already ranking (positions 4–14) for high-intent keywords and move them up 2–5 positions.

1. **Rewrite title tags and meta descriptions** across the 25 highest-traffic `book-*` pages to front-load the exact keyword and include a CTA or value proposition.
   - Pattern: `Artist Name Booking Fees, Price & Event Availability 2026 | TKC Talent`
   - Add urgency signals: "Verified 2026 fees", "Pan-India bookings", "Quote in 24 hrs".
2. **Improve SERP features**:
   - Ensure every major page has a compelling, unique `og:image` with the artist's face and the TKC brand lockup.
   - Add FAQ schema to the 25 top-ranking pages where missing (e.g., "What is Arijit Singh's concert fee?", "How to book X for a wedding?").
3. **Reduce spam-prone ranking leakage**:
   - De-optimize or reframe pages ranking for "phone number / WhatsApp number" queries so they rank for "booking fees / event price" instead. Add a note that contact details are shared after a brief is submitted.
4. **Strengthen internal linking** from the homepage and hub pages to these 25 priority artist pages using exact-match or near-match anchor text.

## Phase 2: Hub Page Architecture & Content Expansion (Weeks 2–4)
Build category and intent hubs that pass authority to the 137 artist pages and capture broader search demand.

1. **Create / strengthen existing hubs** (each targeting 1,000+ words + FAQ + Breadcrumb + internal links):
   - `/book-singer-for-wedding/` — Wedding singer booking guide + fees by city.
   - `/book-bollywood-actor-for-event/` — Actor appearance fees for corporate/brand events.
   - `/celebrity-host-for-corporate-event/` — Emcee/MC options (Kapil Sharma, Samay Raina, etc.).
   - `/book-comedian-for-event/` — Stand-up/comedy night packages.
   - `/book-influencer-for-brand-collaboration/` — Influencer endorsement and event appearance fees.
   - `/book-celebrity-for-wedding/` — Master landing page for wedding entertainment.
2. **City intent hubs** (expand beyond Delhi/Gurgaon):
   - `/celebrity-booking-mumbai/`, `/celebrity-booking-bangalore/`, `/celebrity-booking-hyderabad/`, `/celebrity-booking-chennai/`, `/celebrity-booking-pune/`, `/celebrity-booking-jaipur/` (already exists).
   - Each hub links to relevant artists and includes a city-specific "event planners" section.
3. **Fee comparison / listicle hubs** (already partially built, strengthen):
   - `/top-indian-celebrities/`
   - `/celebrity-singer-fees-2026/`
   - `/celebrity-brand-endorsement-fees-2026/`
   - Add sortable/filterable tables, 2026 fee bands, and update dates for freshness.
4. **Add a `/artists/` directory** (A–Z listing) and a `/events/` case-study hub with real, anonymized event budgets and photos to build E-E-A-T.

## Phase 3: Authority & E-E-A-T (Ongoing)
Your Authority Score is 9. The biggest lever is not more on-page tricks — it's trust signals and backlinks.

1. **Real client case studies** on the site:
   - Create 10–15 detailed event case studies (wedding, corporate, concert, brand launch) with photos, budgets, cities, and outcomes.
   - Link each case study to the artist pages and hub pages involved.
2. **Media mentions & press page**:
   - Publish a `/press/` or `/newsroom/` page listing all media coverage, IITEO dignitary photos, and event photos.
   - Add `NewsArticle` schema to press items and link back to relevant service pages.
3. **Expert content**:
   - Add a dedicated "About TKC" / "Our Team" / "Founders" page with founder bios, photos, and `Person` schema.
   - Publish an annual "India Celebrity Booking Report 2026" as a downloadable asset to attract backlinks and social shares.
4. **Backlink strategy** (white-hat):
   - Convert existing brand mentions on `thekabircompany.com` and other partner sites to follow backlinks.
   - Guest posts on event-industry blogs, wedding planning blogs, and corporate hospitality sites.
   - Get listed in event-management and celebrity-booking directories (weddingz, wedmegood, eventfaqs, etc.).
   - Pitch event photos/IITEO coverage to local Delhi/NCR news sites.

## Phase 4: Technical & UX Improvements (Week 2)
1. **Page speed**:
   - Lazy-load all images below the fold on hub pages and gallery pages.
   - Convert hero images to WebP/AVIF with proper `srcset`.
   - Defer non-critical JS.
2. **Schema audit**:
   - Add `BreadcrumbList` schema to all 137 artist pages and every hub/city page.
   - Add `AggregateRating` / `Review` schema to hub pages using real client testimonials.
   - Validate with `scripts/verify-artist-schema.py` after changes.
3. **Sitemap & indexing**:
   - Keep `sitemap.xml` updated with new hubs and accurate `lastmod` dates.
   - Add an `image-sitemap.xml` for artist/hub images.
   - Re-submit to GSC after each content batch.
4. **Canonical & hreflang**:
   - Ensure every page has a self-referencing canonical.
   - Consider adding `hreflang="en-IN"` sitewide.

## Phase 5: Local & GBP SEO (Week 3)
1. **Google Business Profile**:
   - Post weekly updates using the GBP content pack already created.
   - Add service categories, products, and Q&As for "Celebrity booking", "Wedding entertainment", "Corporate event management".
   - Actively collect reviews with a link in the post-event follow-up email.
2. **Location pages**:
   - Strengthen existing Delhi/Gurgaon pages with unique photos, local client logos, and testimonials.
   - Add `/event-management-noida/`, `/event-management-faridabad/`, `/event-management-ghaziabad/` to complete Delhi NCR coverage.

## Phase 6: Measurement & Iteration (Ongoing)
1. **Dashboards**:
   - Extend `/admin/gsc-priority/` to track new hubs and 25 priority artist pages.
   - Add a "keyword position tracker" using the GSC connector for the 50 target keywords.
2. **A/B test title tags**:
   - Test "Fees" vs "Price" vs "Booking Charges" in titles for CTR improvements.
3. **Monthly SEO sprints**:
   - Month 1: CTR + 5 new hubs.
   - Month 2: Case studies + backlink outreach.
   - Month 3: City expansion + schema enhancements.

## Expected Outcomes
- **Short term**: 10–20% CTR lift on existing rankings, reducing spam-call keywords and increasing enquiry-intent traffic.
- **Medium term**: 50–100% organic traffic growth within 3–6 months through hub pages and long-tail keyword coverage.
- **Long term**: Authority Score increase to 20+ as case studies, press, and backlinks compound, enabling competitive ranking for high-volume artist-name queries.

## Next Step Options
1. **Implement Phase 1 first** (CTR rewrites + 25 priority page schema) — fastest ROI.
2. **Implement Phase 2 first** (build 5–6 new hub pages) — biggest long-term traffic growth.
3. **Start with a full SEO audit + technical fix pass** (Phase 4) before content expansion.

Which phase should we begin with, or do you want me to combine Phase 1 + Phase 2 into a single build?