# The quantized lattice fold - design (free-lane, night shift 2026-10-04)

- Seat: ZCode night shift, FREE-LANE design ask (memory/frontier/HELP_WANTED.md 2026-10-03 item 2: "design the quantized lattice fold for the ghost"). Relaunch of a first attempt that died on an account rate limit. No paid APIs used.
- Mode: read-only analysis plus this one design doc. Not committed. Python = `.\.venv\Scripts\python.exe` only; every count below was measured live this shift (instruments named inline).
- Aligned with the sibling verdict landed tonight: watch/inbox/night_shift_20261004/verkle_vs_embedding.md - the fold's citation leg is structural (exact id + row hash), never similarity-based. Do not contradict that row.
- Ask-context vs byte truth (trust bytes): the ask's context line says "v0.3 packs: 24 frontier / 12 flash / 12 local". Disk says v0.4, compiled 2026-09-29T15:18:39Z, packs 24 / 12 / 338 (compile_report.json). The "12 local" figure is the v0.3-era cutoff that left 283 kept laws in no pack; v0.4's L4 linker law (tools/thought_quantizer.py:225-245) takes the remainder into local, which is why local is 338. mag/estate_bridge.py:189 still advertises "Thought Quantizer v0.3 ... 2026-09-28" - a live example of hand-copied intel drifting from bytes.

## (a) Current-state inventory (file:line evidence)

### A1. The packs and their producer

- Location: memory/corpus/quantized_thought/ (instructions_frontier.jsonl 24 rows, instructions_flash.jsonl 12 rows, instructions_local.jsonl 338 rows, compile_report.json, plus adversarial_arc_invariants.jsonl 12 rows and graph_ghosts/; counted by chunked line read this shift).
- Producer: tools/thought_quantizer.py - input memory/percolator/invariants.json (DEFAULT_IN, tools/thought_quantizer.py:73), output the tier files (:74). Semantics: two-pass classify (fragments + pure telemetry refused, error-quoting laws kept, :106-139), weight = recency x shape (:142-160), disjoint tier bands flash -> frontier -> local with kept == packed enforced (:225-245). CLI defaults --frontier 24 --flash 12 --local 0 (:324-328). Fossil arm `--check` exits 1 when packs exceed the decay bar (:288-313).
- The ONE decay bar: PACK_STALE_DAYS = 7 (mag/constants.py:19), imported by the producer (:71), the one live consumer (mag/context_pack.py:14), and the boot meter (tools/freshness_check.py:39,63). L3 law: no second bar anywhere.
- Row shape (first flash row, read live): `{id: a77444ced5ab, class: law, raw_count, count_verdict: "inflated echo - provenance only", weight: 0.8, shape: imperative, last_seen: 2026-09-29, sources: [...], frontier: "[steer] Verify with git diff / actual file bytes...", flash: "Verify with git diff / actual file bytes before declaring done.", status: compiled-v0.4}`. The `id` is the first 12 hex of the percolator invariant key; ids persist across compiles while text can change, so id alone does not bind row bytes.
- Measured freshness and drift (this shift, .venv python): pack age 4.74d (bar 7d; goes STALE 2026-10-06T15:18Z). Input registry now 646 invariants vs 401 at compile = +245 (+61%) uncompiled drift; newest invariant last_seen 2026-10-04T07:33Z, i.e. the registry writes continuously while the packs sit. Per-tier recency: flash 0/12 rows older than 2026-09-27; frontier 14/24; local 327/338 - flash is the fresh band by construction, local is the decaying archive band.
- No scheduler compiles the packs: grep of scripts/ + configs/ finds thought_quantizer only in configs/fossil_registry.json:10-12 (the recompile/check commands registered as a fossil class). The alarms that exist are the fossil check, the boot meter, and the consumer's visible-debt line. Nothing recompiles on its own.

### A2. The one live consumer (and the dormant ones)

- Live: mag/context_pack.py:377-428 `_quantized_laws` - flash tier only, <= 1800 chars, rides the boot pack field "quantized_laws" (:989). Staleness is visible, never silent: past the bar it renders the one-line debt pointer and hides the law (:413-415). This is the delivery seam the v0.2 night never wired (its own docstring, :380-389). Consumers of context_pack are seats (mag.cmd context-pack), NOT the ghost.
- Marginal: mag/verb.py:32 reads adversarial_arc_invariants.jsonl as oracle grounding (a different file, 12 rows). tools/concept_span_check.py:61 cross-checks quantizer tiers. tools/graph_heal.py heals graph_ghosts/.
- The ghost consumes NONE of the tier packs today (grep for quantized/instructions_ across mag/ghost*.py: zero hits). The ghost's only percolator contact is a display-only count block: state["percolator"] = {ok, n_invariants, false_positives, noise, intake_open, explore} at mag/ghost.py:774-786 - and nothing downstream reads it (the director context builder omits it too, mag/ghost_director.py:179-201).

