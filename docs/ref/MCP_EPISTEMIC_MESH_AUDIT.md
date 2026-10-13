# The Epistemic Mesh Audit + Build Proposals (operator-canon companion, 2026-10-05)

Companion to docs/ref/MCP_EPISTEMIC_MESH_SPEC.md. Three layers arrived in one
wave: the critical audit, the escalation framing with the Estate Seed engine
mapping, and the distribution-layer idea. Banked verbatim-in-substance; the
load-bearing rulings are at the bottom.

## The audit's structural findings (all three STAND)

1. THE CLOSED LOOP AT BIGGER SCALE: a mesh of agents built/curated/governed by
   one operator is still one lab. Epistemic openness requires a promotion the
   operator did not predict. (Maps to the estate's own operator-is-unmeasured
   Socratic finding.)
2. PROVENANCE IS NOT TRUTH / THE IDENTICAL-COGNITION CONFOUND: five agents on
   one base model "independently replicating" is prompt convergence wearing a
   mesh costume (the invariant-salon problem; the estate's own consensus-
   illusion law). Independent = different code paths, different data,
   different model families.
3. MIRROR-SCORER CIRCULARITY: mesh concepts scored by mesh instruments need a
   control ontology of equal size from unrelated material.

Plus the unnamed gap BOTH critical voices converged on: NO DEMOTION PATH. A
one-way promotion ladder accumulates once-true-now-false sediment; the mesh
needs decay functions + challenge counters or it cannot forget and therefore
cannot learn. And the query channel itself is the forgotten attack surface:
every search_evidence() response is untrusted input mid-reasoning; typed
schemas make injection easier to detect AND easier to aim. A reproducer node
that executes from a description is an RCE boundary.

## The buildable proposals (tri-stated)

- THE DECISIVE EXPERIMENT, k3s form: istio emptyDir/runAsNonRoot conflict as
  Problem 1, linkerd variant as held-out Problem 2; metrics TTFH, MCP calls to
  convergence, concept invocation rank <= 1; falsifier: > 3 calls to re-derive
  = ephemeral context caching, not memory evolution. UNPROVEN, n=0, runnable
  when a k3s failure domain exists.
- THE IMMUNE RACE: 50 subtly-poisoned failure reports; arm A one frontier
  monolith vs arm B three distinct 8Bs in verifier/skeptic/reproducer roles;
  false-positive rate at <= 2x compute. DISPUTED, n=1, THE CHEAPEST REAL
  PROBE - runnable on the estate's free lanes + fleet this week.
- THE DECAYING CAPABILITY MANIFEST: ed25519-signed node advertisement,
  re-signed every T hours, exponential trust decay to 0 for silent nodes.
  SUPPORTED - and the estate already ships ed25519 signing (mag/seed_seal.py,
  the PAM spec) so this is a port not a build.
- LOCAL CLAIM -> HYPOTHESIS_STAGING rename: free, kills anchoring bias at the
  vocabulary level. ADOPTED on banking.
- THE SIBIL SIMULATION as the foundational test: 100 fake nodes endorsing one
  false claim; the promotion protocol passes only if it refuses. Before any
  peer mesh.

## The escalation mapping (Estate Seed engines)

The nine memories -> existing seed engines (spine_walk, librarian_catalog,
estate_atlas, estate_smith_chart, cooker, task_wall, phone_relay,
MANIFEST.sha256, ledger) plus four new (epistemic_router, provenance_verifier,
ontology_compiler, immune_cell). Law 7 generalizes to one-authority-per-
epistemic-transition. NOTE: these engine names live in the seed repo, not this
repo - the mapping is for the pushable package, and its claims verify there,
not here.

## The nine memories, ESTATE SIDE (R4b mapping, 2026-10-05)

The escalation mapping above aimed the mesh spec's nine memory types
(spec section 2, docs/ref/MCP_EPISTEMIC_MESH_SPEC.md) at seed-repo
engines and named zero organs of THIS repo. This table is the local
half, landed by the ouroboros R4b lane: for each mesh memory type, the
estate organ that already IS it, the instrument that touches its
freshness, and its demotion path or an explicit LACK. The general
register memory/fold_history/SUPERSEDED.md is new (minted 2026-10-05);
most organs predate it with nothing of their own, and the table says so
honestly rather than papering it.

