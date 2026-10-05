"""Shared HTML builders for the priority keyword pages (static export)."""
import json, re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tkctalent.com"
IMG = "/assets/blog/tkc-event-management/"
EMAIL = "hello@tkctalent.com"
UPDATED = "2026-10-05"


def e(s):
    return escape(s, quote=True)


def shell():
    """Return (head_common, nav, footer_and_tail) from a page that is not rewritten."""
    s = (ROOT / "event-management-mumbai" / "index.html").read_text(encoding="utf-8")
    org = re.search(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"Organization".*?</script>', s).group(0)
    i = s.index("</head>")
    j = s.index("<main>")
    k = s.index("</main>")
    nav = s[i + len("</head>"):j]
    tail = s[k + len("</main>"):]
    return org, nav, tail


def photo(name, alt, eager=False, w=960, h=540):
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{IMG}{name}-640.webp 640w, {IMG}{name}-960.webp 960w" sizes="(min-width: 1024px) 960px, 100vw"/>'
            f'<img src="{IMG}{name}-960.jpg" alt="{e(alt)}" title="{e(alt)}" width="{w}" height="{h}" decoding="async" {load} class="h-auto w-full object-cover"/></picture>')


def hero(eyebrow, h1, answer_html, facts, img, img_alt):
    lis = "".join(f'<li><strong>{e(k)}:</strong> {v}</li>' for k, v in facts)
    return f'''<section class="mx-auto max-w-5xl px-6 pt-12 pb-8 sm:px-0 sm:pt-16">
<p class="text-xs uppercase tracking-[0.3em] text-foreground/50">{e(eyebrow)}</p>
<h1 class="mt-3 font-display text-3xl font-bold leading-tight sm:text-5xl">{e(h1)}</h1>
<div class="mt-6 rounded-2xl border border-foreground/15 bg-foreground/[0.03] p-6" data-speakable="answer">
<p class="text-xs uppercase tracking-[0.25em] text-foreground/50">Quick answer</p>
<p class="mt-2 text-base leading-relaxed text-foreground/90 sm:text-lg">{answer_html}</p>
<ul class="mt-4 grid gap-2 text-sm text-foreground/80 sm:grid-cols-2">{lis}</ul>
</div>
<div class="mt-6 flex flex-wrap gap-3">
<a href="/contact-us/" class="inline-flex items-center rounded-full bg-foreground px-5 py-3 text-sm font-medium text-background hover:opacity-90">Send your brief →</a>
<a href="mailto:{EMAIL}" class="inline-flex items-center rounded-full border border-foreground/20 px-5 py-3 text-sm font-medium hover:bg-foreground hover:text-background">Email {EMAIL}</a>
</div>
<figure class="mt-8 overflow-hidden rounded-2xl border border-foreground/10">{photo(img, img_alt, eager=True)}<figcaption class="px-4 py-2 text-xs text-foreground/50">{e(img_alt)}</figcaption></figure>
</section>'''


def sec(h2, body, wide=False):
    w = "max-w-5xl" if wide else "max-w-4xl"
    return f'<section class="mx-auto {w} px-6 py-10 sm:px-0"><h2 class="font-display text-2xl font-bold sm:text-3xl">{e(h2)}</h2>{body}</section>'


def p(t):
    return f'<p class="mt-4 text-foreground/80 leading-relaxed">{t}</p>'


def ul(items):
    return '<ul class="mt-4 list-disc space-y-2 pl-5 text-foreground/80">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def ol(items):
    return '<ol class="mt-4 list-decimal space-y-2 pl-5 text-foreground/80">' + "".join(f"<li>{i}</li>" for i in items) + "</ol>"


def cards(items):
    out = '<div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">'
    for t, d in items:
        out += f'<div class="rounded-2xl border border-foreground/10 p-6"><h3 class="font-display text-lg font-semibold">{e(t)}</h3><p class="mt-2 text-sm text-foreground/70">{d}</p></div>'
    return out + "</div>"


