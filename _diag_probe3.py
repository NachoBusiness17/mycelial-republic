import json

sid = 'session:autonomous-auto-fkb-183618'
out = []

with open('memory/derived/derived_dag_index.json') as f:
    data = json.load(f)

node = data['nodes'].get(sid)
if node:
    out.append(json.dumps(node, indent=2))
else:
    out.append('NOT FOUND')

with open('_diag_out.txt', 'w') as f:
    f.write('\n'.join(out))