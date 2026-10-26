# CHAIN_FIXES_APPLIED_20261019

Applied 2026-10-19 (America/New_York). Operator approved all 5 fixes from CHAIN_APPENDONLY_RESEARCH_20261019.md.
No git commit. No push. Live chain bytes unchanged (sha256 D887CCC223C97B311DA2C91A4F08AD0252A754EBED0DADDD605E665654F522B3). Chain file not rewritten or truncated.

## Per-fix status

| # | Fix | Status | Notes |
|---|-----|--------|-------|
| 1 | OS append-only ACL on verkle_chain.jsonl | done (soft) | DENY WD + grant RX,AD for foste; DENY D removed (Python open requests DELETE and broke reads). Other SIDs still (M). Container: Linux bind via Docker Desktop; NTFS ACL is host-side soft shell only. App-level gate is the real rail. |
| 2 | Gate v1 amend / _rewrite_chain / heal | done | Refuse unless MAG_ALLOW_CHAIN_REWRITE=1. v2 append path unchanged. |
| 3 | MAG_DISABLE_LAB=1 + recreate mag | done | docker compose up -d --no-deps --force-recreate mag. Env=1. No lab process in container. Port 8000 healthy (HTTP 200 /health). 8765 is host svchost Listen (parked; not Mag dashboard). |
| 4 | Daily prefix seal check in ratchet | done | tools/chain_prefix_seal_check.py hooked in scripts/ratchet_daily.ps1. Currently RED (expected; 24 rewrites on 10/17). No repair performed. |
| 5 | Fail-closed chain:biography lease + dry repair no lock | done | consolidate + live repair require lease+flag. chain_repair --dry skips verkle_lock. |

## What changed (file:line)

- mag/verkle_knot.py:73-82 _chain_rewrite_allowed / _refuse_chain_rewrite
- mag/verkle_knot.py:91+ _append_chain_line (ctypes FILE_APPEND_DATA on win32)
- mag/verkle_knot.py:749-752 _rewrite_chain gate
- mag/verkle_knot.py:1154-1156 v1 amend gate
- mag/verkle_knot.py:1195 uses _append_chain_line
- mag/verkle_knot.py:1242-1243 heal gate
- mag/verkle_knot.py:1304-1325 consolidate gate + chain:biography lease fail-closed
- tools/chain_repair.py:54-79 dry skips lock; live needs MAG_ALLOW_CHAIN_REWRITE=1 + lease
- docker-compose.yml:26 MAG_DISABLE_LAB: "1" under mag service
- scripts/ratchet_daily.ps1:39-45 prefix seal hook (exit non-zero on fail)
- tools/chain_prefix_seal_check.py NEW (read-only; n=12016 root ab595c33 candidate sha 0da8026d)
- configs/restricted_leases.json note on chain:biography (lease already existed from fda902344)
- tests/test_chain_rewrite_gate_20261019.py NEW (4 tests)
- tests/test_ah19_append_leaves.py v1 fixture sets MAG_ALLOW_CHAIN_REWRITE=1
- tests/test_chain_byte_exact_io.py test_rewrite_chain_writes_lf_only sets flag

## Backups

Directory: %TEMP%\magfix20261019\
BACKUP_SHA256.txt:
- 2d56c5c05bc9a038f55526fbcd076ce157372d96b228e5f0e30afae31e0d8785  mag\verkle_knot.py
- 074af25b004f96ce56128b29a56eec71a2b4eac4a16e9f247ae878275e37ac28  docker-compose.yml
- ee4ce88adf02ea29fe12078f9fed3fc4a751b1a4e41237952663dcc6d3c111b3  configs\restricted_leases.json
- a20402a8b8aaa5ad48e1b62f59512d512122db4aa747ebc80db50efc713f5aac  tools\chain_repair.py
- 363c230c9960ea24b4ca5996646b7b359c0b18fc76ce1dfc45dd983ee76490c8  scripts\ratchet_daily.ps1
- fb72bf046740cf1bf3ec9581e7e4379dc675da24c5aa34341ab120e37264f9d2  mag\leases.py (unchanged vs live)

ACL saves: verkle_chain.acl.save (pre-fix), verkle_chain.acl.save2 (after soft ACL).
Rollback: %TEMP%\magfix20261019\rollback.ps1 (restores code/compose/leases note, removes new tools/tests, restores ACL from acl.save, prints compose recreate hint).

