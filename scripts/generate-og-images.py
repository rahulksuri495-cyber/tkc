#!/usr/bin/env python3
"""Generate per-page branded 1200x630 og:image cards and update HTML metadata.

Covers all 6 city pages, /ourservice/, /corporate-event-management/,
/celebrity-booking-india/, and every /book-*/ actor page.

Each card is composited from the page's existing source image (hero or
headshot) with a brand bar + dark gradient + page-specific title so social
platforms (Facebook, LinkedIn, X, WhatsApp) get a consistent, correctly sized
preview that can never be reused incorrectly across pages.
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1200, 630
BRAND = "TKC TALENT  ·  THE KABIR COMPANY"
ACCENT = (246, 196, 83)

def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    match = subprocess.run(
        ["fc-match", "-f", "%{file}\n", f"Liberation Sans:{weight}"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return ImageFont.truetype(match, size)

def resolve_local(src: str) -> Path | None:
    if src.startswith("http"):
        src = urlparse(src).path
    if not src:
        return None
    p = ROOT / src.lstrip("/")
    return p if p.is_file() else None

def cover_resize(im: Image.Image) -> Image.Image:
    iw, ih = im.size
    scale = max(W / iw, H / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - W) // 2
    y = (nh - H) // 2
    return im.crop((x, y, x + W, y + H))

def gradient(alpha_top: int, alpha_bot: int) -> Image.Image:
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / (H - 1)
        grad.putpixel((0, y), int(alpha_top * (1 - t) + alpha_bot * t))
    grad = grad.resize((W, H))
    layer = Image.new("RGBA", (W, H), (10, 10, 14, 0))
    layer.putalpha(grad)
    return layer

def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def render_card(source: Path | None, eyebrow: str, title: str, subtitle: str, out: Path) -> None:
    canvas = Image.new("RGB", (W, H), (10, 10, 14))
    if source:
        try:
            bg = Image.open(source).convert("RGB")
            bg = cover_resize(bg).filter(ImageFilter.GaussianBlur(radius=6))
            canvas.paste(bg, (0, 0))
        except Exception:
            pass
    # left-to-right dark gradient for legibility
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(W):
        a = int(220 * max(0.0, 1.0 - x / (W * 0.85)))
        od.line([(x, 0), (x, H)], fill=(8, 8, 12, a))
    # bottom vertical gradient
    overlay = Image.alpha_composite(overlay, gradient(0, 200))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

    d = ImageDraw.Draw(canvas)
    # brand strip top
    d.rectangle([(0, 0), (W, 6)], fill=ACCENT)
    d.text((60, 40), BRAND, font=font("bold", 22), fill=ACCENT)

    # eyebrow
    d.text((60, 200), eyebrow.upper(), font=font("bold", 28), fill=ACCENT)
    # title
    tfont = font("bold", 78)
    lines = wrap(d, title, tfont, W - 120)
    if len(lines) > 2:
        tfont = font("bold", 62)
        lines = wrap(d, title, tfont, W - 120)
    y = 250
    for line in lines[:3]:
        d.text((60, y), line, font=tfont, fill=(255, 255, 255))
        y += tfont.size + 8

    # subtitle
    sfont = font("regular", 30)
    for line in wrap(d, subtitle, sfont, W - 120)[:2]:
        d.text((60, y + 18), line, font=sfont, fill=(230, 230, 230))
        y += sfont.size + 4

    # footer cta
    d.text((60, H - 70), "tkctalent.com  ·  +91 95995 99699", font=font("bold", 24), fill=(255, 255, 255))

    canvas.save(out, "JPEG", quality=86, optimize=True, progressive=True)

PRETTY_CITY = {
    "delhi": "Delhi NCR", "mumbai": "Mumbai", "goa": "Goa",
    "gurgaon": "Gurgaon", "jaipur": "Jaipur", "noida": "Noida",
}

def update_html(path: Path, og_path: str) -> None:
    src = path.read_text(encoding="utf-8")
    abs_url = f"https://tkctalent.com{og_path}"
    replacements = {
        r'<meta property="og:image" content="[^"]*"\s*/?>': f'<meta property="og:image" content="{abs_url}"/>',
        r'<meta property="og:image:secure_url" content="[^"]*"\s*/?>': f'<meta property="og:image:secure_url" content="{abs_url}"/>',
        r'<meta property="og:image:width" content="[^"]*"\s*/?>': '<meta property="og:image:width" content="1200"/>',
        r'<meta property="og:image:height" content="[^"]*"\s*/?>': '<meta property="og:image:height" content="630"/>',
        r'<meta property="og:image:type" content="[^"]*"\s*/?>': '<meta property="og:image:type" content="image/jpeg"/>',
        r'<meta name="twitter:image" content="[^"]*"\s*/?>': f'<meta name="twitter:image" content="{abs_url}"/>',
        r'<meta property="twitter:image" content="[^"]*"\s*/?>': f'<meta property="twitter:image" content="{abs_url}"/>',
    }
    for pat, rep in replacements.items():
        if re.search(pat, src):
            src = re.sub(pat, rep, src)
        else:
            src = src.replace("</head>", rep + "</head>", 1)
    # remove additional duplicate og:image variants beyond the first
    seen = {"og:image": 0, "twitter:image": 0}
    def dedup(m: re.Match) -> str:
        prop = m.group(1)
        seen[prop] += 1
        return m.group(0) if seen[prop] == 1 else ""
    src = re.sub(r'<meta (?:property|name)="(og:image|twitter:image)" content="[^"]*"\s*/?>', dedup, src)
    path.write_text(src, encoding="utf-8")

def current_og(path: Path) -> str | None:
    src = path.read_text(encoding="utf-8")
    m = re.search(r'og:image" content="([^"]+)"', src)
    return m.group(1) if m else None

def slug_to_name(slug: str) -> str:
    return " ".join(w.capitalize() for w in slug.split("-"))

def main() -> None:
    targets: list[tuple[Path, str, str, str, str]] = []
    # (page_path, source_image_hint, slug, eyebrow, title, subtitle)
    for city, label in PRETTY_CITY.items():
        targets.append((
            ROOT / f"celebrity-booking-{city}" / "index.html",
            f"assets/locations/{city}-celebrity-event.jpg",
            f"city-{city}",
            "Celebrity Booking",
            f"Book Bollywood Celebrities in {label}",
            "Singers · Actors · Comedians · DJs · Influencers — 2026 fees on request",
        ))
    targets.append((ROOT / "ourservice/index.html", "assets/services/event-services-hero.jpg",
                    "service-ourservice", "Our Services",
                    "Celebrity Booking & Event Management",
                    "Artist booking, corporate events, weddings, brand integrations across India."))
    targets.append((ROOT / "corporate-event-management/index.html", "assets/services/corporate-event-hero.jpg",
                    "service-corporate", "Corporate Events",
                    "Corporate Event Management India",
                    "Conferences, town halls, product launches, dealer meets with celebrity headliners."))
    targets.append((ROOT / "celebrity-booking-india/index.html", None, "service-celebrity-booking-india",
                    "Pan-India", "Celebrity Booking India — Fees & Availability",
                    "Verified booking agency for Bollywood actors, singers, comedians and influencers."))

    for actor_dir in sorted(ROOT.glob("book-*/")):
        slug = actor_dir.name.removeprefix("book-")
        targets.append((actor_dir / "index.html", None, f"actor-{slug}",
                        "Book Celebrity",
                        f"Book {slug_to_name(slug)} for Your Event",
                        "Official booking enquiries · 2026 fees · pan-India availability"))

    rendered = 0
    for page, hint, slug, eyebrow, title, subtitle in targets:
        if not page.is_file():
            continue
        source = resolve_local(hint) if hint else None
        if source is None:
            existing = current_og(page)
            if existing and "og-image.jpg" not in existing:
                source = resolve_local(existing)
        out = OUT_DIR / f"{slug}.jpg"
        render_card(source, eyebrow, title, subtitle, out)
        update_html(page, f"/assets/og/{slug}.jpg")
        rendered += 1
    print(f"rendered {rendered} og cards into {OUT_DIR.relative_to(ROOT)}")

if __name__ == "__main__":
    main()