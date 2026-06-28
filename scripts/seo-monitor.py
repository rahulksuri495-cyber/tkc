#!/usr/bin/env python3
"""SEO compliance monitor + dashboard generator.

Walks every public index.html under the project root and audits:
  * JSON-LD blocks parse cleanly (json.loads)
  * <link rel="canonical"> exists and self-references tkctalent.com
  * <meta name="robots"> present
  * og:image present, points at tkctalent.com, declares 1200x630 dimensions
  * page appears in sitemap.xml

Outputs:
  - admin/seo-monitor/report.json   (machine-readable, used by CI alerts)
  - admin/seo-monitor/index.html    (human dashboard, noindex)

Exit code is non-zero when any failing check is found. The GitHub Action in
`.github/workflows/seo-monitor.yml` runs this on every push and on a daily
schedule and opens an issue when the script fails — that's the automated
alert channel for JSON-LD / canonical / robots regressions.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://tkctalent.com"
SKIP_PARTS = {"dist", "node_modules", ".git", "admin"}

MAJOR_PREFIXES = ("book-", "celebrity-booking-", "corporate-event-management",
                  "ourservice", "celebrity-booking-india", "contact-us",
                  "comedian-booking-india", "celebrity-dj-booking",
                  "influencer-booking-india", "pan-india-celebrity-booking",
                  "iiteo")

# Robots.txt AI-signal invariants. If any of these regress (Content-Signal
# flips ai-input back to "no", or major AI crawlers get removed) the monitor
# fails and the GitHub Action opens an alert issue.
REQUIRED_ROBOTS_TOKENS = ["ai-input=yes", "search=yes"]
REQUIRED_AI_AGENTS = [
    "GPTBot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot",
    "Google-Extended", "ClaudeBot", "Applebot-Extended",
    "Google-CloudVertexBot", "Meta-ExternalAgent",
]
CITY_SLUGS = ["delhi", "mumbai", "gurgaon", "noida", "jaipur", "goa"]

class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.canonical = ""
        self.robots = ""
        self.og_image = ""
        self.og_w = ""
        self.og_h = ""
        self.title = ""
        self.jsonld: list[str] = []
        self._collect = False
        self._buf: list[str] = []
        self._in_title = False
        self.ai_declaration = ""
        self.content_usage = ""
        self.llms_links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "meta":
            n, p, c = a.get("name", ""), a.get("property", ""), a.get("content", "")
            if n == "robots": self.robots = c
            elif p == "og:image": self.og_image = self.og_image or c
            elif p == "og:image:width": self.og_w = c
            elif p == "og:image:height": self.og_h = c
            elif n == "ai-content-declaration": self.ai_declaration = c
            elif n == "content-usage": self.content_usage = c
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._collect = True
            self._buf = []
        elif tag == "title":
            self._in_title = True
        if tag == "link" and a.get("rel") == "alternate" and a.get("type") == "text/markdown":
            self.llms_links.append(a.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "script" and self._collect:
            self.jsonld.append("".join(self._buf))
            self._collect = False
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._collect: self._buf.append(data)
        if self._in_title: self.title += data

def route_for(p: Path) -> str:
    rel = p.relative_to(ROOT)
    return "/" if rel == Path("index.html") else f"/{rel.parent.as_posix()}/"

def is_major(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    return rel == "index.html" or any(rel.startswith(pfx) for pfx in MAJOR_PREFIXES)

def audit_page(p: Path, sitemap_urls: set[str]):
    src = p.read_text(encoding="utf-8", errors="ignore")
    page = Page(); page.feed(src)
    route = route_for(p)
    url = f"{BASE}{route}"
    errors = []
    warnings = []
    ai_notes: list[str] = []
    ai_ok = True

    # JSON-LD
    jsonld_count = len(page.jsonld)
    jsonld_bad = 0
    for i, block in enumerate(page.jsonld):
        try:
            json.loads(block)
        except Exception as e:
            jsonld_bad += 1
            errors.append(f"JSON-LD block #{i+1} failed to parse: {e}")
    if jsonld_count == 0:
        warnings.append("no JSON-LD blocks")

    # Canonical
    noindex = "noindex" in (page.robots or "").lower()
    if not page.canonical:
        (warnings if noindex else errors).append("missing canonical link")
    elif not page.canonical.startswith(BASE):
        errors.append(f"canonical not on {BASE}: {page.canonical}")

    # Robots
    if not page.robots:
        warnings.append("no robots meta")
    elif "noindex" in page.robots.lower():
        warnings.append(f"robots noindex: {page.robots}")

    # OG image
    if not page.og_image:
        (warnings if noindex else errors).append("missing og:image")
    elif not page.og_image.startswith(BASE):
        errors.append(f"og:image not on {BASE}: {page.og_image}")
    if page.og_w != "1200" or page.og_h != "630":
        warnings.append(f"og:image dimensions not 1200x630 (got {page.og_w}x{page.og_h})")

    # Sitemap
    if url not in sitemap_urls and url.rstrip("/") not in {u.rstrip("/") for u in sitemap_urls}:
        warnings.append("not in sitemap.xml")

    # AI fetch/parse signal audit
    if jsonld_bad:
        ai_ok = False; ai_notes.append("invalid JSON-LD")
    if not page.ai_declaration:
        ai_notes.append("missing ai-content-declaration meta")
        if is_major(p): ai_ok = False
    if not any("llms" in (l or "") for l in page.llms_links):
        ai_notes.append("no llms.txt alternate link")
        if is_major(p): ai_ok = False
    rel = p.relative_to(ROOT).as_posix()
    for slug in CITY_SLUGS:
        if rel == f"celebrity-booking-{slug}/index.html":
            if not any(f"llms-{slug}.txt" in (l or "") for l in page.llms_links):
                errors.append(f"missing llms-{slug}.txt alternate link")
                ai_ok = False

    return {
        "route": route, "url": url, "title": page.title.strip()[:120],
        "canonical": page.canonical, "robots": page.robots,
        "og_image": page.og_image,
        "og_dimensions": f"{page.og_w}x{page.og_h}" if page.og_w else "",
        "jsonld_count": jsonld_count, "jsonld_invalid": jsonld_bad,
        "errors": errors, "warnings": warnings,
        "status": "fail" if errors else ("warn" if warnings else "pass"),
        "major": is_major(p),
        "ai_declaration": page.ai_declaration,
        "content_usage": page.content_usage,
        "llms_links": page.llms_links,
        "ai_parse_ok": ai_ok and jsonld_count > 0,
        "ai_notes": ai_notes,
    }

def load_sitemap() -> set[str]:
    sm = ROOT / "sitemap.xml"
    if not sm.is_file(): return set()
    return set(re.findall(r"<loc>([^<]+)</loc>", sm.read_text()))

def audit_robots() -> dict:
    """Validate robots.txt Content-Signal + AI crawler allowlist against baseline."""
    rp = ROOT / "robots.txt"
    if not rp.is_file():
        return {"status": "fail", "errors": ["robots.txt missing"], "warnings": [],
                "content_signal": "", "ai_agents": []}
    txt = rp.read_text(encoding="utf-8")
    errors, warnings = [], []
    cs_match = re.search(r"^\s*Content-Signal:\s*(.+)$", txt, flags=re.M | re.I)
    cs = cs_match.group(1).strip() if cs_match else ""
    if not cs:
        errors.append("Content-Signal directive missing from robots.txt")
    else:
        compact = cs.replace(" ", "")
        for tok in REQUIRED_ROBOTS_TOKENS:
            if tok not in compact:
                errors.append(f"Content-Signal regressed: '{tok}' not present (got: {cs})")
    agents = set(re.findall(r"^\s*User-agent:\s*(\S+)", txt, flags=re.M | re.I))
    missing = [a for a in REQUIRED_AI_AGENTS if a not in agents]
    if missing:
        errors.append("AI crawler allowlist regressed — missing: " + ", ".join(missing))
    baseline_path = ROOT / "admin" / "seo-monitor" / "robots-baseline.json"
    current = {"content_signal": cs,
               "ai_agents": sorted(agents & set(REQUIRED_AI_AGENTS))}
    if baseline_path.is_file():
        prev = json.loads(baseline_path.read_text())
        if prev.get("content_signal") and prev["content_signal"] != cs:
            errors.append(f"Content-Signal CHANGED since baseline (was: {prev['content_signal']!r})")
        removed = sorted(set(prev.get("ai_agents", [])) - set(current["ai_agents"]))
        if removed:
            errors.append("AI crawlers REMOVED since baseline: " + ", ".join(removed))
    else:
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(json.dumps(current, indent=2))
        warnings.append("robots baseline initialized")
    return {"status": "fail" if errors else ("warn" if warnings else "pass"),
            "errors": errors, "warnings": warnings,
            "content_signal": cs, "ai_agents": current["ai_agents"]}

def render_dashboard(report: dict) -> str:
    rows = []
    for row in sorted(report["pages"], key=lambda r: (r["status"] != "fail", r["status"] != "warn", r["route"])):
        cls = {"fail": "fail", "warn": "warn", "pass": "pass"}[row["status"]]
        issues = "<br>".join(html.escape(e) for e in row["errors"] + row["warnings"]) or "—"
        major = "★" if row["major"] else ""
        ai_badge = "✓" if row.get("ai_parse_ok") else "✗"
        ai_extra = "; ".join(row.get("ai_notes", []))
        rows.append(
            f'<tr class="{cls}"><td>{major}</td>'
            f'<td><a href="{html.escape(row["route"])}">{html.escape(row["route"])}</a></td>'
            f'<td>{row["jsonld_count"]}</td><td>{"✓" if row["canonical"] else "✗"}</td>'
            f'<td>{html.escape(row["robots"] or "—")}</td>'
            f'<td>{html.escape(row["og_dimensions"] or "—")}</td>'
            f'<td title="{html.escape(ai_extra)}">{ai_badge}</td>'
            f'<td class="cap">{row["status"].upper()}</td>'
            f'<td>{issues}</td></tr>'
        )
    s = report["summary"]
    rb = report["robots"]
    rb_cls = rb["status"]
    rb_issues = "<br>".join(html.escape(e) for e in rb["errors"] + rb["warnings"]) or "All AI signals intact."
    return f"""<!doctype html><html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>SEO Monitor · TKC Talent</title>
