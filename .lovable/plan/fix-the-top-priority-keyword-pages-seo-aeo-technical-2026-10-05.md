# Fix the top-priority keyword pages (SEO + AEO + technical)

## What the checks found
The earlier audit got some things wrong. A fresh check of the site shows:

- **Two pages already exist that the audit missed.** `/event-management-delhi/` is already titled "Event Management Company in Delhi NCR", but only 11 pages link to it. `/corporate-event-management/` already targets "corporate event management company" and has 143 links. The audit pointed to the blog versions of both instead.
- **The city event pages are near-copies of each other.** `/event-planners-delhi/`, `/event-management-delhi/`, `/event-management-gurgaon/` and `/event-management-mumbai/` share 47–57% identical text. Google tends to show only one page from a group like that, or none. This is the most likely reason for zero impressions.
- **Pages compete for the same searches.** Two Delhi pages target the same searches. Two corporate pages do too (the service page and the blog). `/celebrity-booking-delhi/` uses the word "wedding" 18 times, so it competes with `/book-celebrity-for-wedding/`, which only 3 pages link to. `/pan-india-celebrity-booking/` competes with `/celebrity-booking-india/`.
- **Things that are already fine:** all pages return 200 on the live site, can be indexed, have correct canonicals and appear in the sitemap. They also already have FAQ, LocalBusiness and Breadcrumb schema. More schema or more meta tweaks won't help. The fixes needed are unique content, one page per keyword, and internal links.

## One page per keyword

| Keyword | Main page | Action |
|---|---|---|
| event management company (6,600) | **new** `/event-management-company/` | Build a real service page. The Top 50 blog stays as a guide and links to it |
| event planners in delhi (2,400) | `/event-planners-delhi/` | Rewrite with planning-focused content that doesn't repeat the other pages |
| event management company in delhi / delhi ncr / best ... (1,300) | `/event-management-delhi/` (existing) | Rewrite the content. Add a "Best event management company in Delhi NCR" answer and a comparison. Raise links from 11 pages to sitewide |
| book celebrity for wedding | `/book-celebrity-for-wedding/` | Make it the only wedding page. Remove wedding targeting from the Delhi and Bollywood celebrity pages. Link to it sitewide |
| wedding planner delhi (1,900) | **new** `/wedding-planner-delhi/` | Build it with an answer-first intro, services and process, and celebrity add-ons |
| event management company in gurgaon (880) | `/event-management-gurgaon/` | Rewrite with Gurgaon-specific content and link it from the Gurgaon Durga Puja stalls |
| corporate event management company (880) | `/corporate-event-management/` (existing) | Make it the main page. Retitle the blog as a costs and planning guide that links to it |
| celebrity booking / book celebrity (140 each) | `/celebrity-booking-india/` | New title and H1 ("Celebrity Booking in India — Book a Celebrity for Your Event"), an answer-first intro and a fee table. Refocus the pan-India page on multi-city tours, linking back with the anchor "celebrity booking" |

## Applied to every page above
- **Answer-first intro (for AI answers):** 40–60 words that directly answer the search, then a short facts list covering who, where, starting price, contact and lead time.
- **Unique content:** each page gets its own sections, FAQs and examples, so no two pages share large blocks of text. Target overlap is under 25%.
- **Title and H1** start with the exact keyword. Each page gets its own meta description.
- **Internal links:**
  - add an "Event Management" group to the main menu and footer
  - add links from the homepage and the services page
  - link the city pages to each other
  - add links from artist pages to the wedding and celebrity-booking pages
- **Content rules:** only real photos and data you've already given us. No invented prices; where no price is known, the page says "quote on request". No "exclusive" or "authorized" wording, and email or enquiry form only (no phone numbers), as before.

## Technical
- Update the sitemap dates, add the 2 new pages, and update the llms.txt files.
- Notify search engines through the existing IndexNow ping.
- Run the existing canonical, schema and image checks, then a duplicate-text check.
- Run a browser check of every changed page.
- Give you a short list of URLs for "Request indexing" in Search Console. Only you can click that button.

## Honest expectations
These fixes remove the problems we can see on the site itself. A 6,600-search keyword like "event management company" is also decided by reviews, backlinks and your Google Business Profile, which are outside the site. Results usually show in Search Console 2–6 weeks after you publish and request indexing.

## Technical details
- Static HTML pages live in folders such as `/<slug>/index.html`. The shared menu and footer come from `_templates/header.html` and `_templates/footer.html`, which existing scripts copy to every page.
- A new script, `scripts/priority-keyword-fix.py`, will apply the link blocks and de-targeting across pages and can be safely run more than once.
- The duplicate-text check reuses the word-sequence comparison from this investigation, with a limit of 0.25 between priority pages.
- Update `roadmap.md` to close "Part 3 optimization" for these keywords.
