# DRIFT PATROL - 2026-10-12

- class: RECEIPT
- writer: drift-patrol-cron
- automation: automation-a7c71ad1 (daily 08:00)

| check | result | verdict |
|---|---|---|
| backup exposure | **2 unpushed** - ratchet blocked (3 NEW debts) - accepted by name (register 1,018 claims, +3) - **push pending receipt commit** | IN PROGRESS AT FILING |
| fleet vitals | **SEVEN containers all healthy**: tortoise-db 32h, gstd-node 3d, sovereign 3d, mcp 3d, factorio 3d, worker/redis 3d | CLEAN |
| inbox fold integrity | refolded: 14,519 events - 4,161 items; INDEX derived fresh (patrol refold); verify race row = known class | CLEAN, LIVE |
| surface integrity | **record volume: 50 static drifts healed in one pass** (the frontier_olm_adhoc sweep filed 45+ files and the autoseal beats edited the usual suspects); 93 residual = in-flight flood classes, zero tampering indicators | TRIAGED (day 18) |
| link ledger | 8 duplicates on file (stable) | CLEAN |

## Ratchet ceremony: 3 debts, one of them ours

Accepted by name: `tools/gstd_accounts.py:63` except-pass + `tools/prepush_verkle_hermeticity.py:415` file-too-long (GSTD audit windows) + **`tools/suno_lane.py:171` env-key-read (SUNO_API_KEY)** - the suno lane reads its key directly from env instead of the vault fallback pattern the opencode keys use. Fix owed: route through the `_key` fallback. Register: 1,018 claims.

## Overnight: light and real

HERMES DIGEST lane fire 3: upstream release-integrity day (checksum-failed artifacts refetched, in-transit corruption flip-tested - trust-bytes upstream; new config keys must ship with docs - a borrowable docs-drift patrol twin). Scout daily quiet. Convergence, not gap.

**Top risks (boldest first):**
1. **Surface residual 93 and the heal pass healed a record 50** - the treadmill's input volume (frontier_olm_adhoc alone filed 45 files) makes single-pass convergence mathematically impossible; the autoseal-at-close fix (day 19 owed) is the only exit.
2. **suno_lane.py env-key-read is our own ratchet debt** - the lane the operator armed carries the exact anti-pattern the fleet keys-vault law forbids; one-line fix owed.
3. **X-INTEL dialect rows persist** (day 18) + event log 14,519 lines - the two compaction/design debts stay open.
