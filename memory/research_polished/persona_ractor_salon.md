# POLISHED — cluster `persona_ractor_salon`
Wave: 2026-09-20 burn · Seat: polish agent · Sources: 17 packs (rp_clusters.json) + register rows (digest_rp_05/06/07/10/15) + full pack reads + independent repo spot-checks (2026-09-20, marked ✅chk).

---

## 1 · Thread essence

**How to steer — and when to trust — stochastic models, from the seam outward.** The cluster runs one spine through every pack: **deterministic spec → stochastic execution → deterministic audit** (steiniger §7, renderman §2, verkle report §3). Out of that spine the thread develops four faces:

1. **The puppeteer seam** (operator_inbox): steering works, is measurable, and is size-dependent — low models DO, high models DETECT (quiet-forge, tournament, puppet-toolbox, powershell gauntlet).
2. **The render doctrine**: spend on the spec (RIB), not the tier — "design needs HIGH" was falsified by probe (renderman §4).
3. **The operator authority + truth-provenance gaps**: the seam has no signed guidance, no intent classifier, no persona-theater detector, no provenance channels — the same holes the pack's own gauntlet proved exploitable (operator-input-authority, puppet-toolbox H1–H15, verifiable-vs-asserted).
4. **The typed-decision endgame** (Jev/SemIf, THE50 W3 T11): decisions become typed reads (CHOICE/SCORE/NOUL) with published literature under them — the steering question formalized as oracle calibration.

Latinate name is lexical (salon.com URL in lattice-url-5; persona-theater packs), not thematic. lattice-url-5 and bench-flock are peripherals folded in here.

---

## 2 · Merged findings (deduplicated, receipts-first)

### F1 · Obedience–silence tradeoff is near-linear with model size; no model is both obedient and silent
- 165 experiments, 6 models × 7 vectors, $0 local, ~8h. 32B: obey 0.62, leaks 46%. 2B: obey 0.37, silent 85%. 3B "noisy puppet": obey 0.75, silent 50%. **`escalate` is the only universal vector** (1.00 obedience on 3B/7B/32B, 0/5 silent everywhere).
- **Intent AMPLIFIES across cascade hops** (3B→7B→2B sim 0.000→0.083→0.167), not attenuates.
- Receipts: `20260808T_tournament-results-obedience-silence-tradeoff.md`; data ✅chk `memory/runs/tournament/` (9 files incl. R1–R4 × 2 runs + manifest).
- Folded to code ✅chk: `mag/ghost.py:3370-3375` (escalate/penny seed vectors, tournament tags), `mag/ghost.py:2651-2661` (model-size boost: +8 escalate/penny for large, +6 wrong for 2B).

