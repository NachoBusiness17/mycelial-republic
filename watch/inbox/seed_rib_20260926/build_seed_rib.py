"""Build the LANDED seed-rib v0.1 tree (card seedrib revision, 2026-09-26).

Durable home: watch/inbox/seed_rib_20260926/seed-rib/ (judge critique bullet 2;
the shared inbox is the estate's durable write root, so the tree lands here
instead of being deleted as proof-tree pseudo-state).

Assembles the tree from:
  - frozen zip bytes  (watch/inbox/seed-3.2.0.zip, sha256 e9f4603a... verified)
  - repo bytes        (tools/seed_rib.py)
  - live extractions  (AGENTS.md sections, handoff procedure, context-pack L0b,
                       state/START_BRIEF.md + state/CURRENT.md heads,
                       memory/law seals)
  - authored identity (SEED_VERSION, SEED_RIB.md)
Every output file gets a row in derivation.json (beside this script, OUTSIDE
the tree): source + method. Regenerates MANIFEST.sha256 (verify_seal contract)
and POINTERS.sha256 (pointer carrier).

Revision deltas vs the candidate proof build (critique bullets):
  - reduction report: the L1-L5 budget levers are MEASURED from this build and
    printed mechanically (bullet 6), no longer prose only.
  - POINTERS named-value rows are concrete and checkable: live git HEAD +
    branch, warm_state verkle tip + index, and the dated essentials pack file
    with bytes + sha256 (bullet 5).
  - SEED_RIB.md records the exact seed_rib.v0 compat invocation (bullet 3).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path('.').resolve()
HOME = REPO / 'watch/inbox/seed_rib_20260926'
TREE = HOME / 'seed-rib'
ZIP = REPO / 'watch/inbox/seed-3.2.0.zip'
CAP = 100_000

CARRIED_FROM_ZIP = [
    'LICENSE', 'CHANGELOG.md', 'AGENTS.md', 'FIRST_BOOT.md', 'SETUP.md',
    'THE_METHOD.md', 'TOUR.md', 'HANDOFF.md', 'ACCOUNTS.md', 'DATA_TIERS.md',
    'MORNING_LOOP.md', 'SALON.md', 'ZERO_CONTEXT_DELEGATION.md',
    'SHARED_SURFACE_LAW.md', 'BUILD_DISCIPLINE_LAWS.md', 'TRUST_BYTES_LAW.md',
    'ARTIFACT_LEDGER_LAW.md', 'STATE_BRIEF_CONTRACT.md', 'BOOT_BUDGET_CARD.md',
    'CAPABILITY_GATE_LEDGER.md', 'VSCODE.md', 'verify_seal.py',
    'configs/keys.json', 'configs/chores.json', 'configs/law_registry.json',
    'configs/mode_budgets.json',
    'engines/seed_init.py', 'engines/spine_walk.py', 'engines/key_law.py',
    'engines/keys.py', 'engines/cooker.py',
]
LEFT_OUT_ZIP = [
    'engines/claritas.py', 'engines/estate_atlas.py',
    'engines/estate_smith_chart.py', 'engines/flight_recorder.py',
    'engines/librarian_catalog.py', 'engines/lite_guard.py',
    'engines/model_bakeoff.py', 'engines/phone_relay.py',
    'engines/process_supervisor.py', 'engines/stealth_sweep.py',
    'engines/task_wall.py',
    'ACTIVITY_TRAIL.md', 'CAMPAIGN_EVIDENCE.md', 'COST_LEDGER_TEMPLATE.md',
    'LOOP_GAP_TEMPLATE.md', 'SKILLS.md', 'TRAINING_EVENT_TEMPLATE.md',
    'TRAINING_SPINE_LAW.md',
    'tests/__init__.py', 'tests/test_seed_laws.py',
]
UNIVERSE_REPO = [
    'AGENTS.md', 'docs/FRAMEWORK_LOAD.md',
    'docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md', 'docs/ref/MYCELIAL_SCIENCE_MAP.md',
    'docs/ref/MAG_DIRECTION_ARTIFACT_v2.md', 'docs/ref/MAG_PROJECT_PROPOSAL.md',
    'docs/ref/OPERATOR_CARD.md', 'docs/DNA.md', 'memory/law/registry.json',
    'tools/seed_mcp.py', 'configs/lanes.yaml', 'configs/version_roadmap.yaml',
    'watch/inbox/SEED_RIB_FORMAT_v0_20260926.md',
    'watch/inbox/SEED_RIB_HANDOFF_KERNEL_20260926.md',
    'watch/inbox/SEED_RIB_CURRENT_20260926.json',
]
KERNEL_CAPS = {'env.law.md': 800, 'load.order.md': 1100, 'thesis.card.md': 1500,
               'state.now.md': 1500, 'filing.law.md': 800, 'tier.law.md': 500,
               'law.heads.json': 1500}
# B2-300 TOC caps with load.order at its original 600 (the L5 floor).
B2300_FLOOR = dict(KERNEL_CAPS, **{'load.order.md': 600})

derivation: dict[str, dict] = {}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def put(rel: str, data: bytes, source: str, method: str):
    p = TREE / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    derivation[rel] = {'bytes': len(data), 'sha256': sha(data),
                       'source': source, 'method': method}


def section(text: str, cap: int, name: str, source: str) -> bytes:
    b = text.encode('utf-8')
    assert len(b) <= cap, f'{name} over cap: {len(b)} > {cap}'
    return b


z = zipfile.ZipFile(ZIP)
now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

# --- 1. carried frozen bytes from the zip ---
for rel in CARRIED_FROM_ZIP:
    put(rel, z.read('seed-3.2.0/' + rel), 'watch/inbox/seed-3.2.0.zip!seed-3.2.0/' + rel,
        'carried-frozen (byte-identical zip entry)')

# --- 2. carried repo bytes ---
put('rib/seed_rib.py', (REPO / 'tools/seed_rib.py').read_bytes(),
    'tools/seed_rib.py', 'carried-from-repo (byte-identical)')

# --- 3. authored identity ---
put('SEED_VERSION',
    ('seed-rib 0.1 merge: seed 3.2.0 (public pack) + seed_rib.v0 (B2-180) '
     '+ handoff kernel (B2-300)\n').encode(),
    'authored', 'authored-new (merge identity)')

SEED_RIB_MD = """# SEED_RIB: the merge law and the cold-join procedure

