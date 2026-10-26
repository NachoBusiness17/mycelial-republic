# BREAK-ECONOMICS: hostile second pass on the economics lens (2026-10-10)

Instrument this sitting: byte-read of every cited source (perimeter CARD.md,
GSTD_TOKENOMICS_AUDIT.md, DOGFOOD_DATA.md, gb_pitch CARD.md, dead_salmon
CARD.md, mcp_layer_status_20261010.md, mag/consensus_gate.py,
tools/gps_mcp/ledger.py, ROUTER_VOCAB_LANDED.md tail, gb_pitch lines),
tools/seed_mcp.py existence + join_protocol grep (377 lines, hits at :8,
:204, :264, :312-313), and arithmetic recomputation via
`.venv/Scripts/python.exe -c` (outputs inline below). No live network call
by this pass either (same restraint as the lens); every rate/price input
is the audit's 2026-10-09 disk receipt. The ask's copy of the lens
truncated mid-F4; the lens's banked file (economics.md, this dir) supplied
the full F1-F5 set, and that is what is verdicted here.

## Verdicts

### F1 revenue leg 4-5 orders below cost leg: CONFIRMED (and strengthened)

Byte-check: all inputs verify. 0.0095 GSTD/task at
GSTD_TOKENOMICS_AUDIT.md:28-29, price 0.0000514607 USD with the thin-pool
SPECULATION label at :59-60, network lifetime 56.6955 GSTD = $0.0029 at
:57-58, Pi-era 0.1787/task at :64. Price class $0.10-0.25/hr is at
CARD.md:45 (lens cited :46, one-line drift, content intact); "tens of
dollars per month" at CARD.md:46-47 (lens cited :48-49, two-line drift);
the guild income sentence is verbatim at CARD.md:60-61; the 10/30 demo
anchor is real (gb_pitch CARD.md:46-48).

Arithmetic reproduces exactly (venv python, this sitting): 50 nodes x 1
task/h = $0.00058665/day = $0.0176/month; 5-instance core $360-900/month
on-demand, $180-450 reserved; burst at Pi rates $0.2207/day. Ratio range
1:10,227 (reserved low) to 1:51,138 (on-demand high): the lens's "roughly
1:10,000" is the favorable corner, the honest headline "4-5 orders" holds
(4.0 to 4.7).

Strengthening the lens missed (see ADD-1): the lens's $0.0176/month
revenue estimate is itself 7.5x the ENTIRE network's measured emission
rate (1.53 GSTD/day network-wide, audit :82-84, = $0.0024/month total),
and its 1200-tasks/day assumption is ~150x the network's observed demand
(~300 lifetime tasks over ~37 days, audit :64 + :57-58). The finding
survives a fortiori: the revenue leg was generously overpriced and still
loses by 4+ orders.

### F2 second negative control (consensus_gate ladder): CONFIRMED

Byte-check: mag/consensus_gate.py:4-8 carries the law with AUROC 0.09 at
120B (also :53), the ladder at :45-54 including (2.0, 0.62) at :47,
CONFIRMATION_THRESHOLD 0.85 at :57, SMALL_MODEL_FLOOR_B 3.0 at :60, and
the R3 n>=2 + refusal-stripping floors at :31-40 and :128-138 (lens
window ":45-64" holds the ladder/threshold/floor; R3 detail sits just
outside it, minor). The card's only A2 control is the dead-salmon shuffle
(CARD.md:19-20); the dead-salmon drop card's amendment demand is real
(dead_salmon CARD.md:21-25). The mechanism claim checks: shuffle breaks
agreement to chance so unanimous small models BEAT it, while
consensus_gate.py:165-167 refuses unanimity below 3B outright. The two
controls are independent as claimed.

Two nits, not weakenings: (a) the CONVERGENT flag rides a law-level
match; the dead-salmon amendment's named lane is suppression-topology
probes, not consensus harnesses. (b) verdict() takes ONE model_params_b
(signature :113-117), so K heterogeneous models need per-model verdicts
or a min-size rule; the "~10 lines" move is honestly ~20-30 with the
refusal-pool fixture.

### F3 A1 instrument = counter-delta + on-chain, never txHash: CONFIRMED

Byte-check: settlement theater verbatim at audit :19-23 (token.ts:387-396
'confirmed' fabrication, server.ts:3305 claim-path fabrication, zero
chain-call code in engine.ts; lens cited :20-24, one-line drift); phantom
verifyQuorum/SettleTaskWithProof at :49-53 (exact); /api/v1/nodes graded
MET at :131 (exact); A1 wording "balance/ledger delta lands as claimed"
at CARD.md:13-14 (exact). The TON-explorer check is honestly OWED
(economics.md:83); not run by this pass either.

