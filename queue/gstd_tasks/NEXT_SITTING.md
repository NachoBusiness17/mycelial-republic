# GSTD DRAIN - NEXT SITTING REGISTER (filed 2026-10-13)

## 1. Relay-skip anomaly (OPEN, receipted 10/12)

Intermittent bonus-relay skip: settle A at 01:51:20Z showed out 3, settle B at
02:02:13Z showed out 4, identical inputs. The one genuine contract question for
GB. Reproduce with trace-v6-settles.ts across N settles before asking.

## 2. Task-bank co-evolution law (NEW, from DUET + this paper)

Two independent papers force the same design item:

- DUET (dair_ai drop 3): update the grader alongside the agent - the agent's
  failure modes change as it improves.
- Persistent Memory in Multi-Agent LLM Inference (arXiv:2610.07782): the null is
  STRUCTURAL on single-question benchmarks - stored traces have nothing
  informative to retrieve when every condition resets them.

Design item: the battery's task bank must (a) rotate/regenerate tasks as
reputation climbs (the council of five must not become the old king's scales),
and (b) add LONGITUDINAL tasks - sequences where run N's trace is informative
for run N+1 - because that is the only shape in which the estate's memory tier
(mycelium, rib_bus, residue) is measurable at all. A memory-ablation arm on
longitudinal tasks, preregistered, would give the mycelial thesis its first
honest accuracy measurement. Until then: the estate claims memory as continuity,
never as per-task accuracy lift.

## 3. Loop standing (operator decision)

The earn loop is window-driven; overnight it idled 14.5h. A cron (MagGstdDrain,
like MagCensusPatrolDaily) makes it standing. Master TON 1.73 supports it.

## Closed this sitting (2026-10-13 morning)

- T90 jetton wallet: DEPLOYED, 50 GSTD held, on-chain rep 1 (was the pending item).
- 08:24Z settle: LANDED - desktop JW at 100,000,325, exactly the claimed 325.
- Drain fired live: desktop STRUCTURE +25 + settle rc 0; bob NOISE-CLASS refused.

---

## UPDATE 2026-10-13: relay-skip ROOT-CAUSED (was item 1) - CLOSED

The decoder's 60-tx sweep shows the skips are NOT random: every out-3 settle
(03:20, 04:18, 04:34, 10:30, 11:20) sits in the master's low-balance band, and
after the 11:27 2.0 TON top-up nothing skips again. Mechanism, read from
SettlementMaster.tact:208-231: the bonus relay sends with mode SendIgnoreErrors -
when the master's remaining balance cannot cover the 0.3 TON send, the message
silently no-ops. "Identical inputs" was the wrong premise: input messages were
identical, the governing state (balance) differed. Deterministic after all.

Cures: (1) PR #1 client-side fresh-read gate (shipped), (2) greed law
[floor 1, cap 10] TON now LIVE in tools/gstd_drain.py (defaults), (3) upstream
PR for GB: replace SendIgnoreErrors on the bonus send with a checked branch that
emits a bonus-deferred event (file with the PR #1 review).

## MAINNET RUNG 1 STAGED

DEPLOY_MAINNET.md: fresh keys generated (key-law hardened generator), greed law
live, fire sequence written. WAITING ON: operator funds the deployer with ~5 TON.

## ITEMS FROM THE MOAT-CORRECTION REVIEW (2026-10-13 morning, pre-mainnet)

**2a. Claim-entropy logging at the gate.** VeriHarness measured +0.6 on
unanimous consensus pools vs +6.1 on disputed pools. The battery credits
STRUCTURE (high consensus) - which is where verification adds least. Log claim
entropy per settle; route deeper verification to split pools. Preregistered
replication on the next 20 certified artifacts: if the gate shows large gains
on unanimous pools, it is measuring judge-leniency - fold with the same
violence as the coherence meter.

**2b. Coverage receipt v0 (new organ, pre-mainnet).** Every certification now
carries checks-run / checks-checkable, the checkable set enumerated from spec
AND receipt before verification starts. The 50-cycle mainnet soak produces
coverage receipts alongside settle receipts. Until coverage is a first-class
receipt, the differentiation claim is a hash function - and hash functions are
free. Also: resolver/challenger split adopted verbatim (separate contexts,
merging costs 0.8 points).

**7. Compass namespace (public cut).** Prefix the compass doc to
republic-compass in the next public snapshot (dshakes/compass collision).

**8. Canary clause (attestation organ).** Rotating clause in the compass; any
seat whose first output cannot echo it did not load the law (AGENTS.md loading
is conditional across provider lanes). Boot-time check by the planned
agent-replay organ.

**9. Upstream PR amendment gains a line.** The on-chain fixes (checked bonus
send + band invariant) now also carry R2's lesson: the contract's bonus branch
should emit a bonus-deferred EVENT (coverage observability on-chain), not just
stop dropping silently.
