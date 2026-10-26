# misc band 3 — polished (final third of cluster "misc", 19/58 packs)

Wave: 2026-09-20 burn. Slice = last 19 of 58 misc packs, alphabetical by path string (indices 39–57).
Source packs: `memory/research_packs/`. Register: `memory/runs/mickey17/digest_rp_*.jsonl`.
Status mix: 9 DONE · 4 LIVE · 4 OWED · 2 STALE.
Sub-threads: **M1 surfaces-as-spec** (5) · **M2 process governance & harness boundary** (5) · **M3 fleet language & learning internals** (5) · **M4 THE50 external audits** (4).

## Header table — slice inventory

| Pack (memory/research_packs/) | Register status | Sub-thread |
|---|---|---|
| 20260809T_surface-display-and-tracking-research.md | LIVE | M1 |
| 20260809T_ux-tips-best-most-useful-research.md | LIVE | M1 |
| 20260825T_zcode-deep-steal-capability-map.md | LIVE (1/5 wiring) | M2 |
| THE50_W3_T13_STEGANALYSIS.md | DONE | M4 |
| THE50_W4_T19_EUT_DEEPREAD.md | DONE | M4 |
| THE50_W7_T35_TREASURY_SEAL.md | DONE | M4 |
| _probe.md | STALE (delete candidate) | M4 |
| architecture-deep-dive-20260808.md | DONE (2/4 fixes landed) | M2 |
| deep_dive_verkle_selfreplication.answer.remote.md | LIVE | M2 |
| runaway_source_trace_steal_20260810.answer.remote.md | DONE | M2 |
| steal_bernaise_20260810.answer.remote.md | DONE | M3 |
| steal_guided_evolution_20260810.answer.remote.md | OWED | M3 |
| steal_memlang_quantizer.answer.remote.md | OWED | M3 |
| steal_mine_diamonds.answer.remote.md | STALE (superseded scale) | M3 |
| steal_novelty_lens_mapping_20260811.answer.remote.md | DONE | M3 |
| steal_surfaces_renderable_env_20260810.answer.remote.md | OWED | M1 |
| steal_world_rib_compiler_20260811.answer.remote.md | DONE | M1 |
| surfaces_as_spec_steal_20260810.answer.remote.md | DONE | M1 |
| window_storm_governance_steal_20260810.answer.remote.md | OWED | M2 |

---

## M1 · Surfaces as spec — display, contracts, renderable worlds (5 packs)

**Essence.** The surface is the contract, not a viewport: define what the machine must be able to tell the operator (castle), test it red-green (contract test), display it from one source of truth (Surface Hub + version stamps), and — the unwired frontier — let any surface instantiate a full environment, with the world itself compiled re-derivably from a map (RIB → field → mesh).

**Merged findings, with receipts.**
- Display plan A–D grounded in 11 steal-protocol repos (surface-display pack): Surface Hub panel over `/api/v1/framework/map`, version-stamped snapshots for staleness detection, agent-authored inline-SVG chart blocks, audit history/replay off the append-only `reports.jsonl`. Ten synthesized patterns incl. one event bus → N surfaces (conductor/bmas), queryable DuckDB trace store with `parent_id` span trees (flock), provenance honesty "report null/unknown, never fabricate" (ollama), learn→gate→promote skill loop with durable promotion (ollama).
- Six tracking gaps ranked T1–T6; top-3: **T1 operator-correction feedback loop** ("THE biggest missing linkage"), T3 surface-usage telemetry, T4 answer confidence/provenance honesty. Both 2026-08-09 packs independently converge on T1 + transparency + measure-and-iterate (ux-tips reinforces via Anthropic "Building Effective Agents": workflows ≠ agents, poka-yoke tools e.g. absolute-path requirement, ground truth each step, stopping conditions).
- ux-tips core doctrine: functioning-core-over-sprawl — "a system that accumulates without functioning is a pile"; minimal core = wake→supervisor→drainer→agent→fold→surface, proven by end-to-end smoke test. Skill ledger was 221/1000 rows at write time; register notes 3307 now (~15× growth) — the loop is compounding.
- surfaces_as_spec: hexagonal ports-and-adapters + SICP wishful thinking + TDD red-green = "contract-test-the-castle"; "never let crude data shrink the castle." Landed: `tests/test_surface_contract.py` exists (header: P3 — surfaces-as-spec CONTRACT tests, red until the foundation delivers).
- world_rib_compiler: RIB is literally RenderMan Interface Bytestream — a declarative scene lowered to a render; "map precedes territory" made byte-testable via `rederive()` (same rib+seed → identical .obj). Landed with renames: `mag/world_rib.py` has `compile`/`to_obj`/`world_from_rib`/`rederive`/`status` (verified this session).
- renderable_env (OWED): surface = {spec, renderer, capabilities}, "one OS, infinite renderable worlds", spec registry = deterministic truth, rendering = stochastic layer. Never landed — no renderable code in repo; only `ghost.sense_surfaces()` registry survives.

