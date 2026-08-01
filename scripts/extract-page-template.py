#!/usr/bin/env python3
"""Create new SEO hub pages using the existing header/footer template."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_SRC = ROOT / "celebrity-management-company" / "index.html"

# Extract header and footer from a representative page
src = TEMPLATE_SRC.read_text(encoding="utf-8")
body_start = src.find("<body")
body_end = src.find("</body>")
body = src[body_start:body_end]

# Find header: everything before first <main> or <section>
header_end = body.find("<main")
if header_end == -1:
    header_end = body.find("<section")
header = body[0:header_end]

# Find footer: from last <footer> to </footer>
footer_start = body.rfind("<footer")
footer = body[footer_start:body.find("</footer>", footer_start) + 9]

# Save templates
(ROOT / "_templates").mkdir(exist_ok=True)
(ROOT / "_templates" / "header.html").write_text(header, encoding="utf-8")
(ROOT / "_templates" / "footer.html").write_text(footer, encoding="utf-8")
print(f"Header template: {len(header)} bytes")
print(f"Footer template: {len(footer)} bytes")
