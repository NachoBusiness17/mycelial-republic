# P0 — 5 hanging endpoints fixed (honest-dark deadline)

Date: 2026-09-10. Lane B finding: `/api/status`, `/api/quota`, `/api/providers`,
`/api/overview`, `/api/loop-health` accept connections and hang forever.
File touched: `dashboard/rest.py` (backup: `dashboard/rest.py.bak_p0`).

## What was fixed

1. **Deadline wrapper** (`_dl`, rest.py just above `ROUTES`): every wrapped handler runs in a
   worker thread with a hard 5.0s deadline. On timeout it returns HTTP 503 with
   `{"ok": false, "stale": true, "error": "timeout", "last_known": <last good payload or null>}`.
   Successful payloads are cached per-endpoint, so after one good response, later timeouts
   degrade to stale data instead of nothing. Hung worker threads are abandoned (daemon pool,
   8 workers) — worst case a request waits 5s and gets honest-dark, never a hang.
2. **Wrapped in both ROUTES and LEGACY** (v1 + legacy aliases share the same handlers):
   `/api/v1/loop/health` + `/api/loop-health`, `/api/v1/overview` + `/api/overview`,
   `/api/v1/providers` + `/api/providers`, `/api/v1/quota` + `/api/quota`.
3. **`/api/status` was NOT defined — new stub added** (`h_status`): pure file-on-disk health,
   no container calls, no subprocess. Returns mtimes + ages for `state/CURRENT.md`,
   `memory/biography/verkle_chain.jsonl`, `queue/`, `watch/`, plus a `dark` verdict.
4. **`/api/loop-health` was NOT registered as a legacy alias** (only `/api/v1/loop/health`)
   — legacy alias added, pointing at the wrapped handler.

Root cause of the hangs (confirmed live during verification):
`models.providers.status_table()` and `models.quota.all_budgets()` hang on this box right now
(provider probes with no timeout). `loop_health.status()` and `api_overview()` are slow
(2.4-3.9s) but return. The wrapper turns all four shapes into bounded responses.

## Verification (all receipts fresh, 2026-09-10)

Unit: injected 8s sleeper through `_dl` → 503 honest-dark body at exactly 5.0s. PASS.

Curl against a fresh instance of the new code (127.0.0.1:8799), `--max-time 6`:

| endpoint | result | time |
|---|---|---|
| /api/status | 200 `{"ok": true, "schema": "status.v1", ...}` (file-based stub) | instant |
| /api/loop-health | 200 `{"ok": true, "schema": "loop_health.v1", "overall": "degraded", ...}` | 3.9s (dispatch) |
| /api/overview | 200, 3907 sessions payload | 2.4s (dispatch) |
| /api/providers | 503 `{"ok": false, "stale": true, "error": "timeout", "last_known": null}` | 5.01s |
| /api/quota | 503 `{"ok": false, "stale": true, "error": "timeout", "last_known": null}` | 5.01s |

All five RETURN. The two real hang sources (providers/quota) were caught by the deadline
live — the page degrades to honest-dark instead of hanging.

## Deploy note

The production dashboard on 127.0.0.1:8765 (PID 17192) still runs the OLD code — Python does
not hot-reload `dashboard.rest`. The fix goes live on the next server restart. Restart is
operator's call: that PID also listens on :8000 and :9000, so do not blind-kill it.