<meta name=robots content="noindex,nofollow">
<meta name=description content="Internal SEO compliance dashboard: sitemap, canonical, robots and JSON-LD validation per page.">
<style>:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#0a0a0a;color:#f5f1e8;font:14px/1.55 system-ui,sans-serif}}main{{max-width:1400px;margin:auto;padding:40px 24px}}h1{{font-size:clamp(2rem,5vw,3.2rem);margin:.2em 0}}.muted{{color:#aaa}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:1px;background:#333;border:1px solid #333;margin:24px 0}}.metric{{background:#151515;padding:18px}}.metric strong{{display:block;font-size:1.9rem}}.pass{{color:#86efac}}.warn{{color:#fde68a}}.fail{{color:#fca5a5}}table{{width:100%;border-collapse:collapse;background:#111;font-size:13px}}th,td{{padding:10px;text-align:left;border-bottom:1px solid #2b2b2b;vertical-align:top}}th{{position:sticky;top:0;background:#1a1a1a;z-index:1}}tr.fail td{{background:#2a0d0d}}tr.warn td{{background:#2a220d}}a{{color:#f6c453}}.cap{{font-weight:600;letter-spacing:.05em}}.legend{{margin:16px 0;color:#aaa}}.scroll{{max-height:70vh;overflow:auto;border:1px solid #333}}.panel{{padding:14px 18px;margin:18px 0;border-radius:6px;background:#151515;border:1px solid #333}}.panel.fail{{border-color:#7f1d1d;background:#1a0a0a}}.panel.warn{{border-color:#78350f;background:#1a140a}}.panel.pass{{border-color:#14532d;background:#0a1a10}}@media(max-width:800px){{th:nth-child(5),td:nth-child(5),th:nth-child(6),td:nth-child(6){{display:none}}}}</style></head><body><main>
<p class=muted>TKC Talent · Internal SEO monitor</p>
<h1>SEO compliance dashboard</h1>
<p class=muted>Generated {html.escape(report["generated_at"])} · Refresh by running <code>python3 scripts/seo-monitor.py</code> or via the <code>seo-monitor</code> GitHub Action.</p>
<section class=grid>
  <div class=metric><span>Pages scanned</span><strong>{s['total']}</strong></div>
  <div class=metric><span class=pass>Passing</span><strong class=pass>{s['pass']}</strong></div>
  <div class=metric><span class=warn>Warnings</span><strong class=warn>{s['warn']}</strong></div>
  <div class=metric><span class=fail>Failing</span><strong class=fail>{s['fail']}</strong></div>
  <div class=metric><span>JSON-LD blocks</span><strong>{s['jsonld_blocks']}</strong></div>
  <div class=metric><span>In sitemap</span><strong>{s['in_sitemap']}/{s['total']}</strong></div>
  <div class=metric><span>AI parse OK</span><strong class=pass>{s['ai_parse_ok']}/{s['total']}</strong></div>
