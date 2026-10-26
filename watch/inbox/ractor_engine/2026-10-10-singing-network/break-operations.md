# BREAK-OPERATIONS: hostile pass on the operations lens (2026-10-10)

Breaker seat: break-operations (the second pass). Target:
watch/inbox/ractor_engine/2026-10-10-singing-network/operations.md (read in full
this sitting; the ask's JSON copy was truncated mid-F5, the disk file is
authoritative). Method: re-read every cited primary source and code site
firsthand, re-run the absence censuses scoped, attack each falsifier for
dropped conditions. Everything below was read or run this sitting; no em-dashes.

## Verdicts

### F1 (A1 measures the theater) - CONFIRMED

Every cite byte-checks clean, read firsthand this sitting:

- CARD.md:13-14 is the A1 block with no instrument named (read).
- reference/gstdcoin/gstdbot/src/blockchain/token.ts:387-404 recordEarning:
  `hash: 'tx_' + randomBytes(16).toString('hex')` at :391, `status:
  'confirmed'` at :398. Exactly as the lens quoted.
- GSTD_TOKENOMICS_AUDIT.md:19-23 banks precisely what the lens says:
  token.ts:387-396 fabrication, server.ts:3305 claim txHash, engine.ts:15
  header-vs-zero-chain-code. The D1 counter cite is audit line 17-19
  (platform-link.ts:246 comment, which I also read: "Nodes earn TASK_FEE_GSTD
  per completed task recorded in D1").
- CONVERGENT flag is fair: audit doc + my independent source read agree.

Falsifier attack (one dropped condition): "if chain-read balance deltas equal
platform-claimed deltas on every staging task, A1 passes honestly" presumes
staging mints on-chain at all. If GB's staging rail pays purely via D1 (as the
live platform does, audit sec 1), chain deltas are ZERO BY DESIGN and every
staging task "diverges" without any theater being caught. The A1 spec must
first bank GB's answer to "does staging settle on testnet?" and carry a third
arm: if no, the honest A1 on staging is D1-delta == node-claimed-delta with
the chain leg marked UNOBSERVABLE, not "theater caught". The lens's own blind
spot names testnet-vs-mainnet as unobservable but the falsifier does not
consume it.

### F2 (A2 must route through consensus_gate + family blocks) - CONFIRMED

- mag/consensus_gate.py read in full: CALIBRATION_LADDER (2.0, 0.62) at :47,
  (7.0, 0.71) at :49, CONFIRMATION_THRESHOLD 0.85 at :57,
  SMALL_MODEL_FLOOR_B = 3.0 at :60, LAW-CONS-ILL-001 at :3-4. All constants
  as cited.
- CARD.md:19-20 read: the control battery names ONLY the label-shuffle
  baseline. Verified.
- ROUTER_VOCAB_LANDED.md sec 2 read and re-counted: the lens said "5
  qwen2-class, 5 gemma-class" of 14. Actual census from the table: qwen2-arch
  strict = rows 1-5 (5), plus qwen25vl row 6 and qwen2-arch r1-distill row 7
  (qwen-lineage 5-7); gemma-class = rows 8-13 = SIX (gemma:2b, gemma2:2b,
  gemma4, gemma4-desk, gemma4-hermes, athena-class 30.7B); ternary 27B = 1.
  Two families hold 12-14 of 14, and the lens's "2-8B params plus one 27B"
  misses that athena-class is a 30.7B gemma4. The correlation worry is
  STRONGER than the lens stated, not weaker. Conclusion unaffected;
  counts corrected.
- volume_fidelity.py: line 355 (perm shuffle null) and :407 (label-shuffle
  null) are genuine K-shuffle null models; :398 is pair-index subsampling,
  not a null. Cite substantially holds.

Two amendments the move needs (both found this sitting):

1. verdict() is same-model-shaped: it takes ONE model_params_b scalar
   (consensus_gate.py:114-116) and its docstring frames the pool as N runs of
   one janitor model. A heterogeneous fleet has K different sizes; the import
   is not mechanical. Honest adaptation: call verdict() per model family
   block, or extend the organ with a per-response params list. ALSO:
   SMALL_MODEL_FLOOR_B=3.0 means any pool typed at <3B can never return
   CONFIRMED (consensus_gate.py:165-167), so typing the fleet at min-params
   makes most unanimous sweeps UNVERIFIED by construction. That is the gate
   being strict, which is correct, but the spec must say so or the first
   receipts will look like the harness is broken.
