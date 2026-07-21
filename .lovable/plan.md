## Goal

Stop the spam-call funnel without killing genuine call leads. Spammers scrape "management contact" strings (FAQ answers, JSON-LD, agent files). We replace the phone number **only in those management/manager contexts** with `info@thekabircompany.com`. Every existing CTA (header, hero, sticky mobile call button, footer, WhatsApp) keeps the phone number exactly as it is.

## Scope — what changes vs what stays

**Changes to email only (`info@thekabircompany.com`):**
- Artist page FAQ answers that respond to "[Name] management" and "[Name] contact details" (137 pages, added recently).
- Any "Management Contact" / "Manager Details" / "Official Management" text blocks on artist and hub pages.
- JSON-LD on artist pages — remove `telephone` from LocalBusiness/Organization/contactPoint under management/manager context; add `email`. Keep `telephone` in the site-wide LocalBusiness where it exists as the business phone (footer/homepage).
- Agent-facing files: `.well-known/agent-card.json`, `.well-known/mcp/server-card.json`, `.well-known/agent-skills/index.json`, `.well-known/agent-skills/request-quote.md`, `.well-known/api-catalog`, `llms.txt` — swap management-contact phone references for the email.

**Stays untouched (CTA / conversion surface):**
- Header phone number and click-to-call.
- Hero "Call Now" buttons.
- Sticky mobile call button.
- Footer contact line.
- WhatsApp deep links.
- Google Business Profile.
- Homepage / service page CTAs.

## Approach

1. Grep the repo for the phone number in three passes:
   - Inside artist FAQ answer strings for "management" / "contact details" questions.
   - Inside JSON-LD blocks (`"telephone"`) that sit in a management/manager/contactPoint node.
   - Inside `.well-known/**` and `llms.txt`.
   Each pass produces a review list before edits.
2. For each match in scope, replace the phone value with `info@thekabircompany.com` (JSON-LD gets `"email"` key, prose gets "Email the management team at …").
3. Leave every other occurrence of the number alone — verified by a diff pass that lists the CTA files we intentionally skipped (header, footer, hero, sticky bar, WhatsApp).
4. Update the FAQ JSON-LD `acceptedAnswer` strings to match the new visible text so schema stays consistent.
5. After edits: run the existing artist schema CI check to confirm no schema regressions.

## Technical notes

- FAQ answer replacement is a scripted pass over the 137 artist pages, matched on the question text ("… management", "… contact details") so we don't touch other CTAs on the same page.
- JSON-LD edits target nodes whose `@type` is `ContactPoint` with `contactType` in {`management`, `customer service` when adjacent to management copy}, or a top-level `Organization`/`Person` `telephone` used as management contact. Site-wide `LocalBusiness.telephone` in the footer/global schema is left alone.
- No changes to routing, forms, or backend. This is a content + JSON-LD pass only.

## Out of scope

- Number obfuscation / click-to-reveal on CTAs.
- Swapping to a new phone number.
- Form honeypot / rate-limit changes.
- Any GBP changes.

We can layer those on later if spam persists after this pass.
