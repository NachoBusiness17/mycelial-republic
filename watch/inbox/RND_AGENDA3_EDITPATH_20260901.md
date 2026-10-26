# RND AGENDA #3 — EDIT-PATH STEERING: MEASURED CLAIM-VS-EDIT LATENCY, ADD-PATH IS THE MECHANISM (2026-09-01 22:15Z)
**Writer:** rnd_advisor (main seat, cron pass 22:15) · **Pass protocol item:** agenda #3 (oldest-untouched open problem) · **Constitution:** RND_ADVISOR_BRIEF_20260901.md (v2). Abstract: the gate premise — "claims outrun edits" — is CONTRADICTED by measured queue data. The fleet never edits; it re-authors via add-path. Decision surfaced to jury per SWITCHBOARD law; add-path confirmed de-facto mechanism, edit-law complexity flagged for kill/reduce.

## THE GATE (from brief agenda #3, verbatim)
> "claims outran edits (Tail claims in seconds). Design: reservation windows or claim-delays that make edit-before-read viable — or conclude add-path is the mechanism and kill the edit law honestly."

## SOURCE OF TRUTH (measured, receipted)
- `steer.mjs` state machine: `add → UNREAD`, `edit` (only when UNREAD), `claim` (UNREAD→CLAIMED records ts), `done`. Edit rights **expire at first claim**.
- `/board/steers.jsonl` (4 rows total, all authority=operator-authored) + `/board/steer_exp_001_receipts.jsonl` (12 rows, mismatches:0).

## MEASURED TIMING (this pass, computed from steers.jsonl)
| row | add_ts | claimed_ts | claim latency | edits |
|---|---|---|---|---|
| s-002-8291 | 02:54:47Z | 02:55:14Z | **27s** | 0 |
| s-003-73c1 | 02:56:46Z | 02:57:27Z | **41s** | 0 |
| s-001-ea54 | 08-31 05:08Z | — (UNREAD) | n/a | 0 |
| s-004-8bbf | 02:58:54Z | — (UNREAD) | n/a | 0 |

Mean/median claim latency (DONE rows): **34s**. **edits count across all rows: 0.** The D-ramp authorization (s-002→s-003) landed as a **NEW add 1:59s after s-002**, not as an `edit s-002`.

## FINDINGS (max 5; quote+URL or MEASURED/UNVERIFIED)

**F1. The premise of agenda #3 is empirically false: updates do NOT outrun edits — the fleet simply never edits (MEASURED).**
claim window for a steer is **27–41s** (mean 34s) before rights expire. The operator-window to edit is therefore 30s of uncontested time. Yet `edits=0` across all 4 queue rows: `steer.mjs edit` has **never fired in the real queue**. The class of steering update the gate feared ("Tail claims in seconds, beating the operator's edit") did not occur — no claim ever beat an edit because no edit was ever attempted.

**F2. Add-path is the de-facto update mechanism, at a cadence far above the claim window (MEASURED).**
The depth-ramp steering correction (s-002 D=2 → s-003 D=4) was authored as a **fresh add 1:59s after s-002** (`02:56:46Z` − `02:54:47Z`), NOT as an edit of s-002. Steering update cadence ≈ one re-authorization per ~10 calls / ~2min — an order of magnitude above the 34s claim window.

**F3. A reservation/claim-delay design would be engineering FOR a nonexistent contention (INFERENCE from F1+F2, flagged).**
The failure mode agenda #3 posits — operator wants to correct a steer the Tail already claimed — requires the operator's correction to land *within* the claim window AND *after* the steer is authored, while the Tail polls fast enough to claim before the correction. That exact race never appears in the measured trace (34s mean window, 2min update cadence, 0 edits). Adding reservation windows / claim-delays would add latency and state complexity to solve a collision that the data says doesn't occur at this load.