### A3. The ghost's organs today

- Organ map (mag/ghost.py:1-22): SENSE -> DEPLOY -> MEASURE -> CATALOG -> COMPOUND. Plus the satellites: ghost_director (DeepSeek designs experiments), ghost_auto (deterministic cadence), ghost_doctor (subswarm healer), ghost_identity (the persona vector), ghost_cold_boot (whisper restore).
- SENSE: sense() at mag/ghost.py builds fkb_signals, spider_blind, verkle_tip_stale, training_rows, frustration triggers (:849-855), percolator counts (:774-786), surfaces, and `_sig_text` (:826-836) - a lowercase token soup used for vector matching.
- AUTONOMOUS LOOP: autonomous_task_loop (mag/ghost.py:1314-1467) - 60s cycle; composes janitor quests from FKB sigs (tier split hardcoded: count >= 10 -> deepseek-v4-flash else qwen2.5-coder:7b, :1410-1411), dedups by sig for 60 min (:1296-1311), and suppresses a sig permanently once its diagnosis file exists (:1399-1409, the 2026-09-22 loop-close). Spawns land in memory/runs/ghost/autonomous_trail.jsonl rows `{ts, sig, quest_id, task_id, outcome}`.
- DIRECTOR: build_director_context (mag/ghost_director.py:147-201) shows fkb/spider/verkle/training/inbox + vectors + results - no compiled-law section. Last director trail rows are dry previews from 2026-08-08 (memory/runs/ghost/director/trail.jsonl tail): the director is wired but dormant in practice.
- GHOST_AUTO: run_cadence (mag/ghost_auto.py:121-162) - tesuji leaf + one_sizer record + at most 1 bounded stateless dispatch/day. No quantizer arm.
- GHOST_DOCTOR: prescribe() folds a lesson, reruns the circuit breaker, and dispatches a heal task through invariant_lattice.dispatch_to_k8s (mag/ghost_doctor.py:104-108).
- IDENTITY: ghost_identity.py:27-93 names the ghost's static body = the Verkle lattice and enumerates capabilities (sense/deploy/measure/coordinate/detect/quantize/consult/freeze/enforce/publish) - there is NO compiled-law organ in the list. That absence is precisely this ask.
- Lattice vocabulary already owned by: mag/invariant_lattice.py (mycelial view of doctrine nodes, verkle lattice view, steer_ollama, dispatch_to_k8s, render) and the ribs (memory/rib/DOCTRINE_MEMWEAVE_20260810.md:15,44-49: the lattice is where everything FOLDS; memory/rib/RIB_ROUNDTRIP_STATELESS_TURTLES_20260810.md:35: SENSE read lattice -> TRANSFORM -> FOLD write knot). Any "lattice fold" design must be a leg on THAT loop, not a new graph.

### A4. The measured defects the fold answers

- Re-fire bleed (autonomous_trail.jsonl, 2,696 rows 2026-08-08 -> 2026-10-04): 2,682 of 2,696 rows belong to multi-fire sigs; top sig fkb:run_python:2e689948ccfa fired 528 times. The loop-close fix stops sigs that HAVE a diagnosis file; sigs without one re-arm forever: fkb:amd_window_guard:5c63f4a34186 has 182 fires, no memory/runs/ghost/autonomous_fixes/amd_window_guard_5c63f4a34186.md, 4,770 total rows in logs/failure_kb.jsonl (counted this shift), and still spawning at 2026-10-04T08:43Z (2 of the last 3 trail rows). The compiled escalation law ("Escalate to the next smarter tier; stop local token bleed", flash row 74dbeef70dc8) exists in the pack and is exactly about this - and the loop never reads it.
- Packs fossilize on a moving registry: +245 invariants of drift in 4.74d, no recompiler, expiry 2026-10-06. The v0.2 fossil disease (packs compiled once, zero consumers, zero alarms - tools/thought_quantizer.py:4-10) is one missed recompile away from recurring.
- Ghost decisions are uncitable: trail/result rows carry sig/task ids but no reference to any law or doctrine row they rode. The estate's citation lint (AGENTS.md, a05-r2) enforces this for prose; the ghost's own ledger has no equivalent.

## (b) The fold design

