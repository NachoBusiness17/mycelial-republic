import json

sid = 'autonomous-auto-fkb-183618'
chain_path = 'memory/biography/verkle_chain.jsonl'

with open(chain_path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        s = obj.get('session_id', '')
        if s == sid:
            print("BASELINE SESSION ROW:")
            print(json.dumps(obj, indent=2, default=str))
            print()
            ti = obj.get('tension_index', '<MISSING>')
            dc = obj.get('dossier_commit', '<MISSING>')
            print(f"tension_index = {repr(ti)}  type={type(ti).__name__}  is_float={isinstance(ti, (int,float))}")
            print(f"dossier_commit = {repr(dc)}  len={len(str(dc))}")
            break
    else:
        print(f"Session {sid} NOT FOUND in verkle_chain.jsonl")