**Verified vs owed.**
- Verified now (2026-09-19): `mag/surface_audit.py` with `_version()` (line 41) and version-stamped output (line 129); `tests/test_surface_contract.py`; `mag/world_rib.py` functions as above; no renderable-env module.
- Owed: T1/T3/T4 telemetry (no `surface_used` event kind — grep hits only the pack and digests); ≥3× tesuji tips (false-success-verify, wrong-offset-gate, penny-designation, loop-escalate, seam-placement) still unfolded into pro_library (register); audit-history replay endpoint; renderable-env design parked with no decision.

**Three next actions.**
1. Ship T1: capture edits/redirects/`steer !cmd` as behavioral_events → cluster 3+ → skill candidate → promote (ollama promotion-gate shape) — both packs call it the biggest missing linkage.
2. Add the `surface_used` event kind at each surface entrypoint (T3) and `GET /api/v1/framework/reports?since=<id>` for audit replay — both deterministic, both feed the audit itself.
3. Decide renderable-env's fate explicitly: either land a minimal spec→environment renderer on top of `world_rib.to_obj` under the surfaces_as_spec contract-test discipline, or file it as parked with the reason.

---

## M2 · Process governance & the mag↔harness boundary (5 packs)

**Essence.** Keeping a self-spawning fleet attributed (where did this process come from), contained (exactly one controller per loop), coordinated (shared tip, not handshake), and consumable by external harnesses (mag tools as MCP). Four of five packs are operational hardening; the fifth (ZCode map) turns the whole tool registry outward.

