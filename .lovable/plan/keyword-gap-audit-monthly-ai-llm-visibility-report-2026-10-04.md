# Keyword Gap Audit + Monthly AI/LLM Visibility Report

## Part 1 — Keyword and page audit (one-off report)
Make one list of every high-volume target keyword and the page meant to rank for it. Build it from:
- **Google Search Console** (last 3 months): impressions, clicks, average position and the page that actually shows in Google for each search.
- **Semrush** (India market): monthly search volume, difficulty, and which sites hold the top 10 today.
- **On-page check** of each target page: title, H1, a direct answer at the top, FAQ, schema, internal links, word count, and whether two of our own pages compete for the same keyword.

Starting keyword groups, grown from GSC and Semrush suggestions:
- Event management: "best event management company in delhi ncr", "event management company delhi", "event planners delhi", "event management gurgaon", "best event management company in india", "corporate event management".
- Celebrity booking: "book celebrity", "celebrity booking india", "celebrity booking agency", "hire bollywood celebrity", "celebrity management company india", "bollywood celebrity charges".
- Artist booking: "singer booking india", "comedian booking", "celebrity dj booking", "haryanvi artist booking", plus "<artist> fees/price/booking" for the top artist pages.
- Seasonal: Durga Puja stalls and sponsorship terms.

Output: `/admin/keyword-audit/` (private) and a downloadable spreadsheet. Each row shows keyword, volume, current position, target page, a status (ranking / page 2 / not ranking / wrong page ranking / no page), and the fixes listed in priority order. Gaps such as a missing dedicated "Delhi NCR" page get flagged as new pages to build.

## Part 2 — Monthly AI search and LLM visibility tracking
What can and can't be measured:
- **Google AI Mode / AI Overviews:** Search Console mixes these into normal web results and does not report them separately. We'll track the closest available signals: monthly impressions and positions for question-style searches.
- **ChatGPT, Perplexity, Gemini, Claude:** each month, ask these engines a fixed set of about 40 buyer questions (for example "best event management company in Delhi NCR", "how to book a celebrity in India"). Record whether TKC is mentioned, its position in the answer, whether tkctalent.com is cited, and which competitors appear.
- **Meta AI:** there is no public way to query it automatically. Meta AI answers will be a manual monthly check entered into the same report.
- **AI referral visits:** visits arriving from chatgpt.com, perplexity.ai, gemini, copilot and meta.ai, if site analytics can capture them.

Output: `/admin/ai-visibility/` dashboard with month-by-month trend charts (mention rate per engine, citations, share against competitors), stored in a monthly history file.

## Part 3 — Optimization (after you review the audit)
Fix the pages marked high priority first: answer-first intros, keyword-matched titles and H1s, FAQ and schema, internal links from strong pages, merging pages that compete with each other, and updating llms.txt files. Then build any missing pages.

## Technical details
- The GSC data script extends `scripts/fetch-gsc-priority.py` to fetch data by query and page.
- The AI probe script uses Lovable AI models (Gemini/GPT) with web grounding where possible. Perplexity needs your own Perplexity API key. A GitHub Action runs it on the 1st of each month and commits `admin/ai-visibility/history.jsonl`.
- AI-engine results are sample-based and can vary from run to run. The report will say so.
