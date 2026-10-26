# THE BUILD QUEUE: what remains to build from the olm mines (2026-10-11)

The mines have produced ~20 steal cards across 13 days. What follows is the
consolidated PORT QUEUE - mechanisms the cards mapped onto named estate organs
with line anchors, but which are not yet BUILT. Each entry names: the organ,
the move, the source card, and the size class. This file IS the next fill-ball
/ execute-burn lane table.

## TIER 1 - one-sitting ports (organ exists, mechanism mapped, lines cited)

1. KV env contract on the janitor fleet (kv-cache): set OLLAMA_FLASH_ATTENTION=1
   + OLLAMA_KV_CACHE_TYPE=q8_0 on every fleet host; accept gate = trust-bytes
   (OLLAMA_DEBUG=1 log must NAME the loaded cache type; ollama ps Processor
   column <100% = RAM spill). Repo grep today: 0 hits for the env vars. ~30 min.
2. Heal-log drain in knowledge graph build() (agent-memory): mag/knowledge_graph.py
   build() gains a final step draining tools/graph_heal.py's heal_log.jsonl,
   re-applying authored why_context edges idempotent by edge id, dead-lettering
   dangling. Closes the 117-edges-to-zero wipe class, live-proven open. ~1 sitting.
3. NO-SINGLE-JUDGE-WASTE-GATE invariant (kv-cache judge study): second-judge arm
   + reported agreement score required before any waste metric gates fleet
   behavior; lands in memory/percolator/invariants.json + a v2 marker_penalty
   profile (3-family, OFF by default). ~1 sitting.
4. Schema-placement law in the context pack freeze (kv-cache): only
   session-stable schemas enter the frozen block (a mid-session schema change
   forces full-prefix refreeze, mag/context_pack.py:960-984); dynamic schemas
   render in the evolving tail as plain-text contracts + backend validation
   (99.9% malformed-resolution at ~0.9% overhead, Slow Vale measured). ~1 sitting.
5. Cap-above-draw-range invariant (inference): percolator mint - caps must sit
   above the family's measured draw range (glm-5.3-flash empties at ANY cap,
   rib census); preventive recovery upstream of the terminal-marker check. ~1 sitting.
6. Cloud-suffix REFUSE in ollama_policy verify_pins (open-local): refuse models
   whose tag carries a cloud suffix (a local address is not locality);
   OLLAMA_NO_CLOUD pinned on the janitor host; live 15-model baseline already
   clean. ~1 sitting.
7. Registry presence (mcp-landscape): file the estate seed + GPS router into
   Smithery/PulseMCP listing formats - the discovery surface we are absent from
   (19,444 listings). ~1 sitting + operator naming call.

## TIER 2 - one-wave (multi-file, instrument + probe pairs)

8. Merge-fidelity probe in lora_pipeline (finetuning VERIFY leg): pre-trust check
   + base-vs-adapter eval on a frozen quiz (McNemar template); the bf16
   merge-erasure class (17-37% of deltas) must be caught before any adapter
   promotes. Blocked on: an actual adapter to protect (no LoRA run yet).
9. Family-stamped witness rows + family-calibrated consensus (Personas):
   stamp base-model family on every consensus witness; same-family agreement
   counts as ONE witness class under the roshamon independence rule. ~half wave.
10. rr_tail eviction race (kv-cache RR-Evict): round-robin 1,024-token
    tail-chunk eviction vs the LRU null arm at 1x/2x/4x pack budgets on
    tools/prefix_cache_sim.py + tools/lru_null_arm.py. ~half wave, $0.
11. Prefix-sticky janitor router (inference find 5): thin router hashing the
    frozen RIB prefix to the warm instance with overload spill; KV hits
    25% -> >80% measured in the field. ~1 wave, raceable on the same instruments.
12. Budget-matched test-time-scaling null arm (evals): routing must beat
    same-budget-more-inference on held-out asks or the routing law demotes to
    hypothesis. ~1 wave.
13. Semantic-entropy routing arm (finetuning): multi-sample cluster-by-meaning
    at the janitor tier; +22pp cross-family average claimed in the field.
    ~1 wave.
14. Percolator hard_moves() review (evals MemSkill): deterministic bucket review
    of non-ok ledger rows by (source, shape, outcome), each bucket closed with an
    evolution decision; ghost dialect registered or routed. ~1 wave.

## TIER 3 - gated (operator call, external dependency, or frontier cost)

15. MTP-head graft onto fleet GGUFs (inference find 4): 23 -> 37 tok/s claimed;
    gated on gemma-family head existence (OWED check) + a GGUF graft toolchain.
16. Dex-composition for desk models (open-local GSQ/RCO): per-tensor sensitivity
    + mmap-disk-embeddings config for athena-class (32.6 GB on this desk already
    disk-resident). Gated on desk VRAM upgrade or acceptance of disk-speed.
17. $2k used-3090 rig decision (open-local Sunk Cost): 57 t/s measured in the
    field; buy-axis priced against the 43-year breakeven - operator wallet call.
18. Voxel/flow-model few-step serve (physics feed, Data-Space Iteration): file
    under Voxelmancy's renderer shelf; gated on the renderer existing.

## THE LAW THE QUEUE TEACHES

Every tier-1 item is a CONFIG or a SMALL PATCH on an organ that already exists.
The mines have stopped producing "we should build X" and started producing
"X's last 50 lines are specced, here." The build debt is now smaller than the
port debt - and the port debt is queued.