2. consensus_gate has ZERO production consumers today: census run this
   sitting (grep consensus_gate over mag/ tools/ tests/ *.py) returns only
   mag/consensus_gate.py itself and tests/test_consensus_degeneracy_20261005.py.
   The perimeter harness would be its first production consumer; if the
   harness ships computing consensus without calling it, the estate births
   another unwired organ with a law sitting beside it.

### F3 (consensus-contrib rows do not exist; read verdict_log) - CONFIRMED

tools/gps_mcp/ledger.py read in full this sitting. All four cites verified:

- Schema is exactly two tables + one index: SCHEMA_SQL :132-158. No consensus
  class. CARD.md:80 read: "Feeds the GPS capability ledger as
  consensus-contrib rows" names a nonexistent row class.
- Dedupe triple (model_id, task_shape, evidence_hash): partial UNIQUE index
  :32-34 and :153-157, SELECT fast path :393-413.
- "it logs, it does not punish": record_verdict docstring :366 (and module
  docstring :91). The clamp itself: :434-443 on capability means only.
- "v0 is single-threaded anyway": connection() comment :273.
- The falsifier's instrument exists: tools/gps_mcp/receipts.jsonl present on
  disk (29,554 bytes, mtime 2026-10-09) and its tail carries the verbatim
  reason line "1 candidate(s) pass constraints and pass-rate threshold 0.85;
  cheapest wins" (read this sitting).

One dropped condition (addition A3 below): the same dedupe gate that keeps
per-model rows distinct WITHIN a sweep will collapse ACROSS-sweep reruns
whenever a deterministic model (temp 0, the natural setting for the exact-match
shapes A2 wants) returns byte-identical answers to the same prompt: same
evidence_hash, duplicate-skipped, capability frozen at sweep 1. Sweep evidence
bytes must include per-run variance (sweep id, node id, latency, payout delta)
or a repeated Phase 3 task bank measures once and then goes silent.

### F4 (Phase 2 sizing fails its own rate-bucket law) - CONFIRMED, STRENGTHENED ~4x

Cites verified: pitch CARD.md:18-21 (6/11 at ~16/min, sustained ~1 req/10-15s,
120/min nominal), perimeter CARD.md:68-69 (5 instances x 10 nodes), :40-43
(the RATE-BUCKET LAW paragraph), :56-58 (staging limits UNOBSERVABLE until GB
confirms).

The arithmetic correction (found this sitting, the substantive break):

- The lens read the SIGNATURE DEFAULTS: platform-link.ts:85
  `start(intervalMs = 60000)`, :253 `startTaskLoop(intervalMs = 30000)`. Both
  verified. But the production call sites are in
  reference/gstdcoin/gstdbot/src/gateway/server.ts:4749-4750:
  `this.platformLink.start(10 * 60_000)` (heartbeat 600s) and
  `this.platformLink.startTaskLoop(5000)` with the comment "poll for tasks
  every 5s". The 5s poll is HARDCODED: grep of gstdbot/src for
  TASK_POLL/POLL_INTERVAL/HEARTBEAT_INTERVAL env overrides returns nothing
  near these call sites. The lens knew the production heartbeat was 600s
  (cited the audit's 600s beats) yet still ran its arithmetic on the 60s/30s
  defaults, and never found the 5s poll at all.
- Production per-node outbound to the platform is ~12.1 req/min (5s poll +
  0.1/min heartbeat). Ten nodes on one instance: ~121 req/min, against a
  bucket measured to 429 at ~16/min with sustained usable 4-6/min. That is a
  20-30x overage, not the lens's 3.5-7x. Phase 1 (3-5 desktop nodes) is
  36-60/min, not 6-15/min.
- Arm 1's own sizing line compounds it: CARD.md:44 sizes a 64-128GB instance
  at 30-60 node containers, i.e. 363-726 req/min from one IP if each
  container runs its own link. The CARD's Arm 1 paragraph and its
  RATE-BUCKET LAW paragraph are internally inconsistent at production
  cadences.
- Second loop found: compute/marketplace.ts:73 JOB_POLL_INTERVAL = 15_000
  (+4 req/min per node) whenever that module boots. The lens counted neither
  loop correctly.

The conclusion (sizing fails its own law) survives and hardens: the
shared-platform-link-per-host / token-bucket fix is not the cheaper option,
it is the only shape that fits the measured bucket at all. Falsifier dropped
condition: "zero 429s on staging" can also mean the staging deployment ships
without the production rate limiter or with whitelisted IPs; a green result
then proves nothing about production sizing. The falsifier must either
confirm the staging limiter exists (GB question) or rerun the probe against
the public platform endpoint.

### F5 (the perimeter IS the seed-MCP second consumer) - WEAKENED

Evidence cites all verified: mcp_layer_status_20261010.md sec 6 item 4 (read,
lines 114-116: "a SECOND, different-client cold boot (e.g. a garage-guild
bench or a Pierre-class external) would upgrade it from proved-once to
proved-portable"), SEED_RIB_FORMAT_v0_20260926.md (inline/pointer carriers
:44-49 and :110-118, never-invent law :72-73 and :96-99), ROUTER_VOCAB sec 4
+ live receipts.jsonl reason line. The learning instrument (coverage of
evidence_resolved=1 pairs grows AND routing decisions change) is sound and
its reason-line instrument is real on disk.

