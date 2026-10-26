# -*- coding: utf-8 -*-
"""Refresh RECEIPT.md's full folder inventory fence to the current folder
state (the cold-reader fix pass landed 4 files and changed 3 sizes after the
previous fence moment), disclose the refresh, and re-fixed-point the self
size. All measurements taken fresh in this script. Every opened or written
path is normalized and validated to stay inside the repo root (Mimosa
hardening)."""
import os

REPO = os.path.realpath(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
ROOT = os.path.realpath(os.path.join(REPO, "watch", "inbox", "frontier_olm_2026-10-03"))
RECEIPT = os.path.realpath(os.path.join(ROOT, "RECEIPT.md"))
INV = os.path.realpath(os.path.join(ROOT, "sweep", "tmp", "fold2_inventory_current.txt"))
TXT = "sweep/tmp/fold2_inventory_current.txt"


def guarded(path):
    """Normalize and require the path to stay inside the repo root."""
    real = os.path.realpath(path)
    if not (real == REPO or real.startswith(REPO + os.sep)):
        raise ValueError("path escapes repo root: %s" % path)
    return real


RECEIPT = guarded(RECEIPT)
INV = guarded(INV)

text = open(RECEIPT, encoding="utf-8").read()

# 1. disclosure line appended to the checks list
old_check_tail = "Repair planning uses the lens numbers."
count = text.count(old_check_tail)
assert count == 1, count
text = text.replace(old_check_tail,
                    "Repair planning uses the lens numbers.\n9. Receipt refresh (same sitting, cold-reader follow-up): the full folder inventory fence below was regenerated because the fix pass landed four scratch and artifact files (sweep/tmp/coldread_fix.py, sweep/tmp/fold2_receipt_fix.py, sweep/tmp/fold2_receipt_fix2.py, sweep/tmp/kg_reconcile.json) and changed DIGEST.md, RECEIPT.md and sweep/tmp/fold2_inventory_current.txt after the previous fence moment; the fold-files table values were re-verified against measured truth.")

# 2. rebuild the inventory fence with a placeholder for RECEIPT.md's own size
marker = "### Full folder inventory"
idx = text.index(marker)
head = text[:idx]
placeholder_fence = (
    "### Full folder inventory (PENDING files, PENDING bytes, measured 2026-10-04 after the cold-reader fix pass)\n"
    "\n"
    "```text\n"
    "@@INVENTORY@@\n"
    "```\n"
)
text = head + placeholder_fence

for _ in range(5):
    with open(guarded(RECEIPT), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    entries = []
    total = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            p = guarded(os.path.join(dirpath, fn))
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
            entries.append((rel, os.path.getsize(p)))
            total += os.path.getsize(p)
    entries.sort()
    size_map = dict(entries)
    inv_lines = []
    for rel, sz in entries:
        if rel == "RECEIPT.md":
            inv_lines.append("%9d  %s" % (0, rel))
        else:
            inv_lines.append("%9d  %s" % (sz, rel))
    inv_lines.append("TOTAL files=%d bytes=%d" % (len(entries), total))
    new_text = text.replace("@@INVENTORY@@\n", "\n".join(inv_lines) + "\n")
    new_text = new_text.replace("(PENDING files, PENDING bytes", "(%d files, %d bytes" % (len(entries), total))
    new_text = new_text.replace("%9d  RECEIPT.md" % 0, "%9d  RECEIPT.md" % size_map["RECEIPT.md"])
    if new_text == text:
        break
    text = new_text

with open(guarded(RECEIPT), "w", encoding="utf-8", newline="\n") as f:
    f.write(text)
final = os.path.getsize(guarded(RECEIPT))
body = open(guarded(RECEIPT), encoding="utf-8").read()
assert ("%9d  RECEIPT.md" % final) in body, "self size row wrong"
print("RECEIPT.md bytes:", final)

# also refresh the companion measurement artifact to the same moment
claims = [
    ("steal/agent-memory-and-continuity.md", "chars", 16124),
    ("steal/open-and-local-language-models-arxiv-hf.md", "bytes", 24852),
    ("steal/quantization-and-compression.md", "chars", 22856),
    ("sweep/agent-memory-and-continuity-hn.md", "bytes", 15259),
    ("sweep/evals-and-self-improvement-x.md", "bytes", 21603),
    ("sweep/open-and-local-language-models-arxiv.md", "bytes", 18525),
    ("sweep/quantization-and-compression-hn.md", "bytes", 34342),
    ("sweep/swarm-orchestration-hn.md", "bytes", 16729),
    ("sweep/swarm-orchestration-reddit.md", "bytes", 35621),
    ("sweep/swarm-orchestration-x.md", "bytes", 31487),
]
with open(guarded(INV), "w", encoding="utf-8", newline="\n") as f:
    for rel, sz in entries:
        f.write("%9d  %s\n" % (sz, rel))
    f.write("TOTAL files=%d bytes=%d\n" % (len(entries), total))
    f.write("claimed-versus-measured (regenerated at the receipt refresh):\n")
    for rel, unit, claimed in claims:
        f.write("  %-55s claimed %s=%d measured=%d match=%s\n" % (
            rel, unit, claimed, size_map.get(rel, -1), str(size_map.get(rel) == claimed).lower()))
    f.write("round-1 fold files (historical, from the round-1 receipt): 30695 24640 15161 15190\n")
    f.write("round-1 cross-check values for files since grown by round-2 lanes (historical): 20931 12374 16905 14506 16674 19205\n")
print("companion artifact refreshed: files=%d bytes=%d" % (len(entries), total))
