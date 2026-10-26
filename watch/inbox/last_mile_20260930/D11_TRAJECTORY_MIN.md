# D11 trajectory minimizer (2026-09-30)

Mission (operator, watch/inbox/last_mile_20260930): "derive the trajectory
and minimize it... learn as we go". The trajectory
(memory/trajectory/steps.jsonl) is the raw standing wave - every step every
agent takes. This lane built the minimizer: classify each step row
signal/noise using the receipts as ground truth, emit the minimal
trajectory + coverage stat, and extract the differentiator (what patterns
live in signal but not noise). FILE OWNERSHIP: `tools/trajectory_minimizer.py`,
`tests/test_trajectory_minimizer.py`, this receipt, plus the two run
artifacts named below.

## 1. What landed

- `tools/trajectory_minimizer.py` (400 lines, sha256 7bcf9dd347ab45f8) -
  spec-first docstring, then code. SIGNAL = three byte-backed prongs, any
  one suffices:
  - **P1 receipt_minute**: the step's ts (UTC) falls inside a minute cited
    by a receipt under watch/inbox (3,062 *.md read; 3,429 ISO-minute
    tokens; tz markers Z/+00:00/EDT/EST converted, bare token = UTC estate
    log convention; local `H:MM EDT` tokens anchored only to single-date
    filenames - 365 ambiguous ones skipped). **PRECISION LAW**: day-only or
    hour-only citations make NO row signal - a citation too coarse to
    contain a step cannot cite a step's timeframe (receipts exist on every
    wave day, so day granularity would mark the whole 38K wave signal and
    minimize nothing; hour granularity measured 74% - not minimization).
  - **P2 anomaly_named**: rows named by `tools/anomaly_flagger.py`
    (IMPORTED live via `af.scan_steps`, never copied - dogfood; "named
    row" stays owned by one tool).
  - **P3 milestone**: face == 'milestone' - the stream's own doctrine mark.
  Everything else is noise. Fail-closed: missing stream/inbox or an inbox
  with ZERO minute citations exits 2 (ground truth silently gone).
  Ratchet-clean: exactly 400 lines (the first 499-line draft was NEW
  file-too-long debt; fixed by compaction, not baseline).
- `tests/test_trajectory_minimizer.py` (15 tests, sha256 86b56e86dc54525f):
  tz-marker conversion (incl. the EDT sign bug the tests caught in draft
  one: west-of-Greenwich ADDs), single-date filename anchoring + ambiguous
  skip, day-only-never-signal precision law, three-prong classification,
  cluster merge/noise-break/milestone-standalone/bounded gists, coverage
  math, differentiator enrichment + min-count floor + degenerate split,
  CLI exit 0/2 paths incl. zero-citation fail-closed.
- Run artifacts (durable, shared inbox):
  `watch/inbox/last_mile_20260930/TRAJECTORY_MINIMAL.jsonl`
  (2,539 cluster entries, sha256 1cca29361bb02d84) and
  `watch/inbox/last_mile_20260930/TRAJECTORY_MIN_REPORT.json`
  (sha256 0b0274ba470c0189).

## 2. Live findings (run 2026-10-01T00:11Z snapshot, stream mtime same
moment, exit 0; census law - the stream is live append-only, counts are of
one moment)

**Coverage stat: 7.63% of the rows carry the wave's substance.**
- 2,952 / 38,683 rows signal (36 malformed rows included via P2) ->
  2,539 cluster entries (1.16 rows/entry; entries carry verb mix, exit
  pattern, <=5 bounded gists, <=3 receipt pointers - what was learned, not
  the raw bytes).
- Substance inside those 7.63%: milestones 22/22 (100%), anomaly-named
  rows 38/38 (100%), 117/355 distinct coarse instrument shapes (32.96%).
- Sessions: 695/1,555 carry signal; **860 pure-noise sessions** (55% of
  sessions never touched a receipt-cited minute).
- 1,336 distinct receipt-cited minutes found in 3,062 receipts.

## 3. The LEARNING - signal vs noise differentiator

Patterns IN signal that are absent/depleted in noise:
- **Signal runs the estate's own instruments**: `.venv/Scripts/python.exe`
  shapes are x2.32 enriched (9.36% of signal vs 4.04% of noise); git state
  inspection enriched (git status x2.64, git log x1.89, git grep x1.51),
  cp x1.79 (landing artifacts), timestamp capture x3.5.
- **Pure transport/platform plumbing NEVER gets receipt-cited**: wsl,
  findstr, gh have ZERO signal rows; docker x0.25, E="C: env plumbing
  x0.23, which/where x0.45, rm x0.4. What the wave "does to itself"
  (venv python, git, cp) is what receipts cite; what it "does to the
  platform" (wsl, docker, gh, findstr) is never cited.
- Signal concentrates in operator-local evening hours 16-21 EDT (top 5
  hours all in 16-21); noise spreads across the whole clock.

Honest negatives (features that FAIL to separate - findings, not failures):
exit!=0 (signal 6.0% vs noise 7.3%), truncated output (52.7% vs 50.7%),
command length median (285 vs 266 chars). The wave's failure/outcome
texture is uniform - what separates signal from noise is WHICH INSTRUMENT
and WHICH SESSION, not how a command looks or whether it failed.

**The differentiator in one line: signal is estate-instrument work
(venv python + git + landing copies) in operator-evening sessions; noise
is platform plumbing and routine reads - and outcome shape (exits,
truncation, length) carries zero signal information.**

## 4. Next-window hooks

- The 860 pure-noise sessions are the compression frontier: none of their
  rows need survive byte-level; a session-level digest suffices.
- Receipt citation concentration: 458 of the 1,336 cited minutes are on
  2026-09-26 (burn-wave receipts quoting timestamps en masse); the signal
  set inherits that day's weighting - known bias, byte-visible.
- A step-hash citation form exists nowhere in the inbox (0 of 3,429
  tokens): receipts cite TIMES, never step hashes - the minimizer's
  minute-join is the only join the receipts actually support.
