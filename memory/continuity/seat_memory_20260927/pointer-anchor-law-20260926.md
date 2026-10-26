---
name: pointer-anchor-law-20260926
description: 9/26 pointer-anchor law (B2-491) — every NEW file:line pointer in a burn brief must carry a byte anchor (path:NN#token); tools/pointer_rot_check.py names rotted pointers; born from two same-day pointer rots
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Burn-brief file:line pointers rot silently when upstream files move (providers.yaml edits shifted the ollama block from :66-67 to :84 and the mistral block from :473-488 to :534-550 in one afternoon). Law landed by B2-491 in the QUEUE.md header: every NEW file:line pointer carries a byte anchor `path:NN[-MM]#token` (exact key/symbol/quoted fragment present at filing time); bare pointers legal only when naming no lines.

**The checker:** `tools/pointer_rot_check.py` re-resolves pointers against current bytes — OK / ROT (anchor absent from cited range, with definition-like repair hints) / ROT-SEED / MISSING / OOB / UNANCHORED (counted, never fatal); `--briefs` for receipts, `--json`, `--selftest`; exit 1 while any rot stands. Its own falsifier held twice the day it landed (both seed rots fired live mid-landing).

**How to apply:** when writing dispatch briefs or receipts, anchor line-number pointers to a token; when picking up a ghost brief, re-check resolution FIRST and file a verification-only receipt if the target resolved (B2-356's rule). Related: [[flash-lane-burn-20260926]], [[no-fabrication-law-20260919]].

**Extension (build-fold-verify green pass, 9/27):** the rot species also lives in LEDGER code rows — code citations name SYMBOLS not line numbers, and one b2-34 anchor went ~120 lines stale in a single day. Standing falsifier pre-registered: a WARN-ONLY ledger anchor patrol (anchor rot in the ledger is invisible to the pointer_rot_check briefs mode because rows cite the file, not the range). Related: [[atlas-fix-queue-20260927]].
