import json, sys

sid = 'autonomous-auto-fkb-183618'
out = []

with open('memory/derived/derived_dag_index.json') as f:
    data = json.load(f)

t = type(data).__name__
out.append(f'type: {t}')

if t == 'dict':
    out.append(f'keys_count: {len(data)}')
    ks = list(data.keys())[:5]
    out.append(f'first_keys: {ks}')
    out.append(f'has_fkb_key: {any("fkb" in str(k) for k in data.keys())}')
    # Look for session under each top-level key
    for k, v in data.items():
        if isinstance(v, dict) and v.get('session_id') == sid:
            out.append(f'FOUND under key={k}')
            out.append(json.dumps(v, indent=2)[:5000])
            break
        elif isinstance(v, str) and sid in v:
            out.append(f'Key {k} contains sid as string value')
    else:
        out.append('NOT FOUND as session_id in any top-level dict value')
elif t == 'list':
    out.append(f'len: {len(data)}')
    for i, item in enumerate(data[:3]):
        out.append(f'item[{i}] type={type(item).__name__}: {str(item)[:200]}')
else:
    out.append(f'val: {str(data)[:200]}')

with open('_diag_out.txt', 'w') as f:
    f.write('\n'.join(out))
