"""s2-07 instrument v2: cycle-safe walk, top files by byte count.

Excludes dirs named .git/.venv/node_modules/corpus anywhere in the tree.
Cycle protection: a directory whose realpath was already visited (or that
resolves outside/outside-above ROOT) is pruned. Progress every 5000 dirs.
"""
import os
import sys
import datetime

ROOT = os.path.realpath(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
EXCLUDE = {".git", ".venv", "node_modules", "corpus"}

rows = []
visited = set()
dirs_seen = 0
skipped_cycles = 0
skipped_outside = 0
skipped_nul = 0

def scan(dirpath, depth=0):
    global dirs_seen, skipped_cycles, skipped_outside, skipped_nul
    dirs_seen += 1
    if dirs_seen % 5000 == 0:
        print(f"[progress] dirs={dirs_seen} files={len(rows)} at {dirpath}", file=sys.stderr, flush=True)
    if depth > 60:
        print(f"[depth-cap] {dirpath}", file=sys.stderr, flush=True)
        return
    try:
        entries = list(os.scandir(dirpath))
    except OSError as e:
        print(f"[oserror] {dirpath}: {e}", file=sys.stderr, flush=True)
        return
    subdirs = []
    for e in entries:
        try:
            if e.is_dir(follow_symlinks=False):
                subdirs.append(e)
                continue
            st = e.stat(follow_symlinks=False)
            p = e.path
            try:
                rel = os.path.relpath(p, ROOT)
            except ValueError:
                skipped_nul += 1
                continue
            mt = datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")
            rows.append((st.st_size, rel, mt))
        except OSError:
            continue
    for e in subdirs:
        if e.name in EXCLUDE:
            continue
        real = os.path.realpath(e.path)
        if real in visited:
            skipped_cycles += 1
            print(f"[cycle] {e.path} -> {real}", file=sys.stderr, flush=True)
            continue
        if not (real == ROOT or real.startswith(ROOT + os.sep)):
            skipped_outside += 1
            print(f"[outside] {e.path} -> {real}", file=sys.stderr, flush=True)
            continue
        visited.add(real)
        scan(real, depth + 1)

visited.add(ROOT)
scan(ROOT)

rows.sort(reverse=True)
print("total_files", len(rows))
print("total_bytes", sum(r[0] for r in rows))
print("dirs_scanned", dirs_seen)
print("skipped_cycles", skipped_cycles, "skipped_outside", skipped_outside, "skipped_nul", skipped_nul)
print("rank\tbytes\tmtime\trelpath")
for i, (sz, rel, mt) in enumerate(rows[:25], 1):
    print(f"{i}\t{sz}\t{mt}\t{rel}")