</section>
<div class="panel {rb_cls}"><strong>robots.txt AI signals — {rb['status'].upper()}</strong><br>
Content-Signal: <code>{html.escape(rb['content_signal'] or '—')}</code><br>
AI crawlers allow-listed: <code>{html.escape(', '.join(rb['ai_agents']) or '—')}</code><br>{rb_issues}</div>
<p class=legend>★ major page (homepage, services, locations, actors). Failing checks block the SEO monitor CI job and trigger an alert issue.</p>
<div class=scroll><table><thead><tr><th>★</th><th>Route</th><th>JSON-LD</th><th>Canonical</th><th>Robots</th><th>OG size</th><th>AI</th><th>Status</th><th>Issues</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
</main></body></html>"""

def main() -> int:
    sitemap_urls = load_sitemap()
    pages = []
    for p in sorted(ROOT.glob("**/index.html")):
        if SKIP_PARTS.intersection(p.parts): continue
        pages.append(audit_page(p, sitemap_urls))
    robots_report = audit_robots()
    summary = {
        "total": len(pages),
        "pass": sum(1 for r in pages if r["status"] == "pass"),
        "warn": sum(1 for r in pages if r["status"] == "warn"),
        "fail": sum(1 for r in pages if r["status"] == "fail"),
        "jsonld_blocks": sum(r["jsonld_count"] for r in pages),
        "jsonld_invalid": sum(r["jsonld_invalid"] for r in pages),
        "in_sitemap": sum(1 for r in pages if "not in sitemap.xml" not in r["warnings"]),
        "major_failing": sum(1 for r in pages if r["major"] and r["status"] == "fail"),
        "ai_parse_ok": sum(1 for r in pages if r["ai_parse_ok"]),
        "ai_parse_failing_major": sum(1 for r in pages if r["major"] and not r["ai_parse_ok"]),
        "robots_status": robots_report["status"],
    }
    report = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary": summary,
        "pages": pages,
        "robots": robots_report,
    }
    out_dir = ROOT / "admin" / "seo-monitor"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(json.dumps(report, indent=2))
    (out_dir / "index.html").write_text(render_dashboard(report))
    with (out_dir / "history.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": report["generated_at"], **summary,
                             "robots_content_signal": robots_report["content_signal"]}) + "\n")
    print(json.dumps(summary, indent=2))
    return 1 if (summary["major_failing"] or summary["jsonld_invalid"]
                 or robots_report["status"] == "fail") else 0

if __name__ == "__main__":
    sys.exit(main())