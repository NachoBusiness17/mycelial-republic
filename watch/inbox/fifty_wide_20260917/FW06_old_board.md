# FW-06 — old fifty-wide boards marked SUPERSEDED (2026-09-28)

- Ask: annotate `watch/inbox/FIFTY_WIDE_BOARD_20260915.md` + `memory/plans/fifty_wide_20260915.md`
  SUPERSEDED with pointer to the 09-17 board (kills the 80 ghost refs).
- Bytes verified first: the two files are byte-identical (`diff` → empty), 76 lines each, and
  `memory/runs/fifty_wide/` does not exist (`ls` → No such file or directory) — so all 40
  `memory/runs/fifty_wide/*` pointers per copy (80 total) are dead, matching the 09-17 census.
- Landed: a `> **SUPERSEDED 2026-09-28 (FW-06, fifty_wide_20260917):**` blockquote appended at
  the end of BOTH files, naming the dead directory, the superseding board
  (`memory/plans/fifty_wide_20260917.md`) and the live receipts root
  (`watch/inbox/fifty_wide_20260917/`), and voiding the `memory/runs/fifty_wide/*` class.
  Append-only; original board text untouched (never-rewrite law).
- Note on "kills 80 ghost refs": the strings remain in the files by design (append-only), so a
  naive census still counts them; what the annotation kills is their STATUS — future readers
  hit the void disclaimer first, and FW-14's audit classifies the echo explicitly. The census
  echo mechanism itself is dispositioned in FW08_census_selfrefs_lineage.md.
- Checks run this session: `diff` of the two files (identical), `ls memory/runs/fifty_wide`
  (absent), tail-read of both files post-append (blockquote present).