### B0. What "lattice fold" means here (vocabulary alignment)

The round-trip law (SENSE the lattice -> TRANSFORM -> FOLD back) currently has a missing leg for compiled law: percolator invariants are folded INTO tier packs (the quantizer), and the boot pack folds flash law into SEATS (context_pack) - but the GHOST, the autonomous loop itself, never senses, cites, or re-folds the packs. The fold designed here is that leg, in three moves:

1. DELIVER: tier rows ride the ghost's existing decision surfaces (quest goals, director context, heal dispatches) as bounded riders - never as new gates.
2. CITE: every ghost decision row records the exact pack row it rode (tier + id + row-hash + compile ts), byte-checkable after the fact.
3. REFRESH + RE-FOLD: the ghost's own cadence keeps the packs fresh against the percolator registry (recompile arm), and catalog rows carrying law citations re-enter the percolator as usage facts (the compounding leg).

This deliberately reuses the standing-wave shape (watch/inbox/STANDING_WAVE_PROTOCOL_20260918.md:37-39): the packs are the queue-of-law, ghost_auto the tender, trail/results rows the receipt ledger (law 5: receipt-per-attempt), PACK_STALE_DAYS the lane ladder's cheap rung. No new substrate.

### B1. Which tier feeds which organ

| Ghost organ | Tier fed | Payload bound | Stage |
|---|---|---|---|
| sense() (60s loop) | none (metadata all tiers) | state["quantized_lattice"]: v, age_d, n per tier, stale flag | SVV |
| autonomous quest composer (ghost.py:1390-1467) | flash (top-K <= 3 by weight, K rows <= 300 chars) | law appendix in janitor goal text + law_refs in trail row | SVV |
| ghost_auto cadence (ghost_auto.py:121) | none | recompile arm (freshness + drift triggers) | SVV |
| director context (ghost_director.py:147) | frontier (24 rows, <= 1200 chars) | "## Compiled Fleet Law" section; system prompt addendum: cite law ids used | stage 2 (dormant organ) |
| ghost_doctor heal (ghost_doctor.py:104) | flash (top-1 by cause-token overlap) | heal goal rider + dispatch row law_refs | stage 2 |
| catalog/compound (ghost.py:2821) | passthrough | results rows gain law_refs; percolate "[ghost] law <id> rode <verdict>" | stage 2 (percolation arm), stage 3 (weight amendment - operator gate) |
| local tier (338 rows) | NO organ in v1 | archive band: the citation checker's lookup corpus and the lattice/microbial views' walking surface. Never a prompt payload. | standing |

Tier rationale follows the estate's own dose doctrine (mag/context_pack.py:377-389): flash = the boot-context dose of <= 220-char imperatives for every janitor quest; frontier = the deliberate-ask nuance for the one organ that actually deliberates (the director); local = the remainder archive, consulted by id, never injected.

### B2. Organ details

SENSE (SVV, ~15 lines). Add to sense() beside the percolator block (ghost.py:774-786): read compile_report.json + the three tier files through an mtime cache (the pattern at mag/percolator.py:105 - the 60s loop must not re-parse 338 rows per beat); emit {v, compiled, age_d, stale: age_d > PACK_STALE_DAYS, n: {frontier, flash, local}}. Display-only, deterministic, $0. When stale, the state carries the same one-line debt pointer context_pack renders so every dashboards sees it.

QUEST COMPOSER (SVV, the core). In autonomous_task_loop's FKB branch, after building the quest goal (ghost.py:1412-1425):
- Match: score flash rows by deterministic token overlap between the row's flash text and the sig string + goal tokens - the same `_tokens`/overlap trick as invariant_lattice.py:44-45 and match_vector's tag matching (ghost.py:2643-2644). Lexical and citable, NOT an embedding (retrieval-ladder alignment, B6).
- Rider: append up to 3 top-weight matched rows, total <= 300 chars, as a final goal line: `Fleet law (compiled 2026-09-29): <law 1> | <law 2>`.
- Citation: the appended trail row gains `"law_refs": [{"tier": "flash", "id": "<12hex>", "sha8": "<sha256(canon(row))[:8]>", "compiled": "2026-09-29"}]`. Canonical row = json.dumps(row, sort_keys=True) - the field-sorted hashing rule the activation spec already froze (watch/inbox/spec_quantizer_activation_20261002.md item 4).
- Escalation cites: when count >= 10 routes to deepseek (ghost.py:1410), the row that carried the escalation law (if matched) is recorded first in law_refs - the tier decision now names the law it rode instead of an anonymous threshold.
- Staleness: if the pack is stale, omit the rider entirely and record `"law_stale": true` on the trail row. The ghost still acts - law is a rider, never a gate (B4).

