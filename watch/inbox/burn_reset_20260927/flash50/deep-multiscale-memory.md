# DEEP: The Unified Multiscale Memory Architecture

Item: deep-multiscale-memory, flash50 lane, 2026-09-28. Grounded in reads of the estate's own
memory modules plus two live checks run this pass. No em-dashes per law.

## 0. What was actually read and run

Read this pass (paths verified): `mag/context_pack.py` (full), `mag/state_quantizer.py` (1-150),
`mag/bonds.py` (1-120), `mag/hermes_warm_boot.py` (full), `mag/memory_consolidate.py` (1-130),
`mag/state_snapshot.py` (1-100), `mag/context_checkpoint.py` (1-80), `mag/context_compression.py`
(1-100), `mag/context_admission.py` (header), `mag/verkle_compaction.py` (header),
`mag/chain_substrate.py` (header), `mag/solved_surface.py` (header), `mag/percolator.py` (header),
`mag/agent_state.py` (header), `tools/thought_quantizer.py` (1-90), `tools/pile_classify.py`
(header), `memory/rib/` listing, `memory/biography/verkle_chain.jsonl` tail + first-knot keys,
`memory/biography/verkle_tip.json`, `memory/warm_state.json`.

Live checks run this pass (both green):

1. Janitor context pack build: `.venv\Scripts\python.exe -c "...build_context_pack(mode='janitor',
   fast=True); format_context_pack_text(p)..."` produced a 1,196-char pack against the 1,200-char
   janitor budget (`mag/context_pack.py:57`), `tip.ok=True` root `be326c3b1ed7...`, bonds clipped
   to 500, quantized_laws section present reading `compile v0.3 2026-09-28`.
2. Quantizer fossil arm: `.venv\Scripts\python.exe tools\thought_quantizer.py --check` printed
   `THOUGHT-QUANTIZER: fresh, 3.3h old (v0.3)`, exit 0.

Measured facts used below: the chain file `memory/biography/verkle_chain.jsonl` is 5,782,308
bytes across 8,247 knots; tip root `11ef5df8b409c659...`, `updated_minute 2026-09-28T19:22:27Z`,
last session `autonomous-auto-fkb-5409be`. Knot fields (read from line 1 of the chain): `ts,
filename, leaf_hash, session_id, start_minute, end_minute, dominant_theme, theme_vector_normalized,
tension_index, dossier_commit, amended, index, n_leaves, parent_verkle_root, verkle_root`.
`memory/rib/` holds 45 files spanning 2026-08-10 to 2026-09-28. `memory/percolator/invariants.json`
holds 352 hash-keyed entries (counted with the venv interpreter this pass). `memory/warm_state.json`
was generated 2026-09-28T16:20:10Z with chain index 8211, i.e. 36 knots behind the tip when read,
which is itself evidence for the staleness model in section 4.

## 1. The scales as they exist today (inventory, not proposal)

The ask names five scales. The estate actually implements seven, and two of the extra two are the
interesting ones.

