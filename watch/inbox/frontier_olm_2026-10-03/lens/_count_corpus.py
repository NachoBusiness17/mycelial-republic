import json, collections

p = 'catalog/catalog.jsonl'
n = 0
bad = 0
zone = collections.Counter()
top = collections.Counter()
keys = collections.Counter()
ext = collections.Counter()
corpus_sub = collections.Counter()
library_sub = collections.Counter()
domain_hits = collections.Counter()

DOMAINS = {
    'agents/orchestration': ['agent', 'orchestr', 'swarm', 'ractor', 'fleet', 'lane'],
    'rag/memory/retrieval': ['rag', 'retriev', 'embedding', 'vector', 'memory', 'fts', 'index'],
    'local-llm/inference': ['ollama', 'llama', 'gemma', 'quantiz', 'inference', 'model'],
    'verkle/proofs/crypto': ['verkle', 'merkle', 'ed25519', 'proof', 'seal', 'sha256'],
    'games/dnd/sim': ['dungeon', 'game', 'dd_', 'brawl', 'salon', 'town', 'river', 'hydrology'],
    'economics/burn/cost': ['burn', 'cost', 'budget', 'credit', 'usage', 'ledger'],
    'prompt/persuasion': ['persua', 'cialdini', 'prompt', 'claritas'],
    'workflows/gates': ['workflow', 'gate', 'ratchet', 'lint'],
    'sensing/web/frontier': ['frontier', 'sensing', 'digest', 'steal'],
}

with open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        n += 1
        try:
            r = json.loads(line)
        except Exception:
            bad += 1
            continue
        for k in r:
            keys[k] += 1
        zone[r.get('zone', '?')] += 1
        ext[r.get('ext', '')] += 1
        path = r.get('path', '').replace('\\', '/')
        parts = path.split('/')
        top[parts[0] if len(parts) > 1 else '(root)'] += 1
        if parts[0] == 'corpus' and len(parts) > 1:
            corpus_sub[parts[1] if len(parts) > 2 else '(file)'] += 1
        if parts[0] == 'library' and len(parts) > 1:
            library_sub[parts[1] if len(parts) > 2 else '(file)'] += 1
        lp = path.lower()
        for d, kws in DOMAINS.items():
            if any(k in lp for k in kws):
                domain_hits[d] += 1

print('rows', n, 'bad_json', bad)
print('keys', dict(keys))
print('zones', zone.most_common())
print('TOP_DIRS')
for k, v in top.most_common(40):
    print(' ', k, v)
print('CORPUS_SUB')
for k, v in corpus_sub.most_common(30):
    print(' ', k, v)
print('LIBRARY_SUB')
for k, v in library_sub.most_common(20):
    print(' ', k, v)
print('DOMAIN_PATH_HITS')
for k, v in domain_hits.most_common():
    print(' ', k, v)
print('EXT_TOP', ext.most_common(15))
