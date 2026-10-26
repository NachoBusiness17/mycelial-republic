# THE 50 · W9 · T44: Nightly vision batch automation

Filed 2026-09-19 by the T44 builder seat. Program list: `watch/inbox/THE_50_PROGRAM_20260918.md` W9 INFRA item 44 ("Nightly vision batch automation").

## What landed

The Mr Pool vision triage now has a standing, unattended nightly drain. Four pieces, all durable in the repo:

| Piece | Path | Role |
|---|---|---|
| Driver | `scripts/vision_nightly.py` | env check + coverage snapshot + fire plan; modes `--dry-run`, `--smoke`, `--run` |
| Engine | `scripts/vision_triage_pool.py` | unchanged; idempotent triage batches on the local sovereign lane |
| Wrapper | `scripts/vision_nightly.ps1` | schtasks entry point; venv python, correct cwd, START/END log markers |
| Wiring | `scripts/register_vision_nightly.ps1` | registers Windows Task Scheduler task `MagVisionNightly`, daily 02:30, /RL LIMITED |

## How it works

- `--run` (the nightly fire): checks ollama is up and `qwen2.5vl:3b` is served (loopback-pinned GET, same SSRF posture as the pool script), snapshots coverage, then delegates to `vision_triage_pool.py --run --lane local --batches 1` (up to 200 images per night, paced). Exit 0 on success; propagated pool exit code otherwise.
- Idempotent by construction: the pool skips msg_ids already in `vision_triage.jsonl`, so a complete corpus is an honest no-op receipt, and any new media dropped into `media_full/` or future error rows are drained automatically on later nights.
- Env not ready (ollama down): clean skip receipt, exit 0. An unattended cron must not error-spam; the receipt row is the alarm trail.
- Transport deaths (429/timeout) land in `vision_errors.jsonl`, never counted as verdicts (2026-09-19 law, upheld: the pool script enforces this).
- Every fire appends a JSONL receipt to `watch/inbox/mrpool_export/vision_nightly_receipts.jsonl` (json.dumps) and logs to `logs/vision_nightly.log`.

## Proof (all run during this ask, 2026-09-19)

1. **Dry-run** (no inference): `./.venv/Scripts/python.exe scripts/vision_nightly.py --dry-run` → exit 0, `ollama=ready`, `coverage=1980/1980 remaining=0`, plan printed, receipt row `mode=dry_run ok=true`.
2. **Live smoke** (one real inference through the pool's guarded POST, read-only): `--smoke` → exit 0, `msg_752.jpg` read by `qwen2.5vl:3b` in 29.6s, valid format head `TYPE: photo / SUBJECT: Dark room with a bright light shining through an open door.` No triage rows written.
3. **Real-mode guard**: `--run` with corpus complete → receipt `fired=0, note="corpus complete, idempotent no-op"`, exit 0.
4. **Scheduled chain end-to-end**: task registered, then `schtasks /Run /TN MagVisionNightly` → **Last Result: 0** (verified via `schtasks /Query /V`), Next Run Time 9/20/2026 2:30:00 AM, Status Ready, Enabled. Log shows wrapper START, driver run, `END exit=0`.
5. **Defect found and fixed during the wiring proof**: the first wrapper draft used `Tee-Object` into `logs/vision_nightly.log`; that held the file open (UTF-16) across the python run and collided with the driver's own UTF-8 appends (sharing violation, scheduled fire failed with a traceback). Fixed by making the driver the sole log owner; re-fired the scheduled task, Last Result 0. The failed attempt stays in the log as an honest trail.

## Coverage state at filing (measured, not assumed)

- `media_full/` contains 1,980 `msg_*.jpg`; `vision_triage.jsonl` holds 1,980 unique msg_ids; **remaining = 0**. The nightly is wired for when that changes.
- The 3 local-lane transport errors (msg 423/428/537, HTTP 500, in `vision_errors.jsonl`) are all present in triage (read by the seat directly, per `watch/inbox/RESUME_20260919_UPDATE_RECOVERY.md`).
- Context: `ledger_full.jsonl` has 3,663 msg_ids; 1,683 have no file under `media_full/`. The RESUME receipt's "2,011 denominator, 31 not locatable" is a different (harvest-time) universe. Full universe re-derivation from the ledger remains OWED to the next window (pre-existing debt, not this task).

## Test suite (real numbers, filed per fleet law)

Full `./.venv/Scripts/python.exe -m pytest -q` run this ask: **35 failed, 1464 passed, 9 skipped, 1 error in 1698.43s (28:18)**. Baseline census was 34 failed / 1305 passed / 9 skipped, summing to 1,348 tests (2026-09-14; corrected 2026-09-26 from the mis-copied "over 1,341 tests" total, which contradicts its own trio; the estate-wide 1,341 headline remains unreconciled against 09-14 bytes and is owed a real recount. Cause: wave-2 audit batch 8.3, `watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md`); the suite has since grown to ~1,508 tests. None of the 35 failing files reference this task's code (`grep -rl vision_nightly tests/` = no matches); the session's repo footprint is three new untracked scripts plus inbox receipts, no existing code touched.

## Operate

- Verify wiring: `schtasks /Query /TN MagVisionNightly /V`
- Fire now: `schtasks /Run /TN MagVisionNightly`
- Disable: `schtasks /Change /TN MagVisionNightly /DISABLE`
- Dry-run: `./.venv/Scripts/python.exe scripts/vision_nightly.py --dry-run`
- Live probe: `./.venv/Scripts/python.exe scripts/vision_nightly.py --smoke`
- Heavier drain (rare): `--run --batches 4` drains up to 800 images in one fire.

## Re-verified 2026-09-25 (second seat, read state then proved, no rebuild needed)

All four pieces intact unchanged (mtimes 09-19); no drift to repair. Proof run during this ask:

1. **Unattended fires confirmed, 6 consecutive nights**: `watch/inbox/mrpool_export/vision_nightly_receipts.jsonl` rows at 06:30Z (02:30 local) on 09-20, 09-21, 09-22, 09-23, 09-24, 09-25; every row `mode=run ok=true fired=0 note="corpus complete, idempotent no-op"`. The cron fires without a human; the no-op receipt is the designed behavior on a complete corpus.
2. **Scheduler state**: `schtasks /Query /TN MagVisionNightly /V /FO LIST` → Status Ready, Scheduled Task State Enabled, Last Run 9/25/2026 2:30:01 AM, **Last Result: 0**, Next Run 9/26/2026 2:30:00 AM, daily 02:30, task points at `scripts/vision_nightly.ps1`.
3. **Log chain**: `logs/vision_nightly.log` this morning shows wrapper `START` 02:30:02, driver `ollama=ready (ok); coverage=1980/1980 remaining=0`, `END no-op`, wrapper `END exit=0`.
4. **Dry-run proof (this ask)**: `./.venv/Scripts/python.exe scripts/vision_nightly.py --dry-run` → `ollama=ready (ok); coverage=1980/1980 remaining=0`, `DRY-RUN plan: fire=False batches=1 lane=local`, `END ok=1`, exit 0; receipt row `mode=dry_run ok=true` appended at 2026-09-25T20:46:53Z.
5. **Coverage re-measured independently** (not from driver output): 1,980 files matching `media_full/msg_*.jpg`; 1,980 unique `msg_id`s parsed from `vision_triage.jsonl`; `vision_errors.jsonl` still 3 rows (the known 09-19 transport errors, all re-triaged). Remaining = 0.

Verdict: still wired, still firing unattended nightly, dry-run green. The pre-existing debt noted above (1,683 ledger msg_ids with no file under `media_full/`) remains OWED and untouched by this re-verification.
