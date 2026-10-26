# BREAK-LINEAGE pass: lineage.md (THE SINGING NETWORK) - 2026-10-10

Hostile second pass over
watch/inbox/ractor_engine/2026-10-10-singing-network/lineage.md. Every check
below was run THIS sitting (instrument named per row; moment 2026-10-10,
this break session). The ask's JSON truncated at F4; the on-disk lineage.md
carries five findings (F1-F5) and all five are verdicted here. No em-dashes.

## Verdicts

### F1 (A1 does not close settlement theater; phantom method unnamed): CONFIRMED

Every cite byte-holds, and the census is now triple-run:

- CARD.md:13-14 claims A1 "closes our audit's settlement-theater finding on a
  staging rail" - exact (sed read).
- GSTD_TOKENOMICS_AUDIT.md:17-24: D1 counter, token.ts:387-396 fabricated
  'tx_'+randomBytes, engine zero chain-call - exact (sed read).
- DOGFOOD paycheck quote: the quoted line is DOGFOOD_DATA.md:104-105, not
  :105 (spans two lines); substance exact, the only paycheck receipt read the
  platform counter.
- My grep re-run: `grep -rn -E "verifyQuorum|SettleTaskWithProof"
  reference/gstdcoin/contracts/ --exclude-dir=.git --exclude-dir=node_modules`
  = zero hit lines, exit 1. Node-side refs exact at
  gstdbot/src/p2p/attestation.ts:3, :34, :80; p2p/node.ts:128;
  swarm/agent.ts:694 (grep output this sitting). attestation.ts:2-3 carries
  the verbatim "MUST exactly match" quote.
- SettlementMaster.tact: `receive(msg: SettleTask)` at :128; full receive
  surface grep = 121, 128, 231, 237, 248, 256, 263 - no WithProof receiver,
  no verifyQuorum. Confirmed.
- The lens's AUDIT:132-134 cite for "Top unmet need" lands at :133-134
  (off by one line, substance exact).

Strengthened, not just confirmed: see Addition A3 (a 6th phantom-method site
the lens missed). CONVERGENT standing is real: audit grep 10-09, lens grep
10-10, my grep 10-10, all zero against contracts/.

### F2 (no sample-size floor in the live router): WEAKENED - operative core confirmed byte-exact, two sub-claims false

Confirmed by my re-runs:

- router.py:252-253 `passes_threshold = pass_rate >= constraints.pass_rate_threshold`
  - exact; DEFAULT_PASS_RATE_THRESHOLD = 0.85 at :40 - exact.
- sample_size never gates: `grep -n -E "min_sample|min_support"
  tools/gps_mcp/router.py` = zero hits, exit 1. It sorts (shape_table rank key,
  router.py:759-766) but no floor exists anywhere.
- "cheapest wins" reason string at router.py:340-341 - exact.
- gps_router_v0.py:237 `min_support: int = 5`, gating at :261 - exact.
- Ledger census re-run (.venv/Scripts/python.exe sqlite over
  tools/gps_mcp/gps_ledger.db3): capability 34 rows, 12 at n<=2, 6 at
  rate 1.0 with n<=2 - EXACT match, and the six rows are nameable:
  gemma2:2b summarize 1.0/1, gemma:2b probe 1.0/1, qwen2.5:3b classify
  1.0/1, qwen2.5:7b extract 1.0/1, deepseek-v4.1-flash schema-design 1.0/2
  and planning 1.0/2.
- ROUTER_VOCAB_LANDED.md:96-97 (rate 1.0 n=1 rows) and :117-124 (honest
  classify downgrade, 3 of 5) - exact.

What breaks:

1. CITE DEFECT: min_support=5 is named at ROUTER_VOCAB_LANDED.md:18, not
   :30-31. Line 18: "(min_support=5). Not the extension surface." Lines 30-31
   discuss the exploration test double. `grep -n min_support` over the file
   returns exactly one hit, :18.
2. LINEAGE NARRATIVE REVERSED: "invented in the generated-table instrument
   then dropped when the live router was built" is backwards. git bytes:
   tools/gps_mcp/router.py landed 2026-09-29 (91acc5bdf "gps-mcp v0 LANDED",
   git log --follow); min_support entered gps_router_v0.py 2026-10-07
   (9bac820a1, git log -S "min_support"); `git log -S "min_support" --
   tools/gps_mcp/router.py` returns ZERO commits - the floor never existed in
   the live router at any point. It was invented LATER in the shadow
   instrument and never ported back. For a lineage lens whose signature claim
   is the between-generations drop, the direction of this one is the product;
   it is wrong. The move survives unchanged (the port is the same 45-60 min).

### F3 (no boot path in the perimeter; seed MCP join_protocol fills it): CONFIRMED