def table(head, rows, caption=""):
    th = "".join(f'<th scope="col" class="border-b border-foreground/15 px-3 py-2 text-left font-semibold">{e(h)}</th>' for h in head)
    trs = ""
    for r in rows:
        trs += "<tr>" + "".join(f'<td class="border-b border-foreground/10 px-3 py-2 align-top">{c}</td>' for c in r) + "</tr>"
    cap = f'<caption class="mb-2 text-left text-xs text-foreground/50">{e(caption)}</caption>' if caption else ""
    return f'<div class="mt-6 overflow-x-auto"><table class="w-full min-w-[560px] text-sm text-foreground/85">{cap}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def gallery(items):
    out = '<div class="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">'
    for name, alt in items:
        out += f'<figure class="overflow-hidden rounded-2xl border border-foreground/10">{photo(name, alt)}<figcaption class="px-3 py-2 text-xs text-foreground/60">{e(alt)}</figcaption></figure>'
    return out + "</div>"


def faq_html(faqs):
    out = '<div class="mt-6 space-y-3">'
    for q, a in faqs:
        out += f'<details class="rounded-2xl border border-foreground/10 p-5"><summary class="cursor-pointer font-medium">{e(q)}</summary><p class="mt-3 text-sm text-foreground/75">{a}</p></details>'
    return out + "</div>"


def links_block(title, links):
    lis = "".join(f'<li><a class="underline underline-offset-4 hover:opacity-70" href="{u}">{e(t)}</a></li>' for t, u in links)
    return f'<section class="mx-auto max-w-5xl px-6 py-8 sm:px-0" aria-label="{e(title)}"><h2 class="font-display text-xl font-bold">{e(title)}</h2><ul class="mt-4 grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-3">{lis}</ul></section>'


