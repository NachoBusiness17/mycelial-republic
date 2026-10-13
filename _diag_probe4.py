import json, re

sid = 'autonomous-auto-fkb-183618'
chain_path = 'memory/biography/verkle_chain.jsonl'

rows = []
with open(chain_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        # Check if session id appears in the row
        row_str = json.dumps(obj)
        if sid in row_str:
            rows.append(obj)

out = []
out.append(f'Total rows matching session {sid}: {len(rows)}')
out.append('')

for i, row in enumerate(rows):
    out.append(f'=== ROW {i} ===')
    out.append(json.dumps(row, indent=2, default=str))
    out.append('')

with open('_diag_out.txt', 'w') as f:
    f.write('\n'.join(out))