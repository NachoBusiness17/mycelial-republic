# BOT3 — mag/* organ steal map for the KV OS kernel

Lane: mag/*.py organs that are secretly KV-OS building blocks. Read-only survey, 2026-09-10.
954 files in mag/*.py; ~30 touch SESSIONS / CACHE / MEMORY / TOKENS / ROUTING / TELEMETRY.
Import tests run on the 5 most important: kvos_block, refeed_guard, burn_steer, topic_index, verkle_knot — **all 5 import OK, zero BROKEN found.**

## THE POINT

The mag/ directory already contains every layer of a KV operating system, scattered across standalone organs: content-hash addressing (kvos_block, verkle_knot, agent_state), tiered paging (memory_consolidate, topic_index, the warmed/cold probes), scheduling (fuel_feed, lane_cadence, swarm_worker), policy (cache_router, burn_gate, percolator, canon_seal), and metering (refeed_guard, burn_steer, tesuji_map). None were built as an OS — each was built to answer one measured question — so their schemas are one-off and unlinked. The KV OS build is therefore mostly a wiring job: adopt kvos_block's hash-chain block as the universal page format and let the dormant-but-sound cache_router and memory_consolidate drop in as the policy and paging layers over it.

## THE MAP

Kernel functions: ADDRESSING (content-hash blocks) · PAGING (hot/warm/cold tiers) · SCHEDULING (who runs when, prefix adjacency) · POLICY (admit/evict/pin/derive) · METERING (tokens, hits, quota).

| organ (mtime) | role in the OS | kernel function | state | the one function to steal |
|---|---|---|---|---|
| kvos_block.py (09-10) | content-addressed prefix blocks; every corpus file = hash chain of 400-word pages; measures corpus-wide prefix duplication | ADDRESSING | ALIVE | `chain_file()` + the kvos_blocks.v1 manifest (dup_pct = the OS's founding number) |
| burn_steer.py (09-10) | reads telemetry, renders the burn board (stdout + burn_board.html, bitmap-font PNG renderer already present) | METERING (render) | ALIVE | the board render pass — turn it into the kernel's page-pressure dashboard |
| percolator.py (09-09) | raw signal → noise stripped → repeatables compiled to invariants | POLICY (derive) | ALIVE | `percolate()` — derive new pages from repeated blocks |
| grounding_wave.py (09-08) | hash-chained append-only claim ledger, tri-state verdicts | ADDRESSING (log) | ALIVE | the append+verify chain row format |
| worldline_seed.py (09-07) | portable manifest of a closing session: genome+invariants+organs+record, sha-verified | ADDRESSING (snapshot) | ALIVE | the 5-slab seed verify — a session's swap-out image |
| burn_gate.py (09-07) | promo-hours + quota-floor gate on dispatch; judgment never gated | POLICY (admit) | ALIVE | `check()` exit-code gate — the kernel's admission control |
| cache_identity.py (09-07) | measured ollama longest-common-prefix KV reuse: warm-ident re-lights, 1-byte drift collapses | PAGING (probe) | ALIVE | the COLD/WARM-IDENT/DRIFT arm harness — page-fault semantics, measured |
| warmed_cold_replay.py (09-07) | warmed vs cold logprob replay through host ollama; perplexity per arm | PAGING (probe) | ALIVE | warmed-vs-cold perplexity delta — the prefetch payoff meter |
| knot_at_close.py (09-07) | bridges ended CLI-db sessions into the verkle chain (report + backup-first backfill) | SCHEDULING (teardown) | ALIVE | the backfill dossier builder — session close = page writeback |
| overseer.py (09-07) | stateless one-pass habitat snapshot to dashboard/static/overseer.json | TELEMETRY | ALIVE | the LOOK pass — kernel /proc |
| cite_gate.py (09-07) | deterministic citation classify/demote before rightsizing | POLICY (verify) | ALIVE | LOCAL-VERIFIED premise-span check — page trust bit |
| tesuji_map.py (09-07) | hash-chained probe ledger: tokens, ms, verdict per cell | METERING | ALIVE | the row schema — per-probe token/ms counters |
| fuel_feed.py (09-05) | real work sources → free lanes, entropy-routed, fairness rotation, honest down-reporting | SCHEDULING | ALIVE | `sources()`+entropy routing — the kernel run queue |
| topic_index.py (09-05) | 1,040 cards / 23 buckets keyword catalog over a time-and-seat-organized corpus | PAGING (index) | ALIVE | query/recall mode — the page table lookup |
| canon_seal.py (09-05) | sha256 manifest seal over canon; verify compares, never deletes | POLICY (pin) | ALIVE | `seal()/verify()` — pin + integrity bit for cold tier |
| refeed_guard.py (09-05) | measures the refeed tax: 94% of input is re-fed reads; char proxy + tok_* cross-check | METERING | ALIVE (tested OK) | the per-session input/output char split — the working-set-size meter |
| swarm_worker.py (09-05) | stateless headless swarm binary, namespaced queue | SCHEDULING (exec) | ALIVE | the queue-drain loop — kernel worker threads |
| mcp_http.py (09-04) | MCP streamable-HTTP over TOOL_MAP, loopback + X-API-Key, one sense one instance | SCHEDULING (syscall seam) | ALIVE | the TOOL_MAP→HTTP adapter — the kernel call gate |
| seat_dispatch.py (09-03) | task ANY body through ONE interface | SCHEDULING | ALIVE | `route(intent)` over the BODIES registry |
| verkle_knot.py (09-01) | content-addressed chain leaves, Merkle-Verkle hybrid tip, single-writer lock | ADDRESSING (chain) | ALIVE (in weekly use) | `append_verkle_knot()` under its lock — the journal |
| agent_state.py (09-01) | versioned agent-state packs: content_commit + parent + merkle tip; recall edge, never a second DNA | ADDRESSING (versioned pages) | DORMANT (sound) | the version-leaf commit — COW page semantics |
| ask_router.py (08-31) | outcome-ledger-driven lane ranking; control plane, no model calls | SCHEDULING | DORMANT (sound) | `route()` from ledger rows — LRU by observed outcome |
| lanes.py (08-30) | resource lanes + usage log | METERING | DORMANT (sound) | the usage-log append — per-lane token counters |
| ghost_memlance.py (08-30) | memory-state selector: ghost reasons, disk verifies; never memory-of-memory | PAGING (fault handler) | DORMANT (sound) | the select+verify-against-bytes step — page fault → verified read |
| lane_cadence.py (08-28) | learned lane rhythm: retry_after backoff, fall-through order | SCHEDULING (policy) | DORMANT (sound) | `retry_after(lane)` — the scheduler's backoff clock |
| max_distill_arms.py (08-27) | frozen-trace recorder + skill admission validator | METERING (trace) | DORMANT (sound) | the frozen-trace recorder — trajectory pages |
| memory_consolidate.py (08-18) | MemGPT-style consolidation: importance/recency/dedupe, recursive summary folded on token pressure | PAGING (tiering) | DORMANT (sound) | the token-pressure fold trigger — this IS hot→warm→cold eviction |
| cache_router.py (08-16) | prefix STABLE+append → cache-hit lane; VOLATILE tail → free tier; audit + simulate on real logs ("the 50x shrink") | POLICY (route) + METERING | DORMANT (sound) | the per-turn stable/volatile route decision — the kernel's page-placement policy |
| agent_knot.py (08-12) | agent as standing verkle invariant; knot-if-changed dedupe; standing pointer = address | ADDRESSING (identity page) | DORMANT (sound) | `stand()` dedupe — pinning the kernel's own page |
| knot_untangle.py (08-11) | near-duplicate cluster detection + re-synthesis into one invariant | POLICY (dedupe/evict) | DORMANT (sound) | token-overlap clustering — garbage collection |
| self_drive.py (08-09) | pick model, redo prompt, assemble cached context, inject principles, spawn | SCHEDULING (compose) | DORMANT (sound) | cached-context assembly — prefix-adjacent page batching |
| agent_state_router.py (08-09) | custom agent state drives resource auto-selection | SCHEDULING | DORMANT (sound) | state→resource resolver |
| memory_map.py (08-08) | entity→opaque-token at rest, decode at operator surface, verkle-anchored | POLICY (ACL) | DORMANT (sound) | `encode/surface` — the kernel's protection rings |
| memory_events.py (08-07) | append-only JSONL event stream for state recovery without transcript replay | METERING (events) | DORMANT (sound) | the event row — kernel event log |

## Single most valuable stolen organ

**mag/cache_router.py** — dormant since 08-16 but sound, and it is the only organ that already implements a complete KV-OS *policy* layer against measured economics: it reads a byte-stable prefix check (invariant.py), real hit/miss token rates (cache_map.py MODEL_RATES over provider_usage.jsonl), routes the stable+append case to cache-hit lanes and the volatile tail to free lanes, and ships both `audit()` (what the 50x miss tax actually cost) and `simulate()` (replay the log under the router). Hand it kvos_block.py's content-hash pages as its prefix-stability signal and the kernel gets its page-placement policy, its metering cross-check, and its proof harness in one file.

Runners-up: memory_consolidate.py is the ready-made hot/warm/cold pager (token-pressure fold = eviction); kvos_block.py is the addressing layer and the founding measurement (dup_pct of the corpus).
