"""Fetch Twitter syndication timelines for quant-relevant handles, parse embedded
tweets, print rows in the 30-day window 2026-09-07..2026-10-07 that match quant
keywords. Door + parser shape reused from day-6 sweep (_raw/bing/parse_synd.py).
No subprocess spawns; urllib only (so the CREATE_NO_WINDOW law is moot here).
"""
import json
import re
import io
import sys
import time
import datetime
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HANDLES = [
    'danielhanchen', 'reach_vb', 'rohanpaul_ai',
    'HuggingFace', 'DeepSeek_AI', 'lmsysorg',
]
KEY = re.compile(
    r'quant|Q4_K|Q8_0|Q3_K|Q2_K|Q6_K|IQ[0-9]|KLD|imatrix|importance matrix|'
    r'KV cache|KV-cache|kv_quant|Vulkan|tok/s|gguf|GGUF|bits?/weight|awq|AWQ|GPTQ|'
    r'FP8|fp8|INT4|int4|4-bit|8-bit|2-bit|bitnet|ternary|compress', re.I)
WINDOW = (datetime.date(2026, 9, 7), datetime.date(2026, 10, 8))

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
    path = OUTDIR + '\\synd_' + handle + '.html'
    with open(path, 'w', encoding='utf-8') as f:
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


total = 0
for h in HANDLES:
    time.sleep(20)
    rows = fetch(h)
    if not rows:
        time.sleep(30)
        rows = fetch(h)
    inwin = [r for r in rows if r[0] and WINDOW[0].isoformat() <= r[0] <= WINDOW[1].isoformat()]
    matched = [r for r in inwin if KEY.search(r[2])]
    print(f'### {h}: {len(rows)} unique tweets, {len(inwin)} in-window, {len(matched)} quant-matched')
    for ds, tid, txt in matched:
        print(f'{ds} https://x.com/{h}/status/{tid} :: {txt[:360]}')
    total += len(matched)
    for ds, tid, txt in inwin[:5]:
        print(f'  (inwin-sample) {ds} {txt[:120]}')
print(f'TOTAL quant-matched rows: {total}')
