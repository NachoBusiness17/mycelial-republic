# M1 — CHAIN JANITOR FIX + KNOT LANDING REPORT

Date: 2026-09-11 · Lane: Mickey 1/7 · Worker: zcode seat · Bounds kept: 1 file changed (mag/verkle_audit.py), this card.

## THE POINT
The chain's one auto-healer (`verkle_audit --fix`, run by the ghost self-heal quest,
mag/ghost.py:1458) was firing at a flag that did not exist. Worse: the audit module had
NO `__main__` guard at all, so `python -m mag.verkle_audit --full` — the exact subprocess
governor_autorun.py:537 runs — imported the module and exited 0 doing NOTHING. The audit
itself was a silent no-op from the `-m` lane. Both are fixed. The retro-knotter CANNOT
land the 21,479 staged knots: it does not exist as code, only as a staging spec, and its
own gate (append lock + truth witness + operator GO) is not yet in force.

## WHAT WAS BROKEN (three defects, one file)
1. `--fix` flag referenced but never implemented — ghost.py:1458 and framework_map.py:205
   both instruct running `python -m mag.verkle_audit --fix`; argparse would reject it.
2. Missing `if __name__ == "__main__":` guard — `python -m mag.verkle_audit` (any flag)
   produced zero output, zero report, exit 0. Callers could not tell no-op from success.
   This is exhibit #2 of the except-pass silent-drop class Lane 8 flagged.
3. (Not broken, found live:) the tip bookmark had drifted again since the 09-11 repair —
   chain at 7,511 leaves while the bookmark still held 7,377/8bd58896.

## WHAT I FIXED (mag/verkle_audit.py only)
- Added `fix: bool` to `run_audit()`; when set it calls the SANCTIONED
  `mag.verkle_knot.repair_tip_if_consistent()` — the exact repair executed 09-11. That
  function proves chain rows are internally consistent first and refuses to touch
  anything if the last row disagrees with the recomputed root; it only heals the stale
  tip bookmark. Chain rows are never rewritten, reordered, or dropped.
- Added `--fix` to the argparse CLI (docstring updated).
- Added the missing `if __name__ == "__main__": raise SystemExit(_cli(None))` guard.
- Exit code is now 1 when `--fix` runs and the repair refuses (integrity failure
  surfaces to callers instead of vanishing).

## RECEIPT (verification run, 2026-09-11)
`python -m mag.verkle_audit --fix` from repo root:
```
ok: True
fix.ok: True | fix.repaired: True | n_leaves: 7511 | root: 58192672...
tip.n_leaves: 7511 | tip.root: 58192672...
gaps: 1
exit=0
```
The first real run of the flag did real work: recomputed the Merkle root from all 7,511
leaf hashes, verified the last chain row against it, and healed the drifted tip bookmark
in place. Backup-first honored by design: the repair path refuses chain mutation and the
tip is a 494-byte pointer (prior backup convention: verkle_tip.json.bak-poisoned-20260911).

## WHAT THE RETRO-KNOTTER WOULD DO (and why it cannot land yet)
Source: watch/inbox/RETROKNOTTER_PREP_20260911.md (read in full). Findings:
- THE SCRIPT DOES NOT EXIST. The retro-knotter is a staging SPEC — fold order, amendment
  stamp format, falsifiers — not code. Nothing appends today.
- DRY-RUN MODE: none exists to run. The spec's dry-run equivalent is "Step 0 — partition
  recount": a read-only walk of memory/biography/knots/ applying the fold-eligibility
  gate (file exists, date-prefix in class range, 8-hex tag matches no current-chain
  leaf_hash AND filename in no chain row). The cycle-genetics note demands Step 0 be
  produced as its OWN counted artifact — it has not been run yet. The mission's two
  class counts (2,960 all-files census vs 13,693 never-referenced census) overlap
  imperfectly and would double-fold hundreds of knots without it.
- IF BUILT AND GATED, it would fold the 21,479 off-chain knots in three classes,
  appended at the current tip (now idx 7,511+), never inserted mid-chain, never
  backdated (ts = fold moment; history lives in original_ts + filename):
  - Class 1 FIRST: the 2,960 silence knots (Aug-16..31), kpi.jsonl as independent
    second witness; 16 zero-byte/corrupt files recorded as gaps, not folded.
  - Class 2: remaining dated orphans (~10,733 backlog + 1,452 cut survivors whose
    original rows survive verbatim in biography_backup_20260830 — byte-faithful restore
    of original leaf_hash/ts). The 304 absent + 18 missing files stay unrecoverable;
    the fold does not fabricate.
  - Class 3 LAST: the 15 kpi-only leaves (counts 6,662-6,676) via dossier_commit path;
    dossier absent = documented GAP row, never an invented hash.
  - Every folded row carries `recovery: {stamp: recovered-2026-09-11, class, witness}`.
- THE GATE (spec §1, hard): no append until (A) a single append lock
  (verkle_chain.jsonl.lock, exclusive, held across read-tip→hash→append→fsync, stale-lock
  rule, sequence fence) covers EVERY appender incl. mag/records.py and
  mag/grounding_wave.py::post (which today has NO lock), AND (B) a second-witness truth
  gate verifies each row (or at minimum every PASS is renamed LINKAGE-PASS), AND
  (C) operator GO lands. Falsifiers: byte-prefix invariance of rows 0..7,376, zero
  duplicate leaf_hash/verkle_root/filename chain-wide, 100% tag-to-file hash binding,
  count reconciliation, 100% stamp census.

## STATE OF THE CHAIN AT REPORT TIME
7,511 leaves, tip root 58192672..., bookmark now synced to the chain. 1 verkle gap open
(the count-reconciliation warning class). Chain appends flowing.

NEXT: Build the retro-knotter Step-0 partition recount as a read-only script — walk
memory/biography/knots/, apply the fold-eligibility gate, emit a counted partition file
(per-class true counts + per-file eligibility) as its own artifact.
SPAWNABLE: step-0 recount is read-only, one script + one output file, no chain writes,
no GO needed — fits one agent in ~15 calls. The append-lock (spec §1 Requirement A) is
the task after it and is ground-truth surgery on the chain append path — that one needs
its own careful lane, not a Mickey.
