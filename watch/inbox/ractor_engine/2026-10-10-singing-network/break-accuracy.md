# BREAK-ACCURACY pass: the singing network lens (2026-10-10)

Seat: break-accuracy (hostile second pass). Instrument: every lens evidence cite
re-read as bytes or re-run as a command this sitting; every command named with its
output. The lens report arrived TRUNCATED at finding 5's move text ("Restore the
qualifier in the CARD line and the GB addendum, o..."); verdicts below cover the
five findings received. No em-dashes by law.

## Verdicts (5 of 5 findings CONFIRMED; one lens caveat killed inside finding 3)

### 1. A2 ignores the live consensus-illusion law: CONFIRMED (strengthened)

Byte-check, all re-read this sitting:
- watch/inbox/gstd_perimeter_design_20261010/CARD.md:15-20: A2 is
  majority/exact-match for closed-form shapes with only the arXiv 2512.18792
  label-shuffle guard. Exact as cited.
- mag/consensus_gate.py: CALIBRATION_LADDER carries (2.0, 0.62) and (120.0, 0.09)
  at :45-54; REFUSAL_PREFIXES :70-88 plus _is_refusal :91-94 (the cited :70-94
  range is exact); MIN_SAMPLES_FOR_CONFIRMED = 2 at :64 with the comment at
  :62-63 (the cited :62-64 is exact).
- memory/facts/ox_artifact.jsonl:348-354: all seven rows are the CID lineage,
  present as cited. Row 350: "Majority/confidence aggregation implicitly assumes
  votes are conditionally independent draws around the truth. They are not";
  row 353 scopes the law to N responses from models "possibly the same model,
  possibly correlated via shared training data" - so heterogeneous fleets are
  INSIDE the law's scope. The lens's "de-certifies exactly the raw-majority
  signal" is byte-supported, not rhetorical.
- Grep `grep -rn "consensus_gate" --include="*.py" mag tools tests`: only
  mag/consensus_gate.py itself and tests/test_consensus_degeneracy_20261005.py.
  No harness, dispatcher, or aggregator consumes the organ. The lens's
  "grep found no consensus harness using it" is confirmed.
- Tests re-run (lens blind spot): `.venv/Scripts/python.exe -m pytest
  tests/test_consensus_degeneracy_20261005.py tests/test_gps_router_v0.py
  tests/test_gps_dedupe.py tests/test_gps_evidence_resolution.py
  tests/test_gps_coverage_20261005.py tests/test_gps_metabolism_20261005.py -q`
  -> 65 passed in 11.09s.
- Minor accuracy note (does not weaken): LAW-CONS-ILLU-001 is NOT enrolled in
  memory/law/registry.json (grep count 0 this sitting); the id resolves to the
  fact lineage (ox_artifact.jsonl) and the organ docstring only. The law's
  substance is live; the id is organ-local.

### 2. The GPS ledger banked the lax grader's verdict: CONFIRMED

Live sqlite on tools/gps_mcp/gps_ledger.db3, run this sitting:
- capability(qwen2.5:3b-instruct, classify) = pass_rate 1.0, sample_size 1.
- PRAGMA table_info(verdict_log): ts, model_id, task_shape, verdict,
  evidence_hash, evidence_resolved, evidence_source, evidence_bytes. NO grader
  column (docstring schema ledger.py:16-25 and live DDL agree; the lens's
  :16-23 cite is one line short of the column list tail, immaterial).
- ROUTER_VOCAB_LANDED.md:117-124 verbatim: "PASS under the declared
  presence-based grader ... HONEST DOWNGRADE: strict per-line pairing was 3 of 5
  ... treat qwen2.5:3b classify capability as weak, not proven-1.0."
- The banked row: verdict=1, evidence_resolved=1, evidence_source
  'gstd-node-live-20261009: pace run direct gateway call, receipt
  watch/inbox/gstd_basecamp_20260109/ROUTER_VOCAB_LANDED.md' - bytes attached,
  verdict never recomputed under the strict reader.
- Exactly 4 gstd-node-live rows exist (gemma:2b probe, gemma2:2b summarize,
  qwen2.5:3b classify, qwen2.5:7b extract), matching the lens move's "the 4".

### 3. No sample-size floor, no evidence filter on the read path: CONFIRMED,
### and the lens's own byte-honest caveat is FALSE (severity understated)

Byte-check of the mechanism claims:
- tools/gps_mcp/router.py:252-253: `passes_threshold = pass_rate >=
  constraints.pass_rate_threshold` - rate only; :263 reads sample_size into the
  Candidate; _select (:336 `qualifying = [c for c in eligible if
  c.passes_threshold]`) never gates on it; cheapest() ranks on
  (cost, momentum, tier, id). One pass at n=1 -> rate 1.0 -> routing grade.
