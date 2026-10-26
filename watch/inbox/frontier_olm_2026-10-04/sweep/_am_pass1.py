import json, time, urllib.request, urllib.parse, os, sys

UA = {'User-Agent': 'mag-frontier-sweep/1.0 (agent-memory area, hn door)'}
SINCE = 1788480000  # 2026-09-04T00:00:00Z, the ask's 30-day window
OUT = os.path.dirname(os.path.abspath(__file__))

def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

# (endpoint, query, use_date_filter, hits_per_page)
lanes = [
    ('search_by_date', 'agent memory', True, 30),
    ('search_by_date', 'LLM memory', True, 20),
    ('search_by_date', 'agent memory', False, 0),  # placeholder replaced below
]
lanes = [
    ('search_by_date', 'agent memory', True, 30),
    ('search_by_date', 'LLM memory', True, 20),
    ('search', 'sleep-time compute', False, 15),
    ('search_by_date', 'sleep-time', True, 15),
    ('search_by_date', 'memory consolidation', True, 20),
    ('search', 'MemGPT', False, 10),
    ('search_by_date', 'Letta', True, 15),
    ('search', 'memory reinforcement learning', False, 15),
    ('search_by_date', 'MemAgent', True, 10),
    ('search', 'context rot', False, 10),
    ('search_by_date', 'context rot', True, 10),
    ('search', 'long context retrieval', False, 15),
    ('search_by_date', 'long-term memory', True, 20),
    ('search_by_date', 'memory layer', True, 15),
    ('search_by_date', 'knowledge graph', True, 20),
    ('search_by_date', 'reflection agent', True, 10),
    ('search_by_date', 'warm start', True, 10),
    ('search_by_date', 'compaction', True, 15),
    ('search', 'memory benchmark', False, 10),
    ('search_by_date', 'conversation memory', True, 15),
]

seen = {}
negatives = []
for ep, q, dated, hpp in lanes:
    url = f'https://hn.algolia.com/api/v1/{ep}?query={urllib.parse.quote(q)}&tags=story&hitsPerPage={hpp}'
    if dated:
        url += f'&numericFilters=created_at_i%3E{SINCE}'
    try:
        res = get(url)
    except Exception as e:
        negatives.append((ep, q, 'ERR ' + str(e)))
        continue
    hits = res.get('hits', [])
    if not hits:
        negatives.append((ep, q, 'nbHits 0'))
    for h in hits:
        oid = h.get('objectID')
        if not oid:
            continue
        rec = seen.get(oid)
        lane_tag = f'{ep}:{q}' + ('[30d]' if dated else '')
        if rec is None:
            seen[oid] = {
                'id': oid,
                'title': h.get('title') or '',
                'url': h.get('url') or '',
                'points': h.get('points') or 0,
                'comments': h.get('num_comments') or 0,
                'created': h.get('created_at') or '',
                'lanes': [lane_tag],
            }
        else:
            rec['lanes'].append(lane_tag)

rows = list(seen.values())
# in-window = last 30 days per the ask
inwindow = [r for r in rows if r['created'] >= '2026-09-04']
inwindow.sort(key=lambda r: r['created'], reverse=True)
older = [r for r in rows if r['created'] < '2026-09-04']

with open(os.path.join(OUT, '_am_p1_hits.json'), 'w', encoding='utf-8') as f:
    json.dump({'in_window': inwindow, 'older': older, 'negatives': negatives}, f, ensure_ascii=False, indent=1)

print(f'unique stories total: {len(rows)}; in-window(>=2026-09-04): {len(inwindow)}; older: {len(older)}')
print('--- negatives ---')
for n in negatives:
    print(n)
print('--- IN WINDOW (newest first) ---')
for r in inwindow:
    t = r['title'][:95]
    print(f"{r['created'][:10]} {r['id']:>9} {r['points']:>4}p {r['comments']:>4}c | {t}")
print('--- OLDER (relevance catches, for RQ-lineage reads) ---')
for r in sorted(older, key=lambda r: r['points'], reverse=True)[:25]:
    t = r['title'][:95]
    print(f"{r['created'][:10]} {r['id']:>9} {r['points']:>4}p {r['comments']:>4}c | {t}")
