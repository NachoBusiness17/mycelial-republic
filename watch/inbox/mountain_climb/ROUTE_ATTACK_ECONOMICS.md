# ROUTE ATTACK: ECONOMICS + ATTENTION (Phase 1, free lens #2)

Date: 2026-09-30 · Owner seat: this lane (file ownership per dispatch) · Target: `ROUTE_V0.md` · No commit.
Inputs read: `ROUTE_V0.md`, `watch/inbox/last_mile_20260930/IMP5_COST.md`, `watch/inbox/last_mile_20260930/AH_REFIRE_QUEUE.md` (window laws), plus byte-grounding from `LW2_ADAM_INVITE.md`, `AJ9_NOUS_402.md`, `IMP8_REPLICATION_RUN.md` (all same directory). Em-dash count: 0.

Ground truths used (all 2026-09-30 bytes):
- **G1 wall:** 20-wide operator-ordered fire died wholesale at `[1308] Usage limit reached for 5 hour`; 13 AH lanes + AE7 dead (most "not started"), zero landed; refire law 6-8 staggered, clean shape 10-12; operator drops (AI1-AI7) queue AHEAD of repairs; MC lanes fire after MC1-3 (`AH_REFIRE_QUEUE.md`).
- **G2 cost:** grand $135.7095 / 25,376 calls; trailing week 0 / 0 / 0.8777 / 0.3448 / 0 / 1.9245 / 6.0712, so 09-30 alone is ~66% of the week. Dollars are trivial; the scarce currencies are account quota and operator attention (`IMP5_COST.md`).
- **G3 RAM:** 64 GB shared box; the fp32 replication run gated on >=38 GB free while free read 27-31 GB; 9 orphaned pytest zombies cleared; launch deferred ~40 min; law "never swap the estate" (`IMP8_REPLICATION_RUN.md`).
- **G4 Adam:** invite NOT SENT; no GitHub username for Adam exists in the estate (both handle guesses 404); the fix is the operator asking Adam on Discord (`LW2_ADAM_INVITE.md`).
- **G5 Nous:** prime models (the driving ladder's workhorse+judgment tier) 402 on reservation; cheap lane alive; fix is operator-only portal check/top-up, no API balance endpoint (`AJ9_NOUS_402.md`).

---

## F1. Lane-day estimates hide two measured multipliers: wall-death refire and the RAM gate

**SEVERITY: HIGH · CONFIDENCE: HIGH · NOT-UNDERMINED: only if the 1308 wall proves rare at widths <=10 (AH bytes show the 5h limit is account-level, hit at one bad burst, and the operator's burst reflex is the documented failure mode, so recurrence at sustained width is the live risk).**

Per-pitch magnitudes (P2 1-2, P3 3-5, P4 4-6 lane-days) are honest as relative effort. The unit is not: a "lane-day" assumes one focused window of clean runtime. Two multipliers from today's bytes:

1. **Wall-death multiplier.** A lane that dies at the 5h wall does not resume; it refires at queue-back, behind the operator's next drop (G1 refire law: drops first, repairs second). Expected cost per lane = estimate x P(wall death) x queue delay. G1 measured P(wall death) > 0 at one operator burst, and ROUTE_V0's own risk-2 names the burst reflex as the estate's failure mode. The route's totals ("12-16 serial + 8-10 parallel lane-days; 4-6 focused windows") divide to 4-5.2 lane-days per window, i.e., every lane runs clean every window. G1's window produced 14 dead, 0 landed. One burned window = 17-25% of the route's entire window budget.
2. **RAM-gate multiplier.** Any local-test-heavy pitch (P3 export CI, P4 replay verification, P7 worldgen hashes) queues behind the fleet on the shared 64 GB box (G3): launch deferred, never swapped. P4's deepest-unknown estimate (4-6) prices design risk but prices zero queue time.

Also P4's falsifier ("two clients on two DIFFERENT physical machines") is an operator-hands dependency (second machine) disguised as a technical gate.

## F2. The route's tail serializes on the operator more than it admits; one gate is already proven blocked

**SEVERITY: HIGH · CONFIDENCE: HIGH (byte-backed) · NOT-UNDERMINED: if the operator pre-answers the three gates this week (Discord ask, portal top-up, Phase-2 GO word), the serialization collapses to a single digest row; until then the bytes say blocked.**

- P6's "human calendar" gate is actually operator -> Discord -> Adam -> GitHub (G4). The estate already burned a full lane (LW2) to discover it cannot proceed without operator hands. The 72h fallback clock starts at artifact-ready, but the PRIMARY path is stalled today on a question only the operator can ask.
- P8/Phase 2 needs operator GO ($5 cap) and, per G5, a portal top-up the route never lists as a gate. The "funded tier reserved for verification and the P8 ask" is 402-dry on prime models NOW, so every verification climb is parked on an operator portal visit.
- Window content is operator-scheduled (drop-first law, G1): the operator is the dispatcher, so his steering bandwidth, not lane width, is the route's true critical path. The route prices lanes; it does not price his attention. Expected outcome without change: more lanes spent rediscovering operator-gates (the LW2 pattern).

## F3. Quota-economics: "local/free-lane by design" is true of compute, false of quota; the route assumes a machine that does not exist

**SEVERITY: HIGH · CONFIDENCE: MEDIUM-HIGH · NOT-UNDERMINED: the weekly-reset half of the mission brief found no byte this session (flagged unverified); if Task-agent lanes are later shown to ride a budget separate from the 1308 wall, the width half weakens, though AH's same-session lane deaths argue against it.**

- The spine's lanes are ZCode Task agents on this same 1308-walled account (G1). "Local" work still spends account quota. Only mates (opencode) and stealth are separate-budget.
- Usable windows: the 5h wall caps active burn; the refire law adds "never fire into a closed window." Net: the route's 4-6 clean windows must also absorb the AI-drop queue, the 14-lane AH refire backlog, and standing metabolism. ROUTE_V0 prices none of its queue position.
- The cost trend (G2) shows acceleration (66% of weekly spend on 09-30) with trivial dollars: the binding constraint is quota walls, which the route mentions only as risk-2 attention sprawl, not as route arithmetic.

## F4. The operator-burnout early warning is decorative as instrumented, and blind in one direction

**SEVERITY: MEDIUM · CONFIDENCE: HIGH (instrument absence); MEDIUM (direction claim) · NOT-UNDERMINED: if a standing patrol already polls operator word-gap / digest answers / D-owes growth, this retracts; none was found in the cited surfaces.**

The signal (risk-5) detects WITHDRAWAL: 48h of no GO/STEER, unanswered digest, growing D-owes. Today's bytes show the opposite mode: OVERDRIVE (operator ordered a 20-wide window-burn while 14 lanes sat dead, then dropped a fresh 7-lane research wave). The 09-27 fear moment followed by 09-30 escalation is an overpresence trajectory this ledger cannot see. Worse, no instrument owns it: no tool polls the word-gap, no meter counts D-owes; it is a clause, not a check. Half-real: the belay-point mitigation genuinely exists in the pitch design.

## F5. What to CUT to make the week survivable

**SEVERITY: recommendation · CONFIDENCE: MEDIUM-HIGH · NOT-UNDERMINED: any cut gets re-earned by B4's missing-list screaming for it (the route's own falsifiability).**

1. **Cut P1** to opportunistic-only. Its own attack surface concedes no pitch consumes a mate output; route evidence agrees (G1: mates are a separate budget and broken at auth).
2. **Cut P7's "start mid-P4":** defer wholly behind P6. The route itself flags the ordering as falsifiable; starting it mid-P4 is polishing before the stranger speaks.
3. **Cut P5's GPS live-flip:** at 1 event/day the route's own attack line calls live routing premature theater. Keep the append-only JSONL round.
4. **Downgrade P4's falsifier** to one physical machine plus one CI/VM runner (removes an operator-hands dependency from the deepest pitch).
5. **Add an operator-queue card:** one digest row naming the three open operator gates (Adam Discord ask, Nous portal top-up, Phase-2 GO). Price attention upfront instead of spending lanes to rediscover it (the LW2 pattern).

## Verdict

ROUTE_V0's pitch-level engineering is honest; its ECONOMICS assume a machine the 09-30 bytes disprove: clean windows, quota-free "local" lanes, a funded tier that is currently 402-dry, and a stranger reachable only through the operator. Fix F1-F3 arithmetic, instrument or redirect F4, take the F5 cuts, and the 4-6 window claim becomes defensible; unchanged, the week's real shape is: 2-3 wall-capped windows/day, shared with a 20-lane backlog, tail-gated on three operator actions.

**Filing:** amendment receipt per ROUTE_V0 section 6; register in `watch/inbox/index_events.jsonl` (INDEX lane owns the inventory table). No commit.