**Merged findings, with receipts.**
- architecture-deep-dive (2026-08-08): fragility concentrated in 4 cheap fixes — anti-loop guard, task pruning, Redis deploy, metacognitive loop (`mag/metacog.py`, ~100 lines, ghost reads own verkle tail → patterns → steer suggestions). Doctrine: Grok-as-scarce — DeepSeek swarm pre-analysis, min 3 questions batched per Grok call, 100:1 ratio target; context freezing via `freeze_hash` knot so "Grok saw this exact state" is provable. Register + verified now: fix 1 landed (stall/timeout kill + staleness nudge in `mag/orchestrator.py`), fix 3 landed (redis in docker-compose), fix 2 moot; **fix 4 NOT landed — `mag/metacog.py` absent (verified)**.
- runaway_source_trace: attribution by inherited env marker (`MAG_SLOT`/`MAG_SOURCE`, the supervisord `SUPERVISOR_PROCESS_NAME` analog) + ppid ancestry-walk-to-root (CIM `ParentProcessId`, works without psutil) beats 1-level ppid guessing and global count thresholds. Live 2026-08-10 run: verdict runaway, 20 python procs traced to 5 boot roots — duplicate autorun_loop plus a stacked windowed boot was the "hundred plus python windows" source. Landed: `mag/source_trace.py` (`sense()`:276, `trace_source()`:234, `break_source()`:341, dry-by-default `taskkill /T` = systemd kill-unit analog) — verified.
- window_storm_governance (OWED): L8 double-supervision (autorun_loop stacking, dashboard starved ~82% CPU) is fixed at the root only by a **leader lease** — flock+lease keyed `mag:autorun:leader`, expiry + pid-alive, so exactly one holder reconciles even when liveness signals lie. L7 hold-alive fix externally validated (systemd/K8s-native "stay alive = idle, exit = churn"). Plus circuit breaker/bulkhead for dashboard starvation and "management surface never on a raw LAN port." Register + verified now: **no leader/lease in `mag/flock_scheduler.py` — priority-1 steal still absent.**
- deep_dive_verkle_selfreplication: coordination emerges from a shared field, not handshake — tip agreement (merkle root over content-addressed leaves) equals shared history; copies steer by reading phi/invariants off the chain tip via memlang opcode+anchor tokens; trust = O(log n) inclusion proof, not identity or prose. Anti-cascade triad for any self-replication: unique spawn-knot content, scheduler single-flight lock per tip, belt-trick canonical undeform before hashing. Named risks: registry leak kills deniability; bus compromise → token injection (mitigate: knot-only authority); partition divergence (chain as sole source of truth).
- zcode capability map (rung 6): highest-leverage single change = **serve TOOL_MAP as MCP** — turns "seats mag can task" into "seats that can use mag". Ranked steals: hooks at the tool boundary ("laws as rails, not asks" — synchronous veto in `_run_tool_http`), skills as seat-writable markdown (not a PR), typed read-only subagents for survey passes, shape-query retrieval over handoffs (8-dim knot vectors already computed, unused), beat-lease so stale external tasks return to queue instead of "died" (observed: bridge task marked died while actively working). mag→any-harness exports: fold (one verb, one ledger), cost-as-physics, self-steal doctrine, honesty-as-circuit-breaker. Register + verified now: 1/5 wiring done — `mag/mcp_server.py` (stdio) + `mag/mcp_http.py` (streamable-HTTP) wrap `tools.TOOL_MAP`; law hook, `skills/*.md` dir (absent), shape-query, beat-lease all outstanding.