One provenance nit: "GB's ask #4 wording" is from the ask material (the
frame's 'verification the network pays rewards to participants'), not a
disk byte; the gb_pitch card's ask list (gb_pitch CARD.md:50-57) is the
operator-to-GB direction. Substance unaffected.

### F4 IP count is the capacity unit: CONFIRMED

Byte-check: 6-of-11 429s and ~1 req/10-15s sustained at
DOGFOOD_DATA.md:52-59 (exact); the gb_pitch duplicate at CARD.md:18-21;
RATE-BUCKET LAW at CARD.md:40-43; blade single-IP at :56-58; "the real
fix, his side" at :42-43. Staging UNOBSERVABLE honestly falsified.

Arithmetic nit in the lens's favor being corrected: 20 buckets at
1/10-15s gives 1.33-2.0 req/s, so 1000 SINGLE-REQUEST tasks = 8.3-12.5
min (my run), not the lens's 10-20; but a task is not one request
(submit DOGFOOD:86-87, claim/poll :102-104, completion/report), so the
honest floor is ~3x that, ~25-40 min at 1.6 req/s (3000 slots / 1.6 / 60
= 31.25 min, my run). Conclusion unchanged (feasible, IP-bounded);
see ADD-3 for the control-plane traffic the lens left unpriced.

### F5 toggle layer rides existing law + GPS ledger as the instrument: CONFIRMED

Byte-check: all five cite clusters verify with <=2-line drift: seed-rib
falsifier 10/10 at mcp_layer_status:20-22; profiles-as-projections law
(2026-08-31) at :24-25; parity CLOSED + pin-gate scalp at :71-84;
second-consumer gap at :114-116; capability schema (model_id,
task_shape, pass_rate, sample_size) at ledger.py:5-14; dedupe partial
UNIQUE at :32-34 and the a04 double-bank cause at :40-51; Q28
evidence-resolution gate at :53-76; the 10 ungated shapes needing 5-row
farms at ROUTER_VOCAB_LANDED.md:155-158. tools/seed_mcp.py exists
(377 lines) with join_protocol live at :8, :204, :264, :312-313 (grep
this sitting). The 5x10=50 verdicts arithmetic is trivially right. The
"config, not code" cold-boot wiring remains untested (the lens's own
blind spot, economics.md:169-171; this pass did not line-audit container
compatibility either).

Phasing block: rides F1/F2/F3, no independent claims to break.

Blind-spot register: honest, all six byte-match reality (this pass made
no live calls either; vast prices are the card's own ESTIMATE-CLASS per
CARD.md:7-9).

## Additions (what the lens missed)

### ADD-1: the revenue ceiling is the network's own emission rate; the lens overpriced the revenue leg 7.5x

Finding: F1's $0.0176/month fleet-revenue estimate exceeds the ENTIRE
live network's measured emission rate ($0.0024/month total), and its
demand assumption (1200 tasks/day) exceeds observed network-wide demand
(~8 tasks/day) by ~150x; the ratio is therefore worse than the lens
priced at every honest anchor.
Evidence: GSTD_TOKENOMICS_AUDIT.md:82-84 (1.53 GSTD/day network-wide),
:57-58 (56.6955 GSTD TOTAL lifetime = $0.0029), :64 + gb_pitch
CARD.md:28 (Pi 288 tasks lifetime); my run: 1.53 x 0.0000514607 x 30 =
$0.00236/month network cap vs lens's $0.0176/month (7.5x); ~300
lifetime tasks / ~37 days = ~8/day vs 1200/day assumed.
Falsifier: staging mints per-task at fleet scale (counters did move per
completion for one node, DOGFOOD_DATA.md:105-106) AND staging carries
real demand; then the cap objection dissolves and only the price
objection (F1 proper) remains. One GB-side sentence about staging
demand shape settles it.
Move: 10 min, same edit as F1's move: add the demand/emission ceiling
line to the repriced guild sentence.

### ADD-2: A2's dispatch path is unoperationalized against three byte-measured platform behaviors (race shape, cache collision, param drop)

Finding: "the same task dispatched to K nodes" (CARD.md:15-16) collides
with the measured platform: tasks are poll RACES with one winner
(DOGFOOD_DATA.md:80-81, audit :75-78 "won 100% of poll races"), the
gateway L1-caches on the first 200 chars of the last message so any
templated task bank cross-serves one node's answer to its siblings
(DOGFOOD_DATA.md:60-66, router.ts:147-150; the proof rows C2/C3/C4), and
the gateway drops temperature/max_tokens so sampling noise deflates
consensus (DOGFOOD_DATA.md:67-72). The harness line (CARD.md:77-78, task
bank from the dogfood S/C/E shapes + payout delta asserted) reads as one
pipeline but A2-consensus and A1-payout need DIFFERENT dispatch shapes
(local-direct vs platform-submit).
Evidence: as cited, plus CARD.md:66 ("dispatch K") and :77-78.
Falsifier: GB's staging rail supports explicit one-task-to-K-nodes
fan-out (ask him; that would itself be a new platform feature worth
naming in the reply), or a sweep where cache-tier rows are filtered and
the consensus rate is unchanged, proving the collision never fired.
Move: 20 min: dispatch-path decision row in the harness spec (A2
local-direct with per-node unique first-200-chars + tier-marked
receipts; A1 platform-submit), one GB-reply line asking after task
fan-out.

### ADD-3: control-plane traffic alone breaks the card's container stacking; the blade and the 30-60/instance sizing were never rate-budgeted

Finding: the card's sizing (30-60 node containers per instance,
CARD.md:44) is infeasible against the measured bucket even with zero
tasks: heartbeats (one per node per 600s beat, audit :32-34) at 30-60
nodes = 3-6 req/min, which is most or all of one instance's measured
usable bucket (~4-8 req/min, DOGFOOD_DATA.md:52-59), and ONE node
falling back to the 5s poll (12 req/min, DOGFOOD_DATA.md:73-76) doubles
the bucket by itself; the lens's F4 priced data-plane requests only.
Evidence: CARD.md:44-45, DOGFOOD_DATA.md:52-59 + :73-76, audit :32-34.
Falsifier: staging's limiter is per-key or endpoint-scoped (heartbeats
on a separate bucket from task traffic), or push-lane-only operation is
verified on staging so no node ever falls back to poll.
Move: 15 min: control-plane budget row (req/min per instance: heartbeats
+ fallback polls + per-task cycle, >=3 requests/task per ADD-2) beside
the bucket column F4 already adds; stagger fallback polls in node
config.

