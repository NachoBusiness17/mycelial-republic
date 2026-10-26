# GSTD LAUNCH BRIEF - ractor fold, night session 2026-10-13 (mode-2, operator asleep)

Question: what's next for GSTD, what stands in the way, how do we launch.
Dogfood: every lane ran an estate instrument, not an opinion. Receipts on disk.

## LANE HEALTH (instrument: gstd_drain + greed law + read scripts)

- Fresh master read caught the FIRST LIVE GREED-LAW TRIGGER: master drifted to
  0.9188 - below the floor, inside the SendIgnoreErrors silent-drop band - via
  the excess-return mechanism walking it down overnight. The law caught it; the
  funding leg cured it (send-fund.ts, 0.5 TON, bounce:false, seqno 89->90,
  master 1.4186, CONFIRMED in-band).
- Readiness battery: desktop STRUCTURE (+25, certified), bob NOISE-CLASS
  (refused, zero credit - the gate still bites).
- LIVE-FIRE BUG CAUGHT AND FIXED: --dry fired the gated bridge for real
  (desktop JW +100 GSTD on-chain, master -0.20, deployer seqno bumped). Root
  cause: the claim block had no dry gate. Fixed: dry now suppresses with
  "rehearsal never settles"; post-fix run verified ZERO on-chain movement
  (deployer, seqno, master all byte-identical). A dry mainnet rehearsal would
  have settled real TON; caught on testnet where it costs nothing.
- STANDING: the excess-return walks the master down continuously - the floor
  law plus the funding leg is a permanent maintenance loop. This wants the
  standing cron.

## LANE RED (instrument: deepseek sensing, $0.0015, hostile-reviewer frame)

Four threats against DEPLOY_MAINNET.md + NEXT_SITTING:
1. Unverified PR #1 bytecode on mainnet (never run on mainnet, unmerged).
   Mitigation: 50-cycle soak on a fresh testnet against the amended build.
2. Single-operator key custody, no documented backup/multisig.
3. Greed law is CLIENT-SIDE ONLY - the contract enforces no band; any other
   caller can push the master back into the silent-drop band.
4. SendIgnoreErrors is STILL in the contract we would deploy - the client gate
   reduces probability, it does not eliminate the failure mode.
Verdict: HOLD until (a) the on-chain fixes are folded into PR #1 and (b) the
soak runs. Sensing-grade: every point was checked against the evidence files.

## LANE AUDIT (instrument: the Pool scorecard, applied to ourselves)

Our own dated promises (DEPLOY_MAINNET fire sequence, PR #1 claims): all
PENDING, none BROKEN, none LANDED yet. The instrument that killed Mr Pool's
genre now polices ours - the first self-application. When the mainnet run
fires, its rows start scoring for real.

## THE FOLD: the launch sequence, revised by the lanes

1. AMEND PR #1 with the two on-chain fixes the RED lane forced: checked bonus
   send (+ bonus-deferred event) and the contract-level balance-band invariant.
   This kills threats 3+4 and strengthens the PR for GB - the relay-skip fix is
   the thing their own token needs.
2. CUSTODY RUNBOOK: encrypted offline mnemonic backup + two-machine split,
   documented before funding (threat 2).
3. SOAK: 50-cycle fresh-testnet loop against the amended build (threat 1).
4. MAINNET: deploy, capped float, greed law live, first settle verified on the
   transaction list.
5. GB SIGN-OFF with the amended PR = Rung 2 (his token on our organ).

## STANDING BLOCKERS (each owned)

- Mimosa L3 unblock (operator): the relay-skip fix, greed law, dry-bug fix, and
  launch brief are staged-uncommitted behind pre-existing gstdbot findings.
- Operator funding: ~5 TON to the mainnet deployer when rung 4 opens.
- Funded-tier credits: the certified consensus leg for the veil/graded claims.
- GB review: Rung 2 only; Rung 1 does not wait on him.

## The one-paragraph answer to the operator's question

What's next: amend PR #1 with the two on-chain fixes, then soak, then mainnet.
What stands in the way: three things, all named and owned - your unblock click,
your 5 TON, and GB's review for the second rung only. How we launch: not
tonight, and that is the red team's gift - the plan that survives is the one
where the contracts stop trusting the client, the keys have a runbook, and the
build soaks for fifty cycles before it touches real money. The machine spent
the night proving it can catch its own bugs before they cost anything: that is
the launch.
