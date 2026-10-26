# B2-279 2026-09-26: file the Shared-file claim law CLAIM lines for this lane's
# edit set (scripts/index_fold_host.mjs working-tree-modified, tests/test_index_fold_host.py
# git-untracked, QUEUE.md the lane's own board) BEFORE editing those bytes.
# QUEUE.md is CRLF (od check at lane start); inserts preserve the live EOL.
import datetime
import io

QUEUE = "watch/inbox/burn_wave_20260926/QUEUE.md"

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
claims = [
    f"- CLAIM B2-279 scripts/index_fold_host.mjs {now} (B2-279 sort totality: total-order event key, inexact-double demotion with counted fold warning, refold-stability pin)",
    f"- CLAIM B2-279 tests/test_index_fold_host.py {now} (B2-279: reorder expectations under the totality law plus the refold-stability and demotion tests)",
    f"- CLAIM B2-279 watch/inbox/burn_wave_20260926/QUEUE.md {now} (lane's own board: claim lines, landing note, self-feeds)",
]

with io.open(QUEUE, "r", encoding="utf-8", newline="") as fh:
    text = fh.read()

crlf = "\r\n" in text
eol = "\r\n" if crlf else "\n"
anchor = "## Open" + eol
assert text.count(anchor) == 1, "Open anchor not unique"
block = anchor + eol.join(claims) + eol
text = text.replace(anchor, block, 1)

with io.open(QUEUE, "w", encoding="utf-8", newline="") as fh:
    fh.write(text)

print("claim lines appended at", now, "eol", repr(eol))
