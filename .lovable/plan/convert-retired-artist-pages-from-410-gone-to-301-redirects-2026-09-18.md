# Convert retired artist pages from 410 Gone to 301 redirects

Switch the five retired booking pages from 410 Gone to permanent 301 redirects so their rankings and link equity pass to the closest relevant page instead of being lost.

## Why not the homepage

Redirecting everything to the homepage is treated by Google as a "soft 404" — the content doesn't match what the searcher wanted, so Google drops the URL and you lose the traffic anyway. Redirects only preserve SEO value when the target page is a close topical match.

## What happens

1. **Update `.htaccess`** — replace the five 410 rules with 301 redirects to the nearest matching hub:

   | Old URL | Redirects to |
   |---|---|
   | /book-arijit-singh/ | /singer-booking-india/ |
   | /book-badshah/ | /singer-booking-india/ |
   | /book-sunidhi-chauhan/ | /singer-booking-india/ (already 301 — unchanged) |
   | /book-asees-kaur/ | /singer-booking-india/ (already 301 — unchanged) |
   | /book-kapil-sharma/ | /comedian-booking-india/ |

2. **Strengthen the target pages** — singer-booking-india and comedian-booking-india already list the remaining bookable artists, so redirected visitors land on a useful, on-intent page (this is what makes Google accept the redirect instead of soft-404ing it).

3. **Validate** — re-run verify-canonical-urls.py and the artist-schema check, confirm the .htaccess rules are syntactically correct.

4. **Publish** — the 301s take effect on tkctalent.com with the next publish.

## What to expect

- Google will transfer most of the retired pages' ranking signals to the hub pages over a few weeks.
- Hub pages may start ranking for "arijit singh booking" style queries — weaker than the dedicated page did, but far better than a 410 or a homepage redirect.
- The artist names stay removed from the site content (as you asked); only the URLs redirect.

## After you approve

I'll apply the .htaccess changes, validate, and the redirects go live at your next publish.
