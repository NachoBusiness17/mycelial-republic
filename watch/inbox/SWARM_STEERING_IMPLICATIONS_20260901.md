# SWARM STEERING — HISTORY DIGEST + IMPLICATIONS (2026-09-01 03:45Z)
**Writer:** rnd_advisor (main seat, on operator request) · **Inputs:** STEERING_LINEAGE, STEERING_SYNTHESIS, SWARM_DOCTRINE, OPS_RESEARCH_001, HOT_JURY_F1F2, steer_exp_001_receipts.jsonl (12 rows), FLEET_STRUCTURE, LANE_SLOT_MAP · Digest child receipt: worker session c549a5f4.

## WHAT THE HISTORY ACTUALLY SAYS (receipt-backed, /mag/memory/runs/)
- **steer_compare** (08-08, 40 files, TESTED): 6 models × baseline/escalate/loop, leak/flip/emergent scoring.
- **gap_swarm_experiment** (08-10, design + 5 probes): gap→escalate gate designed — **the loop that never closed**.
- **steer_router/pins.json** (08-10/15): DORMANT, empty `[]`.
- **seat_steer** (08-14→31, 84 files): STEER blocks compiled into seat prompts; seat activity collapsed 59 files/day → single digits within days.
- **Why it dormed:** ① surface died at the browser layer (`playwright not installed on host`, CDP socket hang-up); ② cost (grok cap 36 vs 20, "grok/chatgpt scarce"); ③ verkle O(n²) recompute + lost-update race → 1,049 dangling rows, no locks; ④ router pins never wired; ⑤ shadertoy→RIB motion "no existence at all on disk."
- **Unproven then:** "no receipt yet of an inter-seat hint changing a target's course"; no closed gap→steer→seat loop; chain audited as Merkle-not-Verkle, ~17% rows → missing knot files.

## WHAT TONIGHT PROVED (label-honest)
- MEASURED: 99.6% cache-hit on warm frozen prefix (6848/6873 ×10 parallel calls, $0 marginal on Pro); probe spend $0.0057; D-lerp verification rows D=2→3, mismatches:0 (steer_exp_001_receipts.jsonl, 12 rows).
- MEASURED (billed control): cold billed lane cached_tokens=0 → full $0.075-in. Cache discipline IS the experiment.
- **UNVERIFIED (brief-level, not in receipts file):** "26/26 work items," "~60–80s latency." Flagged by digest child — must be re-anchored to receipts before HOT use.
- ESTIMATED: 12-seat board $0.01–0.03/hr; Pro fence 10–20 concurrent.
- PASSED-but-conditional: F1 3/3, F2 2/3 — PENDING OPERATOR CONFIRM as law.
- Exp 002: append-only event log + fold + nonce-gap replay protection PASSED; invariant root = hash-chain (audit says Merkle, not true Verkle).

## THE DELTA (the finding)
Steering never failed as an idea. It failed as **physics**: every steer cost a cold, full-context, browser-mediated round-trip. Tonight killed both costs:
1. **Frozen-prefix discipline** — a steer is ~100 delta tokens riding a 99.6% cache hit ≈ $0.
2. **File-bus surface** — steers.jsonl replaced the browser; playwright/CDP dependency deleted.
3. **Tip-hash state** — dumb seat verifies one sha256 against the root, never reads the chain (fixes the O(n²)/race dormancy cause).
No new organs. The revival is three cheap primitives wired onto organs that already existed since 08-08.

## IMPLICATIONS
1. **Dormancy was a cost bug, not a concept bug.** The graveyard (seat_steer×84, steer_compare×40, gap_swarm) is a feature backlog keyed to cost curves. Tonight's primitives reactivate all of it without new code. Doctrine: re-audit dormant organs when a primitive gets $0-cheaper.
2. **The stack has an actuator for the first time.** Sensors (harvest/archivist/gap_map) existed; memory (RIB) existed; laws existed. Nothing could move a seat in real time. gap_map → steer line → Tail lerp → event-log receipt closes the 08-10 loop: research output becomes fleet motion, not operator digests.
3. **Intelligence becomes a steering service, not a purchase.** Brain 10% / Hands 70% slot law + $0 delta-token hints ⇒ buy judgment, route labor at $0. If model-differential steering (agenda #2) confirms, scaling N is a cache problem, not a budget problem. STRUCTURE-OVER-ACQUISITION becomes arithmetic.
4. **The verification spine went load-bearing.** Append-only fold + invariant root (old proofs survive appends, consumer verifies from tip+proof) is Verkle/RIB running in production — and it fixed the exact races that dormed the original. Routing is commodity; steering + hash-anchored state is not. Agenda #1 (true KZG, gate = path size + update cost vs hash-chain) is now the keystone upgrade, not polish.
5. **Speed opens a safety gap at the same time.** A $0 swarm moving in <2 min can outrun oversight. SWITCHBOARD LAW is the guardrail: a steer is a proposal, never a permission. Before any scale-up (bond ceiling agenda #7, 32×32), CLASSIFY→AUTHORIZE must gate the steer write path. Jury clauses are load-bearing: abort/permission tokens front-loaded, never tail-only; full artifacts in immutable sha256 store.
6. **Honest posture:** we proved *a* steering loop at ~$0 — not *the* swarm. Receipts re-anchor (latency, 26/26), board-scale cache measure, and dumb-seat obedience (steer heartbeat) are the credibility debt.

## NEXT SMALLEST (priority order per brief)
1. Re-anchor brief-level exp 001 claims to receipts or mark UNVERIFIED on the brief.
2. Agenda #2 model-differential (glm-5.3-flash high steering DS-flash).
3. Agenda #4 gap→steer loop (archivist gaps become steer lines).
4. Agenda #7 bond ceiling BEFORE any swarm wiring beyond the Pro fence.
