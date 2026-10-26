# misc band 2 — polished (middle third of cluster "misc", 20/58 packs)

Wave: 2026-09-20 burn. Slice = items 20–39 of 58 misc packs, alphabetical by raw path string (same convention as band 1; pupeteer + hermes packs fell in band 1's slice and are polished there).
Source packs: `memory/research_packs/`. Register: `memory/runs/mickey17/digest_rp_*.jsonl`. Repo state re-verified 2026-09-20.
Sub-threads: **M1 deterministic shell & useful-output telemetry** (6) · **M2 instrument the loop: ghost seams + surface telemetry + tesuji folds** (4) · **M3 one process, one surface** (4) · **M4 external-signal digs: SSI contracts, lattice residue, AOS embassy** (6).

## Header table — slice inventory

| Pack (memory/research_packs/) | Register status | Sub-thread |
|---|---|---|
| 20260731T170652Z_deep-c-2fcab987a80f.answer.local.md | DONE (steal landed) | M4 |
| 20260731T171224Z_blast-focus.answer.local.md | STALE (no sources) | M4 |
| 20260731T172429Z_deep-c-2fcab987a80f.answer.local.md | DONE (core landed, increments died) | M4 |
| 20260731T172700Z_deep-c-0b3cacba98e3.answer.local.md | STALE (contradicted by later smoke) | M1 |
| 20260731T173124Z_blast-focus.answer.local.md | STALE (superseded by lattice_loop.py) | M4 |
| 20260802T231123Z_deep-c-2fcab987a80f.answer.local.md | OWED | M4 |
| 20260808T154500Z_warning-signal-classification-research-project.md | OWED (never executed) | M1 |
| 20260808T155500Z_agent-framework-process-organization-research-project.md | OWED (survey done, build not) | M3 |
| 20260808T_mag-shader-system-codify-entire-system.md | OWED (never built) | M3 |
| 20260808T_migrate-dashboard-into-vscode-feed-drainer.md | OWED (spike not built) | M3 |
| 20260808T_session-state-history-protocol-shared-world-state.md | OWED (never built) | M3 |
| 20260809T020241Z_usefulness-oracle-anti-hallucination-tes.answer.remote.md | OWED (verified absent) | M1 |
| 20260809T020307Z_adventurenlearn-aos-partner-research-swa.answer.remote.md | DONE (loop closed 08-21) | M4 |
| 20260809T020632Z_reliable-control-deterministic-layer.answer.local.md | LIVE | M1 |
| 20260809T020632Z_reliable-control-deterministic-layer.answer.remote.md | STALE (dedup of local) | M1 |
| 20260809T031118Z_failure-kb-usefulness-and-remedy-loop.answer.remote.md | OWED (verified absent) | M1 |
| 20260809T112359Z_ghost-agent-improve-test-nested-env-frontier.answer.remote.md | OWED → TASKS fix LANDED 09-20 | M2 |
| 20260809T113230Z_ghost-contained-director-grok-handoff-plans.answer.remote.md | OWED (R2 landed via sibling) | M2 |
| 20260809T_surface-display-and-tracking-research.md | LIVE (Hub built; T1/T3/T4 open) | M2 |
| 20260809T_ux-tips-best-most-useful-research.md | LIVE | M2 |

---

## M1 · Deterministic shell & useful-output telemetry (6 packs)

**Essence.** One doctrine, four failed instrumentation attempts. The doctrine (reliable-control, local variant): reliability is boundary discipline, not model property — make deterministic everything expressible as a state machine or byte comparison; leave the model only the open-ended next-choice, narrowed. The four packs that tried to instrument "pass ≠ useful" (usefulness oracle, failure_kb extension, warning classification, data_integrity_check step) are all still unimplemented — the doctrine governs, its telemetry does not exist yet.

**Merged findings, with receipts.**
- The four concentric layers L0–L4: shrink-the-band (frozen prefix, tool-graph restrict) → verification gates → typed control channel (note/veto/cancel/approve/pause/resume) → persistent operator model. Rule: control signals operate on the deterministic layer; prose injection is a probabilistic nudge (`20260809T020632Z` local).
- Typed-vs-prose, concrete: prose "stop" survives only if a regex classifies it AND the model complies AND the process honors it; a typed `pause` is a job_floor state transition any observer can verify in `jobs.json`. Three properties: mappable, verifiable, non-blocking ("no operator answer" is a first-class path via approval timeouts that fall to autonomous) (same pack).
- Oracle strength ranking (strongest first): byte-verify/sha256 > invariant > golden-output > property/type > self-consistency > verifier-model > LLM-judge. Honest limit: byte-verify proves state, never semantic correctness; a green result means "the deterministic contract held" (`20260809T020632Z` local §3). The usefulness-oracle pack restates it as: never let "no exception" be the assertion — every assertion must reference something outside the function's own return (`20260809T020241Z`).
- Three-tier verdict PASS_USEFUL / PASS_EMPTY / FAIL with a `usefulness_oracle` decorator reusing `answer_grounded_in_pack` + `spec_gate.check`; deterministic oracles for truth, LLM-judge only for quality, only with a different model + explicit rubric (`20260809T020241Z`).
- failure_kb extension: `detect_useless_output(text, turn_mutated, tool_calls, spec_hint)` → useful/empty/low_content/false_success/no_mutating_tool/spec_mismatch, logged via existing `log_failure(kind="useless_output")` so each sub-verdict gets its own signature and auto-drafted remedy; remedy fold computes rate_before vs rate_after, effective when recurrence drops ≥50% — turns the remedy diary into case law. Key economy: log only the negative; `pass_with_useful` is the absence of a useless_output event (`20260809T031118Z`, full diff in pack §5).
- Warning classification brief: the loudest monitor theme ("refused: tier T1 cannot use remote deepseek") is ambiguous between routing bug and correct policy enforcement; classify before fixing — tag bug/expected/retry_noise/false_positive, never widen the regex, precision is the metric (`20260808T154500Z`).
- Earliest instance of the same move: add a `data_integrity_check` auditor step after `critic_risk` so data quality is gated, not assumed from task completion (`20260731T172700Z`).
- Live TOCTOU evidence folded in: `operator_inbox.json` showed the same guidance committed 5+ times by concurrent seats past the `pending_n==0` guard; typed `note` with an idempotency key (sha256 of intent class + payload) dedups deterministically where exact-text prose dedup is fragile (`20260809T020632Z` local §4).

**Verified vs owed.**
- Verified live: `mag/spec_gate.py`, `mag/job_floor.py`, `mag/governor.py` all exist (L0–L2 of the doctrine); TOCTOU dedup guard landed in `commit_guidance` (register); `operator_inbox` still classifies prose by regex — `_VETO_PAUSE`/`_VAGUE` at `mag/operator_inbox.py:33,44` (grep 09-20) — so the L3/L4 gap is open exactly as the pack says.
- Verified absent (grep 09-20): `mag/usefulness_oracle.py` and `tests/test_usefulness_oracle.py`; `detect_useless_output`/`remedy_drafted_at` 0 hits in `mag/failure_kb.py` and 0 useless_output rows in `logs/failure_kb.jsonl` (register); `memory/runs/warning_monitor/classifications.jsonl` — the whole directory does not exist, the classification research never ran; `data_integrity_check` 0 hits anywhere; `configs/selftest/multi_smoke_fixture.txt` exists but contains zero failure/negative cases.
- Dedup: the 28-line remote sibling adds nothing beyond its local twin — archive candidate (register verdict confirmed).

**Next actions.**
1. Land `detect_useless_output` in `mag/failure_kb.py` + the end-of-turn call site in `agent_cli.py` (pack `20260809T031118Z` §5 is a ready diff) — it subsumes the data_integrity_check idea and gives the three-way telemetry split.
2. Run the warning classification as a half-day deterministic pass (group 20 sigs, tag 4 classes, trace the three T1/deepseek tasks) — the brief's method needs no LLM and no new infra.
3. Replace the `_VETO_PAUSE`/`_VAGUE` regex with the typed vocabulary `note|veto|cancel|approve|pause|resume` mapped to job_floor transitions, keeping prose as the nudge channel — the doctrine's L3 gap.

---

## M2 · Instrument the loop: ghost seams, surface telemetry, tesuji folds (4 packs)

**Essence.** The 2026-08-09 audit wave (ghost audit + surface audit + UX synthesis) converged on one gap: nothing compounds because measurement is untrusted (untested experiment runners) and incomplete (no operator-correction loop, no surface-usage telemetry, no confidence honesty). Two pre-scope packs distilled the ghost fixes to $0 deterministic facts; the surface/UX packs ranked what to track; one fix already landed.

**Merged findings, with receipts.**
- Ghost audit facts, pre-resolved so a frontier call only buys judgment: `run_designed_experiment` referenced `TASKS.keys()` at two sites with no `TASKS` defined (guaranteed NameError on any non-dry designed experiment); 1-line fix `TASKS = {kind: i for i, (_p, kind) in enumerate(GUINEA_TASKS)}`; plus a 4-seam deterministic test plan (~17 tests, zero live models): monkeypatch the model boundary for runners, FastAPI TestClient for REST/SSE, extract loop bodies for async loops, pure-function tests for PIPE 1/3/6 (`20260809T112359Z` §3).
- Sibling pre-scope adds: naming gap (`sense_verkle`/`match_context`/`deploy_contextual` documented in loops_registry, don't exist — real path is `sense()`/`match_vector()`/`deploy()`); `MAG_CONTAINER=1` set in docker-compose but zero code branches on it — containment is comment-aspiration, ghost runs identically native vs contained; `match_vector` is keyword-overlap, not semantic (settled fact, upgrade is open design) (`20260809T113230Z` §0).
- Surface-audit tracking gaps ranked: T1 operator-correction feedback loop (edits/redirects/`steer !cmd` → behavioral_events → cluster ≥3 → propose skill → promote) is "the biggest missing linkage"; T3 surface-usage telemetry (which of CLI/REST/ext/dashboard/cast actually get used → retire dead launchers); T4 answer confidence/provenance honesty (report null/unknown, never fabricate — ollama pattern) (`20260809T_surface-display`, §2).
- Ten stealable display/tracking patterns from the 11 cloned repos; standout: learn→gate→promote skill loop (ollama-agent-harness: candidate queue + thresholds + durable promotion) and flock's queryable DuckDB trace store with parent_id span trees (same pack §3).
- UX synthesis: six habits — minimal functioning core + finish-discipline (the existential threat is accumulation without a working whole), define primitives at creation, route to cheapest capable tier, verify by bytes not self-report, transparency (show planning steps), poka-yoke tools (Anthropic's absolute-path file-edit example). Workflows ≠ agents: spend agents only where flexibility pays (`20260809T_ux-tips` Parts B–C).

**Verified vs owed.**
- Verified LANDED 09-20: the TASKS fix is in `mag/ghost.py:2910-2912` with a comment crediting "the Mickey 17 digestion (two packs pre-resolved this)" — this slice's two pre-scope packs directly caused the fix. Use sites at :3944/:3962 now resolve.
- Verified built: Surface Hub — `mag/surface_audit.py` + `GET /api/v1/surface-audit` route (grep 09-20); skill_ledger at 3308 rows (vs 221 at pack-write time).
- Verified still open (grep 09-20): `sense_verkle`/`match_context`/`deploy_contextual` 0 hits in `mag/ghost.py`; `MAG_CONTAINER` 0 hits; no `surface_used` event kind anywhere in `mag/`; the ~17-test plan unimplemented (register: runners/daemon/loops still untested); the ≥3× tesuji tips (false-success-verify, wrong-offset-gate, penny-designation, loop-escalate, seam-placement) not yet folded into pro_library; both grok elevation calls never made (one died HTTP 403).

**Next actions.**
1. Add the `containment` key to `sense()` reading `MAG_CONTAINER` + `/proc/1/cgroup` and gate at least one behavior on it (R4, $0) — closes the "comment-aspiration" boundary gap.
2. Alias `sense_verkle`/`match_context`/`deploy_contextual` to the real functions or fix loops_registry — ship == doc (R1, $0).
3. Ship T1 (operator-correction → behavioral_events → cluster → promote) — it is the same learn→gate→promote shape the ghost COMPOUND phase and the UX pack both call the biggest missing linkage.

---

## M3 · One process, one surface (4 packs)

**Essence.** Four 2026-08-08 design packs attacking the same disease from different flanks — sprawl. Terminal sprawl (9 python tabs), surface sprawl (dashboard vs IDE vs tablet), module sprawl (~10 overlapping state readers), and data sprawl (raw user data vs shareable world). None was built; the diagnoses still hold and cross-validate each other.

**Merged findings, with receipts.**
- Process: surveyed 11 steal-protocol repos → 5 hosting patterns (P1 single supervisor with asyncio tasks; P2 supervisor-spawns-workers; P3 compose; P4 CLI+`serve`; P5 headless+reattach-viewer). General signal: none of AutoGen/LangGraph/CrewAI/MetaGPT requires one terminal per agent — terminal sprawl is a packaging failure, not an architecture requirement. Recommendation: P1 supervisor hosting dashboard+governor+drainer+ghost+overseer as togglable asyncio tasks with `POST /api/v1/loop/{name}/start|stop`, then P5 (Control Room = pure viewer), compose last (`20260808T155500Z` §3–4).
- Surface: the :8765 dashboard is a thin client over 300+ REST routes, so IDE migration is a front-end re-skin with zero backend change. Ranking rule: control surfaces (Direct Mag, runs&seats, agents) earn the IDE first, read-only monitors second, novelty (3D tapestry) last. RQ3's split: VS Code = full control, browser control.html stays as tablet/remote thin client. CSP warning is load-bearing — no CDN scripts in webviews (`20260808T_migrate-dashboard`).
- Module: the RenderMan mapping — RIB = `configs/system.yaml` (scene spec), shader = pure `fn(state) -> {action, outcome}` per subsystem, PBR = one unified move format, renderer = dumb executor. Dedup payoff: `session_state_brief` + `context_pack` + `system-map` become three render() shaders over one `sense()` instead of three bespoke state readers. Guard: `render_audit.py` compares declared yaml signatures vs actual function signatures — trust bytes; RQ2 (is the RIB authoritative or a drifting mirror?) is the right first question for any registry-of-record (`20260808T_mag-shader-system`).
- Data: the Session State History Protocol — auto-file an encoded, verkle-anchored session brief into a shared scratch world (anagram/archetype/room encoding from the D&D campaign template); the verkle tip is the world address; models reason in-world by roleplay without seeing raw data; mapping key never leaves the machine. Honest limits stated in-pack: does not protect against an adversary holding the key, over-specific content, or the live chat itself; RQ4 even challenges the "without awareness" framing (consented roleplay may be safer) (`20260808T_session-state-history` §6–7).

**Verified vs owed.**
- Verified absent (09-20): `POST /api/v1/loop/{name}/start|stop` routes — only `GET /api/v1/loop/health` exists (`dashboard/rest.py:5097`); `mag/supervisor.py` is the pre-existing governor slow-think supervisor, not a process host (register); `configs/system.yaml`, `mag/shader_lib.py`, `tools/render_audit.py` all absent — no audit tool exists, so the overlapping-state-readers problem has no counter-evidence of being solved another way; `mag/session_state_protocol.py`, `memory/shared_scratch/`, `configs/world.yaml` all absent, and the campaign_codec dependency (pack #74) is also unbuilt.
- Partial base: vscode-mag-map has read-only `control_room.js` + `mag_views.js` and an actively maintained extension.js, but no `direct.js`/`ideas.js`/`history.js` and no enqueue capability — success criterion 1 (file goal from IDE → drainer) unmet (register).

**Next actions.**
1. Smallest real step toward P1: add `POST /api/v1/loop/{name}/start|stop` for the drainer only (it already owns the queue it drains), then fold governor/ghost in the order the RQ1 collapse-order question decides.
2. Build the `render_audit.py` half of the shader system first (it needs no yaml authority decision): list modules that read the same state files — it produces the dedup target list even if the RIB never becomes authoritative.
3. De-scale SSHP to its cheapest testable core: `file_brief()` wired into the existing `session_end_hook` with the zero-raw-name-token automated check — deferring the roleplay/awareness questions until encoding fidelity (RQ1/RQ3) is measured.

---

## M4 · External-signal digs: SSI contracts, lattice residue, AOS embassy (6 packs)

**Essence.** Three external-signal programs. The SSI/Ilya dig (3 re-fires of the same extraction) produced one durable, landed steal — skill beads as merge-free learning. The blast-focus lattice residue (2 packs) produced nothing grounded and is superseded by the live instrument. The AOS partner research is the only fully closed loop in the slice.

**Merged findings, with receipts.**
- SSI process contracts (stable across all three re-fires): the bottleneck claim is generalization/sample efficiency, not scale; failure modes are "jagged" (bug fix introduces new bug, loops); "emotions ≈ value function" → a mid-trajectory critic that short-circuits bad paths before full rollouts; continual learning = accumulating discrete portable skill beads without weight merges (FIND→FILE→LOAD); refuse architecture reverse-engineering, weight-pulling, and any undisclosed "missing principle" (`20260731T170652Z`, `20260731T172429Z`, `20260802T231123Z`).
- Unique increments per re-fire: #172429 adds DRO (chi-squared/CVaR via Levy/Carmon) as a verifiable public contract + a jagged-failure test library; #231123 adds HYPOTHESIS_FILE.md quarantine (speculative breakthroughs flagged so they never pollute operational logic); #170652 adds the orphan-branch quarantine move (`git checkout --orphan hypothesis_contracts/p0_process_map`) — never executed among 77 branches (register).
- Blast-focus residue: capture via "residual saturation of adjacent failure points" + narrative overload exhausting critical-attention capacity; the steal is the pattern of selective omission, not the omitted content; both packs admit zero external sources and purely theoretical analysis; the recommended next move (hunt a shared financial intermediary between `layer_ms13_claim` and `core_rope` "within the last 18 months") is unfalsifiable OSINT speculation with no data (`20260731T171224Z`, `20260731T173124Z`). Register verdict: superseded by `mag/lattice_loop.py`, which runs full dig cycles with Verkle beads.
- AOS/AdventureNLearn: solo anti-capture builder whose system (ARK/LPIN: tri-state claims, evidence supremacy, Gate 6 symmetry audit, Gate 7 adversarial stress test, Phoenix self-correction, G1–G8 OPSEC) is "the same skeleton grown independently" as Ghost — one-to-one alignment table in-pack (ARK Gate 6 ↔ symmetry_audit, Phoenix ↔ failure_kb+improve_loop, anti-self-report ↔ false-success guard). The embassy move: hand a runnable, forkable, deterministic test suite (21 passing tests) mapping onto gates he already coded, framed as extension of ARK/LPIN never replacement; speak his register (the Frog Letter). Timeline verified closed: §6 packet received 08-09 → OPSEC HOLD → delta returned, loop closed 08-21 (`memory/embassy/AOS/EMBASSY-REPLY-CLOSE-2026-08-21.md`, exists on disk).
- Cross-pack note: the one transferable warning-classification lesson from the blast-focus pair — stacked high-impact claims function as attention-exhaustion attacks — is a pack-first reminder, not evidence.

**Verified vs owed.**
- Verified landed: `write_skill_bead` (SCHEMA mag_skill_bead.v1) in `ijl_core.py` + mid-critic in `agents/critic.py` + `memory/improve/pins/skills/` populated with bead files (grep 09-20 confirms all three).
- Verified dead: DRO/CVaR has no code trace; the jagged-failure library edit targeted `memory/research_packs/2026-07-28.md` which does not exist — both increments died with the mispathed file (register); `feature_compose_contract_v1.md` (from #231123) never created; HYPOTHESIS_FILE quarantine unexecuted.
- Owed (still worth it): the HYPOTHESIS_FILE quarantine pattern is cheap and doctrine-compatible — speculative packs flagged and quarantined from operational logic.

**Next actions.**
1. Fold the "jagged failure test case library" into the existing test tree instead of the dead research-pack path: 3 non-linear multi-step fixtures where success requires noticing that a fix introduced a new bug.
2. Adopt HYPOTHESIS_FILE.md quarantine (from #231123) as the standard filing for speculative-contract packs — one file, one convention, zero infra.
3. Treat AOS as the reusable embassy template: the anti-pitch pattern (runnable deterministic suite mapped to the partner's own gates, extension-never-replacement framing) is the protocol for any future partner contact.

---

*Polished 2026-09-20 · band 2 of 3 · companion: `misc_band1.md` (slice overlap: pupeteer + hermes polished there). All "verified" marks re-checked against the repo this date; register rows from `memory/runs/mickey17/digest_rp_*.jsonl`.*
