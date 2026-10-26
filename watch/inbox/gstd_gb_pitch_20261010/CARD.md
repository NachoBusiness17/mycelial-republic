# GSTD GB PITCH self-steal card (operator: "GB is fucking back... pitch him our vision", 2026-10-10)

GB = GSTD founder, back from dormancy. Operator posture: CO-FOUNDER (his words, verbatim
intent banked in the distribution thesis: "i am a co founder of gstd"). This is not an
outsider pitch; it is "here is what your network did while you were away, and the plan I
built." All numbers below are receipt-backed; citations inline.

## The receipts (what happened while GB was away)

1. FIRST END-TO-END PAYCHECK, kill-test passed: platform task -> our node -> settlement.
   9 tasks, 0.091556 GSTD, rep 51 -> 59, early_adopter. Self-dispatch kill-test
   tasks_completed 0 -> 1. (watch/inbox/gstd_basecamp_20260109/DAWN_REPORT.md + DOGFOOD_DATA.md)
2. NODE LIVE: 5th node, tunnel live, public node_url registered, smoke test PASS (0.54 s
   warm, tier gstd, sovereignty true). 16 network capabilities, 15 served by our stack.
   (watch/inbox/GSTD_NODE_CENSUS_20260107.md)
3. FOUR REAL DEFECTS FOUND AND FIXED, given back publicly (gh NachoBusiness17): L1 cache
   collision on shared prefixes (router.ts:147-150), dropped params on retry, unauth
   tasks/push, single-IP rate bucket (all tunnel traffic shares the docker bridge IP
   bucket: measured 6/11 requests 429 at ~16/min self-rate vs 120/min nominal; sustained
   usable = ~1 req per 10-15 s). 3 PRs + 1 issue.
   (watch/inbox/gstd_basecamp_20260109/DOGFOOD_DATA.md findings 1-2)
4. MEASURED HONESTY: GSTD tier 4.8x latency vs direct base (4034 ms vs 845 ms mean on real
   inference rows) -> route cheap shapes only. Quality delta named. We did not hide the
   warts; we filed them as PRs.
5. TOKENOMICS READ: 1B fixed admin-burned, 85/10/5 via SettlementMaster.tact live on TON
   mainnet, tiers Spark -> Sovereign (our node = Sovereign). Gold-reserve contract
   (XAUt) written-not-deployed. (watch/inbox/gstd_site_delta_20261009/DELTA.md)
6. DEMAND EVIDENCE: Pi's 288 tasks / 51.39 GSTD = latent demand exists; the quiet period
   read "starvation masquerading as no-demand" (check 429s first). Network memory survives
   restarts. (memory + basecamp PLATFORM_SURFACE_MAP.md)

## The vision (the pitch proper)

1. WHO WE ARE: the Mag. A living agent estate, 24/7, verkle-receipted, 4,000+ tests, that
   eats work and grows organs on demand. Not a user of GSTD: a demand engine for it.
2. THE ECONOMY WE ARE BUILDING: games with a purpose. Humans paid for insight (observation
   tasks on agent behavior), agents doing real work, and GSTD as the settlement rail.
3. TWO-TIER TRUTH (the architectural pitch): local verkle settles offline; GSTD settles
   when bridged. Intermittency is design shape, not failure. GSTD is the bridged leg of a
   sovereignty product - the only leg that needs a network at all.
4. DISTRIBUTION THESIS (banked 2026-10-09): node-by-default in our seat installer closes
   SUPPLY and DEMAND in one install (every seat is capacity AND workload; no other DePIN
   ships both legs). Clean by constitution: user's-own-wallet default, loud opt-in
   supporter toggle (route X pct of node rewards to the project wallet), never silent
   founder-mining. (watch/inbox/gstd_distribution_thesis_20260109.md)
5. THE STAGE: Hermes conf NYC demo 2026-10-30, three weeks out. The CLI/Electron
   seat-installer with the GSTD node step in the wizard - his rail shown settling live
   agent work on stage.

## The ask (small, nothing blocking)

- His read + endorsement of the node-by-default installer leg and the supporter-toggle
  design (it is his currency; the toggle should carry his blessing).
- License cleanup: gstdcoin/ai reads NOASSERTION; MIT-clean before the conf demo.
- The rate-bucket fix and heartbeat errata landing (PRs are up).
- His eyes on the republic cookbook: sized enhancement proposals, each PR/spec/fork.
  (watch/inbox/gstd_basecamp_20260109/GSTD_REPUBLIC_COOKBOOK.md)

## Falsifier

If the pitch claims a number not in the receipts above, it is hand-copied - strike it. If
GB's return changes the tokenomics (burn schedule, fee split), the site-delta read is
stale same-day: re-verify before sending.