The claim overreaches on the doctrine's own bar:

1. Sec 6 item 4 asks for a DIFFERENT-CLIENT boot. A vast Ubuntu instance
   running the estate's own tools/seed_mcp.py is the SAME client class on a
   new machine. That banks machine-portability (real, worth having); it does
   not bank the client-portability the open item names. The lens quietly
   retitled the bar; its own falsifier (c) ("fails portability" below 10/10)
   does not test client class at all.
2. The gstd-node containers themselves are not MCP clients in any sense:
   gstdbot speaks platform HTTP (platform-link.ts fetch loops), not MCP. The
   cold client on a vast instance is the harness/orchestrator seat, i.e.
   estate code either way. Folding the seed boot into the harness spec is
   still the right one-afternoon move; calling it the doctrine's second
   consumer is the overclaim. Client-portability still wants the garage
   bench or Pierre-class external.

The toggle's opt-in framing (OURS never a requirement) is intact and the
falsifier set (a) fat-images-anyway and (b) accumulation theater are good
instruments; only the headline verdict weakens.

## Blind-spot adjudication (the lens's own list)

- "No consensus harness code exists in the tree... grep found no
  dispatcher/aggregator": WEAKENED as phrased. My scoped census this sitting
  (grep -rniE over mag/ + tools/ *.py for consensus+harness/dispatch/aggregate
  and for class *sweep*/*harness*/*dispatcher*/*aggregator*) found
  mag/riddler_transport.py (dispatches to K providers, one surrogate face
  each, aggregates consensus_action/consensus_strength, :222, :422-423) and
  mag/research_director.py:552 (aggregated consensus_action).
  Dispatch-to-K-then-aggregate-consensus machinery DOES exist in the riddler
  lane; what does not exist is the perimeter's exact shape (same task to K
  heterogeneous models on gstd task shapes). Scoped absence true, universal
  phrasing overstated (the quantifier law's own class).
- mcp_parity.py: NOT RUN by this breaker either. No finding's evidence chain
  depends on the five-surfaces status; it remains a self-report from
  mcp_layer_status_20261010.md and is cited as such.
- vast pricing, staging endpoint, GB-side facts: agreed unobservable; this
  pass added two GB-side preconditions the falsifiers must consume (A4).

## Additions (what the lens missed)

1. The production 5s poll (gateway/server.ts:4750, hardcoded) makes Phase 2's
   overage 20-30x, not 3.5-7x, and Arm 1's 30-60-container sizing
   (CARD.md:44) self-contradicts the RATE-BUCKET LAW paragraph. Evidence:
   server.ts:4749-4750 read this sitting; no env override (grep). Falsifier:
   a staging or config flag that disables the 5s poll loop (none exists in
   the clone as of e0bbe48). Move (~20 min): amend the CARD sizing block with
   production cadences and make shared-link-or-token-bucket a Phase 2 GO
   condition, not an option.
2. consensus_gate has zero production consumers (census this sitting: only
   tests/test_consensus_degeneracy_20261005.py). The perimeter harness is its
   first chance to be load-bearing; ship the harness without calling verdict()
   and the LAW-CONS-ILL-001 organ stays doctrine-decorated. Falsifier: grep
   for consensus_gate consumers outside tests after the harness lands; zero
   means the law was cited, not used.
3. The a04 dedupe gate freezes deterministic reruns: same prompt + same model
   + temp 0 -> identical answer bytes -> identical evidence_hash ->
   duplicate-skipped (ledger.py:27-34, :393-413); a repeated Phase 3 task
   bank measures once. Evidence: ledger.py read this sitting. Falsifier: run
   the same task twice through record_verdict with identical evidence_bytes;
   second call must return duplicate-skipped and capability must not move.
   Move (~10 min): the harness spec's evidence payload names per-run variance
   fields (sweep id, node id, latency, payout delta).
4. A1's two GB-side preconditions the falsifiers dropped: (a) whether staging
   settles on-chain at all (else the chain reader measures design, not
   theater, GSTD_TOKENOMICS_AUDIT.md:17-19); (b) the 402/DEPLOYMENT_DISABLED
   kill switch (audit :114-119, platform can silence any node at will)
   confounds Phase 3's "does payout hold at 1000 participants": the receipt
   must distinguish payout-failed-at-scale from centrally-switched-off.
   Falsifier: a Phase 3 receipt attributing silence to payout failure
   without logging each node's DEPLOYMENT_DISABLED state.
5. A2's control battery is missing the random-weights arm: the estate's own
   dead-salmon card mandates "a mandatory negative-control arm (random-weights
   model, label-shuffled run)" (dead_salmon_airllm_drop_20261010/CARD.md:21-24)
   while the perimeter CARD.md:19-20 and the lens's F2 both carry only the
   label-shuffle. A random-init small model is nearly free on vast/blade and
   closes the battery to the estate's own published standard. Falsifier: a
   consensus rate on real models that does not beat BOTH nulls (shuffled
   labels, random weights) is dead salmon by the card's own law.
6. The dispatch-path fork is unnamed: the GPS facade is MCP-shaped but not
   MCP-wired (mcp_layer_status sec 6 item 3). The harness should call
   tools/gps_mcp/router.py in-process the way the pace instrument did
   (ROUTER_VOCAB sec 3, pace_run.py "direct call -> ... -> routed ask"),
   NOT convert the documented wiring debt into a Phase 1 dependency.
   Falsifier: a Phase 1 harness blocked on MCP wiring work is the wrong fork
   by construction.

## Instrument log (what this pass actually ran)

- Read in full: gstd_perimeter_design CARD.md, mcp_layer_status_20261010.md,
  gstd_gb_pitch CARD.md, GSTD_TOKENOMICS_AUDIT.md, ROUTER_VOCAB_LANDED.md,
  SEED_RIB_FORMAT_v0, unisub CARD.md, dead_salmon CARD.md, garage_wizard
  CARD.md, mag_magatama CARD.md, ractor50/mcp.md, RIB_LIVING_WEIGHTS,
  gstd_distribution_thesis, mag/consensus_gate.py, tools/gps_mcp/ledger.py,
  the lens file operations.md.
- Read at cite sites: token.ts:370-419, platform-link.ts:70-110 and :195-264,
  gateway/server.ts:4720-4764, volume_fidelity.py:345-418,
  riddler_transport.py:200-259.
- Ran: locate platform-link.ts/token.ts; grep startTaskLoop + platformLink.start
  call sites; grep TASK_POLL/HEARTBEAT_INTERVAL env overrides; grep
  consensus+harness/dispatch/aggregate and class-shape census over mag/ +
  tools/ *.py; grep consensus_gate consumers over mag/ tools/ tests/; ls +
  tail of tools/gps_mcp/receipts.jsonl and gps_ledger.db3.
- NOT run: tools/mcp_parity.py (no verdict depends on it), any live network
  call (staging does not exist; public platform not probed this pass).
