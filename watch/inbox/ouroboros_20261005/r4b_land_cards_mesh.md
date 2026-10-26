# R4B LAND: CARDS MOUNTED + THE NINE-MEMORY TABLE (ouroboros R4 moves 6 and 7)

Seat: R4b-LC lane. Moment: 2026-10-06T09:2x-09:5xZ (2026-10-05 ET). Ask: execute moves
6+7 of watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md (the RESUMED
run's fold, findings S6 + S7). Laws held: .venv\Scripts\python.exe only; no git commit
(the coordinator commits); no em/en dashes in added lines (grep over this diff's added
lines: zero hits).

## MOVE 6: BEHAVIOR CARDS, disposition MOUNT (consumer-or-strike)

The rib memory/rib/RIB_BEHAVIOR_CARDS_20260928.md promised "the seat warms it at boot"
with zero boot consumers (S6: only the miner tools/behavior_cards_x.py). Judgment by
boot-time cost: the deck is small enough to mount and the R4 synthesis itself warned the
rib "would deserve the strike if left unmounted after this round", so the claim was made
true rather than struck. A head-only VAULT_RIBS mount would have cut off mid first card
(LAW_HEAD_CHARS=1200 vs the deck's card bodies), so the mount rides head PLUS a dated
CARD INDEX amendment (the right-size slice per the ask):

1. memory/rib/RIB_BEHAVIOR_CARDS_20260928.md: AMENDMENT (2026-10-05, R4b ouroboros move
   6) appended, amend-never-rewrite. Carries: the disposition record (promise without a
   performer, now mounted), the CARD INDEX (all nine card names in file order: LINK-DROP,
   GO, CORRECTION, TERSE-EVAL, X-DROP @name, STEAL-ORDER, FUNDING-STATEMENT,
   RESOURCE-ORDER, GENESIS-TESTIMONY, plus the standing-lanes triage), and an explicit
   demotion LACK (no card has ever been retired; SUPERSEDED.md takes conclusions, not
   cards). File grew 3631 B to 4906 B.
2. mag/rib_boot.py: VAULT_RIBS gains the deck as a sixth entry with a dated receipt
   comment naming the cause (consumer-or-strike) and the slice rationale (index
   amendment, not the mid-card cut). The printout count stays live via len(VAULT_RIBS).
3. tests/test_rib_boot_amendments.py: the driver test asserted == 5; now asserts
   == len(VAULT_RIBS) with the cause in a comment (census-denominator law: a hard-coded
   count is a constant that rots on every deliberate mount change; the test pins the
   mechanism, every named rib mounts).
4. rib_boot.json regenerated (ts 2026-10-06T09:24:14Z): vault_law_ribs_mounted 6/6,
   vault_amendments_mounted 5 (4 prior + the deck index), deck law_head 2471 chars
   carrying "CARD INDEX at mount moment" and "Demotion: LACK" (byte-verified via a JSON
   read of the artifact). Consumers now real end to end: rib_boot.json feeds
   mag/context_pack.py's vault block, which renders amendment bodies into packs (R4-L2
   wiring, test_context_pack_consumes_the_vault_block rides the suite).

SIZE DELTA, banked honestly: controlled A/B mount at one moment, same instrument
(mount_vault(), json.dumps indent=1): vault block 23302 B with the deck vs 19370 B
without = the deck contributes 3932 B. Whole-file context: rib_boot.json read 38278 B
at this seat's first census (2026-10-05 22:42 mtime), a sibling regen had already moved
it to 42230 B before my regen (shared hot tree; attribution: not this seat), and the
post-regen artifact holds 42230 B with the deck riding. The clean attributable number
is the 3932 B A/B delta, not the whole-file drift.

## MOVE 7: THE NINE-MEMORY TABLE (estate side)

docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md, new section "The nine memories, ESTATE SIDE (R4b
mapping, 2026-10-05)", placed between the seed-engine mapping and the distribution
layer. For each of the spec's nine memory types (docs/ref/
MCP_EPISTEMIC_MESH_SPEC.md section 2 table): the estate organ that IS it, its freshness
instrument, and its demotion path or explicit LACK:

