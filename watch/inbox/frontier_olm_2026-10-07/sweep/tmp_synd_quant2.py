"""Paced syndication fetch for 4 specific handles whose post IDs I need.
One fetch per 45s, one retry per handle. urllib only, no subprocess."""
import json
import re
import io
import sys
import time
import datetime
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HANDLES = ['BrandonMusicKy', 'Fermonroyh', 'Shiken_Tei', 'ankit_appy']
OUTDIR = r'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-07\sweep\_raw'


def fetch(handle):
    url = f'https://syndication.twitter.com/srv/timeline-profile/screen-name/{handle}'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'### {handle}: FETCH-FAIL {e}')
        return []
    with open(OUTDIR + '\\synd_' + handle + '.html', 'w', encoding='utf-8') as f:
        f.write(body)
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', body, re.S)
    if not m:
        print(f'### {handle}: NO NEXT_DATA ({len(body)} bytes)')
        return []
    d = json.loads(m.group(1))
    out = []

    def walk(o):
        if isinstance(o, dict):
            if 'id_str' in o and ('full_text' in o or 'text' in o):
                out.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(d)
    seen = {}
    for t in out:
        tid = t.get('id_str')
        txt = t.get('full_text') or t.get('text') or ''
        ca = t.get('created_at', '')
        if tid and tid not in seen:
            seen[tid] = (ca, txt.replace('\n', ' '))
    rows = []
    for tid, (ca, txt) in seen.items():
        try:
            ds = datetime.datetime.strptime(ca, '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        except Exception:
            ds = ''
        rows.append((ds, tid, txt))
    rows.sort(reverse=True)
    return rows


for h in HANDLES:
    rows = fetch(h)
    if not rows:
        time.sleep(45)
        rows = fetch(h)
    print(f'### {h}: {len(rows)} unique tweets')
    for ds, tid, txt in rows[:25]:
        print(f'{ds} https://x.com/{h}/status/{tid} :: {txt[:340]}')
    time.sleep(45)
