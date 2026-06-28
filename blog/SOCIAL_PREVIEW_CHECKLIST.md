# Social Preview Re-Scrape Checklist

Run this after every deployment that touches `/blog/`, `/assets/blog/`,
or any page's OG/Twitter metadata. Crawlers cache previews aggressively
— without a forced re-scrape, shared links keep showing the old image
and title for days.

## 0. Pre-flight (local, before deploy)

- [ ] `bun run verify:blog-og` exits 0 (CI also enforces this)
- [ ] If it complains about a missing image, run `bun run fix:blog-og`
      to swap in the default fallback `/assets/blog/og-default.jpg`,
      then commit and redeploy.
- [ ] Bump the service worker version in `sw.js` so returning users
      pick up new images.

## 1. URLs to re-scrape

- https://tkctalent.com/blog/
- https://tkctalent.com/blog/event-management-company-india/
- https://tkctalent.com/blog/celebrity-booking-agency-india/
- https://tkctalent.com/blog/artist-booking-agency-india/
- https://tkctalent.com/blog/corporate-event-management-india/

## 2. Facebook (also powers Instagram, WhatsApp, Messenger previews)

1. Open https://developers.facebook.com/tools/debug/
2. Paste each URL above.
3. Click **Scrape Again** (run twice if the first pass shows stale data).
4. Confirm: og:title, og:description, og:image (1200×630), og:url match
   the deployed page. No "Inferred Property" warnings on og:image.

## 3. LinkedIn

1. Open https://www.linkedin.com/post-inspector/
2. Paste each URL.
3. Click **Inspect**. LinkedIn caches for ~7 days — re-inspecting forces a refresh.
4. Confirm the card image, title, and description render correctly.

## 4. X / Twitter

X retired the public Card Validator UI. Use either:

- **Quick check:** paste the URL into a Draft post in the X composer
  (do not publish) — the card preview that appears is the freshly
  fetched one.
- **Cache bust if wrong:** append `?v=YYYYMMDD` to the URL once, share
  that, then share the clean URL after.
- Confirm: `twitter:card=summary_large_image`, title, description, and
  image all render.

## 5. WhatsApp / iMessage / Slack / Telegram

These pull from Facebook's OG cache (WhatsApp, iMessage) or their own
(Slack, Telegram). After step 2 succeeds, paste each URL into:

- [ ] A WhatsApp chat to yourself
- [ ] A Slack DM to yourself (`/remove preview` then re-paste if stale)
- [ ] A Telegram "Saved Messages" chat

## 6. Done criteria

- [ ] All 5 blog URLs show the correct branded card on Facebook + LinkedIn
- [ ] X composer preview shows the correct large-image card
- [ ] No console errors on any blog page (`F12` → Console)
- [ ] `bun run verify:blog-og` still exits 0

If any preview is wrong after a re-scrape, the og:image file is most
likely 404 or wrong dimensions — re-run `python3 scripts/verify-blog-og.py`
to confirm and `bun run fix:blog-og` to fall back to the default card.