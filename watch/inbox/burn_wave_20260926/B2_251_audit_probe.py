"""B2-251 audit probe: resolve landing receipts for every checked Open row in QUEUE.md.

Read-only census. Prints per checked row: line no, id, whether the row text names a
filesystem path that resolves, and which lane-id receipt files exist on disk with a
Verdict heading. No bytes are modified by this probe.
"""
import os
import re
import glob

QUEUE = 'watch/inbox/burn_wave_20260926/QUEUE.md'
WAVE = 'watch/inbox/burn_wave_20260926'

lines = open(QUEUE, encoding='utf-8').read().split('\n')
open_start = next(i for i, l in enumerate(lines) if l.strip() == '## Open')
row_re = re.compile(r'^- \[([ xX])\] (B2-\d+)')
# path-shaped tokens that could be receipts or pointers
path_re = re.compile(
    r'(?:watch[/\\]inbox[/\\][A-Za-z0-9_./\\-]+|'
    r'(?:tools|scripts|configs|tests|mag|docs|githooks|memory|roblox|corpus|state|logs|agents)'
    r'[/\\][A-Za-z0-9_./\\-]+)'
)

receipts = {}
for f in glob.glob(os.path.join(WAVE, 'B2_*.md')):
    m = re.match(r'B2_(\d+)_', os.path.basename(f))
    if m:
        receipts.setdefault(int(m.group(1)), []).append(f)

for i in range(open_start, len(lines)):
    m = row_re.match(lines[i])
    if not m or m.group(1).lower() != 'x':
        continue
    bid = int(m.group(2).split('-')[1])
    text = lines[i]
    named = []
    for pm in path_re.finditer(text):
        p = pm.group(0).rstrip('.,;:)').replace('\\', '/')
        named.append((p, os.path.exists(p)))
    resolving = [p for p, e in named if e]
    dead = [p for p, e in named if not e]
    lane_recs = []
    for r in receipts.get(bid, []):
        head = open(r, encoding='utf-8', errors='replace').read(4000)
        lane_recs.append((os.path.basename(r), '## Verdict' in head))
    # a named path counts as a resolvable in-row receipt pointer when it exists and
    # sits in the burn wave receipt directory
    named_receipt_resolves = any(
        e and 'burn_wave_20260926' in p and p.endswith('.md') for p, e in named
    )
    tag = 'INROW-RECEIPT' if named_receipt_resolves else ('LANE-RECEIPT' if lane_recs else 'NO-RECEIPT')
    print(f'{i+1} {m.group(2)} {tag} lane_receipts={lane_recs}')
    if not named_receipt_resolves:
        print(f'    resolving: {resolving[:4]}')
        if dead:
            print(f'    dead: {dead[:4]}')