- tools/gps_mcp/ledger.py:414-449: running-mean update
  (new_rate = (old_rate * old_size + v) / new_size), no floor, no evidence
  filter; :712-721 get_rate reads pass_rate/sample_size raw.
- Counts re-run at a second moment this sitting: 707 verdict rows, 494 with
  evidence_resolved=0 (EVIDENCE_RESOLVED semantics verified at ledger.py:121:
  "recomputed from bytes, agrees with claim"; resolved=0 = self-attested),
  34 capability rows. Identical to the lens's numbers.

The killed caveat: the lens wrote "of the 10 qualifying rows (rate >= 0.85)
zero have zero resolved verdicts, so the gap is structural, not yet bitten."
My per-row query this sitting: 6 of the 10 qualifying rows have ZERO
evidence_resolved=1 rows:
  mountain-world-v0/world-tick (resolved 0 of 4),
  legality-propagator-v1/legality-water-graph-v1 (resolved 0 of 100),
  x-ai/grok-4.7/adversarial-review (0 of 9),
  deepseek/deepseek-v4.1-flash/schema-design (0 of 2),
  deepseek/deepseek-v4.1-flash/planning (0 of 2),
  z-ai/glm-5.3-prime/askbank-v1-safeguard (0 of 3).
Alternate instrument tested (evidence_hash non-empty): 0 of 10 lack hashed
evidence - so the lens's sentence is true ONLY under the hash-presence
instrument its own 494 count does not use. The gap is ALREADY bitten: a
hundred-iteration running mean (legality-water-graph-v1, n=100) sits at
routing grade 1.0 on purely self-attested evidence. The finding survives
intact and gets louder, not softer.

### 4. A1 names no read instrument; scaler confound unpriced: CONFIRMED

- CARD.md:13-14 asserts "the paying node's balance/ledger delta lands as
  claimed" with no endpoint, no field; the harness line CARD.md:79
  ("payout delta asserted") is equally unnamed.