All seven cite clusters byte-verified this sitting:

- CARD.md:37-43: identity pinning, rate buckets, tailnet; full CARD read
  confirms no boot/join clause anywhere in the file.
- seed_mcp.py:8-13 (pointer laws, --max-fetch cap) and :204-232 join_protocol
  7 steps; step 7 at :233-235 including the exact check "the fleet can audit
  the join from the receipt alone".
- mcp_layer_status_20261010.md: cold-join falsifier 10/10 hash-verified at
  :21-23 (lens said :19-22, one line early, substance exact); demand-precedes-
  organ at :109-111; second-consumer open item 4 at :114-116 - exact.
- ractor50/mcp.md:214-247: missing-tools items 1-7; seed_fetch item 3 at
  :234-239; estate_gps_ask/cascade item 6 at :246-247 - exact.
- estate_receipt_append live: tools/__init__.py:65 (TOOL_MAP entry) and
  mag/estate_bridge.py:122 (input schema) - exact.

### F4 (guild blade has no wallet law; silence defaults to silent mining): CONFIRMED

- CARD.md:59-61 guild-play quote - exact.
- gstd_distribution_thesis_20260109.md:22-28 "DEFAULT WALLET = THE USER'S
  OWN, loud opt-in... cannot silently mine for the founder" - exact; supporter
  toggle at :26-29.
- garage_wizard_network CARD.md:33-36 "each garage node = supply AND demand"
  and :91-96 receipt-weighted ranking - exact.
- The absence claim now carries a named instrument:
  `grep -n -i -E "wallet|revenue|split|payout"` over the garage CARD returns
  zero hits (exit 1); the perimeter CARD has zero wallet hits (full read +
  grep). Scope: those two documents only, as the lens scoped it.

### F5 (consensus measurement already banked; dead-salmon control tonight): WEAKENED - numbers byte-exact, the instrument as specified is unbuildable on current bytes

Confirmed by my re-runs:

- verdict_log arena-agreement-v1 rows: 461 - exact (sqlite count).
- Per-model rates: the lens read the CAPABILITY table, and it is byte-exact
  there: sonnet 0.3243/n=148, opus 0.5430/n=135, haiku 0.0467/n=107, fable
  0.3369/n=71 (capability rows, last_measured 2026-10-05T07:15:15Z).
- b8_gwap.md:99-103 feed receipt (distinct=461) - exact.
- dead_salmon CARD.md:19-25 falsifier law, unisub CARD.md:44-49,
  perimeter CARD.md:19-20, :22-25, :24-25, :80 (the consensus-contrib shape
  name that would orphan the warm half) - all exact.

What breaks:

1. NO TASK KEY. The MOVE specifies "sample verdicts with labels shuffled
   within task". verdict_log's schema is (ts, model_id, task_shape, verdict,
   evidence_hash, evidence_resolved, evidence_source, evidence_bytes) -
   pragma table_info this sitting; there is no task/round column, and
   evidence_hash does not substitute: 461 rows carry 461 DISTINCT
   evidence_hash values, zero groups with more than one verdict (group-by
   census this sitting). There is nothing to shuffle WITHIN. The control can
   only shuffle globally (a weaker arm) or wait for a schema key.
2. CLAMP ASYMMETRY. capability.pass_rate is a running mean with the LM7
   positive floor (ledger.py:356-373, operator positive-steering law
   2026-09-30: a fail during a RISING window may not sink the rate below the
   window-start floor). Measured consequence: the ledger's opus rate 0.5430
   vs the raw verdict fraction 72/135 = 0.5333; fable 0.3369 vs 23/71 =
   0.3239 (sonnet and haiku match raw exactly). A control that compares
   raw-shuffled rates against clamped-measured rates inherits a manufactured
   margin (+0.0097 opus, +0.0130 fable) that exists with zero signal - the
   exact fake-learning pass the control exists to catch. Both arms must go
   through the same write path, or compare raw-to-raw.
3. OVERSTATEMENT. "Those ARE heterogeneous-model-consensus numbers" - they
   are per-model agreement-with-the-arena rates. K-model MUTUAL consensus
   (A2's actual bar) is not reconstructable from these rows at all (see 1:
   no join key). Two models can each agree with the arena 32% on disjoint
   rounds and share 0% pairwise consensus.

The zero-spend-before-hardware spirit survives; the instrument needs a
schema key and a same-path comparison first.

## Additions (what the lens missed)

- A1 (SCHEMA, the load-bearing miss): the network's memory cannot express
  "same task, K models" - verdict_log has no task/round key and evidence_hash
  is per-verdict unique (461/461 distinct, 0 shared groups, census this
  sitting). Every consensus row the perimeter writes will be an unjoinable
  single-model verdict unless a task_id column (or a consensus table with a
  round key) lands first. The n-floor (F2) is a gate bug; this is a schema
  hole under the entire A2 design. Falsifier: show one query that joins two
  models' verdicts on the same task from current bytes. Move: ~30 min schema
  + writer amendment BEFORE Phase 1 receipts land.
