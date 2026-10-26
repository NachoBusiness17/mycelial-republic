"""Verify the seed-rib v0.1 proof tree: seals, budget, derivation closure,
pointer honesty, state absence. Candidate two (card seedrib), 2026-09-26."""
from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from pathlib import Path

REPO = Path('.').resolve()
CANDS = REPO / 'watch/inbox/ractor_panel_20260926/cands'
TREE = CANDS / '_seedrib_two_tree/seed-rib'
ZIP = REPO / 'watch/inbox/seed-3.2.0.zip'
venv_py = str(REPO / '.venv/Scripts/python.exe')

results = []


def check(name: str, ok: bool, detail: str):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# C1: budget (filesystem truth, not derivation arithmetic)
files = [p for p in TREE.rglob('*') if p.is_file()]
total = sum(p.stat().st_size for p in files)
check('C1 budget', total <= 100_000 and len(files) == 43,
      f'{len(files)} files, {total} bytes on disk (cap 100,000; margin {100_000 - total})')

# C2: verify_seal.py exit 0 inside the tree (the pack's own verifier)
r = subprocess.run([venv_py, str(TREE / 'verify_seal.py')],
                   capture_output=True, text=True, cwd=str(TREE))
check('C2 verify_seal', r.returncode == 0, f'exit {r.returncode}: {r.stdout.strip()}')

# C3: derivation closure + carried byte-identity
der = json.loads((CANDS / '_seedrib_two_derivation.json').read_text(encoding='utf-8'))
tree_rels = {p.relative_to(TREE).as_posix() for p in files}
check('C3a closure', tree_rels == set(der),
      f'{len(tree_rels)} tree files vs {len(der)} derivation rows, symmetric difference '
      f'{sorted(tree_rels ^ set(der))}')
z = zipfile.ZipFile(ZIP)
bad = []
for rel, meta in der.items():
    if meta['method'].startswith('carried-frozen'):
        if TREE.joinpath(rel).read_bytes() != z.read('seed-3.2.0/' + rel):
            bad.append(rel)
    if meta['method'] == 'carried-from-repo (byte-identical)':
        if TREE.joinpath(rel).read_bytes() != REPO.joinpath(meta['source']).read_bytes():
            bad.append(rel)
    b = TREE.joinpath(rel).read_bytes()
    if sha(b) != meta['sha256'] or len(b) != meta['bytes']:
        bad.append(rel + ' (derivation row stale)')
check('C3b carried-identity', not bad, f'{len(bad)} mismatches {bad}')

# C4: POINTERS.sha256 honesty (every hash row matches its named source)
ptr = (TREE / 'POINTERS.sha256').read_text(encoding='utf-8').splitlines()
rows = [l for l in ptr if not l.startswith('#') and l.strip()]
badp, checked = [], 0
for row in rows:
    if row.startswith('-  '):
        continue  # named-value rows (git HEAD, verkle tip, essentials pack)
    h, rest = row.split('  ', 1)
    size, rest = rest.split('  ', 1)
    path, src = rest.split('  ', 1)
    if src == 'seed-3.2.0.zip':
        b = z.read('seed-3.2.0/' + path)
    else:
        b = REPO.joinpath(path).read_bytes()
    checked += 1
    if sha(b) != h or len(b) != int(size):
        badp.append(path)
check('C4 pointers', not badp, f'{checked}/{len(rows)} rows hash-checked, {len(badp)} bad {badp}')

# C5: state absence (nothing generated, no records, no ledgers)
stateish = [r for r in tree_rels if r.endswith('.jsonl') or r.startswith(('records/', 'logs/'))]
check('C5 no-carried-state', not stateish, f'state-like files in tree: {stateish}')

# C6: kernel sections present, non-stub, capped (B2-300 caps)
caps = {'env.law.md': 800, 'load.order.md': 1100, 'thesis.card.md': 1500,
        'state.now.md': 1500, 'filing.law.md': 800, 'tier.law.md': 500,
        'law.heads.json': 1500}
kern = {k: TREE.joinpath('kernel', k).stat().st_size for k in caps}
over = {k: (v, caps[k]) for k, v in kern.items() if v > caps[k]}
kernel_total = sum(kern.values())
check('C6 kernel', not over and kernel_total <= 9_700,
      f'7 sections, kernel total {kernel_total}B (cap 9,700), over-cap {over}')

# C7: law_refs ids exist in the sealed registry source
lh = json.loads((TREE / 'kernel/law.heads.json').read_text(encoding='utf-8'))
reg = json.loads((REPO / 'memory/law/registry.json').read_text(encoding='utf-8'))
missing = [i for i in lh['law_refs'] if i not in reg]
check('C7 law_refs', not missing and len(lh['law_refs']) == len(reg),
      f'{len(lh["law_refs"])} ids attested vs {len(reg)} in registry, missing {missing}')

# C8: cold-kernel answers (B2-300 acceptance, grep level)
env_b = (TREE / 'kernel/env.law.md').read_text(encoding='utf-8')
load_b = (TREE / 'kernel/load.order.md').read_text(encoding='utf-8')
fil_b = (TREE / 'kernel/filing.law.md').read_text(encoding='utf-8')
th_b = (TREE / 'kernel/thesis.card.md').read_text(encoding='utf-8')
ok8 = ('.venv' in env_b and 'never bare' in env_b.lower() or 'mag.cmd' in env_b) \
    and 'FRAMEWORK_LOAD' in load_b and 'watch/inbox' in fil_b and 'STANDING THESIS' in th_b
check('C8 cold-kernel answers', ok8,
      'env law names the venv interpreter; load order carries FRAMEWORK_LOAD path; '
      'filing law carries watch/inbox receipt law; thesis card carries the standing thesis')

print()
fails = [n for n, ok, _ in results if not ok]
print(f'{len(results) - len(fails)}/{len(results)} checks passed' + (f'; FAILS: {fails}' if fails else ''))
raise SystemExit(1 if fails else 0)
