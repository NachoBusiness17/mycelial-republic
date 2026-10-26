# SELF STEAL — TRAJECTORY_STEP, SPINE BUILD #1 LANDED (Sep 5, 2026)

*Operator: "Build then dogfood/self steal." The tesuji is built: every Bash call in the
harness now seals a TrajectoryStep — schema trajectory_step.v1, step_hash integrity,
append-only. The base is frozen. The vertical's clock runs.*

## WHAT SHIPPED (same turn, $0, all local)
- **mag/trajectory_step.py** — `hook` (stdin event → sealed row), `verify` (recompute every
  step_hash; 2/2 hash-clean at birth), `stats` (total / today-UTC / pace against 100/day),
  `test-reject` (the falsifier as a verb: **PASS — schemaless write REFUSED**).
- **PostToolUse hook wired** in ~/.zcode/cli/config.json (matcher Bash; backup
  config.json.bak-pre-trajectory-20260905; one-block revert if the steer_47 console-flash
  class recurs — scar noted in the config note key).
- Stream: **memory/trajectory/steps.jsonl** — louver law holds: the cage keeps payloads,
  boards show counts.

**Honest edge:** hooks load at session start, so new windows inherit the stream; THIS
window's remaining calls predate the arm. The vertical's true step-1 is the next window's
first command — probably tonight's 23:00 night shift, which means the watch seals the first
organic steps while he sleeps.

## THE LINEAGE (seven waves, one row)
1. **The vendor envelope (this morning, 11:3xZ):** z.ai's own Trajectory export — input /
   tool-result / output channels, 24-hex step hash, timing. We adopted the shape at our
   scale: 16-hex step_hash, the three faces, timing in ts.
2. **The rib salon fold law:** "schema_version MANDATORY (drift killer)" — implemented as a
   REJECT at write time, not a convention. Enforced structure, not prose (architecture-is-law).
3. **The chain's hash discipline:** leaf_hash → step_hash. Append-only jsonl, the same medium
   as room.jsonl and verkle_chain.jsonl — one record grammar, three layers (command / room /
   day).
4. **The song (magatama edition):** "Every day I file becomes a bead on the chain" + "freeze
   the base, let the workers report the drift." The tesuji is a lyric with a schema now.
5. **The thought-bank's 9,305 orphans:** blobs without chains — the orphan class the T1
   rejoiner was chartered to heal. The wrapper is prevention at birth: every future step is
   born hashed, sessioned, and schemaed. No new orphans, ever.
6. **The standing-wave miner:** frozen prefix + append-only turns — the cache law applied to
   the record layer. The wave mines; the stream freezes.
7. **Lensing (today, an hour ago):** the stream is the deterministic render of stochastic
   work — the base frozen so the lens has something to lens. Pre-climb route cards will read
   this stream.

## DOGFOOD RECEIPT (at the bytes, 17:07–17:1xZ)
- Unit: manual event → row `d9ab9831b1f9e386 $ echo pre-flight` — hash-clean 1/1.
- Falsifier SCHEMA: **PASS** — `SCHEMA REJECT: row without schema_version (drift killer)`.
- Verify: **2/2 hash-clean** after the second seeded row. Stream 556 B at birth.
- Coverage (standing): next window's first Bash call must land a row, or the wrapper is dead.
  Check is one command: `python -m mag.trajectory_step stats`.

## THE RULE GOING FORWARD
The Sep-20 vertical (100 sealed steps/day) is no longer a promise — it is a counter that
starts at every window boot. Boards and salons may READ the stream; nothing may rewrite it.
The next arc's asks continue the spine card (TRAJECTORY_LENS_20260905.md) — never siblings.
