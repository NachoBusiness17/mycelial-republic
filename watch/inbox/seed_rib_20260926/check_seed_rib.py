"""Verify the LANDED seed-rib v0.1 tree: seals, budget, derivation closure,
pointer honesty (hash rows AND named-value rows), state absence, kernel caps,
law_refs, cold-kernel answers, compat invocation, reduction report.

Card seedrib revision battery (2026-09-26). Critique deltas vs the candidate
battery: C4b makes the three named-value pointer rows checkable against their
live named sources (bullet 5); C9 reruns the exact compat invocation recorded
in SEED_RIB.md (bullet 3); C10 re-derives the reduction report from the tree
and fails on drift vs build.out (bullet 6).
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

REPO = Path('.').resolve()
HOME = REPO / 'watch/inbox/seed_rib_20260926'
TREE = HOME / 'seed-rib'
ZIP = REPO / 'watch/inbox/seed-3.2.0.zip'
venv_py = str(REPO / '.venv/Scripts/python.exe')

results = []


def check(name: str, ok: bool, detail: str):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    d = hashlib.sha256()
    with p.open('rb') as h:
        for chunk in iter(lambda: h.read(4 * 1024 * 1024), b''):
            d.update(chunk)
    return d.hexdigest()


# C1: budget (filesystem truth, not derivation arithmetic). .mimosa/ is the
# Mimosa hook's per-session state dropped into the cwd of subprocesses this
# battery spawns inside the tree (observed 2026-09-26 this revision); foreign
# droppings, excluded by name, never seed content.
files = [p for p in TREE.rglob('*')
         if p.is_file() and '.mimosa' not in p.parts]
total = sum(p.stat().st_size for p in files)
check('C1 budget', total <= 100_000 and len(files) == 43,
      f'{len(files)} files, {total} bytes on disk (cap 100,000; margin {100_000 - total})')

# C2: verify_seal.py exit 0 inside the tree (the pack's own verifier)
r = subprocess.run([venv_py, str(TREE / 'verify_seal.py')],
                   capture_output=True, text=True, cwd=str(TREE))
check('C2 verify_seal', r.returncode == 0, f'exit {r.returncode}: {r.stdout.strip()}')

# C3: derivation closure + carried byte-identity
der = json.loads((HOME / 'derivation.json').read_text(encoding='utf-8'))
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
named = [l for l in rows if l.startswith('-  ')]
hash_rows = [l for l in rows if not l.startswith('-  ')]
badp, checked = [], 0
for row in hash_rows:
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
check('C4 pointers', not badp,
      f'{checked}/{len(hash_rows)} hash rows checked, {len(badp)} bad {badp} '
      f'(+{len(named)} named-value rows -> C4b)')

# C4b: named-value rows verified against their live named sources (bullet 5)
git_row = next(l for l in named if 'git HEAD' in l)
m = re.match(r'-\s+git HEAD ([0-9a-f]{40}) branch (\S+)', git_row)
live_head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(REPO),
                           capture_output=True, text=True).stdout.strip()
live_branch = subprocess.run(['git', 'branch', '--show-current'], cwd=str(REPO),
                             capture_output=True, text=True).stdout.strip()
check('C4b git HEAD + branch', m is not None
      and m.group(1) == live_head and m.group(2) == live_branch,
      f'row HEAD {m.group(1) if m else "?"} / branch {m.group(2) if m else "?"} '
      f'vs live {live_head} / {live_branch}')

vk_row = next(l for l in named if 'verkle tip' in l)
m2 = re.match(r'-\s+verkle tip (\S+) index (\d+)', vk_row)
ws = json.loads((REPO / 'memory/warm_state.json').read_text(encoding='utf-8'))
check('C4b verkle tip', m2 is not None
      and m2.group(1) == ws['chain']['verkle_root'] and int(m2.group(2)) == ws['chain']['index'],
      f"row tip {m2.group(1) if m2 else '?'} index {m2.group(2) if m2 else '?'} vs "
      f"warm_state {ws['chain']['verkle_root']} index {ws['chain']['index']} "
      f"(source stores the root {len(ws['chain']['verkle_root'])} chars, truncated by its writer)")

pk_row = next(l for l in named if 'essentials-pack' in l)
m3 = re.match(r'-\s+([0-9a-f]{64})\s+(\d+)\s+(\S+)\s+essentials-pack', pk_row)
pk_ok, pk_detail = False, 'row did not parse'
if m3:
    pk = REPO / m3.group(3)
    if pk.is_file():
        live_sz, live_h = pk.stat().st_size, sha_file(pk)
        pk_ok = live_sz == int(m3.group(2)) and live_h == m3.group(1)
        pk_detail = (f'{m3.group(3)} row {m3.group(2)}B/{m3.group(1)[:12]} vs '
                     f'live {live_sz}B/{live_h[:12]}')
    else:
        pk_detail = f'{m3.group(3)} named by row but absent on disk'
check('C4b essentials pack', pk_ok, pk_detail)

# C5: state absence (nothing generated, no records, no ledgers)
stateish = [r for r in tree_rels if r.endswith('.jsonl') or r.startswith(('records/', 'logs/'))]
check('C5 no-carried-state', not stateish, f'state-like files in tree: {stateish}')

# C6: kernel sections present, non-stub, capped (B2-300 caps, load.order
# amended to 1,100 in the canonical TOC this revision)
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

# C8: cold-kernel answers (B2-300 acceptance, grep level; the cold-SEAT run
# is administered separately and its raw output is filed beside this battery)
env_b = (TREE / 'kernel/env.law.md').read_text(encoding='utf-8')
load_b = (TREE / 'kernel/load.order.md').read_text(encoding='utf-8')
fil_b = (TREE / 'kernel/filing.law.md').read_text(encoding='utf-8')
th_b = (TREE / 'kernel/thesis.card.md').read_text(encoding='utf-8')
ok8 = ('.venv' in env_b and 'never bare' in env_b.lower() or 'mag.cmd' in env_b) \
    and 'FRAMEWORK_LOAD' in load_b and 'watch/inbox' in fil_b and 'STANDING THESIS' in th_b
check('C8 cold-kernel answers', ok8,
      'env law names the venv interpreter; load order carries FRAMEWORK_LOAD path; '
      'filing law carries watch/inbox receipt law; thesis card carries the standing thesis')

# C9: compat invocation (bullet 3): rerun the exact command recorded in
# SEED_RIB.md and fail if the recorded numbers rot.
sr_md = (TREE / 'SEED_RIB.md').read_text(encoding='utf-8')
rec_b = re.search(r'build: (\d+) entries \((\d+) inline, (\d+) pointer\), seed (\d+) bytes, '
                  r'law_refs (\d+)', sr_md)
rec_v = re.search(r'verify: inline (\d+) hash-matched', sr_md)
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    out = tmp / 'seed_from_tree.json'
    into = tmp / 'rebuilt'
    r1 = subprocess.run([venv_py, str(TREE / 'rib/seed_rib.py'), 'build',
                         '--root', str(REPO), '--out', str(out),
                         '--glob', 'memory/law/*.md'],
                        capture_output=True, text=True)
    got_b = re.search(r'build: (\d+) entries \((\d+) inline, (\d+) pointer\), seed (\d+) bytes, '
                      r'law_refs (\d+)', r1.stdout)
    r2 = subprocess.run([venv_py, str(TREE / 'rib/seed_rib.py'), 'verify',
                         '--seed', str(out), '--into', str(into)],
                        capture_output=True, text=True)
    got_v = re.search(r'verify: inline (\d+) hash-matched', r2.stdout)
    ok9 = (r1.returncode == 0 and r2.returncode == 0 and rec_b and rec_v
           and got_b and got_v
           and got_b.groups() == rec_b.groups() and got_v.group(1) == rec_v.group(1))
    check('C9 compat invocation', ok9,
          f'build exit {r1.returncode}: {(r1.stdout or r1.stderr).strip()} | '
          f'verify exit {r2.returncode}: {(r2.stdout or r2.stderr).strip()} | '
          f'recorded in SEED_RIB.md: {rec_b.group(0) if rec_b else "NOT PARSED"}, '
          f'{rec_v.group(0) if rec_v else "NOT PARSED"}')

# C10: reduction report (bullet 6): re-derive the levers from the tree on
# disk and fail on drift vs the report the build printed into build.out.
def manifest_row(rel: str) -> int:
    return 64 + 2 + len(rel) + 1


def pointers_row(rel: str, size: int) -> int:
    return 64 + 2 + len(str(size)) + 2 + len(rel) + 2 + len('seed-3.2.0.zip') + 1


def lever(files: list[str]) -> int:
    freed = 0
    for rel in files:
        sz = TREE.joinpath(rel).stat().st_size
        freed += sz + manifest_row(rel) - pointers_row(rel, sz)
    return freed


floor_caps = dict(caps, **{'load.order.md': 600})
floor_freed = sum(max(0, TREE.joinpath('kernel', k).stat().st_size - c)
                  for k, c in floor_caps.items())
levers = [('L1', ['VSCODE.md']), ('L2', ['TOUR.md', 'SALON.md']),
          ('L3', ['MORNING_LOOP.md']), ('L4', ['ACCOUNTS.md'])]
lever_files_ok = all(TREE.joinpath(f).is_file() for _, fs in levers for f in fs)
over_cap = max(0, total - 100_000)
cum, taken, need = 0, 0, 0
for name, fs in levers:
    cum += lever(fs)
    if taken < over_cap:
        taken += lever(fs)
        need += 1
path_covers = taken >= over_cap
detail = (f'recomputed L1={lever(["VSCODE.md"])} L2={lever(["TOUR.md", "SALON.md"])} '
          f'L3={lever(["MORNING_LOOP.md"])} L4={lever(["ACCOUNTS.md"])} L5={floor_freed}; '
          f'lever files present={lever_files_ok}; over-cap {over_cap}B '
          f'covered by first {need} levers={path_covers}')
build_out = HOME / 'build.out'
if build_out.is_file():
    bo = build_out.read_text(encoding='utf-8')
    rep_l1 = re.search(r'L1 pointer-ize [^:]+: frees (\d+) B', bo)
    rep_l5 = re.search(r'L5 kernel caps to B2-300 floor \(load\.order 600\): frees (\d+) B', bo)
    rep_tot = re.search(r'tree total: (\d+) B in (\d+) files', bo)
    matches = (rep_l1 and int(rep_l1.group(1)) == lever(['VSCODE.md'])
               and rep_l5 and int(rep_l5.group(1)) == floor_freed
               and rep_tot and int(rep_tot.group(1)) == total and int(rep_tot.group(2)) == 43)
    detail += f'; build.out report matches recomputation={bool(matches)}'
else:
    matches = True
    detail += '; build.out absent (recomputed from tree only)'
check('C10 reduction report', lever_files_ok and path_covers and matches, detail)

print()
fails = [n for n, ok, _ in results if not ok]
print(f'{len(results) - len(fails)}/{len(results)} checks passed' + (f'; FAILS: {fails}' if fails else ''))
raise SystemExit(1 if fails else 0)
