import json, collections

p = 'catalog/catalog.jsonl'
c = collections.Counter()
b = collections.Counter()
intake_n = 0
intake_bytes = 0
intake_wi = 0
with open(p, encoding='utf-8', errors='replace') as f:
    for line in f:
        r = json.loads(line)
        path = r.get('path', '').replace('\\', '/')
        parts = path.split('/')
        n = r.get('bytes', 0) or 0
        if r.get('zone') == 'intake':
            intake_n += 1
            intake_bytes += n
            if 'watch/inbox' in path or 'watch\\inbox' in path:
                intake_wi += 1
        if parts[:2] == ['local_sovereign_agent', 'agents'] or (len(parts) == 1 and parts[0] == 'agents'):
            c['agents'] += 1; b['agents'] += n
        if len(parts) > 1 and parts[1] == 'mine':
            c['mine'] += 1; b['mine'] += n
        if len(parts) > 2 and parts[1] == 'memory' and parts[2] == 'ghost':
            c['ghost'] += 1; b['ghost'] += n
        if len(parts) > 1 and parts[1] == 'logs':
            c['logs'] += 1; b['logs'] += n
        if len(parts) > 2 and parts[1] == 'memory' and parts[2] == 'agent_state':
            c['agent_state'] += 1; b['agent_state'] += n
        if parts[:3] == ['local_sovereign_agent', 'corpus', 'library'] and len(parts) > 3 and parts[3] == 'openai-cookbook':
            b['openai_cookbook'] += n
        if parts[:2] == ['local_sovereign_agent', 'corpus'] and len(parts) > 2 and parts[2] == 'oral_history':
            b['oral'] += n
        if parts[:3] == ['local_sovereign_agent', 'corpus', 'library']:
            b['library'] += n
        if parts[0] == 'azerothcore-wow':
            b['az'] += n
        if parts[0] == 'tortoise-wow':
            b['tort'] += n

for k in ('agents', 'mine', 'ghost', 'logs', 'agent_state'):
    print(k, c[k], 'bytes', b[k])
for k in ('library', 'openai_cookbook', 'oral', 'az', 'tort'):
    print('MB', k, round(b[k] / 1000000, 1))
print('zone intake', intake_n, 'MB', round(intake_bytes / 1000000, 1), 'intake-with-watch/inbox-path', intake_wi)
