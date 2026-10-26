"""Build the seed-rib v0.1 proof tree for candidate two (card seedrib, 2026-09-26).

Assembles watch/inbox/ractor_panel_20260926/cands/_seedrib_two_tree/seed-rib/ from:
  - frozen zip bytes  (watch/inbox/seed-3.2.0.zip, sha256 e9f4603a... verified)
  - repo bytes        (tools/seed_rib.py)
  - live extractions  (AGENTS.md sections, handoff procedure, context-pack L0b,
                       state/START_BRIEF.md + state/CURRENT.md heads,
                       memory/law seals)
  - authored identity (SEED_VERSION, SEED_RIB.md)
Every output file gets a row in derivation.json: source + method. Regenerates
MANIFEST.sha256 (verify_seal contract) and POINTERS.sha256 (pointer carrier).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path('.').resolve()
CANDS = REPO / 'watch/inbox/ractor_panel_20260926/cands'
TREE = CANDS / '_seedrib_two_tree/seed-rib'
ZIP = REPO / 'watch/inbox/seed-3.2.0.zip'

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
KERNEL_CAPS = {'env.law.md': 800, 'load.order.md': 600, 'thesis.card.md': 1500,
               'state.now.md': 1500, 'filing.law.md': 800, 'tier.law.md': 500,
               'law.heads.json': 1500}

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

## Carrier law (seed_rib.v0, re-homed onto a directory)

- A file PRESENT in this tree is the INLINE carrier: raw bytes, sealed in
  MANIFEST.sha256. `python verify_seal.py` proves the whole tree (exit 0).
- A row in POINTERS.sha256 with no file is the POINTER carrier: path + bytes +
  sha256. Pointers are promises with hashes, never hand-waves. Fetch from the
  named source and hash-check; the verifier never invents pointer bytes.
- kernel/law.heads.json carries law_refs (the law registry ids this seed
  attests) and per-law-file seals.

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
   names a source (repo path in the fleet mirror, or the git/essentials rows);
   fetch, hash-check, lay down. The universe is never carried, only sealed.

## Budget and growth laws

- Whole tree < 100,000 bytes (measured at build; see MANIFEST row count).
  Reduction levers, in order: L1 pointer-ize VSCODE.md (~1.4KB); L2 TOUR.md +
  SALON.md (~3.2KB); L3 MORNING_LOOP.md (~1.2KB); L4 ACCOUNTS.md (~1.6KB);
  L5 tighten kernel caps back to the B2-300 minimums.
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
                path = cells[1].strip('`').strip()
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
# cap amended 600 -> 1100 by dated amendment (B2-300 mechanism): full 64-hex
# sha256 seals for 7 file rows cost ~450B alone; kernel total stays <= 9,700.
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
rows.append(f'-  git HEAD {head} branch mag/run-beta1-factory-build-audi-20260806T231709Z'
            f' (universe root; rehydrate via clone)')
rows.append(f'-  verkle tip {ws["chain"]["verkle_root"]} index {ws["chain"]["index"]}'
            ' (memory/warm_state.json; chain continuity)')
rows.append('-  ESSENTIALS_PACK_<date>.tar.gz.enc: universe pack; seal lives with the'
            ' pack itself (watch/inbox/ESSENTIALS_RESTORE.md)')
put('POINTERS.sha256', '\n'.join(rows).encode() + b'\n',
    'generated', 'generated (LEFT-OUT + universe rows, hashed at build)')

# --- 6. MANIFEST.sha256 (regenerated; excludes itself) ---
man = []
for p in sorted(TREE.rglob('*')):
    if p.is_file() and p.name != 'MANIFEST.sha256':
        rel = p.relative_to(TREE).as_posix()
        man.append(f'{sha(p.read_bytes())}  {rel}')
put('MANIFEST.sha256', ('\n'.join(man) + '\n').encode(),
    'regenerated over the assembled tree', 'generated (verify_seal contract)')

# --- 7. derivation.json (build evidence; lives OUTSIDE the tree) ---
(CANDS / '_seedrib_two_derivation.json').write_text(
    json.dumps(derivation, indent=1, sort_keys=True), encoding='utf-8')

total = sum(v['bytes'] for v in derivation.values())
print(f'TREE={TREE}')
print(f'files={len(derivation)} total_bytes={total} over_100KB={total > 100000}')
for rel in sorted(derivation, key=lambda r: -derivation[r]['bytes'])[:8]:
    print(f"  {derivation[rel]['bytes']:>7} {rel}")
