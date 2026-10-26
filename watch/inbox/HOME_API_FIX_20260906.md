# HOME_API_FIX_20260906 — /api/home un-break (docfix)

**Seat:** zcode (Sancho) · **Date:** 2026-09-06 · **Scope:** dashboard/rest.py
**Backup:** `dashboard/rest.py.bak-docfix-20260906` (pre-edit, byte-identical)

## Symptom
`GET /api/home` (and `/api/summary`, same handler `h_home_summary`, rest.py:880)
timed out (>12s from the browser, >6s curl) while every static page and several
other API routes served fine. Browser showed PROVISIONAL/DOWN. Dashboard server
lives in container `mag-sovereign` (host PID 9088 is com.docker.backend.exe, the
loopback port-proxy for 127.0.0.1:8765) — NOT a host python process.

## Diagnosis (piece-by-piece timing, 20s-capped subprocesses)
Timed inside the container (the true surface — Windows→Docker bind mount is the
multiplier; on native NTFS the same pieces run <1.5s total):

| piece | container | note |
|---|---|---|
| **residual dig-edge glob scan** | **20.9s** | reads+parses ALL 2,777 `memory/biography/residual/*.json` through the bind mount, INLINE in the handler |
| `ingest_bonds(write=True)` (only if BONDS_MD missing) | 7.3s | conditional; BONDS_MD currently present, so latent |
| `mag.health.sanity()` | 2.0s | bounded probes; also why /api/health costs ~1.4s |
| registry/economy/smoke/ideas/compose | <0.3s each | fine |

Steady-state handler cost ≈ 21s+ → every request timed out.

**Second culprit found (NOT fixed here — separate handler):** `/api/quota`
(`h_quota` → `models.quota.all_budgets()`) takes **31.7s in-container / 10.7s on
host** — it makes provider network probes with weak timeouts. It hangs today the
same way /api/home did. Worth its own docfix (timeout-guard or TTL-cache it).

**Server NOT wedged:** /api/health 1.35s OK, /api/verkle 0.32s OK — hang was
handler-specific, not the process. (ThreadingHTTPServer, so one slow handler
didn't block the others.)

## Fix (minimal, schema-identical — `mag_home_summary.v2`, 28 keys, zero diff)
In `dashboard/rest.py`:
1. Extracted the residual glob scan → `_home_dig_edges_scan()`.
2. New `_home_bg_refresh()`: runs `sanity()` + dig-edge scan on a daemon thread,
   publishes to in-process memory + `state/home_cache.json` (**60s TTL**;
   `state/` is bind-mounted so host and container share one cache file). Busy-flag
   prevents stampedes. The handler **never blocks** on the expensive pieces:
   fresh cache → last-known values → cheap defaults while the first refresh lands.
3. `ingest_bonds` when BONDS_MD is missing → moved to a background thread
   (`_home_bonds_ingest_bg`); handler proceeds with `load_bonds_json()`.
4. Added `import threading`.

## Verification
- **Equivalence (host):** old vs new handler payload — **0 keys added/removed,
  0 value diffs**; OLD 2.81s → NEW 0.16s.
- **Container (mag-sovereign, real FS):** cold call **0.72s** (was >12s hang);
  bg refresh lands ~22s later; warm call **0.36s** with real values
  (`health.status=degraded`, verify 4/6 — matches what /api/health reports
  in-container; in-container sanity has always read "degraded").
- Cache file `state/home_cache.json` written by the container process.
- Live routes sampled: /api/health 200 1.35s, /api/verkle 200 0.32s,
  /api/home **still times out** (see below), /api/quota still hangs (separate
  culprit above).

## ⚠️ RESTART NEEDED: YES (operator's call — not done)
The running `mag-sovereign` container's dashboard server (up 27h) holds the OLD
rest.py in RAM; python does not hot-reload. Until it restarts, /api/home keeps
timing out and the browser keeps showing PROVISIONAL/DOWN. The fixed code is
already on the bind-mounted files and verified working — one restart of
mag-sovereign (its windows/other services ride the same container, so the
operator decides when) puts the fix live. On restart there is no 21s cold spike:
first request returns in <1s (defaults or fresh cache file), real numbers land
~22s later in the background.

## Laws honored
backup-first ✔ · no daemons added (threads live inside the existing server) ✔ ·
no network calls introduced ✔ · running server not killed/restarted ✔
