import json, collections, io

base = r'C:\Users\foste\Documents\projects\local_sovereign_agent\catalog'

# 1) second-level under local_sovereign_agent/ in catalog.jsonl
p = base + r'\catalog.jsonl'
lsa2 = collections.Counter()
with io.open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        path = (r.get('path') or '').replace('\\', '/')
        parts = path.split('/')
        if len(parts) > 1 and parts[0] == 'local_sovereign_agent':
            lsa2[parts[1]] += 1

print('local_sovereign_agent second-level (top 50):')
for k, v in lsa2.most_common(50):
    print(' ', k, v)

# 2) tags.jsonl: sample structure + top tags
tp = base + r'\tags.jsonl'
n = 0
tagcounter = collections.Counter()
sample_fields = None
sample = None
with io.open(tp, encoding='utf-8', errors='replace') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        n += 1
        if sample_fields is None:
            sample_fields = sorted(r.keys())
            sample = r
        for t in (r.get('tags') or []):
            if isinstance(t, str):
                tagcounter[t] += 1
            elif isinstance(t, dict):
                tagcounter[str(t.get('tag') or t.get('name'))] += 1

print('tags rows', n)
print('tags fields', sample_fields)
print('sample', json.dumps(sample, ensure_ascii=False)[:300])
print('top tags (top 60):')
for k, v in tagcounter.most_common(60):
    print(' ', k, v)
