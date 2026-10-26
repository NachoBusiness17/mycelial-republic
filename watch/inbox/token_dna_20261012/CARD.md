# TOKEN-DNA: modeling token behavior + the whole DNA (2026-10-12, operator ask)

Operator: "How do we model token behavior and the whole DNA."

## The two models (they are one system, read at two scales)

1. TOKEN BEHAVIOR = the flow dynamics: how GSTD moves through the factory -
   mint (SettlementMaster bonus), settle (85/10/5), pool (drain/refill),
   accumulate (wallets), cap (workerPoolMax 400M), starve (idle-accrual
   scaler, 152x variance per the audit). Questions the model answers: does
   the pool drain at 1000 nodes? Does the cap hold? (the audit says the cap
   never held on any real day!) What is the equilibrium worker income at
   fleet scale?
2. TOKEN DNA = the lineage: every GSTD coin carries WHAT IT PAID FOR. Not a
   fungible blank - a receipt chain: taskId, consensus verdict (which model
   families agreed, the quality score), the falsifier run, the timestamp, the
   machloket if any dispute existed at settlement. The DNA strand is the
   merkle path from mint to current holder. docs/DNA.md's law (residual +
   registry + leaf = filed workdays) applied to the token: the token IS a
   filed workday.

## The build: the factory becomes the simulator

settle_factory.html is already the visual layer. It gains a SIM mode:

- AGENTS: N worker nodes (each a magatama), M task spawners, 5-model judge
  panel, the SettlementMaster machine, the pool tank, three wallets.
- TICK: a task spawns -> judges answer -> consensus gate (majority, noise
  control at 0.15 margin) -> SettleTask -> splits -> balances tick.
- PARAMETERS (from the real bytes, all cited): baseRate 0.001 GSTD/CU
  (SettlementMaster.tact:110), shares 85/10/5 (:106-108), minPayment 0.05
  TON (:116), gas 0.1 TON (:139), workerPoolMax 400M (GSTDJetton.tact:111),
  consensus margin 0.15 (tools/consensus_harness.py verdict), idle-accrual
  scaler variance as a confound dial (AUDIT:71-74).
- DNA RENDERING: every settled token draws its strand - a vertical helix of
  its receipt chain (task id -> verdict -> families -> quality -> holder).
  Click a coin, read its DNA. The token is a filed workday you can audit.
- THE RUNS (the research questions, pre-registered):
  R1: pool drain time vs N workers at measured task rates (does 1M GSTD
  cover 1000 nodes, and for how long?).
  R2: cap-law enforcement - does workerPoolMax bind before adoption saturates?
  R3: consensus-quality vs payout drift - do quality scores decay as the
  fleet grows (the Personas warning: family stamps on witnesses)?
  R4: idle-accrual variance - does the 152x scaler make worker income
  unpredictable enough to break participation (the participation cliff)?
  R5: GSTD-DNA auditability - what fraction of circulating supply carries a
  complete receipt chain? (the "token you can trust" metric - no other token
  publishes this.)

## Why the DNA half matters more than the flow half

Flow modeling exists (any DePIN whitepaper). TOKEN DNA does not: a token
whose every unit carries its verifiable work-history is a different asset
class - you can refuse to accept coins with no consensus receipt, price
coins by the quality of the work that minted them, and prove the economy's
honesty by auditing supply against receipts. That is the dead-salmon law as
monetary policy: coins that cannot show their work are unbanked.

## First sitting (lane A)

The sim core as a single python file (tools/token_dna_sim.py): agents,
judges, SettlementMaster, DNA chains, the five runs, CSV + the JSON ledger
out. The factory HTML reads the ledger for the visual pass (lane B). The
percolator gets the invariant: NO TOKEN MINTS WITHOUT A DNA CHAIN.
