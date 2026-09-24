#!/usr/bin/env python3
"""Fetch GSC data for the 10 priority book-* pages and write admin/gsc-priority/data.json."""
import json, os, sys, urllib.request, urllib.error
from datetime import date, timedelta

SITE = "https://tkctalent.com/"
PAGES = [
    "book-salman-khan","book-shah-rukh-khan",
    "book-alia-bhatt","book-deepika-padukone","book-diljit-dosanjh",
    "book-darshan-raval","book-shreya-ghoshal",
    "blog/event-management-company-india",
]
GATEWAY = "https://connector-gateway.lovable.dev/google_search_console/webmasters/v3/sites/https%3A%2F%2Ftkctalent.com%2F/searchAnalytics/query"
HEADERS = {
    "Authorization": f"Bearer {os.environ['LOVABLE_API_KEY']}",
    "X-Connection-Api-Key": os.environ['GOOGLE_SEARCH_CONSOLE_API_KEY'],
    "Content-Type": "application/json",
}

def gsc(body):
    req = urllib.request.Request(GATEWAY, data=json.dumps(body).encode(), headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print("ERR", e.code, e.read()[:400], file=sys.stderr); return {"rows":[]}

today = date.today()
# GSC data lags ~2 days
end = today - timedelta(days=2)
cur_start = end - timedelta(days=27)      # last 28d
prev_end = cur_start - timedelta(days=1)
prev_start = prev_end - timedelta(days=27)  # previous 28d

def daily_totals(page_url, start, end):
    r = gsc({
        "startDate": start.isoformat(), "endDate": end.isoformat(),
        "dimensions": ["date"], "rowLimit": 1000,
        "dimensionFilterGroups":[{"filters":[{"dimension":"page","operator":"equals","expression":page_url}]}],
    })
    return [{"date": row["keys"][0], **{k:row[k] for k in ("clicks","impressions","ctr","position")}} for row in r.get("rows",[])]

def top_queries(page_url, start, end, limit=25):
    r = gsc({
        "startDate": start.isoformat(), "endDate": end.isoformat(),
        "dimensions":["query"], "rowLimit": limit,
        "dimensionFilterGroups":[{"filters":[{"dimension":"page","operator":"equals","expression":page_url}]}],
    })
    return [{"query": row["keys"][0], **{k:row[k] for k in ("clicks","impressions","ctr","position")}} for row in r.get("rows",[])]

out = {"generated_at": today.isoformat(), "current": {"start": cur_start.isoformat(), "end": end.isoformat()},
       "previous": {"start": prev_start.isoformat(), "end": prev_end.isoformat()}, "pages": []}

for slug in PAGES:
    url = f"https://tkctalent.com/{slug}/"
    print("fetch", slug, file=sys.stderr)
    daily = daily_totals(url, cur_start, end)
    cur_q = top_queries(url, cur_start, end)
    prev_q = {q["query"]: q for q in top_queries(url, prev_start, prev_end, limit=100)}
    deltas = []
    for q in cur_q:
        p = prev_q.get(q["query"])
        deltas.append({
            **q,
            "prev_impressions": p["impressions"] if p else 0,
            "prev_position": p["position"] if p else None,
            "impressions_delta": q["impressions"] - (p["impressions"] if p else 0),
            "position_delta": (p["position"] - q["position"]) if p else None,  # positive = climbing
        })
    out["pages"].append({"slug": slug, "url": url, "daily": daily, "queries": deltas})

with open("admin/gsc-priority/data.json","w") as f:
    json.dump(out, f, indent=2)
print("wrote admin/gsc-priority/data.json")