- Evidence: watch/inbox/ + corpus/papers + corpus/library; landing habit + mag.shared
  surface validate; LACK by position (demotion lives in a SUPERSEDED row citing the
  receipt).
- Artifact: mag/ + tools/ indexed by memory/capability_manifest.md + memory/
  tool_manifest.json; capability_manifest.py regen crank + pre-push ratchet/gates; LACK.
- Concept: corpus/canon/ + memory/knowledge_graph.json; graph rebuilds + MagFtsIndex
  Daily; PRESENT for canon (corpus/canon/_retired/, superseded-not-deleted with its
  README naming cause), LACK in the graph (fold() supersession gap, R4 synthesis S5).
- Procedural: .agents/skills/ + memory/skills/ + memory/improve/skill_ledger.jsonl;
  skill_fired.v1 rows per pack injection + MagImproveDaily; LACK.
- Failure: memory/training/loop_gaps.jsonl + memory/failure_kb/signatures.json +
  memory/falsifier/close_rate.jsonl; live writers + ouroboros falsifier fires; PARTIAL
  (falsifier.close.v1 closed rows exist; loop gaps dedupe with no closure stamp).
- Decision: memory/rib/; rib_boot regen chain + amendment mounts; PRESENT, strongest
  (POST-DATUM sections + SUPERSEDED.md pointed at every boot).
- Provenance: verkle chain (memory/biography/verkle_tip.json + memory/verkle/ +
  mag/seed_seal.py); hermes warm boot + tip age-debt bar; BY LAW append-only, retraction
  rides SUPERSEDED, never a chain rewrite.
- Agent: RIB_BEHAVIOR_CARDS deck + memory/zknot/LATEST.md; the miner + zknot logon
  regen + tonight's rib_boot mount; LACK.
- Capability: starter-kit/ARMORY.md + capability manifest; reader-coupled crank
  (tool_manifest.json the stale sibling); LACK (the decaying-manifest proposal would
  supply decay).

Score line landed: PRESENT two, append-only-by-design one, PARTIAL one, LACK five;
consequence: the mesh mounts these organs, it must not mint a second memory stack.

STAMP FIX (same file): RULINGS item 2 read "ouroboros R3 (dwfrun-e2567adf, RUNNING
RIGHT NOW)". Corrected: R3 completed, synthesis banked at watch/inbox/ractor_engine/
2026-10-05-ouroboros-r3-trust/SYNTHESIS.md, executor receipts through
watch/inbox/ouroboros_20261005/r3_land_consensus_seal.md (header stamps Moment:
2026-10-05T23:19Z, its own bytes), R4 folded after (fold moment 2026-10-06 per the R4
synthesis header). The correction names itself: a stale line in the doc that audits
staleness.

## GATES

- pytest tests/test_rib_boot_amendments.py -q: 9 passed in 4.52s.
- citation_lint check --files docs/ref/MCP_EPISTEMIC_MESH_AUDIT.md: CITATION-LINT: ok,
  blocking=0, warns=0, exit 0.
- violation_ratchet check --changed: 5 changed files, hits=3, registered=2, NEW=1. The
  NEW hit (tools/thought_quantizer.py file-too-long) is a sibling lane's in-flight
  file this seat never opened (the R4 synthesis row 1 quantizer ask, another lane's
  move). Zero NEW attributable to this lane's diff (mag/rib_boot.py, the test file,
  the rib, the audit doc).
- Em/en dash law: grep over this diff's added lines, zero hits.

## BLOCKERS / OWED

None blocking these two moves. Owed, named in the table as facts rather than cured
here: the reader-coupled regen crank (no clock leg, synthesis row 2, another lane's
ask), tool_manifest.json staleness, the knowledge-graph supersession stamp (row 3).
The knowledge graph itself was rebuilt by a sibling at 2026-10-06T09:20:14Z mid-session
(not this seat).
