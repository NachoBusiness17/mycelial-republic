import json, collections

p = 'catalog/catalog.jsonl'
lib2 = collections.Counter()
lib_total = 0
arxiv_days = collections.Counter()
mem_corpus = collections.Counter()
mem_corpus_total = 0
oral = collections.Counter()
oral_total = 0
bio = collections.Counter()
res_packs = collections.Counter()
res_total = 0
dfhack = 0
pd = collections.Counter()
misc = collections.Counter()


def cut(path, n):
    parts = path.split('/')
    return '/'.join(parts[:n]) if len(parts) >= n else path


with open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        r = json.loads(line)
        path = r.get('path', '').replace('\\', '/')
        parts = path.split('/')
        lp = path.lower()
        if parts[:3] == ['local_sovereign_agent', 'corpus', 'library']:
            lib_total += 1
            lib2[cut(path, 5)] += 1
        elif parts[:2] == ['local_sovereign_agent', 'corpus'] and len(parts) > 2 and parts[2].startswith('oral_history'):
            oral_total += 1
            oral[cut(path, 5)] += 1
        elif parts[:2] == ['local_sovereign_agent', 'corpus'] and len(parts) > 2 and 'dfhack' in parts[2].lower():
            dfhack += 1
        elif lp.startswith('local_sovereign_agent/state/arxiv'):
            arxiv_days[cut(path, 4)] += 1
        elif parts[:2] == ['local_sovereign_agent', 'memory'] and len(parts) > 2 and parts[2] == 'corpus':
            mem_corpus_total += 1
            mem_corpus[cut(path, 5)] += 1
        elif parts[:2] == ['local_sovereign_agent', 'memory'] and len(parts) > 2 and parts[2].startswith('biography'):
            bio[parts[2]] += 1
        elif parts[:3] == ['local_sovereign_agent', 'memory', 'research_packs']:
            res_total += 1
            res_packs[cut(path, 5)] += 1
        elif len(parts) > 1 and parts[1].startswith('pd_'):
            pd[parts[1]] += 1

print('LIB_TOTAL', lib_total)
for k, v in lib2.most_common(15):
    print('  LIB', k, v)
print('ORAL_TOTAL', oral_total)
for k, v in oral.most_common(8):
    print('  ORAL', k, v)
print('DFHACK', dfhack)
print('ARXIV_TOTAL', sum(arxiv_days.values()), 'days', len(arxiv_days))
for k, v in arxiv_days.most_common(5):
    print('  ARXIV', k, v)
print('MEM_CORPUS_TOTAL', mem_corpus_total)
for k, v in mem_corpus.most_common(14):
    print('  MEMCORPUS', k, v)
print('BIO', dict(bio))
print('RES_PACKS_TOTAL', res_total)
for k, v in res_packs.most_common(5):
    print('  RES', k, v)
print('PD', pd.most_common(12))
