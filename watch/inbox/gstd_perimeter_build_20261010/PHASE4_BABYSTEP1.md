# PHASE 4 BABYSTEP 1 - the consensus-to-payment bridge - 2026-10-11 late (closed)

**Verdict: the loop GSTD's roadmap calls Phase 4 now exists on our stack end to end.** A live harness run (consensus-20261011T235925Z: 5 model families, 13 tasks, 9 distinct truths, consensus 0.8462 vs dead-salmon noise 0.3227, verdict STRUCTURE) was settled through SettlementMaster v3: DESKTOP worker wallet 100,000,025 to 100,000,050 GSTD, first poll. Balance-reader law held (getter, never txHash).

## The principle, now enforced by code

The bridge (`settle-consensus.ts`) refuses to pay unless the caller passes verdict=STRUCTURE - the instrument's own certification, read from the run summary in the open before invoking. Proven both directions tonight:

- **Refusal fired live:** the 3-task run consensus-20261011T235008Z came back DEGENERATE-TASKBANK (distinct truths under 4) and the bridge answered PAYMENT REFUSED, exit 3, zero chain interaction. (A second run, consensus-20261011T235346Z, came back WEAK - 0.40 consensus against 0.369 noise, not certification; same gate refuses it.)
- **Payment fired live:** the 5-model 13-task run certified STRUCTURE and the settle executed; taskId 53001297761; qualityScore 6923 (the run's consensus-correct rate).

## The road tonight taught (model-mix law)

The 3-model mix (gemma:2b, deepseek-r1:1.5b, qwen2.5:3b-instruct) went DEGENERATE (3 tasks), WEAK (5 tasks), WEAK (13 tasks) - classify shape never reached consensus. The 5-model mix (+ gemma2:2b-instruct-q5_K_M, qwen-desk:latest) hit STRUCTURE at 14 tasks earlier tonight and 13 tasks now. Phase 4 note: model-mix width is a certification parameter, not a vibe - the proven recipe is the 5-model full battery.

## Stack state after babystep 1

- SettlementMaster v3: EQBaW5BqIePGNstaJI8ECwoTMju_e6Ta-4NNrAlwfScYnePI (baseRate 1 GSTD/CU, pool 99,950 GSTD after two bonus payouts)
- DESKTOP worker jetton wallet: 100,000,050 GSTD
- Bridge script: scripts/settle-consensus.ts (no file access by design - every settle input visible in the invoking command; node-to-wallet map in one table, bob/t90 rows land when their runners do)
- Consensus runs banked: reference/gstdcoin/contracts/consensus_runs/ (this window) + watch/inbox/gstd_perimeter_build_20261010/runs/ (the earlier arcs)

## Next babysteps (the Phase 4 ladder)

1. bob and t90 run their own harnesses (RUNNERS.md paste-lines are ready; Termux/python installs are the gate) - then the node map routes per-node and settlement pays the certifying node, not just desktop.
2. Reputation accumulation: every settled taskId appends (run_id, verdict, rates, taskId) to an on-chain-or-ledger reputation row per node - the roadmap's "reputation routing" starts as a file, becomes a getter.
3. Cold-worker probe: settle to an undeployed wallet to prove the 0.15 gas fix survives worker-wallet deployment inside the bonus send.
4. Package the three contract findings + the bridge as the GB PR set (rate default, TEP-74 op compliance line, gas hardening) - the co-contributor deliverable.

## Falsifier

"The bridge pays only certified runs" dies if any non-STRUCTURE verdict settles (the gate is a string compare - audit the invocations), and "the loop pays" dies if DESKTOP's getter stops reading 100,000,050 GSTD.
