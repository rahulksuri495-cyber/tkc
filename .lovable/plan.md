
## Goal
Produce a single downloadable SEO & schema validation report for `/iiteo/` that confirms metadata is stable across refreshes and recommends high-volume keywords around event organisers / top event companies.

## What the report will contain

1. **Metadata validation (static HTML inspection)**
   - Title (length, keyword presence), meta description (length), canonical, hreflang
   - OpenGraph + Twitter card tags (presence, image dimensions, alt text)
   - Robots / geo tags
   - H1 uniqueness, heading hierarchy
   - Verdict: PASS/WARN/FAIL per check

2. **Refresh stability check**
   - Confirm all SEO tags are baked into static HTML (not JS-injected), so they render identically on initial load, hard refresh, and back/forward navigation. Diff two fetches of `/iiteo/` to prove byte-identical `<head>`.

3. **JSON-LD schema validation**
   - Parse the inline `application/ld+json` block
   - Validate each @graph node (Article, Organization/LocalBusiness, FAQPage, BreadcrumbList) against schema.org required fields
   - Flag missing recommended properties (e.g. Article.datePublished, Article.image)

4. **Keyword research via Semrush (India database)**
   - Run `semrush--keyword_research` and `semrush--keyword_compare` on seeds: "event management company", "top event companies in india", "event organisers delhi", "exhibition organisers india", "celebrity event management", "best event planners delhi ncr", "corporate event company india"
   - For each: monthly volume, difficulty, CPC, intent band, recommendation (target / support / skip)
   - Map top candidates to where they should appear on `/iiteo/` (title, H2, body, FAQ)

5. **Recommendations**
   - Concrete edits to title/description/H2s/FAQ to capture the chosen high-volume terms without disrupting the existing IITEO legacy narrative
   - Any missing schema fields to add

## Deliverable
`/mnt/documents/iiteo-seo-report.html` (styled, printable) + a `<presentation-artifact>` link in the chat reply. No code changes to the site in this pass — recommendations only. If you want, I can apply the recommended on-page edits as a follow-up.
