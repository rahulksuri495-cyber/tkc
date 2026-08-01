#!/usr/bin/env python3
"""Extract reusable head, header, and footer templates from a representative page."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_SRC = ROOT / "celebrity-management-company" / "index.html"

src = TEMPLATE_SRC.read_text(encoding="utf-8")

# Extract full <head> (including <head> and </head> tags)
head_match = re.search(r"(<head>.*?</head>)", src, re.S | re.I)
head = head_match.group(1) if head_match else ""

# Extract body header: from <body> to first <main> or <section>
body_start = src.find("<body")
body_end = src.find("</body>")
body = src[body_start:body_end]
header_end = body.find("<main")
if header_end == -1:
    header_end = body.find("<section")
header = body[0:header_end]

# Extract footer: from last <footer> to </footer>
footer_start = body.rfind("<footer")
footer = body[footer_start:body.find("</footer>", footer_start) + 9]

(ROOT / "_templates").mkdir(exist_ok=True)
(ROOT / "_templates" / "head.html").write_text(head, encoding="utf-8")
(ROOT / "_templates" / "header.html").write_text(header, encoding="utf-8")
(ROOT / "_templates" / "footer.html").write_text(footer, encoding="utf-8")
print(f"Head template: {len(head)} bytes")
print(f"Header template: {len(header)} bytes")
print(f"Footer template: {len(footer)} bytes")
