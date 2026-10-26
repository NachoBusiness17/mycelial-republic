# Verkle Chain Summary - 2026-10-02

Fresh chain summary receipt. All evidence from this lane's own read-only runs
(instruments: ./.venv/Scripts/python.exe, git, ls). No state was edited.

## 1. Tip (warm boot)

Command: ./.venv/Scripts/python.exe -m mag.hermes_warm_boot
Output (verbatim):
  chain: index=8838 root=861e7f716c849df9... ts=2026-10-02T01:32:45.320677Z

Chain file: memory/biography/verkle_chain.jsonl (mag/hermes_warm_boot.py:32).
Rows: 8839 on disk (wc -l = 8839; parsed = 8839; last index 8838, 0-based).
First row ts 2026-08-12T16:41:39Z, last row ts 2026-10-02T01:32:45Z.

## 2. Health verdict: GATE RED - rows consistent, tip bookmark divergent

Command: ./.venv/Scripts/python.exe -m mag.hermes_warm_boot --verify
Output (verbatim):
  chain_verify: ok=False reason=tip root mismatch (tip aba227fda4da9e4b vs recomputed 861e7f716c849df9)
True exit code 1 (direct run without pipe; exit law at mag/hermes_warm_boot.py:255-256).

Breakdown (verifier: mag/verkle_knot.py:684-724, _verify_chain_consistent):
- Rows are internally consistent. Last-row check passed: row 8838's committed
  verkle_root 861e7f716c849df9 equals the recomputed merkle root over all 8839
  leaves. Also verified: row 8837's root equals prefix-8838 root (both
  0ba82d2811d1bb67) and row 8836's equals prefix-8837 root (both 4c4034deed3d169d).
- The TIP file failed (check at mag/verkle_knot.py:718-719):
  memory/biography/verkle_tip.json holds root aba227fda4da9e4b4481...
- The tip is a MIXED object, not simply behind: its n_leaves=8839 and its
  last_leaf_hash f58f0195... both match the current tail (comparison returned
  True), but its root matches NO prefix of the current chain (checked prefixes
  8837, 8838, 8839, the padded-8838 variant, and a scan window: no match).
  Its identity fields name the tail knot 2026-09-13_1225_biography_mag-agen_
  cd2a1f8c (session mag-agent-orc-t55072bb296), which IS row 8838 (an
  append-leaves re-save of a 2026-09-13 session dossier).
- Cause not attributable from bytes on disk. Candidate class: mixed-version
  concurrent writer (the race tools/chain_repair.py documents). OWED, not asserted.

Effect: append_verkle_knot refuses to extend an unverified chain
(mag/verkle_knot.py:810-813), so appends are refused until the tip is healed.
Chain file mtime Oct 1 21:54 EDT (01:54Z), tip mtime Oct 1 21:52 EDT; no
appends since (now 2026-10-02T14:07:46Z, ~12h13m quiet). Quiet is consistent
with refused appends but is not proof any append was attempted.

Sanctioned heal (NOT run: read-only lane):
  ./.venv/Scripts/python.exe -m mag.verkle_audit --fix
This calls repair_tip_if_consistent (mag/verkle_audit.py:351-355, def at
mag/verkle_knot.py:768), which re-derives the tip and refuses only on
row-root disagreement; rows agree, so the heal is expected green.
tools/chain_repair.py is the wrong verb here: its row scan would find no bad
row (row class is clean) and report a racy read.

## 3. Growth rate

Per-day row counts (ts census over the jsonl, this lane):
  2026-09-27: 896   2026-09-28: 947   2026-09-29: 125
  2026-09-30: 259   2026-10-01: 1057  2026-10-02: 87 (partial, to 01:32Z)
Last 3 complete days (09-29..10-01): 1441 rows, ~480/day.
The 10-01 spike (1057) aligns with the 20-wide burn and GAP ANALYSIS waves
dated 10-01 (commits 2cb1e2cf2, 5d2263f10 per git log); correlation only,
those commits do not name row counts.
Lifetime: 8839 rows over 2026-08-12..2026-10-02 (~51 days) = ~173/day.

## 4. Dangling / repair state vs the 2026-09-27 cure

09-27 baseline (commit 7b8617d78; mainline carries the same message as
18342ffd3 per git log): row 7937 pre-race root repaired under lock,
post-append self-heal guard landed in verkle_knot, tools/chain_repair.py
healed strike #2 (row 7980). Changes since (git log -- mag/verkle_knot.py):
- c98f23c44 (AG5): both main-path tip writes atomic (_write_tip_atomic);
  warm boot --verify really verifies; then-live 8645-leaf chain verified.
- T1W1 tickets 4+7 (2026-10-01; pinned by tests/test_t1w1_ractor_fixes.py,
  cited from mag/verkle_knot.py:690-700 and tools/chain_repair.py:87-92):
  the gate now fails closed on corrupt/absent/stale tips and binds n_leaves.
  Today's red gate is that fail-closed law working as designed.
- tools/tip_witness.py (W3, 2026-09-30): external gist witness exists but
  memory/biography/tip_witness_state.json is ABSENT = never published (tool
  header: PAT gist read ok, write denied 403). First publish remains OWED.

Read-only dangling census (this lane; jsonl filenames vs knots dir):
- All 8839 rows carry a filename; 56 rows' knot files are missing on disk.
- 0 rows flagged dangling; 618 rows flagged evidence_lost (the 2026-09-26
  B2-82 marker expected 620: memory/biography/verkle_repair_state.json).
- tools/verkle_dangling_repair.py (W3N 09-30; law pinned by
  tests/test_verkle_dangling.py:1-4) classifies dangling rows into an
  append-only side ledger; NOT run here because it writes. The 56
  unclassified missing-knot rows are OWED a classification run.
- state/organ_vitals_chain.json last ts 2026-09-26T00:57Z (6 days stale).

Manifest (the bones) is healthy and independent of the red tip:
./.venv/Scripts/python.exe -m mag.manifest verify -> "state": "committed",
"verified": true, manifest_hash 111fc776... equals anchored_hash.

## 5. OWED

1. OPERATOR: heal the tip via python -m mag.verkle_audit --fix (rows agree,
   expected green). This lane stayed read-only and did not touch state.
2. Attribution of the aba227 tip-root writer (mixed-version writer is the
   candidate class, unproven; no append-attempt log checked).
3. First tip_witness publish (PAT gist-write scope denied, tools/tip_witness.py).
4. Dangling classification run over the 56 missing-knot rows.
5. No alarm exists for this divergence in memory/attention.md (grep -i
   verkle/chain hits only tip_witness DIVERGENT response text, lines
   369/388/470); patrols watch tests, not the chain tip. A tip-health patrol
   may be owed.

## ADDENDUM (fold seat, 2026-10-02T14:3xZ)

The RED tip reported above was HEALED same-sitting: .venv/Scripts/python.exe -m mag.verkle_audit --fix (repair_tip_if_consistent) -> verify ok=True (8839 leaves). Incident + the main.py --fix no-op defect logged in memory/attention.md. Fold receipt: watch/inbox/full_width_fold_20261002.md.
