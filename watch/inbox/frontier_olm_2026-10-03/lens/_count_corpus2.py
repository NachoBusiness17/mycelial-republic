import json, collections

p = 'catalog/catalog.jsonl'
shelf = collections.Counter()
research_sub = collections.Counter()
margin_sub = collections.Counter()
wow = collections.Counter()
exts = collections.Counter()

SHELVES = ['oral_history', 'tartaria', 'telegram', 'game_estate', 'frontier_thinking',
           'canon', 'ractor_ribs', 'watch/inbox', 'docs/ref', 'handoff']

with open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        r = json.loads(line)
        path = r.get('path', '').replace('\\', '/').lower()
        parts = path.split('/')
        for s in SHELVES:
            if s in path:
                shelf[s] += 1
        if parts and parts[0] == 'research' and len(parts) > 1:
            research_sub[parts[1] if len(parts) > 2 else '(file)'] += 1
        if parts and parts[0] == 'the_margin_lean' and len(parts) > 1:
            margin_sub[parts[1] if len(parts) > 2 else '(file)'] += 1
        if parts and parts[0] in ('azerothcore-wow', 'vmangos-core', 'tortoise-wow'):
            wow[parts[0]] += 1
        if 'library' in path and len(parts) > 2 and parts[0] == 'library':
            exts[r.get('ext', '')] += 1

print('SHELF_PATH_CONTAINS')
for k, v in shelf.most_common():
    print(' ', k, v)
print('RESEARCH_SUB (top 25)')
for k, v in research_sub.most_common(25):
    print(' ', k, v)
print('MARGIN_SUB (top 10)')
for k, v in margin_sub.most_common(10):
    print(' ', k, v)
print('WOW_CORES', dict(wow))
