import json

chain_path = 'memory/biography/verkle_chain.jsonl'

total = 0
fkb_rows = 0
non_float_tension = 0
short_commit = 0
both = 0
tension_values = set()
commit_values = set()
affected_sessions = set()

with open(chain_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        ti = obj.get('tension_index', '')
        dc = obj.get('dossier_commit', '')
        sid = obj.get('session_id', '')

        if 'fkb' in str(sid).lower():
            fkb_rows += 1
            ti_is_float = False
            try:
                float(ti)
                ti_is_float = True
            except (ValueError, TypeError):
                pass
            if not ti_is_float:
                non_float_tension += 1
                tension_values.add(str(ti))
            if len(str(dc)) < 40:
                short_commit += 1
                commit_values.add(str(dc))
            if not ti_is_float and len(str(dc)) < 40:
                both += 1
                affected_sessions.add(sid)

out = []
out.append(f'Total rows in chain: {total}')
out.append(f'fkb session rows: {fkb_rows}')
out.append(f'fkb rows with non-float tension_index: {non_float_tension}')
out.append(f'fkb rows with short dossier_commit (<40 chars): {short_commit}')
out.append(f'fkb rows with BOTH anomalies: {both}')
out.append(f'Unique non-float tension_index values: {sorted(tension_values)}')
out.append(f'Unique short dossier_commit values: {sorted(commit_values)[:20]}')
out.append(f'Unique affected sessions: {len(affected_sessions)}')
out.append(f'Affected session IDs: {sorted(affected_sessions)[:10]}')

with open('_diag_out.txt', 'w') as f:
    f.write('\n'.join(out))