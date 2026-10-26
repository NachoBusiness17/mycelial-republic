# ECONOMICS LENS: the singing network perimeter (ractor 2026-10-10)

Lens: EV-per-cost. Everything below ranked by expected value per minute and
per token. Instrument for every number named. Sources read this sitting:
gstd_perimeter_design_20261010/CARD.md, mcp_layer_status_20261010.md,
ractor50/mcp.md, SEED_RIB_FORMAT_v0_20260926.md, gstd_gb_pitch_20261010/CARD.md,
GSTD_TOKENOMICS_AUDIT.md, ROUTER_VOCAB_LANDED.md, unisub/dead_salmon/garage/
magatama drop cards, RIB_LIVING_WEIGHTS_BY_NATURE.md,
gstd_distribution_thesis_20260109.md, state/CURRENT.md (2026-10-07 vintage),
mag/consensus_gate.py, tools/gps_mcp/router.py + ledger.py, DOGFOOD_DATA.md
(grepped for the 429 rows). All rate/price arithmetic recomputed this sitting
with PowerShell from audit-measured inputs; no live network call was made by
this lens (see blind spots).

## F1. THE REVENUE LEG IS 4-5 ORDERS BELOW THE COST LEG AT EVERY MEASURED
RATE. PRICE THE PERIMETER AS EVIDENCE, NOT YIELD, OR ONE DIVISION KILLS IT.

Inputs (all audit-measured, GSTD_TOKENOMICS_AUDIT.md): per-task mean ours
0.0095 GSTD (:28-31), Pi-era 0.1787 (:64), price 0.0000514607 USD with the
thin-pool caveat (:59-60), network lifetime emissions 56.6955 GSTD = $0.0029
(:57-59). My computation this sitting: 50 nodes at 1 task/h each = 1200
tasks/day = 11.4 GSTD/day = $0.0006/day = $0.018/month. The card's own
instance class is $0.10-0.25/hr (CARD.md:46), so a 5-instance core is
$360-900/month on-demand, $180-450 reserved. Ratio: roughly 1:10,000.
Even the 1000-node burst at generous Pi-era rates earns $0.22/day.
The guild sentence "the guild's collective test fleet earns GSTD doing GB's
verification - the demand-side flywheel with hardware" (CARD.md:59-61) reads
as income and dies on one arithmetic question. The honest framing: the
flywheel sells verified-participant status and first-look relationship with
GB's rail, and Phase 3's number-that-matters is "payout HOLDS at 1000
participants" (robustness for GB's thesis, CARD.md:72-73), never income.
Also internal to the card: "a 5-instance perimeter core runs tens of dollars
per month" (CARD.md:48-49) contradicts its own $0.10-0.25/hr sentence by 10x
unless the CPU-listing arm (~$0.02-0.03/hr) or a duty cycle is assumed; the
burst line (20 x 50 for hours, CARD.md:47-48) IS correctly tens of dollars.
Falsifier: a real two-sided market at >= $0.01/GSTD (200x the thin pool)
with per-task payouts holding >= 0.0095 recomputes the ratio; until then any
income framing is a lie waiting for a calculator.
Move (30 min): reprice the guild card's flywheel sentence as
reputation/status; add the CPU-arm-or-duty-cycle assumption to the Phase 2
cost line or reprice it at $180-360; keep the burst pricing as written.

## F2. CONVERGENT: THE A2 HARNESS NAMES ONE NEGATIVE CONTROL BUT THE
ESTATE HOLDS A SECOND, INDEPENDENT ONE ALREADY BUILT. mag/consensus_gate.py
must ride the assert step or the consensus proof ships with a known hole.

