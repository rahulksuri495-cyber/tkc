#!/usr/bin/env python3
"""Auto-prepare owner replies for new Google/GBP reviews.

Reads incoming reviews from admin/reviews/inbox.json (one object per review)
and writes prepared owner replies to admin/reviews/replies.json for a human
to paste back into Google Business Profile.

Input schema (admin/reviews/inbox.json):
[
  {"id": "rev_001", "reviewer": "Rohan Mehta", "rating": 5,
   "text": "Booked Zakir Khan through TKC. Flawless.",
   "artist": "Zakir Khan", "event": "corporate annual day",
   "city": "Delhi", "date": "2026-07-14"}
]

Output: admin/reviews/replies.json with a matching `reply` per review, tuned
to rating band and echoing the artist / city / event for keyword relevance.
Run manually or from the GitHub Actions workflow.
"""
from __future__ import annotations
import json, os, sys, pathlib, datetime as dt

ROOT = pathlib.Path(__file__).resolve().parents[1]
INBOX = ROOT / "admin/reviews/inbox.json"
OUT = ROOT / "admin/reviews/replies.json"

SIGN_OFF = "— Team TKC Talent · The Kabir Company · +91 95995 99699"

def reply_for(rev: dict) -> str:
    reviewer = rev.get("reviewer", "there").split()[0] or "there"
    rating = int(rev.get("rating", 5))
    artist = rev.get("artist", "").strip()
    city = rev.get("city", "").strip()
    event = rev.get("event", "").strip()

    ctx_bits = []
    if artist: ctx_bits.append(f"the {artist} booking")
    if event: ctx_bits.append(f"your {event}")
    if city: ctx_bits.append(f"in {city}")
    ctx = " ".join(ctx_bits) or "your event"

    if rating >= 5:
        body = (
            f"Thank you, {reviewer}! It genuinely means a lot that {ctx} came together the way you'd envisioned. "
            f"Our principal partners work directly with celebrity management to keep every booking transparent, "
            f"contract-clean and stress-free — and reviews like yours are why we do it. Do keep us in mind for the next one."
        )
    elif rating == 4:
        body = (
            f"Thanks so much for the honest note, {reviewer}. So glad {ctx} worked out overall. If there's a specific "
            f"detail we could have tightened, drop us a line at hello@tkctalent.com — we take that feedback into every "
            f"future booking."
        )
    else:
        body = (
            f"Thank you for flagging this, {reviewer}. We take every booking personally and clearly fell short on "
            f"{ctx}. Our founder would like to speak with you directly — please write to hello@tkctalent.com or call "
            f"+91 95995 99699 and we'll make this right."
        )
    return body + "\n\n" + SIGN_OFF

def main() -> int:
    if not INBOX.exists():
        INBOX.parent.mkdir(parents=True, exist_ok=True)
        INBOX.write_text("[]", encoding="utf-8")
        print(f"created empty inbox at {INBOX.relative_to(ROOT)}")
    inbox = json.loads(INBOX.read_text(encoding="utf-8"))
    prepared = []
    for rev in inbox:
        prepared.append({
            "id": rev.get("id"),
            "reviewer": rev.get("reviewer"),
            "rating": rev.get("rating"),
            "artist": rev.get("artist"),
            "reply": reply_for(rev),
            "prepared_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(prepared, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"prepared {len(prepared)} replies -> {OUT.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())