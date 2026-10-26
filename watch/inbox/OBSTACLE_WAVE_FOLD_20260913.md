# OBSTACLE WAVE FOLD — 12/12 (2026-09-13, the resonance experiment)

**Wave receipt:** 12 lanes through the probe-before-route gate — 84.6s wall, ~$0.01 (deepseek ×1, rest free lanes). **Gate verdict (PROBE_LOG.json, the dogfood receipt): stepfun + solar correctly EXCLUDED (HTTP 400 — the known-dead slugs stayed dead, zero lanes burned); ling-sante + ling-fin FALSE-excluded** — the probe asked for 16 max_tokens and thinking models returned empty content, the glm-5.3 lesson at probe scale. Fix named below; the fallback chain absorbed it (6 lanes auto-rerouted to longcat, zero losses). Intake card: watch/RESONANCE_INTAKE_20260913.md. Pack + returns: memory/runs/obstacle_wave/.

## THE DOCTRINE (the experiment's answer)

**The fleet already moves its huge obstacles by resonance — it just never had the name.** Cache-mining pumped 68.1M of 75.4M tokens through glm-4.5-air for $4.38 (90% of the load moved by a trace, not by force) — that is the crane's 20x, already banked. The wave cadence (burst, then sanctioned idle) is pump-and-catch. Tesuji is small stones instead of fighting the board. The stigmergy the strangers taught is the doctrine the fleet went public with in August. What was missing: the named deadlifts and the failure detectors. The wave named both.

## THE SELF-STEALS (all three landed)

1. **Socratic tease-out applied** (L01): the question chain on "resonance not force," five questions, each receipt-answerable, four-tagged — verdict: the doctrine is BUILT-NOT-SAID (cache stats prove it, no card named it until today).
2. **The 72-step written down** (L02): 7 macro-stages × ~10 micro-steps as a state machine — INGEST→MAP→ASSERT→ATTACK→MEASURE→CORRECT→CROP from the existing corpus genome; **Step 0 = probe-before-route gate, Step 72 = DISPOSITIONS write**; falsifier: a paste reaching Step 72 with OPEN-WIRE and no CORRECT loop invalidates the spec. L10's amendment stands: extract steps 1-2 executable, leave the other 70 as the anchor — building the monolith first would be the deadlift.
3. **Purple harvest scoring applied** (L03): crane MATH 9 / ORGAN 7 / SPECIMEN 8 → ROUTE: BUILD small (a pendulum sim replicating the 20x is the one build this intake earns); anchor = doctrine card; stigmergy = doctrine + SHELF the dupe; listicle + rumor = specimen tags; Swift-Qwen = library lane pending receipt. Verdict: this intake is mid-band except the crane — the purple harvest itself was edge-of-band.

## THE FIX (dogfooded) AND ITS GENERALIZATION (L12)

**PROBE-BEFORE-ROUTE as a 4-file organ:** `probe.py` (minimal payload per slug) + `ttl.json` (default 6h — free-lane availability flips provider-side, the 09-12→09-13 flip proves 7d is too long) + `route.py` (live slugs only, dead slugs to exceptions.log) + `probe_log.schema.json` ({ts, slug, payload_hash, http_status, latency_ms, verdict: live|dead|flaky, ttl_expires}).
**Amendment from today's run:** probe max_tokens must be ≥512 (or retry once on empty content) — thinking models return None at 16, and a gate that false-kills live slugs is just a quieter deadlift.
**The generalized failure class:** LISTING ≠ SERVABLE. Same gate, three more doors: mirror resume guard (resume ≠ upstream unchanged), cite-gate fetch door (cite ≠ URL alive), healthz semantics (200 ≠ serving). One gate shape, domain-specific probe payloads.

## THE DEADLIFT INVENTORY (L04 + L10, with primitives assigned)

| obstacle | primitive | next step (no deadlifts) |
|---|---|---|
| 480 fold owed to Matthew | pump at frequency | micro-deliverables on the obligation's rhythm, not one grind |
| mint waiting on consents | pivot | pre-staged config stays; rotate when the gate opens — force is useless on a stuck gate |
| engram build | counterweight | existing receipts (chain knots, fold cards) balance the load; no fresh lift |
| migration | CATCH first | build the destination validation script BEFORE pumping any load across |
| the 72-step organ | ANCHOR, not obstacle | steps 1-2 executable now; the monolith never |

## FAILURE MODES + DETECTORS (L11 — the wave's warning label)

1. **Thrust-brake** (success that cheats the force budget): today's 6-lane burn was exactly this — output produced, quota and attention overspent. Detector: the probe gate.
2. **Anti-resonance** (pumping at the wrong frequency): cache-mining without a rubric pass-rate amplifies noise. Detector: cache-output rubric pass-rate.
3. **Phase cancellation** (overthinking loops — the Swift-Qwen lens): re-derivation after verdict. Detector: verdict-lock (L07) — post-CROP re-derivation of the same artifact gets terminated. Falsifier: if verdict-lock kills a third sweep that would have surfaced a hidden falsifier, it breaks necessary resonance.
4. **Resonant buildup** (stigmergy without decay — noise amplified): sponsored/rumor specimens accumulating as if they were ore. Detectors: L09's SOURCE CHECK rubric row + trace-decay check.
5. **The open loop** (L08): hourly canary senses drift but has no actuator — wire score to lane circuit-breaker. Falsifier: degrade a model deliberately; breaker must trip within one cadence cycle.

**Falsifier for the whole doctrine (L04):** if the cache-read ratio on the next mining receipt falls below 50%, the "natural frequency" story is brute force in disguise and this card gets amended.

**Cost of the whole experiment:** ~$0.01 + one paste. The obstacle moved anyway.
