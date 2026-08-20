# CROWN JEWELS — full self-steal inventory (2026-08-20)

Everything genuinely novel we hold, cataloged for the Mycelial Republic exchange.
Grouped into systems (not a file dump). Flagged: **[ONLY US]** = mechanism we believe
nobody else runs. This is the *machinery* we'd offer a prolific creator to use and enhance.

---

## TIER 1 — the mechanisms nobody really has but us

### 1. The Stateless System **[ONLY US]**
The operator's own flag: "the insane stateless system nobody really has but us."
A worker can be born fresh — no accumulated state, no persona, no history — and
bootstrap purely from a **frozen prefix** of current state (tools + interfaces + live
truth). Workers die; the **wave persists**. Identity lives in the invariant, not a
mutable blob.
- `mag/stateless_research.py`, `mag/ghost_cold_boot.py`, `mag/self_drive.py`
  (`fresh_context_pack` mode), `mag/state_quantizer.py`, `mag/state_snapshot.py`
- The doctrine that makes the clean-slate launch possible at all.

### 2. MemWeave **[ONLY US]**
The memory doctrine: **memlang × RIB × weave** — memory written in a compact language,
frozen into specs (RIBs), woven into a standing wave across sessions. Memory isn't
stored-and-queried; it's *resonated*. Crosswalked with source truth, never interpreted
loose.
- `mag/memweave.py`, `mag/memlang.py`, `mag/rib_bus.py`, `mag/shader_bus.py`,
  `mag/mem_weave_distributor.py`, `mag/standing_wave.py`, `mag/gpu_memweave.py`

### 3. MemLance / VerkleLance — selective memory **[ONLY US]**
Not "load everything." **Select** the memory to surface per-task (Quicksort-style
selection), then lance only the relevant leaves. A memory economy: the right bytes at
the right moment, not the whole chain.
- `mag/ghost_memlance.py`, `mag/verkle_lance.py`, `mag/mem_lands.py`,
  `mag/attention_ranker.py`, `mag/mem_state_feed.py`

### 4. The Verkle Knot / hash-linked memory chain **[ONLY US]**
A content-addressed, append-only, hash-linked chain of **knots** — the sovereign's
durable substrate (6k+ leaves, ~20-min cadence). Every commit references its parent
root; state is replayable and verifiable. This is the "disk is law" made structural.
- `mag/verkle_knot.py`, `mag/verkle_bus.py`, `mag/verkle_lance.py`, `mag/verkle_rib.py`,
  `mag/verkle_audit.py`, `mag/knot_math.py`, `mag/chain_query.py`, `mag/chain_substrate.py`

### 5. Ghost — the execution surface
The custom agent / tool-runner that *executes* through its own tools (mem, weave,
artifacts, dry-runs, integration) instead of a terminal spawn. The hand that does the
work; the reason "never a terminal spawn" is possible.
- `mag/ghost*.py` — ghost, ghost_auto, ghost_cold_boot, ghost_control, ghost_doctor,
  ghost_experimenter, ghost_identity, ghost_ledger, ghost_memlance, ghost_nudge,
  ghost_pylance, ghost_server, ghost_summon, ghost_talk, ghost_whisper

---

## TIER 2 — highly novel, strong share value

### 6. The autonomous loop (governor + autorun + drainer)
A self-running loop: work is **queued**, a **drainer** eats it headless, a
**governor/autorun** reconciles on a cadence, an **AFK loop** runs even when no one
watches. This is "sovereign" operationally — the system keeps itself alive.
- `mag/governor_autorun.py`, `mag/afk_cadence.py`, `mag/afk_loop.py`,
  `mag/orchestrator.py`, `mag/resume_order.py`, `mag/drainer_stats.py`, `mag/process_supervisor.py`

### 7. The cache-mining economics
The technique that made the cheap/owned side carry the load: measured **~98% cache
hit** → low-single-digit dollars for a workload whose frontier-equivalent was
**~$100–400+**. A portable economics lesson, not just a number.
- `mag/cache_router.py`, `mag/cache_extract.py`, `mag/cache_map.py`, `mag/cache_shard.py`,
  `mag/tokenomics.py`, `mag/token_economy.py`, `mag/compute_reconcile.py`