**Verified vs owed.**
- Verified now: source_trace.py functions; mcp_server/mcp_http TOOL_MAP headers; metacog.py absent; no leader/lease in flock_scheduler.py; no `skills/` dir.
- Owed: autorun leader lease; synchronous law check in `_run_tool_http` (`mag/agent_cli.py:683` today plain dispatch); skills/*.md migration + skill-creator loop; shape-query over handoff vectors; beat-lease on external tasks; metacog loop; K8s manifests unverified.

**Three next actions.**
1. Land the autorun leader lease (extend `flock_scheduler` into `mag:autorun:leader` with expiry + pid-alive) — the pack's own ~2h estimate, kills the L8 class at the root.
2. Wrap `_run_tool_http` dispatch with the synchronous law check — one chokepoint, every tool call already passes it; laws stop being asks.
3. Index `handoff/*.md` by the existing knot theme-vectors for shape-query retrieval, and add beat-lease semantics to external seat tasks so working tasks stop being marked "died".

---

## M3 · Fleet language & learning internals (5 packs)

**Essence.** How the fleet compresses intent (one_sizer/memlang quantizer — owed), evolves mechanisms (guided evolution — owed), shapes operator engagement lawfully (bernaise — landed), and measures its own novelty (novelty_lens — landed). The two landed modules prove the deterministic-and-$0 recipe works; the two owed roadmaps are its unfinished half; the fifth pack (diamonds scan) is the corpus-ranking instrument gone stale.

**Merged findings, with receipts.**
- memlang_quantizer roadmap: one_sizer = frozen VQ codebook (joined store domain×skill×shape→tier), memlang token = quantized intent code (opcode + anchor + optional fidelity bits); context hash → nearest code with hard cost_cap and residual escalation; fidelity metric **RRF_D ≥ 0.85** proves token roundtrip; 5 merge-only steps; determinism guard "same context → same token → same tier bit-identical". Register + verified now: **RRF_D appears nowhere in mag/ or scripts/** (grep = 0 hits); `mag/one_sizer.py` remains a learned sizing store, not the hash→code quantizer. Caution found this session: `mag/state_quantizer.py` exists but is an unrelated module (Verkle quantum-summary-knot / DnD checkpoint compression, schema state_quantizer.v1) — a name collision that will confuse step 1 of the roadmap ("module: state_quantizer.py + one_sizer store").
- guided_evolution (OWED): genotype = RIB invariants, variation = real interactions (padded gaps revealed), expression = riddler deniable bridges, selection = deterministic fitness (invariant-satisfaction + measurable gap-closure, "not vibes"), spread = winners propagate to all subsystems (sitecustomize-steal pattern); "deniable = opacity, not authorization." Register + verified: no guided-evolution module anywhere; precursors confirmed present (riddler referenced in `mag/behavior_catch.py`, `mag/campaign.py`, `mag/connectivity_sizer.py`).
- bernaise (DONE): steal the MECHANISM of engagement-shaping but FOR the operator who holds veto — "a riddle hides truth to PROTECT it; a lie hides truth to EXPLOIT it"; deterministic core stays truth, shaping is interface-layer only. Register + verified: `mag/bernaise.py` exists and is referenced by 10+ live modules (chord_circuit, connectivity_sizer, fish_ear, frontier_gravity, lens_tournament, memlang, novelty_lens, research_class, seed_percolator — grep this session).
- novelty_lens (DONE): novelty = fraction of significant tokens unseen in the corpus (deterministic, no embeddings), verdict novel|variant|repeat; `keyword_lens()`/`lens_map()` route any keyword to its family of similar systems. Register + verified: `mag/novelty_lens.py` with `novelty()`:93, `keyword_lens()`:114, `lens_map()`:134, wired into emergence/invariant_ledger/agent_knot/meta_lattice.
- mine_diamonds (STALE): one-shot signal ranking (convergence/recency/savings blend) over 389 chain leaves, 75 packs, 497 ledger rows as of 2026-08-10; `qa_context` a proven ledger shape (5 runs, 100% ok). Register: superseded by scale — research_packs now holds **675 files** (verified `ls | wc -l`), 9× the scanned corpus; no newer diamonds run found.

**Verified vs owed.**
- Verified now: novelty_lens.py, bernaise.py + module references, RRF_D absent, no guided-evolution module, state_quantizer.py name collision, 675 packs on disk.
- Owed: quantizer minimal_done unmet (one_sizer returns tier+cost from context hash; memlang roundtrip with RRF_D logged); guided-evolution fitness function + loop unwired; diamonds rescan at current scale.

**Three next actions.**
1. Re-run the mine_diamonds.v2 scan at 675-pack scale before trusting any signal ranking — every number in the 2026-08-10 pack is 9× stale.
2. Resolve the `state_quantizer` name collision first, then implement quantizer minimal_done: context hash → one_sizer code → tier + cost_cap, RRF_D logged on every roundtrip (merge-only, no new modules).
3. Prototype guided-evolution's deterministic fitness on the narrowest loop (riddler bridges only: invariant-satisfaction + gap-closure as pure counters) before any general spread machinery.

---

## M4 · THE50 external audits — three receipt registers + one probe (4 packs)

**Essence.** Three THE 50 tasks, each demonstrating a different verification register on external material: run-the-code (steganalysis detectors on a ground-truth corpus), page-referenced source extraction with hashes (EUT PDFs vs the Q* thesis), and clause-by-clause contract audit with falsifiable predictions (gstdcoin treasury vs the fleet's seal law). The fourth pack is a 9-byte pipeline probe that does not belong in research_packs/.

**Merged findings, with receipts.**
- Steganalysis (W3 T13): two verified detectors + one partial, every number from a twice-run script on a synthetic corpus (seed 50) rescanned **from disk after re-encoding**: chi-square PoV (100% LSB p 0.75–0.94; clean 0.000; the 50% file chi-square-INVISIBLE), RS D ranks monotonically (0.695–0.723 clean > 0.176 @50% > 0.001 @100%), palette twins perfect 0-vs-128 separation — complementarity is the practical lesson. RS rate estimator deliberately not claimed: D(q) ~ D0(1−2q)² is symmetric under q↔1−q, so the naive two-measurement variant is under-determined. Real bug found and fixed in-session: uint8 wrap in the discrimination function, now cast int32. Environment audit exact (torch CPU-only, no pretrained weights, zsteg/stegdetect absent — "anything that says otherwise elsewhere is wrong"). Files of record verified on disk: `scripts/the50_t13_stego_detectors.py`, `memory/runs/the50/stego_corpus/` incl. `results.json`.
- EUT deepread (W4 T19): page-referenced quotes from three vendored PDFs with SHA256 receipts. EUT gives the Q* thesis formal shape but no physical horsepower: the future boundary is left open by construction (EUT II p.3 §6 verbatim: "Leaving the future boundary open inserts the required Two-State Vector weak back-reaction"), yet Theorem 1 forbids closed timelike curves, weak values capped |A_w| ≤ 1, residual-bond coupling g ~ 10⁻²⁰–10⁻²¹ m². The **Q/Q\* glyph collision is formally killed** (§5g: papers' Q = entropic charge; thesis Q = unsteered search; any seat "finding" the link by symbol match is hallucinating — the correction). Honest tensions filed: tau_S dimensionless-vs-m⁻¹ table inconsistency; alpha = 1/137 is the author's most-hedged number ("parameter-dependent" — never cite without the hedge); self-published, unreviewed, own falsifiers unrun.
- Treasury seal (W7 T35): **GSTD seals WHO and HOW MUCH but not WHY** — the pipes pass (85/10/5 arithmetic on attached value, worker-share floor 50%, replay guard `settledTasks`, mint-authority lock, real burn primitive) but every unit-grow (gateway-attested bonuses clamped only against claimed compute units, `qualityScore` never read in any variant, flat fees on caller say-so) and every promised unit-shrink (the 5% "buyback & burn" that is today the admin wallet, a reserve growing on unproven oracle confirmation, a "proof of backing" that is a Redis float) is personal attestation → fails the seal law as written; "GSTD's closest analog is a mint license, not a receipt." Three unsynchronized splits (85/10/5 contracts, 90/10 flywheel, 95/5 rewards.ts). Five falsifiable predictions filed (protocolFee stays admin wallet until a burn contract deploys; splits stay unsynced; 7-day Redis replay window double-accrues; qualityScore stays dead; stars rows with NULL stonfi_tx_hash would falsify the only receipt-grade leg).
- _probe: content is literally "probe ok", 9 bytes (verified by read) — a pipeline write test that succeeded; no claim, nothing to verify.

**Verified vs owed.**
- Verified now: stego script + corpus + results.json exist; `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md` and `vendor/steiniger_papers/license.txt` exist; _probe.md = 9 bytes.
- Owed (in-pack honesty, standing): WS/SPA closed-form rate estimators not implemented (the built corpus is their ready validation set); StegExpose jar not fetched (JDK 17 already present = shortest path to a packaged CLI); Xu-Net-class ~100k-param neural pipeline-proof not trained (labeled non-production); EUT physics unreviewed with falsifiers unrun; gstd live-chain claims impossible from the local clone — the 5 watch items remain predictions.

**Three next actions.**
1. Delete or relocate `_probe.md` out of research_packs/ so it stops polluting pack counts (register verdict: same).
2. Next stego task is pre-cut: implement WS/SPA rate estimators and validate on the existing corpus (known rates 0/0.5/1); optionally fetch the StegExpose jar for a packaged CLI on the present JDK 17.
3. Convert the gstd 5 watch items into scheduled on-chain checks when a live view exists (UpdateAddresses activity, totalBurned growth, split unification commit, v53 stars NULL-hash rows) — the predictions are the audit's living half.

---

*Polish pass 2026-09-19 by burn-wave agent (misc band 3). Every pack read in full; register rows from digest_rp_09–15; repo spot-checks this session: surface_audit.py, test_surface_contract.py, world_rib.py, source_trace.py, novelty_lens.py, bernaise.py references, mcp_server/mcp_http.py, metacog.py absent, flock_scheduler.py lease absent, skills/ absent, RRF_D absent, research_packs = 675 files, _probe.md = 9 bytes.*