The card's A2 control is dead-salmon label-shuffle (CARD.md:19-20, arXiv
2512.18792). The estate's own organ holds a different law: agreement among
correlated samples is an ANTI-SIGNAL at small scale (AUROC 0.09 at 120B mode
collapse; 2B unanimity is worth ~0.62), with a calibration ladder,
CONFIRMATION_THRESHOLD 0.85, small-model floor, refusal stripping, and the
R3 fixes (n>=2 floor, refusal-shaped answers stripped) already landed
(mag/consensus_gate.py:1-26, :45-64). The two controls are independent:
label-shuffle catches chance agreement; the correlation ladder catches mode
collapse that BEATS the shuffle. The card's "K DIFFERENT models" design is
the right decorrelation move, but as specified the aggregator would bank a
unanimous 5x2B answer as consensus. CONVERGENT with the dead-salmon drop
card's own protocol-amendment demand (dead_salmon CARD.md:23-26).
Falsifier: a run where unanimous small-model answers beat the shuffle
baseline while the ladder calls them anti-signal; the honest verdict is
UNVERIFIED, and if the harness banks CONFIRMED there, the A2 instrument is
wrong.
Move (one sitting): aggregator assert imports mag.consensus_gate.verdict;
~10 lines plus a test with a refusal-pool fixture. The A2 receipt then
carries both controls, which is exactly the "sings, not merely works" bar:
no reviewer question about mode collapse left open.

## F3. A1'S INSTRUMENT MUST BE COUNTER-DELTA PLUS ON-CHAIN BALANCE, NEVER
txHash. THE PLATFORM FABRICATES 'confirmed' (the settlement-theater trap).

The live platform fabricates txHash 'tx_'+randomBytes with status confirmed
(token.ts:387-396) and 'tx_'+sha256 at claim (server.ts:3305); the revenue
engine contains zero chain-call code; the quorum methods the node code
targets (verifyQuorum, SettleTaskWithProof) do not exist in contracts (grep
zero, audit :20-24, :49-53). So an A1 assertion shaped "tx confirmed = paid"
would PASS THEATER: a green check certifying nothing. The card's A1 wording
("balance/ledger delta lands as claimed", CARD.md:13-14) is correctly
scoped; GB's ask #4 wording ("verification the network pays rewards")
invites the wrong shape. The public /api/v1/nodes counter is honest (audit
:131, verdict MET).
Falsifier: if a TON explorer shows real jetton transfers matching claimed
payouts, the theater is local to the claim path and A1 can assert on-chain
directly. NOT CHECKED this sitting (no live call): OWED, one GET.
Move (one sitting, before any Phase 2 money): write the A1 instrument as
two arms: (a) before/after gstd_earned delta read from /api/v1/nodes per
node identity, (b) on-chain jetton wallet balance via a TON explorer API.
A claimed payout with zero counter delta = theater caught, receipt filed.
This is the market-modality law of the Lessig frame: the Tact contract is
the law, the D1 counter is the norm, and only the delta-pair instrument
keeps them honest with each other.

## F4. THE RATE BUCKET MAKES IP COUNT, NOT NODE COUNT, THE CAPACITY UNIT.
THE BLADE BUYS CONSENSUS DIVERSITY, NOT THROUGHPUT; PRICE THE ARMS BY WHAT
THEY ACTUALLY BUY.