### ADD-4: the card never says which token the staging rail pays; on mainnet the perimeter recreates the audit's 91%-founder-mining pattern, and A1 "closes the settlement-theater finding" overstates

Finding: if staging pays mainnet GSTD, a 50-1000-node fleet funded from
one wallet becomes the dominant emissions recipient, the exact shape the
audit convicted (91% of all emissions to the operator's own
gateway/Pi wallet, audit :95-98) and the distribution thesis forbids
("user's-own-wallet default ... never silent founder-mining", gb_pitch
CARD.md:43-45). Also CARD.md:14's "closes our audit's
settlement-theater finding" overstates scope: a staging delta-pair
check verifies the node-side counter class; the mainnet findings
(gateway-trusted SettleTask fields audit :46-48, phantom quorum methods
:49-53, owner-still-admin :113-114) stay open regardless of the staging
result.
Evidence: CARD.md:4-5 + :34-36 (staging endpoint, token unstated),
audit :95-98, :113-114, gb_pitch CARD.md:43-45.
Falsifier: staging is testnet (emission-share question dissolves, but
F3's on-chain arm must then read testnet jettons), or staging carries
per-wallet payout caps; either answer is one GB sentence.
Move: 10 min: add "which token does staging pay" to the GB reply, plus
an emissions-share ceiling pre-commitment in the test receipt, and
rescope the A1 sentence to "closes the node-side theater class on a
staging rail".

### ADD-5: the blade's "$0 marginal cost" is false by the card's own wattage line

Finding: CARD.md:55 says "at $0 marginal cost; power ~200-400W" in one
sentence; 200-400W x 730h = 146-292 kWh/month, which is $15-58/month at
$0.10-0.20/kWh (my run), i.e. the same "tens of dollars" class the card
claims for the vast core. The lens priced the vast arm's hours but took
the blade's $0 at face value, so its cost leg for Arm 2 is understated.
Evidence: CARD.md:55 (both clauses); kWh price is ASSUMPTION-CLASS (no
estate byte for local electricity price; OWED), the wattage is the
card's own byte.
Falsifier: a bench power meter reading materially under 200W at fleet
duty, or guild bench space donating electricity (marginal cost to the
network $0 even if not to the world).
Move: 5 min: strike "$0 marginal" to "power-only marginal, ~$15-58/month
at $0.10-0.20/kWh, meter the bench"; folds into F1's
evidence-not-yield repricing.

## Score

Five findings, five CONFIRMED (zero weakened, zero killed): the lens's
evidence chain is byte-solid end to end, with only 1-2-line cite drift
on four CARD.md windows and one ask-material provenance nit (F3's GB
ask #4). Its arithmetic reproduces exactly; its one soft spot is that it
was GENEROUS to the revenue leg (ADD-1) and silent on control-plane
costs (ADD-3), the blade's power (ADD-5), A2's dispatch confounders
(ADD-2), and the staging-token/founder-mining exposure (ADD-4). All
five additions are cheap (60 min combined) and all land before Phase 2
money, matching the lens's own ordering law.
