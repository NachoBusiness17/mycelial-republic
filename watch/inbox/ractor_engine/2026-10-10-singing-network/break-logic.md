# BREAK-LOGIC PASS: hostile second read of the logic lens (2026-10-10, seat break-logic)

Target: watch/inbox/ractor_engine/2026-10-10-singing-network/logic.md (findings
F1-F5 + blind spots), topic THE SINGING NETWORK (GSTD closed perimeter +
heterogeneous-model consensus + estate MCP toggle layer). Method: byte-check
every evidence cite against the named files, rerun every check the lens claims
to have run, attack the falsifiers, hunt the dropped conditions. No em-dashes.
Every claim below is what I read or ran THIS sitting on THIS tree.

## Verdicts (one per lens finding)

### F1 promote-gate disagreement (live router promotes on n=1): CONFIRMED

Every cite holds and the probe reproduces VERBATIM on a fresh throwaway ledger:

- Code cites byte-checked: router.py:245-268 (passes_threshold = pass_rate >=
  threshold only; sample_size rides the Candidate at :263 and never gates),
  router.py:315 (exploration ends the moment task_shape_has_history is true),
  router.py:336-344 (qualifying branch), ledger.py:712-728 (get_rate +
  task_shape_has_history; the latter flips on ANY capability row, SELECT 1
  ... LIMIT 1 at :723-728).
- Probe rerun mine, throwaway db in TEMP, shipped test-double config.json,
  offline (production gps_ledger.db3 untouched). Output verbatim:
  `verdict result: 1.0 1 resolved`; `A chosen = yesno-tiny`,
  `A exploration = False`,
  `A reasons = ["1 candidate(s) pass constraints and pass-rate threshold 0.85; cheapest wins"]`;
  never-seen shape: `B chosen = flash-mid-1`, `B exploration = True`,
  exploration reason line verbatim; capability row after n=1: rate 1.0 n 1,
  task_shape_has_history True. Identical to logic.md F1 in every byte that
  matters.
