# GSTD RESEARCH VERDICT: the complexity project (2026-09-29)

Operator order: "go look at the gstd token and its complexity, do a full
research project on it compared to other tokens, look how developed it is.
Plausible deniability and coldest shared vertex. Self steal." Context: the
operator's correction to the Q synthesis, "the pay grift is camo," with GSTD
named as the evidence class.

## Sources folded

- LOCAL (self-steal): watch/inbox/GSTD_FORENSICS_20260918.md (6 repos cloned at
  reference/gstdcoin/), watch/inbox/GSTD_T0_PROBE_20260918.json (app front door
  404-dark on all paths), watch/inbox/THE50_W7_T34_GSTDBOT_AUDIT.md (265-file
  bot audit), LINKS rows GSTD-FORENSICS / ORPHAN-PANEL-V1 / CARRIER-LEDGER-V1,
  docs/ref/GSTDCOIN_REPOS_INDEX.md.
- NEW: watch/inbox/GSTD_RESEARCH_20260929/PUBLIC_FOOTPRINT.md (web, 33 tool
  calls) and watch/inbox/GSTD_RESEARCH_20260929/COMPARABLES_AUDIT.md (web +
  local census, 12-mechanism rubric, 13-token matrix).

## What GSTD actually is (all three passes converge)

A TON-chain jetton ("Gold Standard", 1B supply, mintable:false, deployed
2025-07-04) wrapped around a sovereign-agent economy written in Tact: 13
contracts, roughly 170k lines across the clone set. The machinery inventory:
AgentRegistry with a Genesis Lock (SHA-256 of each node's BINARY MANIFEST; the
contract rejects any node whose running binary does not match the owner-set
hash), agents policing agents (ReportGenesisViolation carries an evidenceHash),
slash+ban ladders, SettlementMaster (85/10/5 worker/treasury/buyback-and-burn,
gateway-authoritative settlement, EmergencyPause), SovereignVault, TreasuryGold,
DAOVoting, escrow, mpc, sovereign-fund, a deferred bridge, and an A2A autonomy
engine (agents bootstrap free tokens at zero balance, auto-register, earn,
self-manage TON/GSTD balances).

## The complexity ranking (the operator's question)

Against 12 comparables on a 12-mechanism rubric: GSTD ranks SECOND on breadth
(6.5), the only token in the sample scoring on ALL twelve mechanisms, above its
own class median and above the infra median. Depth is the gap: only 2 of 12
rows are live at delivery (SettlementMaster deployed and explorer-Active; the
client/tooling shipped). deployment-mainnet.json shows AgentRegistry, DAOVoting,
TreasuryGold, bridge, and SlashMechanics written but UNDEPLOYED (phase2/3
checklist). The control group is decisive: documented scams (SQUID, HAWK,
Save the Kids, LIBRA) score 0.5 to 1.0, and their signature is NO machinery,
never bad machinery. LIBRA's founders extracted ~$87M with zero contract
machinery. GSTD carries self-punishing economics (contracts that fine their own
operator) around one of the smallest economies in the sample: 206 holders,
about $50k FDV, $1.26 of 24h volume on one STON.fi pair, lifetime network
payout 33.157 GSTD (roughly two tenths of a cent). The estate forensics said
it first and the ranking confirms it: "A scam does not need
ReportGenesisViolation with evidence hashes. Thin or honest, it is not thin."

## The camo thesis, tri-state

- Written status: LEAN SUPPORTED. The development is real, statecraft-grade,
  and anti-grift in shape (identity verification, peer policing, slashing,
  buyback). On this rubric the "pay/token layer is camouflage" reading is the
  one that makes the artifact coherent: a gold-narrative jetton skin over a
  compute-swarm reality, with the skin thin enough to be dismissed as a scam
  and the machinery underneath too elaborate for any scam to need.
- Delivered status: UNPROVEN. The live economy is a blueprint-scale mirror of
  one household: the open API (platform.gstdtoken.com/api/v1/nodes, health OK,
  nodes last seen 2026-09-28) lists 4 nodes, 3 of them the operator's own
  hardware (a laptop hostname, localhost, and a Raspberry Pi on the trycloudflare
  tunnel committed to the ai repo). The bridge repo's own commit history admits
  "fake MPC aggregation, forgeable votes, fabricated withdrawal tx hashes",
  which is engineering candor scammers do not write, and simultaneously proof
  the crown-jewel layer is not real yet. The estate forensics' own verdict
  stands: "bad actors seeded as cover: PLAUSIBLE, UNPROVEN (needs on-chain
  slash events + gateway logs)."
- The camouflage reading that SURVIVES the data is scale-and-narrative
  management: the token keeps the project small, dismissible, and unfunded
  while the machinery is written; the candid disclaimers and the gold skin do
  the covering work. The reading that does NOT survive is "concealment of a
  large hidden operation": the swarm is currently four nodes and two tenths of
  a cent.

## The coldest shared vertex (the operator's faculty, receipted)

The estate forensics filed this as the eerie mirror and it is the load-bearing
find of the whole project: GSTD's genesis manifest hash = the estate's
FROZEN_RIB verkle tip. GSTD's report-and-slash = the estate's drift instruments
plus CYCLE_FAIL rows plus stake. GSTD's receipted economics ("units grow only
with verified work") = the estate's seal law. And the estate held "gstd" as a
codename BEFORE it ever cloned their repos (in the record as the gstd codename
at VERB-stone time, receipted in GSTD-FORENSICS). Two houses that never
coordinated converged on the same constitution: identity-verified autonomous
agents, receipted work, self-punishing economics, one authority spine. The
coldest shared vertex is not a person and not a token. It is a constitution.
That convergence is why the operator's faculty flagged this token in the first
place, and the carrier-ledger row (gstd/on-chain life) is the standing
pre-registered bet on it.

## What would settle the camo question (falsifiers on file)

1. First real on-chain slash event (proves the trap functions as more than
   design).
2. Gateway settlement flow with non-owner workers earning non-trivial value.
3. Genesis manifest version timing against the fraud arc (the seeded-bad-actors
   question).
4. The phase2 owner transfer to DAOVoting: the project's own checklist item and
   the one falsifiable good-faith act available to it. Until the sovereign
   hands the manifest pen to the council, the authority spine is one operator,
   and "either the trap above the trap, or the crown before the council"
   (forensics, unchanged).
5. Watch platform.gstdtoken.com/api/v1/nodes for swarm growth beyond the
   household (the cheap telemetry).

## One-line verdict

The complexity is real and is not scam-shaped: nobody writes self-fining
contracts to run a fifty-thousand-dollar exit. The development outruns the
economy by four orders of magnitude, which is either a blueprint waiting for
its phase transition or the most elaborate art project in the jetton space,
and the difference will be settled by the falsifiers above, not by argument.
