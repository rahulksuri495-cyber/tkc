# Clean up duplicate navigation links

Inspection of the live nav (222 links total) found three distinct duplication problems:

1. **15 comedians listed twice in the same menu** — every comedian (Kapil Sharma, Zakir Khan, Samay Raina, etc.) appears twice inside `Celebrity Booking India > Comedian Booking India`. Pure duplication, no reason to keep both.
2. **Durga Puja 2026 appears twice** — once as a top-level nav item and once inside the Celebrity Booking India dropdown ("Durga Puja 2026 — CR Park").
3. **Trending 2026 / Top Indian Celebrities point to the same URL** — the top-level "Trending 2026" item and a child item inside its own dropdown both link to `/top-indian-celebrities/`.
4. **27 singers appear in two different menus** — under `Celebrity Booking India > Singers & Performers` and again under `Trending 2026 > Singer Fees 2026`.

## What will change

- Remove the duplicated comedian block so each comedian shows once.
- Keep "Durga Puja 2026" only as the top-level nav item; drop the duplicate from the Celebrity Booking dropdown.
- Keep "Trending 2026" as the top-level link and remove the redundant self-link inside its dropdown.
- Leave the singer cross-listing as-is by default (two genuinely different menus: booking vs. fees) unless you want them de-duplicated too — see the question below.
- Add a final safety pass that removes any anchor whose URL already exists under the same parent menu, so future injections can't re-introduce same-menu duplicates.
- Apply all of it to desktop nav, mobile drawer, and tablet drawer.

## Technical notes

All nav items are injected by `assets/nav-enhance-v3.js`. Fixes go there:
- Make the comedian/actor/actress/singer injectors idempotent by keying on an existing `a[href="..."]` inside the target `<ul>` before appending (the comedian path currently misses this guard).
- Drop the Durga Puja insert in `ensureCelebrityBookingMenu()`, keep `ensureDurgaTopLevel()`.
- Filter the self-referencing `/top-indian-celebrities/` child out of the Trending dropdown.
- Add a `dedupeNav()` run at the end of the init sequence and after each MutationObserver pass, scoped per `<ul>`.

Verification: re-run the Playwright nav audit and confirm zero same-parent duplicates.
