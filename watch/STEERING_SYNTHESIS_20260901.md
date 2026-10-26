# STEERING_SYNTHESIS — Design for a real-time multi-model steering revival
Date: 2026-09-01T02:37Z · Author: subagent, lane B (design forward, no archive archaeology)
Reader: operator / lane wiring / basecamp · Class: PROPOSAL

Context: this revives the operator's 02:33Z idea that dormed. Tonight's measured
physics (SWARM_DOCTRINE Pro-lane 99.6% cache hit at $0 marginal; OPS_RESEARCH F1
frozen-prefix + F2 compact-handoff, both jury-passed) unblocked it. This is the
design. No novel, all receipts+arithmetic.

---

## 0. Why it dormed, and what unblocked it

The idea was: models on a 4chan-style board steering each other — hints on where
to look and why, gap analysis steered into prompts, shared invariants built on
the fly, smart→dumb direction, shadertoy-motion→RIB. It dormed because every one
of those features costs *a live round-trip per steer per seat*, and round-trips
on a cold/billed lane are the exact thing tonight's physics kills:

- **The Pro lane measures 99.6% cache-hit on a warm frozen prefix at $0 marginal**
  (SWARM_DOCTRINE §3). A steering message appended to a *frozen shared tail*
  rides that hit — the steer is essentially free.
- **F2 compact-handoff (sha256-pointer + 3-line delta, 2/3 ADOPT)** is *exactly*
  the shape a steer needs: a steer is a delta on a frozen context. It was already
  jury-passed as a *handoff* contract — this design reuses it as a *steering*
  contract.
- **F1 frozen-prefix (3/3 ADOPT)** means the steer's surrounding prompt never
  churns; only the delta tail changes per steer, so the cache stays astronomically
  hot.

So the revival is not "build new organs" — it is "the existing organs already
obey the cost law; the missing piece is one thin connector that turns a steer
into a frozen-prefix delta." The rest is wiring existing seats to an existing
surface (room.jsonl is already a live chat surface; steers.jsonl already an
edit-before-read queue; the verkle chain is already a tamper-evident tip).

---

## 1. Answer to design question — REAL-TIME HINT DROPPING

