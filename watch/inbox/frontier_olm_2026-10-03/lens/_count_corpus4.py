import json, collections

p = 'catalog/catalog.jsonl'
lib = collections.Counter()
memc = collections.Counter()
oral = collections.Counter()
pd = collections.Counter()

with open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        r = json.loads(line)
        path = r.get('path', '').replace('\\', '/')
        parts = path.split('/')
        if parts[:3] == ['local_sovereign_agent', 'corpus', 'library'] and len(parts) > 3:
            lib[parts[3]] += 1
        if parts[:3] == ['local_sovereign_agent', 'memory', 'corpus'] and len(parts) > 3:
            memc[parts[3]] += 1
        if parts[:3] == ['local_sovereign_agent', 'corpus', 'oral_history'] and len(parts) > 4:
            oral[parts[4] if parts[3] in ('seat_pools', 'nacho_archaeology') else parts[3]] += 1
        for i, seg in enumerate(parts):
            if seg.startswith('pd_'):
                pd[seg] += 1
                break

print('LIBRARY_PROJECTS total', sum(lib.values()))
for k, v in lib.most_common(30):
    print('  ', k, v)
print('MEM_CORPUS_PROJECTS total', sum(memc.values()))
for k, v in memc.most_common(20):
    print('  ', k, v)
print('ORAL split total', sum(oral.values()))
for k, v in oral.most_common(10):
    print('  ', k, v)
print('PD', sum(pd.values()), pd.most_common(12))
