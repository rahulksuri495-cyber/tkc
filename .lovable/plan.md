# robots.txt — verify against pasted spec (plan)

## Result of comparison (already done)

Current `robots.txt` already matches the spec's section 1 except one item:

- **Missing: `LinkedInBot` block** — the spec includes it (LinkedIn sharing; section 22 also asks for a "LinkedIn sharing implementation" report item).
- Everything else is already present and correct:
  - `Content-Signal: search=yes, ai-input=yes, ai-train=no` (same values; kept at top of file — position is irrelevant to crawlers)
  - All AI/answer-engine agents: GPTBot, OAI-SearchBot, ChatGPT-User, PerplexityBot, Google-Extended, Google-CloudVertexBot, ClaudeBot, Claude-Web, anthropic-ai, Applebot, Applebot-Extended, Bingbot, msnbot, BingPreview, adidxbot, Meta-ExternalAgent, Meta-ExternalFetcher, Amazonbot, DuckAssistBot, YouBot, MistralAI-User, cohere-ai, cohere-training-data-crawler, Diffbot, Bytespider, PetalBot
  - `Disallow: /404.html`, `Disallow: /admin/`
  - Both `Sitemap:` lines
  - No unofficial GrokBot / xAI crawler (spec forbids it)

## Change to make

1. `robots.txt` — add one block under the Bing/Microsoft group, keeping all other lines byte-identical:

   ```txt
   # LinkedIn (share/link preview crawling; used by section-5 OG checks)
   User-agent: LinkedInBot
   Allow: /
   ```

2. Verification:
   - Run `python3 scripts/seo-monitor.py` — its robots audit must still pass (adding an agent cannot trip the baseline; only *removals* of required agents or a Content-Signal change fail).
   - Confirm `admin/seo-monitor/robots-baseline.json` stays unchanged (same content_signal, same required agents).

## Out of scope (already satisfied or separate topics)

- Open Graph / Twitter tags (spec section 5): already implemented on priority pages; unchanged here.
- Sitemaps, canonicals, JSON-LD, llms.txt (spec sections 2–14): already built in prior work; the user's request this time is robots.txt only.