- min_support=5 confirmed at ROUTER_VOCAB_LANDED.md:14-19 (the ml3 route
  table's evidence gate), so the 1-vs-5 disagreement is real.
- The move is live, not already done: Constraints (router.py:65-69) has NO
  min-sample field; grep for min_sample/sample_floor/MIN_SAMPLE across
  tools/gps_mcp/*.py = zero hits; no receipt in the lens's scoped set
  (gstd_basecamp_20260109/, mcp_layer_status_20261010.md, ractor50/mcp.md)
  flags the n=1 promotion (grep rerun, zero hits).

Strengthening found by my pass (see Addition 1): the capture has a SECOND
latch the lens did not name. After 1 pass + 5 distinct-evidence fails (rate
0.167, n=6) the router STILL chose yesno-tiny, reason verbatim
"no candidate meets pass-rate threshold 0.85; cheapest constraint-passing
fallback (yesno-tiny at 0.16666666666666666)" (router.py:345-353: the
fallback branch sorts by cost alone and ignores pass_rate entirely). So even
a measured-bad cheap model stays pinned whenever no candidate qualifies,
which is the early-fleet norm since only touched models carry rates. F1's fix
must gate the fallback branch too or the floor just moves the pin.

### F2 family-correlated consensus certified as network consensus: CONFIRMED

- Grep rerun mine: `grep -n -i -E "consensus_gate|duel|family"
  watch/inbox/gstd_perimeter_design_20261010/CARD.md` = exit 1, zero hits.
  The absence claim names its instrument and scope; I re-censused it.
- Fleet recount from the vocab table (ROUTER_VOCAB_LANDED.md:34-50): rows 1-7
  qwen-lineage (row 6 is qwen25vl arch, still qwen lineage; row 7 is a qwen2
  distill), rows 8-13 gemma-lineage, row 14 ternary experiment, row 15
  unmapped embedding. 7 of 14 mapped qwen + 6 gemma = the lens's count,
  exact.
- CARD.md:44-45 verbatim: "1-2GB each with shared small models".
- Consensus-gate outputs ALL reproduced live this sitting:
  same3@2B = UNVERIFIED, same3@30B = CONFIRMED, single = UNVERIFIED,
  allrefusal = UNVERIFIED, split = DISPUTED. CID ladder numbers verified at
  mag/consensus_gate.py:47 (2.0, 0.62) and :53 (120.0, 0.09); law text at
  :1-26.
- Cross-family duel law verified where the lens cited it: family_of at
  router.py:618-620; the challenger-must-differ loop at router.py:799-807
  (with the only-one-family gap named at :808-812).
- Label-shuffle vs lineage argument is code-grounded, not rhetoric: the
  shuffle reassigns labels across the SAME models, so a wrong answer shared
  by siblings survives every permutation. Sound.

One instrument gap in the lens's own move (Addition 2): the gate it tells the
perimeter to adopt is homogeneous-pool by signature (one model_params_b
scalar for the whole response list, mag/consensus_gate.py:113-117); wiring it
into a heterogeneous fleet needs a per-response-params amendment first.

### F3 phantom adjudicator between the two balances: CONFIRMED (CONVERGENT flag justified)

- Grep rerun mine: `grep -rn -E "verifyQuorum|SettleTaskWithProof"
  reference/gstdcoin/contracts | wc -l` = 0. And the other half of the claim
  verified: the node code DOES point at the phantom names, six sites
  (gstdbot/src/p2p/attestation.ts:3, :34, :80; p2p/identity.ts:11;
  p2p/node.ts:128; swarm/agent.ts:694). Two instruments, phantom third,
  reproduced.
- The prior-audit convergence is real: GSTD_TOKENOMICS_AUDIT.md:48-53
  carries the same zero-hit grep dated 2026-10-09. CONVERGENT per the
  duplication law (independent re-derivation, different run).
- Audit cites verified: :17-24 (gstd_earned is a platform D1 counter;
  token.ts:387-396 fabricates 'tx_'+randomBytes status confirmed;
  /api/rewards/claim fabricates txHash; engine.ts promises chain settlement
  with zero chain-call code).
- Contract cites verified on today's tree: SettlementMaster.tact:16-22
  (SettleTask message carries workerAddr/gstdBonusAmount/qualityScore/
  computeUnits as trusted fields), :128-129 (require sender is owner or
  gateway, "Only DAO or Gateway can settle"); GSTDJetton.tact:89-108 area
  (mintAuthority state at :89, init + maxSupply 1B + workerPoolMax 400M at
  :103-111).
- CARD.md:13-14 A1 wording verified, including "closes our audit's
  settlement-theater finding on a staging rail".

The falsifier (chain-read before/after) is the right instrument and its
cheap wrapper estimate is plausible. Additions 4 sharpens the instrument set
(claim path + kill switch were also unnamed).

### F4 toggle-doctrine mislabel + no consensus-shaped write path: CONFIRMED, one framing correction

Byte-facts all verified:

- CARD.md:79-81 carries "Feeds the GPS capability ledger as
  consensus-contrib rows" verbatim.
- The write path does not exist: schema is capability + verdict_log only
  (ledger.py:5-34); verdict is INTEGER 1 pass / 0 fail (ledger.py:20) and
  _normalize_verdict REJECTS anything unparseable (ledger.py:564-577), so a
  consensus-flavored verdict literally cannot be expressed in the current
  write path. No consensus table anywhere in the schema docstring.
- pace_run.py instrument cite verified (ROUTER_VOCAB_LANDED.md:100-102,
  direct call -> mechanical grade -> verdict -> routed ask).
- GB-side memory cite verified (GSTD_TOKENOMICS_AUDIT.md:75-81: reputation
  formula unpublished, D1 counters).

Framing correction (weakens the rhetoric, not the finding): the harness spec
that embeds the ledger is OUR lane (CARD.md:75 heading "The harness (one
lane, reuses estate organs)"), not a GB-side dependency; GB's platform never
reads our ledger. "HIS harness spec already embeds the ledger" overstates
whose requirement it is. The substantive claim survives intact: the fold
must declare the ledger load-bearing on OUR side with mechanical-grade-only
capability writes and a separate append-only consensus receipt lane, exactly
as the lens's move prescribes.

### F5 routing-differential test as the acceptance bar: CONFIRMED

- router.py:336-344 (selection reads capability) and :281-295 (momentum
  tiebreak, the only verdict-history sensitivity beyond threshold) verified.
- CARD.md:75-81 aggregator scope verified: consensus rate, matrix,
  dead-salmon arm, receipts, ledger feed; no differential test named
  anywhere in the card.
- Determinism precondition for the frozen-snapshot arm holds: _select is a
  function of (registry config, ledger state, constraints) only; receipts
  are append-only and never read back into selection (Router.__init__
  router.py:226-231; ReceiptLog write-only use at :389-399). The three-arm
  falsifier (frozen/decoration/echo) is sound and each arm catches a
  distinct fake.

## Blind-spot audit

All six blind spots are honest and hold. Two corrections:

1. The not-run note says "the gps_mcp test suite (28 tests)". I ran it:
   `./.venv/Scripts/python.exe -m pytest tools/gps_mcp -q
   -p no:cacheprovider` = 42 passed in 5.97s, zero failures. The lens's 28
   is a hand-copied count inside a not-run note; the suite is green today.
2. The mcp_layer_status_20261010.md:114-116 cite (seed-MCP second-consumer
   proof owed) is byte-accurate (verified at :114-116).

## What the lens missed (additions, each run or read this sitting)

1. (CONVERGENT with F1, deeper latch) The no-qualifier fallback re-pins the
   cheapest model after measured failure: 1 pass + 5 distinct-evidence fails
   (rate 0.167) and the router still chose yesno-tiny via the fallback
   branch, which sorts by cost alone and ignores pass_rate (router.py:345-
   353; probe output quoted in the F1 verdict above). Falsifier: give a
   second model qualifying history (rate >= 0.85) and rerun; if the
   qualifying branch then wins, the latch only holds while no model
   qualifies, which is still the early-fleet norm. Move (~10 min on top of
   F1's fix): the min-sample floor must gate the fallback branch too.
2. The organ F2 prescribes is homogeneous-pool by signature: verdict()
   applies ONE model_params_b scalar to the entire response list
   (mag/consensus_gate.py:113-117), so the tri-state cannot express a
   heterogeneous fleet (K DIFFERENT models is A2's whole point). Falsifier:
   grade the same mixed-pool bytes at min-size vs max-size; the verdict
   flips between UNVERIFIED and CONFIRMED with no per-model truth changed.
   Move (~20 min before Phase 1): per-response params or conservative
   min-of-pool.
3. A2 ships one of the two mandatory dead-salmon arms: the doctrine the card
   cites mandates BOTH a random-weights model AND a label-shuffled run
   (dead_salmon_airllm_drop_20261010/CARD.md:21-24); CARD.md:19-20 carries
   only the shuffle. The dropped arm is the one that catches
   answer-leakage-from-task-signature, complementary to F2's lineage catch.
   Falsifier: run a garbage-model arm; if its consensus rate approximates
   the fleet's, the task bank leaks answers. Move (~15 min): add the arm to
   the harness spec.
4. A1's instrument set omits the claim path and the kill switch: the audit
   proved earnings custody is auth-by-address (/api/wallet/claim forwards
   only X-Wallet-Address, server.ts:2511-2534, audit :104-105) while
   CARD.md:37-39 pins node identities, not wallet keys, and the card has no
   custody design for 50-100 per-container wallets; and the platform can
   silence any node at will (402/403 kill-switch class, platform-link.ts:
   131-137, audit :115-117), so at 1000 nodes a silent stall can masquerade
   as payout failure. Falsifier: claim from a second machine using only the
   address string; if the claim lands, custody is string-knowledge and A1's
   "balance delta lands" has a spoofable read. Move (~15 min): name wallet
   custody and an HTTP-status receipt class in the fold, banked beside the
   D1-vs-chain divergence class.
5. The card's scientific analogy drops the source's own qualifier: CARD.md:
   22-25 calls A2 "the behavioral analog of today's unisub paper claim
   (disjoint models converge)", but the drop card's own honest-caveat
   section says universality is WITHIN shared architectures, "do not
   overclaim cross-architecture" (unisub_drop_20261010/CARD.md:14 and
   :51-55). A2's fleet is cross-family by design, so the card motivates the
   test with the stronger unqualified claim; a LOW cross-family consensus
   rate would then read as network failure when it is the hypothesis's
   stated boundary. Falsifier: none needed, it is a citation defect.
   Move (~10 min): pre-register both expected directions (within-family
   convergence expected per the paper; cross-family open) in the harness
   spec.

## Checks run this sitting (mine)

1. Router probe replica, throwaway ledger, shipped config.json, offline:
   output in F1 verdict. Command: .venv/Scripts/python.exe on a TEMP script
   (deleted after; TEMP scratch verified empty).
2. Fallback re-pin probe, same conditions: output in F1 verdict + Addition 1.
3. Consensus-gate five-way tri-state check: output in F2 verdict.
4. grep CARD.md consensus_gate|duel|family: exit 1, zero hits.
5. grep contracts tree verifyQuorum|SettleTaskWithProof: 0 hits; grep
   gstdbot/src for the same names: 6 sites (the pointing-at half).
6. grep min_sample/sample_floor/MIN_SAMPLE across tools/gps_mcp/*.py and the
   lens's scoped receipt set: zero hits.
7. pytest tools/gps_mcp -q -p no:cacheprovider: 42 passed in 5.97s.
8. Personal line reads: SettlementMaster.tact:16-22, :120-149;
   GSTDJetton.tact:85-114; router.py:65-80, :220-355, :600-680, :780-839;
   ledger.py:1-60, :300-420, :545-744; consensus_gate.py (whole);
   GSTD_TOKENOMICS_AUDIT.md (whole); ROUTER_VOCAB_LANDED.md (whole);
   perimeter CARD.md (whole); mcp_layer_status_20261010.md:95-116;
   dead_salmon + unisub drop cards (whole); pitch-card falsifier lines.

Not run: live platform or chain reads (same blind spot as the lens, still
true); no Tact execution; vast.ai pricing page not fetched (prices stay
ESTIMATE-CLASS per CARD.md:6-9, verified verbatim).

## Net

The lens survives the hostile pass whole: five for five confirmed, one with
a framing correction (F4), all evidence intact under byte-check, both
absence claims re-censused with named instruments. My pass adds five
conditions the lens dropped, of which Addition 1 (the fallback latch) makes
F1's fix incomplete as specced, and Addition 2 makes F2's move unexecutable
as specced. The two moves that must absorb amendments before Phase 1 fires:
the min-sample floor belongs on BOTH branches, and the tri-state organ needs
per-model sizes before it can judge a heterogeneous fleet.