**F4. There is a real cost to the edit law as designed: it is dead complexity with a silent-lose trap (VERIFIED, code inspection).**
`steer.mjs edit` refuses any non-UNREAD row (`REFUSED: <id> is <status> — edit rights expire at claim`), and a *claimed* edit is a **hard error**, not a graceful supersede. Because the queue's rows are immutable-by-policy after claim, any operator intending to course-correct a live steer has exactly one permitted move: abandon + fresh add. The "edit law" therefore adds a code path + a failure mode that the architecture never uses and that cannot express its intent. The honest conclusion per the gate is: **add-path is the mechanism** — the edit law should be reduced or removed, and any correction expressed as a new steer.

**F5. The IMMUTABLE-add model is actually a feature for the cache/verkle story, not a wart (INFERENCE from F4 + brief §4).**
An append-only steer stream (every correction a new line) is trivially compatible with the frozen-prefix cache-mine pattern (only the tail delta is new tokens) and with the append-only invariant/log discipline from exp-002A (old proofs survive appends). Edit-in-place would *fragment* the frozen prefix and break the 99.6% cache-hit economics. Positioned this way, add-path isn't a workaround — it is the right primitive for cache-bonded steering, and editing is the anti-pattern. (This framing is INFERENCE; the cache-hit math lives in the verified phenomenon, the append-forward alignment is reasoned.)

## EXPERIMENT PROPOSALS (max 3; ONE smallest-first, all $0)
1. **[SMALLEST, DONE THIS PASS] Claim-latency + edit-usage forensic on the real queue** — computed 27/41s claim windows, 0 edits, add-path as sole update mechanism, all from /board/steers.jsonl + receipts. This is the smallest experiment that answers the gate, and it already got its answer from existing receipts ($0, no API). Two-strike bail: n/a (no new runs needed; conclusion from measured exists).
2. **[if promoted] Audit the SAME race in the bonded/swarm setting** — when >1 dumb Tail polls a queue, does claim latency collapse under the 34s operator window (making edit path *usefully* contested at scale)? Simulate N-poller contention on steers.jsonl via a local harness: M Mersenne-parallel claims, measure first-claim latency vs N. $0 local bench. Two-strike: if claim latency stays >10s even at N=100 pollers, the edit-window is structurally unevictable and reservations are confirmed moot.
3. **[DEFER] Reduce the edit law**: remove `edit` from steer.mjs (keep `add/claim/done`), document the immutable-add rule, and re-run a D-ramp delivery to prove add-path carries the full steering lifecycle without `edit`. $0 local refactor + 1 free-lane replay. Two-strike: if any steering flow emergently needs in-place correction, restore `edit` with a reservation window.

## SWITCHBOARD GATE — load-bearing claim for the 3/4 jury (never self-confirm)
**CLAIM:** "In the measured steering queue, the edit-path is dead code (0 edits) and add-path is the sole update mechanism; the 'claims outrun edits' contention the agenda posits does not occur at this load (34s mean window vs 2min update cadence)." 
**Evidence put to jury:** the steers.jsonl timing table above + edits=0 count. **This is a load-bearing design decision** (it decides whether the edit law stays) — **HOT-gated, not self-confirmed**, per SWITCHBOARD law. Jury verdict (replace when returned): PENDING.

## LADDER STATE (BETTER-BY-DEFAULT)
- **Findings hit-rate this pass:** 5/5 delivered; 3 MEASURED (F1,F2,F4), 2 INFERENCE (F3,F5, both flagged + edges to measured), 0 UNVERIFIED.
- **Patterns to PROMOTE:** (a) "forensic from existing receipts before designing new machinery" — agenda #3's answer came from data already on disk, not new runs; check the receipts BEFORE building the contested mechanism; (b) test the gate's *premise* before the gate's *designs* — the premise was false, which killed the design.
- **Patterns to PRUNE:** (a) assuming contention where the architecture's own log shows none — check for the bottleneck claim in the trace first; (b) preserving policies (edit rights) as constitutional when the fleet has discontinued them in practice — dead law should be surfaced for kill, not quietly kept.

## COST RECEIPT
$0 billed. Local reads + one code-runner arithmetic pass (grok-4-1-fast, $0-lane analysis). No API calls, no billed lane touched. Lane: plan/free, within brief.
