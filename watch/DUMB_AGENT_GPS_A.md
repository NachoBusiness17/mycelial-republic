# DUMB-AGENT GPS — Lane A (OpenClaw corpus self-steal)
2026-09-01 · MINED (bounded). Catalog of implicit navigation primitives for flash-tier agents (know
where you are / where to go / stay on course WITHOUT expensive reasoning). Verified=receipted · vibe=estimate.

## PART A — IMPLICIT PRIMITIVES WE BUILT WITHOUT NAMING (17)
Axes: T=task-position · Q=depth · D=direction · R=resource.

| Primitive | Navigates | File pointer |
|---|---|---|
| 1 D-lerp depth param D=2→3 | Q | STEERING_JET_PHASE "discrete phase steps"; SWARM_STEERING "D-lerp... mismatches:0" |
| 2 RIB depth-motion `{param:depth,range,rate,ttl}` | Q continuous | STEERING_SYNTHESIS §1/§3/§7 |
| 3 One-step climbs R0–R6 w/ halt criteria | T | BASECAMP_REMAP §5 |
| 4 ask_router outcome-memory routing | T | AUDIT_D_MAP (MEM:33); MOONSHOT_CHARTER M1 |
| 5 Atlas byte-span/vertex map | T where-am-I | MOONSHOT_CHARTER M4/M5; MODEL_KEY_ATLAS |
| 6 RIB deref `<path>:a-b`+sha256, label-immunity | T+pointing | riddler_common 00:06/00:38Z |
| 7 Hash-anchored waypoints (verkle tip `2670c…`) | D fresh/fork-safe | STEERING_SYNTHESIS §2; AUDIT_C 6311/6311 |
| 8 Water gates/levels (off-peak/isolation/family/wall/…) | R | WATER_NETWORK_SPEC "THE GATES" |
| 9 Flock signals: paste.rs + ntfy rib-bus | D who's alive | HANDOFF_0600Z §4 |
| 10 Trajectory tape "Ledger of Empty Chairs" | D history | riddler_common 11:09Z |
| 11 Decode-gated riddles (4/4, traps passed) | D pub markers | riddler_common 11:08Z |
| 12 F2 compact handoff (sha256+3-line delta) | T cheap point | STEERING_SYNTHESIS §0/§1 |
| 13 WARM_PACK spine L0/L1/L2 (2.9KB) | T start pos | riddler_common 00:50Z |
| 14 Ractor 3-line epilogue | D turn handoff | riddler_common 12:12Z |
| 15 Elder evidence ladder DECLARED→LIVE→GHOST | T status | FLEET_AUDIT evidence ladder |
| 16 steers.jsonl claim-before-act queue | T queue pos | STEERING_SYNTHESIS §1 |
| 17 INDEX.json hash-fold (append-only + replay) | T receipts map | HANDOFF_0600Z §1 EXP-002 |

**DUMB-agent fit:** YES-#1,2,6,7,8,9,12,13,16,17 (cheap, no reasoning). PARTIAL-#3/15 (halt/ladder
must be pre-written in seat prompt), #5 (expert-maintained), #10/11/14 (smart-produced, dumb-consumed).
NEEDS SMART:#4 (follows once row exists), #10/14 writing.

## PART B — GAPS (complete dumb-GPS needs, we hold NOTHING)
- **G1 no dumb→dumb routing** — all direction is smart→dumb one-way (#16); no peer lookup beyond hand atlas.
- **G2 no self-locate-on-cold** — atlas/ladder describe *orgs*, not "given this task, what rung am I now?";
  one-step climb (#3) is expert-authored per shift.
- **G3 escalation=gap→steer gate designed 08-10, NEVER CLOSED** (SWARM_STEERING "loop that never closed").
- **G4 obedience unenforced&unmeasurable** — silent miss if a seat ignores a steer; "steer heartbeat" proposed, not built (STEERING_SYNTHESIS §8.6).
- **G5 no meter-grade self-check** — SALON Ellul: no gate fires on a meter it can't read; free-tier meters polled/self-derived.
- **G6 chain is Merkle NOT Verkle** — SHA-256-only trust; true KZG is the "keystone upgrade," unowned (AUDIT_C; SWARM_STEERING).

## PART C — VERIFIED vs VIBE
**VERIFIED (receipts):** D-lerp 12 rows D=2→3 mismatches:0 (steer_exp_001_receipts.jsonl) · cache-hit
99.6% Pro/99.7% zai/100% Together · steering-through-cache 4/4 @570ms (W4) · cache law r=0.214 H=1.0
(78.6% vs 79.3%) · verkle 6311/6311 0-orphan · F1 3/3,F2 2/3 PENDING operator · EXP-002 fold PASS.
**VIBE/flagged:** "D-lerp 26/26"+"60–80s latency" brief-level ONLY, flagged not-in-receipts (SWARM_STEERING
"UNVERIFIED brief-level") · 12-seat $0.01–0.03/hr ESTIMATED · shadertoy→RIB "no existence on disk" ·
dumb-obedience / escalation-loop / true-verkle NEVER proven (G3/G4/G6).

## FINISH
17 primitives · 6 gaps. Next-lane spec: one missing connector — **cold-start self-locate** (fingerprint
BOM→compute elder-ladder rung) which unblocks G1/G2/G4 in one small shape.
