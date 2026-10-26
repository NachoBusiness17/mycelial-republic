---
name: no-sacred-cows-execution-20260927
description: Operator "No sacred cows these were all the best ideas we had at
  the time" executed — daemon recycle (mixed-version writer race killed, 25 rows
  zero breaks), GROUNDING voids via v4 verbs with off-by-one misfire reversed by
  void-of-void (first live fire), suite 28/40 fixed, salvage split DONE
  (attic 100% structural orphans, verkle-chain family extension granted)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_bb9913b3-7c0e-45ff-9e15-d94e98cdb6aa
---

2026-09-27, the Socratic four-asks executed on the operator's grant
([[socratic-asks-four-laws-20260927]]). Receipt:
watch/inbox/NO_SACRED_COWS_20260927.md, commits 603ad91bf, c2082614b.

**1. Daemon recycle DONE + empirically proven.** The verkle chain had broken
TWICE the same day (rows 7937, 7980) — root cause class: **mixed-version
writers**: long-lived processes (ghost loop from 09:04, autorun loop from
12:52) hold verkle_knot code loaded at process start, so a post-guard code
change leaves stale writers racing current code on the shared chain file
(same-second appends, pre-race roots). Killed both, relaunched headless on
the repo venv. **Proof: 25 chain rows landed post-restart with ZERO breaks**
and the memlang order-pollution suite failures vanished. Arm C-200 untouched
per handoff. Mechanics learned: inline `python -c` through PowerShell
Start-Process dies on quoting — use launcher scripts (scripts/run_{ghost,
autorun}_loop.py shape: root sys.path bootstrap + the loop) on
.venv/Scripts/pythonw.exe; a duplicate uv-python twin spawned once — kill
non-venv duplicates, keep one per loop.

**2. GROUNDING_WAVE ablations EXECUTED via the v4 verbs** (delete-as-append
void + witness; the operator's verbatim word rode the witness evidence
field, seat "operator", zcode posting on that authority — provenance
transparent): void #122/#123 MALFORMED (the frozen truncated row + orphan,
the 09-16 staging), void #105 EVIDENCE_DEAD (the misnamed
privlidge_school_receipt png). **OFF-BY-ONE MISFIRE, caught and reversed**:
the test's failure messages print 0-BASED row indices; the dead pointer
lived on 1-based #105 but the void went to #104 (innocent fish-schooling
row) — reversed through the DESIGNED void-of-void path (SUPERSEDED,
witnessed): the reversal mechanism's first live fire, and it worked. Tests
updated to the v4 reader law (walk LIVE rows via _admission/_live_claim;
prev linkage honors _reanchor_ok) — 3/3 green, xfail marks removed.

**3. Salvage split DONE (lane returned):** attic census
(lens_20260927/ATTIC_ORPHAN_CENSUS.md) — 527,826 file members across 17
sealed tars, **100% structural orphans** under the strict 9-shape registry
(every family snapshotted at relocated/flattened roots) — but 95.2% of mass
in 3 families: biography verkle knots 204k = the verkle_chain backing store
one root-relocation from its claimed shape (38.7%), Mimosa hook-state
baselines 160k hash-named sources (most of the bytes), ghost leak reports
138k (the LANE4B unversioned-risk class). **Operator granted "Family
extension"** for the verkle-chain family (drops attic to 68.3% orphan);
the one-line shape_map FAMILY_CLAIMS edit is owed to the next batch —
hooks refuse compound Bash edits on mag/ sources, use Read+Edit.
Manifest cross-check found the hook-state manifest counted dirs not files
(understates by 5 orders of magnitude); cards_backup unmanifested.
Valued-orphan call + the hook-state/leak-report disposition stay operator's
(seat recommendation: claim knots, leave the other two unclaimed until
something reads them).

**Suite final: 28 of the morning's 40 honest failures fixed outright, 0
xfails, 12 remain** (desk_baseline_probe 6 = dashboard spec reconciliation,
+6 one-dig singles, all root-caused in SUITE_BURNDOWN_20260927.md). Earlier
in the arc: verkle chain race repaired twice + standing
tools/chain_repair.py verb + post-append self-heal guard in verkle_knot
(recompute from DISK rows under lock, heal own row); water_computer's 5
failures were a NEVER-WIRED engine-module seam (handle() had zero callers —
_MODULE_HANDLERS dispatch + boil/freeze parser verbs landed; the test's `or`
short-circuit on a harmless look hid the unparseable verb); frontier tests
were reading the LIVE weekly allowance ledger (burn week really spent the
frontier caps — now pinned hermetic).

**Why:** the day proved the estate can repair its own record (chain, ledger,
daemons) with receipts and designed reversals instead of ceremony — and that
gating was mostly timidity.

**How to apply:** (a) after landing any change to shared-file-writing code,
RESTART the long-lived writer processes — stale in-memory code is a standing
race; (b) before voiding/burying a row named by a test failure, CHECK the
index base (test messages are often 0-based; ledger verbs often 1-based);
(c) when a void misfires, the reversal is void-of-void with SUPERSEDED +
witness — use it, don't hand-edit; (d) failure output that "disagrees" with
a direct probe may be a print-side filter (one debug pass printed only
line:-prefixed void keys and hid the hash-voids). Related:
[[gate-fix-lens-20260927]], [[socratic-asks-four-laws-20260927]].
