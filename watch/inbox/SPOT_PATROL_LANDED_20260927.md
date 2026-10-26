# LEDGER SPOT-CHECK PATROL LANDED — 2026-09-27

**What landed:** `tools/ledger_spot_patrol.py`, the WARN-ONLY claim-vs-artifact instrument that adversarial-self-probes pass c (BURN_adversarial-self-probes_20260927_c.md) pre-registered after hand-verifying one LANDED row. It samples 3 LANDED rows per UTC day (deterministic day-rotation over the 329-row LANDED pool), mechanically checks every path-existence, sha256, and byte-size claim extractable from each one_line against disk, and appends findings to `memory/burns/SPOT_PATROL.jsonl`. WARN-ONLY by law: exit 0 unless the ledger is unreadable; it never edits the ledger.

**First runs (today):** default 3-row sample: 2 mechanical checks, 0 warns. Widened 12-row sample: 9 checks, 0 warns. Every path-existence check passed.

**The self-caught blind spot (fixed same session):** the first end-to-end sha test on B2-298-patrol-prompt-persistence surfaced a false-positive WARN class: the row's one_line names `configs/drift_patrol_prompt_a7c71ad1.txt` because it claims the file is ABSENT (the retracted duplicate), and a naive path-exists check treats any named-but-missing file as a mismatch. Fix: claim polarity. When a one_line carries an absence marker (absent/retracted/removed/not on disk/deleted), a missing named file is reported as info (absence-claimed, no warn); only presence-claiming rows warn. Post-fix B2-298 grades 5 checks, 0 warns: both live files exist, the retracted twin is correctly absent, and the sha256 claim matches `configs/drift_patrol_prompt.txt` exactly (95a514b061f49bea..., the same hash pass c verified by hand).

**Falsifier clock (pre-registered, starts today):** if two consecutive weeks surface zero claim-artifact mismatches AND no lane acts on a patrol warning, the patrol is vacuous overhead and reverts to manual probes. The greppable trail is SPOT_PATROL.jsonl.

**Scheduling:** none registered (scheduling is an operator call per fleet law). The patrol runs on demand: `.venv/Scripts/python.exe tools/ledger_spot_patrol.py` (or `--rows N`). Burn fires may include a patrol run as an in-distribution probe.
