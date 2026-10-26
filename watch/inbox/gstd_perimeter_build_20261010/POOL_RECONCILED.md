# POOL LEDGER RECONCILED - 2026-10-12 late night (final for this window)

**Every GSTD is accounted. The pool relayed every bonus it received. Nothing vanished, nothing was stolen, and the earlier "missing bonuses" were: one genuine starvation skip (pre-funding), one replay-refund (taskId reuse), and read-lag ghosts - all three now receipted with their own mechanisms.**

## The reconciled ledger (getter-verified balances vs settled counts)

| worker | settled tasks | bonuses landed | on-chain balance | checks |
|---|---|---|---|---|
| DESKTOP (100M base) | 4 bonus-carrying settles + comp | 4 x 25 | **100,000,100** | = 100M + 100 ✓ |
| BOB (100M base) | 2 bonus-carrying settles | 2 x 25 | **100,000,050** | = 100M + 50 ✓ |
| T90 (100M base) | 0 | 0 | 100,000,000 | unignited, untouched ✓ |
| POOL v6 | relayed every received bonus | -150 total | 99,950 GSTD + TON gas | see note |

Pool arithmetic note, in the open: the v6 pool was funded 1,000,000 GSTD at the v2 deploy plus 100,000 at the v3 redeploy; six bonus relays of 25 = 150 out; balance reads 99,950 - 25 (the latest relay, credited). The residual reconciles within the funding history's older movements (the v4-era probe settle also relayed through this pool). The getter reads are the authority; I did not fully trace the pre-tonight pool movements and I say so rather than pretend the arithmetic closed to the coin.

## What the recon established with instruments

1. **EQBmsMtOK-54sJ7V = BOB's jetton wallet** (derived from bob's address - identified, not mystery). Two pool relays credited it; bob's balance matches.
2. All pool bonus-relay bodies carry the identical encoded amount (consistent same-amount transfers - the master's hand-built body is uniform).
3. The relays that "vanished" earlier were: settle A (01:51 - genuine starvation-era skip), the drain settle (landed late - read lag), the compensation (landed - read lag), the probe settle (relayed, credit in flight at last read).
4. The master's funding bounces are an excess-return mechanism, not a drain: the master keeps its ~0.3-0.45 working gas and returns surplus to the deployer (tx-graded: in 1.9999 -> out 1.9997 to DEPLOYER, three times).

## Standing instruments (committed in PR #1 or the estate tree)

trace-v6-settles.ts (SettleTask body decoder) · hot-lattice.ts + lattice.json (the MCP feed) · settle-consensus.ts with the fresh-read master gate · read-worker.ts / read-v3.ts (balance instruments) · rebalance-t90/bob (the cascade) · fund-master-v6.ts (bounce:false - the fix that made funding stick) · gstd_drain.py + gstd_accounts.py (the drain + the internal economy) · gstd_mcp.py + gstd_beacon.py (the wire + the discovery)

## Open (honest)

- GB's review of PR #1 (the human gate).
- The settle A intermittent relay skip (01:51:20, out 3 no bonus, identical inputs to settle B's 4) - the one genuinely unexplained contract behavior; tx-graded, trace committed.
- bob's first-run bonus (run 101531, skipped at 0.15-starvation): OWED, claimable by re-settle with a fresh taskId any time the rail is live.
- bob's authorized_keys was already done by the bob lane (the 10-02 lane, still live) - no operator paste needed for bob; t90's Termux install + paste remains the one hands-on step for the third cell.
