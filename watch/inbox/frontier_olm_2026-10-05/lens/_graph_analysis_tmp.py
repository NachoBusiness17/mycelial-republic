import json, os
from collections import Counter, defaultdict

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

with open(os.path.join(ROOT, 'memory', 'knowledge_graph.json'), encoding='utf-8') as f:
    g = json.load(f)
nodes = g['nodes']; edges = g['edges']
by_id = {n['id']: n for n in nodes}

def kind_of(nid):
    n = by_id.get(nid)
    return n['kind'] if n else '<MISSING>'

print('=== rel -> (from kind, to kind) counts ===')
rc = Counter((e['rel'], kind_of(e['from']), kind_of(e['to'])) for e in edges)
for (r, fk, tk), c in rc.most_common():
    print(f'{r}: {fk} -> {tk} = {c}')

missing_from = sorted({e['from'] for e in edges if e['from'] not in by_id})
missing_to = sorted({e['to'] for e in edges if e['to'] not in by_id})
print()
print('dangling from-ids:', len(missing_from), missing_from[:5])
print('dangling to-ids:', len(missing_to), missing_to[:8])

deg = defaultdict(int)
for e in edges:
    deg[e['from']] += 1
    deg[e['to']] += 1

print()
print('=== skills_pack edges breakdown ===')
sp = 'module:skills_pack'
inc = [e for e in edges if e['to'] == sp]
out = [e for e in edges if e['from'] == sp]
print('in:', len(inc), dict(Counter(e['rel'] for e in inc)))
print('out:', len(out), dict(Counter(e['rel'] for e in out)))

print()
print('=== module isolation by source directory (top 15 by isolated) ===')
dirs = defaultdict(lambda: [0, 0])
for n in nodes:
    if n['kind'] != 'module':
        continue
    d = os.path.relpath(os.path.dirname(n['source']), ROOT)
    dirs[d][0 if deg[n['id']] > 0 else 1] += 1
rows = sorted(dirs.items(), key=lambda kv: -kv[1][1])[:15]
for d, (conn, iso) in rows:
    print(f'{d}: {iso} isolated / {conn + iso} total')

print()
print('=== case_law maps_to targets (top 5) ===')
print(Counter(by_id[e['to']]['label'] for e in edges if e['rel'] == 'maps_to').most_common(5))
print()
print('=== already_inside endpoints (from kind -> to kind) ===')
print(Counter((kind_of(e['from']), kind_of(e['to'])) for e in edges if e['rel'] == 'already_inside'))

print()
print('=== landscape nodes and their degrees ===')
for n in nodes:
    if n['kind'] == 'landscape':
        print(n['id'], '| deg', deg[n['id']], '|', n['label'])

print()
print('=== top Law invariant ===')
for nid, d in sorted(deg.items(), key=lambda x: -x[1]):
    n = by_id.get(nid)
    if n and n['label'].startswith('Law'):
        print(repr(nid)[:130], 'deg', d)
        print('summary:', str(n.get('summary', ''))[:220])
        break
