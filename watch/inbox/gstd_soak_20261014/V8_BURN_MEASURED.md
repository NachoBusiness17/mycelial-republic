# V8 BURN MEASURED - the fountain fix proven on-chain (2026-10-14)

SettlementMaster v8: EQArRbzf9lhdzIytV_DuROSWzdWvkCo1KVrjrsoMhVsUdQTu
(testnet, fresh deploy from PR head, funded 2.5 TON, pool 100K GSTD).

## The measurement (5 settles, master balance read before/after each)

| settle | worker state | master net |
|---|---|---|
| 1 | COLD (rep=0, jetton wallet deployed by this settle) | **-0.2014** TON |
| 2 | warm | **-0.0515** TON |
| 3 | warm | **-0.0515** TON |
| 4 | warm | **-0.0515** TON |
| 5 | warm | **-0.0515** TON |

All five: "PHASE4 BABYSTEP1 PROVEN - worker +25 GSTD" - the relay fired
every time, zero silent skips, pool 100,000 -> 99,875 (25 x 5, byte-exact).

## What it means

- The two-tier relay works exactly as designed: the cold first settle pays
  the 0.3 deploy gas, every warm settle after pays 0.15. Master burn rate
  dropped 4x (from -0.20/settle to -0.05/settle).
- The funding trigger question ("why fund it before the economics work")
  now has its number: at -0.05/settle warm, a 2.2 TON float covers ~40
  settles; at the standing cron's cadence the wage recycle (sweep_wages)
  covers the loss many times over. THE FOUNTAIN IS CLOSED.
- The operator's 2-TON-every-few-hours experience was v6/v7 at -0.2 to
  -0.25/settle with no recycle. Measured, fixed, measured again.

## Remaining

- v6 -> v8 cron cutover: the standing drain still targets v6 (old
  bytecode). Decision owed (v8's reputation map starts fresh).
- Batching one relay per N settles: the next lever, client-side, takes the
  warm cost per delivered bonus down further.
- Mainnet trigger status: unit economics now measured and survivable; the
  external-payer leg remains the real business unlock.
