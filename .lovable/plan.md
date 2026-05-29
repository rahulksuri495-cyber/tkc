I verified the issue in the mobile preview: the drawer opens, but the “Celebrity Booking India” dropdown has no submenu content rendered underneath it. The click is happening, but because hydration was disabled earlier, React never creates the conditional submenu DOM.

Plan:

1. Repair the static mobile navigation
   - Add a robust vanilla JavaScript fallback for the mobile drawer.
   - Ensure dropdown buttons actually create/show their submenu links, not only toggle `aria-expanded`.
   - Keep nested groups visible and usable on mobile, including Bollywood Actors, Bollywood Actresses, Comedians, Singers & Performers, DJs, Pan-India Celebrities, and Influencers.

2. Apply the same fix across all affected static pages
   - Update every page where hydration was disabled and the mobile nav depends on static JS.
   - Do not alter page content, SEO data, or desktop navigation styling.

3. Verify before delivery
   - Test at mobile width around 320px.
   - Confirm: hamburger opens, “Celebrity Booking India” expands, submenu links appear, nested category links are reachable, and links close/navigate correctly.
   - Spot-check at least home, celebrity booking, singer booking, and a category page before marking done.