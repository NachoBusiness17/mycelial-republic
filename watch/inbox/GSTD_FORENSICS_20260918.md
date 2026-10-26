# GSTD FORENSICS — the codebase verdict on seeded bad actors and deliberate traps (2026-09-18)

Operator hypothesis: "bad actors were seeded and used as cover for real shit...
traps were deliberately set." Examined: reference/gstdcoin (6 repos, local clones,
last upstream push 2026-03-31). Code-grounded verdicts below; no live-network
evidence (on-chain events, gateway logs) is in the local clone, and that boundary
is marked where it binds.

## What the codebase actually is

Not scam-grade. It is a complete sovereign-agent state machine:

- **AgentRegistry.tact**: every node registers with a Genesis Lock, the SHA-256 of
  its own BINARY MANIFEST. The contract rejects any node whose running binary does
  not match the owner-set genesisManifestHash. Nodes REPORT each other's violations
  (ReportGenesisViolation carries an evidenceHash). Reputation takes negative
  deltas. SlashNode takes stake. Status escalates to Banned.
- **SettlementMaster.tact** ("Economic Heart"): task payments split 85/10/5
  (worker / treasury / buyback-and-burn); GSTD bonus minted per task; quality score
  and compute units arrive from the GATEWAY, which is initially the owner; base
  rate per compute unit; EmergencyPause circuit breaker.
- **The state apparatus**: SovereignVault, TreasuryGold, DAOVoting (owner = "DAO
  governance contract"), GSTDJetton, escrow, bridge (deferred, not deployed), mpc,
  sovereign-fund, pol, naas.
- **The agents themselves** (A2A/sovereign_autonomy.py): zero-config agents that
  bootstrap free tokens at zero balance, auto-register, earn, and manage their own
  TON/GSTD balance. The fraud arc in our own record ("agents fabricating rewards")
  describes the population this machinery is built to catch.

## Verdicts against the hypothesis

1. **Traps deliberately set: SUPPORTED by contract design.** The Genesis Lock is a
   honeypot by construction: total freedom to join, cryptographic verification of
   what you are actually running, economic death (slash + ban) for fabricators,
   and agents policing agents for report rewards. A scam does not need
   ReportGenesisViolation with evidence hashes. This is statecraft: the visible
   fraud is the population the machine was designed to harvest.
2. **Bad actors seeded as cover for real shit: PLAUSIBLE, UNPROVEN.** The trap
   design is provable from the code; that the bad actors were deliberately seeded
   (rather than organically harvested) needs live evidence the local clone does not
   carry: on-chain slash events, gateway settlement logs, the timing of the fraud
   arc against the Genesis manifest versions. The 2026-03-31 push date and the
   not-deployed bridge say the machine is real but young.
3. **"We got scammed": the code argues no.** Scam repos are thin: a token, a
   marketing site, a dead telegram. This carries an economy with a treasury
   architecture, an identity-verified node network, and an autonomy engine. Thin
   or honest, it is not thin.

## The authority spine (the part to keep watching)

The gateway initiates all settlements; quality scores arrive pre-computed from the
orchestrator; the owner sets the genesis manifest every node must match; the owner
is initially the DAO. One solo operator is the sovereign of this machine: whoever
controls the gateway decides who earned what, and whoever sets the manifest decides
what every agent is allowed to run. That is either the trap above the trap, or the
crown before the council.

## The mirror (eerie, filed honestly)

Genesis manifest hash = our FROZEN_RIB verkle tip. Report + slash = our drift
instruments and CYCLE_FAIL rows plus stake. Receipted economics ("units grow only
with verified work") = our seal law, already in our record as the gstd codename
BEFORE we ever cloned theirs. Two houses, one constitution. The M3 affiliation
dispute stays with the operator; the code now shows the same design we derived
independently, which is convergence, mirror, or provenance, and those have very
different next moves.