GHOST_AUTO RECOMPILE ARM (SVV). Add to run_cadence (mag/ghost_auto.py:121-162) before the dispatch step: call tools.thought_quantizer.compile_packs (import, same venv, deterministic $0; the sanctioned producer - no second compiler) when EITHER trigger fires:
- WALL: pack age > PACK_STALE_DAYS (the 7d outer wall; at current churn this never fires first).
- DRIFT: len(invariants) - compile_report.stats.in >= QUANTIZER_DRIFT_ROWS (new constant, proposed 128, mag/constants.py beside PACK_STALE_DAYS). Measured drift is ~52 invariants/day (245 in 4.74d), so 128 fires about every 2.4 active days; quiet weeks fall back to the wall. DRIFT_ROWS is a compile-cadence trigger, NOT a staleness bar - staleness semantics stay solely on PACK_STALE_DAYS (L3 one-bar law preserved).
The arm appends a row to memory/runs/ghost/ghost_auto state (or a small jsonl beside it): {compiled ts, pack shas, n in, drift closed}. This is the self-tending intake law (standing wave law 1) applied to law itself: nobody hand-feeds the packs.

DIRECTOR (stage 2). build_director_context gains "## Compiled Fleet Law" - the frontier tier verbatim, <= 1200 chars, with ids inline; DIRECTOR_SYSTEM (ghost_director.py:53-97) gains one constraint: "When a designed experiment relies on a compiled law, echo its id in the JSON as law_refs." The director is the deliberate-ask surface, so it gets frontier nuance, matching the dose doctrine. Dormant organ today (last trail 2026-08-08) - which is exactly why it is stage 2.

GHOST_DOCTOR (stage 2). prescribe() picks the top flash row by token overlap with the diagnosed cause, appends it to the heal goal, and the dispatch records law_refs. The doctor already routes through invariant_lattice.dispatch_to_k8s (ghost_doctor.py:104-108) - this only adds the rider + citation to a route that exists.

CATALOG / COMPOUND (stage 2-3). catalog() (mag/ghost.py:2821) passes law_refs from deploy into results.jsonl rows. Percolation leg: each measured outcome percolates one fact, "[ghost] law <id> rode a <consumed|silent|flipped> vector" - through the standing percolate() path (the only promotion gate, mag/percolator.py:23-27), so real usage accumulates as provenance on the invariant behind the law. Weight stays recency x shape in v0.4 semantics; a usage-informed weight amendment is a future operator-gated quantizer version, not this fold.

### B3. Refresh cadence, tied to percolator invariants

The percolator registry refreshes continuously (percolate() callers: mag/compiler_lang.py:110, mag/chord_pipeline.py:98, mag/evolving_wave.py:223, mag/ox_percolate.py:111, mag/frontier_help.py:152; newest last_seen 2026-10-04T07:33Z). The packs are a compiled VIEW of that registry, so their refresh law is derived from the registry's own motion: WALL (PACK_STALE_DAYS) OR DRIFT (>= 128 new invariants since stats.in). Both triggers read only numbers already on disk (compile_report.stats.in vs len(invariants.json)); both are checked in the ghost_auto cadence (deterministic, in-venv, no scheduling infrastructure beyond the cadence that already runs - afk_cadence.py:156 calls ghost_auto.run_cadence). The fossil classes already registered (configs/fossil_registry.json:10-12) remain the alarm if the cadence dies.

### B4. Staleness law (single bar, visible debt)

- ONE bar: PACK_STALE_DAYS = 7 (mag/constants.py:19). No per-tier bars, no organ-specific bars.
- Fresh: organs deliver + cite.
- Stale: organs OMIT law text and mark the decision row (law_stale: true); sense state carries the debt pointer naming the recompile command. Same semantics as mag/context_pack.py:413-415 - law hidden until fresh, debt visible, ghost never blocked.
- Tamper/shape failure: omit + debt line. When watch/inbox/spec_quantizer_activation_20261002.md lands (sha-verified, verkle-tip-bound, last-good serving), the ghost organs switch from reading files to consuming mag/quantizer_activation.py as their single source - the fold's consumer side is written against that interface shape from day one (id + sha8 + compiled ts is exactly what the activation manifest will bind).

### B5. Citation grammar (how a decision cites the row it rode)

Row field on any ghost decision ledger (autonomous_trail.jsonl, results.jsonl, director trail, heal dispatch):

