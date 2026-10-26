import json, collections, io

base = r'C:\Users\foste\Documents\projects\local_sovereign_agent\catalog'
lib2 = collections.Counter()
mine_ext = collections.Counter()
mine_title = collections.Counter()
memcorpus2 = collections.Counter()
packs = []
n_mine = 0
with io.open(base + r'\catalog.jsonl', encoding='utf-8', errors='replace') as f:
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
        if len(parts) > 3 and parts[:3] == ['local_sovereign_agent', 'corpus', 'library']:
            lib2[parts[3]] += 1
        if len(parts) > 3 and parts[:3] == ['local_sovereign_agent', 'mine', 'raw']:
            n_mine += 1
            mine_ext[r.get('ext')] += 1
            t = (r.get('title') or '').lower()
            for kw in ('arxiv', 'paper', 'quantum', 'biology', 'protein', 'kubernetes', 'k8s',
                       'hydrop', 'geolog', 'verkle', 'agent', 'llm', 'inference', 'mcp',
                       'rl ', 'reinforcement', 'transformer', 'embedding', 'gpu', 'kernel',
                       'training', 'dataset', 'benchmark', 'eval'):
                if kw in t:
                    mine_title[kw] += 1
        if len(parts) > 3 and parts[:3] == ['local_sovereign_agent', 'memory', 'corpus']:
            memcorpus2[parts[3]] += 1
        if len(parts) > 3 and parts[:3] == ['local_sovereign_agent', 'memory', 'research_packs']:
            packs.append(r.get('title') or parts[-1])

print('corpus/library second level (top 30):')
for k, v in lib2.most_common(30):
    print(' ', k, v)
print('mine/raw rows', n_mine)
print('mine/raw exts:', dict(mine_ext.most_common(8)))
print('mine/raw title keyword hits:', dict(mine_title.most_common(25)))
print('memory/corpus second level (top 15):')
for k, v in memcorpus2.most_common(15):
    print(' ', k, v)
print('research_packs rows', len(packs))
for t in packs[:10]:
    print(' pack:', t[:110])

# verify manifest kind_counts against tags.jsonl myself
kc = collections.Counter()
with io.open(base + r'\tags.jsonl', encoding='utf-8', errors='replace') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        kc[r.get('kind')] += 1
print('kind counts (mine, from tags.jsonl):', dict(kc.most_common()))