This directory is the SEED-RIB merge: the public seed pack 3.2.0 (method +
engines + laws-as-config) fused with the seed_rib.v0 carrier law (B2-180) and
the handoff kernel sections (B2-300). It is the fleet KERNEL: everything a
cold agent needs to rebuild the fleet's shape and regrow its state.

## Carrier law (seed_rib.v0.1, re-homed onto a directory)

- A file PRESENT in this tree is the INLINE carrier: raw bytes, sealed in
  MANIFEST.sha256. `python verify_seal.py` proves the whole tree (exit 0).
- A row in POINTERS.sha256 with no file is the POINTER carrier: path + bytes +
  sha256. Pointers are promises with hashes, never hand-waves. Fetch from the
  named source and hash-check; the verifier never invents pointer bytes.
- kernel/law.heads.json carries law_refs (the law registry ids this seed
  attests) and per-law-file seals.
- Canonical format home: watch/inbox/SEED_RIB_FORMAT_v0_20260926.md (v0.1
  amendment note, 2026-09-26) recognizes this directory carrier.

## Cold join (rebuild the fleet kernel from this directory alone)

0. `python verify_seal.py`: exit 0 or stop here (trust bytes, not reports).
1. Read kernel/ in order: thesis.card.md, state.now.md, env.law.md,
   load.order.md, tier.law.md, filing.law.md. These seven sections are the
   handoff kernel: the cold seat now knows the thesis, the owed, the env law,
   the load order, the tier ladder, the filing law.
2. Zero state, honestly: `python engines/spine_walk.py <this-dir>` indexes the
   kernel itself (the map regenerates; it is never hand-maintained). The full
   method's smith chart (FIRST_BOOT step 2) is a POINTER row: the kernel boot
   substitutes this self-index; fetch the chart engine when you run lanes.
3. `python engines/key_law.py --audit`: passes on declared 'awaiting' keys,
   fails loud the moment a live key is undeclared.
4. `python engines/cooker.py status`: the free-lane reset table.
5. Grow: a stranger runs `python engines/seed_init.py <target>` and grows
   their own estate under THE_METHOD.md (FIRST_BOOT.md is that path).
   A fleet seat rehydrates the UNIVERSE instead: every row of POINTERS.sha256
   names a source (repo path in the fleet mirror, or the git/verkle/essentials
   rows); fetch, hash-check, lay down. The universe is never carried, only
   sealed.

## Compat build (the seed_rib.v0 JSON is a build product, not the carrier)