`"law_refs": [{"tier": "flash", "id": "74dbeef70dc8", "sha8": "ab12cd34", "compiled": "2026-09-29"}]`

- id = the pack row id (12 hex, inherited from the invariant key). sha8 = first 8 hex of sha256 over the field-sorted row JSON - this is what binds exact bytes, because ids survive recompiles with changed text (measured: frontier rows carry the same ids across v0.3 -> v0.4 while text and status fields changed).
- Verification arm (SVV-adjacent, small): extend tools/concept_span_check.py (already quantizer-aware, :61) or add a 30-line checker: for each law_refs row, the id must exist in the named tier file AND sha8 must match the canonical hash AND compiled must equal compile_report.compiled. Misses are PHANTOM-CITE findings, the ledger twin of the prose citation lint (a05-r2).
- This is structural citation by exact id and hash - the retrieval ladder's deterministic, citable class. The relevance MATCH that selected the row is deterministic token overlap, replayable from the sig string + pack bytes.

### B6. Smallest viable version (what lands first, in order)

1. sense() quantized_lattice block (metadata only, mtime-cached).
2. Quest composer flash rider + law_refs on autonomous_trail rows.
3. ghost_auto recompile arm (WALL or DRIFT, through the sanctioned producer).
4. The 30-line phantom-cite checker + one test file.

Everything else (director, doctor, catalog passthrough, percolation leg) is stage 2 and touches only dormant or additive surfaces. SVV touches two live files (mag/ghost.py, mag/ghost_auto.py) + one tool, all read-only toward the packs.

## (c) Falsifier (one measurable claim a pilot can refute)

CLAIM: once the SVV fold is live, any FKB sig at count >= 10 with >= 20 historical re-fires and no landed diagnosis (the live cohort as of this shift is exactly fkb:amd_window_guard:5c63f4a34186: 182 trail fires, 4,770 failure_kb rows, no memory/runs/ghost/autonomous_fixes/amd_window_guard_5c63f4a34186.md, still spawning 2026-10-04T08:43Z) lands its diagnosis file within its first 3 law-cited spawns.

Pilot: 14 days from fold-live; scoring reads autonomous_trail.jsonl (rows now carry law_refs) and the autonomous_fixes directory. Scoring rule: law_refs that fail the phantom-cite check score as spawns WITHOUT law (the rider must be real bytes to count).

REFUTATION: the pilot ends with any qualifying sig having >= 3 byte-verified law-cited spawns and still no diagnosis file. That outcome means the compiled-law rider did not change quest outcomes - the fold is steering theater, reject it, and spend the effort on the composer's actual gap instead (the diagnosis-landing path, not the law delivery). Secondary integrity kill: if < 95% of recorded law_refs byte-verify, the citation leg itself is broken and the fold is rejected regardless of the resolution claim.

## (d) Explicit non-goals

- NO new decay/staleness constant: PACK_STALE_DAYS stays the one bar (L3 law, tools/thought_quantizer.py:28-31). DRIFT_ROWS is a compile-cadence trigger only.
- NO embeddings or similarity retrieval anywhere in the fold: law rows are fetched by exact id + hash and matched by deterministic token overlap - per the sibling verdict's retrieval-ladder row (semantic recall may exist elsewhere as sensing; it never feeds the ghost's decision path).
- NO auto-promotion of pack rows into AGENTS.md, ribs, or doctrine: promotions stay human/byte-check gates (standing wave law 7; percolator promote-gate alpha-budget, mag/percolator.py:23-27). The fold delivers and cites; it never canonizes.
- NO second lattice or new graph store: mag/invariant_lattice.py owns the lattice views; this fold adds delivery + citation legs on existing organs and existing files. No new jsonl except the tiny ghost_auto recompile log row.
- NO paid spend and NO new model calls: flash riders ride quests that already spawn; the recompile arm is deterministic $0; the director stage-2 change only edits context text of a cadence that already exists.
- NO compile in the sense() hot path: the 60s loop reads mtime-cached metadata only; compiles happen in the ghost_auto cadence.
- NO rewrite of quantizer semantics: weights stay recency x shape, tiers stay disjoint bands, the L4 linker law and L1 refusals stand untouched. Usage-informed weighting is a future operator-gated amendment.
- NO gating of ghost actions on pack state: staleness hides the rider and marks the row; the ghost always acts (a stale law pack must never become a silent no-op loop).
- NOT committing anything: this document lands in the shared inbox only; landing the code is a future seat's build with its own spec-first discipline.

Receipt ends. Instruments: .venv python (counts, ages, hashes over the files named), chunked line reads, grep -r. Plain hyphens only.
