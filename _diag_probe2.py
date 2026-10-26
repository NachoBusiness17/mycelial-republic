import json

sid = 'autonomous-auto-fkb-183618'
out = []

with open('memory/derived/derived_dag_index.json') as f:
    data = json.load(f)

# Search each top-level key for the session
for key in ['nodes', 'built', 'children', 'identity_merges', 'parents']:
    val = data.get(key)
    if val is None:
        continue
    t = type(val).__name__
    out.append(f'key={key} type={t}')
    if t == 'dict':
        if sid in val:
            out.append(f'  FOUND at data["{key}"]["{sid}"]')
            out.append(json.dumps(val[sid], indent=2)[:5000])
        elif any(sid in str(k) for k in val.keys()):
            matching = [k for k in val.keys() if sid in str(k)]
            out.append(f'  partial key matches: {matching}')
        elif any(sid in str(v) for v in val.values() if isinstance(v, str)):
            out.append(f'  string value contains sid')
    elif t == 'list':
        matches = [i for i, v in enumerate(val) if sid in str(v)]
        out.append(f'  len={len(val)}, matches={len(matches)}')
        if matches:
            for i in matches[:3]:
                out.append(f'  [{i}]: {str(val[i])[:500]}')

with open('_diag_out.txt', 'w') as f:
    f.write('\n'.join(out))