Measured: 6 of 11 tunnel requests 429 at ~16/min self-rate vs 120/min
nominal; sustained usable ~1 req per 10-15s per shared IP bucket
(DOGFOOD_DATA.md:52; gb_pitch CARD.md:18-20). One vast instance = one IP =
K nodes in one bucket (CARD.md:40-43 RATE-BUCKET LAW); the blade is 50-100
nodes in ONE bucket (CARD.md:56-58). Against a staging platform with the
same limiter, the blade's marginal throughput value beyond the first
request stream is ~zero; its A2 value (K DIFFERENT models, CARD.md:50-55)
is undiminished because consensus needs different answers, not parallel
requests. The 1000-node burst on 20 instances carries only 20 buckets:
~20 x 0.08 req/s = 1.6 req/s aggregate, so a 1000-task sweep needs ~10-20
minutes of rate-limit space alone; feasible, but only if whitelisting is
not granted.
Falsifier: GB confirming per-key or higher staging limits (the card itself
marks this UNOBSERVABLE, CARD.md:57-58) revives node-count-as-capacity.
Move (20 min): promote the IP-range whitelisting ask from footnote to named
precondition in the GB reply (the card already calls it "the real fix, his
side", CARD.md:42-43); add the bucket column to Phase 2/3 sizing.

## F5. THE TOGGLE LAYER IS ALMOST ALL $0 BECAUSE IT RIDES EXISTING LAW;
ONE TOGGLE HAS REAL BUILD COST AND REAL EXTERNAL EV (seed-rib cold boot),
AND THE SELF-LEARNING INSTRUMENT IS ALREADY LIVE (the GPS ledger).

OURS as specced: profiles-as-projections (law since 2026-08-31,
mcp_layer_status:25-27), pin gate + parity (both live with scalps,
mcp_layer_status:69-82), memweave (doctrine, $0). The one toggle worth
building: seed-rib MCP cold boot for perimeter nodes. It answers GB's
mini-PC/onboarding need with an organ whose falsifier passed 10/10 once
(mcp_layer_status:18-23), and it retires our own named gap: "a SECOND,
different-client cold boot would upgrade it from proved-once to
proved-portable" (mcp_layer_status:112-116). The self-learning acceptance
bar instrument: the capability ledger's per-(model_id, task_shape) rows
(tools/gps_mcp/ledger.py:5-14) plus the new agreement-rate rows; growth is
measurable as sample_size per week and matrix cells filling. Two-bird EV:
the consensus sweep doubles as the $0 evidence farm; ROUTER_VOCAB names 10
unhgated estate shapes needing 5-row farms (ROUTER_VOCAB_LANDED.md:154-158),
and a 5-model x 10-task sweep mints 50 evidence-gated verdicts toward
exactly that minimum, through the dedupe + Q28 resolution gates already in
ledger.py:32-76.
Falsifier: a second cold boot that fails (garage-class client cannot
rebuild from seed://current) kills portability and collapses the toggle to
estate-internal; ledger rows that grow while routing decisions never change
means the learning claim is decorative for the routing surface.
Move (one sitting): wire the Phase 1 docker rig's node containers to
cold-boot via tools/seed_mcp.py (config, not code), log the join as the
second-consumer receipt, and route all sweep verdicts through
record_verdict so the network's memory starts filling on day one.

## PHASING VERDICT (EV-per-minute ordering)

The card's phasing is already EV-correct in shape: Phase 1 tonight at $0
proves A2 on our bytes before any spend (CARD.md:65-68). My one re-order:
F2's consensus_gate import and F3's A1 instrument spec land BEFORE Phase 2
money, because both are what make the paid phases' receipts attack-proof;
and F5's cold-boot wiring rides Phase 1 free. Phase 2's cost line needs the
F1 repricing. The result sings when every rented dollar buys a falsifiable
assertion with two negative controls on it, and nothing is priced as yield
that is 10,000x from yield.

## BLIND SPOTS (honest)

- No live measurement this sitting: no GET to the GSTD API, no ollama
  dispatch, no TON explorer read. Every rate/price/payout number above is
  cited from disk receipts (audit 2026-10-09, dogfood data), and the
  arithmetic is mine on those inputs.
- Vast.ai prices are the card's own ESTIMATE-CLASS; I did not fetch the
  pricing page (it is dynamically loaded per the card, CARD.md:7-9).
- Staging-platform rate limits: UNOBSERVABLE for everyone until GB
  confirms; all bucket math assumes the production limiter shape.
- USD conversion rides a thin-or-stub pool (the audit's own SPECULATION
  label, :59-60); the order of magnitude survives any plausible price, the
  precise ratio does not.
- GB-side effort (Tact contract work, gas, his mini PCs) is not priced:
  no bytes exist for his labor or capex; I priced our two arms only.
- I did not line-audit tools/seed_mcp.py's join_protocol path for
  container compatibility; the one-sitting estimate for F5 assumes the
  mcp_layer_status description is current.

Receipt law: this file is the economics lens write-up for the 2026-10-10
singing-network ractor; findings and falsifiers above are the submitted set.