def cta(h2, text):
    return f'''<section class="mx-auto max-w-5xl px-6 py-12 text-center sm:px-0"><h2 class="font-display text-2xl font-bold sm:text-3xl">{e(h2)}</h2><p class="mx-auto mt-3 max-w-2xl text-foreground/70">{text}</p>
<div class="mt-6 flex flex-wrap justify-center gap-3"><a href="/contact-us/" class="inline-flex items-center rounded-full bg-foreground px-6 py-3 text-sm font-medium text-background hover:opacity-90">Open the enquiry form →</a><a href="mailto:{EMAIL}" class="inline-flex items-center rounded-full border border-foreground/20 px-6 py-3 text-sm font-medium hover:bg-foreground hover:text-background">{EMAIL}</a></div></section>'''


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def build(slug, d):
    org, nav, tail = shell()
    url = f"{SITE}/{slug}/"
    faqs = d["faqs"]
    ld = []
    ld.append({"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage", "url": url, "name": d["title"],
               "description": d["desc"], "inLanguage": "en-IN", "dateModified": UPDATED,
               "isPartOf": {"@type": "WebSite", "name": "TKC Talent", "url": SITE + "/"},
               "about": {"@id": f"{SITE}/#org-tkc-org-jsonld-v1"},
               "primaryImageOfPage": SITE + IMG + d["img"] + "-960.jpg",
               "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", "[data-speakable='answer']"]}})
    svc = {"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": d["service_name"],
           "serviceType": d["service_type"], "url": url, "description": strip_tags(d["answer"]),
           "provider": {"@type": "LocalBusiness", "@id": f"{SITE}/#localbusiness-crpark", "name": "TKC Talent (The Kabir Company)",
                        "url": SITE + "/", "email": EMAIL, "image": SITE + IMG + d["img"] + "-960.jpg", "priceRange": "₹₹₹",
                        "address": {"@type": "PostalAddress", "streetAddress": "600, CR Park", "addressLocality": "New Delhi",
                                    "addressRegion": "Delhi", "postalCode": "110019", "addressCountry": "IN"},
                        "geo": {"@type": "GeoCoordinates", "latitude": 28.5386, "longitude": 77.2479},
                        "foundingDate": "2005"},
           "areaServed": [{"@type": "City" if a not in ("India", "Delhi NCR") else "Place", "name": a} for a in d["area"]]}
    ld.append(svc)
    ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faqs]})
    crumbs = [("Home", SITE + "/")] + d.get("crumbs", []) + [(d["crumb"], url)]
    ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]})
    if d.get("gallery"):
        ld.append({"@context": "https://schema.org", "@type": "ImageGallery", "@id": url + "#image-gallery", "name": d["h1"] + " — event photos",
                   "url": url, "associatedMedia": [{"@type": "ImageObject", "contentUrl": SITE + IMG + n + "-960.jpg", "name": a, "caption": a,
                                                    "width": 960, "height": 540, "creditText": "TKC Talent",
                                                    "copyrightHolder": {"@type": "Organization", "name": "The Kabir Company"}} for n, a in d["gallery"]]})
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    og_img = SITE + IMG + d["img"] + "-960.jpg"
    head = f'''<!DOCTYPE html><html lang="en"><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="author" content="The Kabir Company"/>
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"/>
<meta name="theme-color" content="#0a0a0a"/>
<meta name="geo.region" content="{d.get("geo_region", "IN-DL")}"/><meta name="geo.placename" content="{e(d.get("geo_place", "New Delhi, India"))}"/>
<title>{e(d["title"])}</title>
<meta name="description" content="{e(d["desc"])}"/>
<link rel="canonical" href="{url}"/>
<link rel="alternate" hreflang="en-IN" href="{url}"/>
<link rel="alternate" hreflang="x-default" href="{url}"/>
<meta property="og:site_name" content="TKC Talent"/>
<meta property="og:type" content="website"/><meta property="og:locale" content="en_IN"/>
<meta property="og:url" content="{url}"/>
<meta property="og:title" content="{e(d["title"])}"/>
<meta property="og:description" content="{e(d["desc"])}"/>
<meta property="og:image" content="{og_img}"/><meta property="og:image:width" content="960"/><meta property="og:image:height" content="540"/>
<meta property="og:image:alt" content="{e(d["img_alt"])}"/>
<meta property="article:modified_time" content="{UPDATED}T09:00:00+05:30"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:site" content="@tkctalent"/>
<meta name="twitter:title" content="{e(d["title"])}"/>
<meta name="twitter:description" content="{e(d["desc"])}"/>
<meta name="twitter:image" content="{og_img}"/>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;family=Space+Grotesk:wght@500;700&amp;display=swap"/>
<link rel="stylesheet" href="/assets/styles-B3eDpzGa.css"/>
<link rel="alternate" type="text/markdown" href="{SITE}/{d.get("llms", "llms.txt")}" title="LLM-friendly summary"/>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-WQF5WX2TTB"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-WQF5WX2TTB');</script>
{ld_html}{org}
</head>'''
    crumb_html = '<nav aria-label="Breadcrumb" class="mx-auto max-w-5xl px-6 pt-6 text-xs text-foreground/50 sm:px-0">' + " › ".join(
        (f'<a href="{u.replace(SITE, "")}" class="hover:opacity-70">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span aria-current="page">{e(n)}</span>')
        for i, (n, u) in enumerate(crumbs)) + "</nav>"
    updated = f'<p class="mx-auto max-w-5xl px-6 text-xs text-foreground/50 sm:px-0">Last updated: 5 October 2026 · TKC Talent (The Kabir Company), 600 CR Park, New Delhi</p>'
    main = "<main>\n" + crumb_html + hero(d["eyebrow"], d["h1"], d["answer"], d["facts"], d["img"], d["img_alt"]) + updated + "".join(d["sections"])
    if d.get("gallery"):
        main += sec(d.get("gallery_title", "Photos from events we have produced"), p("Real photos from events produced by TKC Talent.") + gallery(d["gallery"]), wide=True)
    main += sec(d.get("faq_title", "Frequently asked questions"), faq_html(faqs))
    main += links_block("Related pages", d["related"]) + cta(d["cta_h2"], d["cta_text"]) + "\n</main>"
    out = head + nav + main + tail
    path = ROOT / slug / "index.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")
    return path