- Audit cites re-read this sitting from
  watch/inbox/gstd_basecamp_20260109/GSTD_TOKENOMICS_AUDIT.md: txHash
  fabrication at :20-21 (token.ts:387-396, server.ts:3305); idle accrual 152x
  at :71-72 (lens's :70-72 range includes it); reputation 51 -> 59 -> 49 while
  earning at :75-78; /api/v1/nodes "Permissionless read of the ledger ... MET"
  at :131 (with the audit's own caveat "for the counter, not for chain proof",
  which supports the lens's instrument choice).
- Lens blind spot 2 CLOSED this sitting: re-read the Tact contracts from
  reference/gstdcoin/contracts. SettlementMaster.tact (sed 100-140): SettleTask
  requires "Only DAO or Gateway can settle" plus the taskId replay guard;
  GSTDJetton.tact (sed 100-130): MintWorkerReward "Only Settlement can mint",
  maxSupply 1B, workerPoolMax 400M. The audit's contract cites byte-verify.

### 5. Dropped within-architecture qualifier: CONFIRMED, falsifier resolved

- unisub_drop_20261010/CARD.md:13-14 carries the qualifier verbatim ("within
  shared architectures - the abstract's own qualifier, do not overclaim
  cross-architecture"), and repeats it at :53-54.
- gstd_perimeter_design_20261010/CARD.md:22-23 renders it "(disjoint models
  converge)" with the qualifier gone; the GB addendum at :84-87 repeats the
  unscoped version.
- The lens could not re-fetch arXiv; I did (WebFetch this sitting,
  arxiv.org/abs/2512.05117): the abstract DOES carry the qualifier - "sparse,
  joint subspaces that are consistently exploited, within shared architectures
  across diverse tasks and datasets." The lens's falsifier resolves in the
  finding's favor. Refinement from the same fetch: the abstract's broad
  sentence ("regardless of initialization, task, or domain") carries no
  qualifier, and the abstract nowhere states disjoint-data convergence - that
  clause rides the paper body/site. The unisub card's "the abstract's own
  qualifier" is right about the qualifier, loose about the disjoint-data
  sentence's location.

## What the lens missed (additions)

1. ALREADY BITTEN (the strongest catch, and it corrects the lens): 6 of 10
   routing-grade capability rows ride zero resolved verdicts; worst is
   legality-propagator-v1/legality-water-graph-v1 at n=100, all self-attested,
   routing-grade 1.0 today. The lens's "not yet bitten" softened its own true
   finding. Move: ship the evidence filter / Wilson floor in the same sitting
   as the lens's fix and re-derive the 6 rows from resolved-only evidence
   before the perimeter writes anything (+30 min on top of the lens's fix).

2. A1's second unpriced confound: the platform kill switch. The audit proves
   DEPLOYMENT_DISABLED 402 stops heartbeats (audit :115-118,
   platform-link.ts:131-137, 189-196) and gstd_earned is a D1 display counter
   (audit :17-19) - an A1 fail could be the switch firing, an A1 pass could be
   counter theater. The lens named the scaler confound only. Move: aggregator
   rows carry heartbeat status / 402 events next to the payout delta so
   failures are classed kill-switch vs settlement vs scaler (+15 min).

3. A2's dead-salmon guard is single-arm AND mis-attributed. WebFetch of
   arxiv.org/abs/2512.18792 this sitting: the abstract's artifact is RANDOM
   INITIALIZATION ("plausible-looking explanations for randomly initialized
   neural networks"); no label-shuffle sentence appears in the abstract. The
   estate's own dead_salmon_airllm_drop_20261010/CARD.md:21-24 mandates the
   negative-control arm class ("random-weights model, label-shuffled run") for
   probe lanes. The perimeter CARD.md:19-20 carries only the shuffle arm and
   attributes it to the paper. For a consensus harness the paper-native
   control is a degenerate-voter arm (a garbage model voting with the fleet),
   which is also the structural form of finding 1's planted-wrong-majority
   falsifier: correlated models sharing a wrong prior can beat a shuffle
   baseline (CID row 350 predicts exactly this). Move: add the degenerate-voter
   arm to A2 and re-attribute the shuffle to the estate falsifier law, not the
   paper's abstract (10 min spec edit). OWED: paper-body check for a shuffle
   test beyond the abstract.

4. Ordering constraint the lens's per-finding moves miss: CARD.md:80 says the
   harness "Feeds the GPS capability ledger as consensus-contrib rows" - i.e.,
   the perimeter's self-learning loop terminates in the exact organ findings
   2-3 prove uninstrumented (no grader class, no floor, no evidence filter;
   verified by PRAGMA this sitting). A consensus-contrib row written today
   would be indistinguishable from a single self-attested verdict, and the
   router would bank agreement-as-competence - the CID disease at the ledger
   layer. Move: land the finding-2+3 schema fix BEFORE Phase 1's first harness
   write, not after (re-ordering, 0 extra minutes).

5. Phase 3's burst is unpriced against the measured rate bucket. The GB pitch
   card carries the measured receipt: single docker-bridge IP bucket, 6/11
   requests 429 at ~16/min self-rate vs 120/min nominal, sustained ~1 request
   per 10-15 s (gstd_gb_pitch_20261010/CARD.md:19-20). Phase 3 = 20 instances
   x 50 containers (CARD.md:47-48): every consensus sweep is request-parallel,
   so 50 nodes per IP cap the sweep at the pipe. The CARD knows the law
   (RATE-BUCKET LAW :40-43, Arm 2 single-IP :56-58) but never prices Phase 3
   against it. Move: either scale instances to nodes (sweep width per IP
   budgeted from the measured bucket) or make the GB-side IP whitelist a Phase
   3 entry condition in the CARD (15 min spec edit).

## Lens blind spots: 4 of 5 closed this sitting

- Tact contract cites: CLOSED (re-read from reference/gstdcoin/contracts).
- Test suites + mcp_parity: CLOSED (65 tests passed in 11.09s;
  `.venv/Scripts/python.exe tools/mcp_parity.py` -> MCP-PARITY PASS ok=3
  diverge=0, stdio 7/7, http 42/42, docker 17/17, image digest match, exit 0).
- One-moment ledger counts: CLOSED (re-run at a second moment, identical
  707/494/34).
- arXiv 2512.05117 and 2512.18792 abstracts: CLOSED via WebFetch (qualifier
  present in the former; no label-shuffle sentence in the latter's abstract).
- Still open: vast.ai pricing re-hit (ESTIMATE-CLASS stands), GSTD platform
  same-day re-verification before anything is sent GB (the pitch card's own
  falsifier), Tact-side gas/mint integration (CARD marks UNOBSERVABLE until GB
  confirms), 2512.18792 paper body beyond the abstract.

## Instruments (exact commands)

- sqlite: `.venv/Scripts/python.exe -c` with sqlite3 against
  tools/gps_mcp/gps_ledger.db3 (PRAGMA table_info; capability, verdict_log
  counts; per-row resolved counts; gstd-node-live rows; hash-presence reading).
- grep: `grep -rn "consensus_gate" --include="*.py" mag tools tests`;
  `grep -n "CREATE TABLE|grader" tools/gps_mcp/ledger.py`;
  `grep -c "LAW-CONS-ILLU-001" memory/law/registry.json` (0);
  scoped LAW-CONS-ILLU-001 locate (ox_artifact.jsonl, consensus_gate.py,
  corpus archives).
- pytest: 6 files, 65 passed in 11.09s.
- parity: tools/mcp_parity.py exit 0, 3 surfaces OK, image match.
- WebFetch: arxiv.org/abs/2512.05117, arxiv.org/abs/2512.18792 (abstracts).
