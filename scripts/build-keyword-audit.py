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
("event management company","6600","25","/blog/event-management-company-india/","Critical","No Google impressions at all. Add 'Event Management Company' to the H1 and title; link to it from the homepage and main menu (only 8 internal links today); build a service page, since a blog list rarely ranks for service searches."),
("event planners in delhi","2400","28","/event-planners-delhi/","Critical","No impressions. Add a 2–3 sentence answer at the top, a Delhi address and LocalBusiness details, real event photos, and links from the homepage and footer."),
("wedding planner delhi","1900","14","(none)","High","No page exists. Build a /wedding-planner-delhi/ page with a direct answer, packages and photos."),
("event management company in delhi","1300","31","(none — /event-planners-delhi/ partly)","Critical","No dedicated page. Build an /event-management-company-delhi/ service page that covers Delhi NCR, and point the 'Delhi NCR' searches to it."),
("event management company in gurgaon","880","26","/event-management-gurgaon/","High","No impressions. Change the URL wording or title to start with 'Event Management Company in Gurgaon', add real Gurgaon events and the Gurgaon Durga Puja stalls, and link from Durga Puja pages."),
("corporate event management company","880","37","/blog/corporate-event-management-india/","High","No impressions. Link to it from the homepage, the services page and the menu (8 internal links today)."),
("best event management company in india","260","15","/blog/event-management-company-india/","High","Recently rewritten. Request indexing in Search Console and add links from city pages."),
("event management company in delhi ncr","70","0","(none)","High","Cover on the new Delhi event management page; add 'Delhi NCR' to the H1."),
("best event management company in delhi ncr","10","0","(none)","Medium","Cover on the new Delhi page with an answer-first 'Best event management company in Delhi NCR' section and comparison table."),
("celebrity management company","210","10","/celebrity-management-company/","High","Only 11 internal links, and the homepage title targets the same phrase. Give the homepage a 'celebrity booking agency' title and link this page sitewide."),
("book celebrity","140","29","/celebrity-booking-india/","High","Google shows /pan-india-celebrity-booking/ instead, at position 12. Use /celebrity-booking-india/ as the main page: H1 'Book a Celebrity in India', an answer-first intro, and FAQ."),
("celebrity booking","140","29","/celebrity-booking-india/","High","Wrong page ranks (/pan-india-celebrity-booking/, position 7.4). Change the H1 'Celebrity Booking in India.' to a descriptive one, add a fee table, and point pan-india internal links to it."),
("celebrity booking agency","110","0","/celebrity-booking-india/","Medium","The homepage ranks at position 3. Keep it, and add an 'agency' FAQ to /celebrity-booking-india/."),
("celebrity booking india","20","0","/celebrity-booking-india/","High","No impressions, even though this page has 177 internal links. Its title and H1 are too short; rewrite them and add a 'How celebrity booking works in India' answer and FAQ schema."),
("book celebrity for wedding",None,None,"/book-celebrity-for-wedding/","Critical","Three pages compete (Delhi page position 10, wedding page position 26, Bollywood page position 38) across 636 impressions. Make /book-celebrity-for-wedding/ the main page: link to it sitewide (only 2 internal links now) and remove wedding wording from the other two."),
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
