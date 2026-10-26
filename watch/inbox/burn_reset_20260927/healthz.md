# burn lane healthz — test_breach_returns_503 root cause + fix (2026-09-27)

Lane: 2/10 evening reset burn (watch/inbox/BURN_RESET_20260927_EVENING.md). Registered pre-existing failure (SUITE_BURNDOWN_20260927.md): `tests/test_healthz_status.py::test_breach_returns_503` failed `assert True is False`.

## Root cause

Defect was in the TEST FIXTURE, not the code under test. `backend/server.py` `semantic_health()` grades the trailing hour per the documented contract (module docstring, inline comment block, endpoint docstring all say "trailing hour"; rows older than now-1h are skipped: `if ts is None or ts < hour_ago: continue`). The test pinned breach rows at absolute `ts: 2026-09-12T02:00:00+00:00`. Once the calendar moved 15 days, every fixture row fell outside the 1h window, the grader correctly counted 0 in-window failures, and `ok` came back True. The absolute timestamp rotted; the breach path never returned a wrong code.

Byte proof (2026-09-27, direct call against `backend/server.py`):

- stale fixture (10 rows @ 2026-09-12): `ok=True, http_tool_fail_1h=0`
- fresh fixture (10 rows @ now-5min): `ok=False, http_tool_fail_1h=10`

Endpoint mapping is `status_code=200 if report["ok"] else 503`, so with a live breach the 503 path is correct; the test's own `test_status_tracks_ok_flag` exercises the real endpoint for the code-iff-ok contract.

## Fix

`tests/test_healthz_status.py::test_breach_returns_503` (test-only change; `backend/server.py` untouched):

- Breach row timestamps are now `datetime.now(timezone.utc) - timedelta(minutes=5)` so the fixture cannot rot again.
- Dated comment (2026-09-27) in the test names the rot, the contract, and the byte proof, per the fix-comment-carries-receipt rule. Contract unchanged; nothing weakened.

## Numbers

- Before: `tests/test_healthz_status.py` 1 failed, 2 passed (`assert True is False` at line 47).
- After (same file + neighbors `tests/test_launch_topology.py`, `tests/test_source_trace.py`): **16 passed, 1 warning in 1.83s**.
- Files touched: `tests/test_healthz_status.py` only (plus this receipt).
