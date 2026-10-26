# THE RIDDLER ARCHIVE SPEC — unifying the dumps (2026-09-08)

The Operator's dumps, unified: the S-001 control-surface audit (+ peer review with the
four inequalities), the RenderMan-LLM compaction analogy (RIB = RenderMan Interface
Bytestream — the RIB pun resolved: the game driver was NAMED for an archival format),
the Diamond Age/Mesh topology (portals, ractor market, HumanDramaticPerformance
capabilities), and the riddler trajectory organ (shipped: mag/riddler_trajectory.py,
94 steps redacted-by-reference).

## The unified architecture: the riddler feed IS a DelayedReadArchive

RenderMan solved "a linear stream of construction commands too large to keep
expanded" by archiving assets and leaving stand-ins in the driver. The riddler
trajectory applies the identical pattern to session history:

| RenderMan | The riddler feed | The private chain |
|---|---|---|
| Full geometry (too big to inline) | full session content (secrets, substance) | **the archive** — decodes the refs |
| DelayedReadArchive stand-in | the redacted step (shape + refs) | expansion = capability-gated |
| The bound ("does this cover what's needed?") | the refs (paths, hashes, salons — machine-generated) | over-keep the pointer, not the content |
| ObjectBegin/Instance | matching refs across sessions → shared KV blocks | token-enhancement by design |
| The scope-stack grammar (never split an open block) | the four inequalities (never split an ActionReceipt from its postcondition evidence) | **the same grammar rule in both domains** |

## The S-001 inequalities become the feed's type discipline

The four inequalities are the riddler feed's constitutional constraints:
1. CapabilityRequest ≠ Capability — the feed RECORDS requests; it does not grant.
2. ActionReceipt ≠ PostconditionEvidence — the feed proves the move happened; the
   private chain holds the proof it worked.
3. PostconditionEvidence ≠ IntentionSatisfied — the refs decode what was done; the
   WHY stays with the seat.
4. ExperienceCandidate ≠ CompiledSkill — the feed is an ExperienceCandidate; the
   compiled skill (if any) lives in the private chain.
Plus the fifth rule the dumps added: **SEMANTIC PROMOTION REQUIRES EXPLICIT
PROVENANCE** — the feed's refs ARE the provenance; without them, it's a rumor.

## The Mesh topology (the old doc's P2P D&D, now wired)

- Each node hosts a portal (human) + a small AI player + publishes ITS riddler feed.
- The shared world = the verkle ledger (the old doc already chose the save file).
- The frontier DM = game_dm_llm's seam (the archaeology already started it).
- The riddler feeds are the node-to-node REFERENCE LAYER: node B can reference
  node A's work by feed-ref without gaining access to A's substance. The 4chan-board
  freedom (cross-conversation reference without dropping a beat) at Mesh scale,
  theft-proof by architecture: the refs decode only against the holding node's chain.
- The token enhancement: matching refs across nodes = shared KV blocks at the model
  layer — the flash cache maps by reference, per the compaction doc's
  ObjectBegin/Instance row.

## The S-001 mappings the old doc already drew (confirmed by the audit's own tables)

The Diamond Age functions → fleet organs: Hackworth (builder) = mag core +
PolicyRegistry · Miranda (ractor) = HumanDramaticPerformance Capability · Judge Fang
(institutional judgment) = escalation gates + Decision receipts · Nell (sovereign
learner) = the player with graduated capabilities · Primer = the router +
ExperienceCandidate promotion · the Ractor Network = the capability market.
The five Diamond Age functions are typed, not metaphorical.

## The graduated participation ladder (the old doc's, adopted)

WATCHER → VOTER → EXTRA → NPC RACTOR → FEATURED RACTOR → DM/DIRECTOR → WORLD BUILDER.
Each step = an explicit Capability issuance on evidence (session logs, audience
review). ExperienceCandidate ≠ CompiledSkill, applied to humans: you don't become a
DM by asking; you become one because a Director reviewed your performance evidence.

## The build order (the open seam, sequenced)

1. read_archive(span) — the dereference organ: capability-gated expansion from the
   private chain (the DelayedReadArchive loader).
2. The auto-surface frustum: when a live turn mentions a path/entity whose bound
   intersects an archived span, surface the pointer (metadata frustum culling).
3. The scope-stack: compaction ILLEGAL inside open tool-call pairs (the grammar
   rule, enforced mechanically).
4. The append-only summary spine: each compaction appends a segment to the stable
   spine — cached tokens survive; regeneration is a per-compaction cost decision.
5. The adversarial validation: query the summary with questions whose answers live
   only in the archived prefix; failures regenerate at higher fidelity (test-render
   before committing the farm).
