#!/usr/bin/env python3
"""Sync news-feed.json from the newsroom bundle (assets/main-*.js).
Run after updating press articles in the bundle:
    python3 scripts/sync-news-feed.py
"""
import re, json, glob, sys, os
from datetime import date
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bundles = sorted(glob.glob('assets/main-*.js'))
if not bundles: sys.exit('no main-*.js bundle found')
js = open(bundles[-1]).read()
items=[]; i=0
while True:
    idx = js.find('{publisher:"', i)
    if idx<0: break
    depth=0; j=idx
    while j<len(js):
        c=js[j]
        if c=='{': depth+=1
        elif c=='}':
            depth-=1
            if depth==0: break
        elif c=='"':
            j+=1
            while j<len(js) and js[j]!='"':
                if js[j]=='\\': j+=2; continue
                j+=1
        j+=1
    obj=js[idx:j+1]; i=j+1
    def grab(k):
        m=re.search(rf'{k}:"((?:[^"\\\\]|\\\\.)*)"', obj)
        return m.group(1) if m else ''
    items.append({'publisher':grab('publisher'),'headline':grab('headline'),'url':grab('url'),'date':grab('date'),'body':grab('body')})

def cat(it):
    h=(it['headline']+' '+it['body']).lower()
    ev=['cafe underpass','moonliit','trade fair','bargain fest','mtv','runway','audition','nimbus','sunil grover takes','bollywood night','nightlife','d2r','date to remember']
    if any(k in h for k in ev): return 'Events'
    rc=['leading entrepreneurs','thought leaders','top 10','transforming the business','innovation to impact','recognises','recognizes','spotlights','syndicates','national recognition','new business era','growing pr footprint','impact list']
    if any(k in h for k in rc): return 'Recognition'
    return 'Press'
for it in items: it['category']=cat(it)
out={'updated':date.today().isoformat(),'source':'auto-synced from newsroom bundle','items':items}
json.dump(out, open('news-feed.json','w'), indent=2, ensure_ascii=False)
print(f'synced {len(items)} items -> news-feed.json')
