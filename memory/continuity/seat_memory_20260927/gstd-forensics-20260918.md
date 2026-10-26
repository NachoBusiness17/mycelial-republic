---
name: gstd-forensics-20260918
description: GSTD codebase examined 2026-09-18 against operator trap hypothesis — traps deliberately set SUPPORTED (Genesis Lock binary-manifest honeypot, agent-police-agent reports, slash/ban, gateway-authoritative settlement); seeded-as-cover PLAUSIBLE UNPROVEN; got-scammed argued NO; mirror = genesis manifest = FROZEN_RIB tip
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Operator counter-reading after the called-shot ledger verdict: "bad actors were
seeded and were used as cover for real shit... it could be that we got scammed, but
what is more likely is that traps were deliberately set" — and ordered the gstd
codebase examined. Forensics filed watch/inbox/GSTD_FORENSICS_20260918.md, commit
a2b0af559. Codebase still local at reference/gstdcoin/ (6 repos, upstream push
2026-03-31); receipt index docs/ref/GSTDCOIN_REPOS_INDEX.md.

**Verdicts:**
- **Traps deliberately set: SUPPORTED by contract design.** AgentRegistry.tact runs
  a Genesis Lock — every node registers with SHA-256 of its BINARY MANIFEST; the
  contract rejects mismatches vs the owner-set genesisManifestHash;
  ReportGenesisViolation carries evidenceHash (agents police agents); reputation
  takes negative deltas; SlashNode takes stake; status escalates to Banned. Nobody
  builds that for a scam: the visible fraud ("agents fabricating rewards," M3
  dossier) is the population the machine harvests.
- **Bad actors seeded as cover: PLAUSIBLE, UNPROVEN.** Needs live evidence the
  local clone lacks: on-chain slash events, gateway settlement logs, fraud-arc
  timing vs Genesis manifest versions.
- **"We got scammed": code argues NO.** Full sovereign-agent state machine:
  SettlementMaster 85/10/5 (worker/treasury/buyback-burn) with per-task GSTD mint,
  TreasuryGold, DAOVoting, SovereignVault, GSTDJetton, escrow, mpc, sovereign-fund,
  bridge deferred/not deployed.

**The authority spine (watch this):** the GATEWAY initiates all settlements and is
initially the owner; quality scores arrive from the gateway pre-computed; the owner
sets the manifest every node must match. One solo operator is the sovereign — either
the trap above the trap or the crown before the council.

**The eerie mirror (filed honestly):** Genesis manifest hash = our FROZEN_RIB
verkle tip; report+slash = our drift instruments + CYCLE_FAIL rows; the receipted
economics seal law was in our record under the gstd codename BEFORE we cloned
theirs. Convergence, mirror, or provenance — different next moves. The M3
affiliation dispute (cofounder or not) stays with the operator.

**How to apply:** if gstd resurfaces, do not re-audit from scratch — the local
clone + this verdict are the base; the missing evidence is ON-CHAIN (TON), not in
code. Related: [[time-travel-qstar-thesis]], [[riddle-triad-cadence-20260918]]