**Surface:** reuse `/board/room.jsonl` + Mag room API as the *shared* steering
surface (it is already a live multi-seat chat stream), and `/board/steers.jsonl`
+ `steer.mjs` as the *queue with edit-before-read semantics* (the operator's law).
The board is the firehose (read-only, post-once); the queue is the actionable
subset (claim-before-act). Smart seats post to both; dumb seats only poll the
queue.

**Message shape** (one JSON line on the queue; a post on the board is a humanized
rendering of the same object). The operator's sketch `{target_seat, where, why,
ttl, sha256-anchored-to-verkle-tip}` is correct — keep it verbatim as the core,
and add the two fields that make it cheap to consume (a) and safe to trust (b):

```json
{
  "hint_id": "h-031-ab12",
  "kind": "hint",
  "target_seat": "hands-a",
  "where": "/board/EconomistSpendAudit... line 22 | fetch :2608.19 case-3",
  "why": "gap: 8 leads classified but 0 harvested; steer depth up, breadth down",
  "ttl": 900,
  "anchor": "2670c7ea555c",          // verkle tip root prefix (chain-addressable)
  "delta": "+breadth -depth +temp0.1", // shadertoy-style motion (see Q4)
  "claims_until": 26-lines-back-seat-context
}
```

Laws that keep it cheap and safe:

1. **Frozen system/tool/catalog prefix** on every destination seat — the hint is
   appended to the volatile tail, so 99.6% of the prompt is cache-hit and only
   ~60–120 tokens (the hint line) re-render. This is F1 applied to steering.
2. **The hint is itself a compact handoff (F2)**: `where` is up to a 3-line delta
   + an anchor, never a full artifact. A hint that points is cheap; a hint that
   *attaches* a full doc is a bug.
3. **`anchor`** is the verkle tip root prefix (today `2670c7ea555c`, tip index
   6311). A dumb seat may safely ignore a hint whose anchor is older than the tip
   it last saw — the steering surface is fork-safe against stale racers.
4. **Post-once, claim-in-queue**: the board is append-only firehose; `steers.jsonl`
   carries the claimable copy. `steer.mjs` already enforces edit-before-read and
   claim-before-act — a dumb seat does `node steer.mjs claim <id> <seat>`.

Direction of the firehose vs queue: **smart posts hint → dumb polls hint → dumb
claims (queue) → dumb acts → dumb posts receipt**. The receipt rides back on the
same cheap lane as a delta (cache stays hot because the prefix is frozen and the
receipt is tail-only).

---

## 2. Answer to design question — SHARED INVARIANTS ON THE FLY

**Problem:** multiple models propose rules "all lanes must hold"; a dumb model
must consume an invariant without reading the whole chain.

**Answer (the operator's own hint, confirmed):** *the invariant IS a compact
handoff*. The invariant is NOT a document — it is **one machine-readable line,
sha256-tied to the verkle tip at the moment of proposal**. A dumb seat never reads
the chain; it reads the current tip root (one tiny `verkle_tip.json` read, already
maintained by `verkle_lance.py`) and compares it against the invariant's anchor.

Invariant line (a 3-line delta by construction, F2):

```json
{
  "inv_id": "i-044-c01",
  "kind": "invariant",
  "rule": "all lanes: fetch→extract must give the cited URL or abstain",
  "anchor": "2670c7ea555c",          // tip root when proposed
  "proposer": "brain-a",
  "status": "proposed|passed|active|stale",
  "ttl": 3600
}
```

**How a dumb seat consumes it (no full-chain read):**
1. Read current tip root (`verkle_tip.json`, bytes, cheap).
2. If `i.anchor == tip`: invariant is current — obey it. No chain read needed.
3. If tip advanced past `i.anchor` and the invariant is `active`, the seat may
   still obey it (the invariant is *immutable* once `active` — the anchor is a
   snapshot, not a moving pin), OR wait for Brain to re-anchor a renewal.
4. If `i.anchor` is *older* than the tip and status is `stale`/`rejected` → drop.

**Why this is safe:** `verkle_lance.py` verifies content-addressing and parent→prev
root chaining for all 6311 links (audit C: 6311/6311 chains intact, 0 orphans).
An invariant tied to a real tip root inherits the chain's integrity — it is
tamper-evident at the *anchor*, which is all a dumb seat needs, not the whole
history.

**Consensus-on-the-fly:** multiple seats proposing invariants is a *salon jury*
(SWARM_DOCTRINE's proven cross-family pattern) — 3-lane vote (DeepSeek/NVIDIA/zai
were today's working jury), 2/3 ADOPT = PASSED, exactly as HOT_JURY_F1F2 did at
$0 on the Pro lane. A proposed invariant that juries 2/3 is *tied into the chain*
via `verkle_lance link` (the event temporal tie-in tool, audit C §5):

```
# SUPERSEDED (FW-11 2026-09-28): one-shot verkle_lance link example, 2026-09-01. Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
python -m mag.verkle_lance link --event "invariant i-044 active" --when "<proposal ts>"
```

Consumption cost: one tip-root read + one hash comparison per seat — effectively
free, no chain read.

---

## 3. Answer to design question — SMART→DUMB DIRECTION

**Mechanism:** Brain slot writes directions into the shared steering queue;
Tail/Hands (the two largest call shares, ~70% + ~20% per lane-slot map) execute.
With cache discipline (F1 jury-passed), the *direction prefix stays frozen*. Only
the delta line (the direction body) changes per steer.

This is the key unlock: **a direction update is a frozen-prefix tail append**, so
it rides at cache-hit price on the Pro lane — which is **$0 marginal (plan-funded,
99.6% measured hit)**. On the *billed* DeepSeek Hands lane ($0.007 cache-hit/M),
a steering delta is also nearly free.

**Quantify — a steering update per N calls costs:**

Assume each direction-bearing call re-renders a ~100-token delta on top of a
~7,000-token frozen prefix (matching SWARM_DOCTRINE's measured probe shape).

| Lane | Marginal delta tokens/call | Rate on delta | Steering update per call |
|---|---|---|---|
| z.ai Pro 5.3-flash (cached) | 100 | $0 (plan-funded, 99.6% hit) | **$0** |
| deepseek-v4-flash billed, off-peak cache-hit | 100 | $0.007/M | **$0.0000007** |
| z.ai billed 5.3-flash (measured no-cache-billing) | 100 | $0.075/M (full input) | **$0.0000075** (if prefix somehow cold) |
| glm-4.7-flash (free tier) | 100 | $0 | **$0** |

So: **steering updates are effectively free on every lane that obeys F1** (Pro
$0, free flash $0, DS-flash cache-hit $0.0000007/call). The delta is 100 tokens;
the arithmetic below (§5) shows the full-board hourly cost resolves to *near-zero
on the bonded $0 lanes*. The only lane where a steer costs anything measurable is
a *cold-prefix billed* call, which is the tell to never cold-start a steering
prefix — establish it once, freeze it, ride the cache.

**Throughput bound is not dollars — it's the Pro concurrency fence (~10–20
parallel, SWARM_DOCTRINE §3).** Steering is low-frequency (each seat re-steers on
a beat, not per-call), so fence pressure is trivial; the board cadence (beats in
room.jsonl) already spaces this out.

---

## 4. Answer to design question — SHADERTOY-MOTION → RIB

**The metaphor, made literal:** steering is *continuous motion parameters*, not
discrete rewrites. Instead of a seat getting a "do X now" rewrite that restarts its
context, it gets a **RIB-style parameter line it lerps toward** over its next N
calls. The seat does not restart; it shifts its search-temperature, -depth,
-breadth, and focus-continuously, per call, toward the target.

This is the RIB idea already present (RIB = lossless spans; `verkle_rib` in the
catalog; MEMORY_RIB.jsonl exists). So a **steering RIB line is one row**:

```json
{
  "rib_id": "r-017",
  "param": "depth",       // or "breadth" | "temperature" | "focus"
  "range": "[-2,+4]",     // lossless span: lerp from current value to target
  "rate": 0.3,            // fraction of the span moved per call → smooth, not step
  "ttl": 1200,            // seconds this motion stays live
  "anchor": "2670c7ea555c"
}
```

**A dumb seat's consume loop (minimal viable):**
- On each call, read the live steering-rib rows for its `seat_role`.
- Pick the highest-priority param (e.g., `depth`).
- `current += (target - current) * rate`; emit the *current* value in that call's
  prompt head (which is at the tail of the frozen prefix, so it is cache-safe and
  only ~20 tokens).
- Lower `temperature` when depth is up; raise `breadth` when a `why` says the
  area is under-explored.

**Why this is RIB, not rewrite:** the motion is *lossless spans with a lerp rate*,
so a Brain seat can steer smoothly and a Tail seat can consume blindly without
ever re-reading context. It is exactly the "shadertoy motion → RIB file" the
operator described: continuous parameters over time, encoded as spans, played back
by lerping, not recomputed.

**Minimal viable version (MVP):** one param tracked — **depth** (or breadth) — on
two seats. That proves motion-based (not restart-based) steering fits the frozen
prefix. All six params can be the same code path (a param is just a scalar field in
the frozen tail); the MVP limits scope, not mechanism.

**Interaction rule:** if a Brain seat emits a *discrete* steer (kind `hint` or
`direction` with no lerp), that is a **priority override** that cancels the current
RIB motion for that seat — discrete rewrites are reserved for emergencies; the
default steering language is motion.

---

## 5. COST — $/hour for a live steering board

**Board spec (the operator's ask):** 5 steering seats (Brains) + 7 acting seats
(Tail/Hands), for one hour, on bonded $0-marginal lanes (z.ai Pro + glm-4.7-flash
free + DS-flash off-peak cache-hit).

**Basis:**
- Frozen-prefix discipline (F1) on every seat → dominant token mass is cache-hit.
- Pro lane 99.6% hit, plan-funded → $0 marginal (MEASURED).
- glm-4.7-flash free tier → $0 (DOCS).
- DS-flash off-peak, cache-hit → $0.007/M on the delta (~20–100 tokens/call).
- Steering is low-frequency: each Brain posts ~1 steer/beat; each acting seat runs
  ~a call per beat. Assume a conservative **1,200 calls/seat-hour spread of:
  5 Brain + 7 acting = 12 seats, ~100 calls each over the hour** (12,000 total
  calls; actual will be far lower on the board cadence).

Arithmetic per lane for the hour:

| Lane | Seats×calls | Frozen prefix | Delta/call | Cache-hit cost | IN cost | OUT | $/hr |
|---|---|---|---|---|---|---|---|
| z.ai Pro 5.3-flash (Brain ×5) | 5×100=500 | ~7,000 tok | ~200 tok | $0 (plan) | ~1M in @$0 | ~50K out @$0.25 | **$0.0125** |
| glm-4.7-flash (acting ×5) | 5×100=500 | ~4,000 tok | ~100 tok | $0 (free) | ~2M @$0 | ~50K @$0 | **$0** |
| DS-flash off-peak (acting ×2) | 2×100=200 | ~7,000 tok cache-hit | ~100 tok | 200×(200×$0.007/M)=... | see note | — | **$0.00003** |
| z.ai billed (spare, if Pro fence hit) | 0 (avoid) | — | — | cold = $0.075/in | — | — | **$0 (avoided)** |

DS-flash detail: 200 calls × 100 delta × $0.007/M = 200×100×7e-9 = **$0.00014**;
the frozen prefix rides cache-hit at effectively $0 marginal. Even if we count all
12,000 calls on DS-flash off-peak cache-hit, it is 12,000 × (100→200 delta) ×
$0.007/M ≈ **$0.02/hr**.

**TOTAL ≈ $0.01–$0.03/hr for a live 12-seat steering board** (12,000 calls), with
the Pro + free-flash share at $0.01 and the only non-negligible lane (DS-flash
billed) at ~$0.0002 if kept cache-hit, ~$0.02/hr worst-case if every call re-reads
delta. **The board runs for repeated hours for under a dime on the bonded $0
lanes** — it is cheaper per hour than the 8/31 overnight fleet, which already ran
under $1/day. Compare: a single cold billed 5.3-flash call is $0.000075; our
*whole live hour* is ~100–300 such cold-calls' worth. The Pro+free bonding is
what makes continuous live steering viable; the moment a lane goes cold-billed,
that seat's steers price up 100×, so the operator rule is **steer only on hot
frozen-prefix lanes; escalate, never run, a cold steer.**

Concurrency: 12 seats × their call frequency stays well under the ~10–20 Pro
fence when ceiling-sequenced (SWARM_DOCTRINE §3 degrades ~10–20 concurrent). At
1–2 concurrent across Brain seats and ~4–6 across acting seats, the fence is
untouched. If a 429 appears → redistribute to the free flash lane (pipe-bonding
already in SWARM_DOCTRINE).

---

## 6. WIRE-LIST — WHAT EXISTS vs WHAT TO BUILD

**Existing organs that compose (all already live / proven tonight):**

| Organ | Exists (path / evidence) | Role in the steering board |
|---|---|---|
| `room.jsonl` + Mag room API | /board/room.jsonl live stream | the shared chat surface / firehose |
| `steer.mjs` queue | /root/.openclaw/workspace/steer.mjs | edit-before-read + claim-before-act queue (operator law) |
| `steers.jsonl` | /board/steers.jsonl | queue storage (1 live steer row today; format proven) |
| `grok_steer` (grok_hook / grok_feed) | /board/grok_hook.py, grok_feed.jsonl | an existing steer-capable seat to reuse as a Brain |
| `verkle_lance` | /mag/mag/verkle_lance.py | chain store: anchor, `link` tie-in, tip read, integrity |
| `party_subchain` — NOT on this cage (`/mag/memory/runs/party_subchain*` absent) | ⚠️ does not exist | **do not build on it**; the verkle store lives at `/mag/memory/biography/` (audit C §0) — use that |
| salon chan / jury pattern | SALON_* receipts, HOT_JURY_F1F2 | cross-family invariant/hint consensus (2/3 ADOPT) |
| worker spawns | SWARM_DOCTRINE, lane scaffolds | the 5 Brain + 7 acting seats are existing lane seats, not new spawns |
| Lanes batch metadata | /mag/memory/runs/openclaw_catalog/latest.json | seat↔model↔slot routing (Tail/Hands/Brain) |
| RIB concept | /board/MEMORY_RIB.jsonl, verkle_rib | the motion/spans model for steering RIB lines |

**The single smallest missing connector:**

A **thin `steer_rib` reader/pruner** — a ~150-line script that (a) reads the
current live steering rows bound to a `seat_role`, (b) recomputes the lerped
`current` value for each motion param, and (c) emits that param block **at the
tail of the seat's frozen prompt** (so it is cache-safe and only ~20 tokens).
That is the bridle: it turns `steers.jsonl` entries and board posts into
`{param, range, rate, ttl, anchor}` rows a dumb seat consumes without reading the
chain, and it is hash-receipted back onto the queue so Smart sees the state.

Everything else — the board post formatter, the invariant tie-in via `verkle_lance
link`, the jury vote — is assembling already-proven organs. No new model, no new
store. **Build one connector, wire two seats, prove the loop.**

---

## 7. SMALLEST FIRST EXPERIMENT ($0 live demo)

**One 30-minute run, two seats, on the keep board, all on $0 lanes (z.ai Pro
5.3-flash + glm-4.7-flash free).**

- Seat 1 (Smart, Brain slot): post 5–10 steering hints to the board/queue —
  `where`+`why`+`anchor` to the verkle tip `2670c7ea…`, plus a RIB depth-motion
  (`{param:depth, range:[-1,+2], rate:0.3, ttl:900}`).
- Seat 2 (Dumb, Tail slot): poll the queue, claim each hint, and *lerp* its depth
  value per the RIB row for ~100 calls on the frozen prefix (the exact SWARM_DOCTRINE
  shape: ~7K input, ~100 delta).
- Receipt rows written to `steers.jsonl` (claim + done + the emitted per-call depth)
  and a `STEERING_DEMO_RECEIPT` row posted to the board.

**Success gate:** (a) Smart→Dumb hint consumed and claimed (queue states UNREAD→
CLAIMED→DONE), (b) Dumb's depth actually moved continuously across ~100 calls
(not a discrete jump), (c) **measured $ ≈ $0** on the Pro lane for the full 30 min,
and the tip anchor advanced correctly (`deepseek`/`grok_steer`/`verkle_lance` hooks
route naturally on this cage). 30 minutes ≈ 100–300 delta calls ≈ **$0–$0.001**.
Expected spend ≈ **$0.001**, well under any cap; serves as the live proof that
motion-steering rides the cache.

---

## 8. HONEST GAPS

1. **The Pro-lane cache-hit is MEASURED on a *probe* shape, not yet a 12-seat live
   board.** F1's frozen-prefix pass applies, but the 99.6% figure is from 10-parallel
   against one warm prefix (SWARM_DOCTRINE §3). A 12-seat board with 12 distinct
   frozen seats needs 12 hot prefixes established *once* each (worst cold ~24.5s +
   ~$0.075-in each). Cold-start cost is one-time; budget it.
2. **F2 compact-handoff is jury-passed (2/3) but PENDING OPERATOR CONFIRM**; the
   steer-as-delta contract inherits that pending status — it becomes law only on
   operator confirmation (HOT_JURY_F1F2 caveat lines).
3. **The `party_subchain` path cited in the task does not exist on this cage**
   (audit C: only `/mag/memory/biography/` verkle store). Any design that assumed
   `party_subchain` would silently wire to nothing. This design anchors to the real
   `biography/verkle_tip.json`.
4. **No Python on the subagent cage** — `python -m mag.verkle_lance link` /
   `self_check` must run from the host (`mag` venv), not the worker. The invariant
   tie-in step is therefore host-side, which is a real operational dependency for
   the demo receipt (the demo can skip the tie-in and still prove the loop).
5. **`ts` is write-time, not session-time** in the verkle store (audit C §2) — any
   receipt that dates by `ts` will be misleading; anchor by `index`/`filename`.
6. **Dumb-seat obedience is unenforced** — a Tail seat that ignores a hint produces
   no error, just a silent miss. The demo should count receipts (did it claim? did
   it lerp?) rather than assume obedience; a "steer heartbeat" (Brain re-anchors
   each beat) is the safety net.
7. **When NOT to steer (SWARM_DOCTRINE's tie-break):** escalation/verdict-shaped
   work still belongs on a warm single lane, never fanned. Steering is for
   *directing breadth/depth of parallel search*, not for synthesizing. Respect it
   or the board degenerates into N agreeing copies of one failure.

---

## FINISH

sha256 && copy to /board/inbox/ && INDEX.json item appended (below). All figures
receipted; no novel. The smallest experiment is §7 and can run today at ~$0.001.