### F2 · Low models DO, high models DETECT — the thought-disconnect is a routing signal, but the instrument never recorded
- Design: obey_score at executor tier vs detect_score at critic tier; map-is-territory (room description = tic-tac-toe spec). Dry-run validated (campaign-23830bda1792); one real run (campaign-7621cf286726: 2 steers deployed, 1 detected, 0 resisted).
- **Unrecorded**: 0 `thought_disconnect` hits in `memory/runs/campaign/measurements.jsonl` (✅chk today), party_actions empty, artifact-capture adapter (compile + unit-test scribe's tic_tac_toe.py) never built → RQ1–RQ5 unanswered.
- Receipts: `20260808T163000Z_quiet-forge-thought-disconnect-swarm-experiment.md`; echoed in puppet-toolbox §4.1 (route exec to cheap+seams, review to high) and pipeline topic 3.

### F3 · Flip is conditional on weak priors — the gauntlet's B5 boundary confirmed by a clean NULL
- PowerShell fault split E1 (stray hermes venv python, no pytest) vs E2 (cp1252 mojibake): probes E+U, control 1.00 vs puppeteer 1.00, Δ 0.00, 0/5 flips, both arms silent — **because the correct fix was visible in the options**. A 3B solves it unaided; steering pays only on hidden or strong-prior-contradicting choices.
- Real yield = method: never accept "I fixed it" — run the candidate (`_run_passes`: exit 0 + "passed") or byte-diff (`E2 80 94`); two harness bugs fixed en route (rstrip `b"\r\n"` on Windows; force "answer with just the option letter").
- Receipts: `20260808T_powershell-error-ghost-puppeteer-research-project.md` §9; ✅chk `memory/runs/pupeteer/20260808T130440Z/REPORT.md` + `raw.json` exist.

### F4 · "Render, don't predict" — the spec is the product, tier is the last lever
- Tier A/B falsified "design needs HIGH": design task flash-off 1.00 (10 concrete cmds) vs pro+thinking 0.70 (0 concrete cmds) at ~18.7× lower cost; exec 1.00/1.00. Doctrine: spend on the RIB; sample cheap + filter with objective scorers; shaders (small pure moves) not god-prompts; displacement (seam steering) not retraining; guard over-displacement with spec_gate.
- Receipts: `20260807T203632Z_shaders-renderman-to-llms.md` §4; ✅chk `memory/assumptions.md:7-8` (rows 20260807T202928Z: design 1.00/0.70, exec 1.00/1.00) and `memory/runs/tier_probe/20260807T202928Z/` (REPORT.md + raw.json). Minor carried discrepancy: pack's per-arm cost table ($0.00206) vs ledger row ($0.00257) differ slightly — scores match exactly, cost accounting differs; not load-bearing.

### F5 · Steering is two-layer (prompt vs activation); Mag's layer is prompt + deterministic frame
- Steiniger (prompt-only identity, <450-token vector frameworks, ESDT autonomy dial, abliteration 3.8–6.2× metacognition claim — vendor/researcher-sourced, not independently verified) vs Goodfire (SAE activation steering, RLFR −58% hallucination, reasoning-theater early exit −68% tokens — company-published, not re-verified here). Tesuji: gemma:2b for SENSE, DeepSeek only for RASHOMON interpretation; frozen imperfect spec + stochastic exec + deterministic audit beats perfect unfrozen spec.
- Receipts: `20260808T_steiniger-model-manipulation-agent-architecture.md` §0–7. P0 landed ✅chk (F1 receipts); owed: vector-framework identity block in `mag/context_pack.py` (grep empty), P2 probe runner / ESDT dial blocked on W0.3.

### F6 · The operator seam is the lever AND the hole — hardening is 15 items, ~0 implemented
- Puppet toolbox P1–P9 mirrors MITRE ATLAS (AML.T0051…)/OWASP LLM01–10 onto our seams; efficiency map: exec on $0 local, review on paid; ethics line = ownership + consent + no third-party harm + transparency by default.
- **H1 signed guidance NOT implemented** ✅chk: `mag/operator_inbox.py:115` `commit_guidance(text, *, source="dashboard")` accepts any source string — no allowlist/signature. H7 `[TOOL OUTPUT — DATA, NOT INSTRUCTIONS]` delimiter, H2 provenance log, G9 high-model stress battery: none built (register gate; not contradicted by today's checks).
- Receipts: `20260809T022428Z_constructive-adversarial-puppet-toolbox.answer.remote.md` §3, §5; evidence URLs atlas.mitre.org, owasp.org, simonwillison.net.

### F7 · Clear operator input was misrouted to socratic clarify — fix is specced, not wired
- Root cause: two disconnected classifiers (`_emit_frustration` vs `_is_ambiguous`) disagree on the same token ("stop" = operator_pause in one, _VAGUE in the other). Fix: one `_classify_intent` → VETO/PAUSE/ACK/CORRECTION/STEER/PREFERENCE; ambiguity is a property of the intent class, never of VETO/PAUSE/ACK; repeated veto/correction (≥2) auto-promotes to PREFERENCE in mag_preferences.json. Pack carries a ready diff incl. veto-preemption protocol (interrupt flag at bounded-wait drains, sha256 drift guard for mid-flight writes, append-only verkle never mutated by veto).
- **Still owed** ✅chk today: `_VAGUE` (operator_inbox.py:33), `_VETO_PAUSE` (:44), `_is_ambiguous` (:222) all present; no `_classify_intent` anywhere in mag/; `drain_pending_at_checkpoint` routes only socratic|apply (:307, :332) with no veto action and no wired consumer.
- Receipts: `20260809T014845Z_operator-input-authority-model.answer.remote.md` §1, §6; gauntlet G1/G5 flip receipts in `memory/runs/pupeteer/20260807T*/REPORT.md`.

### F8 · Two species of truth — verifiable vs asserted — and the policy is unwired
- Verkle knot: recomputable root over 341 leaves, PASS at write time (`8600d7ee…`, gauntlet-run receipt in pack). #aiTruthCode: 79 pseudo-Python persona-theater docs (Chris Beck/"Kuwbiyahu"), authority = persuasion, "verification theater," nothing computes. Rule: a mirror survives recomputation, a puppet survives only affirmation; asserted content quarantined, never folded into the verkle layer; fail-closed ingest (untagged = unverified = excluded).
- **Owed** ✅chk: no persona-theater detector module in tools/ or mag/ (grep hits are prose mentions in checkin_route.py / local_usable.py only); `mag/verkle_knot.py` write path carries no asserted/verified provenance tags (its "verified" is the chain-integrity gate, :515/:533/:613 — different thing); two-channel rule unwired.
- Receipts: `20260809_verkle_vs_aitruthcode_report.md`; `20260809T024658Z_verifiable-vs-asserted-truth-provenance.answer.remote.md` §3–5; corpus `research/aiTruthCode/` (git-ignored).

### F9 · Typed-decision oracles: the Jev line sits on published canon; vendor claims partially unverified
- 17 sources, every arXiv ID verified by direct abstract fetch this ask; **caught 2405.13927 wrong → 2405.21047** (Grammar-Aligned Decoding). Lineage: Kadavath P(True) → NOUL; Holtzman PMI normalization → why fat CHOICEs bleed mass (matches the receipt's 50-point decomposed-Nouls ablation); Outlines FSM → the SemIf build path; RouteLLM/FrugalGPT → cascade economics; conformal (2305.18404) → replace eyeballed tau gates. Compiler rule: any Choice >4 options → fan-out Nouls aggregated by deterministic code. Vendor "RLCD" = name collision with a real-but-different paper (2307.12950, contrastive distillation).
- Fleet-internal numbers receipt-sourced, not re-verified: SemIf 0.845 vs Jev 0.883 (3pp sovereignty threshold), openjev-sglang prefill-only endpoint → A/B is a base-URL swap behind the lane runner. TechCrunch origin story unverified.
- Receipts: `THE50_W3_T11_TYPED_DECISION_ORACLES.md` (sources 1–17 + "explicitly not verified"); `watch/inbox/JEV_CONSOLIDATED_BRIEF_20260919.md`, `JEV_CHORD_FORMALIZED_20260919.md` (receipt-sourced).

### F10 · Swarm steering absorbed as a field; map precedes territory adopted in live code
- flock_field: agents as particles in a multivector field, steer = −∇φ + boid terms, rotors, belt-trick undeform before hash; convergence_cost = (agent-steps × avg|F|)/success_rate; guardrails (stochastic kick, rotor renorm, clamped force, lipschitz abort). ✅chk all five modules exist (`mag/flock_{field,grid,job,scheduler,shader}.py`).
- "Map precedes territory": instruction-first cost inversion; map-correctness becomes the #1 gate (re-derivable, content-addressed, revertible; lying map worse than no map). Verified adopted in live code: `mag/agent_knot.py:73`, `mag/cache_shard.py:16,103`, `mag/atlas.py:46`, docs FRONTIER_PROMPT_V1/THE_OS_THESIS/STACK_V1 (register gate). Carried: the lens doc `memory/repo/operational-lens-map-precedes-territory-20260811.md` is MISSING from the tree.
- Receipts: `deep_research_flocking_ga.answer.remote.md`; `steal_deep_research_adoption_map_precedes_territory_20260811.answer.remote.md`.

### F11 · Peripherals (in-cluster but small)
- **Wearable swarm control** — built and ✅chk: `mag/wearable_swarm.py`, `dashboard/static/wearable.html`, cast routes `/wearable` + `/api/v1/wearable/{surface,command}` (`mag/cast_server.py:34-46`). Pattern: sync awareness vs async action over the same queue; no new runtime.
- **Titor RIB attractor spec** — honest shape-steal (fiction → attractor field): modules all exist ✅chk (`castle_foundation.py`, `attractor_tools.py`, `roshomon.py`, `worldline_seed.py`, `divergence_meter.py`) but no assembled end-to-end pipeline; Roshomon surviving core = convergent worldline is the destination concept.
- **Grok-swarm ping-pong pipeline** — OWED: paper.md written, 1/5 topics swarmed, xai read timeout (stage1_error.json), `memory/runs/pipeline/iterations/` EMPTY ✅chk, arm-A-vs-arm-B head-to-head never ran. The 6-stage loop is a reusable scaffold; stage2_run.py runnable.
- **lattice-url-5 (falsifier card)** — direct fetch proved franklinreport.com is a home-services directory; the "Franklin Report Summary"/"sealed-file history" citations in lattice cycles 2–3 are FALSE. The only node in that chain that verified a source against its actual content. Strike the citation if the node is ever revived.
- **bench-flock stub** — consensus "send" strength 0.6 on deniable-steering risk question; stub carries no answer body by design; weak signal, nothing stealable without re-firing the flock.

### Contradictions — resolved or carried
| # | Conflict | Status |
|---|---|---|
| C1 | "Silence is unconditional" (toolbox B6, scoped to 3B) vs tournament "B6 breaks at 32B" | **Resolved**: B6 is size-scoped — holds 2B–7B, breaks at 32B (46% leak). Toolbox P5 guidance inherits the scope. |
| C2 | `operator_escalate` counts: 42×/7× (toolbox) vs 45×/4× (authority pack) vs ghost.py:717 comment "1102 (724 = system escalate_on_loop…)" | **Carried**: different digest windows; and ghost.py's own comment attributes the bulk to system escalate_on_loop, not operator input — the "operator frustration" signal is partly detector artifact (toolbox open Q5 confirms). Dig before acting on it. |
| C3 | Invariant count 37 (flocking pack, seeds φ) vs 36 (distilled_invariants pack, economics cluster) | **Carried**: canonical count must be recounted; flock_field φ seeding depends on it. |
| C4 | Pack §4 costs ($0.00206 design pro arm) vs assumptions.md ledger row ($0.00257) | **Carried, minor**: scores match exactly; cost accounting differs. Use the ledger as canonical. |

---

## 3 · Verified/built vs unverified/owed

**Built / receipt-verified (exist in repo, checked 2026-09-20):**
- escalate/penny seed vectors + model-size boost — `mag/ghost.py:2651-2661, 3370-3375`
- Tournament dataset (165 experiments) — `memory/runs/tournament/` (9 files)
- flock_field absorption — `mag/flock_{field,grid,job,scheduler,shader}.py`
- Wearable command surface — `mag/wearable_swarm.py` + `dashboard/static/wearable.html` + cast routes (`mag/cast_server.py:34-46`)
- Pupeteer E+U gauntlet with deterministic ground truth — `memory/runs/pupeteer/20260808T130440Z/REPORT.md`
- Tier-probe doctrine ledger — `memory/assumptions.md:7-9` + `memory/runs/tier_probe/20260807T202928Z/`
- Map-precedes-territory in live code — `mag/agent_knot.py:73`, `mag/cache_shard.py:16,103`, `mag/atlas.py:46`
- Verkle chain integrity gate (recompute-before-extend) — `mag/verkle_knot.py:515-613`; root PASS receipt (341 leaves, `8600d7ee…`) at pack write time
- Jev/SemIf arXiv lineage (17 IDs incl. the 2405.13927→2405.21047 correction) — verified by direct fetch at pack time
- Titor/worldline modules exist (not assembled) — `mag/{castle_foundation,attractor_tools,roshomon,worldline_seed,divergence_meter}.py`

**Unverified / owed (highest-leverage first):**
1. `_classify_intent` + veto consumer — specced with diff, **absent** (✅chk: `mag/operator_inbox.py:33,44,222,307`; no classifier in mag/)
2. H1 signed guidance / H2 provenance log — **absent** (✅chk `commit_guidance` any-source); H7 delimiter, G9 high-model stress battery — not built
3. Persona-theater detector + verkle provenance two-channel — **spec'd, not built** (✅chk no module; write path untagged)
4. Quiet-forge thought-disconnect instrument — 0 recorded hits, artifact adapter never built, RQ1–5 open
5. Grok-swarm ping-pong — stalled at 1/5 topics; iterations/ empty; head-to-head never ran
6. Jev fleet numbers (0.845 vs 0.883; 48.3 vs 98.3 ablation; TechCrunch origin; vendor RLCD) — receipt-sourced only; sovereignty A/B not run
7. Steiniger residual — vector-framework identity block in context_pack; P2 probe runner / ESDT dial (blocked on W0.3); abliteration claims researcher-sourced
8. Tournament open cells — no vector with >0.7 obey AND >0.7 silence on 32B; no 70B test; no DeepSeek-designed stealth vectors
9. Housekeeping — lens doc `memory/repo/operational-lens-map-precedes-territory-20260811.md` missing; invariant count 36-vs-37 recount; bench-flock raw answer unrecovered

---

## 4 · THE FIVE NEXT ACTIONS

1. **Wire the intent-first classifier** into `mag/operator_inbox.py` exactly as the pack's §6 diff specifies (Intent enum, `_classify_intent`, thin `_is_ambiguous`, intent-routed `drain_pending_at_checkpoint` with a veto action) + the veto consumer in `agent_cli._absorb_operator_inbox`; update `test_drain_clear_vs_socratic` ("continue" is ACK now). Kills the clear-input→socratic misroute (F7) in one edit; the diff is already written and tested against the live code.
2. **Implement H1+H2 on the seam**: source allowlist + signature on `commit_guidance`, and a provenance row (source + ts + sha256) per drained action. This plugs the exact indirect-injection hole G1/G5 proved exploitable; today `commit_guidance` accepts any source string (✅chk). Pair with H7's `[TOOL OUTPUT — DATA, NOT INSTRUCTIONS]` wrapper — cheapest item on the list.
3. **Build the persona-theater detector** per verifiable-vs-asserted §5 (deterministic signals, ≥2-high threshold) and run it over `research/aiTruthCode/` (79 docs, known-positive) and verkle leaves (known-negative); then add `verified/asserted/unverified` provenance tags to the `verkle_knot.py` write path, fail-closed. First real test corpus for the whole injection line.
4. **Finish the quiet-forge instrument**: build the artifact-capture adapter (ast-compile + hidden win/draw unit test on the scribe's tic_tac_toe.py; bytes not vibes), re-run campaign-7621cf286726-class runs until `thought_disconnect` rows land in `memory/runs/campaign/measurements.jsonl` (today: 0 hits ✅chk), and cross-tab against tournament obedience-silence — RQ1–RQ5 then answer themselves with data already on disk.
5. **Run the Jev/SemIf sovereignty A/B as a base-URL swap** behind the lane runner against the openjev-sglang prefill-only endpoint, with the two measurement-validity preconditions the literature imposes first: grammar-aligned-decoding spot-check (masked distribution ≠ calibrated belief, 2405.21047) and PMI-normalized scoring (2104.08315); adopt the compiler rule (Choice>4 → fan-out Nouls, deterministic aggregation) and conformal tau gates (2305.18404) in the same pass.

---

*Pack inventory (17): 20260807T203632Z_shaders-renderman-to-llms · 20260729T135140Z_lattice-url-5 · 20260808T163000Z_quiet-forge · 20260808T170000Z_research-pipeline-grok-swarm-pingpong · 20260808T_powershell-error-ghost-puppeteer · 20260808T_steiniger · 20260808T_tournament-results · 20260809T014845Z_operator-input-authority-model · 20260809T022428Z_constructive-adversarial-puppet-toolbox · 20260809T024658Z_verifiable-vs-asserted-truth-provenance · 20260809_verkle_vs_aitruthcode_report · THE50_W3_T11_TYPED_DECISION_ORACLES · deep_research_flocking_ga · flock_steal_bench-flock_20260810 · steal_deep_research_adoption_map_precedes_territory_20260811 · steal_wearable_swarm_control_20260811 · titor-rib-attractor-spec*
