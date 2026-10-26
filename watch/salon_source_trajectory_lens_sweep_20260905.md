# SOURCE DIGEST — THE TRAJECTORY LENS: everything built, one sweep (Sep 5, 2026)

Operator order: "self steal this is not the first time i asked you to look into this. how do we
make sure this is now understood and how can you now look through literally everything we have
built through this lens? full Salon."

## THE LENS (definition of record)
Every interaction is an ENVELOPE: {input, tool_result, output, reasoning, step_hash, timing,
envelope_layers}. z.ai's Trajectory window renders exactly this (preserved sample:
corpus/training_materials/zai_trajectory_window_sample_20260905.txt, sha256 efd424dd...).
Through the lens, every built thing is one of:
- PRODUCER — generates envelope rows (seats, salons, runners, automations)
- RECORD — stores/transmits them (chain, db, CONVO, bank)
- COMPILER — turns trails into portable artifacts (ribs, training chains)
- DARK — captures or renders WITHOUT envelope structure (dashboards, excerpts, state views)

## THE RECEIPTED LINEAGE (why the operator says "not the first time" — 4 drops proven)
| date | ask/receipt | artifact | what got dropped |
|---|---|---|---|
| 08-27 | "transmit trajectory as RIB, dumb agent codes it" | RIB_TRAJECTORY_20260827_DRAIN_HARDENING.md — the thesis dogfood RAN (pennies, cross-seat) | not repeated; pattern not institutionalized |
| 08-28 | compiler spec | docs/ref/TRAJECTORY_RIB_COMPILER_SPEC.md — fused from 3 witnesses; [ONLY-US] edge proven (nobody packages trajectories as portable artifacts w/ acceptance commands) | SPEC NEVER BUILT to the gated build order |
| 08-28 | architecture | docs/ref/TRAJECTORY_ARCHITECTURE.md — full council: committer first, tape=untrusted sidecar, stream remembers, compile=only legal bridge | architecture shelved |
| 09-05 03-04Z | operator FOUND the trajectory viewer | thought_bank_app.py → 9,305 reasoning parts banked as BLOBS | blobs, not chains; envelope schema ignored |
| 09-05 morning | operator hand-carries the export | trajectory_rib salon 7/7; T1 schema + T2 extractor on board | — (current arc) |
ROOT CAUSE of the drops — OPERATOR REFRAME (09-05, binding): "duplication is emphasis — we built
this shit dozens of times." The recurrence is NOT shame and NOT fragmentation-to-be-mourned: the
doctrine kept resurfacing because it is load-bearing, and each arc built one real facet (spec,
architecture, bank, schema). Read the table as FOUR EMPHASIS WAVES of one program, each leaving
reusable bones. The program is now NAMED; the sweep CONTINUES it. DO NOT RE-INVENT: cite the
existing bones, name the reinterpretation, build the delta.

## OPERATOR MANDATES FOR THIS SALON (09-05, binding)
1. DUPLICATION IS EMPHASIS — every prior artifact is emphasis-wave material; fuse, don't restart.
2. HUGE NUANCE — triage is MULTI-LABEL: one build can be RECORD+COMPILER (chain+seal), PRODUCER+RECORD
   (salon_runner keeps its own posts), DARK-in-part (live_feed: envelope excerpts, no chains). No
   blunt stamping; name the facet that is dark, not the whole thing. Hold the Aug-28 council's
   distinctions: tape=untrusted sidecar vs stream=committed record vs compile=only legal bridge.
3. SACRED COWS, NOT LEGACY SHIT — TRAJECTORY_RIB_COMPILER_SPEC, TRAJECTORY_ARCHITECTURE,
   RIB_TRAJECTORY_20260827, the bank, Hermes' trajectory_compressor steal: each is a draft of the
   same brain. STEAL THE BONES, NAME THE REINTERPRETATION, RETIRE THE DRAFT. Never frame fleet
   history as garbage.
4. MOONSHOT FRONTIER — swing for the complete design: the [ONLY-US] edge (no surveyed product
   packages trajectories as portable artifacts with acceptance commands as first-class data —
   proven 08-28 vs papers/PRMs/trace-vendors) means the fleet can become the FIRST
   trajectory-native company: every interaction portable, replayable, verifiable, trainable.
   Design that company's spine, not a patch list. Sep 20 proof candidate.

## THE INVENTORY (triage every item through the lens)
RECORDS: verkle chain (7,243 knots, OTS-sealed nightly) · session db (184+ sessions, typed
part-stream: text/reasoning/tool, session_id+message_id+sequence) · thought-bank 9,305 parts /
17.3M chars · CONVO.md · room.jsonl · memory/seals · corpus MANIFEST · law lattice (58) ·
DISPOSITIONS.json · falsifier_counter ledger · steer_log.jsonl · usage sweeps.
PRODUCERS: every ZCode seat + subagents · salon_runner v4 (7 shapes+fold) · salon_phone
(android) · swarm_worker · night shift a5e12eea · monitor lane · decks_nightly · art_forge ·
GA (73 genes) · arena-bench · pdf_triage.
COMPILERS (partial or shelved): RIB_TRAJECTORY_20260827 (ran once) · TRAJECTORY_RIB_COMPILER_SPEC
(written, unbuilt) · TRAJECTORY_ARCHITECTURE (argued, shelved) · thought_bank_app (blobs) ·
seal/OTS (anchors whole files, not steps) · corpus_distiller B4 (chartered, unbuilt) ·
T1 TrajectoryStep + rejoiner (boarded, unbuilt) · T2 UniversalExtractor (boarded, unbuilt).
DARK: dashboards (35+ surfaces render STATE, never envelopes) · live_feed (excerpts, not chains) ·
burn_steer (telemetry) · lane logs · hunger ledger (counts, not envelopes) · intake cards (verdicts,
not chains).

## KNOWN ECONOMICS + LAWS the lens must respect
- 240:1 refeed tax measured (122.4M in → 0.5M out, free plan, 09-05) — envelopes are overhead;
  FROZEN_RIB lesson: ~100 tokens per envelope before the answer. Measured envelopes only.
- The burn is training data (doctrine 09-05): every trail harvests to QLoRA; blobs → chains is
  the upgrade this lens exists to force.
- Aug-28 council LAW still standing: "players write intent, governor writes state, surfaces give
  sight, the stream remembers, the covenant decides, fun ships it." The lens is the stream's
  schema. Tape=untrusted sidecar; committer first; compile=only legal bridge.
- Multiple seats, limited per-seat daily quotas — extraction must be $0-local-first (db door),
  surface door only where the local stream is dark.
- Sep 20 proof deadline: receipts/day scaling. The spine should MAKE receipts, not cost them.

## THE SALON QUESTION
Triage EVERYTHING built through the lens (every item above gets PRODUCER/RECORD/COMPILER/DARK +
its one biggest envelope gap). Then converge the unification: ONE trajectory spine that (a)
adopts the TrajectoryStep schema (with schema_version — drift killer), (b) absorbs the shelved
TRAJECTORY_RIB_COMPILER_SPEC + TRAJECTORY_ARCHITECTURE instead of re-inventing them (cite them,
name the deltas), (c) upgrades the thought-bank blobs to chains via the T1 rejoiner, (d) turns
the DARK surfaces into envelope-aware ones where it is $0-local, (e) feeds the B4 distiller and
the Sep-20 receipts/day proof. Rank the build order by impact/effort with a named falsifier per
build. HARD RULE: code-first — schemas, SQL, adapter interfaces, ≤40 lines inline or exact
file-level specs. Prose per artifact ≤3 sentences. Disagreements are the product.
