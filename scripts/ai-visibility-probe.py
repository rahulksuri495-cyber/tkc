#!/usr/bin/env python3
"""Monthly AI/LLM visibility probe. Asks AI engines buyer questions and records
whether TKC Talent is mentioned / cited and which competitors appear.
Appends one summary line per run to admin/ai-visibility/history.jsonl and
writes the full answers to admin/ai-visibility/runs/<YYYY-MM>.json.
Engines: Lovable AI gateway models (answers from model knowledge, no live web),
plus Perplexity live search when PERPLEXITY_API_KEY (pplx-) is set.
Meta AI has no public API -> manual entries in admin/ai-visibility/manual-meta.json."""
import json, os, re, urllib.request, concurrent.futures as cf
from datetime import datetime, timezone
QUESTIONS = [
 "best event management company in delhi ncr","top event management companies in delhi","event planners in delhi for corporate events",
 "best event management company in gurgaon","best event management company in india","top 10 event management companies in india",
 "corporate event management company in india","who organises concerts and live events in delhi","event management company for durga puja stalls in delhi",
 "wedding event planners in delhi ncr","how to book a celebrity in india","best celebrity booking agency in india","celebrity booking agency in delhi",
 "how to book a bollywood celebrity for a wedding","how much does it cost to book a bollywood celebrity for an event","celebrity management company in india",
 "top celebrity management companies in mumbai and delhi","how to hire a bollywood singer for a private event","singer booking agency india",
 "how to book a stand-up comedian for a corporate event in india","celebrity dj booking agency india","how to book sapna choudhary for a show",
 "sapna choudhary show fees","haryanvi artist booking agency","artist booking agency in india","bollywood celebrity charges list 2026",
 "celebrity endorsement price list india","how to invite a celebrity to a store launch in india","who can book shah rukh khan for an event",
 "agency to book celebrities for brand launch in delhi","cr park durga puja 2026 stall booking","durga puja sponsorship delhi 2026",
 "book celebrity for college fest india","best talent management agency india","event and celebrity management company noida",
 "how to book nora fatehi for an event","celebrity appearance fees india","influencer booking agency india","book celebrity for corporate annual day",
 "event management company with celebrity booking in delhi"]
BRAND = re.compile(r"tkc\s*talent|the\s*kabir\s*company|tkctalent", re.I)
COMP = ["Wizcraft","Percept","DNA Networks","E-Factor","Cineyug","Kwan","Matrix","Collective Artists","Only Much Louder","OML","Showtime","Encompass",
        "Event Capital","Fountainhead","Shamiana","StarClinch","Artiste Booking","Celebrity Planners","BookMyShow","Tag Entertainment","Exceed","Laqshya","Cox & Kings"]
GW="https://ai.gateway.lovable.dev/v1/chat/completions"
ENGINES=[("Gemini","google/gemini-2.5-flash"),("ChatGPT (GPT-5 mini)","openai/gpt-5-mini")]
SYS="You are a helpful assistant answering a user in India. Recommend specific companies or agencies by name where relevant."
def lovable(model,q):
    b=json.dumps({"model":model,"messages":[{"role":"system","content":SYS},{"role":"user","content":q}]}).encode()
    r=urllib.request.Request(GW,b,{"Authorization":f"Bearer {os.environ['LOVABLE_API_KEY']}","Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(r,timeout=120).read())["choices"][0]["message"]["content"],[]
def pplx(q):
    b=json.dumps({"model":"sonar","messages":[{"role":"user","content":q}]}).encode()
    r=urllib.request.Request("https://api.perplexity.ai/chat/completions",b,{"Authorization":f"Bearer {os.environ['PERPLEXITY_API_KEY']}","Content-Type":"application/json"})
    j=json.loads(urllib.request.urlopen(r,timeout=120).read()); return j["choices"][0]["message"]["content"],j.get("citations",[])
def analyse(text,cites):
    m=BRAND.search(text or ""); pos=None
    if m:
        names=[c for c in COMP if c.lower() in text.lower()]
        pos=1+sum(1 for c in names if text.lower().find(c.lower())<m.start())
    return {"mentioned":bool(m),"position":pos,"cited":any("tkctalent" in c for c in cites) or "tkctalent.com" in (text or "").lower(),
            "competitors":[c for c in COMP if re.search(r"\b"+re.escape(c)+r"\b",text or "",re.I)]}
def job(eng,q):
    try:
        t,c = pplx(q) if eng=="Perplexity" else lovable(dict(ENGINES)[eng],q)
        return {"engine":eng,"q":q,"answer":t,"citations":c,**analyse(t,c)}
    except Exception as e: return {"engine":eng,"q":q,"error":str(e)[:200]}
engs=[e for e,_ in ENGINES]+(["Perplexity"] if os.environ.get("PERPLEXITY_API_KEY","").startswith("pplx-") else [])
with cf.ThreadPoolExecutor(8) as ex: res=list(ex.map(lambda a:job(*a),[(e,q) for e in engs for q in QUESTIONS]))
month=datetime.now(timezone.utc).strftime("%Y-%m"); os.makedirs("admin/ai-visibility/runs",exist_ok=True)
json.dump(res,open(f"admin/ai-visibility/runs/{month}.json","w"),indent=1,ensure_ascii=False)
summ={"month":month,"at":datetime.now(timezone.utc).isoformat(timespec="seconds"),"questions":len(QUESTIONS),"engines":{}}
for e in engs:
    rs=[r for r in res if r["engine"]==e and "error" not in r]; comp={}
    for r in rs:
        for c in r["competitors"]: comp[c]=comp.get(c,0)+1
    summ["engines"][e]={"answered":len(rs),"mentioned":sum(r["mentioned"] for r in rs),"cited":sum(r["cited"] for r in rs),
        "mention_rate":round(100*sum(r["mentioned"] for r in rs)/max(1,len(rs)),1),"top_competitors":dict(sorted(comp.items(),key=lambda x:-x[1])[:8]),
        "mentioned_for":[r["q"] for r in rs if r["mentioned"]]}
mf="admin/ai-visibility/manual-meta.json"
if os.path.exists(mf):
    m=[x for x in json.load(open(mf)) if x.get("month")==month]
    if m: summ["engines"]["Meta AI (manual)"]={"answered":len(m),"mentioned":sum(x["mentioned"] for x in m),"cited":0,"mention_rate":round(100*sum(x["mentioned"] for x in m)/len(m),1),"top_competitors":{},"mentioned_for":[x["q"] for x in m if x["mentioned"]]}
hist="admin/ai-visibility/history.jsonl"
lines=[l for l in (open(hist).read().splitlines() if os.path.exists(hist) else []) if json.loads(l)["month"]!=month]
open(hist,"w").write("\n".join(lines+[json.dumps(summ,ensure_ascii=False)])+"\n")
print(json.dumps(summ,indent=1))
