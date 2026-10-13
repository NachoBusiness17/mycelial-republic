import json, sys

short = 0
nonfloat = 0
both = 0
total = 0
none_ti = 0
none_dc = 0
anomaly_rows = []

with open('memory/biography/verkle_chain.jsonl') as f:
    for l in f:
        r = json.loads(l)
        if 'fkb' not in r.get('session_id', ''):
            continue
        total += 1
        ti = r.get('tension_index')
        dc = r.get('dossier_commit')
        ti_bad = ti is not None and not isinstance(ti, float)
        dc_bad = dc is not None and len(str(dc)) < 40
        if ti is None:
            none_ti += 1
        elif ti_bad:
            nonfloat += 1
        if dc is None:
            none_dc += 1
        elif dc_bad:
            short += 1
        if ti_bad and dc_bad:
            both += 1
            anomaly_rows.append({
                'index': r.get('index'),
                'session_id': r.get('session_id'),
                'tension_index': ti,
                'dossier_commit': dc,
                'ts': r.get('ts'),
            })

print(f"total fkb rows: {total}")
print(f"non-float tension_index: {nonfloat}")
print(f"short dossier_commit (<40 chars): {short}")
print(f"both anomalies: {both}")
print(f"null tension_index: {none_ti}")
print(f"null dossier_commit: {none_dc}")
print()
print("=== anomaly rows (first 20) ===")
for row in anomaly_rows[:20]:
    print(json.dumps(row))