rib/seed_rib.py (byte-identical to tools/seed_rib.py) still builds and
verifies a seed_rib.v0 JSON. Default flags select nothing (0 entries), so the
selection must be explicit. Verified invocation, run with the tree's own copy
against the fleet repo (numbers are as-of this seed's build stamp; the live
law corpus moves them: the candidate artifact's 23,595 B / law_refs 11 was
never reproducible because its selection was never recorded, and the same
corpus read 21,473 B / law_refs 12 one build later):

    python rib/seed_rib.py build --root <fleet-repo> --out seed_from_tree.json --glob "memory/law/*.md"
    python rib/seed_rib.py verify --seed seed_from_tree.json --into <tmp-rebuild>

    build: 9 entries (9 inline, 0 pointer), seed 21473 bytes, law_refs 12
    verify: inline 9 hash-matched, exit 0

The battery (check_seed_rib.py, C9) reruns exactly these lines and fails on
drift, so the compat numbers above can never silently rot: when the live law
corpus grows, the battery fails loudly and the seed rebuilds.

## Budget and growth laws

- Whole tree < 100,000 bytes (measured at build; see MANIFEST row count).
  The build prints a REDUCTION REPORT with each lever measured from this
  build's own bytes; when a rebuild exceeds the cap the report names the
  lever set that recovers it. Levers, in order: L1 pointer-ize VSCODE.md;
  L2 TOUR.md + SALON.md; L3 MORNING_LOOP.md; L4 ACCOUNTS.md; L5 tighten
  kernel caps back to the B2-300 minimums (load.order to 600).
- STATE IS NEVER CARRIED. records/, indexes, meters, ledgers regenerate from
  zero by the engines; history folds to pointers (residual + registry + chain
  leaf per docs/DNA.md, sealed in POINTERS.sha256).
- A seed section carries its own as-of stamp; a state section older than the
  seed's build stamp voids the build (the stale-trap law, B2-300).