- **S0, seconds-minutes: the model context window.** Managed by `mag/context_admission.py`
  (preflight admission, repack at 85% of window, "a prompt is admitted before dispatch, not after
  the provider rejects it") and `mag/context_compression.py` (LLingua-style compaction, "compress
  form, not substance"). The window is not a store, it is a cache with a lease: `mag/context_pack.py:430-525`
  implements the A2 law that the system prompt plus tool schemas are a byte-identical frozen
  prefix per session (provider prompt caches price on exact prefix bytes) and every live value
  rides in a capped evolving tail. Repack events are marked inside the tail ("History was compacted
  to fit this provider's context window... do not re-discover from zero").
- **S1, hours: the context pack.** `build_context_pack()` assembles ~47 layers per mode with per-mode
  budgets (`mag/context_pack.py:52-146`): janitor 1,200 chars, route 1,800, build 5,500, audit 7,500,
  plan 11,000, full 4,500 with an operator escape hatch capped at 200,000 (`_full_context_limit`,
  line 283-294). Render order is policy, bonds, skills, build, trail, task, heat.
- **S1.5, hours-days: residual bonds.** `mag/bonds.py` ingests residual + brief + verkle leaf into
  `memory/bonds_active.{md,json}` as "first-class next-session inputs" (docstring line 1-5).
- **S2, days: quantizer packs.** `tools/thought_quantizer.py` compiles the percolator's 352
  invariants into tiered packs (`instructions_{flash,frontier,local}.jsonl`), weight = recency x
  shape, flash capped at 220 chars per law. The docstring names the fossil it replaces: the v0.2
  packs compiled once on 2026-09-18 and were never consumed again; v0.3 wires delivery into the
  boot pack via `_quantized_laws` (`mag/context_pack.py:343-391`).
- **S2.5, days: the pile and case law.** `mag/state_snapshot.py` captures goal/outcome/tier/lessons
  at escalations and session close into `memory/pile/state_summaries.jsonl` (dedup by state_hash,
  line 86-91); `tools/pile_classify.py` drains it overnight with a local model into
  `classified.jsonl` + training rows + skill_ledger case law. `mag/skill_ledger.py` proven moves
  render back into the pack (`_proven_moves_excerpt`, context_pack.py:394-406).
- **S3, weeks: RIBs.** 45 files in `memory/rib/`, dated 2026-08-10 through 2026-09-28. They are the
  memweave doctrine layer: `_rib_doctrine()` (context_pack.py:305-340) injects title + goal line
  per RIB at boot, capped at 2,800 chars (12,000 in full-context mode). Human-and-seat-authored,
  not machine-compiled; per the driving ladder this is the judgment tier.
- **S4, permanent: the Verkle chain.** 8,247 hash-linked knots, parent_verkle_root chaining, tip
  pointer in `verkle_tip.json` whose schema note is a consistency law in one line: "Tip is the
  chain tail. An amended older session does not become the boot." `mag/chain_substrate.py` states
  the unification thesis: "The chain is ONE thing; these are six ways of reading it" (sense, core,
  surface, world, vmem, heartbeat). Compression into the chain happens at two altitudes:
  `mag/context_checkpoint.py` writes per-turn ~200-token checkpoints so "context lives in the
  chain, not in any model's window", and `mag/state_quantizer.py` writes quantum summary knots,
  "a single Verkle knot that represents the compressed state of N previous knots. Agents read ONE
  knot instead of N" (docstring lines 15-19).

The two extra scales (S1.5 bonds, S2.5 pile) are not noise in the ask's taxonomy; they are the
promotion corridors. A scale without a corridor is a museum. The ask's five scales are the
shelves; the bonds and the pile are the conveyor belts.

## 2. What lives at each scale (the unified statement)

The unifying invariant, already latent in the estate and worth making explicit as law:

**The chain is the log. Every other scale is a materialized view of the log, and every view must
declare its rebuild command and render its own staleness.**

- S4 chain: raw record. Append-only, content-addressed, hash-chained. Holds leaves (session
  knots), checkpoints (turn summaries), quantum summary knots (compressed state), agent_state
  versions (`mag/agent_state.py`: "amend = new version, not erase").
- S3 RIBs: distilled understanding extracted from weeks of chain + receipts by judgment (seat or
  operator). Not derivable deterministically from the chain; that is why they live at the judgment
  tier and not in a compiler.
- S2 quantizer packs: compiled law, deterministically derived from the percolator's invariant
  registry (repeat-detection: "if that canonical has been seen before -> REPEAT -> compile to
  INVARIANT. Recurrence = stable truth worth compiling", `mag/percolator.py` header). The
  percolator is a frequency gate on the signal stream; the quantizer is a shape and recency
  compiler on the invariants; the context pack is the delivery vehicle. Three stages, each
  independently runnable, which is exactly why v0.2 fossilized: nothing enforced the pipeline
  stayed connected. v0.3 fixed it by making the consumer render staleness.
- S2.5 pile/classified/case law: episodic-to-semantic corridor. `mag/memory_consolidate.py` names
  its sources in the header: Generative Agents (2304.03442) importance/recency/relevance, MemGPT
  (2310.08560) recursive-summary with a memory-pressure trigger, EverMemOS (2601.02163)
  episodic-to-semantic consolidation. These citations are the estate's own, in code
  (memory_consolidate.py:3-5), and the module implements them with the documented constants:
  pressure fold at 8,000 chars (line 46), decay 0.995 per hour (line 48), retrieval weights
  recency/importance/relevance = 0.3/0.5/0.2 (line 50).
- S1 pack: the hours-scale projection of all of the above into one budgeted, layered document.
- S0 window: the working set. Frozen prefix (doctrine + objective + compiled laws, stable for the
  session) plus evolving tail (pack, residual, goal).

What lives where is therefore decided by one rule: **a fact's scale is set by its write frequency
and its verification cost.** Per-turn facts (tool results, decisions) live in checkpoints and
trail; per-session facts (bonds, residual, brief) live in S1.5; per-occurrence-pattern facts
(invariants, compiled law) live in S2; per-arc understanding (RIBs) lives in S3; per-fact
immutability (leaves, hashes) lives in S4. Anything whose verification cost is high and whose
content is stable gets promoted toward the chain; anything cheap and volatile stays in the window.

## 3. Promotion and demotion triggers (the actual mechanism map)

The estate already implements every arrow; they are just not written down as one table. Here is
the table, each row grounded:

**Promotion (downscale movement, minutes toward permanence):**

| From -> To | Trigger in code | Site |
|---|---|---|
| window -> pack | admission pressure (tokens >= 85% window) fires auto-repack | `mag/context_admission.py assess()`; repack marker in `evolving_tail()` |
| window -> chain | every turn writes a checkpoint ("Every turn writes a checkpoint. No orphaned context windows.") | `mag/context_checkpoint.py` header law |
| window/pack -> pile | escalation or session close captures a structured summary | `mag/state_snapshot.capture_summary()`, wired in `decision_framework.escalate_on_loop` |
| pack -> bonds | session end ingests residual + brief + verkle leaf | `mag/bonds.py ingest_bonds()`, called from pack build when `refresh_bonds` or missing |
| pile -> case law | overnight local-model drain, idempotent by id | `tools/pile_classify.py` -> `classified.jsonl` + skill_ledger `record_decision` |
| signal -> invariants | percolator repeat-detection (canonical seen before) | `mag/percolator.py percolate()` |
| invariants -> packs | quantizer compile, weight = recency x shape | `tools/thought_quantizer.py compile` |
| knots -> summary knot | state quantizer aggregates theme vectors of N knots into one quantum knot | `mag/state_quantizer.py aggregate_theme_vectors()` |
| chain weeks -> RIB | a lesson learned twice (percolator recurrence) plus judgment promotes it to doctrine | `memory/rib/` convention, memweave doctrine |

**Demotion (upscale movement, hot toward cold):**

| From -> To | Trigger in code | Site |
|---|---|---|
| window | pack clip ladder: drop L4 heat, then compact L3, then shed L0d/L0f context blocks, then hard clip; directives and the frozen BUILD contract survive every rung | `format_context_pack_text`, `mag/context_pack.py:1235-1278`, with offload receipts to `watch/inbox/PACK_OFFLOAD.jsonl` |
| pack | quantizer staleness: packs older than 7 days render as a one-line debt pointer instead of law | `_quantized_laws`, `mag/context_pack.py:376-378` |
| retrieval ranking | soft decay: score = recency(exp 0.995/hr) + importance + relevance; unaccessed records stop ranking, "nothing is deleted; the raw store stays append-only" | `mag/memory_consolidate.py:16-18, 128-130` |
| chain | compaction folds only rows whose session evidence is already gone (orphan knot files) into ONE counter leaf carrying a Merkle root over every folded hash; rows with live evidence are kept; plan-only, operator-gated | `mag/verkle_compaction.py` header, pending Q-001 operator GO |

Three design facts worth naming. First, the clip ladder is asymmetric by law: the worker's
contract (frozen BUILD, scope card) outlives context history, so demotion inside the window is
*ordered*, not proportional; the rungs shed heat before doctrine. Second, demotion never deletes
except in the one operator-gated case: the estate's own fossil-99 law ("no silent partial
coverage") requires folding to preserve an anchor (pre-fold root, leaf count, archive sha256,
Merkle root over folded hashes), making the "demotion" of chain rows itself a recorded promotion.
Third, promotion and demotion are not inverses. Promotion is event-driven (a session ends, a
signal repeats, pressure crosses a threshold); demotion is time- or pressure-driven (TTL, age
threshold, window pressure). The architecture is a diode with a relief valve.

## 4. The retrieval path

The read path is pointer-first and cache-shaped, and my live janitor-pack run shows it end to end:

1. **Cold start:** `python -m mag.hermes_warm_boot` reads the chain's last line, the deploy
   registry, and the latest brief into `memory/warm_state.json` (`mag/hermes_warm_boot.py:39-94`).
   This is a tip cache with visible staleness: the file I read was generated 16:20Z with index
   8211 while the tip had moved to 8247 by 19:22Z, a 36-knot lag that is harmless because the
   payload is pointers, not history.
2. **Boot pack:** `build_context_pack()` pulls the tip badge (12-hex root short + n_leaves, not
   payloads, context_pack.py:709-730), doctrine titles, compiled laws, proven moves, solved
   history, bonds text, and the residual census. The census is a measured lesson in retrieval
   cost: the full scan of ~3.7k residual files wedged boots through a container mount, so it is
   cached hourly in `memory/working/residual_census.json` (TTL 3600s, context_pack.py:528-568).
3. **Per-call:** the frozen prefix is byte-identical for the session (A2 law) so provider prompt
   caches hit; only the capped tail re-renders. Retrieval is therefore amortized: the expensive
   cross-scale fan-out happens once per session, not per turn.
4. **Cross-scale lookup:** `mag/solved_surface.py` is the existing unified retrieval seam, reading
   case law (`pro_library.json`), the RIB index, and the verkle tip in one deterministic call,
   surfaced into the pack as "Solved history (what the system already holds - don't redo)"
   (context_pack.py:1113-1118) with the operator directive behind it quoted in its header.
5. **Session continuity:** `restore_pointer()` rehydrates a prior session from its checkpoint
   pointer rather than its transcript (context_pack.py:733-740).

The economics are the checkpoint module's own arithmetic (context_checkpoint.py:14-19): a 10K-token
context per turn versus a 200-token pointer is a 50x cut on the re-read tax, and the bigger win is
model mobility: the pointer is the same bytes for any provider, which is what makes the tier
ladder (ollama to funded remote) survivable.

The one retrieval path that is still O(file): `hermes_warm_boot._chain_tip` reads the entire
5.78MB chain to take its last line (`hermes_warm_boot.py:43`). It works today and matches the
residual-census wedge's shape (a full scan on every boot); the tip file already exists as the
index, so the fix is to trust the tip and verify by leaf_hash rather than re-scan. Not urgent at
5.8MB; certain at 500MB if the fleet keeps landing 8 knots a day plus FKB rebuilds.

## 5. The consistency model

Name it: **log-serialized, view-eventual, staleness-visible, amend-not-erase.**

- **Log-serialized:** the chain is the only serialization point. Hash-linked parent roots give a
  total order; the tip is a cached pointer with the amendment law ("an amended older session does
  not become the boot"), so re-running history never rewrites the record. Reads that need proof
  go content-addressed by leaf_hash ("Checkpoints are content-addressed. Tampering is
  detectable", context_checkpoint.py:24).
- **View-eventual:** every derived scale (packs, bonds, quantizer packs, RIB doctrine titles,
  warm state, census caches) is eventually consistent with the log, with a declared rebuild
  command (brief, bonds, quantizer compile, warm boot, census) and no lock between writer and
  reader. A seat booting against a 36-knot-stale warm state is correct behavior, not a bug.
- **Staleness-visible:** this is the estate's signature move and the part worth generalizing as
  law. No view is allowed to lie about its age: quantizer packs older than 7d render a debt
  pointer instead of content (context_pack.py:376-378); the census drift patrol flags a stale
  test-census carrier; `tools/freshness_check.py` marks boot docs STALE past 7 days; the pack
  itself prints its ts in the header. Compare the fossil this replaces: the v0.2 quantizer packs
  had "zero staleness alarms and, on audit, zero live consumers" (thought_quantizer.py:8-9).
  Visible staleness is what lets eventual consistency be safe, because a stale view announces
  itself instead of masquerading as truth.
- **Amend-not-erase:** writes at every scale are append or new-version (agent_state "amend = new
  version, not erase"; ledger amendments 001-006 in the tide machinery; MEMORY.md index flips
  recorded as events). Conflicts at promotion time are caught structurally, not by merges:
  `bonds.scan_conflicts()` (bonds.py:82-119) refuses a new bond that has opposite polarity and
  high subject overlap with an existing one, which is a cheap, deterministic contradiction gate at
  exactly the scale where contradictions are born.
- **Gated destructive exception:** the only destructive path (chain compaction) is plan-only,
  operator-gated, and anchored: folded rows keep a Merkle root and archive hash, so even garbage
  collection is a recorded event. Per the Q-028 commit line, FW-48/Q-001 remains plan-only OWED
  operator GO, so today the permanent scale has no automatic GC at all: 8,247 knots grow
  unbounded, and the counterfactual cost is the B2-87 receipted FKB rebuild pattern (17 -> 1,421
  signatures) applied to chain bytes.

## 6. Gaps and the three moves that close them

Honest defects observed, not hypotheticals:

1. **Three consolidators, no arbiter.** `state_quantizer` (quantum summary knots), `memory_consolidate`
   (rolling scope summaries), and `pile_classify` (case law) all compress history into durable
   artifacts, and nothing decides which owns which span. The design answer is already half-present:
   the percolator's repeat gate should be the sole promotion test for anything entering invariants,
   the quantizer the sole compiler out of invariants, and the pile the sole corridor for episodes.
   State quantizer's summary knots are the odd one out: they overlap memory_consolidate's folds and
   are the only consolidator with no consumer visible in the pack path. Either wire them into the
   full-context mount or register them dormant, the same fate the fossil law demands for
   wired-but-unconsumed surfaces.
2. **The write-side ladder is thinner than the read-side ladder.** The pack has a four-rung clip
   ladder with offload receipts; the estate lacks a symmetric promotion ladder statement, which is
   why three consolidators could coexist unnoticed. The section 3 table is that ladder; landing it
   as a one-page spec (the memweave doctrine file this item could seed) is the cheapest durable
   fix.
3. **Chain reads are O(file) in two places** (`_chain_tip` full scan; chain_query tail paths).
   The tip file plus a rolling 100-knot index would make every boot O(1) with the leaf_hash
   serving as the integrity check, consistent with the "tip is the chain tail" law.

The unification, in one sentence: **one append-only hash-chained log as the sole record; every
other scale a materialized view with a named rebuild command; promotion by recurrence and
pressure through the bonds-pile-percolator corridors; demotion by TTL and clip ladder with soft
decay and no deletion outside an anchored, operator-gated fold; and staleness rendered, never
hidden.** The estate has already built all of the pieces; what it has not had is the map. This
item is the map.

## 7. Literature anchors (what the code itself claims, plus standard CS analogy)

In-code, verified this pass: `mag/memory_consolidate.py:3-5` cites Generative Agents
(arXiv 2304.03442, importance/recency/relevance scoring), MemGPT (arXiv 2310.08560, recursive
summary under memory pressure), and EverMemOS (arXiv 2601.02163, episodic-to-semantic
consolidation), and implements their constants (decay 0.995/hr, weights 0.3/0.5/0.2, 8,000-char
pressure fold). `mag/context_compression.py:3` cites LLMLingua as its steal source. I did not
fetch those papers this pass; the citations are recorded as the estate's own provenance
statements, and the mechanisms they name are visible in the code that cites them.

The standard-systems analogy, offered as analogy and not as citation: the hierarchy is the
classic storage pyramid with the costs inverted for tokens instead of nanoseconds. The window is
SRAM (tiny, expensive, evicted by a clip ladder that is LRU with doctrine-pinned pages), the pack
is RAM (hours, budgeted per process class), quantizer packs and case law are disk (days,
compiled, seekable), RIBs are tape with a human-authored index, and the chain is WORM storage
with a hash-addressed filesystem. The two estate-specific departures from the textbook are worth
keeping: demotion is re-ranking rather than eviction (soft decay, nothing deleted), and every
cache line carries its own age in-band (visible staleness), which is the property the textbook
hierarchy lacks and the one that saved this fleet from a second quantizer fossil.
