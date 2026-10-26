# B2-408 _log_seat_crash swallows write failures silently (SW-07, 2026-09-26)

## Verdict

LANDED. mag/agent_cli.py _log_seat_crash's bare `except Exception: pass` is replaced with a failure recorder: a loud console line naming the stage, the sink and the error ("CRASH LOG WRITE FAILED ... this crash is NOT logged; failures so far: N") plus the importable module-level CRASH_LOG_FAILURES counter (count, last_error, last_sink, last_stage) that a census or doctor surface can read instead of re-deriving. Probe executed both directions: a successful append still prints the old success line; an unwritable sink (MAG_SEAT_CRASH_LOG under a path whose parent is a file) now records count=1 with the stage, sink and error on both surfaces.

## Evidence file:line quotes

- QUEUE.md row: "the writer wraps the append in except Exception: pass, so a sink that cannot be written (MAG_SEAT_CRASH_LOG pointed at an unwritable path, disk full, permissions) drops every crash with no surface naming it; the B2-358 env tripwire warns only that the variable is SET, never that its target failed, and the seat-crash-guard console line names the log only on success".
- Pre-fix bytes: `except Exception:` / `        pass` at the tail of _log_seat_crash (mag/agent_cli.py:2524-2525 pre-edit).
- New comment (fix-comment law): "FIX 2026-09-26 (B2-408). CAUSE: the bare `except Exception: pass` swallowed sink write failures ... EVIDENCE: pre-fix, pointing MAG_SEAT_CRASH_LOG at an unwritable path and crashing the seat printed nothing anywhere".
- Probe transcript (post-fix): `[seat-crash-guard] CRASH LOG WRITE FAILED: stage=probe_stage sink=...AGENTS.md\nope\crash.log error=FileExistsError(17, ...) -- this crash is NOT logged; failures so far: 1` and `counter: {'count': 1, 'last_error': "FileExistsError(17, 'Cannot create a file when that file already exists')", 'last_sink': '...', 'last_stage': 'probe_stage'}`.

## Work done

- mag/agent_cli.py: except block records CRASH_LOG_FAILURES (module-level dict) and prints the loud failure line; claim line appended before the edit (21:31:38Z, file working-tree-modified, rebased on fresh bytes).
- No production crash path was fired for the probe; the harness called _log_seat_crash directly with a synthetic exception against an unwritable sink.

## Falsifier

The brief's falsifier ("point MAG_SEAT_CRASH_LOG at an unwritable path, crash the seat, and show nothing anywhere records that the crash was not logged") is falsified by the probe: the console line and the counter both name it. Reopen if: the counter exists but no census/doctor surface ever reads it AND a sink failure recurs unnoticed (the importable counter is the designated surface; wiring it into the doctor row is the follow-up if a real failure appears), or the except block reverts to pass.

## Bibliography closed

Read: mag/agent_cli.py (_log_seat_crash + call sites 2685/2713), mag/env_redirect.py and watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md (referenced via the row's claim about the tripwire's scope), QUEUE.md B2-408 row, probe transcript. No external sources.