## Proof: rewrite fails, append works

App gate (no flag):
- APP_REWRITE: PermissionError "chain rewrite refused (_rewrite_chain)..."
- pytest test_rewrite_chain_refuses_without_flag / test_v1_amend_refuses_without_flag PASS
- test_v2_append_still_works_without_flag PASS

ACL on TEMP copy with same soft ACL (DENY WD, grant RX,AD):
- APPEND_ACL_PROOF: OK (ctypes FILE_APPEND_DATA, 29 bytes)
- REWRITE_ACL_PROOF: OK PermissionError on open(..., "w")
- REPLACE_ACL_PROOF: NOTE os.replace still succeeds (ACL does not stop replace). App gate covers that path.

Live ACL (icacls):
- foste:(DENY)(S,WD) + (RX,AD); SYSTEM/Admins (F); several SIDs still (M) including CodexSandboxUsers.

Prefix check (expected red):
- PREFIX-SEAL: match=False live_prefix_sha=5dc56624... expect 0da8026d... FAIL prefix rewritten

## Lab state

- MAG_DISABLE_LAB=1 inside mag-sovereign (printenv)
- Processes: mag_launch.py, main.py api:8001, main.py dashboard, backend.server, mag.ghost:9000, mag.lane_runner, synthesis_agent.py. No lab.
- mag-sovereign healthy; 127.0.0.1:8000 /health -> 200
- Recreate used host bind mounts for memory/state; volumes persisted

## Test results

- tests/test_chain_rewrite_gate_20261019.py: 4 passed
- tests/test_ah19_append_leaves.py + test_chain_byte_exact_io.py + test_verkle_lock_heartbeat.py: 30 passed total with gate suite
- Live chain sha256 unchanged after all edits/tests

## Hostile pass (what we changed)

1. Soft ACL only denies WRITE_DATA for foste. Other (M) SIDs and Admins can still rewrite. os.replace bypasses file ACL (proven). Treat ACL as belt, not suspenders.
2. Docker Linux container does not see NTFS ACE the same way; container root can still os.replace via the bind mount. App gate + lease are the container-side rails.
3. MAG_ALLOW_CHAIN_REWRITE=1 is a single env bit; any process that sets it bypasses the gate. Lease on consolidate/repair is conflict-enforce only when heartbeat/lease infra is up.
4. Prefix check correctly goes red forever until a deliberate re-seal; ratchet_daily will exit 1 daily. Operators must accept red or re-seal after a known-good restore. Do not fix by rewriting the live prefix.
5. chain_repair --dry no longer takes the lock (good); a hostile caller can still race a live repair if they hold the flag+lease.
6. Lab disable is env-only at compose; image/code that ignores MAG_DISABLE_LAB would still spawn lab. Verified post-recreate: no lab cmdline.
7. AH19 v1 tests now set the rewrite flag in the v1 fixture; that is intentional so historical v1 behavior remains testable under operator flag.

## Reused vs new (staleness)

| Item | Reused/New | Staleness |
|------|------------|-----------|
| configs/restricted_leases.json chain:biography | reused (fda902344) + short note | lease schema current; note only |
| mag/leases.py guard/heartbeat | reused unchanged | backup matches live |
| scripts/ratchet_daily.ps1 schedule | reused; added prefix hook | last backup mtime 2026-09-25; hook is additive |
| verkle_lock / heartbeat tests | reused | 7/7 pass |
| tools/chain_prefix_seal_check.py | NEW | sealed constants from CHAIN_RESTORE_20261015 |
| tests/test_chain_rewrite_gate_20261019.py | NEW | covers refuse paths |
| _append_chain_line win32 path | NEW helper in verkle_knot | required for AD-only ACL |
| MAG_DISABLE_LAB compose | NEW env on existing mag service | applied via recreate 2026-10-19 |

## Rollback steps

1. powershell -File %TEMP%\magfix20261019\rollback.ps1
2. cd C:\Users\foste\Documents\projects\local_sovereign_agent; docker compose up -d --no-deps mag
3. Confirm icacls memory\biography\verkle_chain.jsonl matches pre-fix (no DENY WD)
4. Do not delete %TEMP%\magfix20261019 until verified

## Receipt paths

- watch\inbox\CHAIN_FIXES_APPLIED_20261019.md (this file)
- /workspace/mag-audit-20261019/CHAIN_FIXES_APPLIED_20261019.md (box copy)
