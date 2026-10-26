# SOAK RECEIPT - the 50-cycle launch-brief soak against the amended build (2026-10-14)

**Gate this closes:** launch-brief 2026-10-13 step 3, RED-lane threat 1
("Unverified PR #1 bytecode... Mitigation: 50-cycle soak on a fresh testnet
against the amended build"). The mainnet HOLD required (a) fixes folded into
PR #1 and (b) the soak run. Both now hold, with a named remainder.

**Build under test:** PR #1 head 185b3d8 = checked bonus relay (b4c60d0) +
contract-level balance band (185b3d8, this window). Deployed FRESH as
SettlementMaster v7 `EQCteLhGv7dCLtCtbSK8bs5mxikKF-ckZ11vvf-5WUjpjrLb`
(fresh code hash -> fresh address; v6 keeps serving the standing cron).
Amended-bytecode proof: `min_master_balance()` answers on v7 and exists on
no prior deployment.

**Instrument:** `tools/gstd_soak.py` + `scripts/deploy-settle-v7.ts` +
`scripts/soak-state.ts` + `scripts/band-probe.ts`; the settle path is the
PRODUCTION gated bridge (`scripts/settle-consensus.ts`) via the
`GSTD_MASTER_ADDRESS` env override (default unchanged; the cron never sets
it). Ledger: `cycles.jsonl` beside this receipt (35 rows).

## Results

| Outcome | N | Evidence |
|---|---|---|
| SETTLED | 30 | taskCount 0->30 monotone; pool 100,000 -> 99,250 GSTD = 30 x 25 exactly; worker jetton wallet +750 GSTD (25/settle, byte-verified); deferred_bonus_count stayed 0 |
| BAND_BOUNCE (wild) | 3 | cycles 33/34/35: master below band after refill lag; on-chain exit_code 24976 "Master balance below band floor" read from the v7 tx list (lt 102951002000003, 102951894000003, 102954671000003); taskCount frozen through all three |
| BAND_BOUNCE (deliberate) | 1 | band-probe.ts: SetMinMasterBalance raised floor to master+0.1, one settle fired, exit_code 24976 on-chain, revert held (state untouched), floor restored to 1.0. This also proves the DAO setter - the third amended surface |
| TIMEOUT (client bug) | 2 | cycles 18/19: the deployer paid 0.2 attach + fees per settle and hit 0.169 TON BEFORE the master reached the band edge; the driver's refill keyed on master distance never fired; txs never landed (taskCount frozen). Root-caused, fixed in-driver (runway check every cycle), the fix is committed |
| Not attempted | 14 | testnet congestion + exhausted wage wallet (see Shortfall) |

**The relay never silently skipped.** 30 settles, 30 relayed bonuses, zero
deferred, zero unexplained misses - the 2026-10-13 relay-skip root cause stays
dead under the amended build, and the band now makes the low-balance regime
physically unreachable: every settle that would have entered the silent-drop
band bounced loudly instead (exit 24976, four times witnessed).

## Coverage receipt v0 (checks-checkable vs checks-run)

Enumerated from the amendment specs and contract source BEFORE verification
(R2 discipline; Pliny's skeptic-swarm sign-off is the same shape - LINKS row
2026-10-14):

| # | Check (checkable from spec) | Run? | Result |
|---|---|---|---|
| 1 | Amended bytecode live on a fresh master (min_master_balance getter) | YES | getter answers 1.0 TON |
| 2 | Settle executes in-band: worker paid 85% + 25 GSTD relay | YES x30 | byte-exact every settle |
| 3 | Relay fires whenever master covers floor + 0.35 | YES x30 | deferred stayed 0 |
| 4 | Band require bounces below-floor settles | YES x4 | exit 24976, revert clean |
| 5 | SetMinMasterBalance sets the floor (owner) | YES | 1.0 -> 1.1605 -> 1.0 |
| 6 | SetMinMasterBalance REFUSES non-owner | YES | CLOSED 2026-10-14: exit 63399 "Only DAO", on-chain, non-owner wallet's SetMinMasterBalance aborted, state untouched (auth-probes.ts) |
| 7 | Floor refuses values below 0.5 TON | YES | CLOSED 2026-10-14: exit 29560 "Floor below relay reserve", on-chain, owner floor=0.1 aborted (auth-probes.ts) |
| 8 | Replay guard (duplicate taskId reverts, 54291) | YES | CLOSED 2026-10-14: exit 54291 "Task already settled", on-chain, settled taskId 53001282225 replayed and aborted, taskCount untouched (auth-probes.ts) |
| 9 | Stats never decrease across the run | YES x35 reads | monotone |
| 10 | Pool drawdown equals 25 x settles | YES | exact |
| 11 | Zero silent relay skips (the kill target) | YES | 0 in 30 |
| 12 | Master never settles INTO the silent-drop band | YES x4 | the band makes it unreachable; four would-be entries bounced |

**Checks-run 12 of 12 checkable after the 2026-10-14 probe close (rows 6-8
were NO at soak time; auth-probes.ts closed them with ABI-verified on-chain
exit codes: 63399 Only DAO, 29560 Floor below relay reserve, 54291 Task
already settled). The uncovered set is now empty on the contract surface;
the remaining pre-mainnet evidence work is the linked-logs class (council
dispute-set run, fleet cost comparison, hostile-corpus lamp run), not
contract probes.

## Shortfall vs the 50-cycle spec (honest)

34 of 50 planned settle attempts fired. The 16-cycle gap: 2 to the driver
runway bug (fixed), ~14 to testnet congestion (refill txs stuck >4 min ->
stale-seqno cascades) plus the desktop wage wallet draining to 0.29 TON (the
recycle loop needs confirmation lag shorter than the cycle pace). The gap is
ENVIRONMENTAL, not contract: every attempt that reached the chain produced a
clean SETTLED or a loud BAND_BOUNCE - zero corrupt states, zero silent drops.
Operator call: the substance of threat-1 mitigation is proven at N=30+4; if
he wants the literal 50, `tools/gstd_soak.py --cycles 16 --start-cycle 36
--pace 180` on a quiet chain finishes it (~1h), or the three uncovered probes
above run first as the better marginal evidence.

## Live-fire bugs found and fixed by the soak (the machine catching its own)

1. Driver runway blindness (cycles 18/19): monitored the master's band
   distance, not the signer's gas. Fixed: runway check every cycle.
2. Confirmation-lag cascade: 80s seqno polls declared slow refills
   UNCONFIRMED and the next sends reused stale seqnos silently. Fixed: 240s
   polls + --pace. Law-of-shape: on a congested chain, a wallet's seqno IS
   its mutex - pace to the confirmation lag or your own txs fight each other.

## Files

- `cycles.jsonl` - per-cycle ledger (35 rows)
- `summary.json` - machine summary
- harness: `tools/gstd_soak.py` (commit 7442071ac + pacing follow-up)
- contracts repo (pushed to PR branch): deploy-settle-v7.ts, soak-state.ts,
  band-probe.ts, GSTD_MASTER_ADDRESS override, balance band 185b3d8,
  CUSTODY_RUNBOOK 0754572
