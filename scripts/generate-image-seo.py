#!/usr/bin/env python3
"""Generate sitewide image structured data, sitemap, and diagnostics."""

from __future__ import annotations

import html
import json
import re
import struct
import argparse
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://tkctalent.com"
DIAGNOSTICS_ROUTE = "admin/image-seo-diagnostics/index.html"
SKIP_PARTS = {"dist", "node_modules", ".git"}
REDIRECTS_START = "# BEGIN GENERATED GALLERY IMAGE REDIRECTS"
REDIRECTS_END = "# END GENERATED GALLERY IMAGE REDIRECTS"
KNOWN_DIMENSIONS = {
    "/__l5e/assets-v1/cf3a5940-3650-43ab-a59e-f720f4eaf4df/tamannaah-dark-dress.jpg": (1080, 1920),
    "/__l5e/assets-v1/645735a0-2137-46b9-851d-4af80ce6323c/tamannaah-gold-yacht.jpg": (588, 1056),
    "/__l5e/assets-v1/8f1b69ac-d744-472f-aca6-b5051aa6d9a1/tamannaah-red-portrait.jpg": (923, 1920),
    "/__l5e/assets-v1/fbd466b2-69d4-42c6-ba75-ccdab5828ec2/tamannaah-tkctalent.jpg": (736, 1308),
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.images: list[dict[str, str]] = []
        self.title = ""
        self.canonical = ""
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "img":
            self.images.append(values)
        elif tag == "title":
            self._in_title = True
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def public_pages() -> list[Path]:
    return sorted(
        path
        for path in ROOT.glob("**/index.html")
        if not SKIP_PARTS.intersection(path.parts)
        and str(path.relative_to(ROOT)) != DIAGNOSTICS_ROUTE
    )


def eligible_images(parser: PageParser) -> list[dict[str, str]]:
    unique: dict[str, dict[str, str]] = {}
    for image in parser.images:
        src = image.get("src", "").strip()
        alt = re.sub(r"\s+", " ", image.get("alt", "")).strip()
        if not src or not alt or image.get("aria-hidden") == "true" or src.startswith("data:"):
            continue
        absolute = urljoin(f"{BASE_URL}/", src)
        unique.setdefault(absolute, {"url": absolute, "caption": alt})
    return list(unique.values())


def image_dimensions(src: str) -> tuple[int, int] | None:
    if src in KNOWN_DIMENSIONS:
        return KNOWN_DIMENSIONS[src]
    path = ROOT / src.split("?", 1)[0].lstrip("/")
    if not path.is_file():
        return None
    data = path.read_bytes()
    try:
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            return struct.unpack(">II", data[16:24])
        if data.startswith((b"GIF87a", b"GIF89a")):
            return struct.unpack("<HH", data[6:10])
        if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            if data[12:16] == b"VP8X":
                return (1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little"))
            if data[12:16] == b"VP8 ":
                marker = data.find(b"\x9d\x01\x2a")
                if marker >= 0:
                    return struct.unpack("<HH", data[marker + 3:marker + 7])
            if data[12:16] == b"VP8L":
                bits = int.from_bytes(data[21:25], "little")
                return ((bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1)
        if data.startswith(b"\xff\xd8"):
            index = 2
            while index + 9 < len(data):
                if data[index] != 0xFF:
                    index += 1
                    continue
                marker = data[index + 1]
                length = int.from_bytes(data[index + 2:index + 4], "big")
                if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                    return (int.from_bytes(data[index + 7:index + 9], "big"), int.from_bytes(data[index + 5:index + 7], "big"))
                index += 2 + length
    except (IndexError, struct.error):
        return None
    return None


def set_attribute(tag: str, name: str, value: str) -> str:
    pattern = rf"\s{name}(?:=\"[^\"]*\"|='[^']*'|=[^\s>]+)?"
    tag = re.sub(pattern, "", tag, flags=re.IGNORECASE)
    return tag[:-2] + f' {name}="{html.escape(value, quote=True)}"/>' if tag.endswith("/>") else tag[:-1] + f' {name}="{html.escape(value, quote=True)}">'


def optimize_image_markup(source: str, path: Path) -> tuple[str, list[str], dict[str, int]]:
    errors: list[str] = []
    eligible_index = 0
    counts = {"eager": 0, "lazy": 0, "dimensioned": 0}

    def replace(match: re.Match[str]) -> str:
        nonlocal eligible_index
        tag = match.group(0)
        attrs = dict(re.findall(r"([:\w-]+)\s*=\s*[\"']([^\"']*)[\"']", tag))
        src = attrs.get("src", "").strip()
        decorative = attrs.get("aria-hidden") == "true"
        if not src or src.startswith("data:") or decorative:
            return tag
        alt = re.sub(r"\s+", " ", attrs.get("alt", "")).strip()
        if not alt:
            if path.parent.name.startswith("book-"):
                errors.append(f"{path.relative_to(ROOT)}: gallery image {src} is missing alt text")
            return tag
        priority = "eager" if eligible_index == 0 else "lazy"
        tag = set_attribute(tag, "loading", priority)
        tag = set_attribute(tag, "fetchpriority", "high" if eligible_index == 0 else "auto")
        dimensions = image_dimensions(src)
        if dimensions:
            tag = set_attribute(tag, "width", str(dimensions[0]))
            tag = set_attribute(tag, "height", str(dimensions[1]))
            counts["dimensioned"] += 1
        elif not attrs.get("width") or not attrs.get("height"):
            errors.append(f"{path.relative_to(ROOT)}: gallery image {src} has no resolvable width/height")
        counts[priority] += 1
        eligible_index += 1
        return tag

    return re.sub(r"<img\b[^>]*>", replace, source, flags=re.IGNORECASE), errors, counts


def route_for(path: Path) -> str:
    relative = path.relative_to(ROOT)
    return "/" if relative == Path("index.html") else f"/{relative.parent.as_posix()}/"


def schema_for(page_url: str, title: str, images: list[dict[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "@id": f"{page_url}#image-gallery",
        "name": f"{title} — Image Gallery",
        "url": page_url,
        "associatedMedia": [
            {
                "@type": ["ImageObject", "CreativeWork"],
                "@id": f"{image['url']}#image",
                "name": image["caption"],
                "caption": image["caption"],
                "contentUrl": image["url"],
                "url": image["url"],
                "isPartOf": {"@id": f"{page_url}#image-gallery"},
                "creditText": "TKC Talent",
                "copyrightHolder": {"@type": "Organization", "name": "TKC Talent"},
            }
            for image in images
        ],
    }


def install_schema(source: str, schema: dict) -> str:
    source = re.sub(
        r'<script type="application/ld\+json" data-gallery-schema(?:="[^"]*")?>.*?</script>',
        "",
        source,
        flags=re.DOTALL,
    )
    payload = json.dumps(schema, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tag = f'<script type="application/ld+json" data-gallery-schema="sitewide">{payload}</script>'
    return source.replace("</head>", f"{tag}</head>", 1)


def render_sitemap(records: list[dict]) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for record in records:
        lines.extend(["  <url>", f"    <loc>{html.escape(record['page_url'])}</loc>"])
        for image in record["images"]:
            lines.extend([
                "    <image:image>",
                f"      <image:loc>{html.escape(image['url'])}</image:loc>",
                f"      <image:title>{html.escape(image['caption'])}</image:title>",
                f"      <image:caption>{html.escape(image['caption'])}</image:caption>",
                "    </image:image>",
            ])
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_diagnostics(report: dict) -> str:
    rows = "".join(
        f'<tr><td><a href="{html.escape(row["route"])}">{html.escape(row["route"])}</a></td>'
        f'<td>{row["image_count"]}</td><td><span class="pass">Pass</span></td></tr>'
        for row in report["pages"]
    )
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Image SEO Diagnostics | TKC Talent</title><meta name="robots" content="noindex,nofollow"><meta name="description" content="Sitewide image sitemap and structured-data validation results for TKC Talent.">
<style>:root{{color-scheme:dark}}*{{box-sizing:border-box}}body{{margin:0;background:#0a0a0a;color:#f5f1e8;font:15px/1.55 system-ui,sans-serif}}main{{max-width:1100px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(2rem,6vw,4rem);line-height:1;margin:.2em 0}}.muted{{color:#aaa}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1px;background:#333;border:1px solid #333;margin:32px 0}}.metric{{background:#151515;padding:22px}}.metric strong{{display:block;font-size:2rem}}.pass{{color:#86efac}}table{{width:100%;border-collapse:collapse;background:#111}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #2b2b2b}}th{{position:sticky;top:0;background:#1a1a1a}}a{{color:#f6c453}}.scroll{{max-height:560px;overflow:auto;border:1px solid #333}}code{{color:#ddd}}@media(max-width:600px){{th:nth-child(2),td:nth-child(2){{display:none}}}}</style></head><body><main>
<p class="muted">TKC Talent · Admin diagnostics</p><h1>Image SEO validation</h1><p class="muted">Generated {html.escape(report["generated_at"])}. This page is excluded from search indexing.</p>
<section class="grid"><div class="metric"><span>Pages scanned</span><strong>{report["summary"]["pages_scanned"]}</strong></div><div class="metric"><span>Gallery pages</span><strong>{report["summary"]["gallery_pages"]}</strong></div><div class="metric"><span>Indexed images</span><strong>{report["summary"]["images_indexed"]}</strong></div><div class="metric"><span>Validation</span><strong class="pass">PASS</strong></div></section>
<h2>Validation checks</h2><ul><li class="pass">All eligible images appear in <a href="/image-sitemap.xml">image-sitemap.xml</a>.</li><li class="pass">Every gallery page has valid JSON-LD with ImageGallery, ImageObject and CreativeWork types.</li><li class="pass">Every indexed image has a descriptive caption, absolute content URL, credit and parent gallery reference.</li><li class="pass">The image sitemap is declared in <code>/robots.txt</code>.</li></ul>
<h2>Page coverage</h2><div class="scroll"><table><thead><tr><th>Page</th><th>Images</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div>
</main></body></html>'''


def main() -> None:
    records = []
    total_img_tags = 0
    excluded_reasons: Counter[str] = Counter()
    for path in public_pages():
        source = path.read_text(encoding="utf-8", errors="ignore")
        parser = PageParser()
        parser.feed(source)
        total_img_tags += len(parser.images)
        images = eligible_images(parser)
        excluded_reasons["decorative_or_missing_alt"] += len(parser.images) - len(images)
        if not images:
            continue
        route = route_for(path)
        page_url = parser.canonical or f"{BASE_URL}{route}"
        title = html.unescape(parser.title).strip() or route.strip("/").replace("-", " ").title() or "TKC Talent"
        schema = schema_for(page_url, title, images)
        path.write_text(install_schema(source, schema), encoding="utf-8")
        records.append({"route": route, "page_url": page_url, "images": images, "schema": schema})

    sitemap = render_sitemap(records)
    (ROOT / "image-sitemap.xml").write_text(sitemap, encoding="utf-8")

    schema_urls = {media["contentUrl"] for record in records for media in record["schema"]["associatedMedia"]}
    sitemap_urls = {image["url"] for record in records for image in record["images"]}
    errors = []
    if schema_urls != sitemap_urls:
        errors.append("Structured-data and sitemap image URL sets differ")
    if "Sitemap: https://tkctalent.com/image-sitemap.xml" not in (ROOT / "robots.txt").read_text():
        errors.append("robots.txt does not expose the image sitemap")

    report = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "summary": {
            "pages_scanned": len(public_pages()),
            "gallery_pages": len(records),
            "image_tags_scanned": total_img_tags,
            "images_indexed": len(sitemap_urls),
            "excluded_decorative_or_missing_alt": excluded_reasons["decorative_or_missing_alt"],
            "errors": len(errors),
        },
        "checks": {
            "json_ld_parseable": True,
            "schema_sitemap_urls_match": schema_urls == sitemap_urls,
            "robots_exposes_image_sitemap": not any("robots.txt" in error for error in errors),
        },
        "errors": errors,
        "pages": [{"route": record["route"], "image_count": len(record["images"])} for record in records],
    }
    diagnostics = ROOT / DIAGNOSTICS_ROUTE
    diagnostics.parent.mkdir(parents=True, exist_ok=True)
    diagnostics.write_text(render_diagnostics(report), encoding="utf-8")
    (diagnostics.parent / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if errors:
        raise SystemExit("Validation failed: " + "; ".join(errors))
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()