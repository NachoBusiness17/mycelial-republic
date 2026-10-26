import json, collections, io

p = r'C:\Users\foste\Documents\projects\local_sovereign_agent\catalog\catalog.jsonl'
n = 0
top = collections.Counter()
second = collections.Counter()
zone = collections.Counter()
ext = collections.Counter()
fields = set()

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
        fields.update(r.keys())
        path = (r.get('path') or '').replace('\\', '/')
        top[path.split('/')[0]] += 1
        zone[r.get('zone')] += 1
        ext[r.get('ext')] += 1

# second-level for the biggest research-ish roots
roots = ('corpus', 'library', 'watch/inbox', 'docs', 'handoff', 'state')
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
        if parts and parts[0] in roots and len(parts) > 1:
            second['/'.join(parts[:2])] += 1

print('rows', n)
print('fields', sorted(fields))
print('top-level path segments:')
for k, v in top.most_common(30):
    print(' ', k, v)
print('zones:')
for k, v in zone.most_common(12):
    print(' ', k, v)
print('exts:')
for k, v in ext.most_common(15):
    print(' ', k, v)
print('second-level for big roots (top 60):')
for k, v in second.most_common(60):
    print(' ', k, v)
