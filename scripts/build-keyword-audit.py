#!/usr/bin/env python3
"""Build admin/keyword-audit/audit.json + keyword-audit.csv from GSC data + Semrush (India) volumes + on-page review."""
import json, csv
G=json.load(open("admin/keyword-audit/gsc-query-page.json"))
def gsc(q):
    rs=[r for r in G["rows"] if r["query"]==q]
    if not rs: return None
    i=sum(r["impressions"] for r in rs); top=max(rs,key=lambda r:r["impressions"])
    return {"impr":i,"clicks":sum(r["clicks"] for r in rs),"pos":round(sum(r["position"]*r["impressions"] for r in rs)/i,1),
            "ranking_page":top["page"].replace("https://tkctalent.com",""),"pages_competing":len(rs)}
# keyword, Semrush IN volume (None=unknown), difficulty, target page, priority, fixes
K=[
("event management company","6600","25","/event-management-company/","Critical","Fixed 5 Oct 2026: new service page /event-management-company/ (answer-first intro, cost table, FAQ + Service schema), linked from every page footer, the homepage and the menu. Next: Request indexing."),
("event planners in delhi","2400","28","/event-planners-delhi/","Critical","Fixed 5 Oct 2026: rewritten as a planning page (timeline, Delhi permits, budget items) distinct from the Delhi NCR page; linked sitewide. Next: Request indexing."),
("wedding planner delhi","1900","14","/wedding-planner-delhi/","High","Fixed 5 Oct 2026: new /wedding-planner-delhi/ page, linked sitewide. Next: Request indexing."),
("event management company in delhi","1300","31","/event-management-delhi/","Critical","Fixed 5 Oct 2026: existing /event-management-delhi/ made the main Delhi NCR page (rewritten, H1 = keyword), links raised from 11 pages to sitewide. Next: Request indexing."),
("event management company in gurgaon","880","26","/event-management-gurgaon/","High","Fixed 5 Oct 2026: rewritten with Gurgaon areas, permits, tips and Durga Puja Gurgaon stalls; linked sitewide. Next: Request indexing."),
("corporate event management company","880","37","/corporate-event-management/","High","Fixed 5 Oct 2026: /corporate-event-management/ is the main page (title fixed, answer-first box); blog retitled as a costs guide linking to it."),
("best event management company in india","260","15","/blog/event-management-company-india/","High","Recently rewritten. Request indexing in Search Console and add links from city pages."),
("event management company in delhi ncr","70","0","/event-management-delhi/","High","Fixed 5 Oct 2026: covered by /event-management-delhi/ (H1 "Event Management Company in Delhi NCR")."),
("best event management company in delhi ncr","10","0","/event-management-delhi/","Medium","Fixed 5 Oct 2026: "Best event management company in Delhi NCR: how to decide" section + comparison table on /event-management-delhi/."),
("celebrity management company","210","10","/celebrity-management-company/","High","Only 11 internal links, and the homepage title targets the same phrase. Give the homepage a 'celebrity booking agency' title and link this page sitewide."),
("book celebrity","140","29","/celebrity-booking-india/","High","Fixed 5 Oct 2026: /celebrity-booking-india/ new title/H1 (Book a Celebrity for Your Event) + answer box; pan-India page refocused on multi-city tours and links back."),
("celebrity booking","140","29","/celebrity-booking-india/","High","Fixed 5 Oct 2026: same as above; menu label 'Pan-India Celebrities' renamed 'Multi-City Celebrity Tours' on 180 pages."),
("celebrity booking agency","110","0","/celebrity-booking-india/","Medium","The homepage ranks at position 3. Keep it, and add an 'agency' FAQ to /celebrity-booking-india/."),
("celebrity booking india","20","0","/celebrity-booking-india/","High","No impressions, even though this page has 177 internal links. Its title and H1 are too short; rewrite them and add a 'How celebrity booking works in India' answer and FAQ schema."),
("book celebrity for wedding",None,None,"/book-celebrity-for-wedding/","Critical","Fixed 5 Oct 2026: /book-celebrity-for-wedding/ is the only wedding page (new title/H1, answer box), linked from every page footer; Delhi and Bollywood pages no longer target weddings."),
("book celebrity for event",None,None,"/celebrity-booking-delhi/","High","Position 11–14. Add an 'How to hire a celebrity for an event' answer box and HowTo steps."),
("bollywood celebrity charges",None,None,"/bollywood-celebrity-charges/","Medium","Strong (position 2–5 on fee searches) but has no FAQ schema. Add FAQ and a dated 'last updated' line."),
("hire bollywood celebrity",None,None,"/bollywood-celebrity-booking/","Medium","H1 'fully managed.' is vague; rewrite it as 'Hire Bollywood Celebrities for Events'."),
("singer booking","70","0","/singer-booking-india/","Medium","Position 6. The title 'Singer Booking India — More' looks broken; fix it, change the H1 to 'Book Singers in India', and add FAQ schema."),
("comedian booking","30","0","/comedian-booking-india/","Medium","Has no FAQ; add an answer-first intro and FAQ schema."),
("celebrity dj booking","20","0","/celebrity-dj-booking/","Low","Ranks for DJ Chetas searches. Add a DJ fee table."),
("artist booking agency","30","0","/blog/artist-booking-agency-india/","Low","The homepage ranks at position 6. Fine; add an internal link to the blog page."),
("haryanvi artist booking",None,None,"/haryanvi-artist-booking/","Medium","Thin page (604 words) with no FAQ. Expand with artist list, fees and FAQ."),
("sapna choudhary booking","20","0","/book-sapna-choudhary/","Low","New page. Request indexing."),
("durga puja stall booking","0","0","/durga-puja-2026/","Low","Already position 4.9. Keep it updated."),
]
rows=[]
for k,v,d,p,pr,fix in K:
    g=gsc(k)
    if not g: st="Not ranking (no impressions)" if p!="(none)" else "No page"
    elif g["pages_competing"]>1 and g["pos"]>10: st="Pages competing"
    elif p.split()[0] not in (g["ranking_page"],) and not p.startswith("(") : st=f"Wrong page ranking"
    elif g["pos"]<=10: st="Ranking page 1"
    else: st="Page 2+"
    if p.startswith("(none"): st="No page" if not g else st
    rows.append({"keyword":k,"volume_in":v,"difficulty":d,"target_page":p,"impressions_90d":g["impr"] if g else 0,"clicks_90d":g["clicks"] if g else 0,
      "avg_position":g["pos"] if g else None,"page_google_shows":g["ranking_page"] if g else "","status":st,"priority":pr,"fix":fix})
json.dump({"generated":G["end"],"period":f'{G["start"]} to {G["end"]}',"rows":rows},open("admin/keyword-audit/audit.json","w"),indent=1)
with open("admin/keyword-audit/keyword-audit.csv","w",newline="") as f:
    w=csv.DictWriter(f,rows[0].keys()); w.writeheader(); w.writerows(rows)
for r in rows: print(r["priority"][:4],r["status"][:22].ljust(22),r["avg_position"],r["keyword"])
