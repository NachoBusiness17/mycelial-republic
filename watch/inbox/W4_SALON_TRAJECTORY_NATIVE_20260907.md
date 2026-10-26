# W4 — SALON TRAJECTORY-NATIVE + THE VERTICAL METER (2026-09-07)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: salon_runner v5 seals trajectory rows fail-open and chain-safe (seal-test PASS), and the vertical meter projects 46–48 rows vs 1,300 required by Sep 20 (96.3 rows/day shortfall) — SUPPORTED (falsifiers PASS, dogfood step ids cited, tape verify PASS) · falsifier: a seal failure kills the run, the session chain forks under fan-out, or verify FAILs

Card: watch/WORLDLINE_SEED_20260907.md §7 + watch/TRAJECTORY_LENS_20260905.md build #4
and the Sep-20 vertical. Backup-first honored: **watch/salon_runner.py.bak-w4-20260907**
(taken before any edit). $0-local throughout — no lanes fired, no docker/config touched.

## 1. The hook — salon_runner v5 writes TrajectoryStep directly

`watch/salon_runner.py` gained ONE sealing organ, `_seal()` (~26 lines incl. comments),
plus 2 call sites. Lane/fold logic untouched — purely additive around the edges:

- **Post seal:** in `fan_out`, after each gated post survives and is written durably
  (`post_*.md`), one row: input = JSON {kind:"post", salon, brief_sha, shape, lane},
  output = {"chars": N, "survived": true}, timing.duration_s = the lane's own secs.
- **Fold seal:** in `fold`, after a lane clears the gate, one row: output = **verdict
  head capped at 4096 chars** (card law: verdict head; bash_local's OUTPUT_CAP backs it),
  input carries kind:"fold" + brief_sha + fold lane.
- **Chaining:** session_id = `salon-<name>-<YYYYMMDD>` — every step of one salon run
  chains into ONE session line (prev_step_hash → step_hash), via the W0 writer IMPORTED
  (`mag.bash_local.build_row` / `append_row` / `_rows` / `_last_hash_for_session`) —
  zero schema duplication, schema gate inherited (no schema_version = refuse).
- **Concurrency-safe:** module `_SEAL_LOCK` (threading) wraps read-prev+append, so the
  7-wide parallel fan-out cannot fork the session chain.
- **Fail-open house law:** the entire body is try/except; any sealing failure prints ONE
  stderr line (`[seal] WARN trajectory seal failed, run unaffected: ...`) and returns.
  A dead tape can never kill a salon.

## 2. Seal-test — falsifiers PASS ($0, no salon spent)

`python watch/salon_runner.py seal-test` (new subcommand): seals two fake posts into a
dedicated session (`salon-sealtest-<ts>-<date>`, isolated — no other session's chain is
touched), then drills the failure path, then runs the W0 verifier. Fired 09-07 via
`python -m mag.bash_local` (dogfood row step **81633d560e4a0f22**):

- sealed=2, well_formed=True (schema_version=1, step_hash, input, timing present)
- chained=True: c024f6477d8a3d00 → 1358ad4834b2a89b (genesis → S1 → S2)
- fail-open drill: `append_row` monkeypatched to raise OSError("simulated seal failure")
  → crashed=False, tape_rows 2→2 (no partial row), stderr receipt captured in the
  wrapper row's tool_result: `[seal] WARN trajectory seal failed, run unaffected:
  simulated seal failure`
- `python -m mag.bash_local verify` → PASS (all rows valid, chains intact)
- **VERDICT: PASS**
- Fold-cap microcheck (no tape write): 9,000-char verdict head → exactly 4096 chars,
  hash computed (step 2c4f636446a4c8c4 in the cap-check row's output).
- Tape after all W4 dogfood: **28 rows, 13 sessions, tip f41b6e2e26ba8c7c, verify PASS.**
  W4 added only: 2 seal-test rows (salon-sealtest session) + bash-local wrapper rows
  (their own bl-* sessions) — read-only on everything else.

## 3. The vertical meter — mag/vertical_meter.py

`python -m mag.vertical_meter` (or `--json`; `--tape/--today` for what-ifs). $0,
read-only, counts ALL sealed producers (bash-local + salon + every seat) — the fleet's
stream is one tape. Fired 09-07 through `python -m mag.bash_local` (steps
4d70c07887685083 human, c5e6e3f21b007079 json):

- rows today (2026-09-07): 25-26
- last 7 days: 25-26 rows (avg 3.6-3.7/day)
- days to wall (2026-09-20): 13
- required: 100/day flat = **1,300 rows** over 13 days
- projection at current pace: **46-48 rows** over 13 days
- **VERDICT: SHORTFALL 96.3-96.4 rows/day**
- Self-referential honesty: the meter's own dogfood rows move the count it reads
  (25→26 between the two runs) — the dungeon tip-hash gag again, now at rate.

## 4. Meaning

The salon is the fleet's first fully trajectory-native PRODUCER (build #4 LANDED): the
shape train now exhausts TrajectoryStep rows as a byproduct of thinking, same tape, same
schema, same chain as every other seat. What remains for the wall is RATE — the meter
says the salons alone won't carry 100/day; the workers' bash calls, refolds, rbn plays,
and meter pings all seal into the same line, so every seat grinding through
mag.bash_local is already on the vertical. 13 days, 1,300 rows, one tape.

Lines: salon_runner.py +~58 (26 organ + 6 hook sites + 26 seal-test; backup
.bak-w4-20260907) · mag/vertical_meter.py +122 new · tape +2 test rows.
