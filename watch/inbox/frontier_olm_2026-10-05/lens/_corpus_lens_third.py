import json, collections, io

p = r'C:\Users\foste\Documents\projects\local_sovereign_agent\catalog\catalog.jsonl'
third = {k: collections.Counter() for k in (
    'local_sovereign_agent/corpus',
    'local_sovereign_agent/memory',
    'local_sovereign_agent/mine',
    'local_sovereign_agent/agents',
    'local_sovereign_agent/watch',
    'local_sovereign_agent/docs',
    'local_sovereign_agent/research',
)}
lib_hits = collections.Counter()
oral = 0
canon = 0
n = 0
with io.open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        n += 1
        path = (r.get('path') or '').replace('\\', '/')
        parts = path.split('/')
        if parts[:2] == ['local_sovereign_agent', 'library'] or '/library/' in path:
            lib_hits['/'.join(parts[:5])] += 1
        low = path.lower()
        if '/oral_history' in low or low.startswith('oral_history'):
            oral += 1
        if '/canon/' in low:
            canon += 1
        prefix = '/'.join(parts[:2])
        if prefix in third and len(parts) > 2:
            third[prefix][parts[2]] += 1

print('rows total', n)
print('library-ish paths (top 15):')
for k, v in lib_hits.most_common(15):
    print(' ', k, v)
print('oral_history rows', oral)
print('rows with /canon/ in path', canon)
for root, c in third.items():
    print('---', root)
    for k, v in c.most_common(25):
        print(' ', k, v)
