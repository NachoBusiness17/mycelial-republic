import json, glob, os, re

print("--- CHECK 1b: decision recount with exact key attribution ---")
for wave in ['w1','w2','w3','wave5-repair','afterparty','ball-20260929','48h-synthesis']:
    d = 'watch/inbox/gala_20260925/' + wave + '/lanes'
    total = 0; bykey = {}; changed = 0
    for f in sorted(glob.glob(d + '/*.json')):
        if not f.endswith('.json'):
            continue
        try:
            j = json.load(open(f, encoding='utf-8'))
        except Exception as e:
            print(' PARSE FAIL', wave, os.path.basename(f), e); continue
        total += 1
        kfound = None; v = None
        for k in ('decision_changed', 'decision', 'decision_ledger'):
            if k in j:
                kfound = k
                raw = j[k]
                v = raw.get('decision_changed') if k == 'decision_ledger' and isinstance(raw, dict) else raw
                break
        if kfound is not None:
            bykey[kfound] = bykey.get(kfound, 0) + 1
            if str(v).strip().lower() not in ('no', 'false', 'none', ''):
                changed += 1
    print(f'{wave}: lanes={total} changed(non-no)={changed} keys={bykey}')

print()
print("--- CHECK 2b: every receipt path cited in communication.md exists ---")
txt = open('watch/inbox/ractor50/communication.md', encoding='utf-8').read()
cands = set(re.findall(r'(?:watch[/\\]inbox[/\\][A-Za-z0-9_.\-/\\]+|memory[/\\]rib[/\\][A-Za-z0-9_.\-]+|memories[/\\]session[/\\][A-Za-z0-9_.\-]+)', txt))
ok = 0; bad = 0
for c in sorted(cands):
    c2 = c.rstrip('.').replace('\\', '/').rstrip('.,;:')
    c2 = c2.rstrip('.').rstrip('.,;:')
    if len(c2) < 10:
        continue
    if os.path.exists(c2):
        ok += 1
    else:
        bad += 1
        print(' MISSING:', c2)
print(f'cited paths ok={ok} missing={bad}')

print()
print("--- CHECK 4b: retained COLLECT-DRIFT rows in attention.md, with dates ---")
import io
blocks = open('memory/attention.md', encoding='utf-8').read().split('---')
hits = [b.strip()[:200] for b in blocks if 'COLLECT-DRIFT' in b]
print('blocks containing COLLECT-DRIFT:', len(hits))
for h in hits:
    print(' >', h.replace('\n', ' | ')[:180])