- A2 (NORMS): the dead-salmon control must push both arms through the same
  ledger write path (LM7 clamp, ledger.py:356-373) or it is biased toward
  PASS by the measured deltas (opus +0.0097, fable +0.0130). Falsifier:
  replay both arms through record_verdict with identical inputs; equal rates
  kill this addition. Move: ~10 min clause on F5's MOVE.
- A3 (LAW): a SIXTH phantom-method site the census missed:
  gstdbot/src/p2p/identity.ts:11 - "directly usable in a SettleTaskWithProof
  attestation without any format conversion" - and identity.ts is live boot
  code (imported at src/index.ts:69, loadOrCreateAttestorIdentity; type
  consumed at attestation.ts:23). The signed lane's exposure is one organ
  wider than F1 banked. Falsifier: identity.ts removed from the import graph.
  Move: ~2 min, one line on F1.
- A4 (ARCHITECTURE): the no-floor exposure is not confined to ask()/_evaluate.
  shape_table()/pick_duel_contenders rank pass_rate desc with sample_size
  only as a tertiary tiebreaker (router.py:759-766; anchor = table[0] at
  :791-794), and shape_table[0] is the winner-rule ORACLE of
  tools/gps_mcp/gps_embed_trial.py (:93-96, :273). A rate-1.0 n=1 row is duel
  ANCHOR and trial oracle today. F2's fix scoped to Constraints/_evaluate
  leaves this lane crowning lucky-once models. Falsifier: a caller that
  pre-filters the table by n before table[0] (none found; grep this sitting).
  Move: ~15 min, floor the rank key or the table build.
- A5 (HONESTY): blind-spot 4 is byte-false. lineage.md mtime 14:03:33; eight
  of nine siblings carry earlier mtimes (accuracy 13:59:34, economics
  13:59:35, logic 13:59:47, operations 13:59:34, dogfood 14:00:56,
  moonshot-1 14:00:50, moonshot-2 14:01:54, security 14:00:59; ls
  --full-iso). Only communication.md (14:05:45) postdates. "Not on disk when
  I wrote" holds at most for one sibling; cross-lens dedup was possible from
  bytes. Caveat kept: concurrent authorship, mtimes measure completion.
  Falsifier: content or journal evidence lineage.md was drafted before
  13:59. Move: 0 min, the CONVERGENT flags need re-checking against the
  siblings that were present.

## Blind-spot audit (the lens's own honesty, byte-checked)

- GB staging unobservable: HOLDS (the CARD itself marks the class
  UNOBSERVABLE, CARD.md:57; no staging docs on disk).
- Harness not on disk / plan review: HOLDS (no harness file exists; the
  CARD's Phase 1 is future tense).
- Ledger census scoped to capability + verdict_log: HOLDS and was stricter
  than needed - sqlite_master shows the db has exactly those two tables, so
  the census covered the whole database.
- Sibling lenses absent: FAILS (Addition A5).
- vast.ai pricing not re-fetched: HOLDS (CARD.md:6-9 marks it estimate-class,
  dynamically loaded).

## Checks run this sitting

1. grep contracts + gstdbot/src for verifyQuorum|SettleTaskWithProof
   (exclusions named; zero in contracts/, six sites in src).
2. SettlementMaster.tact receive/message surface grep + sed 120-140.
3. .venv/Scripts/python.exe sqlite census: capability (34/12/6 + row list),
   verdict_log (461 arena rows, per-model k/n, verdict distribution,
   evidence_hash grouping, pragma columns).
4. sed reads: DOGFOOD_DATA.md:100-110; router.py:35-45,100-112,245-260,
   335-345,725-812; gps_router_v0.py:230-266; ROUTER_VOCAB_LANDED.md:10-33,
   93-126; seed_mcp.py:8-13,200-236; mcp_layer_status:17-24,107-118;
   ractor50/mcp.md:212-248; distribution thesis:20-30; garage CARD:31-38,
   89-97; b8_gwap.md:97-105; dead_salmon CARD:17-27; unisub CARD:44-49;
   tools/__init__.py:60-70; estate_bridge.py:115-130; attestation.ts:1-6;
   identity.ts:1-20.
5. git: log --follow both router files; log -S "min_support" on both.
6. ls --full-iso of the singing-network dir (mtimes).
7. Absence greps: wallet|revenue|split|payout over both CARDs; min_support
   over ROUTER_VOCAB_LANDED.md; callers of shape_table/pick_duel_contenders.