"""
put('SEED_RIB.md', SEED_RIB_MD.encode(), 'authored', 'authored-new (merge law)')

# --- 4. kernel sections, generated from live sources ---
agents = (REPO / 'AGENTS.md').read_text(encoding='utf-8')


def between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j].rstrip() + '\n'


py_env = between(agents, '## Python env (do not skip)', '## Commands')
env_md = ('# env.law (kernel section 1, extracted from AGENTS.md "Python env", '
          f'as-of {now})\n\n```\n{py_env}```\n')
put('kernel/env.law.md', section(env_md, 800, 'env.law.md', 'x'), 'AGENTS.md',
    'extracted (heading-to-heading slice, stamped)')

load_rows = []
in_table = False
for line in agents.splitlines():
    if line.startswith('## Load order'):
        in_table = True
        continue
    if in_table:
        if line.startswith('## '):
            in_table = False
            continue
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == 3 and cells[0].isdigit():
                # strip bold markers first, then code ticks: the live AGENTS.md
                # bolds the compass/science-map rows and the raw cell reads
                # **`docs/ref/...`** (fixed 2026-09-26 this revision; before
                # the fix rows 2-3 sealed MISSING)
                path = cells[1].replace('**', '').strip('`').strip()
                f = REPO / path
                if f.is_file():
                    seal = sha(f.read_bytes())
                elif ' ' in path:
                    seal = '(command row, no file)'
                else:
                    seal = 'MISSING'
                load_rows.append(f'{cells[0]} `{path}` {seal}')
load_md = (f'# load.order (generated {now}; seed read order: FIRST_BOOT.md -> THE_METHOD.md)\n\n'
           + '\n'.join(load_rows) + '\n')
# cap amended 600 -> 1100 by dated amendment (B2-300 mechanism), folded into
# the canonical TOC (watch/inbox/SEED_RIB_HANDOFF_KERNEL_20260926.md) this
# revision: full 64-hex sha256 seals for 7 file rows cost ~450B alone; kernel
# total stays <= 9,700.
put('kernel/load.order.md', section(load_md, 1100, 'load.order.md', 'x'), 'AGENTS.md',
    'generated (load table paths + full live sha256 seals)')

cp = subprocess.run(['cmd', '/c', 'mag.cmd', 'context-pack'], cwd=str(REPO),
                    capture_output=True, text=True, timeout=120).stdout
l0b = cp[cp.index('### L0b'):cp.index('### L0d')]
card = l0b[:l0b.index('## UPDATE')].rstrip()
thesis_md = (f'# thesis.card (L0b, regenerated {now})\n\n{card}\n')
put('kernel/thesis.card.md', section(thesis_md, 1500, 'thesis.card.md', 'x'),
    'mag.cmd context-pack (L0b)', 'regenerated (live render, sliced at UPDATE)')

sb = (REPO / 'state/START_BRIEF.md').read_text(encoding='utf-8')
runq = between(sb, "## 🟢 What's running", '## 🧠 What landed')
health = between(sb, '## ⚙️ Health', '## 📏')
cur = (REPO / 'state/CURRENT.md').read_text(encoding='utf-8')
owed_i = cur.index('- **owed (top):**')
owed = cur[owed_i:cur.index('\n- **owed (Mag')].rstrip()
now_md = (f'# state.now (kernel section 4, regenerated at seed build {now})\n'
          f'Sources: state/START_BRIEF.md ({sb.splitlines()[2].strip()}) + '
          f'state/CURRENT.md (updated line: {cur.splitlines()[2].strip()})\n\n'
          f'{runq}\n{health}\n{owed}\n')
put('kernel/state.now.md', section(now_md, 1500, 'state.now.md', 'x'),
    'state/START_BRIEF.md + state/CURRENT.md',
    'regenerated (head slices, stamped; never hand-carried)')

ho = (REPO / 'memories/session/next-window-handoff.md').read_text(encoding='utf-8')
proc = between(ho, '## Procedure (every new window, in order)', '## Standing laws')
standing = between(ho, '## Standing laws (do not re-derive)', '## STATE')
filing_md = (f'# filing.law (kernel section 5, extracted {now})\n\n'
             'Handoff procedure (memories/session/next-window-handoff.md):\n'
             + '\n'.join(l for l in proc.splitlines() if l.startswith('5.')) +
             '\n\nStanding law lines:\n'
             + '\n'.join(l for l in standing.splitlines()
                         if 'Residual on disk' in l or 'Append events' in l) +
             '\n\nShared surface: durable writes land on watch/inbox/ with a '
             'receipt + INDEX register (watch/inbox/SHARED_SURFACE_CONTRACT.json, '
             'pointer row).\n')
put('kernel/filing.law.md', section(filing_md, 800, 'filing.law.md', 'x'),
    'memories/session/next-window-handoff.md',
    'extracted (procedure step 5 + standing-law lines)')

tier_md = (f'# tier.law (kernel section 6, extracted {now})\n\n'
           + '\n'.join(l for l in standing.splitlines() if 'T0/T1' in l or 'Janitor' in l)
           + '\nL2 escalate needs `[priority]` / `[L2]` (configs/lanes.yaml, pointer '
             'row); do not claim R0; T0/T1 stay local.\n')
put('kernel/tier.law.md', section(tier_md, 500, 'tier.law.md', 'x'),
    'memories/session/next-window-handoff.md + AGENTS.md',
    'extracted (tier-ladder standing lines + escalate tags)')

reg = json.loads((REPO / 'memory/law/registry.json').read_text(encoding='utf-8'))
law_files = {}
for f in sorted((REPO / 'memory/law').glob('*.md')):
    b = f.read_bytes()
    law_files['memory/law/' + f.name] = {'bytes': len(b), 'sha256': sha(b)}
rb = (REPO / 'memory/law/registry.json').read_bytes()
law_heads = {
    'law_refs': sorted(reg.keys()),
    'registry': {'path': 'memory/law/registry.json', 'bytes': len(rb), 'sha256': sha(rb)},
    'law_files': law_files,
}
put('kernel/law.heads.json',
    section(json.dumps(law_heads, separators=(',', ':')), 1500,
            'law.heads.json', 'x'),
    'memory/law/registry.json + memory/law/*.md',
    'generated (ids parsed live + per-file seals)')

# --- 5. POINTERS.sha256 ---
rows = ['# POINTERS.sha256: the pointer carrier (seed_rib.v0 re-homed)',
        '# row: sha256  bytes  path  source   (fetch, hash-check, lay down;',
        '#        never invent bytes; law-file seals live in kernel/law.heads.json)',
        '# named-value rows start with "-  " and are verified by the battery',
        '# against their live named sources (git, warm_state, pack file).',
        f'# sealed {now}']
for rel in LEFT_OUT_ZIP:
    b = z.read('seed-3.2.0/' + rel)
    rows.append(f'{sha(b)}  {len(b)}  {rel}  seed-3.2.0.zip')
for rel in UNIVERSE_REPO:
    f = REPO / rel
    b = f.read_bytes()
    rows.append(f'{sha(b)}  {len(b)}  {rel}  fleet-repo')
ws = json.loads((REPO / 'memory/warm_state.json').read_text(encoding='utf-8'))
head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=str(REPO),
                      capture_output=True, text=True).stdout.strip()
branch = subprocess.run(['git', 'branch', '--show-current'], cwd=str(REPO),
                        capture_output=True, text=True).stdout.strip()
rows.append(f'-  git HEAD {head} branch {branch}'
            ' (universe root; rehydrate via clone)')
rows.append(f'-  verkle tip {ws["chain"]["verkle_root"]} index {ws["chain"]["index"]}'
            ' (memory/warm_state.json; chain continuity)')
packs = sorted(p for p in (REPO / 'watch/inbox').glob('ESSENTIALS_PACK_*.tar.gz.enc')
               if 'VAULT' not in p.name)
pack = packs[-1] if packs else None
if pack is None:
    raise SystemExit('no dated ESSENTIALS_PACK_*.tar.gz.enc under watch/inbox; cannot seal row')
pack_bytes = pack.read_bytes()
rows.append(f'-  {sha(pack_bytes)}  {len(pack_bytes)}  watch/inbox/{pack.name}'
            '  essentials-pack (restore law: watch/inbox/ESSENTIALS_RESTORE.md)')
put('POINTERS.sha256', '\n'.join(rows).encode() + b'\n',
    'generated', 'generated (LEFT-OUT + universe rows, hashed at build)')

# --- 6. MANIFEST.sha256 (regenerated; excludes itself and foreign hook state) ---
# The Mimosa hook drops .mimosa/hook-state files into the cwd of subprocesses
# this battery spawns inside the tree (observed 2026-09-26 this revision, C2
# verify_seal run); they are foreign droppings, never seed content.
man = []
for p in sorted(TREE.rglob('*')):
    if '.mimosa' in p.parts:
        continue
    if p.is_file() and p.name != 'MANIFEST.sha256':
        rel = p.relative_to(TREE).as_posix()
        man.append(f'{sha(p.read_bytes())}  {rel}')
put('MANIFEST.sha256', ('\n'.join(man) + '\n').encode(),
    'regenerated over the assembled tree', 'generated (verify_seal contract)')

# --- 7. derivation.json (build evidence; lives OUTSIDE the tree) ---
(HOME / 'derivation.json').write_text(
    json.dumps(derivation, indent=1, sort_keys=True), encoding='utf-8')

total = sum(v['bytes'] for v in derivation.values())
print(f'TREE={TREE}')
print(f'files={len(derivation)} total_bytes={total} over_100KB={total > CAP}')
for rel in sorted(derivation, key=lambda r: -derivation[r]['bytes'])[:8]:
    print(f"  {derivation[rel]['bytes']:>7} {rel}")

# --- 8. REDUCTION REPORT (bullet 6: levers measured, mechanical) ---
def manifest_row(rel: str) -> int:
    return 64 + 2 + len(rel) + 1


def pointers_row(rel: str, size: int) -> int:
    return 64 + 2 + len(str(size)) + 2 + len(rel) + 2 + len('seed-3.2.0.zip') + 1


def lever(files: list[str]) -> int:
    freed = 0
    for rel in files:
        freed += derivation[rel]['bytes'] + manifest_row(rel) - pointers_row(rel, derivation[rel]['bytes'])
    return freed


levers = [
    ('L1', ['VSCODE.md']),
    ('L2', ['TOUR.md', 'SALON.md']),
    ('L3', ['MORNING_LOOP.md']),
    ('L4', ['ACCOUNTS.md']),
]
kernel_floor_freed = sum(
    max(0, derivation['kernel/' + k]['bytes'] - cap) for k, cap in B2300_FLOOR.items())
print('REDUCTION REPORT (levers measured from this build; mechanical, not prose)')
print(f'  tree total: {total} B in {len(derivation)} files (cap {CAP}; margin {CAP - total})')
cum = 0
for name, files in levers:
    f = lever(files)
    cum += f
    print(f'  {name} pointer-ize {"+".join(files)}: frees {f} B')
print(f'  L5 kernel caps to B2-300 floor (load.order 600): frees {kernel_floor_freed} B')
print(f'  L1-L4 cumulative: {cum} B; full L1-L5 path: {cum + kernel_floor_freed} B')
over = max(0, total - CAP)
need, taken = 0, 0
for name, files in levers:
    if taken >= over:
        break
    taken += lever(files)
    need += 1
if over == 0:
    print('  over-budget recovery: 0 B over; no lever required this build')
else:
    suffix = ' (+L5)' if taken < over else ''
    print(f'  over-budget recovery: {over} B over; levers L1-L{need}{suffix} '
          f'recover {taken + (kernel_floor_freed if taken < over else 0)} B')
