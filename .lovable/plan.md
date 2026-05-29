## Goal
Publish 9 new press articles (May 19, 2026 — "Leading Entrepreneurs, Businesses and Thought Leaders of India 2026") to the Newsroom page, inserted as **cards #7–#15** (after the existing first 6, before the rest). Same card style as existing entries; on desktop and mobile.

## 9 Articles to insert (in this order)

| # | Publisher | URL | Logo file (uploaded) |
|---|---|---|---|
| 7 | Google News | https://news.google.com/search?q=Leading+Entrepreneurs+Businesses+and+Thought+Leaders+of+India+2026&hl=en-IN&gl=IN&ceid=IN:en | google_news.png |
| 8 | MSN | https://www.msn.com/en-in/news/India/leading-entrepreneurs-businesses-and-thought-leaders-of-india-2026/ar-AA23yvgE | msn.png |
| 9 | Yahoo News | https://search.yahoo.com/search?p=Leading+Entrepreneurs+Businesses+and+Thought+Leaders+of+India+2026 | yahoo_news.png |
| 10 | Business Standard | https://www.business-standard.com/content/press-releases-ani/leading-entrepreneurs-businesses-and-thought-leaders-of-india-2026-125051900672_1.html | business_standard.png |
| 11 | ANI News | https://www.aninews.in/news/business/business/leading-entrepreneurs-businesses-and-thought-leaders-of-india-202620260519181636/ | ani.png |
| 12 | News18 | https://www.news18.com/business/leading-entrepreneurs-businesses-and-thought-leaders-of-india-2026-10100214.html | news_18.png |
| 13 | Tribune India | https://www.tribuneindia.com/news/business/leading-entrepreneurs-businesses-and-thought-leaders-of-india-2026/amp/?utm=relatedarticles | the_tribune.png |
| 14 | Lokmat Times | https://www.lokmattimes.com/business/leading-entrepreneurs-businesses-and-thought-leaders-of-india-2026/ | Lokmat_Times.png |
| 15 | World News Network | https://www.worldnewsnetwork.net/news/leading-entrepreneurs-businesses-and-thought-leaders-of-india-202620260519181636/ | world_news_network.png |

Each card uses publisher name, the shared headline "Leading Entrepreneurs, Businesses and Thought Leaders of India 2026", date badge "May 19, 2026", a short E-E-A-T body summary referencing TKC's inclusion, the logo, and the URL (target=_blank, rel=noopener nofollow).

## Files changed

1. **Copy 9 logos** → `assets/` (hashed-name not needed; use simple names like `assets/google-news.png`, etc.). Reuse existing simple references.
2. **`assets/main-CQYOkFRR.js`** (bundled press array `I2`):
   - Add 9 logo URL constants (e.g. `Gn1="/assets/google-news.png"`).
   - Insert 9 new object entries into `I2` immediately after the 6th entry (byte offset already located at position 2642 inside the array). Existing 26 entries become 35.
3. **`newsroom/index.html`** (prerendered SSR markup):
   - Locate the 6th `<li>` press card and inject 9 sibling `<li>` cards with identical class structure / Tailwind classes before the 7th.
   - Update the `(NN)` count badge in section header from `(26)` to `(35)`.
   - Update the "Press features" stat from `26+` to `35+` in the hero stats.
4. **`assets/newsroom-BPng2Qdx.js`** — only update the hero stats string `26+` → `35+`. **Do NOT touch** the `Publications` (18-logo) grid — that's a curated logo set, not the article list.

## Out of scope
- Publishers grid (curated 18 outlets) — not changing.
- No new react route, no sitemap change (newsroom URL unchanged).
- No design/layout change — cards inherit existing card style exactly.

## Verification
- Grep for the 9 publisher names in both `main-CQYOkFRR.js` and `newsroom/index.html` after edit.
- Confirm `(35)` badge and `35+` hero stat render.
- Visually confirm cards #7–#15 in preview (desktop + mobile viewport).