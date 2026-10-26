import os, io, sys

root = r'C:\Users\foste\Documents\projects\local_sovereign_agent'
pats = ['KVarN', 'KVTether', 'RR-Evict', 'CADOC', 'Beyond Token Savings',
        'Memory Wall', 'Agents Rot', 'DeepSeek-V4.1', 'Vosti', 'provenance',
        'prefix caching', 'lost-in-the-middle', 'lost in the middle']
hits = {p: [] for p in pats}
skip_dirs = {'.git', 'node_modules', '.venv', '__pycache__', 'logs', '.zcode'}
scanned = 0
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    for fn in filenames:
        if not fn.lower().endswith(('.md', '.json', '.jsonl', '.txt')):
            continue
        p = os.path.join(dirpath, fn)
        try:
            if os.path.getsize(p) > 8_000_000:
                continue
            with io.open(p, 'r', encoding='utf-8', errors='ignore') as f:
                t = f.read()
        except OSError:
            continue
        scanned += 1
        low = t.lower()
        for pat in pats:
            if pat.lower() in low:
                hits[pat].append(os.path.relpath(p, root))
print('files scanned:', scanned)
for pat in pats:
    print('PAT:', pat, '->', len(hits[pat]))
    for h in hits[pat][:15]:
        print('   ', h)