### 8. The RIB verification layer
Every finished piece gets a **frozen spec** (contract + expected behavior) and is
verified against it — "trust bytes, not reports." The module-level false-success guard.
- `mag/rib_*.py`, `mag/session_rib.py`, `mag/rib_launcher.py`, `mag/rib_render.py`,
  `mag/rib_k8s.py`, `mag/spec_gate.py`

### 9. The Swarm Surface (route_novel → k8s)
One shared primitive routes any novel research to a cloud swarm; a 24/7 K8s CronJob
drains it in-cluster. Distributed, stateless, deduped by content anchor.
- `mag/swarm_surface.py`, `mag/swarm_worker.py`, `mag/swarm_self.py`, `mag/swarm_emerge.py`,
  `mag/vessel_swarm.py`, `mag/water_swarm.py`

### 10. The Seat Steer / headless seat driver
Drive grok / chatgpt / deepseek / saelis **headless** via queue task files the drainer
executes — no browser, no manual windows. The multi-seat brain.
- `mag/seat_steer.py`, `mag/steer*.py`, `mag/seat_registry.py`, `mag/seat_feed.py`

---

## TIER 3 — distinctive products / surfaces

### 11. The Voice / Gab seat — headless voice loop
A browser-free voice loop: capture → STT → turn → TTS. Voice as a real working surface.
- `mag/gab_seat.py`, `mag/voice_*.py` (~15 voice modules), `mag/tts.py`

### 12. The Game line — distributed collaborative storytelling
A verkle-committed persistent world, state-first/LLM-last engine, narrator, battle
cycle, saga accumulation (the "Boatmurdered" pass-the-save model). This validates the
whole shared-substrate thesis as a playable product.
- `mag/game_*.py` (~35 modules): game_world, game_campaign, game_narrate, game_saga,
  game_dm, game_dm_voice, game_piece_tandem, game_score, game_ramp, game_dfhack

### 13. The Desk — the teaching surface
A desk orchestrator / overseer / observer that *teaches* a local model, probes it,
and observes the loop. The apprenticeship loop.
- `mag/desk_*.py`, `mag/desk_orchestrator*.py`, `mag/desk_teaching.py`

### 14. The Republic — the exchange itself
The governance layer for the Mycelial Republic — ambassador, feed, governance, loop,
OS, wave. The home of this very exchange.
- `mag/republic_*.py`

### 15. The Lenses / Shaders / invariants
A lensing + invariant lattice: map any input to the invariant that governs it;
lens-chain, lens-knot, shader-bus mapping. The "map precedes territory" machinery.
- `mag/lens_*.py`, `mag/shader_*.py`, `mag/invariant*.py`, `mag/template_invariant.py`

### 16. The Shadow / capture-defense layer
Self-defense against capture and mind-viruses: shadow work, capture guard, egregore
steal, guardrail sentinel, leak detector. The anti-capture discipline made code.
- `mag/shadow_*.py`, `mag/capture_guard.py`, `mag/egregore_steal.py`,
  `mag/guardrail_sentinel.py`, `mag/ghost_leak_detector.py`

### 17. Behavioral analytics
Mine *minute behavioral signals* (intonation, pacing, frustration) as training data —
behavior is information.
- `mag/behavioral_analytics.py`, `mag/behavioral_lensing.py`, `mag/behavioral_synth.py`

---

## The share posture (for the republic exchange)
- **Share the machinery, never the contents.** Contracts, patterns, and design laws are
  for the republic. `providers.yaml`, `mag-secret.yaml`, the runtime memory, the
  persona — never.
- **Offer the forkable, enhanceable cores first:** the Stateless System, MemWeave,
  MemLance, the Verkle knot, the cache economics, the autonomous loop. Those are the
  ones a prolific creator can *take and enhance to his needs*.
- **Zero-dependency, zero-friction forks** (pure-stdlib where possible) so a recipient
  runs it with `python -m pytest tests/ -q` — the STEAL hygiene rule.
