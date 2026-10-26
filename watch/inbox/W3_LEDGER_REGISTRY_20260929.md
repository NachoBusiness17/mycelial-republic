# W3 — LEDGER REGISTRY (2026-09-29, re-fire of the 1302-dead lane c7db541d)

The return 19 improvement, landed: ONE CHAIN LAW, SEVEN PRIVATE IMPLEMENTATIONS → one
mount table. The registry runs each chain's OWN verify (no eighth referee), mounts four
families today, files idempotent nightly-canary attention alerts in the gap_sentinel
shape, and ships the cross-ledger query-by-hash stub.

## Files (this lane's ownership; nothing committed)

- `tools/ledger_registry.py` — NEW, 384 lines, ratchet-clean (violation_ratchet check
  --changed raises no claim for it; the two NEW file-too-long claims it does raise are
  sibling lanes' duel_harness.py / regen_front_door.py, untouched here).
- `tests/test_ledger_registry.py` — NEW, 8 tests.
- No production surface touched: `verify` mode is read-only over the estate.

## The mount table (copy N+1 becomes one entry dict)

| family | chains on disk | own verify used |
|---|---|---|
| wow_player | `memory/runs/wow_player/ply-*.json` | `mag/wow_player.verify_file` |
| gwap | `memory/runs/gwap/*.jsonl` | `mag/gwap_payload.verify_chain_file` |
| server_world | `logs/world*.jsonl`, `memory/runs/server_world/*.jsonl` | `server/world.load_log_rows` |
| verkle | `memory/biography/verkle_chain.jsonl` | via its guard `mag/chain_guard.check` (the ask's law — no side door) |

## Real test line

- `pytest tests/test_ledger_registry.py -q` → **8 passed in 0.63s** (fixtures ok,
  corruption caught per family by its own verify, canary idempotent byte-identical,
  exit ladder 0/1/2, verkle-via-guard wiring, query hit/miss).
- Adjacent guard: wow_player + gwap family + server v0 + cast + chain-contract +
  gap_sentinel + registry = **84 passed in 11.90s** and **19 passed in 1.07s** slices.

## REAL verify_all (2026-09-30T00:48:45Z, exit 1)

```
family wow_player — 2 chain(s)
  OK   memory/runs/wow_player/ply-6f93762afaa7.json rows=7 tip=6e50298690cbb218 OK
  OK   memory/runs/wow_player/ply-da9cfc91a7d7.json rows=4 tip=1b137efd6dcbb604 OK
family gwap — 3 chain(s)
  OK   memory/runs/gwap/b3-demo-clean-20260929.jsonl rows=2 tip=a283f6c95f71dce0 OK
  OK   memory/runs/gwap/b3-demo-collusion-20260929.jsonl rows=2 tip=8d5ace0d23d16522 OK
  OK   memory/runs/gwap/mud-demo-20260929.jsonl rows=1 tip=2bf39201fc862935 OK
family verkle — 1 chain(s)
  FAIL memory/biography/verkle_chain.jsonl rows=8437 tip=d735b7142414cc75 regression
TOTAL chains=6 failing=1
```

## First real readings

1. **VERKLE REGRESSION IS LIVE**: its own guard reports state=regression — 300 dangling
   rows lack the evidence_lost flag (371 dangling, 618 flagged; marker 2026-09-26).
   tip_matches_chain=True, no CRLF, no dup sessions: the pre-repair-restore/flag-stripping
   class the canary was built for. `canary` mode files exactly one attention alert for it
   (key carries the detail, so it never re-files while stable); not filed by this lane —
   the ask scoped the real run to verify_all, the nightly step is the operator's.
2. **server_world mounts ZERO chains**: the server writes a log only where --log points;
   the only world chains on disk are 44 throwaway `agents/pytest-tmp-*` fixtures,
   deliberately not swept (fixture churn is not estate truth). Production tapes belong in
   `logs/` or `memory/runs/server_world/` — reprint-lane tapes currently live only inside
   tests.
3. **Query stub proven live**: `query --hash a283f6c95f71dce0` → gwap
   b3-demo-clean-20260929.jsonl row 2 row_sha256 (full hash returned), exit 0.

## Laws stolen-and-credited

- Idempotent alerting (jsonl single-writer first, attention.md best-effort second,
  B2-465 multi-writer law): `tools/gap_sentinel.py` verbatim shape.
- Mount/singleton surface modeled on `mag/chain_query.py` (`FAMILY_BUILDERS` +
  `default_families()` = the mount table; `verify_all()` = the read surface).
- Registry never reimplements verification: ImportError from a family's verify module =
  exit 2 cannot-verify with NO alert (registry broken ≠ chain broken).

## Debts (v1)

- party_subchain + tesuji_map not yet mounted (return 19 named seven implementations;
  each becomes one more entry dict in `FAMILY_BUILDERS`).
- Query stub covers top-level row hashes only; nested evidence hashes (gwap
  `meter_credit.receipt_sha256`) and an index are v1.
- No scheduled task yet for `python tools/ledger_registry.py canary` (nightly 08:30
  patrol lane is the natural host — operator call, same as WARN-arm decisions).

## Run

```
.venv\Scripts\python.exe tools\ledger_registry.py verify
.venv\Scripts\python.exe tools\ledger_registry.py canary
.venv\Scripts\python.exe tools\ledger_registry.py query --hash <hex-prefix>
```
