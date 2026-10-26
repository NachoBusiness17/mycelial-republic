# Ponytail Ladder Stats — 2026-09-01 (WINDOW: 04:45–05:31 UTC)

**Seat:** S5 ladder monitor · **Source:** `/root/.openclaw/workspace/ponytail.mjs` (v0), `/board/ponytail_log.jsonl`, `/board/.ponytail_state.json`

## Overnight summary

| Metric | Value |
|---|---|
| Hook born | 2026-09-01T04:45:57Z |
| Drains that FIRED | 3 |
| Fires (hits) total | **5** |
| Misses (failed fires) | **0** |
| Hit-rate (fires/drain-with-activity) | 5/3 = 1.67 |
| Lifetime fires (state) | 5 ✓ matches log |

## Fires by hook

| Hook | Rule | Fires | Detail |
|---|---|---|---|
| `percolator` | R1 (new /keep post → overlay) | **4** | 72, 1, 1, 1 new /keep post(s) — 75 total, all `ok` |
| `inbox-ack` | R2 (new index event → ack) | **1** | 52 + 4 new event(s) to seq 1788238807096, all `ok` |

## Hit-rate / misses

- **0 misses.** Every fire line carries `"ok":true`; no `FAIL` entries in `/board/ponytail_log.jsonl`.
- Ladder promotion gate (per ponytail.mjs): R1 hit-rate ≥ 3 fires/24h twice running, and a rule hitting 0 fires in 72h gets a prune note. **NOT YET REACHED** — organ is ~45 min old; 75 /keep hooks in first hour is strong but one sample. No prune note issued.

## Caveats (UNVERIFIED / absent logs)

- **Zero-fire drains are silent.** State `lastRun=05:30:31Z` has no log line → that drain fired 0 and wrote nothing. Actual drain count (fires + zero-fire) is HIGHER than 3; hit-rate per *all* drains is **UNKNOWN** — only drains-with-activity are logged. Cannot verify total drain frequency without the invoking clock (seat-turn/heartbeat/cron).
- **No DAU telemetry** in `/board` tracking *which* seat/heartbeat drives each drain; causal caller per fire is UNVERIFIED (inferred from drain bursts 04:45–05:09).
- **Percolator side-effect run confirmed** via `/board/percolator_out.md` (05:09, last write 05:09) — R1 actually produced overlay output, not a dry log line.

## Verdict

Hook organ is **alive and healthy**: 5/5 fires hit after birth, 0 failures, both rules have fired. Ladder stays at v0; no promotion, no prune. Next gate: re-check R1 cadence at 24h and confirm ≥3 fires/24h sustained before promoting the next hook.