| Mesh memory | Estate organ (this repo) | Freshness instrument | Demotion path or LACK |
|---|---|---|---|
| Evidence (papers, experiments, measurements) | watch/inbox/ receipts + corpus/papers + corpus/library | receipt-landing habit + mag.shared_surface validate over the inbox contract; no clocked patrol owns the inbox itself | LACK by position: receipts are append-only records of what happened; demotion lives one layer up, in a SUPERSEDED.md row citing the receipt |
| Artifact (source code, packages, tools) | mag/ + tools/, indexed by memory/capability_manifest.md and memory/tool_manifest.json | capability manifest regen crank (tools/capability_manifest.py; the manifest header stamps its regen moment) + pre-push ratchet and gate suite | LACK: no retired-tools register; deletion rides git history alone |
| Concept (definitions, ontology, relationships) | corpus/canon/ + memory/knowledge_graph.json | knowledge graph rebuilds (artifact header stamps its moment) + the MagFtsIndexDaily corpus-index task | PRESENT for canon: corpus/canon/_retired/ (superseded, not deleted; its README names the retirement and its cause). LACK in the graph: fold() carries no supersession stamp (ouroboros R4 synthesis finding S5) |
| Procedural (how something was done) | .agents/skills/ + memory/skills/ + memory/improve/skill_ledger.jsonl | skill_ledger rows fire per pack injection (schema skill_fired.v1) + MagImproveDaily | LACK: skills append; no skill has ever been retired |
| Failure (failed experiments, bugs, rejected hypotheses) | memory/training/loop_gaps.jsonl + memory/failure_kb/signatures.json + memory/falsifier/close_rate.jsonl | live writers stamp rows on detection (loop-gap rows carry ts) + ouroboros rounds fire falsifiers over organs | PARTIAL: falsifier close rows carry a closed status (schema falsifier.close.v1); loop gaps dedupe but carry no closure stamp, so a cured gap never demotes (the LACK half) |
| Decision (why a design decision was made) | memory/rib/ (the rib vault) | rib_boot regen chain (mag.cmd context-pack fires zknot + hermes_warm_boot + rib_boot, exit on age per the AGENTS.md load-order rows) + POST-DATUM amendments mount at every boot | PRESENT, the estate's strongest: dated POST-DATUM/AMENDMENT sections + memory/fold_history/SUPERSEDED.md pointed at in every boot artifact |
| Provenance (hashes, authorship, timestamps, lineage) | the verkle chain: memory/biography/verkle_tip.json + memory/verkle/ + ed25519 seed seals (mag/seed_seal.py) | hermes warm boot at session start + the rib_boot tip age-debt bar (TIP_DEBT_MINUTES) | BY LAW append-only (the read-only ruling quoted in mag/rib_boot.py); retraction rides a SUPERSEDED.md row, never a chain rewrite |
| Agent (observations, learned local patterns) | memory/rib/RIB_BEHAVIOR_CARDS_20260928.md (the card deck) + memory/zknot/LATEST.md recap | the miner tools/behavior_cards_x.py digs cards; zknot regenerates LATEST.md at logon; as of tonight the deck rides the rib_boot vault mount (R4b, consumer-or-strike) | LACK: cards append as miners dig; no card has ever been retired (the deck's own amendment states it) |
| Capability (what tools/services exist) | starter-kit/ARMORY.md (the graduated index) + memory/capability_manifest.md | the regen crank is reader-coupled (no clock leg); memory/tool_manifest.json is the stale sibling its own header date betrays | LACK: the armory graduates upward only; the audit's decaying-manifest proposal would supply the decay function |

Score at mapping moment: demotion PRESENT for two organs (concept-canon,
decision-ribs), append-only BY DESIGN with register-beside retraction for
one (provenance), PARTIAL for one (failure), explicit LACK for five
(evidence, artifact, procedural, agent, capability). Consequence for the
build: the mesh must not mint a second memory stack beside these organs;
it mounts them, and the missing demotion paths are filed as mesh-build
work, not imported as gaps.

## The distribution layer (operator's torrent-rib idea)

Ribs torrent-streamed: the standing wave distributed as content-addressed
parts - rib files are sha256-named artifacts (torrent piece hashes for free),
the verkle chain is the manifest, peers seed from local caches, and people
contribute compute to the network: old devices become MORE resilience (seed
nodes), not less. This is the delivery mechanism for the mycelial-republic
seed AND the answer to the audit's closed-loop finding: distribution is the
easy half of openness; compute-sharing is the start of the hard half.

## RULINGS (this seat, per the audit's own priority order)

1. BUILD ORDER = the audit's: immune cells FIRST (the race on free lanes),
   then five-server arms A/B/C, then the decisive experiment with the
   contamination controls, peer mesh LAST. The router draft is second-order -
   requested and accepted, but it lands AFTER the immune race fires, because
   the audit is right that everything else is untestable until the immune
   hypothesis stands or dies.
2. The ouroboros R3 (dwfrun-e2567adf) is thematically this exact audit applied
   to the local trust instruments - convergence noted, and its fold landed
   before any of this builds: the R3 synthesis is banked at
   watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md, its
   executor receipts run through
   watch/inbox/ouroboros_20261005/r3_land_consensus_seal.md (header stamps
   Moment: 2026-10-05T23:19Z), and R4, the memory/boot round, folded after it
   (watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md,
   fold moment 2026-10-06 per its own header). STAMP CORRECTED 2026-10-05 by
   the R4b lane: this ruling had read "RUNNING RIGHT NOW" since banking, a
   stale line in the very doc that audits staleness.
3. The immune race is filed as a percolator candidate with its falsifier
   intact. The k3s decisive experiment is filed owed pending a failure
   domain. The manifest decay port is filed owed pending the seed repo.
