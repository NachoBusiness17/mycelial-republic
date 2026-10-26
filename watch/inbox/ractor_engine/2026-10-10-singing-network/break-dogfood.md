# BREAK-DOGFOOD: hostile second pass on the dogfood lens (2026-10-10)

Seat: break-dogfood (ractor hostile pass, singing-network run). Target: the
dogfood lens report, watch/inbox/ractor_engine/2026-10-10-singing-network/dogfood.md
(201 lines, 5 findings). The ask's JSON truncated mid-finding-4; the on-disk
report is authoritative and all 5 findings are verdicted here. Every check
below was run or read THIS sitting; commands verbatim. No em-dashes.

## Instruments fired this sitting

1. `grep -ril consensus tools/gps_mcp/` -> ZERO hits (exit 1). Reproduces the lens.
2. `grep -rn "dead.salmon\|dead_salmon\|label.shuffl" tools/ --include=*.py` -> ZERO hits (exit 1). Reproduces the lens.
3. QUANTIFIER-LAW ESCALATION the lens did not run:
   `grep -ril consensus mag/ tools/ scripts/ tests/` (mimosa + __pycache__ set
   aside for inspection) -> 60+ mag/ source files, including
   mag/consensus_gate.py, mag/_consensus_witness.py, mag/mixture_of_agents.py,
   and tests/test_consensus_degeneracy_20261005.py. The mimosa noise the lens
   reported is real (mag/.mimosa/hook-state/* matched) but it masked real
   estate source, not only cache.
4. `grep -rin "dead.salmon\|dead_salmon\|label.shuffl\|label_shuffle" mag/ tools/ scripts/ tests/ --include=*.py`
   -> mag/volume_fidelity.py:24 and :414 (label-shuffle null, live).
5. Byte reads: tools/gps_mcp/router.py:400-429 + 540-600; tools/duel_harness.py:1-60,
   222-256; tools/gps_mcp/ledger.py:1-40, 215-254; tools/seed_mcp.py:195-254;
   mag/consensus_gate.py:1-55; mag/_consensus_witness.py:1-45;
   mag/mixture_of_agents.py:1-30; mag/volume_fidelity.py:10-39;
   tests/test_consensus_degeneracy_20261005.py:1-45;
   watch/inbox/gstd_perimeter_design_20261010/CARD.md (all 88 lines);
   watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md (all 141);
   ROUTER_VOCAB_LANDED.md (all 177); mcp_layer_status_20261010.md (all 117);
   dead_salmon/unisub/garage_wizard/mag_magatama/gb_pitch cards;
   gstd_distribution_thesis_20260109.md:1-45; ractor50/mcp.md head + metering
   grep; SEED_RIB_FORMAT_v0_20260926.md head; RIB_LIVING_WEIGHTS_BY_NATURE.md head.
6. `python -c` over tools/gps_mcp/config.gstd.json -> 20 providers:
   14 tier=gstd test_double=False, 6 test doubles (3 local + 2 mid + 1 frontier).
   The "14 live gstd-tier providers" claim is byte-true.
7. `wc -l` -> duel_harness.py 581 lines (lens organ map said 581: exact);
   seed_mcp.py 377. `grep -n` mag/estate_bridge.py -> estate_receipt_append
   section at :482, def receipt_append at :490.

## Verdicts

### F1 (loop already sings at K=2; design never names it): WEAKENED

Cites intact: router.py:549-600 block read (import_duel_bank named :556,
pick_duel_contenders :566-567, third-unit semantics disclosure :570-574; the
lens's ":573-576" drifts +2 lines but sits inside the verified block);
duel_harness.py blind v1.1 + slot-A p=0.0436 at :37 and :45-56; judge_prompt
two-slot at :230 and :250-251 (ANSWER_A/ANSWER_B hardcoded, verified);
ledger.py Momentum :221-245 (RISING|STEADY|DECLINING, one-datapoint STEADY);
grep over tools/gps_mcp/ reproduced zero; 581 lines exact.

Weakened on two counts. (a) The universal "The consensus organ is design-class
today" (dogfood.md:21, organ map row 1 "UNBORN") violates the quantifier law:
the census was scoped to tools/gps_mcp/ and the mag/ matches were dismissed as
mimosa cache noise, while the full-tree census (instrument 3) shows the estate
holds prior consensus organs: mag/consensus_gate.py (consensus verdict gate),
mag/_consensus_witness.py (K=3 heterogeneous-lane consensus with ground truth,
2026-08-25), mag/mixture_of_agents.py (N-model fan-out with preserve-dissent
laws). "Nearest organs: duel_harness + cascade" is false; they are the nearest
GPS-path organs only. (b) "Specs its harness as greenfield" is dented by the
card's own text: CARD.md:75 header says "The harness (one lane, reuses estate
organs)" and :80 names the GPS ledger feed; what the card never names is the
duel loop or any consensus prior. The fork move survives as the GPS-path
answer, but the k_harness must steal from the missed organs or it rebuilds
law the estate already banked (see additions A1, A2).

### F2 (A1 as written passes on settlement theater): CONFIRMED

Every cite byte-checks against GSTD_TOKENOMICS_AUDIT.md read this sitting:
:17-23 (gstd_earned is a D1 counter; token.ts:387-396 fabricates
'tx_'+randomBytes status confirmed; server.ts:3305 claim txHash; engine.ts:15
promises SettlementRouter.tact with zero chain-call code, grep no
TonClient/send in engine.ts); :44-53 (phantom verifyQuorum/SettleTaskWithProof,
grep contracts/ zero; SettleTask trusts gateway fields,
SettlementMaster.tact:16-22,128-135); CARD.md:13-14 read (A1 = delta lands,
"closes our audit's settlement-theater finding"). One precision dent, non-fatal:
the lens phrase "a lane whose contracts contain zero chain-call code" is true of
engine.ts specifically, not of the contracts tree (SettlementMaster.tact is
chain code). The falsifier honestly scopes platform-side behavior as
unobservable (audit :6-8). The two-armed A1 move (delta + explorer GET or
OFF-CHAIN-THEATER stamp) is the right 30-minute fix and is the receipt GB most
needs.

### F3 (dead-salmon doctrine twice, instrument never): WEAKENED

Cites intact: CARD.md:19-20 (dead-salmon law verbatim); dead_salmon
CARD.md:21-24 (mandatory negative-control arm); unisub CARD.md:9-14;
AGENTS.md 4,358-tests carrier (2026-10-04 census instrument). The tools/*.py
grep reproduced zero.

Weakened on three counts. (a) The universal "exists as zero bytes of
instrument" is false at estate scope: mag/volume_fidelity.py:24 ("Grounded
against a label-shuffle null") and :414 are a LIVE label-shuffle instrument in
the fidelity gauntlet, plus the gauntlet's NULL-MODEL CONTROL kill test
(:13-20, z < 1.5 => DECORATION). True only scoped: zero bytes in the
consensus/LLM path. (b) The "sharper than the cards" shared-bias insight is
presented as if the estate lacked it, citing only the same-day unisub paper;
mag/consensus_gate.py:1-26 already banks the measured version (LAW-CONS-ILLU-001:
correlated-sample unanimity is an anti-signal, AUROC 0.09 at 120B where all 5
runs return the same wrong answer), and mag/_consensus_witness.py already ran
the ground-truth-armed consensus probe in August. (c) The unisub citation drops
unisub's own qualifier, "within shared architectures ... do not overclaim
cross-architecture" (unisub CARD.md:13-14, repeated :53-54): cross-family
shared-bias agreement is an extrapolation beyond the paper's claim. The
ground-truth arm stands on its own justification regardless. Move survives and
gets cheaper: port _consensus_witness's grounded-question shape and
volume_fidelity's z-score null form (stronger than "print DELTA": a
beats-shuffle-by-z bar, not a raw difference).

### F4 (containers are the seed's missing second consumer): CONFIRMED

All fragments byte-check: mcp_layer_status_20261010.md:114-116 exact
(proved-once -> proved-portable via a second, different-client cold boot);
tools/seed_mcp.py:204-240 exact (tool_join_protocol, 7 steps with checks, read
in full); CARD.md:37-39 (identity pinning / ghost-row law) and :69-70 (5
instances x 10 nodes = 50) and :71-73 (burst to ~1000); estate_bridge.py:482
section header verified with def receipt_append at :490; mcp_layer_status:75-78
(loop-closure landed). The scoped absence "nowhere does the design say how a
vast.ai container boots" holds against my own full read of the card. One
sharpening the lens left on the table, see addition A5: the move "run
tools/seed_mcp.py join_protocol inside it" smuggles the repo into the
container; the portability claim is only load-bearing if the server itself has
a named distribution channel (clone, wheel, or image), which neither the card
nor the move specifies.

### F5 (Phase 3 burst is founder-mining-shaped unless the receipt names the wallet): CONFIRMED

Cites byte-check: CARD.md:71-73 (burst to ~1000 via interruptible vast);
gstd_distribution_thesis_20260109.md:20-32 (DEFAULT WALLET = THE USER'S OWN,
loud opt-in, "cannot silently mine for the founder"); audit :95-98 (gateway
wallet UQB03R2DuNR9... is the top-earning node, 51.4735 of 56.6955 = 91% of
emissions to the operator's own address). The markets-modality reading is
sound, the falsifier honestly marks per-wallet/per-IP caps unobservable
(audit :6-8, :70), and the 15-minute move (rewards_wallet + rail_class on
every payout receipt, wallet named before the burst) is correctly priced.
The lens also correctly pre-empts the defense: on a test rail the burst is
legal; the crime is a receipt that lets it read as demand evidence.

## What the lens missed (additions, this pass)

A1. CONVERGENT and universal-breaking: the estate's own consensus-illusion law
already holds the measured shared-bias doctrine the lens derived from the
same-day paper. mag/consensus_gate.py:1-26 (LAW-CONS-ILLU-001, AUROC 0.09 at
120B, unanimity anti-signal, calibration ladder by parameter count) plus the
R3-hardened refusals and tests/test_consensus_degeneracy_20261005.py:6-14
(single-answer unanimity, refusal triplets, byte-identical quads with inflated
independence, unconstructed strong paths). Consequence: the perimeter's A2
metric "majority/exact-match" (CARD.md:16-18) is uncertified against model
scale and correlation by the estate's own law; a k_harness reporting raw
majority agreement would certify mode collapse as consensus.
Falsifier: a k_harness run where K small/same-family models return unanimous
wrong answers and the receipt reads consensus-signal.
Move (~30 min inside the F1 sitting): k_harness imports
mag/consensus_gate.verdict/classify_batch (or ports the ladder + refusal
strip + n>=2 floor) and stamps its output on every consensus row; the four
degeneracy tests become the harness's own falsifier suite.

A2. The loop sang at K=3 with ground truth before it sang at K=2:
mag/_consensus_witness.py (2026-08-25) fires one grounded question
(12 x 13, GROUND_TRUTH "156") to three heterogeneous free lanes and measures
per-lane correctness AND cross-lane agreement, with a dormant-gate lane filter
(B2-521). This is F1's organ and F3's ground-truth arm in one file, unread by
the lens.
Falsifier: if the witness file's shape cannot be generalized past its single
hardcoded question, it stays a demo, not an instrument.
Move (~20 min): steal the shape (grounded question, per-lane correctness,
agreement matrix, dormant-gate filter on node liveness) into k_harness v0.

A3. Same-family collapse in the 14-provider fan: config.gstd.json verified 14
gstd-tier providers, but several share base weights (qwen2.5:7b + q8 variant;
gemma4 + desk + hermes tunes; ROUTER_VOCAB_LANDED.md rows 1-2 and 10-12). A
K-fan drawn from all 14 counts quant variants and persona tunes of one base as
independent voices, inflating agreement by construction, and per unisub's own
within-architecture qualifier same-family pairs are exactly the predicted
convergence regime. Also all 14 ride one localhost:8080 gateway whose shared
rate bucket ROUTER_VOCAB_LANDED.md:135-141 measured as the bottleneck (1-3
retries, 25s backoff per call), bounding K-fan pacing in the one-sitting move.
Falsifier: a per-family deduped agreement matrix that collapses to near the
pooled one proves family weighting does not matter.
Move (~15 min): weight-family tag on every contender row; agreement matrix
reported pooled AND family-deduped; the two numbers on every receipt.

A4. The dead-salmon arm should be a z-test, not a delta print:
mag/volume_fidelity.py:13-20 shows the estate's own null-control form
(shuffled null ensemble, z < 1.5 => DECORATION). "Consensus must beat a
label-shuffled baseline" (CARD.md:19-20) left as a raw DELTA invites
eyeballing; the z-form is already estate style.
Falsifier: a consensus-vs-shuffle gap under z 1.5 read as signal.
Move (~10 min inside the F3 sitting): report beats-shuffle z, not (only) delta.

A5. The seed's boot channel for foreign containers is unnamed everywhere:
F4's move runs tools/seed_mcp.py (377 lines of repo code) inside a vast.ai
container with "no estate repo, cold disk"; how the server binary itself
arrives (clone, wheel, docker image) is specified neither by the perimeter
card nor by the move, so the proof risks demonstrating same-repo-clone works
rather than portability.
Falsifier: a container that cannot obtain and start the seed server without
operator hand-copying estate files downgrades proved-portable to
proved-shippable-only-after-a-channel-decision.
Move (~10 min of spec, then the same sitting): name the channel in the F4 run
(docker image tag or git clone of a public mirror) BEFORE renting the instance.

## Scorecard

Confirmed: F2, F4, F5 (evidence byte-intact, falsifiers honest, moves priced).
Weakened: F1, F3 (survive in scoped form; both universals broken by the
full-tree census; both moves survive amended). Killed: none. The lens's
sharpest contribution that survives untouched is F2's OFF-CHAIN-THEATER stamp
design; its largest debt is the quantifier-law breach on mag/, which cost it
the estate's own consensus law (A1) as prior art.
