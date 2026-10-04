#!/usr/bin/env python3
"""Fetch 90d GSC query+page data -> admin/keyword-audit/gsc-query-page.json"""
import json, os, urllib.request
from datetime import date, timedelta
G="https://connector-gateway.lovable.dev/google_search_console/webmasters/v3/sites/sc-domain%3Atkctalent.com/searchAnalytics/query"
SITES=["sc-domain%3Atkctalent.com","https%3A%2F%2Ftkctalent.com%2F"]
H={"Authorization":f"Bearer {os.environ['LOVABLE_API_KEY']}","X-Connection-Api-Key":os.environ['GOOGLE_SEARCH_CONSOLE_API_KEY'],"Content-Type":"application/json"}
end=date.today()-timedelta(days=2); start=end-timedelta(days=89)
body={"startDate":start.isoformat(),"endDate":end.isoformat(),"dimensions":["query","page"],"rowLimit":5000}
for s in SITES:
    try:
        url=f"https://connector-gateway.lovable.dev/google_search_console/webmasters/v3/sites/{s}/searchAnalytics/query"
        r=json.loads(urllib.request.urlopen(urllib.request.Request(url,json.dumps(body).encode(),H,method="POST"),timeout=90).read())
        rows=[{"query":x["keys"][0],"page":x["keys"][1],**{k:x[k] for k in("clicks","impressions","ctr","position")}} for x in r.get("rows",[])]
        json.dump({"site":s,"start":str(start),"end":str(end),"rows":rows},open("admin/keyword-audit/gsc-query-page.json","w"),indent=1)
        print(s,len(rows)); break
    except Exception as e: print(s,"ERR",e)
